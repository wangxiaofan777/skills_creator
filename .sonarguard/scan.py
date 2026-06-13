#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonar-guard 扫描入口: 友好 scope 别名 + 多格式报告。

用法:
  python sonar-guard/scripts/scan.py --repo . --scope full
  python sonar-guard/scripts/scan.py --repo . --scope staged --format html
  python sonar-guard/scripts/scan.py --repo . --scope files --files src/Foo.java --format md

--format md|html|json (默认 md):
  md   渲染 Markdown,打到 stdout 并落盘到 .sonarguard/reports/<scope>-<时间戳>.md
  html 渲染 HTML,落盘并自动在浏览器打开(headless 时仅打印 file:// 路径)
  json 透传底层 sonar_api 的原始 JSON(供外部脚本/自动化消费)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import webbrowser
from datetime import datetime

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import sonar_api  # noqa: E402
import render  # noqa: E402


def _print_json(obj: dict) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _reports_dir(repo: str) -> str:
    d = os.path.join(repo, ".sonarguard", "reports")
    os.makedirs(d, exist_ok=True)
    return d


def _write_report(repo: str, scope: str, ext: str, content: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    path = os.path.join(_reports_dir(repo), f"{scope}-{stamp}.{ext}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.abspath(path)


def _emit(result: dict, *, repo: str, scope: str, fmt: str,
          mode: str | None, top: int) -> int:
    """按 format 渲染/落盘/输出。返回退出码。"""
    if fmt == "json":
        _print_json(result)
        return 0

    if fmt == "md":
        md = render.to_markdown(result, scope=scope, mode=mode, top=top)
        path = _write_report(repo, scope, "md", md)
        print(md)
        print(f"\n[报告已保存] {path}")
        return 0

    # html
    html = render.to_html(result, scope=scope, mode=mode, top=top)
    path = _write_report(repo, scope, "html", html)
    url = "file://" + path.replace(os.sep, "/")
    opened = False
    try:
        opened = webbrowser.open(url)
    except Exception:  # noqa: BLE001 — headless/无浏览器不应影响退出码
        opened = False
    print(f"[HTML 报告已保存] {path}")
    if not opened:
        print(f"[未能自动打开浏览器,请手动访问] {url}")
    return 0


def _scope_staged(cfg: dict, repo: str) -> tuple[dict, str | None]:
    """暂存区检查,复用 check_staged 的共用逻辑。返回 (result, mode_label)。"""
    import check_staged
    files, findings, state = check_staged.collect_findings(repo, cfg)
    summary: dict = {}
    for it in findings:
        summary[it["severity"]] = summary.get(it["severity"], 0) + 1
    result = {
        "scope": "staged",
        "stagedFiles": len(files),
        "total": len(findings),
        "bySeverity": summary,
        "issues": findings,
    }
    mode = "服务器" if state == "ok" else f"离线: {state}"
    return result, mode


def main() -> int:
    ap = argparse.ArgumentParser(description="sonar-guard scan")
    ap.add_argument("--repo", default=".", help="仓库路径")
    ap.add_argument("--scope", choices=["full", "staged", "files"], required=True)
    ap.add_argument("--files", nargs="*", default=[], help="scope=files 时的文件路径")
    ap.add_argument("--format", dest="fmt", choices=["md", "html", "json"],
                    default="md", help="报告格式(默认 md)")
    ap.add_argument("--top", type=int, default=render.DEFAULT_TOP,
                    help="MAJOR 详情上限(默认 20)")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    cfg = sonar_api.load_config(repo)

    if args.scope == "full":
        try:
            result = sonar_api.cmd_issues_all(cfg)
        except sonar_api.ApiError as e:
            _print_json({"error": e.kind, "detail": e.detail})
            return 1
        if result.get("error"):
            _print_json(result)
            return 1
        return _emit(result, repo=repo, scope="full", fmt=args.fmt,
                     mode="服务器", top=args.top)

    if args.scope == "files":
        if not args.files:
            _print_json({"error": "missing_files", "detail": "scope=files 需要 --files"})
            return 1
        try:
            result = sonar_api.cmd_issues(cfg, args.files, repo)
        except sonar_api.ApiError as e:
            _print_json({"error": e.kind, "detail": e.detail})
            return 1
        return _emit(result, repo=repo, scope="files", fmt=args.fmt,
                     mode="服务器", top=args.top)

    # staged
    result, mode = _scope_staged(cfg, repo)
    return _emit(result, repo=repo, scope="staged", fmt=args.fmt,
                 mode=mode, top=args.top)


if __name__ == "__main__":
    raise SystemExit(main())
