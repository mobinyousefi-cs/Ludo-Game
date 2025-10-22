#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Ludo Game (Tkinter + Pillow)
File: constants.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Global constants and geometry definitions for the Ludo board and tokens.

Usage: 
from ludo.constants import *

Notes: 
- Board is drawn on a 15x15 logical grid; each cell is SIZE px.
- Path indices run 0..51 (52 cells around), with 6-entry home columns per color.

===================================================================
"""

from __future__ import annotations

SIZE = 36  # pixels per cell
GRID = 15  # 15x15 logical grid
BOARD_PX = GRID * SIZE
MARGIN = 6
TOKEN_RADIUS = SIZE * 0.35
HIGHLIGHT_WIDTH = 4

PLAY_COLORS = ["red", "green", "yellow", "blue"]
COLOR_NAME = {
    "red": "Red",
    "green": "Green",
    "yellow": "Yellow",
    "blue": "Blue",
}

# Entry squares and start indices per color
ENTRY_INDEX = {
    "red": 0,
    "green": 13,
    "yellow": 26,
    "blue": 39,
}

SAFE_INDICES = {0, 8, 13, 21, 26, 34, 39, 47}  # standard safe tiles

# Home column start index per color (abstract index beyond 51)
HOME_START = {
    "red": 52,
    "green": 58,
    "yellow": 64,
    "blue": 70,
}
HOME_END = 76  # exclusive upper bound
HOME_LEN = 6
TOKENS_PER_PLAYER = 4

# Logical track coordinates for a classic Ludo board (0..51)
# Mapped onto a 15x15 grid. Coordinates are (x, y) with (0,0) top-left.
TRACK = [
    (6, 14), (6, 13), (6, 12), (6, 11), (6, 10), (5, 10), (4, 10), (3, 10), (2, 10), (1, 10), (0, 10),
    (0, 9), (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (6, 7), (6, 6), (7, 6), (8, 6),
    (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0), (9, 0), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4),
    (10, 5), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (14, 7), (14, 8), (13, 8), (12, 8), (11, 8),
    (10, 8), (10, 9), (10, 10), (9, 10), (8, 10),
]

# Home column coordinates per color; index 0..5 maps to 6 steps to center (7,7)
HOME_COL = {
    "red":   [(7, 13 - i) for i in range(1, 7)],  # up towards center
    "green": [(1 + i, 7) for i in range(1, 7)],   # right towards center
    "yellow":[(7, 1 + i) for i in range(1, 7)],   # down towards center
    "blue":  [(13 - i, 7) for i in range(1, 7)],  # left towards center
}

# Yard (starting) positions (4 per color) within each corner square
YARD_POS = {
    "red":    [(1.5, 12.5), (3.5, 12.5), (1.5, 14.5), (3.5, 14.5)],
    "green":  [(1.5, 0.5),  (3.5, 0.5),  (1.5, 2.5),  (3.5, 2.5)],
    "yellow": [(11.5, 0.5), (13.5, 0.5), (11.5, 2.5), (13.5, 2.5)],
    "blue":   [(11.5, 12.5),(13.5, 12.5),(11.5, 14.5),(13.5, 14.5)],
}

CENTER = (7, 7)
