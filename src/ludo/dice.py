#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Ludo Game (Tkinter + Pillow)
File: dice.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Dice logic and image generation using Pillow for crisp rendering.

Usage: 
from ludo.dice import Dice

Notes: 
- Deterministic seed can be provided for reproducible tests.

===================================================================
"""
from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Optional

from PIL import Image, ImageDraw, ImageTk


@dataclass
class Dice:
    size: int = 96
    seed: Optional[int] = None

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)
        self._cache = {}

    def roll(self) -> int:
        return self._rng.randint(1, 6)

    def image_for(self, n: int):
        assert 1 <= n <= 6
        if n in self._cache:
            return self._cache[n]
        img = Image.new("RGBA", (self.size, self.size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        r = int(self.size * 0.12)
        margin = int(self.size * 0.2)
        # die face
        draw.rounded_rectangle([(2, 2), (self.size - 2, self.size - 2)], radius=16, fill=(250, 250, 250, 255), outline=(30, 30, 30, 255), width=2)
        # pip positions
        pts = [
            (margin, margin), (self.size // 2, margin), (self.size - margin, margin),
            (margin, self.size // 2), (self.size // 2, self.size // 2), (self.size - margin, self.size // 2),
            (margin, self.size - margin), (self.size // 2, self.size - margin), (self.size - margin, self.size - margin)
        ]
        mapping = {
            1: [4], 2: [0, 8], 3: [0, 4, 8], 4: [0, 2, 6, 8], 5: [0, 2, 4, 6, 8], 6: [0, 2, 3, 5, 6, 8]
        }
        for i in mapping[n]:
            x, y = pts[i]
            draw.ellipse([(x - r, y - r), (x + r, y + r)], fill=(30, 30, 30, 255))
        tk_img = ImageTk.PhotoImage(img)
        self._cache[n] = tk_img
        return tk_img
