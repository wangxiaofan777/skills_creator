## Context

`skills_creator/link-works-whiten-automation` 提供 Link Works 洗白的 Agent SKILL 与 Cursor 安装说明。当前状态：

- 安装脚本：`scripts/install-cursor-skill.ps1`，通过 `$MyInvocation` 自定位包根目录（逻辑可移植），但仅能在 Windows PowerShell 下直接运行
- README：示例命令硬编码 `D:\skills_creator\...`，并指向 Metis 仓库的 `install-link-works-cursor-skill.ps1` 与 `SKILLS_CREATOR_ROOT`
- SKILL.md：`Canonical sources` 含 `D:\skills_creator` 与 Metis OpenSpec 路径

内容已迁到 `skills_creator`；Metis 仓库不在本次变更范围内。洗白执行脚本（`link-works-whiten-all.ps1` 等）仍位于各目标 git 仓库的 `scripts/`，与本次「安装 Cursor Skill」正交。

## Goals / Non-Goals

**Goals:**

- 单一跨平台安装脚本，Windows 与 macOS 使用相同命令
- 文档与 SKILL 内示例均使用相对路径（自仓库根）或 `~` 用户目录，禁止机器绝对路径
- 安装目标统一为 `~/.cursor/skills/link-works-whiten-automation/SKILL.md`
- 根 README 开发规则明确 OS 双平台要求
- 去除 Metis 安装入口与中心化表述（保留「目标仓库自备洗白脚本」说明）

**Non-Goals:**

- 修改 Metis 或任何外部仓库
- 将洗白 `.ps1` 脚本改写为跨平台或迁入 `skills_creator`
- 新增 npm 包或 `package.json` 依赖
- Linux 专项测试或文档（与 macOS 共用 `.mjs` 即可，不单独承诺）

## Decisions

### 1. 安装脚本：Node `.mjs`（非双脚本、非纯 PowerShell）

**选择**：`install-cursor-skill.mjs`，仅用 Node 内置模块（`fs`、`path`、`os`）。

**理由**：

- Win / Mac 同一条命令：`node link-works-whiten-automation/scripts/install-cursor-skill.mjs`
- `os.homedir()` 跨平台解析用户主目录，无需区分 `%USERPROFILE%` / `$HOME`
- 洗白流程已依赖 Node（`link-works-stats.mjs`），不引入新运行时

**备选**：

| 方案 | 弃用原因 |
|------|----------|
| `.ps1` + `.sh` 双脚本 | 维护两份，违背「只写一个脚本」 |
| 单 `.ps1` + pwsh | Mac 需额外装 PowerShell；Windows/Mac 启动命令不一致 |
| 单 `.sh` | Windows 原生不支持 |

### 2. 包根目录解析

使用 `import.meta.url` + `fileURLToPath` 定位脚本文件，`scripts/` 的上两级为 `link-works-whiten-automation` 包根。与现有 `.ps1` 的 `Split-Path` 两级父目录语义一致。

### 3. 删除 `.ps1` 安装器（BREAKING）

旧脚本无转发兼容层；README 与 SKILL 直接指向 `.mjs`。目标安装路径不变，已安装用户无需重装。

### 4. 文档结构

- **安装段**：仓库根 + 一条 `node` 命令 + 手动复制兜底
- **前置条件**：补充 Node.js 18+
- **常用操作**：保留目标仓库内洗白脚本说明；macOS 执行 `.ps1` 时注明需 PowerShell 7 (`pwsh`)
- **Metis**：README 与 SKILL 的 Canonical sources 改为 `skills_creator` 相对路径；Script map 标题改为「目标仓库脚本」类中性表述

### 5. 根 README 规则扩展

在「开发规则」增加第 5 条（或并入现有条目）：安装脚本与文档须覆盖 Windows 与 macOS；禁止在文档中使用盘符或机器相关绝对路径。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 用户未装 Node 无法运行安装脚本 | 文档提供手动复制；前置条件写明 Node 18+ |
| 删除 `.ps1` 打断旧书签/笔记 | BREAKING 在 proposal 标明；命令仅一行且路径不变 |
| SKILL 三端不同步 | tasks 中明确三份 SKILL.md 同批更新 |
| Mac 用户误以为洗白 `.ps1` 也可直接跑 | README 常用操作区分「装 skill」与「跑洗白」 |

## Migration Plan

1. 新增 `install-cursor-skill.mjs` 并在本机验证复制成功
2. 更新 README 与 SKILL 后删除 `install-cursor-skill.ps1`
3. 无需数据库或服务发布；合并即生效
4. **回滚**：恢复 `.ps1`、还原文档（git revert）

## Open Questions

（无——探索阶段已确认 Node 安装、不改 Metis、双平台文档。）
