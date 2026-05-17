"""
HC-SR04 ultrasonic distance sensor + the servo "head" it sits on.

  Ultrasonic     – the distance sensor itself (TRIG/ECHO pins)
  UltrasonicHead – the servo that swivels the sensor left/right
                   (ULTRASONIC_SERVO, BCM 5)

Requires robot.pins.ULTRASONIC_TRIG and ULTRASONIC_ECHO to be filled in
before using Ultrasonic. UltrasonicHead has no pin TODOs.
"""

import RPi.GPIO as GPIO
import time
from robot import pins
from robot.servo import Servo

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

    def distance_cm_median(self, samples: int = 5) -> float | None:
        """Median of N pings; returns None if every ping timed out."""
        if samples < 1:
            raise ValueError("samples must be >= 1")
        readings = [d for d in (self.distance_cm() for _ in range(samples))
                    if d is not None]
        if not readings:
            return None
        readings.sort()
        return readings[len(readings) // 2]

    def cleanup(self) -> None:
        GPIO.cleanup([self._trig, self._echo])

    def __enter__(self) -> "Ultrasonic":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.cleanup()


class UltrasonicHead:
    """The pan servo that swivels the HC-SR04 left/right."""

    def __init__(self, pin: int | None = None, initial_angle: float = 90.0) -> None:
        self._servo = Servo(
            pin if pin is not None else pins.ULTRASONIC_SERVO,
            initial_angle,
        )

    @property
    def pan(self) -> float:
        return self._servo.angle

    def set_pan(self, angle: float) -> None:
        self._servo.set_angle(angle)

    def nudge(self, delta: float) -> None:
        self.set_pan(self.pan + delta)

    def centre(self) -> None:
        self._servo.centre()

    def cleanup(self) -> None:
        self._servo.cleanup()

    def __enter__(self) -> "UltrasonicHead":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.cleanup()
