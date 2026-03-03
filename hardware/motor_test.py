#!/usr/bin/env python3
"""
Motor bring-up test for KS0223F Smart Car.

Confirmed BCM direction pins (from MainControl.py / bp12_avoid_car.py):
  L_IN1 = 20   (left  forward)
  L_IN2 = 21   (left  reverse)
  R_IN1 = 24   (right forward)
  R_IN2 = 25   (right reverse)

TODO – open MainControl.py and fill in these pins before running:
  L_PWM1 = ???   # left  motor PWM (speed) channel A  -- BCM pin TBD
  L_PWM2 = ???   # left  motor PWM (speed) channel B  -- BCM pin TBD
  R_PWM1 = ???   # right motor PWM (speed) channel A  -- BCM pin TBD
  R_PWM2 = ???   # right motor PWM (speed) channel B  -- BCM pin TBD

  (Also capture L_IN3/L_IN4/R_IN3/R_IN4 if the vendor code uses 4-pin control)

How to find them:
  grep -E 'PWM|IN3|IN4' ~/RaspberryPiCar/RaspberryPi-Car/MainControl.py

Running without PWM pins set:
  The test will still exercise direction logic, but motors won't move until
  PWM pins are configured and PWM signals are started.
"""

import RPi.GPIO as GPIO
import time

# --- Direction pins (confirmed) ---
L_IN1 = 20
L_IN2 = 21
R_IN1 = 24
R_IN2 = 25

# --- PWM pins (TODO: fill in from MainControl.py) ---
L_PWM1 = None  # replace with BCM pin number, e.g. 26
L_PWM2 = None  # replace with BCM pin number
R_PWM1 = None  # replace with BCM pin number
R_PWM2 = None  # replace with BCM pin number

PWM_FREQ = 100   # Hz – typical for DC motor PWM
DEFAULT_SPEED = 60  # duty cycle % (0–100)

DIRECTION_PINS = [L_IN1, L_IN2, R_IN1, R_IN2]
PWM_PINS = [p for p in [L_PWM1, L_PWM2, R_PWM1, R_PWM2] if p is not None]


def _stop_all(pwms: dict) -> None:
    for pwm in pwms.values():
        pwm.ChangeDutyCycle(0)
    GPIO.output(L_IN1, GPIO.LOW)
    GPIO.output(L_IN2, GPIO.LOW)
    GPIO.output(R_IN1, GPIO.LOW)
    GPIO.output(R_IN2, GPIO.LOW)


def forward(pwms: dict, speed: int = DEFAULT_SPEED, duration: float = 1.0) -> None:
    print(f"  FORWARD  speed={speed}%  t={duration}s")
    GPIO.output(L_IN1, GPIO.HIGH)
    GPIO.output(L_IN2, GPIO.LOW)
    GPIO.output(R_IN1, GPIO.HIGH)
    GPIO.output(R_IN2, GPIO.LOW)
    for pwm in pwms.values():
        pwm.ChangeDutyCycle(speed)
    time.sleep(duration)
    _stop_all(pwms)
    time.sleep(0.3)


def reverse(pwms: dict, speed: int = DEFAULT_SPEED, duration: float = 1.0) -> None:
    print(f"  REVERSE  speed={speed}%  t={duration}s")
    GPIO.output(L_IN1, GPIO.LOW)
    GPIO.output(L_IN2, GPIO.HIGH)
    GPIO.output(R_IN1, GPIO.LOW)
    GPIO.output(R_IN2, GPIO.HIGH)
    for pwm in pwms.values():
        pwm.ChangeDutyCycle(speed)
    time.sleep(duration)
    _stop_all(pwms)
    time.sleep(0.3)


def turn_left(pwms: dict, speed: int = DEFAULT_SPEED, duration: float = 0.6) -> None:
    """Left motors reverse, right motors forward."""
    print(f"  LEFT     speed={speed}%  t={duration}s")
    GPIO.output(L_IN1, GPIO.LOW)
    GPIO.output(L_IN2, GPIO.HIGH)
    GPIO.output(R_IN1, GPIO.HIGH)
    GPIO.output(R_IN2, GPIO.LOW)
    for pwm in pwms.values():
        pwm.ChangeDutyCycle(speed)
    time.sleep(duration)
    _stop_all(pwms)
    time.sleep(0.3)


def turn_right(pwms: dict, speed: int = DEFAULT_SPEED, duration: float = 0.6) -> None:
    """Left motors forward, right motors reverse."""
    print(f"  RIGHT    speed={speed}%  t={duration}s")
    GPIO.output(L_IN1, GPIO.HIGH)
    GPIO.output(L_IN2, GPIO.LOW)
    GPIO.output(R_IN1, GPIO.LOW)
    GPIO.output(R_IN2, GPIO.HIGH)
    for pwm in pwms.values():
        pwm.ChangeDutyCycle(speed)
    time.sleep(duration)
    _stop_all(pwms)
    time.sleep(0.3)


def main() -> None:
    if not PWM_PINS:
        print(
            "WARNING: No PWM pins configured. Direction logic will be tested but\n"
            "         motors will not spin. Fill in L_PWM1/L_PWM2/R_PWM1/R_PWM2\n"
            "         at the top of this file before running on real hardware.\n"
        )

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in DIRECTION_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    pwms = {}
    for pin in PWM_PINS:
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, PWM_FREQ)
        pwm.start(0)
        pwms[pin] = pwm

    try:
        print("\n--- Motor direction test ---")
        forward(pwms)
        reverse(pwms)
        turn_left(pwms)
        turn_right(pwms)
        print("\nAll direction tests complete.")

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        _stop_all(pwms)
        for pwm in pwms.values():
            pwm.stop()
        GPIO.cleanup()
        print("GPIO cleaned up.")


if __name__ == "__main__":
    main()
