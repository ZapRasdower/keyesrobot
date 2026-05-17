#!/usr/bin/env python3
"""
Interactive camera tilt teleop (curses).

Camera has only tilt on this kit (no pan).

Keys:
  ↑ / ↓     tilt up / down
  k / j     tilt up / down (vim-style)
  c         centre at 90°
  + / -     adjust step size
  q / ESC   quit
"""

import curses

from robot.camera import CameraMount
from robot.setup import gpio_session


def _loop(stdscr, cam: CameraMount) -> None:
    curses.curs_set(0)
    stdscr.keypad(True)
    step = 5.0

    def draw():
        stdscr.erase()
        stdscr.addstr(0, 0, "Camera tilt teleop")
        stdscr.addstr(2, 0, f"  tilt = {cam.tilt:6.1f}°")
        stdscr.addstr(3, 0, f"  step = {step:5.1f}°")
        stdscr.addstr(5, 0, "↑/↓ or k/j: tilt    c: centre    +/-: step    q: quit")
        stdscr.refresh()

    draw()
    while True:
        ch = stdscr.getch()
        if ch in (curses.KEY_UP, ord("k")):
            cam.nudge(+step)
        elif ch in (curses.KEY_DOWN, ord("j")):
            cam.nudge(-step)
        elif ch in (ord("c"), ord("C")):
            cam.centre()
        elif ch in (ord("+"), ord("=")):
            step = min(step + 1.0, 45.0)
        elif ch in (ord("-"), ord("_")):
            step = max(step - 1.0, 1.0)
        elif ch in (ord("q"), ord("Q"), 27):
            break
        draw()


def main() -> None:
    with gpio_session(), CameraMount() as cam:
        curses.wrapper(_loop, cam)
        print(f"final: tilt={cam.tilt:.1f}°")


if __name__ == "__main__":
    main()
