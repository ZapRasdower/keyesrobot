#!/usr/bin/env python3
"""
Interactive ultrasonic-head pan teleop (curses).

The HC-SR04 sensor is mounted on a single pan servo. This swivels it
left/right; it has no tilt.

Keys:
  ← / →     pan left / right
  h / l     pan left / right (vim-style)
  c         centre at 90°
  + / -     adjust step size
  q / ESC   quit
"""

import curses

from robot.setup import gpio_session
from robot.ultrasonic import UltrasonicHead


def _loop(stdscr, head: UltrasonicHead) -> None:
    curses.curs_set(0)
    stdscr.keypad(True)
    step = 5.0

    def draw():
        stdscr.erase()
        stdscr.addstr(0, 0, "Ultrasonic head teleop")
        stdscr.addstr(2, 0, f"  pan  = {head.pan:6.1f}°")
        stdscr.addstr(3, 0, f"  step = {step:5.1f}°")
        stdscr.addstr(5, 0, "←/→ or h/l: pan    c: centre    +/-: step    q: quit")
        stdscr.refresh()

    draw()
    while True:
        ch = stdscr.getch()
        if ch in (curses.KEY_LEFT, ord("h")):
            head.nudge(-step)
        elif ch in (curses.KEY_RIGHT, ord("l")):
            head.nudge(+step)
        elif ch in (ord("c"), ord("C")):
            head.centre()
        elif ch in (ord("+"), ord("=")):
            step = min(step + 1.0, 45.0)
        elif ch in (ord("-"), ord("_")):
            step = max(step - 1.0, 1.0)
        elif ch in (ord("q"), ord("Q"), 27):
            break
        draw()


def main() -> None:
    with gpio_session(), UltrasonicHead() as head:
        curses.wrapper(_loop, head)
        print(f"final: pan={head.pan:.1f}°")


if __name__ == "__main__":
    main()
