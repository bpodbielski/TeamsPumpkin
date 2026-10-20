# 02 — Build Plan (v1.3 — DECIDED 2026-09-22)

Status: DECIDED. All decisions in README. Written 2026-09-21, updated 2026-09-22.

## 1. Goal and success criteria

**Goal.** A foam carvable pumpkin on the porch that, when someone walks up, plays a Microsoft Teams sound and lights up a Teams logo — the "Teams-o-lantern" answer to Guy Dupont's Slack-o-lantern — and survives all of October unattended.

**Done means:**
1. Triggers reliably on a person approaching within ~3–4 m; fires **once** per approach (no machine-gun repeats); no false triggers over a night.
2. Sound is clearly audible from the sidewalk (~15 ft); the logo is legible from the street at night (~40 ft).
3. Runs unattended on a wall outlet, always on, for 4+ weeks; recovers by itself from power cuts.
4. Looks intentional in daylight (no dangling wires, no visible electronics), and nothing organic to rot.
5. Total effort fits two weekends; live by ~Oct 4–5.

## 2. Options considered

### 2a. How to render the logo — decision matrix (second pass)

| | **A. Backlit print insert (RECOMMENDED)** | B. Neon line-art (Adafruit 4117 purple + cold-white, or 4310 NeoPixel neon) | C. nOOds strokes (red+blue for "purple") | D. 16×16 LED matrix behind the silhouette window |
|---|---|---|---|---|
| Likeness to the Teams logo | Exact (fills, gradients, white T, people) | Outline only; corners rounded to the strip's bend radius; heads Ø 25–40 mm can't be bent — dots or nOOd loops instead | Outline only; two-tone lines up close; magenta-violet, not indigo | Good: crisp shape from the foam cut, block colors from pixels; chunky T |
| Night look | Illuminated-sign glow, saturated purple, bright T | Neon-sign lines (the Dupont vibe) | Thin neon lines | Glowing pixel icon; can animate (pop-in, unread badge "3") |
| Daylight look | Printed logo in a logo-shaped window | Purple/white silicone lines on the pumpkin | Colored filaments | Grey panel behind the window unless hidden by a white diffuser |
| Electronics | 30 NeoPixels on the Feather terminal | 12 V supply + 1–2 MOSFET modules + 5 V for the Feather (4117), or 5 V addressable at $35/m (4310) | 4–8 filaments, per-filament resistors, one MOSFET | 256 px on the Feather terminal, brightness capped at 25 % |
| Soldering | None | Yes — every cut piece (T bar, T stem, corners) | Resistors + leads | None (panel has a JST/bare lead) |
| Craft risk | Low: one silhouette cut, tape a print | High: grooves for a rigid-in-one-plane strip on a curved surface | Medium | Low–medium: flat plate + diffuser behind the window |
| Logo-related cost | ~$20 | ~$60–80 | ~$60 | ~$20 |
| Fits the Oct 3–4 target | Yes | Doubtful | Marginal | Yes |
| Upgrade path | → D later: same window, same terminal, code change | Dead end | Dead end | — |

**Why the neon strip loses for *this* logo** (it's a fine product): Slack's logo is four strokes, so a stroke-shaped light source is a perfect match. Teams is a filled square with a white T and two filled people. Neon can only draw the outline, the strip's side-bend geometry can't make the T corners or the heads, it bends in one plane so it can't follow the pumpkin's curve, and each cut segment needs soldering plus a second (12 V) supply. You'd do 3× the work for a rougher likeness. If the neon *look* matters more than fidelity, the honest version is a "neon T-tile": one continuous purple 4117 loop as a rounded square (corners ≥40 mm radius) plus a white T from two soldered pieces of cold-white strip, people omitted — that is documented in 03_Parts_List §C.

**Decision: A now, with D as the sanctioned upgrade** (same silhouette window, same NeoPixel terminal; swap the print for a panel on a plate and change `code.py`). D is the route to an *unread-count badge*, which is the funnier escalation for a tech crowd.

### 2b. Controller + audio
| Option | Verdict |
|---|---|
| **Adafruit RP2040 Prop-Maker Feather, CircuitPython (RECOMMENDED)** | One $20 board = MCU + 3 W amp + speaker terminals + NeoPixel terminal with level shifter and switched 5 V + a "Btn" input terminal + servo header (5 V/GND/GPIO). **No soldering** (all screw terminals and a pin header). No SD card, no serial MP3 module. Edit `code.py` on the CIRCUITPY drive from the Mac. Adafruit ships a pumpkin example for this exact board. |
| Arduino Uno/Nano + DFPlayer Mini + speaker + PIR + WS2812B (the transcripts' path) | Works and is well documented, but: 6+ modules, breadboard/soldering, SD formatting, DFPlayer clone quirks, SoftwareSerial upload contention, external 5 V supply with cap/resistor/level shifting. More ways to fail on a porch for a month. Kept as the documented alternative (03_Parts_List §B) — sensible only if Ben already owns an Arduino kit. |
| ESP32-S3 Feather + I2S amp breakout | Adds Wi-Fi (future "real notification" trigger) but needs a separate amp + level shifter + wiring. Not for v1; noted as the upgrade path — everything except the board carries over. |
| Raspberry Pi | Overkill; SD-card corruption risk on nightly power cuts; slow boot. Rejected. |

### 2c. Motion sensor
| Option | Verdict |
|---|---|
| **HC-SR501 PIR (baseline)** | Predictable, tunable delay/range, the tutorials' sensor. Needs its own 24 mm hole for the dome (IR can't pass foam/paper). Avoid direct sun. |
| **RCWL-0516 microwave (test alongside)** | Works *through* the foam — fully hidden, no hole. Risk of through-wall triggering and supply-noise false triggers; mitigate with foil behind it and a clean 5 V. Same firmware. |
| VL53L1X ToF | Needs an optical window and aims a narrow beam. Not needed. |
Decision: buy both PIR and RCWL (≈$10 total), bench-test both, pick the one that behaves on *this* porch.

## 3. Recommended architecture

```
 [5 V / 3 A USB wall adapter] ──(always on)──► USB-C
                                                                    │
 PIR or RCWL ──OUT──► Btn terminal (GPIO19)                          │
   ├── VCC ◄── servo header V+ (switched 5 V)         RP2040 Prop-Maker Feather (CircuitPython)
   └── GND ◄── servo header G                                       │
                                                  ┌─────────────────┴────────────────┐
                                    NeoPixel terminal                        Speaker terminals
                                    5 V / Neo(GPIO21) / GND                       + / −
                                            │                                        │
                              ~30 px WS2812B strip on the                  40 mm 4 Ω 3 W speaker,
                              inside back wall, facing forward             ported through the base
                                            │
                     ┌──────────────────────┴──────────────────────┐
                     │ silhouette-shaped window in the front wall   │
                     │   ← white diffuser sheet                     │
                     │   ← printed transparency of the Teams logo   │
                     └─────────────────────────────────────────────┘
```

Behavior (full spec in 05_Firmware_Spec.md):
- Boot → enable external power → 60 s sensor warm-up (status LED amber, logo dark).
- Idle: logo **off** (decided).
- Motion rising edge (and not in cooldown) → play one ring of the Teams call sound; logo snaps to full white so the print shows in true colors; hold while the sound plays (~3.5 s); fade out over ~1.5 s.
- Cooldown 10 s. If someone is still there when it ends (PIR jumper H keeps the output HIGH while motion continues) → ping again (decided). Any exception → auto-reset. Autoreload off. Always on — no timer.

Upgrade path (v1.5, optional): replace the print with a 16×16 WS2812B panel on a foam-core plate 20 mm behind the same silhouette window; `NUM_PIXELS = 256`, brightness ≤ 0.25, a 16×16 bitmap of the logo, and a red badge digit that increments per trigger.

## 4. Phases, gates, timeline (today = Mon 2026-09-21)

| Phase | When | Work | Gate to pass |
|---|---|---|---|
| **0. Decide & order** | Decided Sep 22; order Sep 22–23 | Order Adafruit board + speaker (~2–4 days to Ohio) and Amazon items (PIR pack, strip, adapter + cable, jumpers, hot knife). Buy the pumpkin locally. Verify the porch outlet. | Everything ordered by Wed Sep 23. |
| **1. Bench electronics** | Parts in hand, target Sat Sep 26–Sun Sep 27 (slip: Oct 3) | Flash CircuitPython UF2; copy `firmware/` contents + `lib/`; wire PIR via jumpers (jumper H, delay pot minimum), strip + speaker via terminals; run self-test; spec tests T1–T9; tune brightness, sensitivity, volume. | 10/10 walk-by triggers at 3 m; 0 false triggers in a 30-min idle; re-ping every ~10 s while waving continuously; board survives a power-cycle and re-arms itself. |
| **2. Pumpkin** | In parallel, Sep 26–Oct 3 | Face measured 2026-10-13 at 178 × 203 mm (7 × 8 in) → logo width set to **125 mm**. Print pages 2–3 (cut silhouette + face layout) on the home laser and page 1 (color insert) at FedEx (2× cardstock + 1× paper); tape the face-layout sheet on and trace; hot-knife the window (3 islands: two heads + body), 24 mm PIR hole low-front (not facing the afternoon sun), speaker port in the base (+3 feet), back hatch with notch; backlight test (stacked cardstock vs paper); mount diffuser + print. | Logo legible at 40 ft when backlit with a flashlight; window edges clean; hatch removable. |
| **3. Integrate** | Sat Oct 3–Sun Oct 4 | Mount board (in a small plastic box or on a foam-core tray), strip on the back wall, speaker at the base port, PIR in its hole; route the USB cable out the hatch; tape the hatch; porch night test; leave it plugged in. | Passes the 5 "done" criteria in §1 at the real porch. |
| **4. Run** | Oct 5–31 | Always on. Weekly 2-minute check (cable, print, false-trigger sanity; PIR sensitivity if animals set it off at night). | Still working on Oct 31. |

Buffer: three-plus weeks between "live" and Halloween. If Adafruit shipping slips, Phase 2 is unaffected.

## 5. Adversarial review log — what the v1 plan got wrong and what changed

I drafted a plan, then attacked it. Changes are already folded into §2–§4 and the other docs.

| # | Attack on v1 | Change made |
|---|---|---|
| 1 | "Copy Dupont: nOOds neon strokes." No purple nOOd exists; the Teams logo is filled shapes; filaments can't be cut to length. | Dropped. Backlit printed insert instead (option A). |
| 2 | A plain square window with a picture inside looks like a lightbox, not a carved pumpkin, in daylight. | Cut the window in the logo's **silhouette** (square + people bumps). It reads as Teams even unlit. Template page 2/4 in `print_template.html`. |
| 3 | Backlit inkjet on plain paper washes out at full brightness — the purple goes pale. | Print on transparency and **stack two copies** (or vellum); do a lit material test before final; idle glow purple (reinforces the purple areas); the white flash is brief. |
| 4 | LEDs around the window rim = bright rim, dark centre; a speaker in the window path casts a shadow on the print. | Strip on the **inside back wall** facing forward (~6–7" throw) with optional white paper lining for bounce; speaker moved out of the light path. |
| 5 | Sound has no way out: foam + paper muffle a 40 mm speaker. | **Speaker port through the base**, pumpkin raised on three 1/2" feet (hot-glued foam offcuts/corks) so sound escapes and reflects off the porch; alternative: a row of 1/4" vent holes hidden low on the back. Sound normalized to −1 dBFS. |
| 6 | A PIR can't see through foam or the print. | Dedicated 24 mm hole low on the front for the dome; **RCWL-0516** bought as the hidden alternative; both use the same active-HIGH pin so firmware doesn't care. |
| 7 | Toggling `EXTERNAL_POWER` to save power (a natural instinct) also cuts the servo V+ that feeds the **PIR** → 60 s re-warm-up and phantom triggers, and it mutes the **amp**. | Firmware rule: `EXTERNAL_POWER` is set HIGH at boot and never turned off. |
| 8 | Boot chatter and re-trigger spam: the PIR outputs garbage for 30–60 s after power-up; a person lingering at the door re-fires every few seconds. | 60 s warm-up gate; **rising-edge** detection; 10 s cooldown; optional "repeat while occupied" flag default off. PIR delay pot at minimum, jumper L. |
| 9 | Any uncaught exception leaves CircuitPython halted → dead pumpkin until someone notices. USB wobble can trigger auto-reload. | `try/except → microcontroller.reset()` around the loop (Adafruit's own pattern); `supervisor.runtime.autoreload = False`. Any power cut is a clean restart (no timer, but outages happen). |
| 10 | Long-uptime timing bugs: `time.monotonic()` is a 32-bit float on RP2040 and loses sub-second resolution after a few hours. | Use `supervisor.ticks_ms()` / `adafruit_ticks` (wraps correctly). |
| 11 | Power: a full-white 30-px strip + amp at 3 W could exceed a weak USB adapter; USB-C-to-C on a PD charger may not negotiate. | 5 V / 3 A **USB-A** adapter + A-to-C cable; flash brightness capped at 70 % (~1.3 A) → worst case ≈ 2 A, inside the 4 A MOSFET and the 3 A adapter. |
| 12 | Weather: a paper insert and an exposed adapter die in the first rain. | Transparency (plastic) print + plastic diffuser; hatch taped; adapter under cover; covered porch confirmed by Ben (outlet to verify). |
| 13 | Sound-file provenance/legality and corporate policy if pulled from a work PC. | Personal-use only; Ben supplied a video-ripped ringtone already; alternatives listed in 06; never commit audio to a public repo. |
| 14 | Trademark. | Personal non-commercial decoration; no merch/sales. Note in `assets/NOTICE.md`. |
| 15 | Carving before the electronics are proven → a carved pumpkin sized for a plan that changes. | Phase 1 bench test gates Phase 3; Phase 2 only depends on the print template, which is fixed once the logo version is chosen. |
| 16 | "The sound" — Ben's file is the **call ringtone** (7.4 s, two rings), not the 1-s message chime the Slack build used. Is a 7 s ring right for a walk-by? | Firmware supports a **list of sounds** (weighted random or sequential). Two cuts prepared: one ring (3.45 s) and two rings (7.2 s). Ben chooses; can add the short "notify" chime later. |
| 17 | Idle-off means a dark blob for most of the month. | Config flag: OFF (max surprise, matches the original) or faint purple breathing (8 %). Ben's call. |
| 18 | The `Btn` terminal might be wired for a button-to-ground with a pull-up; a PIR is push-pull so it's fine, but if GPIO19 misbehaves there's no plan B. | Plan B documented: move OUT to the servo header Sig (GPIO20, plain GPIO). Both are in the wiring doc. |
| 19 | Timeline optimism: everything on one weekend. | Split bench (Sep 26–27) from integrate (Oct 3–4); pumpkin work in between; 3+ weeks of buffer. |
| 20 | Hidden hazard: hot-knifing foam indoors. | Respirator/ventilation step made explicit in Phase 2; do it in the garage or outside. |
| 21 | Second pass — "just use the purple neon strip (4117)". | Verified the product: 12 V, non-addressable, 5 mm edge × 12.2 mm deep side-bend flex, cut every 1" with soldering to reuse pieces. Bend radius too large for the T corners/heads; can't follow the sphere; needs a 12 V supply + MOSFETs. Kept as a documented alternative ("neon T-tile"), not the plan. |
| 22 | "Red + blue nOOds side by side = purple." | Only from a distance or behind a diffuser, and equal drive gives magenta; indigo needs the red at ~¼ current. Documented; rejected. |
| 23 | The addressable neon (4310) removes the 12 V problem — did I dismiss neon too fast? | Re-checked: same side-bend geometry, $35/m, 5.8 A/m at white, and hidden "jumps" through the surface need a twist the strip can't make. Same verdict. |
| 24 | Parking the matrix (D) in v1 threw away the best gag (an unread counter). | Re-instated D as the upgrade path; the v1 window and wiring are chosen so D is a drop-in. |
| 25 | Ben leans toward a glowing look; idle-off may disappoint. | Recommendation flipped to `IDLE_MODE="breathe"` (faint purple) — the pumpkin reads as "Teams" all evening and still pops white on trigger. |
| 26 | A "purple" LED can be a near-UV violet that looks dim and makes whites fluoresce. | Not an issue for A (white LEDs behind a printed purple). Noted for B: check the 4117 photos/reviews before buying; the product photo shows a true violet-purple. |

## 6. Residual risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| RCWL false-triggers from indoor movement through the house wall | Med | Annoying | Foil shield behind it; place pumpkin ≥1 m from the wall; fall back to PIR. |
| PIR false-triggers from sun-warmed surfaces / headlights (always on) | Low–Med | Annoying | Aim the dome down at the walkway and away from the street; sensitivity pot down; covered porch shade. |
| Print looks dull when lit | Med | Cosmetic | Material test in Phase 2; stack two transparencies; raise brightness. |
| Too quiet outdoors | Low–Med | Gag fails | 4 Ω speaker (full 3 W), base port + feet, level 1.0; if still weak, a 3" 4 Ω speaker or vent holes on the front under the logo. |
| Adafruit shipping delay | Low | Schedule | Order first; Phase 2 proceeds regardless. |
| Board doesn't enumerate on a USB-C PD brick | Low | Dead on porch | Use a USB-A brick + A-to-C cable. |
| Kids poke the PIR dome / print | Low | Cosmetic | Dome recessed flush; print taped on all sides inside. |
| Always-on: night-time animals / 6 a.m. joggers set it off | Med | Annoying to neighbors? | Decided and accepted; PIR sensitivity pot down, aim slightly downward toward the walkway; if it becomes a problem, a $10 outlet timer or an `ACTIVE_HOURS` constant can be added later. |
| Always-on: daytime sun on the PIR dome | Low–Med (covered porch) | False pings during the day | Mount the dome so it never sees direct sun or a heat source (vent, grill); covered porch helps. |
| No outlet on the porch (Ben verifying) | ? | Changes the power plan | Option 1: outdoor cord through a window/door gap from inside. Option 2: 20,000 mAh USB power bank that supports "always-on/low-current" mode (idle draw ≈ 0.06 A → ~10 days per charge; ordinary banks auto-off below ~100 mA and would kill it within minutes). |

## 7. Stretch ideas (not in v1)

- **Red notification badge**: one extra pixel behind a 12 mm hole at the logo's top-right, red, lit on trigger and held ~60 s ("1 unread"). Cheap; needs a light-tight tube so it doesn't bleed into the window.
- **PIR dome as the badge**: the 23 mm white dome sitting in a red-painted ring at the badge position hides the sensor in plain sight. Trade-off: no red light there.
- **Sound variety**: 80 % message chime / 15 % ringtone / 5 % "meeting starting now". The mixer already supports it.
- **Real notifications**: swap to an ESP32-S3 Feather + MAX98357 breakout; Power Automate/webhook → Wi-Fi → pumpkin. Corporate tenants will almost certainly block the outbound hook; personal Teams could work. Everything but the board carries over.
- **LED matrix face** (option D) for a "screen" look with animated badge counts.
