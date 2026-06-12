#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thin wrapper — use uninstall.py --platform cursor."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    uninstall_py = Path(__file__).resolve().parent / "uninstall.py"
    args = [sys.executable, str(uninstall_py), "--platform", "cursor", *sys.argv[1:]]
    raise SystemExit(subprocess.call(args))
