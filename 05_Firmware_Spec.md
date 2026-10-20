# 05 — Firmware Spec (`code.py`, CircuitPython, RP2040 Prop-Maker Feather)

Status: **FINAL v1 (2026-09-22) — IMPLEMENTED** in `firmware/code.py` (delegated implementation, then reviewed line-by-line against this spec; two defects fixed: RP2040 bootloader instructions and inverted fade-out easing). Host-side simulation (`firmware/sim/`) passes T1, T3, T4, timing and fault-reset checks; T2, T5–T10 need hardware. Decided values: current (2025) logo (no firmware impact), idle OFF, one ring of the call sound, PIR only (jumper **H**), re-ping every cooldown while someone lingers, 10 s cooldown, always on (no timer).

## 1. Purpose
Motion → play a Teams sound + light the backlit logo, once per approach, forever, unattended.

## 2. Platform
- Board: Adafruit RP2040 Prop-Maker Feather. CircuitPython **9.x or 10.x stable** for `adafruit_feather_rp2040_prop_maker` (UF2 from circuitpython.org).
- Libraries (copy from the matching Adafruit CircuitPython Bundle into `CIRCUITPY/lib/`): `neopixel.mpy`, `adafruit_pixelbuf.mpy`, `adafruit_ticks.mpy`. Everything else is built in (`board`, `digitalio`, `audiobusio`, `audiocore`, `audiomixer`, `supervisor`, `microcontroller`, `random`, `time`).
- Reference implementation to borrow patterns from: `reference/adafruit_propmaker_jack_o_lantern_code.py` (MIT).

## 3. Files on CIRCUITPY
```
code.py
settings.toml            (optional; not used in v1 — all config is constants at the top of code.py)
sounds/teams_call_1ring.wav
sounds/teams_call_2rings.wav
sounds/teams_notify.wav  (when obtained)
lib/neopixel.mpy, lib/adafruit_pixelbuf.mpy, lib/adafruit_ticks.mpy
```
WAV format (hard requirement): **PCM 16-bit signed, mono, 22,050 Hz**. Files in `assets/` already comply.

## 4. Pins (CircuitPython names)
| Purpose | Pin | Mode |
|---|---|---|
| External power enable (NeoPixel 5 V, servo V+ = sensor power, amp enable) | `board.EXTERNAL_POWER` (GPIO23) | Output, **HIGH at boot, never LOW** |
| Motion sensor OUT | `board.EXTERNAL_BUTTON` (GPIO19) | Input, `pull = None` (sensor is push-pull 3.3 V). Constant `SENSOR_PIN` so it can be switched to `board.EXTERNAL_SERVO` (GPIO20) |
| NeoPixel strip data | `board.EXTERNAL_NEOPIXELS` (GPIO21) | `neopixel.NeoPixel(pin, NUM_PIXELS, brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)` |
| I2S audio | `board.I2S_BIT_CLOCK`, `board.I2S_WORD_SELECT`, `board.I2S_DATA` | `audiobusio.I2SOut(...)` |
| Onboard status NeoPixel | `board.NEOPIXEL` | 1 px, brightness 0.2, used as a status indicator |

## 5. Configuration constants (top of `code.py`)
```python
NUM_PIXELS          = 30        # pixels actually wired
SENSOR_PIN          = board.EXTERNAL_BUTTON
SENSOR_ACTIVE_HIGH  = True
WARMUP_S            = 60        # ignore sensor after boot (PIR calibration)
COOLDOWN_S          = 10        # minimum seconds between notifications
REPEAT_IF_OCCUPIED  = True      # DECIDED: re-ping every COOLDOWN_S while the sensor stays HIGH (someone lingering)
IDLE_MODE           = "off"     # DECIDED: "off". ("breathe" supported for later.)
IDLE_COLOR          = (90, 60, 255)   # Teams-ish purple (R,G,B) for breathe mode
IDLE_BRIGHTNESS     = 0.08      # peak of the breathe cycle (0–1)
IDLE_BREATHE_PERIOD_S = 4.0
NOTIFY_COLOR        = (255, 255, 255) # white: shows the print in true colors
NOTIFY_BRIGHTNESS   = 0.70      # power cap (~1.3 A for 30 px)
NOTIFY_ATTACK_S     = 0.05      # snap on
NOTIFY_HOLD_S       = None      # None = hold until the sound finishes; else seconds
NOTIFY_FADE_S       = 1.5       # fade back to idle
SOUNDS = [                      # (filename, weight); weights need not sum to 1
    ("sounds/teams_call_1ring.wav", 1.0),   # DECIDED: one ring, from Ben's clip
]
VOLUME              = 1.0       # mixer voice level 0–1
SELFTEST_ON_BOOT    = False     # True on the bench: fire one notification 3 s after warm-up
DEBUG_PRINT         = True      # serial prints; harmless on the porch
LOOP_PERIOD_MS      = 20
```

## 6. State machine
```
BOOT ──► WARMUP ──(WARMUP_S elapsed)──► IDLE ──(sensor rising edge)──► NOTIFY ──(sound done + fade done)──► COOLDOWN ──(COOLDOWN_S since trigger)──► IDLE
                                                                                                                                    └─(REPEAT_IF_OCCUPIED and sensor HIGH)──► NOTIFY
```
- **BOOT**: `supervisor.runtime.autoreload = False`; external power HIGH; open all WAVs once (`audiocore.WaveFile(open(path, "rb"))`); create `audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1, bits_per_sample=16, samples_signed=True)`; `audio.play(mixer)`; strip all off; status LED amber.
- **WARMUP**: sensor ignored. Status LED amber, slow blink. Strip off (regardless of IDLE_MODE).
- **IDLE**: status LED dim green. Strip per `IDLE_MODE` (off, or a sine "breathe" between 0 and `IDLE_BRIGHTNESS` of `IDLE_COLOR`). Sensor sampled every loop; a **LOW→HIGH transition** (after 3 consecutive HIGH samples = 60 ms debounce) is a trigger.
  The PIR is set to jumper **H (repeat trigger)** with the delay pot at minimum, so its output stays HIGH for as long as motion keeps occurring (+~3 s) and drops LOW when the person leaves. A walk-by therefore produces one ~3 s HIGH pulse; a lingering visitor produces a continuous HIGH.
- **NOTIFY**: choose a sound by weighted random from `SOUNDS`; `mixer.voice[0].level = VOLUME`; `mixer.voice[0].play(wave)`; strip ramps to `NOTIFY_COLOR × NOTIFY_BRIGHTNESS` over `NOTIFY_ATTACK_S`; hold while `mixer.voice[0].playing` (or `NOTIFY_HOLD_S`); then fade linearly to the idle level over `NOTIFY_FADE_S`. Status LED white. Record `trigger_ms`.
- **COOLDOWN**: sensor edges ignored until `ticks_diff(now, trigger_ms) >= COOLDOWN_S*1000`. Then: if `REPEAT_IF_OCCUPIED` and the (debounced) sensor level is still HIGH → NOTIFY again immediately (re-ping); else IDLE, where the next rising edge triggers. Net effect with the decided settings: one ping per walk-by, one ping every 10 s while someone stands there, no pings when nobody is there.

All timing via `supervisor.ticks_ms()` + `adafruit_ticks.ticks_diff/ticks_add` (wrap-safe); no `time.sleep()` longer than `LOOP_PERIOD_MS`. Animations are computed from elapsed time each loop (non-blocking), so audio and lights stay in sync and the sensor keeps being read.

## 7. Robustness rules
1. Whole loop inside `try/except Exception as e:` → print, `time.sleep(2)`, `microcontroller.reset()` (Adafruit's pattern). Startup errors (missing WAV) → status LED red blink for 5 s, then reset (so a bad SD copy is visible on the bench).
2. `EXTERNAL_POWER` never toggled after boot (it powers the sensor and enables the amp).
3. Strip written with `auto_write=False` + one `show()` per loop.
4. Gamma: apply a simple `x*x` curve to brightness ramps so fades look linear to the eye.
5. Mixer/voice objects are created once; never re-create `I2SOut` in the loop.
6. Ignore the sensor during WARMUP even if `SELFTEST_ON_BOOT` fires.
7. Serial output must not block when no host is attached (it doesn't in CircuitPython — just `print`).

## 8. Status LED legend (onboard NeoPixel)
| Color | Meaning |
|---|---|
| Amber blink | Warming up |
| Dim green | Armed / idle |
| White | Notifying |
| Dim blue | Cooldown |
| Red blink | Startup error (check files) |

## 9. Non-goals (v1)
Wi-Fi, real Teams integration, clock/quiet hours (the outlet timer does this), battery management, multiple zones.

Planned v1.5 extension (not in v1 acceptance): 16×16 matrix mode — `NUM_PIXELS = 256`, `NOTIFY_BRIGHTNESS ≤ 0.25`, a 16×16 RGB bitmap of the logo rendered instead of a solid fill, and a red badge digit (3×5 font) at the top-right that increments on each trigger and resets at boot. Same pins, same state machine.

## 10. Acceptance tests (bench, then porch)
| # | Test | Pass |
|---|---|---|
| T1 | Power on with no sensor motion | Amber blink for 60 s, then dim green; strip stays off; nothing plays. |
| T2 | `SELFTEST_ON_BOOT = True` | One notification 3 s after warm-up: sound + white flash + fade; no second fire. |
| T3 | Wave a hand at 1 m, 10 times, ≥12 s apart | 10/10 single notifications; each starts within 200 ms of motion. |
| T4 | Continuous motion (hand waving) for 60 s | With the decided `REPEAT_IF_OCCUPIED = True`: a notification every ~10 s (≈6 in 60 s), each with sound + flash; the strip returns to off between them. With `False`: exactly one. |
| T5 | 30 min with nobody in the room (PIR) / house quiet (RCWL) | Zero notifications. |
| T6 | Delete a WAV and reboot | Red blink → reset loop; restore the file → normal boot. |
| T7 | Pull power mid-notification, restore | Clean boot, warm-up, armed; no stuck LEDs. |
| T8 | Set `IDLE_MODE = "breathe"` (optional mode, not the decided default) | Smooth 4 s purple breathing at low brightness; notification still snaps to white and returns to breathing. Then set it back to `"off"` and confirm the strip is fully dark in idle. |
| T9 | `SOUNDS` with two entries at 0.5/0.5, 20 triggers | Both files play; no crash; RAM stable (`gc.mem_free()` printed each trigger does not trend down). |
| T10 | Porch, night, walk up from the sidewalk 5 times | Fires at ~3–4 m each time; audible at 15 ft; logo legible at 40 ft. |
