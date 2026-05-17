"""
Obstacle-avoidance behaviour.

Drives forward; when an obstacle is closer than STOP_DISTANCE_CM, the
robot stops, reverses briefly, and turns away from the obstacle before
resuming. Designed to be interruptible via KeyboardInterrupt.

Requires the following pins in robot/pins.py:
  - Motor direction pins (already confirmed)
  - At least one motor PWM pin (TODO – see docs/pin_mapping.md)
  - ULTRASONIC_TRIG / ULTRASONIC_ECHO (TODO)
"""

import random
import time

from robot.motor import Motors
from robot.ultrasonic import Ultrasonic

STOP_DISTANCE_CM = 20.0
CRUISE_SPEED     = 55
TURN_SPEED       = 65
REVERSE_S        = 0.4
TURN_S           = 0.5
SAMPLE_PERIOD_S  = 0.08


def _turn_away(motors: Motors) -> None:
    if random.random() < 0.5:
        motors.turn_left(TURN_SPEED)
    else:
        motors.turn_right(TURN_SPEED)
    time.sleep(TURN_S)


def run(duration_s: float | None = None) -> None:
    """Run avoidance loop. If duration_s is None, runs until Ctrl+C."""
    deadline = None if duration_s is None else time.monotonic() + duration_s

    with Ultrasonic() as us, Motors() as motors:
        motors.forward(CRUISE_SPEED)
        while deadline is None or time.monotonic() < deadline:
            dist = us.distance_cm_median(samples=3)
            if dist is not None and dist < STOP_DISTANCE_CM:
                print(f"  obstacle at {dist:.1f} cm – evading")
                motors.stop()
                time.sleep(0.1)
                motors.reverse(CRUISE_SPEED)
                time.sleep(REVERSE_S)
                _turn_away(motors)
                motors.forward(CRUISE_SPEED)
            time.sleep(SAMPLE_PERIOD_S)
        motors.stop()
