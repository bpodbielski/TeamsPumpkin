#!/bin/zsh
# Copy the pumpkin firmware onto the board's CIRCUITPY drive in the safe order:
# libraries -> sound -> code.py LAST (landing code.py is what restarts the board).
set -e
SRC="${0:A:h}"
DEST="/Volumes/CIRCUITPY"

if [[ ! -d "$DEST" ]]; then
  echo "CIRCUITPY isn't mounted. Flash CircuitPython first (step A1), then plug the board in."
  exit 1
fi
missing=0
for f in neopixel.mpy adafruit_pixelbuf.mpy adafruit_ticks.mpy; do
  if [[ ! -f "$SRC/lib/$f" ]]; then
    echo "Missing firmware/lib/$f -- copy it from the Adafruit bundle's lib/ folder (step A2)."
    missing=1
  fi
done
(( missing )) && exit 1

mkdir -p "$DEST/lib" "$DEST/sounds"
cp -X "$SRC"/lib/*.mpy "$DEST/lib/"
cp -X "$SRC/sounds/teams_call_1ring.wav" "$DEST/sounds/"
sync
cp -X "$SRC/code.py" "$DEST/code.py"
sync
echo "Installed to CIRCUITPY."
echo "Expect: status LED blinks amber for 60 s (sensor warm-up), then dim green."
echo "If it doesn't start blinking within a few seconds, press RESET once."
