"""
Camera mount abstraction.

The KS0223F camera is on a single tilt servo (pin CAMERA_SERVO, BCM 6).
There is no camera pan servo on this kit — horizontal sweep is provided
by the ultrasonic head (see robot.ultrasonic.UltrasonicHead) or by
turning the whole car.
"""

from robot import pins
from robot.servo import Servo


class CameraMount:
    def __init__(self, pin: int | None = None, initial_angle: float = 90.0) -> None:
        self._servo = Servo(
            pin if pin is not None else pins.CAMERA_SERVO,
            initial_angle,
        )

    @property
    def tilt(self) -> float:
        return self._servo.angle

    def set_tilt(self, angle: float) -> None:
        self._servo.set_angle(angle)

    def nudge(self, delta: float) -> None:
        self.set_tilt(self.tilt + delta)

    def centre(self) -> None:
        self._servo.centre()

    def cleanup(self) -> None:
        self._servo.cleanup()

    def __enter__(self) -> "CameraMount":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.cleanup()
