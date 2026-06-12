#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonar-guard: SonarQube API 工具(仅用标准库,钩子环境零依赖)。

子命令:
  status                       探测服务器连通性、认证、项目状态(ok/not_found/no_permission/...)
  issues --all                 查询项目全部未解决 issue(B1 全项目扫描)
  issues --files f1 f2 ...     查询指定文件在服务器上的未解决 issue
  rules  [--langs java,py]     列出项目质量配置中的活跃规则(摘要)
  rule   --key java:S2095      查看单条规则的官方描述

通用参数: --repo <仓库路径>(默认当前目录)
输出: JSON(stdout),便于 AI/脚本消费。
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

TIMEOUT = float(os.environ.get("SONARGUARD_TIMEOUT", "5"))
MAX_ISSUE_PAGES = int(os.environ.get("SONARGUARD_MAX_ISSUE_PAGES", "20"))
ISSUE_PAGE_SIZE = 500

SEV_ORDER = {"BLOCKER": 0, "CRITICAL": 1, "MAJOR": 2, "MINOR": 3, "INFO": 4}


def load_config(repo: str) -> dict:
    """合并配置: 仓库 .sonarguard.json / sonar-project.properties + 用户凭证 + 环境变量。"""
    cfg = {"hostUrl": None, "projectKey": None, "token": None,
           "hook": {"mode": "severity", "blockSeverities": ["BLOCKER", "CRITICAL"], "localChecks": True}}

    repo_cfg = os.path.join(repo, ".sonarguard.json")
    if os.path.isfile(repo_cfg):
        try:
            with open(repo_cfg, encoding="utf-8") as f:
                data = json.load(f)
            cfg["hostUrl"] = data.get("hostUrl") or cfg["hostUrl"]
            cfg["projectKey"] = data.get("projectKey") or cfg["projectKey"]
            hook = data.get("hook") or {}
            cfg["hook"].update({k: v for k, v in hook.items() if v is not None})
        except (json.JSONDecodeError, OSError) as e:
            cfg["configError"] = f".sonarguard.json 解析失败: {e}"

    props = os.path.join(repo, "sonar-project.properties")
    if os.path.isfile(props):
        try:
            with open(props, encoding="utf-8") as f:
                for line in f:
                    m = re.match(r"\s*sonar\.projectKey\s*=\s*(\S+)", line)
                    if m and not cfg["projectKey"]:
                        cfg["projectKey"] = m.group(1)
                    m = re.match(r"\s*sonar\.host\.url\s*=\s*(\S+)", line)
                    if m and not cfg["hostUrl"]:
                        cfg["hostUrl"] = m.group(1)
        except OSError:
            pass

    user_cfg = os.path.expanduser("~/.config/sonarguard/config.json")
    if os.path.isfile(user_cfg):
        try:
            with open(user_cfg, encoding="utf-8") as f:
                data = json.load(f)
            cfg["token"] = data.get("token") or cfg["token"]
            cfg["hostUrl"] = cfg["hostUrl"] or data.get("hostUrl")
        except (json.JSONDecodeError, OSError):
            pass

    cfg["token"] = os.environ.get("SONAR_TOKEN") or cfg["token"]
    cfg["hostUrl"] = os.environ.get("SONAR_HOST_URL") or cfg["hostUrl"]
    if cfg["hostUrl"]:
        cfg["hostUrl"] = cfg["hostUrl"].rstrip("/")
    return cfg


class ApiError(Exception):
    def __init__(self, kind, detail=""):
        super().__init__(detail)
        self.kind = kind
        self.detail = detail


def api_get(cfg: dict, path: str, params: dict | None = None) -> dict:
    if not cfg.get("hostUrl"):
        raise ApiError("unreachable", "未配置 hostUrl(.sonarguard.json 或 SONAR_HOST_URL)")
    url = cfg["hostUrl"] + path
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url)
    if cfg.get("token"):
        cred = base64.b64encode((cfg["token"] + ":").encode()).decode()
        req.add_header("Authorization", "Basic " + cred)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise ApiError("no_auth", "认证失败(401): token 缺失或无效") from e
        if e.code == 403:
            raise ApiError("no_permission", "无权限(403): 当前账号无该项目的浏览权限") from e
        if e.code == 404:
            raise ApiError("not_found", f"未找到(404): {path}") from e
        raise ApiError("http_error", f"HTTP {e.code}: {path}") from e
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise ApiError("unreachable", f"服务器不可达: {e}") from e


def _parse_issue(it: dict) -> dict:
    return {
        "rule": it.get("rule"), "severity": it.get("severity"),
        "type": it.get("type"), "message": it.get("message"),
        "file": (it.get("component") or "").split(":", 1)[-1],
        "line": it.get("line"), "status": it.get("status"),
        "creationDate": it.get("creationDate"),
    }


def _issues_summary(issues: list) -> dict:
    summary = {}
    for it in issues:
        summary[it["severity"]] = summary.get(it["severity"], 0) + 1
    return summary


def cmd_status(cfg: dict) -> dict:
    out = {"hostUrl": cfg.get("hostUrl"), "projectKey": cfg.get("projectKey"),
           "tokenConfigured": bool(cfg.get("token")), "hook": cfg.get("hook")}
    if cfg.get("configError"):
        out["configError"] = cfg["configError"]
    if not cfg.get("hostUrl"):
        out["project_state"] = "unreachable"
        out["hint"] = "未配置 Sonar 服务器地址"
        return out
    if not cfg.get("token"):
        out["project_state"] = "no_auth"
        out["hint"] = "未配置 SONAR_TOKEN(环境变量或 ~/.config/sonarguard/config.json)"
        return out
    if not cfg.get("projectKey"):
        out["project_state"] = "unreachable"
        out["hint"] = "未找到 projectKey(.sonarguard.json 或 sonar-project.properties)"
        return out
    try:
        comp = api_get(cfg, "/api/components/show", {"component": cfg["projectKey"]})
        out["project_state"] = "ok"
        c = comp.get("component", {})
        out["project"] = {"name": c.get("name"), "lastAnalysis": c.get("analysisDate")}
        try:
            qg = api_get(cfg, "/api/qualitygates/project_status", {"projectKey": cfg["projectKey"]})
            out["qualityGate"] = qg.get("projectStatus", {}).get("status")
        except ApiError:
            pass
    except ApiError as e:
        out["project_state"] = e.kind
        out["hint"] = e.detail
        if e.kind == "not_found":
            out["hint"] = "项目从未被 Sonar 扫描过;走离线模式,使用内置通用规则"
        elif e.kind == "no_permission":
            out["hint"] = "无权限;请找 Sonar 管理员添加 Browse 权限;当前走离线模式"
    return out


def cmd_issues(cfg: dict, files: list, repo: str) -> dict:
    """查询指定文件的未解决 issue。文件路径需相对仓库根。"""
    rels = []
    for f in files:
        p = os.path.relpath(os.path.abspath(os.path.join(repo, f)), os.path.abspath(repo))
        rels.append(p.replace(os.sep, "/"))
    components = [f"{cfg['projectKey']}:{p}" for p in rels]
    issues, batch = [], 15
    for i in range(0, len(components), batch):
        params = {"components": ",".join(components[i:i + batch]),
                  "resolved": "false", "ps": ISSUE_PAGE_SIZE}
        data = api_get(cfg, "/api/issues/search", params)
        for it in data.get("issues", []):
            issues.append(_parse_issue(it))
    issues.sort(key=lambda x: (SEV_ORDER.get(x["severity"], 9), x["file"], x["line"] or 0))
    return {"total": len(issues), "bySeverity": _issues_summary(issues), "issues": issues}


def cmd_issues_all(cfg: dict, max_pages: int | None = None) -> dict:
    """查询项目全部未解决 issue(B1 全项目扫描)。"""
    if not cfg.get("projectKey"):
        return {"error": "missing_project_key", "detail": "未配置 projectKey"}
    limit = max_pages if max_pages is not None else MAX_ISSUE_PAGES
    issues, page, server_total = [], 1, 0
    while page <= limit:
        params = {"componentKeys": cfg["projectKey"], "resolved": "false",
                  "ps": ISSUE_PAGE_SIZE, "p": page}
        data = api_get(cfg, "/api/issues/search", params)
        server_total = data.get("total", 0)
        for it in data.get("issues", []):
            issues.append(_parse_issue(it))
        if page * ISSUE_PAGE_SIZE >= server_total:
            break
        page += 1
    issues.sort(key=lambda x: (SEV_ORDER.get(x["severity"], 9), x["file"], x["line"] or 0))
    out = {"scope": "all", "total": len(issues), "serverTotal": server_total,
           "bySeverity": _issues_summary(issues), "issues": issues}
    if server_total > len(issues):
        out["truncated"] = True
        out["hint"] = f"已拉取 {len(issues)}/{server_total} 条;提高 SONARGUARD_MAX_ISSUE_PAGES 可获取更多"
    return out


def cmd_rules(cfg: dict, langs: list) -> dict:
    profiles = api_get(cfg, "/api/qualityprofiles/search",
                       {"project": cfg["projectKey"]}).get("profiles", [])
    if langs:
        profiles = [p for p in profiles if p.get("language") in langs]
    result = {}
    for p in profiles:
        rules, page = [], 1
        while True:
            data = api_get(cfg, "/api/rules/search",
                           {"activation": "true", "qprofile": p["key"],
                            "ps": 500, "p": page, "f": "name,severity,lang"})
            for r in data.get("rules", []):
                rules.append({"key": r.get("key"), "name": r.get("name"),
                              "severity": r.get("severity")})
            if page * 500 >= data.get("total", 0) or page >= 6:
                break
            page += 1
        rules.sort(key=lambda x: SEV_ORDER.get(x["severity"], 9))
        result[p["language"]] = {"profile": p.get("name"), "activeRules": len(rules),
                                 "rules": rules}
    return result


def cmd_rule(cfg: dict, key: str) -> dict:
    data = api_get(cfg, "/api/rules/show", {"key": key})
    r = data.get("rule", {})
    desc = re.sub(r"<[^>]+>", "", r.get("htmlDesc") or "")
    return {"key": r.get("key"), "name": r.get("name"), "severity": r.get("severity"),
            "type": r.get("type"), "lang": r.get("lang"), "description": desc[:4000]}


def main():
    ap = argparse.ArgumentParser(description="sonar-guard API 工具")
    ap.add_argument("command", choices=["status", "issues", "rules", "rule"])
    ap.add_argument("--repo", default=".", help="仓库路径")
    ap.add_argument("--files", nargs="*", default=[], help="issues: 相对仓库根的文件路径")
    ap.add_argument("--all", action="store_true", help="issues: 拉取项目全部未解决 issue")
    ap.add_argument("--langs", default="", help="rules: 逗号分隔语言, 如 java,py,js,ts,go")
    ap.add_argument("--key", default="", help="rule: 规则 key, 如 java:S2095")
    args = ap.parse_args()

    cfg = load_config(args.repo)
    exit_code = 0
    try:
        if args.command == "status":
            out = cmd_status(cfg)
        elif args.command == "issues":
            if args.all and args.files:
                out = {"error": "mutually_exclusive", "detail": "--all 与 --files 不能同时使用"}
                exit_code = 1
            elif args.all:
                out = cmd_issues_all(cfg)
                if out.get("error"):
                    exit_code = 1
            elif args.files:
                out = cmd_issues(cfg, args.files, args.repo)
            else:
                out = {"error": "missing_scope", "detail": "issues 需要 --all 或 --files"}
                exit_code = 1
        elif args.command == "rules":
            langs = [x.strip() for x in args.langs.split(",") if x.strip()]
            out = cmd_rules(cfg, langs)
        else:
            out = cmd_rule(cfg, args.key)
    except ApiError as e:
        out = {"error": e.kind, "detail": e.detail}
        exit_code = 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
