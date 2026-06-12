## Context

sonar-guard 当前结构：

- **脚本**：`sonar_api.py`、`check_staged.py` 位于 `claude-code/sonar-guard/scripts/`；Cursor 安装时复制到 `.git/hooks/sonarguard/`
- **AI 规则**：Claude Code SKILL 含完整服务器工作流；Cursor `.mdc` 与 Codex `AGENTS.md` 写死「离线模式」
- **安装**：仅 `install_cursor.py` / `uninstall_cursor.py`；Claude/Codex 需手动复制
- **issues API**：`issues` 子命令强制 `--files`，无法 B1 全项目拉取

用户约束（探索结论）：

- 仓库无 `sonar-project.properties`，需安装时收集 `hostUrl` + `projectKey`
- 全仓库扫描选 **B1**：Sonar 服务器全项目未解决 issue，非 AI 逐文件审查
- 三平台（Claude Code / Cursor / Codex）能力对齐，README 不以 Cursor 为主

## Goals / Non-Goals

**Goals:**

- 公共脚本层 `sonar-guard/scripts/`，三端文档与 AI 规则指向同一路径
- `issues --all` 分页拉取全项目 issue；`issues --files` 保持增量/pre-commit 行为
- 统一 `install.py` / `uninstall.py` 支持 `--platform all|cursor|claude|codex`
- 无 Sonar 配置文件时，安装器写入 `hostUrl`/`projectKey`（CLI 或交互）
- 三端工作流对齐：`status` → `issues --all|--files` → 统一报告格式
- README 三平台并列；配置收敛为 token + 项目两项

**Non-Goals:**

- 集成 `sonar-scanner` 本地引擎或 SonarLint CLI
- 全仓库 AI 逐文件对照 rules 审查（B2/B3）
- pre-commit 改为全项目扫描（保持暂存区 `--files`）
- 将 token 写入 `.sonarguard.json` 或仓库内任何文件

## Decisions

### 1. 脚本目录：提升到 `sonar-guard/scripts/`

**选择**：`sonar_api.py`、`check_staged.py` 作为 canonical 源；`claude-code/.../scripts/` 保留同名文件，内容为「转发 import 或 shutil 说明」以避免破坏已有 SKILL 路径引用。

**备选**：仅保留 claude-code 路径 — 拒绝，与「平台无关」目标冲突。

### 2. B1 实现：`issues --all`

**选择**：扩展 `cmd_issues`：当 `--all` 时调用 `/api/issues/search?componentKeys={projectKey}&resolved=false`，分页 `ps=500` 直至 `total` 收齐；JSON 输出含 `total`、`bySeverity`、`issues`（与 `--files` 同结构）。

**详情截断**：脚本层输出全量 JSON；AI 报告层按 spec 截断（BLOCKER/CRITICAL 全列，MAJOR 前 N 条，MINOR/INFO 仅计数）。不在脚本内硬截断，便于 CI/脚本消费全量。

**备选**：新增独立 `issues-all` 子命令 — 拒绝，与 `--files` 互斥的单一 `issues` 更清晰。

### 3. `scan.py` 薄封装（可选但建议）

**选择**：`scan.py --scope full|staged|files [--files ...]`：

| scope | 行为 |
|-------|------|
| `full` | `sonar_api issues --all` |
| `staged` | 等价 `check_staged.py`（或内部调用） |
| `files` | `sonar_api issues --files` |

**备选**：仅文档说明命令 — 可用，但用户「扫全仓库」口语与 `scan.py --scope full` 更直观。

### 4. 统一安装器

**选择**：`install.py --platform all --repo <path> [--host-url URL] [--project-key KEY] [--no-hook]`

| platform | 动作 |
|----------|------|
| `cursor` | 现有 `install_cursor_rules` + hook + `.sonarguard.json` |
| `claude` | 复制 `claude-code/sonar-guard/` → `~/.claude/skills/sonar-guard/` |
| `codex` | 复制或合并 `codex/AGENTS.md` 片段到目标仓库根 `AGENTS.md`（标记块，可卸载） |
| `all` | 以上三者 + hook 一次 |

无 `sonar-project.properties` 且无 CLI 参数时：**交互式**询问 hostUrl/projectKey（可 Enter 跳过 → `{}` 离线）。

**兼容**：`install_cursor.py` 保留为调用 `install.py --platform cursor` 的薄包装（**非 BREAKING**）。

### 5. 三端 AI 工作流

**选择**：共享步骤写入 `references/workflow.md`（新建于 `sonar-guard/` 或 `claude-code/.../references/`），三端引用同一文本要点：

1. `python sonar-guard/scripts/sonar_api.py status --repo .`
2. `ok` → 全项目：`issues --all`；增量：`issues --files <变更文件>`
3. `not_found|no_auth|unreachable` → 离线模式 + 说明原因
4. 输出统一报告模板（含 B1 汇总表与截断规则）

Cursor `00-sonar-guard-base.mdc`：删除「仅离线」表述，改为与 Claude SKILL 一致的服务器优先、离线 fallback。

### 6. 配置模型（不变，文档强化）

| 层 | 内容 | 位置 |
|----|------|------|
| 个人 | `token` | `SONAR_TOKEN` 或 `~/.config/sonarguard/config.json` |
| 项目 | `hostUrl`, `projectKey` | `.sonarguard.json` 或 `sonar-project.properties` |
| 钩子 | `hook.*` | 默认内置，用户一般不配 |

安装器在无 properties 时写入用户提供的 hostUrl/projectKey，而非空 `{}`（若用户提供了）。

### 7. README 结构

**选择**：

1. 定位 + 三平台能力表（并列）
2. 极简配置（2 项）
3. 一键安装（三平台命令表）
4. 扫描模式：B1 全项目 / 增量 / pre-commit
5. 目录结构

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| B1 依赖项目曾被 Sonar 扫描 | `status` 明确提示 `not_found`；文档说明需 CI 先扫一次 |
| 全项目 issue 数量极大（数千） | 报告截断策略；JSON 全量供脚本，AI 不倾倒全部 |
| Codex AGENTS 合并污染用户 AGENTS.md | 标记块 `# >>> sonar-guard >>>` 可卸载；文档说明 |
| 双份 scripts 路径漂移 | canonical 仅 `sonar-guard/scripts/`；claude-code 转发或 install 时只复制 canonical |
| 交互安装在无 TTY 环境失败 | 支持 `--host-url`/`--project-key`；无 TTY 时跳过交互写 `{}` |

## Migration Plan

1. 实现公共 `scripts/` 与 `issues --all`
2. 更新 hook 安装复制路径指向 canonical scripts
3. 同步三端 AI 规则与 README
4. 新增 `install.py`；`install_cursor.py` 转薄包装
5. 已有用户：重新运行 `install.py --platform all --repo <repo>` 刷新 rules 与 hook 脚本

**Rollback**：`uninstall.py --platform all`；hook 与 rules 按 manifest/标记块移除。

## Open Questions

- Codex 合并 AGENTS.md 默认装到**目标业务仓库**还是仅 skills_creator 文档说明手动合并？（建议：`--repo` 目标仓库可选合并，默认仅装 Cursor+Claude+hook）
- `issues --all` 分页上限：是否设 `maxPages` 防止超大项目超时？（建议：`SONARGUARD_MAX_ISSUE_PAGES` 默认 20，即最多 10000 条）
