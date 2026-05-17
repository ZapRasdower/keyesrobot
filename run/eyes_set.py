#!/usr/bin/env python3
"""
One-shot ultrasonic-head pan: swivel the HC-SR04 mount and exit.

Usage:
    python3 -m run.eyes_set --pan 45    # look hard left
    python3 -m run.eyes_set --pan 135   # look hard right
    python3 -m run.eyes_set --centre
"""

import argparse
import time

from robot.setup import gpio_session
from robot.ultrasonic import UltrasonicHead


def main() -> None:
    p = argparse.ArgumentParser(description="Set ultrasonic-head pan and exit.")
    p.add_argument("--pan", type=float, help="Pan angle 0–180°.")
    p.add_argument("--centre", action="store_true", help="Centre pan at 90°.")
    p.add_argument("--hold", type=float, default=0.5,
                   help="Seconds to hold PWM before exiting (default 0.5).")
    args = p.parse_args()

    if args.pan is None and not args.centre:
        p.error("specify --pan or --centre")

    with gpio_session(), UltrasonicHead() as head:
        if args.centre:
            head.centre()
        if args.pan is not None:
            head.set_pan(args.pan)
        time.sleep(args.hold)
        print(f"pan={head.pan:.1f}°")


if __name__ == "__main__":
    main()
