#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Ludo Game (Tkinter + Pillow)
File: __init__.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Package initializer for the Ludo game. Exposes the main entrypoints.

Usage: 
python -m ludo 

Notes: 
- Keeps the package namespace tidy.

===================================================================
"""

from .main import main

__all__ = ["main"]
