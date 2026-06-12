#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Install sonar-guard from any cwd. Locates skills_creator then delegates to install.py.

Usage (from business repo):
  # After setup-env.ps1 / one successful install from <skills_creator>:
  python "$env:SONARGUARD_HOME/sonar-guard/scripts/install_bootstrap.py" --platform all --repo .
  python .sonarguard/install.py --platform all --repo .
"""
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


def _save_package_root(path: Path) -> None:
    _CONFIG.parent.mkdir(parents=True, exist_ok=True)
    data = _load_config()
    data["packageRoot"] = str(path.resolve())
    _CONFIG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _valid_root(path: Path) -> bool:
    return (path / "sonar-guard" / "scripts" / "install.py").is_file()


def _root_from_bootstrap_location() -> Path | None:
    """When invoked via skills_creator/sonar-guard/scripts/install_bootstrap.py, auto-detect root."""
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
        print(
            f"错误: --package 无效，未找到 {root / 'sonar-guard' / 'scripts' / 'install.py'}",
            file=sys.stderr,
        )
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

    print("未找到 sonar-guard 安装包 (skills_creator 仓库)。", file=sys.stderr)
    print("任选其一（均不需要固定盘符）:", file=sys.stderr)
    print("  A) cd <skills_creator> && python sonar-guard/scripts/install.py --repo <business-repo> ...", file=sys.stderr)
    print("  B) 运行 setup-env.ps1 / setup-env.sh 配置 SONARGUARD_HOME 后重试", file=sys.stderr)
    print("  C) python .../install_bootstrap.py --package <你的skills_creator路径> --repo . ...", file=sys.stderr)
    try:
        entered = input("或输入 skills_creator 绝对路径: ").strip()
    except (EOFError, KeyboardInterrupt):
        print(file=sys.stderr)
        raise SystemExit(1) from None
    if not entered:
        raise SystemExit(1)
    root = Path(entered).expanduser().resolve()
    if not _valid_root(root):
        print(f"错误: 路径无效 {root}", file=sys.stderr)
        raise SystemExit(1)
    _save_package_root(root)
    return root


def main() -> int:
    ap = argparse.ArgumentParser(description="Bootstrap sonar-guard install (any cwd)")
    ap.add_argument("--package", "-P", help="skills_creator 仓库根路径")
    known, rest = ap.parse_known_args()
    root = resolve_package_root(known.package)
    _save_package_root(root)
    install_py = root / "sonar-guard" / "scripts" / "install.py"
    print(f"Using package: {root}")
    return subprocess.call([sys.executable, str(install_py)] + rest)


if __name__ == "__main__":
    raise SystemExit(main())
