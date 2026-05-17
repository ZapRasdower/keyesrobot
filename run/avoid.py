#!/usr/bin/env python3
"""
Entry point: obstacle-avoidance demo.

Usage:
    python3 -m run.avoid              # runs until Ctrl+C
    python3 -m run.avoid --seconds 30 # runs for 30 s then stops
"""

import argparse

from behaviors import avoid
from robot.setup import gpio_session


def main() -> None:
    parser = argparse.ArgumentParser(description="Obstacle-avoidance demo.")
    parser.add_argument(
        "--seconds", type=float, default=None,
        help="Run duration in seconds (default: run until Ctrl+C).",
    )
    args = parser.parse_args()

    with gpio_session():
        try:
            avoid.run(duration_s=args.seconds)
        except KeyboardInterrupt:
            print("\nInterrupted by user.")


if __name__ == "__main__":
    main()
