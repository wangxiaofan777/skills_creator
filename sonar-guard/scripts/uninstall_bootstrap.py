#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uninstall sonar-guard from any cwd. Locates skills_creator then delegates to uninstall.py."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

_CONFIG = Path.home() / ".config" / "sonarguard" / "config.json"


def _load_config() -> dict:
    if not _CONFIG.is_file():
        return {}
    try:
        return json.loads(_CONFIG.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _valid_root(path: Path) -> bool:
    return (path / "sonar-guard" / "scripts" / "uninstall.py").is_file()


def _root_from_bootstrap_location() -> Path | None:
    scripts_dir = Path(__file__).resolve().parent
    if scripts_dir.name != "scripts" or scripts_dir.parent.name != "sonar-guard":
        return None
    root = scripts_dir.parent.parent
    return root if _valid_root(root) else None


def resolve_package_root(package: str | None) -> Path:
    if package:
        root = Path(package).expanduser().resolve()
        if _valid_root(root):
            return root
        print("错误: --package 无效", file=sys.stderr)
        raise SystemExit(1)

    auto = _root_from_bootstrap_location()
    if auto is not None:
        return auto

    env = os.environ.get("SONARGUARD_HOME", "").strip()
    if env:
        root = Path(env).expanduser().resolve()
        if _valid_root(root):
            return root

    saved = _load_config().get("packageRoot", "").strip()
    if saved:
        root = Path(saved).expanduser().resolve()
        if _valid_root(root):
            return root

    print("未找到 sonar-guard 安装包。请用 --package 或设置 SONARGUARD_HOME。", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    ap = argparse.ArgumentParser(description="Bootstrap sonar-guard uninstall (any cwd)")
    ap.add_argument("--package", "-P", help="skills_creator 仓库根路径")
    known, rest = ap.parse_known_args()
    root = resolve_package_root(known.package)
    uninstall_py = root / "sonar-guard" / "scripts" / "uninstall.py"
    print(f"Using package: {root}")
    return subprocess.call([sys.executable, str(uninstall_py)] + rest)


if __name__ == "__main__":
    raise SystemExit(main())
