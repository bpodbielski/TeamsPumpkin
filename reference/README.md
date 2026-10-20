# Reference material

- `adafruit_propmaker_jack_o_lantern_code.py` — Adafruit's MIT-licensed CircuitPython example for the RP2040 Prop-Maker Feather
  ("PropMaker Jack O'Lantern", Liz Clark, 2024). It is the proven pattern we build on: I2S audio via `audiobusio` + `audiomixer`
  (22,050 Hz, 16-bit, mono WAVs), `board.EXTERNAL_POWER` enabled at boot, `board.EXTERNAL_BUTTON` as a digital input,
  non-blocking timing with `adafruit_ticks`, and a try/except that resets the board on any exception.
  Source: https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Spinning_Ikea_Pumpkin/code.py
- Guide: https://learn.adafruit.com/propmaker-jack-o-lantern
- Board guide (pinouts, CircuitPython install): https://learn.adafruit.com/adafruit-rp2040-prop-maker-feather
- CircuitPython UF2 for this board: https://circuitpython.org/board/adafruit_feather_rp2040_prop_maker/
