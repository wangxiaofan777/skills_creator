#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-click remove sonar-guard Cursor install.

Usage:
  python sonar-guard/scripts/uninstall_cursor.py --repo <path-to-git-repo>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from lib.cursor_install_lib import (  # noqa: E402
    uninstall_cursor_rules,
    uninstall_pre_commit_hook,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Uninstall sonar-guard for Cursor")
    parser.add_argument("--repo", "-r", default=".", help="Target git repo (default: cwd)")
    parser.add_argument("--purge-config", action="store_true", help="Also delete <repo>/.sonarguard.json")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()

    try:
        target_dir, removed = uninstall_cursor_rules()
        print(f"Removed {len(removed)} Cursor rules from {target_dir}")

        hook = uninstall_pre_commit_hook(repo)
        if hook.get("removed"):
            print(f"Removed pre-commit hook payload: {hook['guardDir']}")
        else:
            print("Skipped pre-commit (not a git repo or hook absent).")

        config_path = repo / ".sonarguard.json"
        if args.purge_config and config_path.is_file():
            config_path.unlink()
            print(f"Removed {config_path}")
        else:
            print("Kept .sonarguard.json (pass --purge-config to delete).")

        print("\nUninstall complete. Start a new Cursor Agent chat to reload rules.")
    except OSError as err:
        print(f"Uninstall failed: {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
