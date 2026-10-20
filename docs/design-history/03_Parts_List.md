# 03 — Parts List (BOM)

Prices are Sept-2026 estimates unless marked "verified". Verified = seen on the vendor page on 2026-09-21.

> **Superseded for ordering by [07_Order_List.md](07_Order_List.md)** (live prices + exact ASINs, checked 2026-09-23). This file stays as the reasoning behind each choice and the alternative build paths.

## Shopping list for today (decided 2026-09-22)

**Adafruit cart** (adafruit.com; ships from NYC, 2–4 days):
- 1× Adafruit RP2040 Prop-Maker Feather — PID 5768 — https://www.adafruit.com/product/5768 — $19.95
- 1× Speaker 40 mm 4 Ω 5 W — PID 3968 — https://www.adafruit.com/product/3968 — ~$5

**Amazon cart** (search terms; pick well-reviewed listings):
- "HC-SR501 PIR motion sensor" (2–5 pack) — ~$8
- "WS2812B LED strip 5V 60 LEDs/m 1m IP30" (e.g. BTF-Lighting) — ~$10
- "Dupont jumper wires female-female male-female 20cm" (kit) — ~$5
- "USB wall charger 5V 3A USB-A" + "USB-A to USB-C cable 6 ft" — ~$12
- "Walnut Hollow Hot Knife" (or "Creative Versa-Tool") — ~$30
- Optional: "respirator half mask organic vapor" if you don't own one — ~$20

**Lowe's**: Holiday Living 13" Carvable Pumpkin (orange) — ~$20. Check it for dents; note the seam.

**FedEx Office**: **page 1** of `assets/print_template.html` — 2 copies on white cardstock + 1 on plain paper, color, 100 % scale. **Home laser**: **pages 2 and 3** (cut silhouette + full-size face layout).

**Already have / from the garage**: hot glue gun, craft knife, ruler, pencil, packing tape, card stock, 220 sandpaper, a small plastic container for the board, an outdoor extension cord.


## A. Recommended path — Prop-Maker Feather (no soldering)

### Electronics
| # | Item | Qty | Est. price | Source | Notes |
|---|---|---|---|---|---|
| 1 | **Adafruit RP2040 Prop-Maker Feather** (PID 5768) | 1 | **$19.95 (verified, in stock)** | adafruit.com (also Digi-Key/Mouser/Adafruit's Amazon store) | MCU + 3 W amp + NeoPixel driver. Feather-edge headers are loose and not needed. |
| 2 | **Speaker, 40 mm, 4 Ω, 3–5 W** (Adafruit PID 3968 or any "40 mm 4 ohm 3 W" 2-pack) | 1 | $5–8 | Adafruit / Amazon | 4 Ω gets the full 3 W from the amp. Bare wire leads go straight into the screw terminals. |
| 3 | **WS2812B 5 V LED strip, 60 LEDs/m, 1 m, IP30 (non-waterproof)** | 1 | $8–12 | Amazon (BTF-Lighting etc.) or Adafruit PID 2508 ($25) | Cut to ~30 px. Must be 5 V type. Bare-wire or JST-SM lead — bare wires into the terminal. |
| 4 | **HC-SR501 PIR sensor** (usually 2–5 pack) | 1 | $6–10 / pack | Amazon | Baseline sensor. |
| 5 | ~~RCWL-0516 microwave sensor~~ | 0 | — | — | **Not needed — decided PIR.** Documented in 04_Wiring as a fallback if the PIR misbehaves on this porch. |
| 6 | **Jumper wires**: 2× female-female + 1× male-female, ~20 cm | 1 set | $5 | Amazon (any 120-pc kit) | PIR → servo header (F-F) and PIR OUT → Btn screw terminal (M-F). |
| 7 | **USB wall adapter 5 V / 3 A, USB-A** + **USB-A→USB-C cable 3–6 ft** | 1 each | $10–14 | Amazon | Avoid USB-C PD bricks (negotiation ambiguity). |
| 8 | ~~Outdoor outlet timer~~ | 0 | — | — | **Not needed — decided always-on.** Add later only if night-time animal pings become a problem. |
| 9 | **Outdoor-rated extension cord** (if the porch outlet is far) | 1 | $10–20 (may already own) | — | Keep the adapter under cover. |
| 10 | Optional: small plastic food container / project box for the board | 1 | $2 | — | Keeps foam dust and drips off the board. |

Electronics subtotal: **≈ $60–75** (no timer, no RCWL)

### Pumpkin, tools, consumables
| # | Item | Qty | Est. price | Source | Notes |
|---|---|---|---|---|---|
| 11 | **Foam carvable pumpkin ~13"** — Lowe's *Holiday Living 13" Carvable* (orange) **or** Funkins *Classic 13.5"* (premium) | 1 | $15–25 (Lowe's) / $50–80 (Funkins) | Lowe's / Michaels / funkins.com | Dent/tear-free; note the seam; usable flat face ≈ 5–6" wide. Buy 2 if you want a practice cut. |
| 12 | **Hot knife** — Walnut Hollow Hot Knife / Creative Versa-Tool | 1 | $25–35 | Amazon / Michaels / Hobby Lobby | The tool proven on this foam. A sharp craft knife + pumpkin saw is the no-buy fallback. |
| 13 | **Respirator** (or at minimum: garage door open + fan) | 1 | $15–30 (may own) | — | Hot foam fumes. |
| 14 | **FedEx Office color prints of page 1**: 2× cardstock + 1× plain paper | 1 visit | $3–5 | FedEx Office | Home printer is B&W laser → it prints pages 2–3. Stack the two cardstock copies for saturated purple. |
| 15 | **White translucent diffuser**: inkjet vellum sheets *or* a white translucent poly folder / cutting-mat offcut | 1 | $3–8 | Office/craft store | Goes behind the print. Plain paper works but isn't weatherproof. |
| 16 | **Hot glue gun + sticks**, **clear packing tape**, **pencil**, **ruler**, **card stock/bristol board** for templates, **sandpaper (220)** | — | $0–15 (mostly owned) | — | |
| 17 | Optional cosmetics: acrylic paints (raw umber, purple) for weathering / a painted badge ring | — | $5–10 | Michaels | Skip for v1. |

All-in estimate: **≈ $120–150** with the Lowe's pumpkin and a new hot knife; ≈ $95 if the respirator and glue gun are already in the garage.

### Order plan
- **Adafruit** (ships from NYC, typically 2–4 days): items 1, 2 (and 3 if you want the Adafruit strip).
- **Amazon**: items 3, 4, 6, 7, 12 (+13 if needed).
- **Local**: 11 (Lowe's), 14 (FedEx), 15–17.

---

## B. Alternative path — Arduino (the transcripts' approach)

Only if Ben already owns most of this. Not recommended for a month-long porch deployment.

| Item | Qty | Est. price | Notes |
|---|---|---|---|
| Arduino Uno R3 or Nano (Every) | 1 | $10–28 | Nano fits inside more easily. |
| DFPlayer Mini MP3 module (genuine DFRobot preferred over clones) | 1 | $5–10 | Needs micro-SD (FAT32), files `0001.mp3`… |
| Micro-SD card ≤32 GB | 1 | $7 | |
| 3 W 4–8 Ω speaker | 1 | $5 | DFPlayer's amp is ~3 W into 4 Ω (quality varies by clone). |
| HC-SR501 PIR | 1 | $3 | |
| WS2812B 5 V strip 1 m | 1 | $10 | |
| 5 V 3 A power supply with barrel jack + DC jack adapter | 1 | $12 | Powers the strip and the Uno's 5 V pin (via VIN is wrong for 5 V — use the 5 V pin or USB). |
| 1000 µF electrolytic cap, 470 Ω resistor, 1 kΩ resistor, 74AHCT125 level shifter (recommended for 5 V data) | 1 each | $8 (kits) | Per the FastLED video + Adafruit's NeoPixel Überguide. |
| Breadboard + jumper kit | 1 | $10 | Or solder to protoboard for porch reliability. |
| Libraries | — | free | FastLED, DFRobotDFPlayerMini, SoftwareSerial. |

Subtotal ≈ $70–95, plus a soldering iron for anything that must survive outdoors. Code sketch outline: PIR edge-detect (transcript 3) + `fxPlayer.play(1)` + a FastLED white flash/fade (transcript 2); mind the busy pin (transcript 4).

---

## C. Alternative — "neon T-tile" (only if the neon look outranks logo fidelity)

Adds to §A (keep the Feather, sensor, speaker; drop the print, diffuser, NeoPixel strip):
| Item | Qty | Est. price | Notes |
|---|---|---|---|
| Adafruit 4117 Flexible Silicone Neon-Like LED Strip, 1 m, **Purple** | 1 | $13.95 (verified) | One continuous rounded-square loop (~90–110 mm sides, corners ≥40 mm radius); excess dives into the pumpkin. Runs at 12 V, 0.8 A/m. |
| Adafruit 3865 same strip, **Cold White**, 1 m | 1 | $13.95 | Cut two pieces at the 1" marks for the T bar and stem; **solder** two leads to each piece's pads; seal with hot glue. |
| Logic-level MOSFET driver modules with screw terminals (e.g. Adafruit 5648 or IRLZ44N breakout) | 2 | $5–12 each | One per color channel, gate from a Feather GPIO (PWM for fades); common ground with the Feather. |
| 12 V / 2 A DC adapter + 2.1 mm jack-to-terminal adapter | 1 | $10 | Second wall adapter (the Feather stays on 5 V USB), or a 12→5 V buck module. |
| Soldering iron, solder, heat-shrink | — | $20–40 if not owned | Non-negotiable for this route. |
| Larger flat face: Funkins 13.5"–16" pumpkin | 1 | +$30–60 | A 13" Lowe's face is too curved for 100 mm straight runs of a strip that only bends one way. |
Delta ≈ +$70–120 and a soldering skill requirement; people omitted (or two purple nOOd loops, +$15, +2 resistors).

## D. Upgrade — 16×16 matrix behind the same window (v1.5)

| Item | Qty | Est. price | Notes |
|---|---|---|---|
| WS2812B 16×16 flexible panel, 160 × 160 mm, 5 V (BTF-Lighting or similar) | 1 | $15–20 | Replaces the print insert and the 30-px strip; same NeoPixel terminal. Cap brightness at 25 %. |
| Foam-core or corrugated plastic plate ~180 × 180 mm + vellum diffuser | 1 | $5 | Panel glued flat to the plate, plate hot-glued inside ~20 mm behind the window. |
| (unchanged) 5 V/3 A adapter | — | — | ≈1 A at 25 % for a purple/white logo. |
Code delta: a 16×16 bitmap of the logo, `NUM_PIXELS = 256`, an unread-badge digit that increments per trigger and resets at boot.
