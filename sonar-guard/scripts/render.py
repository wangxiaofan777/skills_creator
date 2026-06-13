#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonar-guard 报告渲染(仅标准库,零依赖)。

把 sonar_api / check_staged 产出的结果 dict 渲染为人类友好的 Markdown / HTML。

结果 dict 约定(渲染层只读这些键):
  {
    "total":      int,
    "serverTotal":int | None,          # 全项目扫描时服务器侧总数(可选)
    "bySeverity": {"BLOCKER": n, ...},
    "issues":     [ {severity, file, line, rule, message, source?, type?}, ... ],
    "truncated":  bool | None,         # 服务器分页未拉全(可选)
  }

截断规则(确定性,见 design D7):
  - 汇总各严重级数量必全
  - 详情: BLOCKER/CRITICAL 全列; MAJOR 最多 top 条(默认 20); MINOR/INFO 仅计数
"""
from __future__ import annotations

import html as _html

SEV_ORDER = {"BLOCKER": 0, "CRITICAL": 1, "MAJOR": 2, "MINOR": 3, "INFO": 4}
SEV_ALL = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]
DETAIL_FULL = {"BLOCKER", "CRITICAL"}   # 全列
DETAIL_COUNT = {"MINOR", "INFO"}        # 仅计数
DEFAULT_TOP = 20                        # MAJOR 详情上限


def _sorted_issues(issues: list) -> list:
    return sorted(
        issues,
        key=lambda x: (SEV_ORDER.get(x.get("severity"), 9),
                       x.get("file") or "", x.get("line") or 0),
    )


def _summary(result: dict) -> dict:
    by = result.get("bySeverity") or {}
    if by:
        return by
    out: dict = {}
    for it in result.get("issues", []):
        sev = it.get("severity")
        out[sev] = out.get(sev, 0) + 1
    return out


def _select_detail(issues: list, top: int) -> tuple[list, dict]:
    """返回 (要详列的 issue 列表, 被省略计数 {severity: omitted_n})。"""
    detailed: list = []
    omitted: dict = {}
    major_shown = 0
    for it in _sorted_issues(issues):
        sev = it.get("severity")
        if sev in DETAIL_FULL:
            detailed.append(it)
        elif sev == "MAJOR":
            if major_shown < top:
                detailed.append(it)
                major_shown += 1
            else:
                omitted["MAJOR"] = omitted.get("MAJOR", 0) + 1
        else:  # MINOR / INFO / 未知
            key = sev if sev in DETAIL_COUNT else (sev or "UNKNOWN")
            omitted[key] = omitted.get(key, 0) + 1
    return detailed, omitted


def _title(scope: str, mode: str | None) -> str:
    scope_label = {"all": "全项目", "full": "全项目", "files": "增量文件",
                   "staged": "暂存区(提交前)"}.get(scope, scope)
    suffix = f"(模式: {mode})" if mode else ""
    return f"Sonar 合规检查报告 — {scope_label} {suffix}".rstrip()


# --------------------------------------------------------------------------- #
# Markdown
# --------------------------------------------------------------------------- #
def to_markdown(result: dict, *, scope: str = "full",
                mode: str | None = None, top: int = DEFAULT_TOP) -> str:
    issues = result.get("issues", [])
    summary = _summary(result)
    total = result.get("total", len(issues))
    lines: list[str] = []

    lines.append(f"## {_title(scope, mode)}")
    lines.append("")

    # 汇总表(必全)
    lines.append("### 严重级汇总")
    lines.append("")
    lines.append("| 严重级 | 数量 |")
    lines.append("|---|---|")
    for sev in SEV_ALL:
        lines.append(f"| {sev} | {summary.get(sev, 0)} |")
    lines.append(f"| **合计** | **{total}** |")
    server_total = result.get("serverTotal")
    if result.get("truncated") and server_total:
        lines.append("")
        lines.append(f"> ⚠ 服务器侧共 {server_total} 条,本次拉取 {total} 条"
                     f"(提高 `SONARGUARD_MAX_ISSUE_PAGES` 可获取更多)。")
    lines.append("")

    if not issues:
        lines.append("✔ 未发现问题。")
        lines.append("")
        return "\n".join(lines)

    # 详情(截断)
    detailed, omitted = _select_detail(issues, top)
    lines.append("### 问题明细")
    lines.append("")
    lines.append("| 严重级 | 文件:行 | 规则 | 问题 | 来源 |")
    lines.append("|---|---|---|---|---|")
    for it in detailed:
        loc = f"{it.get('file') or '?'}:{it.get('line') or '?'}"
        src = _source_label(it.get("source"))
        msg = (it.get("message") or "").replace("|", "\\|")
        lines.append(f"| {it.get('severity')} | {loc} | "
                     f"{it.get('rule') or ''} | {msg} | {src} |")
    lines.append("")

    if omitted:
        parts = [f"{k} {v} 条" for k, v in omitted.items()]
        lines.append(f"> 另有 {', '.join(parts)} 未在上表详列"
                     f"(MAJOR 详情上限 {top};MINOR/INFO 仅计数)。")
        lines.append("")

    return "\n".join(lines)


def _source_label(source: str | None) -> str:
    return {"server": "服务器存量", "local": "本地检查"}.get(source or "", "服务器")


# --------------------------------------------------------------------------- #
# HTML(内联模板,无第三方库)
# --------------------------------------------------------------------------- #
_HTML_CSS = """
body{font:14px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
  margin:2rem auto;max-width:960px;color:#1f2328;padding:0 1rem}
h1{font-size:1.4rem;border-bottom:1px solid #d0d7de;padding-bottom:.3rem}
h2{font-size:1.1rem;margin-top:1.6rem}
table{border-collapse:collapse;width:100%;margin:.6rem 0}
th,td{border:1px solid #d0d7de;padding:.4rem .6rem;text-align:left;vertical-align:top}
th{background:#f6f8fa}
.sev{font-weight:600;white-space:nowrap}
.BLOCKER{color:#cf222e}.CRITICAL{color:#bc4c00}.MAJOR{color:#9a6700}
.MINOR{color:#0969da}.INFO{color:#57606a}
.note{color:#57606a;background:#f6f8fa;border-left:3px solid #d0d7de;
  padding:.5rem .8rem;margin:.6rem 0}
.ok{color:#1a7f37;font-weight:600}
"""


def _esc(s) -> str:
    return _html.escape(str(s if s is not None else ""))


def to_html(result: dict, *, scope: str = "full",
            mode: str | None = None, top: int = DEFAULT_TOP) -> str:
    issues = result.get("issues", [])
    summary = _summary(result)
    total = result.get("total", len(issues))
    title = _title(scope, mode)

    rows = "".join(
        f"<tr><td class='sev {sev}'>{sev}</td><td>{summary.get(sev, 0)}</td></tr>"
        for sev in SEV_ALL
    )
    summary_tbl = (
        "<table><thead><tr><th>严重级</th><th>数量</th></tr></thead><tbody>"
        f"{rows}"
        f"<tr><td><strong>合计</strong></td><td><strong>{total}</strong></td></tr>"
        "</tbody></table>"
    )

    trunc_note = ""
    server_total = result.get("serverTotal")
    if result.get("truncated") and server_total:
        trunc_note = (f"<p class='note'>⚠ 服务器侧共 {server_total} 条,"
                      f"本次拉取 {total} 条。</p>")

    if not issues:
        body = f"{summary_tbl}{trunc_note}<p class='ok'>✔ 未发现问题。</p>"
    else:
        detailed, omitted = _select_detail(issues, top)
        drows = "".join(
            "<tr>"
            f"<td class='sev {_esc(it.get('severity'))}'>{_esc(it.get('severity'))}</td>"
            f"<td>{_esc(it.get('file') or '?')}:{_esc(it.get('line') or '?')}</td>"
            f"<td>{_esc(it.get('rule'))}</td>"
            f"<td>{_esc(it.get('message'))}</td>"
            f"<td>{_esc(_source_label(it.get('source')))}</td>"
            "</tr>"
            for it in detailed
        )
        detail_tbl = (
            "<h2>问题明细</h2><table><thead><tr>"
            "<th>严重级</th><th>文件:行</th><th>规则</th><th>问题</th><th>来源</th>"
            "</tr></thead><tbody>"
            f"{drows}</tbody></table>"
        )
        omit_note = ""
        if omitted:
            parts = ", ".join(f"{k} {v} 条" for k, v in omitted.items())
            omit_note = (f"<p class='note'>另有 {parts} 未详列"
                         f"(MAJOR 详情上限 {top};MINOR/INFO 仅计数)。</p>")
        body = f"{summary_tbl}{trunc_note}{detail_tbl}{omit_note}"

    return (
        "<!DOCTYPE html><html lang='zh'><head><meta charset='utf-8'>"
        f"<title>{_esc(title)}</title><style>{_HTML_CSS}</style></head>"
        f"<body><h1>{_esc(title)}</h1>{body}</body></html>"
    )
