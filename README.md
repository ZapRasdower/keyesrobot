# keyesrobot

Clean Python project for the Keyestudio KS0223F Smart Car (Raspberry Pi 4B).

## Hardware
- Raspberry Pi 4B
- Pi Camera (CSI)
- HC-SR04 ultrasonic sensor
- OLED display (I2C `0x3c`)
- GPIO-based motor and servo control (no PCA9685)

## Layout

```
hardware/   bring-up test scripts – run these first to verify wiring
robot/      abstraction modules (pins, motor, servo, ultrasonic)
behaviors/  autonomy modes
run/        entry points
docs/       pin mapping, handoff brief
```

## Quickstart

```bash
# 1. Verify and fill in missing pins
#    See docs/pin_mapping.md and robot/pins.py

# 2. Run hardware bring-up tests in order
python3 hardware/servo_test.py
python3 hardware/motor_test.py
python3 hardware/ultrasonic_test.py
```

## Pin Status

All GPIO assignments are BCM-numbered.
Confirmed: servos (5/6/7), motor direction (20/21/24/25).
Pending: PWM speed pins, ultrasonic, tracking sensors.
See `docs/pin_mapping.md` for the full table and grep commands.

## Behaviours

Once PWM and ultrasonic pins are filled in:

```bash
python3 -m run.avoid                # obstacle-avoidance, Ctrl+C to stop
python3 -m run.avoid --seconds 30   # auto-stop after 30 s
```

## Camera

Use `rpicam-*` commands (not `libcamera-*`) on this OS:
```bash
rpicam-still -o test.jpg
```

### Camera (tilt only) and ultrasonic head (pan only)

The kit has three servos: camera tilt, ultrasonic-sensor pan ("eyes"),
and steering. Camera + eyes each get a small CLI suite.

Camera tilt:
```bash
python3 -m run.camera_set --tilt 60       # one-shot, scriptable
python3 -m run.camera_set --centre
python3 -m run.camera_aim                 # interactive (↑/↓ or k/j)
python3 -m run.camera_sweep               # range sweep, sanity check
python3 -m run.camera_snap --tilt 70 -o shot.jpg
```

Ultrasonic head pan:
```bash
python3 -m run.eyes_set --pan 45          # look hard left
python3 -m run.eyes_set --centre
python3 -m run.eyes_aim                   # interactive (←/→ or h/l)
python3 -m run.eyes_sweep                 # range sweep
```
