"""
BCM pin assignments for KS0223F Smart Car (Raspberry Pi 4B).

Status legend:
  CONFIRMED  – verified from vendor source (MainControl.py / bp*.py)
  TODO       – pin not yet extracted; fill in and remove this marker
"""

# ---------------------------------------------------------------------------
# Servos  (CONFIRMED – MainControl.py)
# ---------------------------------------------------------------------------
SERVO1 = 5   # camera pan / tilt 1
SERVO2 = 6   # camera pan / tilt 2
SERVO3 = 7   # steering servo

# ---------------------------------------------------------------------------
# Motor direction control  (CONFIRMED – MainControl.py, bp12_avoid_car.py)
# ---------------------------------------------------------------------------
L_IN1 = 20   # left  motor: forward
L_IN2 = 21   # left  motor: reverse
R_IN1 = 24   # right motor: forward
R_IN2 = 25   # right motor: reverse

# TODO: extract from MainControl.py
L_IN3 = None   # left  motor: channel B forward (if 4-pin control)
L_IN4 = None   # left  motor: channel B reverse
R_IN3 = None   # right motor: channel B forward
R_IN4 = None   # right motor: channel B reverse

# ---------------------------------------------------------------------------
# Motor PWM (speed)  (TODO – extract from MainControl.py)
# ---------------------------------------------------------------------------
# grep -E 'PWM' ~/RaspberryPiCar/RaspberryPi-Car/MainControl.py
L_PWM1 = None   # left  motor PWM A
L_PWM2 = None   # left  motor PWM B
R_PWM1 = None   # right motor PWM A
R_PWM2 = None   # right motor PWM B

# ---------------------------------------------------------------------------
# Ultrasonic HC-SR04  (TODO – extract from bp3_ultrasonic.py)
# ---------------------------------------------------------------------------
# grep -E 'TRIG|ECHO|trig|echo' \
#   ~/RaspberryPiCar/RaspberryPi-Car/basic_project/bp3_ultrasonic.py
ULTRASONIC_TRIG = None
ULTRASONIC_ECHO = None

# ---------------------------------------------------------------------------
# Tracking sensors  (TODO – extract from bp10_tracking_car.py if needed)
# ---------------------------------------------------------------------------
# grep -E 'sensor|SENSOR|track|TRACK' \
#   ~/RaspberryPiCar/RaspberryPi-Car/basic_project/bp10_tracking_car.py
TRACK_LEFT   = None
TRACK_MIDDLE = None
TRACK_RIGHT  = None
