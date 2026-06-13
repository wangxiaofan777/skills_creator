# link-works-whiten-automation — Link Works 批量洗白

一键批量执行 Link Works「洗白 AI」，以及 git pre-commit 自动洗白指引。洗白 MUST 走 extension 命令 `link-works.whiteningFile`，禁止仅改 `commitReport.*.json`。

> 平台覆盖：✅ Claude Code ✅ Cursor ✅ Codex  
> 本包自带 Agent SKILL、洗白执行脚本与安装器（自包含、不绑定任何特定业务仓库）；执行脚本经 `install-link-works-scripts.mjs` 分发到**目标 git 仓库**的 `scripts/`。

## 前置条件

| 项 | 说明 |
|----|------|
| 扩展 | `link-works.link-works` ≥ 2.12.4 |
| IDE | Cursor 已打开目标 git 仓库 |
| Node.js | 18+（安装 Cursor Skill 时使用） |
| 脚本 | 由本包提供，经 `install-link-works-scripts.mjs` 分发到目标仓库 `scripts/` |

## 目录结构

```
link-works-whiten-automation/
├── README.md
├── claude-code/link-works-whiten-automation/SKILL.md
├── cursor/skills/link-works-whiten-automation/SKILL.md
├── codex/SKILL.md
└── scripts/
    ├── install-cursor-skill.mjs                装 Cursor 用户级 SKILL
    ├── install-link-works-scripts.mjs          分发洗白脚本到目标仓库 scripts/
    ├── link-works-whiten-all.ps1               一键洗白全部 pending
    ├── link-works-pre-commit-whiten.ps1        暂存区∩pending(钩子用)
    ├── link-works-invoke-run-commands.ps1      派发 vscode://runCommands
    ├── install-link-works-pre-commit-hook.ps1  装 pre-commit(opt-in)
    ├── link-works-whiten-all-keybinding.snippet.json
    └── lib/link-works-stats.mjs                读 commitReport、列 pending
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

## 分发洗白脚本到目标仓库

把执行脚本拷进目标业务仓库的 `scripts/`（在 **skills_creator 仓库根目录**执行）：

```bash
node link-works-whiten-automation/scripts/install-link-works-scripts.mjs --repo <目标仓库>
```

只覆盖自有 `link-works-*` 文件，不动目标 `scripts/` 内其它文件；更新脚本后重跑即可。装完后可在目标仓库内 opt-in 安装 pre-commit：`scripts/install-link-works-pre-commit-hook.ps1`。

## 常用操作

以下命令在**目标 git 仓库根目录**执行（非 skills_creator）：

| 场景 | 做法 |
|------|------|
| 列出待洗白 | `node scripts/lib/link-works-stats.mjs list-pending` |
| 一键洗白 | `scripts/link-works-whiten-all.ps1` 或 Tasks → Link Works: Whiten All Pending |
| pre-commit | `scripts/install-link-works-pre-commit-hook.ps1`（opt-in） |

macOS 执行 `.ps1` 洗白脚本需安装 [PowerShell 7](https://learn.microsoft.com/powershell/scripting/install/installing-powershell)（`pwsh`）。列出待洗白等 Node 脚本无需 PowerShell。
