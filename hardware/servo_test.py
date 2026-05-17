#!/usr/bin/env python3
"""
Servo bring-up test for KS0223F Smart Car.

Verified BCM pins (vendor source + empirical bring-up):
  BCM 5  → ULTRASONIC_SERVO  (sweeps the HC-SR04 sensor)
  BCM 6  → CAMERA_SERVO      (camera tilt)
  BCM 7  → STEERING_SERVO    (front-wheel steering)

Standard servo PWM: 50 Hz, pulse width 0.5 ms (0°) to 2.5 ms (180°)
Duty cycle at 50 Hz period (20 ms):
  0°   → 0.5/20 * 100 =  2.5%
  90°  → 1.5/20 * 100 =  7.5%
  180° → 2.5/20 * 100 = 12.5%
"""

import RPi.GPIO as GPIO
import time

SERVO_PINS = {
    "ultrasonic": 5,
    "camera":     6,
    "steering":   7,
}

PWM_FREQ = 50  # Hz


def angle_to_duty(angle: float) -> float:
    """Convert angle (0–180°) to PWM duty cycle (2.5–12.5%)."""
    return 2.5 + (angle / 180.0) * 10.0


def sweep(pwm, name: str, steps: int = 5) -> None:
    """Sweep servo from 0° to 180° and back."""
    print(f"  [{name}] 0° → 180°")
    for angle in range(0, 181, 180 // steps):
        pwm.ChangeDutyCycle(angle_to_duty(angle))
        time.sleep(0.4)

    print(f"  [{name}] 180° → 0°")
    for angle in range(180, -1, -(180 // steps)):
        pwm.ChangeDutyCycle(angle_to_duty(angle))
        time.sleep(0.4)

    # Return to centre
    pwm.ChangeDutyCycle(angle_to_duty(90))
    time.sleep(0.3)


def main() -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    pwms = {}
    for name, pin in SERVO_PINS.items():
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, PWM_FREQ)
        pwm.start(angle_to_duty(90))  # start at centre
        pwms[name] = pwm

    time.sleep(0.5)  # let servos settle

    try:
        for name, pwm in pwms.items():
            print(f"\nTesting {name} (BCM {SERVO_PINS[name]})")
            sweep(pwm, name)
            print(f"  [{name}] PASS")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        for pwm in pwms.values():
            pwm.stop()
        GPIO.cleanup()
        print("GPIO cleaned up.")


if __name__ == "__main__":
    main()
