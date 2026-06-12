#!/usr/bin/env bash
# sonar-guard: 安装 pre-commit 钩子
# 用法: bash install_hook.sh /path/to/repo
set -euo pipefail

REPO="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

GIT_DIR="$(git -C "$REPO" rev-parse --git-dir 2>/dev/null)" || {
  echo "错误: $REPO 不是一个 git 仓库" >&2; exit 1; }
# git-dir 可能是相对路径
case "$GIT_DIR" in
  /*) : ;;
  *) GIT_DIR="$REPO/$GIT_DIR" ;;
esac

HOOK_DIR="$GIT_DIR/hooks"
GUARD_DIR="$HOOK_DIR/sonarguard"
mkdir -p "$GUARD_DIR"

# 1. 复制脚本(自包含, 之后不依赖技能目录)
cp "$SCRIPT_DIR/check_staged.py" "$SCRIPT_DIR/sonar_api.py" "$GUARD_DIR/"

# 2. 写入/追加 pre-commit
PRE_COMMIT="$HOOK_DIR/pre-commit"
MARK="# >>> sonar-guard >>>"
SNIPPET="$MARK
REPO_ROOT=\"\$(git rev-parse --show-toplevel)\"
python3 \"\$(git rev-parse --git-dir)/hooks/sonarguard/check_staged.py\" --repo \"\$REPO_ROOT\" || exit 1
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

# 3. 提示配置状态
if [ ! -f "$REPO/.sonarguard.json" ]; then
  echo "提示: 仓库根目录还没有 .sonarguard.json, 请先创建(包含 hostUrl/projectKey/hook 配置)。"
fi
if [ -z "${SONAR_TOKEN:-}" ] && [ ! -f "$HOME/.config/sonarguard/config.json" ]; then
  echo "提示: 未检测到个人 SONAR_TOKEN(环境变量或 ~/.config/sonarguard/config.json), 钩子将以离线模式运行。"
fi
echo "安装完成。可用以下命令模拟一次检查:"
echo "  python3 \"$GUARD_DIR/check_staged.py\" --repo \"$REPO\""
