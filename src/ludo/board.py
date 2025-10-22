#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Ludo Game (Tkinter + Pillow)
File: board.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Board rendering and geometry helpers for the Ludo Canvas.

Usage: 
from ludo.board import BoardView

Notes: 
- Pure drawing logic; no game rules here.

===================================================================
"""
from __future__ import annotations
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
import tkinter as tk

from .constants import SIZE, GRID, BOARD_PX, TOKEN_RADIUS, HIGHLIGHT_WIDTH, TRACK, HOME_COL, YARD_POS, PLAY_COLORS, COLOR_NAME
from .utils import center_of_cell


@dataclass
class TokenRender:
    token_id: int
    halo_id: Optional[int]


class BoardView:
    def __init__(self, root: tk.Tk):
        self.canvas = tk.Canvas(root, width=BOARD_PX, height=BOARD_PX, bg="#fafafa", highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=20)
        self.token_items: Dict[Tuple[str, int], TokenRender] = {}
        self._draw_grid()
        self._draw_static_board()

    # --- Drawing primitives -------------------------------------------------
    def _draw_grid(self) -> None:
        g = GRID
        for i in range(g + 1):
            x = i * SIZE
            self.canvas.create_line(x, 0, x, BOARD_PX, fill="#e6e6e6")
            self.canvas.create_line(0, x, BOARD_PX, x, fill="#e6e6e6")

    def _draw_static_board(self) -> None:
        # Draw central star
        c = SIZE * 7
        s = SIZE * 3
        self.canvas.create_polygon(c, c - s, c + s, c, c, c + s, c - s, c, fill="#ddd", outline="")

        # Colored home triangles
        self.canvas.create_polygon(0, BOARD_PX, SIZE * 6, BOARD_PX, c, c, fill="red", outline="")
        self.canvas.create_polygon(0, 0, 0, SIZE * 6, c, c, fill="green", outline="")
        self.canvas.create_polygon(BOARD_PX, 0, BOARD_PX - SIZE * 6, 0, c, c, fill="yellow", outline="")
        self.canvas.create_polygon(BOARD_PX, BOARD_PX, BOARD_PX, BOARD_PX - SIZE * 6, c, c, fill="blue", outline="")

        # Track squares
        for idx, (x, y) in enumerate(TRACK):
            x0 = x * SIZE
            y0 = y * SIZE
            x1 = x0 + SIZE
            y1 = y0 + SIZE
            fill = "white"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="#999")

        # Home columns per color
        for color, coords in HOME_COL.items():
            for (x, y) in coords:
                x0 = x * SIZE
                y0 = y * SIZE
                x1 = x0 + SIZE
                y1 = y0 + SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#222")

        # Yard labels
        for i, color in enumerate(PLAY_COLORS):
            x, y = {
                "red": (SIZE * 2.5, SIZE * 12.2),
                "green": (SIZE * 2.5, SIZE * 0.2),
                "yellow": (SIZE * 12.5, SIZE * 0.2),
                "blue": (SIZE * 12.5, SIZE * 12.2),
            }[color]
            self.canvas.create_text(x, y, text=f"{COLOR_NAME[color]}", font=("Segoe UI", 12, "bold"), fill=color)

    # --- Tokens -------------------------------------------------------------
    def place_token(self, color: str, idx: int, cell_xy: Tuple[float, float]) -> None:
        cx, cy = center_of_cell(*cell_xy)
        r = TOKEN_RADIUS
        key = (color, idx)
        if key in self.token_items:
            # move
            self.canvas.coords(self.token_items[key].token_id, cx - r, cy - r, cx + r, cy + r)
        else:
            token_id = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color, outline="#222", width=2)
            self.token_items[key] = TokenRender(token_id=token_id, halo_id=None)

    def highlight_token(self, color: str, idx: int, on: bool) -> None:
        key = (color, idx)
        tr = self.token_items.get(key)
        if not tr:
            return
        if on and tr.halo_id is None:
            x0, y0, x1, y1 = self.canvas.coords(tr.token_id)
            tr.halo_id = self.canvas.create_oval(x0 - HIGHLIGHT_WIDTH, y0 - HIGHLIGHT_WIDTH, x1 + HIGHLIGHT_WIDTH, y1 + HIGHLIGHT_WIDTH, outline="#222", width=HIGHLIGHT_WIDTH, dash=(4,2))
        elif not on and tr.halo_id is not None:
            self.canvas.delete(tr.halo_id)
            tr.halo_id = None

    def token_at(self, x: int, y: int) -> Optional[Tuple[str, int]]:
        """Return (color, idx) if a token's oval is under the click position."""
        items = self.canvas.find_overlapping(x-1, y-1, x+1, y+1)
        for (color, idx), tr in self.token_items.items():
            if tr.token_id in items:
                return (color, idx)
        return None

    # --- Helpers to compute logical positions to grid cells -----------------
    def cell_for_track_index(self, idx: int) -> Tuple[float, float]:
        return TRACK[idx % len(TRACK)]

    def cell_for_home(self, color: str, offset: int) -> Tuple[float, float]:
        return HOME_COL[color][offset]

    def cell_for_yard(self, color: str, idx: int) -> Tuple[float, float]:
        return YARD_POS[color][idx]
