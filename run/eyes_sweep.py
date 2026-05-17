#!/usr/bin/env python3
"""
Sweep the ultrasonic head left ↔ right.

Usage:
    python3 -m run.eyes_sweep
    python3 -m run.eyes_sweep --min 45 --max 135 --step 10 --dwell 0.15
"""

import argparse
import time

from robot.setup import gpio_session
from robot.ultrasonic import UltrasonicHead


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--min", dest="lo", type=float, default=30.0)
    p.add_argument("--max", dest="hi", type=float, default=150.0)
    p.add_argument("--step", type=float, default=15.0)
    p.add_argument("--dwell", type=float, default=0.25)
    args = p.parse_args()

    with gpio_session(), UltrasonicHead() as head:
        try:
            print(f"pan: {args.lo}° → {args.hi}°")
            a = args.lo
            while a <= args.hi:
                head.set_pan(a)
                time.sleep(args.dwell)
                a += args.step
            print(f"pan: {args.hi}° → {args.lo}°")
            a = args.hi
            while a >= args.lo:
                head.set_pan(a)
                time.sleep(args.dwell)
                a -= args.step
            head.centre()
            time.sleep(0.3)
        except KeyboardInterrupt:
            print("\nInterrupted.")


if __name__ == "__main__":
    main()
