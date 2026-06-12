#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-click install sonar-guard for Claude Code / Cursor / Codex.

Usage (from skills_creator repo root):
  python sonar-guard/scripts/install.py --platform all --repo <path-to-git-repo>
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from lib.install_lib import (  # noqa: E402
    PLATFORMS,
    ensure_sonarguard_json,
    install_claude_skill,
    install_codex_agents,
    install_cursor_rules,
    install_pre_commit_hook,
    install_repo_cli,
    print_post_install_hints,
    resolve_platforms,
    save_package_root,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install sonar-guard")
    parser.add_argument("--platform", "-p", choices=PLATFORMS, default="all",
                        help="cursor | claude | codex | all (all = cursor + claude)")
    parser.add_argument("--repo", "-r", default=".", help="Target git repo (default: cwd)")
    parser.add_argument("--host-url", help="Sonar hostUrl (when no sonar-project.properties)")
    parser.add_argument("--project-key", help="Sonar projectKey")
    parser.add_argument("--no-hook", action="store_true", help="Skip pre-commit hook installation")
    parser.add_argument("--force-config", action="store_true", help="Overwrite existing .sonarguard.json")
    parser.add_argument("--no-interactive", action="store_true", help="Skip interactive project prompts")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    platforms = resolve_platforms(args.platform)
    if args.platform == "codex":
        platforms = {"codex"}

    try:
        if "cursor" in platforms:
            target_dir, installed = install_cursor_rules()
            print(f"Cursor: installed {len(installed)} rules → {target_dir}")

        if "claude" in platforms:
            skill_dir = install_claude_skill()
            print(f"Claude Code: installed skill → {skill_dir}")

        if "codex" in platforms:
            agents_path = install_codex_agents(repo)
            print(f"Codex: merged AGENTS block → {agents_path}")

        config_path, created = ensure_sonarguard_json(
            repo,
            force=args.force_config,
            host_url=args.host_url,
            project_key=args.project_key,
            interactive=not args.no_interactive,
        )
        print(f"{'Created' if created else 'Kept existing'} {config_path}")

        cli_dir = install_repo_cli(repo)
        print(f"Repo CLI: {cli_dir}")

        hook_installed = False
        if not args.no_hook and platforms & {"cursor", "claude", "codex"}:
            _, pre_commit_path, action = install_pre_commit_hook(repo)
            print(f"pre-commit hook {action}: {pre_commit_path}")
            hook_installed = True

        print_post_install_hints(repo, config_path=config_path, hook_installed=hook_installed)
        save_package_root()
    except (FileNotFoundError, subprocess.CalledProcessError, OSError) as err:
        print(f"Install failed: {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
