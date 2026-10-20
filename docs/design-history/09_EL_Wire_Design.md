# 09 — EL Wire Outline (DECIDED 2026-10-15)

> **Superseded in part by `10_Build_Changes.md` (2026-10-17):** the strip is now 2 px in a light box (not 30 px), so the §7 power budget drops to ~1.3 A; the EL route and hole positions are in print-template page 4; the module's input +/− twist into the board's 5V/G terminals with the strip's wires.

**Context.** Ben's hot knife left a partial-depth outline groove in the face, and the groove reads clearly as the Teams logo. The glow test was run on 2026-10-15: **the thinned foam does NOT transmit light**, so the relief-glow option is dead. Decision: use the groove as a channel for purple EL wire, keep the NeoPixels for a through-cut white T.

**Design: hybrid.** Purple EL wire traces the outlines (two heads, body, T-tile). The white **T glyph is cut all the way through** and backlit white by the existing 30-pixel strip. Both fire together with the ringtone.

Why the T isn't EL: EL wire's minimum bend radius is ~10 mm. On a 24 mm-wide bar that makes the T's square corners look blobby. A through-cut gives crisp corners and the brightest element in the logo.

---

## 1. Why this works now (the objection that dissolved)

I originally rated the inverter whine a blocker for a sound-based gag. It isn't, because of the trigger design: **the inverter is only powered during the notification**, ~3.5 s, while the Teams ringtone plays at full volume. Between triggers it is unpowered and silent. The whine lives only in the window where the ringtone masks it. (Both the wire and the inverter listings disclose a "slight buzzing/humming sound" — expected and accounted for.)

## 2. Architecture

```
USB 5 V ──► Prop-Maker Feather ──► NeoPixel terminal 5V/GND ──┬──► LED strip (30 px) ──► backlit T
                 │                                             │
                 │  GPIO20 (servo header "Sig", unused)        │
                 └────────────► AOD4184 MOSFET module ◄────────┘
                                        │  switched 5 V
                                        ▼
                               EL inverter (5 V USB)
                                        │  ~100 V AC
                                        ▼
                          purple EL wire seated in the groove
```

GPIO20 is the only free GPIO on the board and needs no change to anything already wired.

## 3. Bill of materials (prices + stock verified 2026-10-15)

| # | Item | ASIN | Price | Stock / delivery |
|---|---|---|---|---|
| 1 | MaxLax EL Wire **Purple**, 9.8 ft / 3 m, 2.3 mm | `B08FCCJR6X` | **$9.99** | In stock · **tomorrow Oct 16** |
| 2 | ABALDI **DC 5 V USB** EL wire inverter | `B085H8TXF2` | **$7.31** | In stock · **Sat Oct 17** |
| 3 | Dual **AOD4184** MOSFET trigger module, 6-pack | `B0FMJH3DML` | **$5.29** | In stock · **tomorrow Oct 16** · 4.7★ |

**Total $22.59.** Everything lands by Sat Oct 17 — 14 days before Halloween.

Notes on the picks:
- **Item 2 is 5 V on purpose.** It runs from the supply already in the pumpkin, so there's no 12 V rail and no second wall wart. Rated "up to 16 ft"; we're driving ~10 ft, so it has headroom (shorter runs also glow slightly brighter).
- **Item 3 uses AOD4184**, a genuinely logic-level MOSFET, and the listing explicitly states a **3.3–20 V** trigger — important, because the Feather's GPIO is 3.3 V. **Do not substitute an IRF520 module**; that part needs ~10 V on the gate and will not switch properly here.
- The battery pack included with item 1 is **not used** — keep it as a spare way to test the wire before wiring anything.

## 4. Known risk: connector compatibility

The MaxLax wire terminates in a quick connector sized for its own battery pack. The ABALDI inverter ships "with a female quick connector." EL quick connectors are near-standard, so they will probably mate — but it is unverified.

**If they don't mate, no soldering is required.** Cut the connector off the MaxLax *battery pack* leaving ~5 cm of pigtail, cut the inverter's output connector off the same way, and join red–red / black–black using two of the spare Dupont jumpers plus tape or a spare screw terminal from the MOSFET 6-pack. The joint lives inside the pumpkin and carries almost no current.

**Test this first, before any cutting:** plug the wire into the inverter, plug the inverter into a USB brick, confirm it lights.

## 5. Wiring

| From | To | Notes |
|---|---|---|
| Feather **GPIO20** (servo header `Sig`) | MOSFET module `SIG` (J1 header) | 4-hole header, not populated — push a male Dupont pin in and anchor with hot glue, or solder. Signal only, microamps. |
| Feather **GND** (servo header `G`) | MOSFET module `GND` (J1) | Common ground — required. |
| NeoPixel terminal **5V** | MOSFET module input **V+** | Piggyback with the strip's 5 V wire. Screw terminal. |
| NeoPixel terminal **GND** | MOSFET module input **V−** | Screw terminal. |
| MOSFET module output **V+ / V−** | EL inverter's USB lead, **cut and stripped** (red = +5 V, black = GND) | One cable cut, no soldering. Screw terminals. |
| EL inverter output | EL wire | Quick connector — see §4. |

The PIR keeps the servo header's `V+` and `G`; only `Sig` is newly used.

## 6. Firmware delta — ✅ APPLIED 2026-10-15

Implemented in `firmware/code.py` and covered by 7 new assertions in `firmware/sim/sim_state_machine.py` (24/24 checks pass). `EL_ENABLED = True` by default; set it `False` for the LEDs-only fallback. The firmware refuses to boot (red blink) if `EL_PIN` and `SENSOR_PIN` collide.

What was added:
```python
EL_PIN = board.EXTERNAL_SERVO          # GPIO20
el = digitalio.DigitalInOut(EL_PIN)
el.direction = digitalio.Direction.OUTPUT
el.value = False
```
In `enter_notify()`: `el.value = True`
Where `run_notify()` returns True (fade complete): `el.value = False`

**On/off only — do not PWM it.** EL inverters flicker badly when their DC input is chopped; the usable dimming range is narrow and non-linear. The EL snapping on with the ring is the effect we want anyway.

Simulator coverage added: one on/off pair per notification, strictly alternating; energised on the same tick as the trigger; de-energised only after the LED fade completes; dark through warm-up, idle and every cooldown gap; and the pin never touched at all when `EL_ENABLED = False`.

## 7. Power budget — tighter than before

| Load | Peak |
|---|---|
| Board + regulator | 0.05 A |
| Amplifier at 3 W | 0.80 A |
| 30 px white @ 70 % | 1.26 A |
| **EL inverter** | **~0.40 A** |
| **Total** | **≈ 2.5 A** against the 5 V / 3 A supply |

~0.5 A of margin. **Brownout symptom: the board resets mid-notification.** If that happens, drop `NOTIFY_BRIGHTNESS` to 0.5 (→ ~2.2 A) or cut the strip to 20 pixels. With EL carrying the outline, fewer pixels are needed anyway — the strip now only has to light the T.

## 8. Physical build

1. **Groove:** widen the existing outline groove to ~3 mm wide × 3 mm deep so the 2.3 mm wire seats below the surface. Hot-knife wand or a V-tip, slowly. Respirator on, outdoors.
2. **Cut the T glyph all the way through** (the only through-cut now) and tape the white diffuser paper behind it inside.
3. **Route as one continuous run** so the wire never needs re-terminating: start at the inverter inside the pumpkin, exit through a small hole at the start of shape 1, trace it, dive back in, emerge at shape 2, and so on. Four shapes → four entry/exit hole pairs, ~3 mm each. Jumps are hidden inside; EL glowing inside the pumpkin doesn't matter.
4. **Tack** the wire every ~30 mm with hot glue.
5. **Cut once at the very end** and seal that end with hot glue. Discard the offcut (a cut end can't be re-powered without re-terminating).
6. **Insulate properly and don't handle it live** — inverter output is ~100 V AC at very low current. Enough for a mild tingle, not a hazard, but seal the cut end.
7. **Damp the whine further** (optional): pot the inverter in hot glue — it quiets the transformer's mechanical buzz — and site it away from the speaker port.

## 9. What's still true

- **Dim.** The maker says "use in dark environments." At 3–4 m on a dark porch it reads well; in bright ambient light it's subtle. The through-cut white T is the bright element carrying the logo.
- **Purple only.** One color per strand; the T's white comes from the NeoPixels.
- **Not water resistant.** Covered porch; consider a bead of clear silicone over the groove.
- **Phosphor decay** is irrelevant over one month.

## 10. Fallback

If the EL disappoints on the bench, nothing is lost: finish cutting the window out along the same groove line and revert to the original backlit-insert plan. The print template and firmware for it are unchanged and still valid.
