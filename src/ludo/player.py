#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Ludo Game (Tkinter + Pillow)
File: player.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Player and Token classes representing game state for Ludo.

Usage: 
from ludo.player import Player, Token

Notes: 
- Token.pos None => in yard; 0..51 => on track; 52+ => in home column.

===================================================================
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

from .constants import ENTRY_INDEX, HOME_START, HOME_END, TOKENS_PER_PLAYER


@dataclass
class Token:
    color: str
    index: int  # 0..3 per player
    pos: Optional[int] = None  # None: yard; 0..51 track; >= HOME_START[color] home path

    def at_yard(self) -> bool:
        return self.pos is None

    def in_home(self) -> bool:
        return self.pos is not None and self.pos >= HOME_START[self.color]

    def reached_center(self) -> bool:
        return self.pos is not None and self.pos >= HOME_END


@dataclass
class Player:
    color: str
    is_ai: bool = False
    tokens: List[Token] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.tokens:
            self.tokens = [Token(self.color, i) for i in range(TOKENS_PER_PLAYER)]

    def all_home(self) -> bool:
        return all(t.reached_center() for t in self.tokens)

    def legal_moves(self, roll: int, ahead_is_occupied, wrap) -> List[Token]:
        """Return list of tokens that can move with the given die roll.

        ahead_is_occupied(token, steps) -> (occupied: bool, by_self: bool, by_enemy: bool)
        wrap(index) -> index % 52
        """
        legal: List[Token] = []
        for t in self.tokens:
            if t.reached_center():
                continue
            if t.at_yard():
                if roll == 6:
                    # May enter if entry square not blocked by own token
                    dst = ENTRY_INDEX[self.color]
                    occ, by_self, _ = ahead_is_occupied(t, 0, absolute=dst)
                    if not by_self:
                        legal.append(t)
                continue
            # Move along the track
            curr = t.pos
            assert curr is not None
            entry = ENTRY_INDEX[self.color]
            steps_to_entry = (entry - curr - 1) % 52 + 1
            if roll > steps_to_entry:
                # into home column
                home_steps = roll - steps_to_entry
                if home_steps <= 6:
                    dst_abs = HOME_START[self.color] + home_steps - 1
                    occ, by_self, _ = ahead_is_occupied(t, roll, absolute=dst_abs)
                    if not by_self:
                        legal.append(t)
            else:
                # stay on track
                dst = wrap(curr + roll)
                occ, by_self, _ = ahead_is_occupied(t, roll, absolute=dst)
                if not by_self:
                    legal.append(t)
        return legal
