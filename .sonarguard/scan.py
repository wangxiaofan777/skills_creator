#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonar-guard 扫描入口: 友好 scope 别名。

用法:
  python sonar-guard/scripts/scan.py --repo . --scope full
  python sonar-guard/scripts/scan.py --repo . --scope staged
  python sonar-guard/scripts/scan.py --repo . --scope files --files src/Foo.java
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import sonar_api  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="sonar-guard scan")
    ap.add_argument("--repo", default=".", help="仓库路径")
    ap.add_argument("--scope", choices=["full", "staged", "files"], required=True)
    ap.add_argument("--files", nargs="*", default=[], help="scope=files 时的文件路径")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    if args.scope == "full":
        cfg = sonar_api.load_config(repo)
        try:
            out = sonar_api.cmd_issues_all(cfg)
        except sonar_api.ApiError as e:
            out = {"error": e.kind, "detail": e.detail}
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 1
        if out.get("error"):
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 1
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    if args.scope == "staged":
        staged = os.path.join(_SCRIPT_DIR, "check_staged.py")
        return subprocess.call([sys.executable, staged, "--repo", repo])

    if not args.files:
        print(json.dumps({"error": "missing_files", "detail": "scope=files 需要 --files"},
                         ensure_ascii=False, indent=2))
        return 1
    cfg = sonar_api.load_config(repo)
    try:
        out = sonar_api.cmd_issues(cfg, args.files, repo)
    except sonar_api.ApiError as e:
        out = {"error": e.kind, "detail": e.detail}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
