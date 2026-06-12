## Why

sonar-guard 文档与实现以 Cursor 为主、Claude Code 为「完整版」、Codex 为离线子集，三平台能力不对齐；用户无法从 Sonar 服务器拉取**全项目存量 issue** 做扫描（B1），且仓库无 `sonar-project.properties` 时不清楚最少要配什么。需要将脚本提升为平台无关公共层、三端工作流对齐（服务器模式 + 全项目 issue 扫描 + 增量 `--files`），并把配置收敛为「token + 项目 hostUrl/projectKey」两项。

## What Changes

- 将 `sonar_api.py`、`check_staged.py` 提升到 `sonar-guard/scripts/` 作为三端共用脚本；`claude-code/.../scripts/` 保留为兼容入口或改为引用公共层
- 扩展 `sonar_api.py`：新增 `issues --all`（分页拉取项目全部未解决 issue，B1 全项目扫描）
- 新增可选薄封装 `scan.py --scope full|staged|files`（`full` 内部调用 `issues --all`）
- 统一安装/移除：`install.py` / `uninstall.py` 支持 `--platform cursor|claude|codex|all`；安装时无 `sonar-project.properties` 时通过 `--host-url` / `--project-key` 或交互写入 `.sonarguard.json`
- 三端 AI 规则对齐：Claude SKILL、Cursor `.mdc`、Codex `AGENTS.md` 统一工作流（`status` → `issues --all` 或 `--files` → 报告）；离线 fallback 保留
- 报告约定：全项目 issue 汇总必全，BLOCKER/CRITICAL 详情全列，MAJOR 截断，MINOR/INFO 仅计数
- 重写 `sonar-guard/README.md`：三平台并列（非 Cursor 打头）、极简配置说明、B1 全项目扫描与增量扫描用法
- 保留现有 pre-commit 暂存区检查行为（`--files`，不改为全项目）

## Capabilities

### New Capabilities

- `sonar-guard-api`: 平台无关 Sonar API 脚本（`status`、`rules`、`issues --files`、`issues --all`、`rule`）及配置合并逻辑
- `sonar-guard-unified-install`: 三平台一键安装/移除（Cursor rules、Claude skill、Codex AGENTS 合并、pre-commit、`.sonarguard.json` 初始化与无配置文件时的项目信息收集）
- `sonar-guard-scan-workflow`: 三端 AI 扫描工作流（B1 全项目 issue、增量 `--files`、报告格式与 issue 详情截断策略）

### Modified Capabilities

- `sonar-guard-cursor-install`: 安装入口从仅 `install_cursor.py` 扩展为统一 `install.py` 的 Cursor 子命令；行为保持兼容或 **BREAKING** 将 `install_cursor.py` 标记为薄包装

## Impact

- `sonar-guard/scripts/`（公共脚本层、install/uninstall/scan）
- `sonar-guard/claude-code/`、`sonar-guard/cursor/`、`sonar-guard/codex/`（工作流与文档同步）
- `sonar-guard/README.md`、根 `README.md`
- 用户本机：`~/.cursor/rules/`、`~/.claude/skills/`、目标仓库 `.sonarguard.json`、`.git/hooks/sonarguard/`
- 无新外部依赖；仍为标准库 Python 3
- 依赖 Sonar 服务器：B1 要求项目至少被 CI/扫描器分析过一次（`project_state: ok`）
