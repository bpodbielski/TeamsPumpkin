# CustomPumpkin — the "Teams-o-lantern"

A foam carvable pumpkin that plays a Microsoft Teams sound and lights up a backlit Teams logo when someone walks by. The Teams answer to Guy Dupont's Slack-o-lantern (Oct 2025), built to survive the whole month of October on the porch.

**Status (2026-10-15): design changed — EL wire outline.** Glow test FAILED (thinned foam is opaque), so the relief idea is dead. New design: purple EL wire in the outline groove + the T cut through and backlit white by the NeoPixels (`09_EL_Wire_Design.md`). $22.59 of parts ordered, all arriving by Sat Oct 17. Firmware needs a small delta (GPIO20 drives a MOSFET). 16 days to Halloween; the original backlit-insert plan remains the fallback. All 15 decisions confirmed by Ben (table below). `firmware/` is ready to copy to the board when it arrives. Parts to order today; pumpkin + hot knife locally this week. Outlet on the covered porch still to be verified by Ben.

## The design in five lines (as decided)
1. **Brain + audio + lights on one $20 board**: Adafruit RP2040 Prop-Maker Feather (CircuitPython) — built-in 3 W amp, NeoPixel driver, sensor input, all screw terminals → **no soldering**.
2. **Logo**: the **current (2025) Teams icon**; window cut in its silhouette in a Lowe's 13" foam pumpkin; behind it two stacked color transparencies of the logo (FedEx) on a white diffuser, lit by ~30 NeoPixels from the inside back wall. **Dark between triggers**; snaps to full white on a notification.
3. **Sensor**: HC-SR501 PIR through a 24 mm hole low on the front, jumper **H** so it re-pings every 10 s while someone stands there.
4. **Sound**: 40 mm 4 Ω speaker ported through the base; **one ring** of the Teams call sound (from Ben's clip, converted in `assets/`).
5. **Power**: 5 V/3 A USB wall adapter, **always on** (no timer); the firmware re-arms itself after any power cut.

Target: live on the covered porch by **Sat–Sun Oct 3–4**; **≈$125–130 all-in** with tax (07_Order_List.md), including the hot knife and the pumpkin.

## Files
| File | Purpose |
|---|---|
| `01_Research_Notes.md` | What the four transcripts teach, what the Slack-o-lantern actually used, verified hardware/logo/sound facts with sources. |
| `02_Build_Plan.md` | Options considered, recommended architecture, phases + gates + dates, the **adversarial review log** (20 attacks → changes), residual risks, stretch ideas. |
| `build_guide.html` | **The step-by-step build guide (published as an artifact)** — 33 steps across 5 phases, with diagrams; progress syncs across devices. |
| `10_Build_Changes.md` | Decisions made while writing the build guide (2-px light box, page 4, hole placement, grounding). |
| `09_EL_Wire_Design.md` | **Current lighting design (decided 2026-10-15)** — purple EL wire outline + through-cut white T; BOM, wiring, firmware delta, power budget. |
| `08_Build_Checklist.md` | **One-page tick-list for the garage and the bench** — carve, flash, wire, test, integrate, tune. |
| `07_Order_List.md` | **Order list with live prices (2026-09-23)** — exact carts, ASINs, links, totals. Start here to buy. |
| `03_Parts_List.md` | BOM for the recommended path (with prices/sources) and the Arduino alternative. |
| `04_Wiring.md` | Every connection, sensor settings, power budget, bench checklist. |
| `05_Firmware_Spec.md` | Delegation-ready spec for `code.py`: pins, config constants, state machine, robustness rules, acceptance tests. |
| `06_Logo_and_Sound_Assets.md` | Logo versions/colors/geometry, print template usage, materials test, sound sourcing + conversion commands. |
| `assets/print_template.html` | Open in a browser, set width, print at 100 %: logo insert + window cut silhouette for both logo versions, with a 100 mm scale bar. |
| `assets/teams_logo_*.svg/.png` | Both Teams logo versions (reference). |
| `assets/teams_call_1ring_22k_mono.wav`, `..._2rings_...` | Firmware-ready sound files cut from `TeamsCallSound.mp3`. |
| `TeamsCallSound.mp3` | Ben's source file (Teams incoming-call ringtone, 12 s). |
| `reference/` | Adafruit's MIT-licensed Prop-Maker pumpkin code — the pattern the firmware follows. |
| `firmware/` | `code.py`, install/bench README with troubleshooting, `sounds/`, and `sim/sim_state_machine.py` (host-side state-machine tests). |

## Decisions (confirmed by Ben, 2026-09-22)
| # | Question | Decision | Consequence in the plan |
|---|---|---|---|
| 1 | Logo rendering | **Backlit print behind a silhouette window** (16×16 matrix stays the optional v1.5 upgrade) | 02 §2a; print template pages 3–4 |
| 2 | Logo version | **Current 2025 icon** | Template page 1 (insert) + pages 2–3 (cut template, face layout); 3 silhouette islands (two heads + body) |
| 3 | Idle look | **Off between triggers** | `IDLE_MODE = "off"` |
| 4 | Sound | **One ring of the call sound, from Ben's clip** | `assets/teams_call_1ring_22k_mono.wav` → `firmware/sounds/teams_call_1ring.wav` |
| 5 | Sensor | **PIR (HC-SR501) through a 24 mm hole** | RCWL dropped from the BOM (kept as documented fallback) |
| 6 | Controller | **Prop-Maker Feather / CircuitPython** | — |
| 7 | Pumpkin | **Lowe's Holiday Living 13" carvable** | Face measured 178 × 203 mm → **logo width 125 mm** |
| 8 | Lingering visitors | **Re-ping every cooldown while they stand there** | `REPEAT_IF_OCCUPIED = True`; PIR jumper **H** (repeat trigger) |
| 9 | Cooldown | **10 s** | `COOLDOWN_S = 10` |
| 10 | Operating window | **Always on, no timer** | Timer removed from BOM; PIR must not face direct sun; expect occasional night-time animal pings |
| 11 | Location | **Covered porch; outlet access assumed, Ben to verify** | If no outlet: see 02 §6 contingency (power bank with always-on mode, or a cord from inside) |
| 12 | Printing | **Home B&W laser + FedEx Office** | Pages 2–3 (cut template + face layout) at home; page 1 (color insert) at FedEx: 2× cardstock + 1× paper |
| 13 | Hot knife | **Buy** (Walnut Hollow) | 03 §A item 12 |
| 14 | Budget / date | **≈$120–150 OK; live by Oct 3–4** | Order today |
| 15 | Firmware process | **Lower-tier implementer from the spec, Claude validates; Ben tunes constants in `code.py`** | `firmware/` |

## Decision log
- **2026-10-17** Design simplified to **EL outer outline only**: no T cut, no LEDs, no light box, no tile groove. Three EL holes. Guide (26 steps) and template page 4 updated.
- **2026-10-17** All parts in hand; build guide written and published. Design refinements from working out the build (see `10_Build_Changes.md`): strip cut to 2 px in a light box behind the T (`NUM_PIXELS=2`, `NOTIFY_BRIGHTNESS=0.15`), print-template page 4 for the EL layout, tile "C" groove, five EL holes with head holes moved off the foam bridges, corrected grounding (one G on the terminal block).
- **2026-10-15** Glow test **failed** — thinned craft-pumpkin foam does not transmit light, killing the relief-glow option. Decided the **EL wire hybrid**: purple EL in the groove for the outlines, T cut through and backlit white. Whine objection withdrawn (the inverter is only powered during the notification, masked by the ringtone). Parts: `B08FCCJR6X` + `B085H8TXF2` + `B0FMJH3DML`, $22.59.
- **2026-10-13** All parts delivered. Face measured **178 × 203 mm (7 × 8 in)** — wider than assumed. **Logo width set to 125 mm** (26 mm clear each side, 71 mm vertical slack). Print template rebuilt: classic-logo pages dropped, now 3 pages (insert / cut silhouette / **new full-size face layout** with the PIR hole positioned). Original Oct 3–4 target slipped; 18 days of runway remain.
- **2026-09-23** Amazon cart ordered ($74.43) after two review passes — charger swapped when the original showed an Oct 8–10 delivery. Build details surfaced by the review (cut the strip to 30 px keeping the input connector; 9 cm speaker leads) written into 04_Wiring.
- **2026-09-23** Adafruit cart ordered (board + speaker, $33.31). Live prices for every item captured in 07_Order_List.md; Adafruit found out of stock on PIR/strip/jumpers, so those go to Amazon.
- **2026-09-22** Firmware v1 implemented by a delegated lower-tier model from the final spec; reviewed and fixed (bootloader procedure, fade easing); 15/15 simulator checks pass.
- **2026-09-22** All 15 decisions confirmed (table above). Notable changes from the proposal: current 2025 logo instead of classic; idle OFF; PIR only (no RCWL); always-on with no timer; re-ping while occupied → PIR jumper H. Firmware implementation started from the final spec.
- **2026-09-21 (second pass)** Evaluated Adafruit 4117 purple neon flex and red+blue nOOds for the logo: rejected for Teams (outline-only, side-bend geometry can't make T corners/heads or follow the sphere, soldering at every cut, 12 V). Kept as documented alternative "neon T-tile" (03 §C). Re-instated the 16×16 matrix as the v1.5 upgrade path (03 §D). Idle look recommendation changed to faint purple breathing.
- **2026-09-21 (second pass)** Sound: Ben's `TeamsCallSound.mp3` (YouTube rip of the call ringtone) confirmed usable; 1-ring and 2-ring WAVs in `assets/` are the firmware inputs.
- **2026-09-21** Rejected nOOds/neon strokes (Dupont's method): no purple filament, Teams is filled shapes. Rejected LED matrix for v1 (power, diffusion, pixel-art likeness). Chose backlit print insert behind a silhouette window.
- **2026-09-21** Chose Prop-Maker Feather over Arduino Uno + DFPlayer Mini. Arduino path kept as documented alternative.
- **2026-09-21** Ben supplied the Teams **call ringtone** (not the message chime). Prepared 1-ring and 2-ring WAVs; firmware designed to take a weighted list of sounds.

## Next actions
1. **Ben, next:** print the three template pages (2–3 at home, 1 at FedEx) and start carving — see `08_Build_Checklist.md`. Verify the porch outlet. ~~Adafruit~~ ✅ ~~Amazon~~ ✅ ~~pumpkin~~ ✅ ~~measure~~ ✅.
2. **Ben:** print pages 2–3 of `assets/print_template.html` on the home laser; get page 1 printed at FedEx (2× cardstock, 1× plain paper). Check the 100 mm scale bar on both.
3. **Done:** `firmware/code.py` validated against the spec (review + simulator). Next firmware step is the bench (spec §10 T2, T5–T9) when the board arrives.
4. **When parts land:** Phase 1 bench test (04_Wiring checklist, spec §10 tests T1–T9), then carve and integrate (02 §4).
