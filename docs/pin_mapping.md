# KS0223F Pin Mapping (BCM numbering)

All pin numbers are **BCM GPIO** numbers (not physical/board numbers).

## Status

| Symbol | Meaning |
|--------|---------|
| ✅ | Confirmed from vendor source |
| ❓ | Not yet extracted – see "How to fill in" below |

---

## Servos

| Name | BCM | Notes | Status |
|------|-----|-------|--------|
| ULTRASONIC_SERVO | 5 | Sweeps the HC-SR04 sensor left/right | ✅ |
| CAMERA_SERVO     | 6 | Camera tilt up/down                  | ✅ |
| STEERING_SERVO   | 7 | Front-wheel steering                 | ✅ |

Source: `MainControl.py` + empirical bring-up (2026-05).
The camera has only tilt on this kit (no pan); the HC-SR04 has only
pan (no tilt).

---

## Motors – Direction

| Name | BCM | Function | Status |
|------|-----|----------|--------|
| L_IN1 | 20 | Left forward | ✅ |
| L_IN2 | 21 | Left reverse | ✅ |
| R_IN1 | 24 | Right forward | ✅ |
| R_IN2 | 25 | Right reverse | ✅ |

Source: `MainControl.py`, `bp12_avoid_car.py`

---

## Motors – Additional direction (4-pin control)

| Name | BCM | Function | Status |
|------|-----|----------|--------|
| L_IN3 | ❓ | Left channel B fwd | ❓ |
| L_IN4 | ❓ | Left channel B rev | ❓ |
| R_IN3 | ❓ | Right channel B fwd | ❓ |
| R_IN4 | ❓ | Right channel B rev | ❓ |

---

## Motors – PWM (speed)

| Name | BCM | Function | Status |
|------|-----|----------|--------|
| L_PWM1 | ❓ | Left PWM A | ❓ |
| L_PWM2 | ❓ | Left PWM B | ❓ |
| R_PWM1 | ❓ | Right PWM A | ❓ |
| R_PWM2 | ❓ | Right PWM B | ❓ |

---

## Ultrasonic (HC-SR04)

| Name | BCM | Function | Status |
|------|-----|----------|--------|
| ULTRASONIC_TRIG | ❓ | Trigger pulse | ❓ |
| ULTRASONIC_ECHO | ❓ | Echo receive | ❓ |

---

## Tracking Sensors

| Name | BCM | Function | Status |
|------|-----|----------|--------|
| TRACK_LEFT | ❓ | Line sensor left | ❓ |
| TRACK_MIDDLE | ❓ | Line sensor middle | ❓ |
| TRACK_RIGHT | ❓ | Line sensor right | ❓ |

Source: `bp10_tracking_car.py`

---

## How to fill in the missing pins

```bash
# PWM + extra direction pins
grep -E 'PWM|IN3|IN4' ~/RaspberryPiCar/RaspberryPi-Car/MainControl.py

# Ultrasonic
grep -E 'TRIG|ECHO|trig|echo' \
  ~/RaspberryPiCar/RaspberryPi-Car/basic_project/bp3_ultrasonic.py

# Tracking sensors
grep -E 'sensor|SENSOR|track|TRACK|IN[0-9]' \
  ~/RaspberryPiCar/RaspberryPi-Car/basic_project/bp10_tracking_car.py
```

Then update `robot/pins.py` with the values found.

---

## I2C

Only device detected on I2C bus 1: OLED at `0x3c`.
No PCA9685 present – motor/servo control is **pure GPIO**.

## Camera

Commands: `rpicam-*` (not `libcamera-*`)
Verify: `rpicam-still -o test.jpg`
