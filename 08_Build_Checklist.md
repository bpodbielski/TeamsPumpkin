# 08 — Build Checklist

One page to work from in the garage and at the bench, pulled from 02/04/05/06 so you're not flipping between docs. Tick as you go.

---

## A. Pre-work — printing (parts ✅ delivered, pumpkin ✅ bought, face ✅ measured 178 × 203 mm)

The template is already set to this pumpkin: logo **125 mm**, face 178 × 203 mm, window 93 %, logo top 20 mm. Don't change the numbers unless the pumpkin changes.

- [ ] Open `assets/print_template.html` in Safari/Chrome.
- [ ] **Home laser — pages 2 and 3**, B&W, **100 % / "Actual size"**, Letter portrait. Page 2 = window cut template. Page 3 = full-size face layout (window + PIR hole + centre line).
- [ ] **Measure the 100 mm scale bar on the printout with a ruler.** If it isn't 100 mm, scaling is on — fix it and reprint before cutting anything.
- [ ] **FedEx — page 1**, color, 100 %, **2 copies on white cardstock + 1 on plain paper**. Save as PDF from the print dialog; tell them "actual size, do not fit to page". Check the scale bar before you leave the store.
- [ ] Verify the porch outlet (the only open logistics item).

## B. Pumpkin work (needs only the hot knife — do it as soon as it lands Sep 24)

> ⚠️ **Respirator on. Outdoors or garage with the door open and a fan running. Never indoors.** Burning polyurethane is worse than polystyrene. Break every 30 min (the tool's own guidance).

- [ ] Tape the **page-3 face layout** over the flat face: blue centre line on the pumpkin's vertical centre, red box inside the moulding seams.
- [ ] Trace the window silhouette **and** the 24 mm PIR circle with a pencil, pressing just hard enough to leave a line in the foam. (Page 2 is the same silhouette on its own if you'd rather cut it out and draw round it.)
- [ ] Mark the **three islands**: big head (Ø ≈ 39 mm), small head (Ø ≈ 32 mm), body. Keep the **~6.5 mm** foam bridges between heads and body.
- [ ] Preheat the wand knife 20–25 s. Plunge at a corner, confirm it's all the way through, then follow the line pulling *away* from the template.
- [ ] Push cut pieces inward; sand melt ridges with 220 grit.
- [ ] **PIR hole**: 24 mm circle, already positioned on the layout sheet (~16 mm below the window, ~15 mm above the bottom of the usable face). Angle the dome slightly down toward the walkway; never facing direct sun, a vent or a grill.
- [ ] **Speaker port**: an opening in the base, plus three ~1/2" feet (foam offcuts or corks) so sound escapes.
- [ ] **Back hatch**: rectangle with a small notch at the bottom so you can pull it out.
- [ ] **Backlight test**: in the dark, hold a flashlight behind each print (2 stacked cardstock vs 1 plain) through a sheet of white paper. Pick the winner, judged from ~20 ft. Don't trim the sheet to the logo — leave it whole; the 4.4 mm overhang is what hides the window edge.
- [ ] Tape the chosen print + white paper diffuser inside, print facing out, all four edges taped.

## C. Bench electronics (when the Adafruit board arrives)

Full detail: `firmware/README.md`. Order matters — add one thing at a time.

- [ ] **Flash CircuitPython**: hold **BOOT**, tap **RESET**, release BOOT → `RPI-RP2` drive → drag the UF2 for `adafruit_feather_rp2040_prop_maker` (9.x or 10.x stable) → reboots as `CIRCUITPY`.
- [ ] **Copy `lib/`**: `neopixel.mpy`, `adafruit_pixelbuf.mpy`, `adafruit_ticks.mpy` from the matching bundle version.
- [ ] **Copy the firmware**: `code.py` and `sounds/` from this repo's `firmware/` folder to the root of CIRCUITPY.
- [ ] **Board alone** → amber blink 60 s, then dim green. Serial: `screen /dev/tty.usbmodem* 115200`.
- [ ] **Prep the strip**: find the input end (arrows point away from it), cut at the **30th LED**, keep the input half, plug in the 3-pin pigtail.
- [ ] **Wire it** (04_Wiring): strip 5V/Neo/GND · speaker +/− · PIR VCC→servo V+, GND→servo G, OUT→**Btn** terminal. 2 mm screwdriver.
- [ ] **PIR settings**: delay pot **fully counter-clockwise**, sensitivity **mid**, jumper **H**.
- [ ] **Self-test**: set `SELFTEST_ON_BOOT = True`, reset → one notification 3 s after warm-up. Set it back to `False` after.
- [ ] **T3**: 10 hand-waves at 1 m, ≥12 s apart → 10 pings, each within ~0.2 s.
- [ ] **T4**: wave continuously 60 s → a ping every ~10 s; stops when you stop.
- [ ] **T5**: leave the room 30 min → zero pings.
- [ ] **T7**: pull power mid-notification, replug → clean boot, re-arms itself.
- [ ] **White check**: does the flash look white, not pink/dim? If pink → shorter Anker cable, or lower `NOTIFY_BRIGHTNESS`.
- [ ] **Volume check**: loud enough from ~15 ft with the speaker sitting in open air?

## D. Integrate (target Sat–Sun Oct 3–4)

- [ ] Board in its plastic box, hot-glued to the floor **within a few inches of the speaker** (its leads are only ~9 cm).
- [ ] Speaker at the base port; strip hot-glued to the **inside back wall**, facing forward.
- [ ] PIR dome seated flush in its hole from inside.
- [ ] USB cable out through the hatch notch; hatch taped.
- [ ] Adapter and any cord joint **under cover**, off the ground.
- [ ] **Night test on the porch**: walk up from the sidewalk 5×. Fires at ~3–4 m each time? Audible at 15 ft? Logo legible at 40 ft?
- [ ] Leave it plugged in (always on, by decision).

## E. Running (Oct 5–31)

- [ ] Weekly 2-minute check: cable seated, print flat, no condensation inside, no false-trigger complaints.
- [ ] If animals set it off at night → turn the sensitivity pot down and/or aim the dome lower.
- [ ] Halloween night: consider `COOLDOWN_S = 5` for faster re-pings with a queue at the door.

---

## Quick reference

**Status LED**: amber blink = warming up · dim green = armed · white = notifying · dim blue = cooldown · red blink = startup error (check files).

**Tuning** — edit at the top of `CIRCUITPY/code.py`, save, press RESET (autoreload is off on purpose):
| Want | Change |
|---|---|
| Quieter / louder | `VOLUME` (0–1) |
| Dimmer / brighter flash | `NOTIFY_BRIGHTNESS` (0.70 now; ≥0.8 eats power headroom) |
| Ping more/less often while someone lingers | `COOLDOWN_S` |
| One ping per approach only | `REPEAT_IF_OCCUPIED = False` |
| Faint purple glow between triggers | `IDLE_MODE = "breathe"` |
| Longer sound (two rings) | copy `assets/teams_call_2rings_22k_mono.wav` into `sounds/` and point `SOUNDS` at it |
