"""
Centralised GPIO setup / teardown for the robot.

Use as a context manager so BCM mode is set once and cleanup always runs:

    from robot.setup import gpio_session
    from robot.motor import Motors

    with gpio_session(), Motors() as motors:
        motors.forward(60)
"""

from contextlib import contextmanager

import RPi.GPIO as GPIO


def setup_gpio() -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


def cleanup_gpio() -> None:
    GPIO.cleanup()


@contextmanager
def gpio_session():
    setup_gpio()
    try:
        yield
    finally:
        cleanup_gpio()
