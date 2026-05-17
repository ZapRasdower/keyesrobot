#!/usr/bin/env python3
"""
One-shot camera aim: set pan and/or tilt angles, then exit.

Usage:
    python3 -m run.camera_set --pan 120 --tilt 60
    python3 -m run.camera_set --pan 90          # tilt unchanged
    python3 -m run.camera_set --centre
"""

import argparse
import time

from robot.camera import CameraMount
from robot.setup import gpio_session


def main() -> None:
    p = argparse.ArgumentParser(description="Set camera pan/tilt and exit.")
    p.add_argument("--pan", type=float, help="Pan angle 0–180°.")
    p.add_argument("--tilt", type=float, help="Tilt angle 0–180°.")
    p.add_argument("--centre", action="store_true", help="Centre both axes first.")
    p.add_argument("--hold", type=float, default=0.5,
                   help="Seconds to hold PWM before exiting (default 0.5).")
    args = p.parse_args()

    if not (args.pan is not None or args.tilt is not None or args.centre):
        p.error("specify at least one of --pan / --tilt / --centre")

    with gpio_session(), CameraMount() as cam:
        if args.centre:
            cam.centre()
        cam.aim(pan=args.pan, tilt=args.tilt)
        time.sleep(args.hold)
        pan, tilt = cam.angles
        print(f"pan={pan:.1f}°  tilt={tilt:.1f}°")


if __name__ == "__main__":
    main()
