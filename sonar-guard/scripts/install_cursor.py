#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-click install sonar-guard for Cursor.

Usage (from skills_creator repo root):
  python sonar-guard/scripts/install_cursor.py --repo <path-to-git-repo>
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from lib.cursor_install_lib import (  # noqa: E402
    ensure_sonarguard_json,
    install_cursor_rules,
    install_pre_commit_hook,
    print_post_install_hints,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install sonar-guard for Cursor")
    parser.add_argument("--repo", "-r", default=".", help="Target git repo (default: cwd)")
    parser.add_argument("--no-hook", action="store_true", help="Skip pre-commit hook installation")
    parser.add_argument("--force-config", action="store_true", help="Overwrite existing .sonarguard.json")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()

    try:
        target_dir, installed = install_cursor_rules()
        print(f"Installed {len(installed)} Cursor rules → {target_dir}")

        config_path, created = ensure_sonarguard_json(repo, force=args.force_config)
        print(f"{'Created' if created else 'Kept existing'} {config_path}")

        hook_installed = False
        if not args.no_hook:
            _, pre_commit_path, action = install_pre_commit_hook(repo)
            print(f"pre-commit hook {action}: {pre_commit_path}")
            hook_installed = True

        print_post_install_hints(repo, config_path=config_path, hook_installed=hook_installed)
    except (FileNotFoundError, subprocess.CalledProcessError, OSError) as err:
        print(f"Install failed: {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
