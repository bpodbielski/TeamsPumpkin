# code.py -- "Someone's calling" Halloween pumpkin prop
# Adafruit RP2040 Prop-Maker Feather, CircuitPython 9.x/10.x
# Motion -> plays a Teams call sound, lights a backlit Teams logo. Once per
# approach, forever, unattended. Authoritative spec: ../05_Firmware_Spec.md
# (comments below cite its section numbers). API patterns borrowed from
# Adafruit's MIT-licensed ../reference/adafruit_propmaker_jack_o_lantern_code.py.

import supervisor
supervisor.runtime.autoreload = False   # never hot-reload a running prop (spec S7.1)

import board
import digitalio
import audiobusio
import audiocore
import audiomixer
import microcontroller
import time
import math
import random
import gc
import neopixel
from adafruit_ticks import ticks_ms, ticks_add, ticks_diff

# ============================== Configuration ===============================
# Decided values from spec S5. Names/defaults are unchanged from that table.

NUM_PIXELS              = 2                      # EL design: 2 px in a light box behind the through-cut T (doc 09/10)
SENSOR_PIN               = board.EXTERNAL_BUTTON  # GPIO19; plan B if it misbehaves: board.EXTERNAL_SERVO (GPIO20, servo header Sig)
SENSOR_ACTIVE_HIGH       = True
WARMUP_S                 = 60      # ignore sensor after boot (PIR calibration)
COOLDOWN_S               = 10      # minimum seconds between notifications
REPEAT_IF_OCCUPIED       = True    # re-ping every COOLDOWN_S while the sensor stays HIGH (someone lingering)
IDLE_MODE                = "off"   # "off" (decided) or "breathe"
IDLE_COLOR               = (90, 60, 255)   # Teams-ish purple (R, G, B) for breathe mode
IDLE_BRIGHTNESS          = 0.08    # peak of the breathe cycle (0-1)
IDLE_BREATHE_PERIOD_S    = 4.0
NOTIFY_COLOR             = (255, 255, 255) # white: shows the print in true colors
NOTIFY_BRIGHTNESS        = 0.15    # START value -- calibrate in the dark so the T beats the EL but doesn't swamp it
NOTIFY_ATTACK_S          = 0.05    # snap on
NOTIFY_HOLD_S            = None    # None = hold until the sound finishes; else seconds
NOTIFY_FADE_S            = 1.5     # fade back to idle
EL_ENABLED               = True    # purple EL wire outline (see ../09_EL_Wire_Design.md)
EL_PIN                   = board.EXTERNAL_SERVO  # GPIO20, servo header "Sig" -> AOD4184 MOSFET gate
SOUNDS = [                         # (filename, weight); weights need not sum to 1
    ("sounds/teams_call_1ring.wav", 1.0),   # one ring, from Ben's clip
]
VOLUME                   = 1.0     # mixer voice level 0-1
SELFTEST_ON_BOOT         = False   # True on the bench: fire one notification 3 s after warm-up
DEBUG_PRINT              = True    # serial prints; harmless on the porch
LOOP_PERIOD_MS           = 20
# ---- Implementation constants (not in spec S5's tunables table) -----------
STATUS_BRIGHTNESS        = 0.2     # onboard status NeoPixel (spec S4)
DEBOUNCE_SAMPLES         = 3       # 3 * LOOP_PERIOD_MS = 60 ms debounce (spec S6)
SELFTEST_DELAY_S         = 3       # spec S5's SELFTEST_ON_BOOT comment
STARTUP_ERROR_BLINK_S    = 5       # spec S7.1 / S8
WARMUP_BLINK_PERIOD_MS   = 1000    # "slow blink" (spec S6 WARMUP), not numerically specced
ERROR_BLINK_PERIOD_MS    = 300     # faster/urgent blink for the red error state, not numerically specced

STATUS_OFF               = (0, 0, 0)
STATUS_AMBER             = (255, 140, 0)
STATUS_IDLE_COLOR        = (0, 60, 0)      # dim green
STATUS_NOTIFY_COLOR      = NOTIFY_COLOR    # white
STATUS_COOLDOWN_COLOR    = (0, 0, 60)      # dim blue
STATUS_RED               = (255, 0, 0)

STATE_WARMUP   = "WARMUP"
STATE_IDLE     = "IDLE"
STATE_NOTIFY   = "NOTIFY"
STATE_COOLDOWN = "COOLDOWN"

# ================================ Hardware ==================================
# Pin table per spec S4. EXTERNAL_POWER is set once here and never touched
# again (spec S7.2) -- it feeds the strip's 5 V, the sensor, and the amp.

external_power = digitalio.DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = digitalio.Direction.OUTPUT
external_power.value = True

status_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=STATUS_BRIGHTNESS,
                                  auto_write=False)
strip = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, NUM_PIXELS, brightness=1.0,
                           auto_write=False, pixel_order=neopixel.GRB)

sensor = digitalio.DigitalInOut(SENSOR_PIN)
sensor.direction = digitalio.Direction.INPUT
sensor.pull = None      # sensor output is push-pull 3.3 V; no internal pull needed

# EL wire outline: this pin drives the gate of an AOD4184 MOSFET module that
# switches the 5 V EL inverter. On/off ONLY -- never PWM an EL inverter's DC
# input, it flickers across most of the duty range. The pin is claimed inside
# the BOOT try/except below so a pin conflict shows up as the red startup-error
# blink rather than a silent halt.
el = None

# ================================= Helpers ===================================

def gamma(t):
    """x*x easing curve so brightness ramps look linear to the eye (spec S7.4)."""
    return t * t

def clamp01(value):
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value

def lerp(a, b, t):
    return a + (b - a) * t

def scale_color(rgb, level):
    level = clamp01(level)
    return (int(rgb[0] * level), int(rgb[1] * level), int(rgb[2] * level))

def lerp_color(rgb_a, rgb_b, t):
    return (int(lerp(rgb_a[0], rgb_b[0], t)),
            int(lerp(rgb_a[1], rgb_b[1], t)),
            int(lerp(rgb_a[2], rgb_b[2], t)))

def stage_progress(elapsed_ms, duration_s):
    """0..1 linear progress through a duration_s-long stage; instant if <= 0."""
    duration_ms = duration_s * 1000
    if duration_ms <= 0:
        return 1.0
    return clamp01(elapsed_ms / duration_ms)

def weighted_choice(items):
    """Pick a (value, weight) item at random; weights need not sum to 1."""
    total = 0.0
    for _, weight in items:
        total += weight
    pick = random.random() * total
    upto = 0.0
    for value, weight in items:
        upto += weight
        if pick <= upto:
            return value
    return items[-1][0]

def set_status(color):
    status_pixel[0] = color
    status_pixel.show()

def blink_phase(now, period_ms):
    """True for the first half of each period_ms window since boot."""
    half = period_ms // 2
    return (ticks_diff(now, boot_ms) // half) % 2 == 0

def idle_color_now(now):
    """The strip color IDLE/COOLDOWN should show right now, per IDLE_MODE."""
    if IDLE_MODE != "breathe":
        return (0, 0, 0)
    elapsed_s = ticks_diff(now, boot_ms) / 1000.0
    linear = (math.sin(2 * math.pi * elapsed_s / IDLE_BREATHE_PERIOD_S) + 1.0) / 2.0
    return scale_color(IDLE_COLOR, gamma(linear) * IDLE_BRIGHTNESS)

def set_strip_level(color):
    """Fill the whole strip with one RGB color. Caller does strip.show()."""
    for i in range(NUM_PIXELS):
        strip[i] = color

_sensor_history = [False] * DEBOUNCE_SAMPLES
_debounced_level = False

def read_sensor_debounced():
    """3-consecutive-sample debounce (spec S6): flips only after 3 matching reads."""
    global _debounced_level
    raw = sensor.value if SENSOR_ACTIVE_HIGH else not sensor.value
    _sensor_history.append(raw)
    del _sensor_history[0]
    if all(_sensor_history):
        _debounced_level = True
    elif not any(_sensor_history):
        _debounced_level = False
    return _debounced_level

def load_sounds():
    """Open every WAV in SOUNDS once; the same WaveFile is replayed on each trigger (spec S7.5)."""
    choices = []
    for path, weight in SOUNDS:
        wave = audiocore.WaveFile(open(path, "rb"))
        choices.append((wave, weight))
    return choices

def startup_error_blink(error):
    """Red blink for STARTUP_ERROR_BLINK_S, then reset (spec S7.1, S8)."""
    print("STARTUP ERROR:", error)
    deadline = ticks_add(ticks_ms(), STARTUP_ERROR_BLINK_S * 1000)
    while ticks_diff(ticks_ms(), deadline) < 0:
        now = ticks_ms()
        set_status(STATUS_RED if blink_phase(now, ERROR_BLINK_PERIOD_MS) else STATUS_OFF)
        time.sleep(0.05)
    microcontroller.reset()

def enter_notify(now):
    """Start a notification: pick a sound, play it, begin the attack ramp."""
    global trigger_ms, notify_stage, notify_stage_start_ms
    trigger_ms = now
    wave = weighted_choice(sound_choices)
    mixer.voice[0].level = VOLUME
    mixer.voice[0].play(wave, loop=False)
    notify_stage = "attack"
    notify_stage_start_ms = now
    if el is not None:
        el.value = True          # snaps on with the ring; stays lit through the fade
    if DEBUG_PRINT:
        print("TRIGGER")
        print("gc.mem_free():", gc.mem_free())

def run_notify(now):
    """Advance the attack/hold/fade animation one tick. Returns True once finished."""
    global notify_stage, notify_stage_start_ms, notify_fade_start_color
    elapsed = ticks_diff(now, notify_stage_start_ms)

    if notify_stage == "attack":
        t = stage_progress(elapsed, NOTIFY_ATTACK_S)
        set_strip_level(scale_color(NOTIFY_COLOR, NOTIFY_BRIGHTNESS * gamma(t)))
        if t >= 1.0:
            notify_stage = "hold"
            notify_stage_start_ms = now
        return False

    if notify_stage == "hold":
        color = scale_color(NOTIFY_COLOR, NOTIFY_BRIGHTNESS)
        set_strip_level(color)
        if NOTIFY_HOLD_S is None:
            done = not mixer.voice[0].playing
        else:
            done = elapsed >= NOTIFY_HOLD_S * 1000
        if done:
            notify_stage = "fade"
            notify_stage_start_ms = now
            notify_fade_start_color = color
        return False

    # notify_stage == "fade"
    t = stage_progress(elapsed, NOTIFY_FADE_S)
    # Fade-out: brightness must follow (1-t)^2 so the *decrease* looks linear to
    # the eye; gamma(t) on the lerp would hang bright and then drop abruptly.
    set_strip_level(lerp_color(notify_fade_start_color, idle_color_now(now), 1.0 - gamma(1.0 - t)))
    return t >= 1.0

# ================================== BOOT ======================================
# spec S6 BOOT: autoreload off (top of file) -> external power HIGH (above) ->
# open WAVs -> create mixer -> audio.play(mixer) -> strip off -> status amber.

boot_ms = ticks_ms()

try:
    if EL_ENABLED:
        if EL_PIN is SENSOR_PIN:
            raise ValueError("EL_PIN and SENSOR_PIN are the same pin -- move one")
        el = digitalio.DigitalInOut(EL_PIN)
        el.direction = digitalio.Direction.OUTPUT
        el.value = False
    sound_choices = load_sounds()
    audio = audiobusio.I2SOut(board.I2S_BIT_CLOCK, board.I2S_WORD_SELECT, board.I2S_DATA)
    mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1,
                              bits_per_sample=16, samples_signed=True)
    audio.play(mixer)
except Exception as e:                     # pylint: disable=broad-except
    startup_error_blink(e)                 # never returns; ends in microcontroller.reset()

set_strip_level((0, 0, 0))
strip.show()
set_status(STATUS_AMBER)

warmup_deadline_ms = ticks_add(boot_ms, WARMUP_S * 1000)
selftest_fire_ms = ticks_add(warmup_deadline_ms, SELFTEST_DELAY_S * 1000)
selftest_pending = SELFTEST_ON_BOOT

state = STATE_WARMUP
prev_debounced = False
trigger_ms = 0
cooldown_deadline_ms = 0
notify_stage = ""
notify_stage_start_ms = 0
notify_fade_start_color = (0, 0, 0)

if DEBUG_PRINT:
    print("STATE -> WARMUP")

loop_period_s = LOOP_PERIOD_MS / 1000.0

# =============================== Main loop (spec S6) ============================
# Single non-blocking loop: sleeps LOOP_PERIOD_MS per iteration and computes every
# animation from elapsed ticks, so audio/lights stay in sync and the sensor is
# always being read. Wrapped per spec S7.1 so any runtime fault resets cleanly.

while True:
    try:
        now = ticks_ms()
        level = read_sensor_debounced()
        rising_edge = level and not prev_debounced

        if state == STATE_WARMUP:
            # Sensor is sampled above but never acted on in this state (spec S7.6).
            set_status(STATUS_AMBER if blink_phase(now, WARMUP_BLINK_PERIOD_MS) else STATUS_OFF)
            set_strip_level((0, 0, 0))     # strip off regardless of IDLE_MODE
            if ticks_diff(now, warmup_deadline_ms) >= 0:
                state = STATE_IDLE
                if DEBUG_PRINT:
                    print("STATE -> IDLE")

        elif state == STATE_IDLE:
            set_status(STATUS_IDLE_COLOR)
            set_strip_level(idle_color_now(now))
            fire = rising_edge
            if selftest_pending and ticks_diff(now, selftest_fire_ms) >= 0:
                fire = True
                selftest_pending = False
                if DEBUG_PRINT:
                    print("SELFTEST fire")
            if fire:
                enter_notify(now)
                state = STATE_NOTIFY
                if DEBUG_PRINT:
                    print("STATE -> NOTIFY")

        elif state == STATE_NOTIFY:
            set_status(STATUS_NOTIFY_COLOR)
            if run_notify(now):
                if el is not None:
                    el.value = False     # EL can't dim, so it cuts at the end of the LED fade
                cooldown_deadline_ms = ticks_add(trigger_ms, COOLDOWN_S * 1000)
                state = STATE_COOLDOWN
                if DEBUG_PRINT:
                    print("STATE -> COOLDOWN")

        elif state == STATE_COOLDOWN:
            # Sensor edges ignored here; only the debounced level is checked,
            # and only once the cooldown has fully elapsed (spec S6 COOLDOWN).
            set_status(STATUS_COOLDOWN_COLOR)
            set_strip_level(idle_color_now(now))
            if ticks_diff(now, cooldown_deadline_ms) >= 0:
                if REPEAT_IF_OCCUPIED and level:
                    enter_notify(now)
                    state = STATE_NOTIFY
                    if DEBUG_PRINT:
                        print("STATE -> NOTIFY (repeat)")
                else:
                    state = STATE_IDLE
                    if DEBUG_PRINT:
                        print("STATE -> IDLE")

        prev_debounced = level
        strip.show()
        time.sleep(loop_period_s)

    except Exception as e:                 # pylint: disable=broad-except
        print("RUNTIME ERROR:", e)
        time.sleep(2)
        microcontroller.reset()
