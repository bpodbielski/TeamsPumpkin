# 01 — Research Notes

Synthesis of the four video transcripts Ben pulled, plus web research done 2026-09-21. Facts are labeled by source; anything not sourced is my inference and is marked as such.

---

## A. The reference build: Guy Dupont's "Slack-o-lantern" (Oct 20, 2025)

What is publicly known (news coverage + his own replies):
- A **real, carved pumpkin** with the Slack logo carved into the face; a **motion sensor** and a **speaker**; on motion it plays the Slack notification sound and the logo lights up. 3.1M TikTok views; he smashed it on video the next day.
- The logo lighting was **Adafruit "nOOds"** — flexible LED filaments. Dupont's reply (quoted in coverage): the light strands "run on 3V and are crazy bright, sold by Adafruit under LED noodles."
- His follow-up video is titled "RIP Slack-o-lantern: **Arduino**-Powered Halloween Fun" → an Arduino-class microcontroller.
- Commenters explicitly asked for a **Teams version** ("the Teams sounds are all way more terrifying").

Why the nOOds approach fit Slack but not Teams (my analysis):
- The Slack logo is four colored *pill strokes*; nOOds are 300 mm colored *strokes* (red, blue, lime green, yellow, pink, warm white). Perfect match.
- The Teams logo is *filled shapes* (an indigo rounded square with a white T, plus two purple people). nOOds don't come in purple, can't be cut, and can't render a filled square. → We render the logo differently (see 02_Build_Plan).

Sources:
- https://www.dailydot.com/news/man-designs-slack-o-lantern/
- https://x.com/gvy_dvpont/status/1980288192042693004
- https://www.tiktok.com/@guy_dupont/video/7563792244872842551 ("RIP Slack-o-lantern: Arduino-Powered Halloween Fun")
- https://www.adafruit.com/product/5506 (nOOds: 3 V nominal, up to 200 mA at 3 V, run at ≤50 mA with a resistor; 300 mm; colors listed above; no purple)

---

## B. Transcript 1 — SKS Props, "Carve, Paint & LED-Light a Retail Foam Pumpkin" (Oct 2020)

Pumpkin: **Holiday Living 13" Carvable Pumpkin from Lowe's** (foam, carvable). Also sold at craft stores.

Process that worked:
1. Pick one with no dents/tears. There is a **seam** up one side — **measure the usable face** before designing so the artwork fits.
2. Draw the design on bristol board, cut a template with a utility knife, tape to the pumpkin, **transfer with a pencil** (pressing lightly into the foam leaves a visible line).
3. Also cut a **back hatch** template so lights can be inserted; cut a **small notch** at the bottom of the hatch so it can be pulled out.
4. Cut with a **multi-temp hot knife** (Walnut Hollow) on the **highest** temperature. Plunge the tip in a corner, make sure it's all the way through, follow the line. Clips were at 2× speed — it goes fast and cuts are very clean.
5. **Respirator + well-ventilated area** — heating foam makes fumes.
6. Push cut pieces inward with a sculpting tool; sand any melt build-up with sandpaper.
7. Optional: airbrush weathering (Createx transparent orange/red into the low spots), Dremel texture on the stem, raw umber dry-brushing at the stem base. Cosmetic only.
8. Lighting: an LED **mist fogger failed** (water ran out in ~2 min). A **sticky-back LED coil** worked. **A plain sheet of paper taped inside** diffused the light evenly across the whole face.

Takeaways we adopt: measure the face first; paper/bristol template → pencil transfer; hot knife at max temp; back hatch with notch; **internal diffuser sheet**; ventilation.

---

## C. Transcript 2 — Rachel De Barros, "Program LED Strips with Arduino + FastLED" (Apr 2024)

WS2812B strip facts:
- Three wires: GND, **data**, 5 V (some strips duplicate GND/5 V). **Data flows in the direction of the arrow** printed on the strip — connect the controller at the input end.
- 5 V strips are easiest to power; 12 V strips only help on long runs. **Never power a strip from the Arduino's 5 V pin**; use a separate 5 V supply with a **common ground**.
- Put a **large electrolytic capacitor** across the strip's power and a **330–470 Ω resistor** in series with the data line (protects the first pixel from spikes).
- FastLED setup: `#define NUM_LEDS`, data pin, `CRGB leds[NUM_LEDS]`, `FastLED.addLeds<WS2812B, PIN, GRB>(leds, NUM_LEDS)`, `setBrightness(0–255)`, `FastLED.show()`. Color order for WS2812B is **GRB**.
- Animations are just loops: single-pixel scanner, chaser, `fill_solid`, `fill_gradient_RGB` (2 or 4 colors — 3 has a bug), `fill_rainbow` with a moving start hue.

Takeaways: GRB color order; the power rules; if we go the Arduino route we need the cap/resistor/level shifting. On the Prop-Maker Feather the 5 V level shifter and switched 5 V power are on the board, and CircuitPython's `neopixel` library replaces FastLED.

---

## D. Transcript 3 — Rachel De Barros, "Motion-activated MP3 with PIR + DFPlayer Mini + Arduino" (Apr 2024)

PIR sensor (HC-SR501 style):
- Pins **VCC / OUT / GND** (pop the dome off to read the labels).
- **Time-delay pot**: fully counter-clockwise = output stays HIGH the shortest time (~3 s); fully clockwise ≈ 5–10 min depending on model.
- **Sensitivity pot**: range ~3 m to ~7 m.
- **Jumper**: L = single trigger (locks HIGH for the delay period, ignores motion meanwhile); H = repeat trigger (the timer restarts on every new motion while HIGH).
- **Needs 30–60 s to calibrate at power-up** — give it a startup delay or the prop "goes crazy".
- Code pattern: read the pin every loop; track a `pirState` label; act on the **LOW→HIGH transition only** ("option 2") so the sound plays once per event, not continuously.

DFPlayer Mini:
- Pins: VCC (5 V), RX, TX, SPK1, GND, SPK2 (speaker wires sandwich the GND pin). 2 W 8 Ω speaker; micro-SD (FAT32; up to 32 GB), files named `0001.mp3`…
- The Uno's hardware serial is shared with USB upload → either unplug the module every upload, or use **SoftwareSerial** on pins 2/3. A **1 kΩ resistor on the module's RX** softens noise.
- Library `DFRobotDFPlayerMini`; `player.begin(fxSerial)`, `volume(0–30)`, `play(n)`; sequential and `random()` track patterns.

Takeaways: PIR settings (delay pot to minimum, jumper L, sensitivity mid, sensor warm-up gate) and the **edge-detection** logic carry straight into our firmware. The DFPlayer quirks (SD formatting, clone chips, serial contention) are the main reason we prefer a board with audio built in.

---

## E. Transcript 4 — BMonster Laboratory, "Motion-Activated MP3 with DY-HV20T + Arduino Mega" (Nov 2024)

- DY-HV20T MP3 module (≈$13; 7 selectable modes via DIP switch; **UART mode = switches 1,2 down / 3 up**), 3.5 mm line out to a Bluetooth speaker for better sound; needs **~7–35 V** supply (he used a 9 V battery), separate from the Arduino.
- **BUSY pin** read by the Arduino so a new track isn't started while one is playing.
- Random track selection; a re-trigger timer to avoid firing again too soon after a track ends.
- Practical warning: **a PIR in direct sun can false-trigger** — keep it in shade.

Takeaways: check an "is playing" state before retriggering; the sun/heat caveat for PIR placement; the DY family (DY-SV17F etc.) is a fallback if we ever need line-out into a bigger amp.

---

## F. Web research — hardware facts used in the plan

### Adafruit RP2040 Prop-Maker Feather (product 5768) — $19.95, in stock 2026-09-21
- RP2040 @ 133 MHz, 8 MB flash, USB-C, LiPo charger, STEMMA QT; **CircuitPython** supported (dedicated board build).
- **MAX98357 I2S 3 W class-D amp** on board → screw terminals for a **4–8 Ω speaker, up to 3 W**. I2S pins: data GPIO16, bit clock GPIO17, word select GPIO18.
- **NeoPixel screw terminal** with a **5 V level shifter** on the data line (GPIO21, `board.EXTERNAL_NEOPIXELS`) and switched 5 V power. The 5 V comes from USB or the LiPo, whichever is higher.
- **External power switch**: GPIO23 `board.EXTERNAL_POWER`; off by default; must be set HIGH to power the NeoPixel terminal, the servo header V+, **and the amplifier**. Adafruit forum staff answer: the MOSFET is rated **4 A**.
- **Btn screw terminal**: GPIO19 `board.EXTERNAL_BUTTON` — "extra digital input or output pin".
- **Servo header** (3 pins, 0.1"): Sig = GPIO20 `board.EXTERNAL_SERVO`, V+ = the same switched 5 V, G = ground.
- 3.3 V regulator 500 mA peak. "Comes assembled and tested, with some header" (the Feather-edge headers are loose; we don't need them — everything we connect uses the screw terminals and the servo header).
- Adafruit's own guide for this board includes a pumpkin project (VL53L1X distance sensor + audio + servo), which is our code template (see `reference/`).
Sources: https://www.adafruit.com/product/5768 · https://learn.adafruit.com/adafruit-rp2040-prop-maker-feather/pinouts · https://forums.adafruit.com/viewtopic.php?t=205873 · https://learn.adafruit.com/propmaker-jack-o-lantern

### CircuitPython audio format
Adafruit's example mixer is configured `sample_rate=22050, channel_count=1, bits_per_sample=16, samples_signed=True` → WAV files must be **16-bit signed PCM, mono, 22,050 Hz** (44,100 Hz also works on RP2040 if ever needed for fidelity, at the cost of CPU/RAM headroom).

### Microsoft Teams logo (two versions in circulation)
- **2019–2025 "classic"**: indigo rounded square (gradient #5A62C3 → #4D55BD → #3940AB) with a white T; large person in #7B83EB and a smaller person in #5059C9 to the right. This is the icon most people picture when they think "Teams".
- **2025–present**: two people (blue-violet gradients, e.g. #85C2FF → #7588FF → #6459FE and #A98AFF → #5F50E2 → #3C2CB8) with a small indigo T tile (#688EFF → #230F94) at the bottom-left. Current app icon.
Both SVGs are in `assets/` (from Wikimedia Commons). Exact geometry is in 06_Logo_and_Sound_Assets.md.

### Teams notification sounds
- New Teams on Windows keeps its sounds as MP3s in `C:\Program Files\WindowsApps\MSTeams_<version>\Audio\` (a protected folder; needs admin/ownership to browse). The classic Teams client kept them inside `%LOCALAPPDATA%\Microsoft\Teams\current\resources\app.asar` under `assets\audio`.
- Ben already supplied `TeamsCallSound.mp3` (the incoming-call ringtone, 12.1 s stereo MP3 ripped from a video). Converted, trimmed, normalized WAVs are in `assets/`.
Sources: https://learn.microsoft.com/en-us/answers/questions/4412679/there-is-any-way-to-change-the-sound-of-teams-noti · https://scribbleghost.net/2018/10/25/microsoft-teams-ringtones-and-notification-sounds/

### Foam carvable pumpkins (all in stores now, late September)
- **Lowe's Holiday Living 13" Carvable Pumpkin** (orange; listing dims 12.8" H × 9.25" W × 9.06" D) — the exact one SKS Props used; budget-friendly.
- **Funkins "Classic" 13.5"** — the premium, most realistic carvable foam pumpkin (funkins.com; also resold via Walmart/Amazon). Thicker, sturdier walls; pricier.
- **Michaels (Ashland) craft/carvable pumpkins** — several sizes/colors.
Sources: https://www.lowes.com/pd/Holiday-Living-12-8-in-Pumpkin-Craft-Pumpkin/5014043077 · https://funkins.com/ · https://www.michaels.com/shop/holidays-occasions/halloween/pumpkin-decor

### Sensors
- **HC-SR501 PIR**: 4.5–20 V in, **3.3 V logic out**, adjustable delay/range, needs line-of-sight through its dome — **cannot see through foam or paper**. ~$2–4 each.
- **RCWL-0516 microwave Doppler sensor**: 4–28 V in, 3.3 V logic out (HIGH ≈ 2 s per detection), ~5–7 m range, **detects through foam/plastic/paper** so it can be fully hidden inside the pumpkin. Downsides: also detects through walls/windows behind it (shield the back with foil or keep the pumpkin off the house wall), and it is sensitive to noisy power supplies. ~$2 each. Same firmware interface as the PIR (active-HIGH pulse).
- **VL53L1X time-of-flight** (Adafruit's pumpkin used it): precise distance but narrow beam and needs a clear optical window; ~4 m max. Not needed for a walk-by trigger.

### Hot knife
- Walnut Hollow "Hot Knife" / Creative Versa-Tool (the tool in the SKS video) — proven on this exact foam. A sharp craft knife or a pumpkin saw also cuts foam pumpkins (Funkins recommends ordinary carving tools); the hot knife just leaves cleaner edges.

---

## G. Second pass (2026-09-21, evening) — neon strips, nOOd color mixing, LED matrix

### Adafruit 4117 "Flexible Silicone Neon-Like LED Strip – 1 Meter – Purple" (Ben's candidate)
Verified on the product page: **$13.95, 33 in stock**; **12 V DC** (9 V dim, 12 V full), **0.8 A per meter**, 120 SMD2835 LEDs/m (~8 mm pitch), **single color, non-addressable** (the whole strip is on or off), IP65 silicone, two bare power wires, "you can cut every 1" (2.5 cm) by looking at markers on the back side", "you might end up breaking one or two LEDs in the process". Family: Ice Blue, Pink, Cold White, Warm White, Blue, Green, Red, Purple, plus an RGB (12 V, 3-channel) version.
From the product photos (cross-checked against the 1,000 × 12.2 × 5.0 mm spec): the light exits a **5 mm-wide edge**; the body is **12.2 mm deep**; the strip **stands on edge and bends in the plane of the surface** ("side-bend" neon flex). The photo loop is ~120 mm radius; no minimum bend radius is published — assume ~40–60 mm like other side-bend flex until tested. Because it bends *only* in that plane, it cannot also follow the pumpkin's spherical curvature; over a 100 mm run on a 13" pumpkin the surface falls away ~7 mm at the ends, so it would have to sit in a groove or float off the surface.
Consequences for a Teams logo at 120–150 mm: the T's inside corners and the round heads (Ø 25–40 mm) are far below the bend radius → **cuts** at each corner/segment; every cut piece needs two wires **soldered** to the pads inside the silicone; a 12 V supply plus a MOSFET per color channel to switch/fade from the Feather (which itself needs 5 V).

### Adafruit 4310 "Flexible Silicone Neon-like Skinny NeoPixel LED Strip" (addressable cousin)
$34.95, in stock, **5 V**, 96 WS281x pixels/m, 12 × 6 mm cross-section, JST-SM 3-pin input, removable IP65 sleeve, cuttable. Addressable → purple and white on one strip and animations from the Prop-Maker terminal, with no 12 V/MOSFETs. Same side-bend geometry limits; ~5.8 A/m at full white so brightness must be capped. Reusing a cut piece still means soldering. (Its RGB tube sibling is product 3869.)

### Can red + blue nOOds side by side make purple?
Physics: additive mixing needs the two lights to overlap on the retina or a diffuser. Two 2.4 mm filaments 3–5 mm apart blend into one line only from far away or behind a diffuser; up close they read as a red line beside a blue line. Color: equal-current red + blue gives **magenta** (hue ≈ 300°); Teams indigo #5059C9 is hue ≈ 235°, i.e. mostly blue with a little red. Since the eye is ~3–4× more sensitive to 625 nm red than 470 nm blue, the red nOOd would have to run at roughly a quarter of the blue's current (≈12 mA vs 50 mA) to land near violet — tunable with resistors, but it doubles the filament count, and nOOds cannot be cut (300 mm fixed). Verdict: possible as a magenta-violet approximation; not worth it when a purple neon strip exists and neither fits a filled-shape logo anyway.

### 16 × 16 WS2812B flexible matrix (the "screen" option, re-examined)
General facts (not vendor-verified this session): 256 pixels on a 160 × 160 mm flexible PCB, 5 V, ~$15–20 (BTF-Lighting and similar; Adafruit's version is ~$50). Worst case 15 A at full white, so brightness is capped at ~25 % (≈1 A for a purple/white logo). Drives from the Prop-Maker NeoPixel terminal as one 256-pixel strip. Mounted flat on a foam-core plate ~20 mm behind the silhouette window with a paper/vellum diffuser, it supplies the *colors* (purple fills, white T, red badge with a digit) while the foam cut supplies the crisp *shape*. Daylight look is a grey panel behind the window unless a white diffuser hides it.
