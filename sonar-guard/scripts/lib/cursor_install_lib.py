#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared helpers for sonar-guard Cursor install / uninstall (stdlib only)."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HOOK_MARK_START = "# >>> sonar-guard >>>"
HOOK_MARK_END = "# <<< sonar-guard <<<"

RULE_NAMES = [
    "00-sonar-guard-base.mdc",
    "sonar-fix-risk.mdc",
    "sonar-java.mdc",
    "sonar-python.mdc",
    "sonar-js-ts.mdc",
    "sonar-go.mdc",
]


def package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def rules_source_dir() -> Path:
    return package_root() / "cursor" / "rules"


def scripts_source_dir() -> Path:
    return package_root() / "claude-code" / "sonar-guard" / "scripts"


def cursor_rules_dir() -> Path:
    return Path.home() / ".cursor" / "rules"


def install_manifest_path() -> Path:
    return Path.home() / ".config" / "sonarguard" / "cursor-install.json"


def read_install_manifest() -> dict | None:
    path = install_manifest_path()
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def write_install_manifest(data: dict) -> None:
    path = install_manifest_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def remove_install_manifest() -> None:
    path = install_manifest_path()
    if path.is_file():
        path.unlink()


def install_cursor_rules() -> tuple[Path, list[str]]:
    source_dir = rules_source_dir()
    target_dir = cursor_rules_dir()
    target_dir.mkdir(parents=True, exist_ok=True)

    installed: list[str] = []
    for name in RULE_NAMES:
        source = source_dir / name
        if not source.is_file():
            raise FileNotFoundError(f"Rule source not found: {source}")
        shutil.copy2(source, target_dir / name)
        installed.append(name)

    write_install_manifest({
        "version": 1,
        "rules": installed,
        "rulesDir": str(target_dir),
        "installedAt": datetime.now(timezone.utc).isoformat(),
    })
    return target_dir, installed


def uninstall_cursor_rules() -> tuple[Path, list[str]]:
    manifest = read_install_manifest()
    target_dir = Path(manifest["rulesDir"]) if manifest and manifest.get("rulesDir") else cursor_rules_dir()
    names = manifest.get("rules", RULE_NAMES) if manifest else RULE_NAMES
    removed: list[str] = []

    for name in names:
        target = target_dir / name
        if target.is_file():
            target.unlink()
            removed.append(name)

    remove_install_manifest()
    return target_dir, removed


def parse_sonar_project_properties(repo: Path) -> dict[str, str | None]:
    props_path = repo / "sonar-project.properties"
    result: dict[str, str | None] = {"hostUrl": None, "projectKey": None}
    if not props_path.is_file():
        return result

    for line in props_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*sonar\.projectKey\s*=\s*(\S+)", line)
        if m:
            result["projectKey"] = m.group(1)
        m = re.match(r"^\s*sonar\.host\.url\s*=\s*(\S+)", line)
        if m:
            result["hostUrl"] = m.group(1)
    return result


def ensure_sonarguard_json(repo: Path, *, force: bool = False) -> tuple[Path, bool]:
    config_path = repo / ".sonarguard.json"
    if config_path.is_file() and not force:
        return config_path, False

    from_props = parse_sonar_project_properties(repo)
    config: dict[str, str] = {}
    if from_props["hostUrl"]:
        config["hostUrl"] = from_props["hostUrl"].rstrip("/")  # type: ignore[union-attr]
    if from_props["projectKey"]:
        config["projectKey"] = from_props["projectKey"]  # type: ignore[assignment]

    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return config_path, True


def git_dir(repo: Path) -> Path:
    raw = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--git-dir"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return (repo / raw).resolve()


def hook_snippet() -> str:
    return f"""{HOOK_MARK_START}
REPO_ROOT="$(git rev-parse --show-toplevel)"
GIT_DIR="$(git rev-parse --git-dir)"
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
"$PY" "$GIT_DIR/hooks/sonarguard/check_staged.py" --repo "$REPO_ROOT" || exit 1
{HOOK_MARK_END}"""


def install_pre_commit_hook(repo: Path) -> tuple[Path, Path, str]:
    repo_path = repo.resolve()
    subprocess.run(
        ["git", "-C", str(repo_path), "rev-parse", "--git-dir"],
        capture_output=True,
        check=True,
    )

    git_dir_path = git_dir(repo_path)
    hook_dir = git_dir_path / "hooks"
    guard_dir = hook_dir / "sonarguard"
    guard_dir.mkdir(parents=True, exist_ok=True)

    for name in ("check_staged.py", "sonar_api.py"):
        shutil.copy2(scripts_source_dir() / name, guard_dir / name)

    pre_commit_path = hook_dir / "pre-commit"
    snippet = hook_snippet()
    action = "created"

    if pre_commit_path.is_file():
        existing = pre_commit_path.read_text(encoding="utf-8")
        if "sonar-guard" in existing:
            pattern = re.compile(
                re.escape(HOOK_MARK_START) + r"[\s\S]*?" + re.escape(HOOK_MARK_END)
            )
            updated = pattern.sub(snippet, existing)
            if updated != existing:
                pre_commit_path.write_text(updated, encoding="utf-8")
                action = "updated"
            else:
                action = "refreshed-scripts"
        else:
            pre_commit_path.write_text(existing.rstrip() + "\n\n" + snippet + "\n", encoding="utf-8")
            action = "appended"
    else:
        pre_commit_path.write_text("#!/usr/bin/env bash\n" + snippet + "\n", encoding="utf-8")
        action = "created"

    (guard_dir / ".installed-by-sonar-guard").write_text(
        datetime.now(timezone.utc).isoformat() + "\n",
        encoding="utf-8",
    )
    return guard_dir, pre_commit_path, action


def uninstall_pre_commit_hook(repo: Path) -> dict:
    repo_path = repo.resolve()
    try:
        git_dir_path = git_dir(repo_path)
    except (subprocess.CalledProcessError, OSError):
        return {"removed": False, "reason": "not-a-git-repo"}

    hook_dir = git_dir_path / "hooks"
    guard_dir = hook_dir / "sonarguard"
    pre_commit_path = hook_dir / "pre-commit"

    if guard_dir.exists():
        shutil.rmtree(guard_dir)

    if pre_commit_path.is_file():
        existing = pre_commit_path.read_text(encoding="utf-8")
        pattern = re.compile(
            r"\n?" + re.escape(HOOK_MARK_START) + r"[\s\S]*?" + re.escape(HOOK_MARK_END) + r"\n?"
        )
        stripped = pattern.sub("\n", existing).strip()
        if not stripped or stripped == "#!/usr/bin/env bash":
            pre_commit_path.unlink()
        elif stripped != existing.strip():
            pre_commit_path.write_text(stripped + "\n", encoding="utf-8")

    return {"removed": True, "guardDir": guard_dir, "preCommitPath": pre_commit_path}


def has_sonar_token() -> bool:
    if os.environ.get("SONAR_TOKEN"):
        return True
    user_cfg = Path.home() / ".config" / "sonarguard" / "config.json"
    if not user_cfg.is_file():
        return False
    try:
        data = json.loads(user_cfg.read_text(encoding="utf-8"))
        return bool(data.get("token"))
    except (json.JSONDecodeError, OSError):
        return False


def print_post_install_hints(repo: Path, *, config_path: Path, hook_installed: bool) -> None:
    from_props = parse_sonar_project_properties(repo)
    needs_project = not (from_props["hostUrl"] and from_props["projectKey"])
    if needs_project and config_path.is_file():
        try:
            cfg = json.loads(config_path.read_text(encoding="utf-8"))
            if cfg.get("hostUrl") and cfg.get("projectKey"):
                needs_project = False
        except json.JSONDecodeError:
            pass

    print("\n--- 装完了，你可能还需要 ---")
    if not has_sonar_token():
        print("① 个人认证（连 Sonar 服务器时需要，本机一次）:")
        print("   设置环境变量 SONAR_TOKEN=squ_xxx")
        print('   或写入 ~/.config/sonarguard/config.json → {"token":"squ_xxx"}')
        print("   不配也能用：对话审查 + 本地 pre-commit 走离线模式。")
    else:
        print("① 个人认证: 已检测到 SONAR_TOKEN 或 ~/.config/sonarguard/config.json")

    if needs_project:
        print("② 项目信息（连 Sonar 且仓库无 sonar-project.properties 时）:")
        print(f"   编辑 {config_path}，补上 hostUrl 与 projectKey")
    else:
        print("② 项目信息: 已从 .sonarguard.json 或 sonar-project.properties 就绪")

    print("③ 新开一条 Cursor Agent 对话，改代码后应自动出 Sonar 合规报告。")
    if hook_installed:
        check_script = git_dir(repo) / "hooks" / "sonarguard" / "check_staged.py"
        print("④ pre-commit 已安装；模拟检查:")
        print(f'   python "{check_script}" --repo "{repo.resolve()}"')
