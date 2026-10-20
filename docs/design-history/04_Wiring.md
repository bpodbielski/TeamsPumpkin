# 04 — Wiring (Prop-Maker Feather path)

No soldering. Everything lands on the board's screw terminals or the 3-pin servo header.

## Before you wire: prepare the LED strip

The BTF-LIGHTING strip ships as **60 LEDs with a 3-pin JST connector pre-installed on each end** plus a loose 3-pin male pigtail with flying leads. We only use 30 pixels (`NUM_PIXELS = 30`), so:

1. **Find the input end.** Arrows printed on the strip show the data direction; the input end is the one the arrows point *away* from. The included pigtail plugs into that end and gives you three bare wires — **no cutting or soldering needed for the connection.**
2. **Cut at the 30th LED**, on the copper-pad line between pixels (scissors are fine).
3. **Keep the half that still has the input connector.** The other half is a spare; using it later would mean soldering to its cut pads.
4. Strip ~5 mm of insulation on the pigtail's three wires if they aren't pre-tinned, and land them per the table below.

> **Do not just wire up all 60 pixels.** At `NOTIFY_BRIGHTNESS = 0.70`, 60 px draw ≈ 2.5 A; add the amplifier and the board and you exceed the 3 A adapter. If you ever do want all 60, set `NOTIFY_BRIGHTNESS ≤ 0.35` first.

## Tools you need at the bench (not electronics)

| Tool | For |
|---|---|
| **Small flat-blade screwdriver (~2 mm, eyeglass-kit size)** | The Prop-Maker's screw terminals — strip, speaker and sensor all land there. Easy to forget and it stops the build dead. |
| Scissors or side cutters | Cutting the strip at the 30-LED mark |
| Wire strippers (or careful scissors) | ~5 mm off the pigtail leads if needed |
| Hot glue gun | Mounting board, strip, speaker, diffuser |

## Verified physical layout (from Ben's board and sensor photos, 2026-10-17)

- **Terminal block**, front of the board, right edge, from the top (the end nearest the SDA pin): **Neo, G, 5V, Btn, −, +**. The labels are printed on the BACK of the board. There is only one ground (`G`) on the block.
- **Servo header**, just left of the block, from the top: **G, V+, Sig**.
- **HC-SR501**, component side with the pins at the top: pins **GND, OUT, VCC** left to right; jumper on the left edge (**H** upper, **L** lower); dials along the bottom: **range** (left), **delay** (right).

## Connections

| From | To (on the Prop-Maker Feather) | Wire | Notes |
|---|---|---|---|
| PIR **VCC** (or RCWL **VIN**) | Servo header **V+** | F-F jumper | Switched 5 V (from USB). HC-SR501 needs ≥4.5 V; RCWL 4–28 V. |
| PIR **GND** (or RCWL **GND**) | Servo header **G** | F-F jumper | |
| PIR **OUT** (or RCWL **OUT**) | Screw terminal **Btn** (GPIO19, `board.EXTERNAL_BUTTON`) | M-F jumper, male end clamped in the terminal | 3.3 V logic from both sensors — safe for the RP2040. **Plan B:** servo header **Sig** (GPIO20, `board.EXTERNAL_SERVO`) if GPIO19 misbehaves. |
| LED strip **5V** (red) | NeoPixel terminal **5V** | strip lead | |
| LED strip **DIN / Data** (green/white) | NeoPixel terminal **Neo** (GPIO21, `board.EXTERNAL_NEOPIXELS`) | strip lead | Connect at the strip's **input** end — follow the arrows printed on the strip. Level-shifted to 5 V on the board. |
| LED strip **GND** (white/black) | NeoPixel terminal **GND** | strip lead | |
| Speaker **+** | Speaker terminal **+** | speaker lead (**only ~9 cm long** — mount the board within a few inches of the speaker, or splice an extension) | 4–8 Ω. Polarity only matters with two speakers. |
| Speaker **−** | Speaker terminal **−** | speaker lead | |
| Wall adapter 5 V / 3 A (USB-A) | **USB-C** jack | A-to-C cable | Always on (decided: no timer). |

Software-controlled on the board (no wire): **GPIO23 `board.EXTERNAL_POWER` → HIGH at boot, never LOW** — it feeds the NeoPixel 5 V, the servo header V+ (i.e. the sensor) and enables the amplifier.

## Diagram

```
                    ┌───────────────────────────────────────────────┐
  USB-A 5V/3A ─────►│ USB-C                                         │
  (always on)       │                                               │
                    │      Adafruit RP2040 Prop-Maker Feather       │
                    │                                               │
   HC-SR501 PIR     │  Servo header      Terminals                  │
   ┌─────────┐      │   Sig  V+  G       5V  Neo  GND  Btn  GND  + − │
   │ VCC ────┼──────┼─────── ┘   │        │   │    │    │         │ │ │
   │ GND ────┼──────┼───────────┘         │   │    │    │         │ │ │
   │ OUT ────┼──────┼───────────────────────────────────┘         │ │ │
   └─────────┘      └────────────────────────────────────────────────┘
                                          │   │    │              │ │
                        WS2812B strip     │   │    │      40 mm   │ │
                        (≈30 px, 5 V)  ◄──┘   │    │      4 Ω    ◄┘ │
                         5V ◄─────────────────┘    │      speaker ◄──┘
                         DIN ◄─────────────────────┘
                         GND ◄──── (strip GND)
```
(Terminal order on the physical block may differ from the sketch — go by the silkscreen labels.)

## Sensor settings (HC-SR501) — decided
- **Time-delay pot**: fully counter-clockwise (shortest, ~3 s). Firmware owns the cooldown.
- **Sensitivity (range) pot** — the LEFT pot with the pins at the top: start at the middle (~5 m). Per Ben's reference card, clockwise = shorter (~3 m), counter-clockwise = longer (~7 m); clone boards sometimes run the other way, so confirm with a walk test on the porch.
- **Jumper**: **H (repeat trigger)**. With H, the output stays HIGH as long as motion keeps occurring (+~3 s after it stops), so the firmware can re-ping every 10 s while someone stands at the door and go quiet as soon as they leave. (L would also work via rising edges, but H makes the "still here" check level-based and reliable.)
- Mount the dome flush in a 24 mm hole low on the front, aimed slightly down at the walkway; never facing direct sun, a dryer/HVAC vent or a grill (always-on means daytime false triggers would be audible).

## Sensor settings (RCWL-0516) — NOT purchased; fallback only if the PIR misbehaves
- No pots. Optional: solder pads for a range-reducing resistor (R-GN) — not needed at first.
- Mount inside, flat against the front inner wall (it detects through foam). Put a 3"×3" square of aluminum foil behind it (between sensor and the back of the pumpkin) if it triggers from indoor movement.
- Add a 10 µF capacitor across VIN/GND if it chatters (rare with a decent USB brick).

## Power budget (5 V rail)
| Load | Idle | Notification peak |
|---|---|---|
| RP2040 board + regulator | ~0.05 A | ~0.05 A |
| PIR (~65 µA) / RCWL (~3 mA) | ~0 | ~0 |
| Amplifier, 3 W into 4 Ω | ~0.01 A | ~0.7 A |
| 30 × WS2812B, purple @ 8 % (idle breathing option) | ~0.10 A | — |
| 30 × WS2812B, white @ 70 % cap | — | ~1.26 A |
| **Total** | **~0.15 A** | **~2.0 A** |

Fits a 5 V/3 A adapter with margin; well under the board's 4 A external-power MOSFET. Keep the USB cable ≤6 ft and reasonably thick (voltage drop shows up as a slightly pink "white").

## Bench-test checklist (Phase 1)
1. Board alone on USB → CIRCUITPY drive appears; `code.py` runs (status LED changes state).
2. Add speaker → self-test plays the WAV at full volume with no distortion.
3. Add strip → white flash / fade runs; check no pixel is off-color (data direction, GRB order).
4. Add PIR → after the 60 s warm-up, a hand wave triggers exactly one event; serial prints "TRIGGER".
5. Swap in RCWL → same, then walk around the room to see what else sets it off.
6. Pull the USB plug and reconnect → it re-arms by itself with no keyboard/screen.
