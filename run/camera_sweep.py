#!/usr/bin/env python3
"""
Sweep the camera pan/tilt servos through their range. Visual sanity check.

Usage:
    python3 -m run.camera_sweep
    python3 -m run.camera_sweep --min 45 --max 135 --step 10 --dwell 0.15
"""

import argparse
import time
from typing import Callable

from robot.camera import CameraMount
from robot.setup import gpio_session


def _sweep_axis(
    set_fn: Callable[[float], None],
    label: str,
    lo: float,
    hi: float,
    step: float,
    dwell_s: float,
) -> None:
    print(f"{label}: {lo}° → {hi}°")
    a = lo
    while a <= hi:
        set_fn(a)
        time.sleep(dwell_s)
        a += step

    print(f"{label}: {hi}° → {lo}°")
    a = hi
    while a >= lo:
        set_fn(a)
        time.sleep(dwell_s)
        a -= step


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--min", dest="lo", type=float, default=30.0)
    p.add_argument("--max", dest="hi", type=float, default=150.0)
    p.add_argument("--step", type=float, default=15.0)
    p.add_argument("--dwell", type=float, default=0.25,
                   help="Seconds to hold each step (default 0.25).")
    args = p.parse_args()

    with gpio_session(), CameraMount() as cam:
        try:
            _sweep_axis(cam.set_pan, "pan", args.lo, args.hi, args.step, args.dwell)
            cam.set_pan(90.0)
            time.sleep(0.4)
            _sweep_axis(cam.set_tilt, "tilt", args.lo, args.hi, args.step, args.dwell)
            cam.centre()
            time.sleep(0.3)
        except KeyboardInterrupt:
            print("\nInterrupted.")


if __name__ == "__main__":
    main()
