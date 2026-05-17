#!/usr/bin/env python3
"""
Aim the camera (optional) and capture a still with rpicam-still.

Usage:
    python3 -m run.camera_snap                            # snap with current aim
    python3 -m run.camera_snap --pan 120 --tilt 60        # aim then snap
    python3 -m run.camera_snap -o shot.jpg --timeout 2000

Requires `rpicam-still` on PATH (Raspberry Pi OS Trixie default).
"""

import argparse
import shutil
import subprocess
import sys
import time

from robot.camera import CameraMount
from robot.setup import gpio_session


def _capture(output: str, timeout_ms: int) -> None:
    cmd = ["rpicam-still", "-o", output, "--timeout", str(timeout_ms)]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"wrote {output}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--pan", type=float, help="Pan angle 0–180° before capture.")
    p.add_argument("--tilt", type=float, help="Tilt angle 0–180° before capture.")
    p.add_argument("-o", "--output", default="snap.jpg")
    p.add_argument("--timeout", type=int, default=1000,
                   help="rpicam-still timeout in ms (default 1000).")
    p.add_argument("--settle", type=float, default=0.4,
                   help="Seconds to wait after aiming before capture (default 0.4).")
    args = p.parse_args()

    if shutil.which("rpicam-still") is None:
        sys.exit("rpicam-still not found on PATH.")

    if args.pan is not None or args.tilt is not None:
        with gpio_session(), CameraMount() as cam:
            cam.aim(pan=args.pan, tilt=args.tilt)
            time.sleep(args.settle)
            _capture(args.output, args.timeout)
    else:
        _capture(args.output, args.timeout)


if __name__ == "__main__":
    main()
