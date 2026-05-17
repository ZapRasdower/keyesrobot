#!/usr/bin/env python3
"""
One-shot camera tilt: set the angle and exit.

Camera has only a tilt servo on this kit.

Usage:
    python3 -m run.camera_set --tilt 60
    python3 -m run.camera_set --centre
"""

import argparse
import time

from robot.camera import CameraMount
from robot.setup import gpio_session


def main() -> None:
    p = argparse.ArgumentParser(description="Set camera tilt and exit.")
    p.add_argument("--tilt", type=float, help="Tilt angle 0–180°.")
    p.add_argument("--centre", action="store_true", help="Centre tilt at 90°.")
    p.add_argument("--hold", type=float, default=0.5,
                   help="Seconds to hold PWM before exiting (default 0.5).")
    args = p.parse_args()

    if args.tilt is None and not args.centre:
        p.error("specify --tilt or --centre")

    with gpio_session(), CameraMount() as cam:
        if args.centre:
            cam.centre()
        if args.tilt is not None:
            cam.set_tilt(args.tilt)
        time.sleep(args.hold)
        print(f"tilt={cam.tilt:.1f}°")


if __name__ == "__main__":
    main()
