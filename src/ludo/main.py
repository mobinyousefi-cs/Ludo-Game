#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Ludo Game (Tkinter + Pillow)
File: main.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Executable entrypoint to launch the Ludo game UI.

Usage: 
python -m ludo

Notes: 
- Sets a modern Tk theme when available.

===================================================================
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk

from .ui import LudoApp


def _set_theme(root: tk.Tk) -> None:
    try:
        root.call("source", "sun-valley.tcl")  # optional if theme file is present
        ttk.Style().theme_use("sun-valley-dark")
    except Exception:
        try:
            ttk.Style().theme_use("clam")
        except Exception:
            pass


def main() -> None:
    root = tk.Tk()
    _set_theme(root)
    app = LudoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
