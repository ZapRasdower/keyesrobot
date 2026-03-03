"""
HC-SR04 ultrasonic distance sensor abstraction.

Requires robot.pins.ULTRASONIC_TRIG and ULTRASONIC_ECHO to be filled in.
"""

import RPi.GPIO as GPIO
import time
from robot import pins

TRIG_PULSE_S  = 10e-6    # 10 µs
SPEED_SOUND   = 343.0    # m/s at ~20 °C
TIMEOUT_S     = 0.05     # 50 ms → ~8.5 m max range


class Ultrasonic:
    def __init__(self) -> None:
        if pins.ULTRASONIC_TRIG is None or pins.ULTRASONIC_ECHO is None:
            raise RuntimeError(
                "ULTRASONIC_TRIG / ULTRASONIC_ECHO pins not set in robot/pins.py"
            )
        self._trig = pins.ULTRASONIC_TRIG
        self._echo = pins.ULTRASONIC_ECHO
        GPIO.setup(self._trig, GPIO.OUT)
        GPIO.setup(self._echo, GPIO.IN)
        GPIO.output(self._trig, GPIO.LOW)
        time.sleep(0.5)  # sensor stabilise

    def distance_cm(self) -> float | None:
        """Return distance in cm, or None on timeout."""
        GPIO.output(self._trig, GPIO.LOW)
        time.sleep(2e-6)
        GPIO.output(self._trig, GPIO.HIGH)
        time.sleep(TRIG_PULSE_S)
        GPIO.output(self._trig, GPIO.LOW)

        t = time.monotonic()
        while GPIO.input(self._echo) == GPIO.LOW:
            if time.monotonic() - t > TIMEOUT_S:
                return None
        start = time.monotonic()

        while GPIO.input(self._echo) == GPIO.HIGH:
            if time.monotonic() - start > TIMEOUT_S:
                return None
        end = time.monotonic()

        return ((end - start) * SPEED_SOUND / 2.0) * 100.0

    def cleanup(self) -> None:
        GPIO.cleanup([self._trig, self._echo])
