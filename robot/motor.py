"""
Motor abstraction for KS0223F Smart Car.

Requires robot.pins to have PWM pins filled in before instantiation.
Direction pins (L_IN1/2, R_IN1/2) are sufficient for basic direction;
PWM pins are required for variable speed control.
"""

import RPi.GPIO as GPIO
from robot import pins

PWM_FREQ = 100  # Hz


class Motors:
    def __init__(self) -> None:
        self._dir_pins = [pins.L_IN1, pins.L_IN2, pins.R_IN1, pins.R_IN2]
        missing = [name for name, val in zip(
            ("L_IN1", "L_IN2", "R_IN1", "R_IN2"), self._dir_pins
        ) if val is None]
        if missing:
            raise RuntimeError(
                f"Motor direction pins not set in robot/pins.py: {missing}"
            )

        self._pwm_pins = [
            p for p in [pins.L_PWM1, pins.L_PWM2, pins.R_PWM1, pins.R_PWM2]
            if p is not None
        ]
        self._pwms: dict[int, GPIO.PWM] = {}

        # Direction pins
        for pin in self._dir_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        # PWM pins
        for pin in self._pwm_pins:
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, PWM_FREQ)
            pwm.start(0)
            self._pwms[pin] = pwm

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def forward(self, speed: int = 60) -> None:
        self._set_direction(
            l_in1=GPIO.HIGH, l_in2=GPIO.LOW,
            r_in1=GPIO.HIGH, r_in2=GPIO.LOW,
            speed=speed,
        )

    def reverse(self, speed: int = 60) -> None:
        self._set_direction(
            l_in1=GPIO.LOW, l_in2=GPIO.HIGH,
            r_in1=GPIO.LOW, r_in2=GPIO.HIGH,
            speed=speed,
        )

    def turn_left(self, speed: int = 60) -> None:
        self._set_direction(
            l_in1=GPIO.LOW,  l_in2=GPIO.HIGH,
            r_in1=GPIO.HIGH, r_in2=GPIO.LOW,
            speed=speed,
        )

    def turn_right(self, speed: int = 60) -> None:
        self._set_direction(
            l_in1=GPIO.HIGH, l_in2=GPIO.LOW,
            r_in1=GPIO.LOW,  r_in2=GPIO.HIGH,
            speed=speed,
        )

    def stop(self) -> None:
        GPIO.output(pins.L_IN1, GPIO.LOW)
        GPIO.output(pins.L_IN2, GPIO.LOW)
        GPIO.output(pins.R_IN1, GPIO.LOW)
        GPIO.output(pins.R_IN2, GPIO.LOW)
        for pwm in self._pwms.values():
            pwm.ChangeDutyCycle(0)

    def cleanup(self) -> None:
        self.stop()
        for pwm in self._pwms.values():
            pwm.stop()

    def __enter__(self) -> "Motors":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.cleanup()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _set_direction(
        self,
        l_in1: int, l_in2: int,
        r_in1: int, r_in2: int,
        speed: int,
    ) -> None:
        GPIO.output(pins.L_IN1, l_in1)
        GPIO.output(pins.L_IN2, l_in2)
        GPIO.output(pins.R_IN1, r_in1)
        GPIO.output(pins.R_IN2, r_in2)
        for pwm in self._pwms.values():
            pwm.ChangeDutyCycle(max(0, min(100, speed)))
