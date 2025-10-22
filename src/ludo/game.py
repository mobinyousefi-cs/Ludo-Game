#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Ludo Game (Tkinter + Pillow)
File: game.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Core game rules and state transitions for Ludo.

Usage: 
from ludo.game import LudoGame

Notes: 
- Keeps UI-agnostic logic separate from rendering.

===================================================================
"""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple

from .constants import ENTRY_INDEX, HOME_START, HOME_END, SAFE_INDICES, TOKENS_PER_PLAYER
from .player import Player, Token


def wrap52(i: int) -> int:
    return i % 52


class LudoGame:
    def __init__(self, colors: List[str], ai_flags: Optional[Dict[str, bool]] = None):
        self.players: List[Player] = []
        self.turn = 0  # index into self.players
        self.last_roll: Optional[int] = None
        self.ai_flags = ai_flags or {}
        for c in colors:
            self.players.append(Player(c, is_ai=self.ai_flags.get(c, False)))

    # --- Queries ------------------------------------------------------------
    @property
    def current_player(self) -> Player:
        return self.players[self.turn]

    def get_token(self, color: str, idx: int) -> Token:
        for p in self.players:
            if p.color == color:
                return p.tokens[idx]
        raise KeyError(color)

    def anyone_won(self) -> Optional[str]:
        for p in self.players:
            if p.all_home():
                return p.color
        return None

    def ahead_is_occupied(self, token: Token, steps: int, absolute: Optional[int] = None) -> Tuple[bool, bool, bool]:
        """Check if destination square is occupied. Returns (occ, by_self, by_enemy)."""
        dst = absolute
        if dst is None:
            assert token.pos is not None
            dst = wrap52(token.pos + steps)
        # Check track occupancy
        for p in self.players:
            for t in p.tokens:
                if t is token or t.pos is None:
                    continue
                # Home column occupancy check
                if t.pos >= HOME_START[t.color]:
                    if dst >= HOME_START[t.color] and dst == t.pos:
                        return True, (p is self.current_player), (p is not self.current_player)
                    continue
                if dst < HOME_START[token.color] and t.pos == dst:
                    return True, (p is self.current_player), (p is not self.current_player)
        return False, False, False

    def legal_tokens(self, roll: int) -> List[Token]:
        return self.current_player.legal_moves(roll, self.ahead_is_occupied, wrap52)

    # --- Actions ------------------------------------------------------------
    def apply_move(self, token: Token, roll: int) -> Tuple[Optional[Tuple[str, int]], bool]:
        """Move token per roll. Returns (captured_token_key, extra_turn)."""
        extra_turn = (roll == 6)
        if token.at_yard():
            token.pos = ENTRY_INDEX[token.color]
            captured = self._capture_if_any(token)
            return captured, extra_turn

        # Move along track or into home column
        assert token.pos is not None
        entry = ENTRY_INDEX[token.color]
        steps_to_entry = (entry - token.pos - 1) % 52 + 1
        if roll > steps_to_entry:
            # into home column
            home_steps = roll - steps_to_entry
            token.pos = HOME_START[token.color] + home_steps - 1
            return None, extra_turn
        else:
            # on track
            token.pos = wrap52(token.pos + roll)
            captured = self._capture_if_any(token)
            return captured, extra_turn

    def _capture_if_any(self, mover: Token) -> Optional[Tuple[str, int]]:
        if mover.pos in SAFE_INDICES:
            return None
        if mover.pos is None or mover.pos >= HOME_START[mover.color]:
            return None
        for p in self.players:
            for t in p.tokens:
                if t is mover or t.pos is None or t.pos >= HOME_START[t.color]:
                    continue
                if t.pos == mover.pos:
                    t.pos = None  # send back to yard
                    return (t.color, t.index)
        return None

    def next_turn(self, had_extra: bool) -> None:
        if not had_extra:
            self.turn = (self.turn + 1) % len(self.players)
