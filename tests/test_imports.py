#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Ludo Game (Tkinter + Pillow)
File: test_imports.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Smoke tests to ensure modules import and package metadata is intact.

Usage: 
pytest -q

Notes: 
- Extend with behavioral tests as needed.

===================================================================
"""
from importlib import import_module


def test_import_package():
    m = import_module("ludo")
    assert hasattr(m, "main")


def test_import_modules():
    for mod in ("constants", "utils", "player", "dice", "board", "game", "ui"):
        import_module(f"ludo.{mod}")
