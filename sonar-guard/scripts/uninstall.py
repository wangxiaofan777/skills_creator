#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-click remove sonar-guard.

Usage:
  python sonar-guard/scripts/uninstall.py --platform all --repo <path-to-git-repo>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from lib.install_lib import (  # noqa: E402
    PLATFORMS,
    resolve_platforms,
    uninstall_claude_skill,
    uninstall_codex_agents,
    uninstall_cursor_rules,
    uninstall_pre_commit_hook,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Uninstall sonar-guard")
    parser.add_argument("--platform", "-p", choices=PLATFORMS, default="all")
    parser.add_argument("--repo", "-r", default=".", help="Target git repo")
    parser.add_argument("--purge-config", action="store_true", help="Also delete .sonarguard.json")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    platforms = resolve_platforms(args.platform)
    if args.platform == "codex":
        platforms = {"codex"}

    try:
        if "cursor" in platforms:
            target_dir, removed = uninstall_cursor_rules()
            print(f"Cursor: removed {len(removed)} rules from {target_dir}")

        if "claude" in platforms:
            if uninstall_claude_skill():
                print("Claude Code: removed skill from ~/.claude/skills/sonar-guard/")
            else:
                print("Claude Code: skill not installed")

        if "codex" in platforms:
            if uninstall_codex_agents(repo):
                print(f"Codex: removed AGENTS block from {repo / 'AGENTS.md'}")
            else:
                print("Codex: no sonar-guard block in AGENTS.md")

        if platforms & {"cursor", "claude", "codex"}:
            hook = uninstall_pre_commit_hook(repo)
            if hook.get("removed"):
                print("pre-commit hook removed")

        if args.purge_config:
            config = repo / ".sonarguard.json"
            if config.is_file():
                config.unlink()
                print(f"Deleted {config}")

        print("\nUninstall complete. Start a new Agent chat to reload rules.")
    except OSError as err:
        print(f"Uninstall failed: {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
