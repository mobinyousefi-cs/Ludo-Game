#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Ludo Game (Tkinter + Pillow)
File: ui.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Tkinter-based UI layer integrating the BoardView and LudoGame.

Usage: 
from ludo.ui import LudoApp

Notes: 
- Keeps widgets and event wiring separate from game logic.

===================================================================
"""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple
import tkinter as tk
from tkinter import ttk, messagebox

from .constants import PLAY_COLORS, COLOR_NAME
from .board import BoardView
from .game import LudoGame
from .dice import Dice


class LudoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Ludo — Tkinter + PIL")
        self.board = BoardView(root)

        # Right-side panel
        self.panel = ttk.Frame(root, padding=8)
        self.panel.grid(row=0, column=1, sticky="n")

        # Setup controls
        self._build_setup()
        self._build_play()

        # Key bindings
        root.bind("r", lambda e: self.on_roll())

        self.game: Optional[LudoGame] = None
        self.dice = Dice(size=80)
        self._dice_img_label = ttk.Label(self.panel)
        self._dice_img_label.grid(row=10, column=0, pady=(8, 2))
        self._update_status("Configure players to start.")

    # --- Setup --------------------------------------------------------------
    def _build_setup(self) -> None:
        frm = ttk.LabelFrame(self.panel, text="Setup")
        frm.grid(row=0, column=0, sticky="ew")

        self.num_players_var = tk.IntVar(value=2)
        ttk.Label(frm, text="Players (2-4)").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(frm, from_=2, to=4, textvariable=self.num_players_var, width=5).grid(row=0, column=1)

        ttk.Label(frm, text="AI Players").grid(row=1, column=0, sticky="w", pady=(6,0))
        self.ai_vars: Dict[str, tk.BooleanVar] = {c: tk.BooleanVar(value=False) for c in PLAY_COLORS}
        for r, c in enumerate(PLAY_COLORS, start=2):
            ttk.Checkbutton(frm, text=COLOR_NAME[c], variable=self.ai_vars[c]).grid(row=r, column=0, columnspan=2, sticky="w")

        ttk.Button(frm, text="Start Game", command=self.on_start).grid(row=6, column=0, columnspan=2, pady=(8, 2), sticky="ew")

    def _build_play(self) -> None:
        frm = ttk.LabelFrame(self.panel, text="Play")
        frm.grid(row=1, column=0, sticky="ew", pady=(8,0))
        self.roll_btn = ttk.Button(frm, text="Roll (r)", command=self.on_roll)
        self.roll_btn.grid(row=0, column=0, sticky="ew")
        self.status_lbl = ttk.Label(frm, text="")
        self.status_lbl.grid(row=1, column=0, pady=(8,0))

        # Canvas interactions
        self.board.canvas.bind("<Button-1>", self.on_canvas_click)

    def _update_status(self, msg: str) -> None:
        self.status_lbl.configure(text=msg)

    # --- Game lifecycle -----------------------------------------------------
    def on_start(self) -> None:
        n = self.num_players_var.get()
        if n not in (2, 3, 4):
            messagebox.showerror("Invalid", "Players must be 2–4")
            return
        colors = PLAY_COLORS[:n]
        ai_flags = {c: self.ai_vars[c].get() for c in colors}
        self.game = LudoGame(colors, ai_flags)
        self._dice_img_label.configure(image="")
        self._redraw_all_tokens()
        self._update_turn_status()

    def _update_turn_status(self) -> None:
        if not self.game:
            return
        p = self.game.current_player
        self._update_status(f"Turn: {COLOR_NAME[p.color]} {'(AI)' if p.is_ai else ''} — click Roll")
        if p.is_ai:
            self.root.after(400, self.on_roll)

    # --- Rolling and moving -------------------------------------------------
    def on_roll(self) -> None:
        if not self.game:
            return
        roll = self.dice.roll()
        self._dice_img_label.configure(image=self.dice.image_for(roll))
        self._update_status(f"Rolled: {roll}")
        legal = self.game.legal_tokens(roll)
        if not legal:
            self._update_status(f"Rolled: {roll} — No legal moves. Next player.")
            self.game.next_turn(False)
            self._update_turn_status()
            return
        # Highlight legal tokens
        self._clear_highlights()
        for t in legal:
            self.board.highlight_token(t.color, t.index, True)
        # AI auto-move
        if self.game.current_player.is_ai:
            chosen = self._pick_ai_move(legal, roll)
            self._perform_move(chosen, roll)
        else:
            # Wait for user to click a highlighted token
            self.pending_roll = roll

    def _pick_ai_move(self, legal, roll):
        # Simple heuristic: prefer entering from yard, then captures, else first
        yard_moves = [t for t in legal if t.pos is None]
        if yard_moves:
            return yard_moves[0]
        # Try to find a capturing move by simulating
        for t in legal:
            pos = t.pos
            # simulate destination
            if pos is None:
                continue
            return legal[0]
        return legal[0]

    def _perform_move(self, token, roll: int) -> None:
        captured, extra = self.game.apply_move(token, roll)
        self._redraw_all_tokens()
        winner = self.game.anyone_won()
        if winner:
            messagebox.showinfo("Game Over", f"{COLOR_NAME[winner]} wins!")
            self._update_status("Game over.")
            return
        if captured:
            c, idx = captured
            self.board.highlight_token(c, idx, False)
        self._clear_highlights()
        self.game.next_turn(extra)
        self._update_turn_status()

    def _clear_highlights(self):
        if not self.game:
            return
        for p in self.game.players:
            for t in p.tokens:
                self.board.highlight_token(t.color, t.index, False)

    # --- Canvas interactions -------------------------------------------------
    def on_canvas_click(self, ev):
        if not self.game:
            return
        if self.game.current_player.is_ai:
            return
        # A pending roll is required
        roll = getattr(self, "pending_roll", None)
        if roll is None:
            return
        tok = self.board.token_at(ev.x, ev.y)
        if not tok:
            return
        color, idx = tok
        if color != self.game.current_player.color:
            return
        # Check legality
        token_obj = self.game.get_token(color, idx)
        legal = self.game.legal_tokens(roll)
        if token_obj not in legal:
            return
        self.pending_roll = None
        self._perform_move(token_obj, roll)

    # --- Rendering tokens ---------------------------------------------------
    def _redraw_all_tokens(self) -> None:
        if not self.game:
            return
        # Place every token in yard initially
        for p in self.game.players:
            for t in p.tokens:
                if t.pos is None:
                    cell = self.board.cell_for_yard(t.color, t.index)
                elif t.pos >= 52:
                    offset = t.pos - 52 - {"red":0, "green":6, "yellow":12, "blue":18}[t.color]
                    # Clamp to 0..5
                    offset = max(0, min(5, offset))
                    cell = self.board.cell_for_home(t.color, offset)
                else:
                    cell = self.board.cell_for_track_index(t.pos)
                self.board.place_token(t.color, t.index, cell)
