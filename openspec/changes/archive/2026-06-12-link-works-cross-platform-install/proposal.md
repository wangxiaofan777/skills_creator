## Why

`link-works-whiten-automation` 的安装文档与脚本目前仅面向 Windows：README 使用 `D:\skills_creator` 等机器相关绝对路径，安装器只有 PowerShell 版本，且仍引用已迁出的 Metis 仓库包装脚本。Mac 用户无法按文档完成安装，且每台电脑路径不同导致示例命令不可复制。需要将 Cursor Skill 安装流程改为跨平台、路径无关，并统一到 `skills_creator` 仓库内维护。

## What Changes

- 新增跨平台 Node 安装脚本 `link-works-whiten-automation/scripts/install-cursor-skill.mjs`（Win / macOS 同一条 `node` 命令）
- **BREAKING**：删除 `install-cursor-skill.ps1`，安装方式从 PowerShell 改为 Node
- 重写 `link-works-whiten-automation/README.md`：相对路径示例、`~/.cursor/skills/` 目标路径、去除 Metis 安装段落与绝对路径
- 更新根 `README.md`：目录结构反映 `.mjs` 安装器；开发规则补充 OS 双平台（Windows + macOS）与禁止文档绝对路径
- 同步三端 SKILL.md（Cursor / Claude Code / Codex）中的 Canonical sources 与 Script map 措辞，去除 Metis 中心化与 `D:\skills_creator` 硬编码
- 不修改 Metis 仓库或任何外部项目代码

## Capabilities

### New Capabilities

- `link-works-skill-install`: Cursor 用户级 Skill 的跨平台安装（Node 脚本、文档约定、目标路径与错误行为）

### Modified Capabilities

（无既有 spec；`openspec/specs/` 为空）

## Impact

- **文件**：`link-works-whiten-automation/scripts/`、`link-works-whiten-automation/README.md`、根 `README.md`、三份 `SKILL.md`
- **依赖**：安装需 Node.js 18+（与洗白流程中 `link-works-stats.mjs` 一致，非新增生态依赖）
- **用户**：已用旧 `.ps1` 安装的用户不受影响（目标路径相同）；新用户按新文档安装
- **范围外**：目标业务仓库内的 `scripts/link-works-*.ps1` 洗白脚本仍由各项目自备；Mac 执行洗白仍可能需要 `pwsh`
