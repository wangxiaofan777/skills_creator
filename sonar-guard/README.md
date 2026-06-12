# sonar-guard — 两阶段 SonarQube 合规检查

让代码在**提交前**就符合 SonarQube 规范，而不是等到上线前 CI 扫描才暴露问题。支持 Java、Python、JS/TS（含 Vue/React）、Go。

> 平台覆盖：✅ Claude Code（完整功能） ✅ Cursor ✅ Codex（后两者默认离线审查；pre-commit 脚本跨平台一键安装）

## 快速开始（Cursor，推荐）

在 **skills_creator 仓库根目录**执行（把 `--repo` 换成你的业务 git 仓库路径）：

```bash
python sonar-guard/scripts/install_cursor.py --repo .
```

一条命令会完成：

1. 安装 6 条 Cursor 规则 → `~/.cursor/rules/`
2. 在目标仓库创建 `.sonarguard.json`（有 `sonar-project.properties` 时自动填入 `hostUrl` / `projectKey`，否则为 `{}`）
3. 安装 pre-commit 钩子（脚本复制到 `.git/hooks/sonarguard/`，不覆盖已有钩子的其他逻辑）

**移除：**

```bash
python sonar-guard/scripts/uninstall_cursor.py --repo .
# 同时删除 .sonarguard.json：
python sonar-guard/scripts/uninstall_cursor.py --repo . --purge-config
```

装完后**新开一条 Cursor Agent 对话**，改代码后应自动出 Sonar 合规报告。

---

## 装完后你只需要配什么

| 配置 | 什么时候要 | 放哪里 | 不配会怎样 |
|------|------------|--------|------------|
| **个人 token** | 要连公司 Sonar 服务器时 | 环境变量 `SONAR_TOKEN`，或 `~/.config/sonarguard/config.json` 里 `{"token":"squ_xxx"}` | 离线模式，对话审查 + 本地 pre-commit 仍可用 |
| **项目 hostUrl + projectKey** | 要连 Sonar，且仓库没有 `sonar-project.properties` 时 | 目标仓库 `.sonarguard.json` | 同上 |

**不用你管的（已有默认值）：**

- `hook.mode` → `severity`（只拦截 BLOCKER / CRITICAL）
- `hook.blockSeverities`、`hook.localChecks` → 脚本内置默认
- Sonar 服务器超时 / 不可达 → 自动降级本地检查，不挡所有人提交
- 紧急情况 → `git commit --no-verify` 跳过钩子（不推荐）

### `.sonarguard.json` 字段说明（能省则省）

| 字段 | 必写？ | 说明 |
|------|--------|------|
| （整个文件） | 是（安装脚本会创建） | 作为「本仓库启用 sonar-guard」开关；`{}` 即可离线使用 |
| `hostUrl` | 否 | 可从 `sonar-project.properties` 或 `SONAR_HOST_URL` 推断 |
| `projectKey` | 否 | 可从 `sonar-project.properties` 推断 |
| `hook.mode` | 否 | `block` / `warn` / `severity`（默认） |
| `hook.blockSeverities` | 否 | 默认 `["BLOCKER","CRITICAL"]` |
| `hook.localChecks` | 否 | 默认 `true`（本地启发式：空 catch、debugger、console.log 等） |

**不要把 token 写进 `.sonarguard.json`**（不进仓库、不进报告）。

---

## 两个检查阶段

1. **开发阶段（对话内）**：写完/改完代码，对照 Sonar 规则审查，输出：有什么问题 → 怎么修 → 修复风险（🟢 低 / 🟡 中 / 🔴 高）。
2. **提交阶段（pre-commit）**：`git commit` 时检查暂存区；按 `hook.mode` 决定拦截或仅警告。

---

## 三平台能力差异

| 能力 | Claude Code | Cursor / Codex |
|------|-------------|----------------|
| 对话内审查 + 修复风险评估 | ✅ | ✅（离线规则子集） |
| Sonar API（活跃规则、存量 issue） | ✅ `scripts/sonar_api.py` | ❌ 需从 Sonar 页面提供，或配 token 后手动跑脚本 |
| pre-commit 暂存区检查 | ✅ | ✅ 用 `install_cursor.py` 安装（与 AI 工具无关） |

pre-commit 装好后全团队受益，不依赖 Cursor / Claude Code 是否打开。

---

## 其他平台安装

**Claude Code**（完整功能）：复制 `claude-code/sonar-guard/` 到 `~/.claude/skills/`，对 Claude 说「帮我配置 sonar-guard」，或手动：

```bash
bash claude-code/sonar-guard/scripts/install_hook.sh /path/to/repo
```

**Codex**：把 `codex/AGENTS.md` 合并进项目根 `AGENTS.md`；pre-commit 仍可用上面的 `install_cursor.py`。

**仅手动装 Cursor 规则**（不用脚本）：复制 `cursor/rules/*.mdc` → 项目或 `~/.cursor/rules/`，并在仓库根放 `.sonarguard.json`（至少 `{}`）。

---

## 目录结构

```
sonar-guard/
├── README.md
├── scripts/
│   ├── install_cursor.py        一键安装（Cursor + 仓库配置 + 钩子）
│   ├── uninstall_cursor.py      一键移除
│   └── lib/cursor_install_lib.py
├── claude-code/sonar-guard/     Claude Code Skill + sonar_api.py / check_staged.py
├── cursor/rules/                Cursor .mdc 规则
└── codex/AGENTS.md
```

---

## 常用操作

| 想做什么 | 命令 / 说法 |
|----------|-------------|
| 一键安装 | `python sonar-guard/scripts/install_cursor.py --repo <仓库>` |
| 一键移除 | `python sonar-guard/scripts/uninstall_cursor.py --repo <仓库>` |
| 只装规则、不装钩子 | 加 `--no-hook` |
| 检查某段代码 | 「帮我看看这段代码有没有 sonar 问题」 |
| 改成只警告不拦截 | 编辑 `.sonarguard.json` → `"hook": {"mode": "warn"}` |
| 手动模拟 pre-commit | `python .git/hooks/sonarguard/check_staged.py --repo .` |

---

## 注意事项

- 服务器 issue 是上次扫描结果，有滞后；新写的代码主要靠对话内审查覆盖。
- 离线启发式是保守子集，不等价于完整 Sonar 扫描，最终以 CI 为准。
- 安装与 pre-commit 脚本均为 **Python 3**（仅标准库），本机需有 `python` 或 `python3`。
