"""
Servo abstraction for KS0223F Smart Car.

Three independent servos on this kit:
  - ULTRASONIC_SERVO  (pin 5): sweeps the HC-SR04 sensor left/right
  - CAMERA_SERVO     (pin 6): camera tilt up/down
  - STEERING_SERVO   (pin 7): front-wheel steering

PWM frequency: 50 Hz (standard servo)
Duty cycle:    2.5% (0°) → 12.5% (180°)
"""

import RPi.GPIO as GPIO
from robot import pins

PWM_FREQ = 50  # Hz


def _angle_to_duty(angle: float) -> float:
    return 2.5 + (max(0.0, min(180.0, angle)) / 180.0) * 10.0


class Servo:
    def __init__(self, pin: int, initial_angle: float = 90.0) -> None:
        self._pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self._pwm = GPIO.PWM(pin, PWM_FREQ)
        self._pwm.start(_angle_to_duty(initial_angle))
        self._angle = initial_angle

    @property
    def angle(self) -> float:
        return self._angle

    def set_angle(self, angle: float) -> None:
        self._angle = max(0.0, min(180.0, angle))
        self._pwm.ChangeDutyCycle(_angle_to_duty(self._angle))

    def centre(self) -> None:
        self.set_angle(90.0)

    def cleanup(self) -> None:
        self._pwm.stop()

    def __enter__(self) -> "Servo":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.cleanup()


class Servos:
    """Convenience wrapper for all three named servos on the car."""

    def __init__(self) -> None:
        self.ultrasonic = Servo(pins.ULTRASONIC_SERVO)
        self.camera     = Servo(pins.CAMERA_SERVO)
        self.steering   = Servo(pins.STEERING_SERVO)

    def centre_all(self) -> None:
        self.ultrasonic.centre()
        self.camera.centre()
        self.steering.centre()

    def cleanup(self) -> None:
        self.ultrasonic.cleanup()
        self.camera.cleanup()
        self.steering.cleanup()

    def __enter__(self) -> "Servos":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.cleanup()
