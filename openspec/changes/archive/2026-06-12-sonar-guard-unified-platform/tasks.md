## 1. 公共脚本层

- [x] 1.1 将 `sonar_api.py`、`check_staged.py` 移到 `sonar-guard/scripts/`（或复制为 canonical 并更新 import 路径）
- [x] 1.2 实现 `issues --all`：分页拉取全项目未解决 issue，`--all` 与 `--files` 互斥
- [x] 1.3 添加可选环境变量 `SONARGUARD_MAX_ISSUE_PAGES`（默认 20）防止超大项目超时
- [x] 1.4 更新 `cursor_install_lib.py` 与 `install_hook.sh` 从 `sonar-guard/scripts/` 复制脚本
- [x] 1.5 在 `claude-code/.../scripts/` 保留兼容入口（转发或文档说明 canonical 路径）

## 2. scan.py 薄封装

- [x] 2.1 新增 `sonar-guard/scripts/scan.py`，支持 `--scope full|staged|files`
- [x] 2.2 `full` → 调用 `issues --all`；`staged` → `check_staged.py`；`files` → `issues --files`

## 3. 统一安装/移除

- [x] 3.1 新增 `install.py`：`--platform cursor|claude|codex|all`、`--host-url`、`--project-key`、交互式 prompt
- [x] 3.2 实现 Claude skill 复制到 `~/.claude/skills/sonar-guard/`
- [x] 3.3 实现 Codex AGENTS 标记块合并（可选 `--no-codex` 或默认跳过，按 design 决定）
- [x] 3.4 新增 `uninstall.py` 对称移除三平台 + hook
- [x] 3.5 将 `install_cursor.py` / `uninstall_cursor.py` 改为调用统一安装器的薄包装

## 4. 三端 AI 规则对齐

- [x] 4.1 新增 `sonar-guard/references/workflow.md`（status → issues --all|--files → 报告 + 截断规则）
- [x] 4.2 更新 Claude Code `SKILL.md`：B1 全项目扫描、`issues --all`、canonical 脚本路径
- [x] 4.3 更新 Cursor `00-sonar-guard-base.mdc`：服务器模式 + 离线 fallback，删除「仅 Claude 提供 API」表述
- [x] 4.4 更新 Codex `AGENTS.md`：同步工作流，规则细节引用 references

## 5. 文档

- [x] 5.1 重写 `sonar-guard/README.md`：三平台并列、极简配置（token + 项目）、B1/增量/pre-commit 用法
- [x] 5.2 更新根 `README.md` 目录结构与 sonar-guard 能力描述
- [x] 5.3 安装后 hint 文案：无 properties 时提示 `--host-url`/`--project-key` 或交互输入

## 6. 验证

- [x] 6.1 本地验证 `sonar_api.py status` / `issues --all`（需有效 SONAR_TOKEN 与 projectKey）
- [x] 6.2 验证 `install.py --platform all --repo .` 与 `uninstall.py` 往返
- [x] 6.3 验证 pre-commit 仍只检查暂存区且脚本来自 canonical 路径
- [x] 6.4 运行 `openspec verify sonar-guard-unified-platform`（若可用）确认 artifact 与实现一致
