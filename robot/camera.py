"""
Camera pan/tilt mount abstraction.

Defaults: SERVO1 = pan (horizontal), SERVO2 = tilt (vertical).
If your physical mounting is reversed, either swap pin assignments in
robot/pins.py or pass explicit pins to CameraMount(pan_pin=..., tilt_pin=...).
"""

from robot import pins
from robot.servo import Servo


class CameraMount:
    def __init__(
        self,
        pan_pin: int | None = None,
        tilt_pin: int | None = None,
        pan_angle: float = 90.0,
        tilt_angle: float = 90.0,
    ) -> None:
        self.pan = Servo(pan_pin if pan_pin is not None else pins.SERVO1, pan_angle)
        self.tilt = Servo(tilt_pin if tilt_pin is not None else pins.SERVO2, tilt_angle)

    def set_pan(self, angle: float) -> None:
        self.pan.set_angle(angle)

    def set_tilt(self, angle: float) -> None:
        self.tilt.set_angle(angle)

    def aim(self, pan: float | None = None, tilt: float | None = None) -> None:
        if pan is not None:
            self.set_pan(pan)
        if tilt is not None:
            self.set_tilt(tilt)

    def centre(self) -> None:
        self.pan.centre()
        self.tilt.centre()

    @property
    def angles(self) -> tuple[float, float]:
        return self.pan.angle, self.tilt.angle

    def cleanup(self) -> None:
        self.pan.cleanup()
        self.tilt.cleanup()

    def __enter__(self) -> "CameraMount":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.cleanup()
