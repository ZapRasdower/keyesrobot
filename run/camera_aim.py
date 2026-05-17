#!/usr/bin/env python3
"""
Interactive camera pan/tilt teleop (curses).

Keys:
  ← / →   pan
  ↑ / ↓   tilt
  h/l     pan  (vim-style)
  j/k     tilt (vim-style; j = down, k = up)
  c       centre both axes
  + / -   adjust step size
  q / ESC quit

Run in a real terminal.
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
        pan, tilt = cam.angles
        stdscr.addstr(0, 0, "Camera teleop")
        stdscr.addstr(2, 0, f"  pan  = {pan:6.1f}°")
        stdscr.addstr(3, 0, f"  tilt = {tilt:6.1f}°")
        stdscr.addstr(4, 0, f"  step = {step:5.1f}°")
        stdscr.addstr(6, 0, "arrows / hjkl: move    c: centre    +/-: step    q: quit")
        stdscr.refresh()

    draw()
    while True:
        ch = stdscr.getch()
        pan, tilt = cam.angles
        if ch in (curses.KEY_LEFT, ord("h")):
            cam.set_pan(pan - step)
        elif ch in (curses.KEY_RIGHT, ord("l")):
            cam.set_pan(pan + step)
        elif ch in (curses.KEY_UP, ord("k")):
            cam.set_tilt(tilt + step)
        elif ch in (curses.KEY_DOWN, ord("j")):
            cam.set_tilt(tilt - step)
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
        pan, tilt = cam.angles
        print(f"final: pan={pan:.1f}°  tilt={tilt:.1f}°")


if __name__ == "__main__":
    main()
