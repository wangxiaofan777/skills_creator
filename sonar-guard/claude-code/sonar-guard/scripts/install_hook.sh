#!/usr/bin/env bash
# sonar-guard: 安装 pre-commit 钩子
# 用法: bash install_hook.sh /path/to/repo
set -euo pipefail

REPO="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANONICAL="$(cd "$SCRIPT_DIR/../../../scripts" && pwd)"

GIT_DIR="$(git -C "$REPO" rev-parse --git-dir 2>/dev/null)" || {
  echo "错误: $REPO 不是一个 git 仓库" >&2; exit 1; }
case "$GIT_DIR" in
  /*) : ;;
  *) GIT_DIR="$REPO/$GIT_DIR" ;;
esac

HOOK_DIR="$GIT_DIR/hooks"
GUARD_DIR="$HOOK_DIR/sonarguard"
mkdir -p "$GUARD_DIR"

cp "$CANONICAL/check_staged.py" "$CANONICAL/sonar_api.py" "$GUARD_DIR/"

PRE_COMMIT="$HOOK_DIR/pre-commit"
MARK="# >>> sonar-guard >>>"
SNIPPET="$MARK
REPO_ROOT=\"\$(git rev-parse --show-toplevel)\"
GIT_DIR=\"\$(git rev-parse --git-dir)\"
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
\"\$PY\" \"\$GIT_DIR/hooks/sonarguard/check_staged.py\" --repo \"\$REPO_ROOT\" || exit 1
# <<< sonar-guard <<<"

if [ -f "$PRE_COMMIT" ]; then
  if grep -q "sonar-guard" "$PRE_COMMIT"; then
    echo "pre-commit 中已包含 sonar-guard, 仅更新了脚本文件。"
  else
    printf '\n%s\n' "$SNIPPET" >> "$PRE_COMMIT"
    echo "已追加 sonar-guard 到现有 pre-commit 钩子。"
  fi
else
  printf '#!/usr/bin/env bash\n%s\n' "$SNIPPET" > "$PRE_COMMIT"
  echo "已创建 pre-commit 钩子。"
fi
chmod +x "$PRE_COMMIT"

if [ ! -f "$REPO/.sonarguard.json" ]; then
  echo "提示: 仓库根目录还没有 .sonarguard.json。运行 install.py 可自动创建。"
fi
if [ -z "${SONAR_TOKEN:-}" ] && [ ! -f "$HOME/.config/sonarguard/config.json" ]; then
  echo "提示: 未检测到 SONAR_TOKEN, 钩子将以离线模式运行。"
fi
echo "安装完成。全项目扫描:"
echo "  python \"$CANONICAL/scan.py\" --repo \"$REPO\" --scope full"
echo "模拟 pre-commit:"
echo "  python \"$GUARD_DIR/check_staged.py\" --repo \"$REPO\""
