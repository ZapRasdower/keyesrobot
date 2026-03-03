#!/usr/bin/env python3
"""
Ultrasonic (HC-SR04) bring-up test for KS0223F Smart Car.

TODO – open bp3_ultrasonic.py and fill in these pins before running:
  TRIG_PIN = ???   # BCM pin that sends the 10 µs trigger pulse
  ECHO_PIN = ???   # BCM pin that receives the echo pulse

How to find them:
  grep -E 'TRIG|ECHO|trig|echo' \
    ~/RaspberryPiCar/RaspberryPi-Car/basic_project/bp3_ultrasonic.py

HC-SR04 operating notes:
  - Supply: 5 V (the Pi's 5 V pin)
  - TRIG:   10 µs HIGH pulse → starts measurement
  - ECHO:   HIGH duration × (speed of sound / 2) = distance
  - Speed of sound ≈ 343 m/s at 20 °C
  - Max reliable range: ~4 m; min: ~2 cm
  - Pi GPIO is 3.3 V logic. ECHO is 5 V output from sensor – use a
    voltage divider (1 kΩ + 2 kΩ) or level shifter to protect the Pi.
"""

import RPi.GPIO as GPIO
import time

# --- TODO: replace with actual BCM pin numbers from bp3_ultrasonic.py ---
TRIG_PIN = None   # e.g. 8
ECHO_PIN = None   # e.g. 9

TRIG_PULSE_S = 10e-6    # 10 µs trigger pulse
SPEED_OF_SOUND = 343.0  # m/s at ~20 °C
TIMEOUT_S = 0.05        # 50 ms → ~8.5 m max; anything beyond = no return echo


def measure_distance_cm() -> float | None:
    """
    Send one ultrasonic ping and return distance in centimetres.
    Returns None on timeout (no echo received).
    """
    # Send trigger pulse
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(2e-6)
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(TRIG_PULSE_S)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Wait for echo to go HIGH
    start = time.monotonic()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        if time.monotonic() - start > TIMEOUT_S:
            return None
    echo_start = time.monotonic()

    # Wait for echo to go LOW
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        if time.monotonic() - echo_start > TIMEOUT_S:
            return None
    echo_end = time.monotonic()

    duration_s = echo_end - echo_start
    distance_m = (duration_s * SPEED_OF_SOUND) / 2.0
    return distance_m * 100.0  # → cm


def main() -> None:
    if TRIG_PIN is None or ECHO_PIN is None:
        raise RuntimeError(
            "TRIG_PIN and ECHO_PIN are not set.\n"
            "Open this file and fill in the BCM pin numbers before running."
        )

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    print(f"Ultrasonic test  TRIG=BCM{TRIG_PIN}  ECHO=BCM{ECHO_PIN}")
    print("Press Ctrl+C to stop.\n")

    time.sleep(0.5)  # sensor settle time

    try:
        while True:
            dist = measure_distance_cm()
            if dist is None:
                print("  No echo (timeout) – object out of range or wiring issue.")
            elif dist < 2.0:
                print(f"  {dist:6.1f} cm  (too close – reading unreliable)")
            else:
                print(f"  {dist:6.1f} cm")
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up.")


if __name__ == "__main__":
    main()
