# Firmware — install and bench procedure

Implements `../05_Firmware_Spec.md` on an **Adafruit RP2040 Prop-Maker Feather**.
Read that doc for *why*; this doc is just the *how* to get it flashed and
running on the bench.

## 1. Flash CircuitPython

1. Download the CircuitPython UF2 for this exact board (**not** a generic
   RP2040 build) from:
   `https://circuitpython.org/board/adafruit_feather_rp2040_prop_maker/`
   Get the latest **9.x** or **10.x** stable release — not a nightly/alpha.
2. Plug the Feather into your Mac over USB-C.
3. Enter the bootloader (RP2040 procedure — *not* the double-click used by
   older SAMD Feathers): **hold the BOOT button down, tap RESET, then release
   BOOT.** The board shows up as a drive named **`RPI-RP2`**. (Holding BOOT
   while plugging in the USB cable does the same thing. A plain single
   click of RESET just restarts `code.py`.)
4. Drag the `.uf2` file onto the `RPI-RP2` drive. The board reboots itself
   and re-mounts as a drive named **`CIRCUITPY`** — that's CircuitPython
   installed.

## 2. Install the three required libraries

The firmware imports `neopixel` and `adafruit_ticks`, which are **not**
built into CircuitPython and must be copied in from Adafruit's library
bundle (everything else it uses — `board`, `digitalio`, `audiobusio`,
`audiocore`, `audiomixer`, `supervisor`, `microcontroller`, `time`, `math`,
`random`, `gc` — is already built in).

1. Download the **Adafruit CircuitPython Bundle** from
   `https://circuitpython.org/libraries` — get the bundle version that
   matches your CircuitPython major version (a 9.x bundle for 9.x firmware,
   a 10.x bundle for 10.x firmware; `.mpy` files are version-locked and a
   mismatched bundle will fail to import or crash on boot).
2. Unzip it. Inside, copy these three files from the bundle's `lib/` folder
   into `CIRCUITPY/lib/` (create the `lib` folder on CIRCUITPY if it isn't
   there yet):
   - `neopixel.mpy`
   - `adafruit_pixelbuf.mpy` (`neopixel` depends on this one — easy to miss)
   - `adafruit_ticks.mpy`

## 3. Copy the firmware onto CIRCUITPY

Final layout on the `CIRCUITPY` drive:
```
CIRCUITPY/
├── code.py
├── sounds/
│   └── teams_call_1ring.wav
└── lib/
    ├── neopixel.mpy
    ├── adafruit_pixelbuf.mpy
    └── adafruit_ticks.mpy
```
From this `firmware/` folder, copy `code.py` and the `sounds/` folder
(with `teams_call_1ring.wav` inside it) to the root of `CIRCUITPY`,
alongside the `lib/` folder from step 2. Paths in `code.py` (e.g.
`sounds/teams_call_1ring.wav`) are relative to `CIRCUITPY`'s root, so the
layout has to match exactly.

As soon as `code.py` lands on `CIRCUITPY`, the board runs it: amber blink
(warm-up) for `WARMUP_S` (60 s default), then dim green (armed).

## 4. Run the self-test

`code.py` sets `supervisor.runtime.autoreload = False` on boot (so a prop
sitting on a porch doesn't randomly restart), which means **editing and
saving `code.py` does not automatically restart it** — you must reset
manually after each edit (single-click RESET, or unplug/replug USB, or
`Ctrl-D` from the serial console in step 5).

1. Open `CIRCUITPY/code.py` in any text editor.
2. Set `SELFTEST_ON_BOOT = True` and save.
3. Reset the board (single-click RESET).
4. Watch: amber blink for 60 s → dim green → 3 s later, one notification
   fires on its own (white flash + the ring sound + fade back down) → dim
   blue for 10 s → back to dim green. No second notification.
5. Set `SELFTEST_ON_BOOT` back to `False`, save, and reset again before
   leaving it unattended — otherwise it self-fires once on every boot.

This exercises the same NOTIFY path a real sensor trigger does, without
needing the PIR wired up yet — it's test **T2** from `05_Firmware_Spec.md`
§10. Once the PIR is connected, `04_Wiring.md`'s bench-test checklist and
the rest of the §10 acceptance tests (T1–T10) are the fuller pass.

## 5. Watch serial output

`DEBUG_PRINT = True` by default, so the board prints state transitions,
`TRIGGER` lines, and free-RAM on every trigger.

On macOS:
```bash
ls /dev/tty.usbmodem*          # find the port; usually just one match
screen /dev/tty.usbmodem14201 115200   # substitute the path you found
```
To exit `screen`: `Ctrl-A` then `K`, then confirm with `Y` (or `Ctrl-A`
then `\`). `Ctrl-C` does **not** exit `screen` — it goes to the board and
(on CircuitPython) raises `KeyboardInterrupt` in the running program instead.
Pressing `Ctrl-D` in the serial console soft-restarts `code.py` — handy
after editing a config constant, since autoreload is off (step 4).

## 6. Status LED legend (the board's onboard NeoPixel)

| Color | Meaning |
|---|---|
| Amber, blinking | Warming up (`WARMUP_S` after boot; sensor ignored) |
| Dim green, solid | Armed / idle |
| White, solid | Notifying (sound + logo lit) |
| Dim blue, solid | Cooldown (`COOLDOWN_S` after a trigger) |
| Red, blinking | Startup error (e.g. a missing/renamed WAV) — blinks ~5 s, then resets and retries. Fix the file and reset. |

## 7. Tuning — config constants at the top of `code.py`

All configuration lives as plain constants at the top of `code.py` (no
`settings.toml` in v1) — edit, save, and reset (step 4) to apply.

| Constant | Default | Effect |
|---|---|---|
| `NUM_PIXELS` | `30` | Pixels actually wired on the strip. |
| `SENSOR_PIN` | `board.EXTERNAL_BUTTON` | Motion sensor input pin. Swap to `board.EXTERNAL_SERVO` only if GPIO19 misbehaves (see `04_Wiring.md` Plan B). |
| `SENSOR_ACTIVE_HIGH` | `True` | Sensor's "motion" logic level. |
| `WARMUP_S` | `60` | Seconds after boot the sensor is ignored (PIR calibration). |
| `COOLDOWN_S` | `10` | Minimum seconds between the *start* of one notification and the next. |
| `REPEAT_IF_OCCUPIED` | `True` | Re-fire every `COOLDOWN_S` while the sensor is still HIGH (someone lingering), instead of just once. |
| `IDLE_MODE` | `"off"` | `"off"` (strip dark) or `"breathe"` (slow sine pulse). |
| `IDLE_COLOR` | `(90, 60, 255)` | Breathe-mode color. |
| `IDLE_BRIGHTNESS` | `0.08` | Breathe-mode peak brightness (0–1). |
| `IDLE_BREATHE_PERIOD_S` | `4.0` | Breathe-mode full cycle length, seconds. |
| `NOTIFY_COLOR` | `(255, 255, 255)` | Notification flash color. |
| `NOTIFY_BRIGHTNESS` | `0.70` | Notification brightness cap (0–1); raise carefully — power draw scales with it (see `04_Wiring.md` power budget). |
| `NOTIFY_ATTACK_S` | `0.05` | Ramp-up time to full brightness. |
| `NOTIFY_HOLD_S` | `None` | `None` = hold at full brightness until the sound finishes; a number = hold that many seconds instead. |
| `NOTIFY_FADE_S` | `1.5` | Fade-down time back to the idle level. |
| `SOUNDS` | `[("sounds/teams_call_1ring.wav", 1.0)]` | `(path, weight)` list; add a second tuple to play more than one clip at random (weights need not sum to 1). |
| `VOLUME` | `1.0` | Mixer playback level (0–1). |
| `SELFTEST_ON_BOOT` | `False` | `True` fires one notification 3 s after warm-up, for bench testing (step 4). Leave `False` on the porch. |
| `DEBUG_PRINT` | `True` | Serial logging (step 5). Harmless to leave on. |
| `LOOP_PERIOD_MS` | `20` | Main loop cadence; also sets the sensor debounce window (3 samples × this = 60 ms). Lower = snappier but busier CPU. |
| `EL_ENABLED` | `True` | Drives the purple EL wire outline. Set `False` to leave GPIO20 untouched and run LEDs-only (the fallback build). |
| `EL_PIN` | `board.EXTERNAL_SERVO` | GPIO20, servo header `Sig` → AOD4184 MOSFET gate. **Must not equal `SENSOR_PIN`** — the firmware refuses to boot if it does. |

## 7b. EL wire outline (see `../09_EL_Wire_Design.md`)

GPIO20 drives the gate of an AOD4184 MOSFET module that switches the 5 V EL inverter.
The firmware energises it **on the same tick as the ring** and de-energises it only once
the LED fade has finished — EL can't dim, so it cuts cleanly at the end rather than
part-way through. It is **on/off only, never PWM**: EL inverters flicker across most of
the duty range.

**Bench it before carving:** with the MOSFET module wired and `SELFTEST_ON_BOOT = True`,
the EL should snap on with the sound and cut ~5 s later, and stay dark through warm-up,
idle and cooldown. If you want to test the LEDs alone first, set `EL_ENABLED = False`.

**Test the EL chain standalone first**, before wiring it to the board: EL wire →
inverter → any USB brick. Confirms both that it lights and that the connectors mate.

## 8. Troubleshooting on the bench

| Symptom | Check |
|---|---|
| Serial shows `STATE -> WARMUP` but the onboard status LED never lights | In the REPL run `import board; print(dir(board))`. If `NEOPIXEL_POWER` is listed, that pin must be driven HIGH before the status pixel works — add it next to `external_power` in `code.py`. |
| Red blink at boot | A WAV is missing/renamed, or a `lib/` file is missing or from the wrong bundle version. Serial prints the exact error. |
| No sound, everything else works | Speaker on the **+/−** speaker terminals (not the NeoPixel block); 4–8 Ω speaker; `EXTERNAL_POWER` is what enables the amp — it is set HIGH by `code.py`, so if the board was reset into the REPL the amp is off. |
| Strip dark | Strip's **input** end (arrow direction) on the terminal; 5 V/Neo/GND order per the silkscreen; `NUM_PIXELS` > 0; the flash is only 3.5 s long — use `SELFTEST_ON_BOOT`. |
| Wrong colors on the strip (white looks tinted) | `pixel_order=neopixel.GRB` is right for WS2812B; some strips are RGB — change it. A pink-ish white at full brightness means voltage drop: shorter/thicker USB cable. |
| Red blink at boot, serial says "EL_PIN and SENSOR_PIN are the same pin" | You set `SENSOR_PIN = board.EXTERNAL_SERVO` (the plan-B sensor pin) while `EL_ENABLED = True`. They both want GPIO20 — move the sensor back to `board.EXTERNAL_BUTTON`, or set `EL_ENABLED = False`. |
| EL never lights, LEDs fine | Check the MOSFET module's `SIG` pin actually contacts GPIO20 (push-in Dupont pins work loose — hot-glue it), common ground between board and module, and that the inverter's USB lead is on the module's **output** terminals, not the input. Test the EL chain standalone off a USB brick to split the problem in half. |
| EL lights but the board resets mid-notification | Brownout — you're near the 3 A supply limit. Drop `NOTIFY_BRIGHTNESS` to 0.5 or cut the strip to 20 pixels. |
| Triggers constantly | PIR still warming up (wait 60 s), delay pot not at minimum, sensitivity too high, dome facing a heat source or sun, or `SENSOR_ACTIVE_HIGH` wrong for a different sensor. |
| Never triggers | PIR `OUT` on the **Btn** terminal; VCC on servo `V+` (5 V) and GND on servo `G`; try `SENSOR_PIN = board.EXTERNAL_SERVO` with OUT on the servo `Sig` pin (Plan B). |

## 9. Host-side simulator (run after any edit to `code.py`)

`sim/sim_state_machine.py` stubs the CircuitPython modules with a virtual clock and a scripted
motion sensor, runs the real `code.py`, and checks the state machine against spec §10:
T1 (no motion), the warm-up-boundary trap, T3 (10 walk-bys, trigger latency), T4 (re-ping every
10 s while occupied, silence after), notify/cooldown timing, and the exception → reset path.
```bash
python3 sim/sim_state_machine.py
```
It also asserts the EL pin behaviour: one on/off pair per notification, energised on the
same tick as the trigger, de-energised only after the fade, dark through warm-up, idle and
cooldown, and completely untouched when `EL_ENABLED = False`.

It cannot test the hardware APIs themselves (pin names, audio, NeoPixel timing) — that is what the
bench tests are for — but it catches logic regressions before you're standing on the porch.

## Reference

- `../05_Firmware_Spec.md` — the authoritative spec, including the full
  state machine and the T1–T10 acceptance tests.
- `../04_Wiring.md` — hardware hookup and the Phase-1 bench-test checklist.
- `../reference/adafruit_propmaker_jack_o_lantern_code.py` — Adafruit's
  MIT-licensed example this firmware's API patterns are borrowed from.
