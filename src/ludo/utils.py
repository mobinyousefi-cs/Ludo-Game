#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Ludo Game (Tkinter + Pillow)
File: utils.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Utility helpers for geometry and Canvas drawing.

Usage: 
from ludo.utils import cell_to_px

Notes: 
- Pure helpers to keep other modules lean.

===================================================================
"""
from __future__ import annotations
from typing import Tuple

from .constants import SIZE, MARGIN


def cell_to_px(x: float, y: float) -> Tuple[int, int, int, int]:
    """Convert a logical grid cell (x,y) to pixel-rectangle on the Canvas.

    Returns (x0, y0, x1, y1)
    """
    x0 = int(x * SIZE + MARGIN)
    y0 = int(y * SIZE + MARGIN)
    x1 = int((x + 1) * SIZE - MARGIN)
    y1 = int((y + 1) * SIZE - MARGIN)
    return x0, y0, x1, y1


def center_of_cell(x: float, y: float) -> Tuple[int, int]:
    x0, y0, x1, y1 = cell_to_px(x, y)
    return (x0 + x1) // 2, (y0 + y1) // 2
