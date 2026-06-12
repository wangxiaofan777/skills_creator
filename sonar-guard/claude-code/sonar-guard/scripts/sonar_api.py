#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compatibility wrapper — canonical: sonar-guard/scripts/sonar_api.py"""
import runpy
from pathlib import Path

_CANONICAL = Path(__file__).resolve().parents[3] / "scripts" / "sonar_api.py"
if __name__ == "__main__":
    runpy.run_path(str(_CANONICAL), run_name="__main__")
