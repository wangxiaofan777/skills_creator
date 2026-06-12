# link-works-whiten-automation — Link Works 批量洗白

一键批量执行 Link Works「洗白 AI」，以及 git pre-commit 自动洗白指引。洗白 MUST 走 extension 命令 `link-works.whiteningFile`，禁止仅改 `commitReport.*.json`。

> 平台覆盖：✅ Claude Code ✅ Cursor ✅ Codex  
> 本目录提供 Agent SKILL 与跨平台安装脚本；洗白执行脚本（`scripts/link-works-*`）由**目标 git 仓库**自备。

## 前置条件

| 项 | 说明 |
|----|------|
| 扩展 | `link-works.link-works` ≥ 2.12.4 |
| IDE | Cursor 已打开目标 git 仓库 |
| Node.js | 18+（安装 Cursor Skill 时使用） |
| 脚本 | 目标仓库已包含 `scripts/link-works-*.ps1`（或等价拷贝） |

## 目录结构

```
link-works-whiten-automation/
├── README.md
├── claude-code/link-works-whiten-automation/SKILL.md
├── cursor/skills/link-works-whiten-automation/SKILL.md
├── codex/SKILL.md
└── scripts/install-cursor-skill.mjs
```

## 安装（Cursor 用户级）

在 **skills_creator 仓库根目录**执行：

```bash
node link-works-whiten-automation/scripts/install-cursor-skill.mjs
```

安装到 `~/.cursor/skills/link-works-whiten-automation/SKILL.md`。

**手动安装（任意平台）**：复制 `cursor/skills/link-works-whiten-automation/` 到 `~/.cursor/skills/link-works-whiten-automation/`。

**Claude Code**：复制 `claude-code/link-works-whiten-automation/` 到 `~/.claude/skills/`。  
**Codex**：复制 `codex/SKILL.md` 到项目或全局 skills 目录。

## 常用操作

以下命令在**目标 git 仓库根目录**执行（非 skills_creator）：

| 场景 | 做法 |
|------|------|
| 列出待洗白 | `node scripts/lib/link-works-stats.mjs list-pending` |
| 一键洗白 | `scripts/link-works-whiten-all.ps1` 或 Tasks → Link Works: Whiten All Pending |
| pre-commit | `scripts/install-link-works-pre-commit-hook.ps1`（opt-in） |

macOS 执行 `.ps1` 洗白脚本需安装 [PowerShell 7](https://learn.microsoft.com/powershell/scripting/install/installing-powershell)（`pwsh`）。列出待洗白等 Node 脚本无需 PowerShell。
