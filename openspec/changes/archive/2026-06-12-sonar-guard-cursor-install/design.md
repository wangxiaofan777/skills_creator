## Context

sonar-guard 已有 Claude Code 完整版（`sonar_api.py`、`check_staged.py`、`install_hook.sh`）和 Cursor 离线 rules（6 个 `.mdc`）。此前 Cursor 接入靠手抄 rules + 手建 `.sonarguard.json`，README 以满配 JSON 示例为主，用户不清楚最少配置。link-works 已用单文件 Node 安装脚本建立先例；本次将 sonar-guard 安装统一为 Python 标准库，并覆盖 rules、仓库开关文件与 pre-commit 三件套。

当前仓库中已实现初版 `install_cursor.py` / `uninstall_cursor.py`；本 change 的文档用于固化需求、验收标准与后续 `/opsx:apply` 对齐。

## Goals / Non-Goals

**Goals:**

- 一条 Python 命令完成 Cursor rules + `.sonarguard.json` + pre-commit（可 `--no-hook`）
- 一条 Python 命令干净卸载（manifest 驱动 rules 删除；钩子按标记块移除）
- README 以「装完只配 token / 项目」为叙事主线
- Windows / macOS 双平台，路径仅用 `~` 与仓库相对路径
- 与现有 `check_staged.py` / `sonar_api.py` 技术栈一致（Python 3 stdlib）

**Non-Goals:**

- 不改 Cursor rules 的审查规则内容本身
- 不在此 change 中实现 Cursor 内自动调用 `sonar_api.py`（仍属 Claude Code 完整版能力）
- 不将 `.sonarguard.json` 触发条件改为读取 `sonar-project.properties`（Cursor rules 仍要求仓库根存在 `.sonarguard.json`）
- 不提供 PowerShell 独立安装脚本（Python 为唯一自动化入口）

## Decisions

### 1. Python stdlib 而非 Node.js

**选择:** `install_cursor.py` + `lib/cursor_install_lib.py`，仅标准库。

**理由:** pre-commit 已是 Python；团队环境通常已有 Python；避免为安装再引入 Node 18+。

**备选:** 延续 `install-cursor.mjs`（link-works 模式）— 已弃用，避免 sonar-guard 双运行时。

### 2. 用户级 rules + 仓库级开关

**选择:** rules 装到 `~/.cursor/rules/`（全局一次）；`.sonarguard.json` 与 pre-commit 按 `--repo` 目标仓库。

**理由:** rules 内容不变，全局安装减少每仓库重复；`.sonarguard.json` 作为 per-repo 开关与团队共享 project 配置，符合现有 `.mdc` 文案。

**备选:** rules 装到项目 `.cursor/rules/` — 每仓库复制，运维成本高。

### 3. 安装清单 `~/.config/sonarguard/cursor-install.json`

**选择:** 记录已装 rule 文件名与目录，卸载时精确删除。

**理由:** 避免误删用户手改的其他 `.mdc`；无 manifest 时回退到固定六文件名列表。

### 4. pre-commit 标记块追加

**选择:** 复用 `install_hook.sh` 的 `# >>> sonar-guard >>>` … `<<<` 片段；钩子内 `python3` 回退 `python`。

**理由:** 与 Claude Code 版行为一致；不破坏已有 pre-commit；Windows Git Bash 可执行。

**实现:** 逻辑迁入 `cursor_install_lib.py`，`install_hook.sh` 保留给 Claude Code 文档路径，不强制删除。

### 5. `.sonarguard.json` 生成策略

**选择:** 不存在则创建；有 `sonar-project.properties` 则填入 `hostUrl`/`projectKey`；否则 `{}`。

**理由:** `{}` 即可触发离线 Cursor 审查；有 properties 则减少用户手写。

## Risks / Trade-offs

- **[Risk] Windows 无 bash 时 pre-commit 不执行** → 文档说明需 Git for Windows（含 bash）；钩子片段与现有 `install_hook.sh` 相同假设。
- **[Risk] 用户未新开 Cursor 对话，rules 未热加载** → 安装结束打印提示「新开 Agent 对话」。
- **[Risk] 全局 rules 与项目级 rules 重名** → 六文件固定命名；卸载只删 manifest 列表。
- **[Trade-off] Cursor 仍要求 `.sonarguard.json` 存在** → 仅有 `sonar-project.properties` 时安装脚本仍会创建 `{}` 或合并字段。

## Migration Plan

1. 合并 change 并发布文档与脚本。
2. 已用 Node 脚本安装的用户：运行 `python sonar-guard/scripts/install_cursor.py --repo <repo>` 刷新；Node 文件已删除。
3. 回滚： `python sonar-guard/scripts/uninstall_cursor.py --repo <repo> --purge-config`（按需）。

## Open Questions

- 是否在后续 change 为 `sonar-guard` 增加与 link-works 同级的 `install_cursor_skill` 别名命令（当前脚本名已足够明确，暂不处理）。
- 是否将 `install_hook.sh` 改为薄包装调用 `install_cursor.py --no-rules`（非本 change 范围）。
