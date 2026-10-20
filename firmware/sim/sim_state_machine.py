#!/usr/bin/env python3
"""Host-side simulator for firmware/code.py — no hardware needed.

Stubs the CircuitPython modules (board, digitalio, neopixel, audio*, supervisor,
microcontroller, adafruit_ticks, gc, time.sleep) with a virtual clock and a
scripted motion sensor, then runs the real code.py and checks the state-machine
behaviour against the acceptance tests in 05_Firmware_Spec.md §10.

Run from the firmware/ folder:   python3 sim/sim_state_machine.py
"""
import sys, types, runpy, builtins, io, contextlib, re, os, pathlib

FIRMWARE_DIR = pathlib.Path(__file__).resolve().parent.parent
os.chdir(FIRMWARE_DIR)                      # so "sounds/..." resolves like on CIRCUITPY

SOUND_MS = 3450                             # length of teams_call_1ring.wav

class StopSim(BaseException):               # BaseException: not caught by code.py's `except Exception`
    pass

class World:
    def __init__(self, high_intervals_ms, end_ms):
        self.t = 0
        self.high = high_intervals_ms
        self.end = end_ms
        self.events = []                    # (t_ms, text)
        self.el_log = []                    # (t_ms, bool) EL pin transitions
        self.strip_max = 0                  # brightest strip value seen after warm-up
        self.voice_started = None
    def sensor_level(self):
        return any(a <= self.t < b for a, b in self.high)

W = None

# ---------------- stub modules ----------------
def make_stubs():
    m = {}
    sup = types.ModuleType("supervisor"); sup.runtime = types.SimpleNamespace(autoreload=True); m["supervisor"] = sup

    board = types.ModuleType("board")
    for name in ("EXTERNAL_POWER", "EXTERNAL_BUTTON", "EXTERNAL_SERVO", "EXTERNAL_NEOPIXELS",
                 "NEOPIXEL", "I2S_BIT_CLOCK", "I2S_WORD_SELECT", "I2S_DATA"):
        setattr(board, name, name)
    m["board"] = board

    dio = types.ModuleType("digitalio")
    dio.Direction = types.SimpleNamespace(INPUT="IN", OUTPUT="OUT")
    dio.Pull = types.SimpleNamespace(UP="UP", DOWN="DOWN")
    class DigitalInOut:
        def __init__(self, pin): self.pin = pin; self.direction = None; self.pull = None; self._v = False
        @property
        def value(self):
            if self.pin == "EXTERNAL_BUTTON": return W.sensor_level()
            return self._v
        @value.setter
        def value(self, v):
            if self.pin == "EXTERNAL_POWER" and self._v and not v:
                W.events.append((W.t, "VIOLATION external_power set LOW"))
            if self.pin == "EXTERNAL_SERVO" and bool(v) != bool(self._v):
                W.el_log.append((W.t, bool(v)))
            self._v = v
    dio.DigitalInOut = DigitalInOut; m["digitalio"] = dio

    npx = types.ModuleType("neopixel"); npx.GRB = "GRB"; npx.RGB = "RGB"
    class NeoPixel:
        def __init__(self, pin, n, brightness=1.0, auto_write=True, pixel_order=None):
            self.pin = pin; self.n = n; self.buf = [(0, 0, 0)] * n; self.shows = 0
        def __setitem__(self, i, c): self.buf[i] = tuple(c)
        def __getitem__(self, i): return self.buf[i]
        def show(self):
            self.shows += 1
            if self.pin == "EXTERNAL_NEOPIXELS":
                W.strip_max = max(W.strip_max, max(self.buf[0]))
    npx.NeoPixel = NeoPixel; m["neopixel"] = npx

    ac = types.ModuleType("audiocore")
    class WaveFile:
        def __init__(self, f): self.f = f
    ac.WaveFile = WaveFile; m["audiocore"] = ac

    am = types.ModuleType("audiomixer")
    class Voice:
        def __init__(self): self.level = 0.0; self._start = None
        def play(self, wave, loop=False):
            self._start = W.t; W.events.append((W.t, "PLAY"))
        @property
        def playing(self):
            return self._start is not None and (W.t - self._start) < SOUND_MS
    class Mixer:
        def __init__(self, voice_count=1, **kw): self.voice = [Voice() for _ in range(voice_count)]
    am.Mixer = Mixer; m["audiomixer"] = am

    ab = types.ModuleType("audiobusio")
    class I2SOut:
        def __init__(self, *a): pass
        def play(self, src): pass
    ab.I2SOut = I2SOut; m["audiobusio"] = ab

    mc = types.ModuleType("microcontroller")
    def reset(): raise StopSim("microcontroller.reset() called")
    mc.reset = reset; m["microcontroller"] = mc

    tk = types.ModuleType("adafruit_ticks")
    tk.ticks_ms = lambda: W.t
    tk.ticks_add = lambda a, b: a + b
    tk.ticks_diff = lambda a, b: a - b
    m["adafruit_ticks"] = tk

    gcm = types.ModuleType("gc"); gcm.mem_free = lambda: 123456; gcm.collect = lambda: None; m["gc"] = gcm

    tm = types.ModuleType("time")
    def sleep(s):
        W.t += int(round(s * 1000))
        if W.t >= W.end: raise StopSim("end of scenario")
    tm.sleep = sleep; tm.monotonic = lambda: W.t / 1000.0; m["time"] = tm
    return m

def run(high_intervals_ms, end_ms):
    global W
    W = World(high_intervals_ms, end_ms)
    saved = {k: sys.modules.get(k) for k in make_stubs()}
    sys.modules.update(make_stubs())
    real_print = builtins.print
    def tprint(*a, **k): W.events.append((W.t, " ".join(str(x) for x in a)))
    builtins.print = tprint
    try:
        runpy.run_path("code.py", run_name="__main__")
    except StopSim:
        pass
    finally:
        builtins.print = real_print
        for k, v in saved.items():
            if v is None: sys.modules.pop(k, None)
            else: sys.modules[k] = v
    return W

def triggers(w): return [t for t, e in w.events if e == "TRIGGER"]
def el_on(w):  return [t for t, v in w.el_log if v]
def el_off(w): return [t for t, v in w.el_log if not v]
def el_alternates(w):
    vals = [v for _, v in w.el_log]
    return all(vals[i] != vals[i+1] for i in range(len(vals)-1)) and (not vals or vals[0] is True)
def transitions(w): return [(t, e) for t, e in w.events if e.startswith("STATE ->")]
def violations(w): return [(t, e) for t, e in w.events if e.startswith("VIOLATION")]

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))

# ---- T1: no motion for 5 minutes -> WARMUP ends at 60 s, IDLE, zero triggers, strip dark
w = run([], 300_000)
tr = transitions(w)
check("T1 warm-up ends at ~60 s then IDLE", len(tr) >= 2 and tr[1][1] == "STATE -> IDLE" and 59_000 <= tr[1][0] <= 61_100, str(tr[:2]))
check("T1 zero triggers with no motion", len(triggers(w)) == 0, str(len(triggers(w))))
check("T1 strip stays dark (idle off)", w.strip_max == 0, f"max={w.strip_max}")
check("T1 EXTERNAL_POWER never set LOW", not violations(w), str(violations(w)))
check("EL: never energised with no motion (off through WARMUP+IDLE)", el_on(w) == [], str(w.el_log))

# ---- Trap: sensor HIGH continuously through warm-up and beyond must NOT fire at the warm-up boundary
w = run([(0, 63_000)], 90_000)
check("Trap: HIGH across warm-up boundary -> no phantom trigger (no rising edge)", len(triggers(w)) == 0, str(triggers(w)))
check("EL: no phantom energise across the warm-up boundary", el_on(w) == [], str(w.el_log))

# ---- T3: ten 3-second walk-bys, 15 s apart -> exactly ten triggers, each within 200 ms of motion onset
starts = [70_000 + i * 15_000 for i in range(10)]
w = run([(s, s + 3_000) for s in starts], starts[-1] + 20_000)
tg = triggers(w)
lat = [tg[i] - starts[i] for i in range(min(len(tg), 10))]
check("T3 exactly 10 triggers for 10 walk-bys", len(tg) == 10, f"{len(tg)} triggers")
check("T3 each trigger within 200 ms of motion onset (debounce 60 ms)", lat and max(lat) <= 200 and min(lat) >= 40, f"latencies ms={lat}")
_nb = float(re.search(r"^NOTIFY_BRIGHTNESS\s*=\s*([0-9.]+)", pathlib.Path("code.py").read_text(), re.M).group(1))
check(f"T3 strip reached the configured {_nb:.0%} white cap", w.strip_max == int(255 * _nb), f"max={w.strip_max} want={int(255*_nb)}")
check("EL: one on/off pair per notification, strictly alternating, starting ON",
      len(el_on(w)) == 10 and len(el_off(w)) == 10 and el_alternates(w), f"log={len(w.el_log)} entries")
check("EL: energises on the same tick as the trigger (snaps on with the ring)",
      el_on(w) == triggers(w), f"on={el_on(w)[:3]} trig={triggers(w)[:3]}")
check("EL: de-energises only after the LED fade completes (>= sound+fade)",
      all(off - on >= 4900 for on, off in zip(el_on(w), el_off(w))),
      str([off - on for on, off in zip(el_on(w), el_off(w))][:3]))
check("EL: dark during every cooldown and idle gap between walk-bys",
      all(el_off(w)[i] < el_on(w)[i+1] for i in range(9)), "overlap between notifications")

# ---- T4: continuous motion for 60 s (REPEAT_IF_OCCUPIED=True) -> a ping every ~10 s, then silence after it stops
w = run([(70_000, 130_000)], 160_000)
tg = triggers(w)
gaps = [b - a for a, b in zip(tg, tg[1:])]
check("T4 ~6 triggers in 60 s of continuous motion", 5 <= len(tg) <= 7, f"{len(tg)} at {tg}")
check("T4 re-ping interval == COOLDOWN_S (10 s) ± loop period", gaps and all(9_950 <= g <= 10_100 for g in gaps), f"gaps={gaps}")
check("T4 no triggers after motion stops", not [t for t in tg if t > 130_000 + 10_100], str([t for t in tg if t > 130_000]))
last_state = transitions(w)[-1][1]
check("T4 ends in IDLE once the person leaves", last_state == "STATE -> IDLE", last_state)
check("T4 EL: one on/off pair per re-ping, alternating", len(el_on(w)) == len(tg) and el_alternates(w), f"{len(el_on(w))} vs {len(tg)}")
check("T4 EL: ends de-energised after the person leaves", w.el_log and w.el_log[-1][1] is False, str(w.el_log[-2:]))

# ---- EL_ENABLED = False must leave the pin untouched entirely
import re as _re
_src = pathlib.Path("code.py").read_text()
pathlib.Path("code.py").write_text(_src.replace("EL_ENABLED               = True", "EL_ENABLED               = False", 1))
try:
    w_off = run([(70_000, 71_000)], 95_000)
finally:
    pathlib.Path("code.py").write_text(_src)
check("EL_ENABLED=False: pin never touched, notification still fires",
      w_off.el_log == [] and len(triggers(w_off)) == 1, f"log={w_off.el_log} trig={len(triggers(w_off))}")

# ---- Notify timing: hold lasts the sound length, then a 1.5 s fade, then cooldown ends 10 s after the trigger
w = run([(70_000, 71_000)], 95_000)
ev = {e: t for t, e in w.events if e.startswith("STATE ->")}
t_notify = [t for t, e in w.events if e == "STATE -> NOTIFY"][0]
t_cool = [t for t, e in w.events if e == "STATE -> COOLDOWN"][0]
t_idle2 = [t for t, e in w.events if e == "STATE -> IDLE"][1]
check("Notify lasts sound (3.45 s) + attack + fade (1.5 s) ≈ 5.0 s", 4_900 <= t_cool - t_notify <= 5_200, f"{t_cool - t_notify} ms")
check("Cooldown ends 10 s after the trigger start", 9_950 <= t_idle2 - t_notify <= 10_100, f"{t_idle2 - t_notify} ms")

# ---- Runtime fault -> reset path (simulate by making the sensor raise once after warm-up)
class Boom(Exception): pass
w = World([], 100_000)
# monkeypatch: after 70 s, sensor read raises -> code.py must print RUNTIME ERROR and call reset (StopSim)
orig = World.sensor_level
def faulty(self):
    if self.t >= 70_000: raise Boom("sensor exploded")
    return False
World.sensor_level = faulty
w2 = run([], 100_000)
World.sensor_level = orig
check("Runtime exception -> 'RUNTIME ERROR' printed and microcontroller.reset() called",
      any(e.startswith("RUNTIME ERROR") for _, e in w2.events) and w2.t < 100_000, str([e for _, e in w2.events][-2:]))

ok = all(r[1] for r in results)
for name, passed, detail in results:
    print(("PASS " if passed else "FAIL ") + name + ("" if passed else f"   [{detail}]"))
print("\nOVERALL:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
