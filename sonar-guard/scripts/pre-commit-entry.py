#!/usr/bin/env python
"""sonar-guard pre-commit hook entry (cross-platform, Windows-safe)."""
from __future__ import annotations

import os
import subprocess
import sys


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def _resolve_check_script(repo: str, git_dir: str) -> str | None:
    for candidate in (
        os.path.join(git_dir, "hooks", "sonarguard", "check_staged.py"),
        os.path.join(repo, ".sonarguard", "check_staged.py"),
    ):
        if os.path.isfile(candidate):
            return os.path.normpath(candidate)
    return None


def main() -> int:
    try:
        repo = _git("rev-parse", "--show-toplevel")
        git_dir = _git("rev-parse", "--git-dir")
        if not os.path.isabs(git_dir):
            git_dir = os.path.join(repo, git_dir)
    except subprocess.CalledProcessError:
        return 1

    script = _resolve_check_script(repo, git_dir)
    if not script:
        return 0

    return subprocess.call([sys.executable, script, "--repo", repo])


if __name__ == "__main__":
    raise SystemExit(main())
