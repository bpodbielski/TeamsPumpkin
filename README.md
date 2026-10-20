# Teams-o-lantern

![A foam pumpkin on a porch at night with a glowing purple outline of the Microsoft Teams logo](docs/img/teams-o-lantern.webp)

A foam pumpkin that rings like an incoming Microsoft Teams call when someone walks up to your door, while a purple EL-wire outline of the Teams logo lights up on its face. It's the Teams answer to the [Slack-o-lantern](https://www.dailydot.com/news/man-designs-slack-o-lantern/), built to sit on a porch all October.

**→ [Step-by-step build guide](https://bpodbielski.github.io/TeamsPumpkin/)** with wiring diagrams and a checklist that remembers your progress.

## How it works

A motion sensor watches the walkway. When it sees someone, an Adafruit RP2040 Prop-Maker Feather plays one ring of the Teams call sound through a small speaker and switches on the EL wire through a MOSFET module. If the visitor lingers, it rings again every 10 seconds. It runs from a USB wall adapter, needs no soldering, and restarts by itself after a power cut.

```
5 V USB adapter ─► Prop-Maker Feather ─┬─► PIR motion sensor
                                       ├─► 4 Ω speaker
                                       └─► MOSFET module ─► 5 V EL inverter ─► purple EL wire
```

## Parts

About US$110–140 in 2026, including the hot knife.

| Part | Example | Notes |
|---|---|---|
| Adafruit RP2040 Prop-Maker Feather | Adafruit [5768](https://www.adafruit.com/product/5768) | Board, 3 W audio amp, screw terminals |
| 40 mm 4 Ω speaker | Adafruit [3968](https://www.adafruit.com/product/3968) | Has solder tabs, no wires; the guide shows a no-solder connection |
| HC-SR501 PIR motion sensor | any 3-pack | Set the jumper to H |
| Logic-level MOSFET trigger module (AOD4184 / "XY-MOS") | Amazon `B0FMJH3DML` | Must accept a 3.3 V trigger. Avoid IRF520 modules |
| Purple EL wire, 3 m, 2.3 mm | MaxLax `B08FCCJR6X` | The outline uses about 1.25 m |
| 5 V USB EL wire inverter | ABALDI `B085H8TXF2` | 5 V, so it shares the board's supply |
| 5 V / 3 A USB-A wall adapter + USB-A to USB-C cable | any | Use USB-A, not a USB-C PD charger |
| Dupont jumper wire kit (M-M, M-F, F-F) | ELEGOO 120 pc | |
| Foam carvable pumpkin, ~13 in | Holiday Living 13 in (Lowe's) | Needs about 7 × 8 in of fairly flat face |
| Hot knife / foam cutter | GOCHANGE 4-in-1 (`B092S6WZ35`) | Bend the wire tip into a U to cut the groove |
| Hot glue gun, small screwdriver, respirator | | Hot-knifing polyurethane foam gives off fumes: work outdoors |

## Wiring

| From | To |
|---|---|
| PIR VCC | Feather servo header V+ (middle pin) |
| PIR GND | Feather servo header G (top pin) |
| PIR OUT | Feather Btn screw (4th from the top) |
| Speaker tabs | Feather − and + screws (bottom two) |
| MOSFET module DC+ / VIN+ | Feather 5V screw (3rd) |
| MOSFET module DC− / VIN− | Feather G screw (2nd) |
| MOSFET module PWM+ / TRIG | Feather servo header Sig (bottom pin) |
| MOSFET module OUT+ / OUT− | EL inverter red / black (cut its USB cable) |
| EL wire | EL inverter output |

The Feather's terminal labels are printed on the back of the board. From the top, the screws are Neo, G, 5V, Btn, −, +.

## Repo layout

| Path | What it is |
|---|---|
| [`docs/index.html`](docs/index.html) | The build guide (served at the link above) |
| [`docs/print_template.html`](docs/print_template.html) | Full-size template for the outline groove and holes; set your pumpkin's size and print at 100% |
| [`firmware/`](firmware/) | CircuitPython `code.py`, the sound file, a one-command installer, and setup notes |
| [`firmware/sim/`](firmware/sim/) | A host-side simulator that tests the trigger, cooldown and EL timing without hardware: `python3 firmware/sim/sim_state_machine.py` |
| [`assets/`](assets/) | The Teams logo SVG and the call sound (original and trimmed) |
| [`docs/design-history/`](docs/design-history/) | The research and planning notes, including designs that were tried and dropped |
| [`reference/`](reference/) | Adafruit's MIT-licensed Prop-Maker example the firmware is based on |

## Quick start

1. Flash CircuitPython for the [Prop-Maker Feather](https://circuitpython.org/board/adafruit_feather_rp2040_prop_maker/) (hold BOOT, tap RESET, drag the UF2).
2. Copy `neopixel.mpy`, `adafruit_pixelbuf.mpy` and `adafruit_ticks.mpy` from the matching [library bundle](https://circuitpython.org/libraries) into `firmware/lib/`.
3. Run `zsh firmware/install_to_board.sh` (macOS), or copy `firmware/lib`, `firmware/sounds` and then `firmware/code.py` to the `CIRCUITPY` drive.
4. Follow the [build guide](https://bpodbielski.github.io/TeamsPumpkin/) for wiring, carving and install.

Settings such as volume and cooldown are constants at the top of `firmware/code.py`; see [`firmware/README.md`](firmware/README.md).

## Credits and license

Code and documentation: MIT, see [LICENSE](LICENSE). The Microsoft Teams name, logo and call sound belong to Microsoft and are not covered by that license; see [`assets/NOTICE.md`](assets/NOTICE.md). This is a fan project, not affiliated with or endorsed by Microsoft. The firmware builds on Adafruit's MIT-licensed Prop-Maker examples, and the carving approach on SKS Props' foam pumpkin tutorial.
