## Why

sonar-guard 的 Cursor 接入步骤分散（手抄 6 个 `.mdc`、手建 `.sonarguard.json`、单独装 pre-commit），README 又以满配 JSON 为主，用户难以判断「最少要配什么」。需要像 link-works 一样提供跨平台一键安装/移除，并把装完后仅需配置的个人认证与项目信息说清楚；安装脚本应与 pre-commit 一样统一为 Python（标准库），避免额外依赖 Node.js。

## What Changes

- 新增 Python 一键安装脚本 `sonar-guard/scripts/install_cursor.py`：安装 Cursor rules、生成 `.sonarguard.json`、安装 pre-commit 钩子
- 新增 Python 一键移除脚本 `sonar-guard/scripts/uninstall_cursor.py`：移除 rules、pre-commit 片段与钩子目录（可选 `--purge-config`）
- 共享库 `sonar-guard/scripts/lib/cursor_install_lib.py`（标准库 only）
- 重写 `sonar-guard/README.md`：以「一条命令安装」开头，明确装完后只需配 `SONAR_TOKEN` 与项目 `hostUrl`/`projectKey`（有 `sonar-project.properties` 时可省略后者）
- 更新根 `README.md` 目录结构，登记 `scripts/install_cursor.py`
- **BREAKING**：移除此前临时的 Node.js 安装脚本（`install-cursor.mjs` / `uninstall-cursor.mjs`），统一入口为 Python

## Capabilities

### New Capabilities

- `sonar-guard-cursor-install`: Cursor 用户级 rules 安装、目标仓库 `.sonarguard.json` 初始化、pre-commit 钩子安装/移除，以及配套文档与跨平台约定

### Modified Capabilities

- （无）`openspec/specs/` 中尚无 sonar-guard 相关主 spec

## Impact

- `sonar-guard/scripts/`（新增 Python 安装/卸载与 lib）
- `sonar-guard/README.md`、根 `README.md`
- 用户本机：`~/.cursor/rules/`、`~/.config/sonarguard/cursor-install.json`、目标仓库 `.git/hooks/sonarguard/`
- 无新外部依赖；安装与 pre-commit 均要求本机 `python` 或 `python3`
