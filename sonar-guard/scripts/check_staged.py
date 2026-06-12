#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonar-guard pre-commit 检查:对暂存区文件做 Sonar 合规检查。

设计原则:
  - 快(服务器 3 秒超时即降级为本地检查,绝不能挡住所有人提交)
  - 零依赖(仅标准库)
  - 行为由 .sonarguard.json 的 hook.mode 决定: block / warn / severity

退出码: 0=放行, 1=阻止提交
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("SONARGUARD_TIMEOUT", "3")
import sonar_api  # noqa: E402

LANG_EXT = {
    ".java": "java", ".py": "py", ".go": "go",
    ".js": "js", ".jsx": "js", ".ts": "ts", ".tsx": "ts", ".vue": "js",
}

LOCAL_RULES = [
    ("local:empty-catch-java", {"java"},
     re.compile(r"catch\s*\([^)]*\)\s*\{\s*\}"),
     "空 catch 块吞掉异常 (类似 java:S2486)", "CRITICAL"),
    ("local:string-eq-java", {"java"},
     re.compile(r'(?:"\s*[=!]=\s*\w|\w\s*[=!]=\s*")'),
     "字符串用 ==/!= 比较, 应使用 equals (java:S4973)", "BLOCKER"),
    ("local:printstacktrace", {"java"},
     re.compile(r"\.printStackTrace\s*\("),
     "printStackTrace 应替换为日志框架 (java:S4507/S106)", "MAJOR"),
    ("local:sysout", {"java"},
     re.compile(r"System\s*\.\s*(out|err)\s*\.\s*print"),
     "System.out/err 调试输出应使用日志框架 (java:S106)", "MAJOR"),
    ("local:bare-except", {"py"},
     re.compile(r"^\s*except\s*:\s*(#.*)?$", re.M),
     "裸 except: 会吞掉所有异常含 KeyboardInterrupt (python:S5754)", "CRITICAL"),
    ("local:py-print-debug", {"py"},
     re.compile(r"^\s*print\s*\(", re.M),
     "print 调试残留, 建议用 logging (启发式, 脚本类项目可在配置中关闭 localChecks)", "MINOR"),
    ("local:console-log", {"js", "ts"},
     re.compile(r"console\s*\.\s*(log|debug)\s*\("),
     "console.log/debug 调试残留 (javascript:S2228 类似)", "MINOR"),
    ("local:js-debugger", {"js", "ts"},
     re.compile(r"^\s*debugger\b", re.M),
     "debugger 语句禁止提交 (javascript:S1525)", "BLOCKER"),
    ("local:js-loose-eq", {"js", "ts"},
     re.compile(r"[^=!<>]==[^=]|[^=!]!=[^=]"),
     "应使用 ===/!== 而非 ==/!= (javascript:S1440)", "MINOR"),
    ("local:hardcoded-secret", {"java", "py", "js", "ts", "go"},
     re.compile(r"(?i)(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*[\"'][^\"']{6,}[\"']"),
     "疑似硬编码密钥/密码 (S2068/S6418), 请改用配置或环境变量", "BLOCKER"),
    ("local:empty-catch-go", {"go"},
     re.compile(r"if\s+err\s*!=\s*nil\s*\{\s*\}"),
     "err != nil 后空块, 错误被忽略 (go:S1116 类似)", "CRITICAL"),
    ("local:todo-fixme", {"java", "py", "js", "ts", "go"},
     re.compile(r"//\s*(TODO|FIXME)|#\s*(TODO|FIXME)"),
     "TODO/FIXME 标记 (java:S1135), 仅提醒", "INFO"),
]

SEV_ORDER = {"BLOCKER": 0, "CRITICAL": 1, "MAJOR": 2, "MINOR": 3, "INFO": 4}
C = {"red": "\033[31m", "yel": "\033[33m", "grn": "\033[32m", "dim": "\033[2m", "off": "\033[0m"}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True, check=False)


def staged_files(repo):
    r = git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACM")
    return [f for f in r.stdout.splitlines() if os.path.splitext(f)[1] in LANG_EXT]


def staged_content(repo, path):
    r = git(repo, "show", f":{path}")
    return r.stdout if r.returncode == 0 else ""


def run_local_checks(repo, files):
    findings = []
    for path in files:
        lang = LANG_EXT[os.path.splitext(path)[1]]
        content = staged_content(repo, path)
        if not content:
            continue
        lines = content.splitlines()
        for rule_id, langs, pattern, msg, sev in LOCAL_RULES:
            if lang not in langs:
                continue
            for i, line in enumerate(lines, 1):
                s = line.strip()
                if rule_id != "local:todo-fixme" and (
                        s.startswith("//") or s.startswith("#") or s.startswith("*")):
                    continue
                if pattern.search(line):
                    findings.append({"file": path, "line": i, "rule": rule_id,
                                     "severity": sev, "message": msg, "source": "local"})
                    break
    return findings


def fetch_server_issues(repo, cfg, files):
    try:
        status = sonar_api.cmd_status(cfg)
        state = status.get("project_state")
        if state != "ok":
            return None, state
        data = sonar_api.cmd_issues(cfg, files, repo)
        issues = [{**it, "source": "server"} for it in data.get("issues", [])]
        return issues, "ok"
    except Exception:  # noqa: BLE001
        return None, "unreachable"


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = args.repo

    cfg = sonar_api.load_config(repo)
    hook = cfg.get("hook", {})
    mode = hook.get("mode", "severity")
    block_sevs = set(hook.get("blockSeverities", ["BLOCKER", "CRITICAL"]))

    files = staged_files(repo)
    if not files:
        return 0

    findings = []
    server_issues, state = fetch_server_issues(repo, cfg, files)
    if server_issues:
        findings += server_issues
    if hook.get("localChecks", True):
        findings += run_local_checks(repo, files)

    if not findings:
        print(f"{C['grn']}✔ sonar-guard: {len(files)} 个暂存文件未发现问题"
              f"{'' if state == 'ok' else ' (离线模式: ' + str(state) + ')'}{C['off']}")
        return 0

    findings.sort(key=lambda x: (SEV_ORDER.get(x["severity"], 9), x["file"], x.get("line") or 0))
    if mode == "block":
        blocking = findings
    elif mode == "warn":
        blocking = []
    else:
        blocking = [f for f in findings if f["severity"] in block_sevs]

    print(f"\n=== sonar-guard 提交检查 (模式: {mode}"
          f"{'' if state == 'ok' else ', 离线: ' + str(state)}) ===")
    for f in findings:
        is_block = f in blocking
        color = C["red"] if is_block else C["yel"]
        tag = "拦截" if is_block else "警告"
        src = "Sonar服务器存量" if f.get("source") == "server" else "本地检查"
        print(f"{color}[{tag}] {f['severity']:<8}{C['off']} {f['file']}:{f.get('line') or '?'} "
              f"{f['message']} {C['dim']}({f['rule']}, {src}){C['off']}")

    print(f"\n共 {len(findings)} 个问题, 其中 {len(blocking)} 个达到拦截级别。")
    if blocking:
        print("提交已被阻止。修复后重新提交; 紧急情况可用 git commit --no-verify 跳过(不推荐)。")
        return 1
    print("以上为警告, 本次提交放行。建议尽快修复。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
