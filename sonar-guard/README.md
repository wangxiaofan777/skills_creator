# sonar-guard — 两阶段 SonarQube 合规检查

开发时 + 提交时对照 SonarQube 规范检查代码，带修复风险评估。支持 Java、Python、JS/TS（含 Vue/React）、Go。

> **平台覆盖**：✅ Claude Code ✅ Cursor ✅ Codex（三端对齐：服务器模式 + B1 全项目 issue + 离线 fallback）

## 你只需要配 2 样

| # | 配置 | 放哪里 | 不配会怎样 |
|---|------|--------|------------|
| ① | **个人 token** | `SONAR_TOKEN` 或 `~/.config/sonarguard/config.json` | 离线模式 |
| ② | **项目 hostUrl + projectKey** | 目标仓库 `.sonarguard.json`（或 `sonar-project.properties`） | 离线模式 |

安装时可传入 `--host-url` / `--project-key`，或在交互提示中填写。`hook.*` 等有默认值，一般不用管。

---

## 三平台一键安装

在 **skills_creator 仓库根目录**执行（`--repo` 换成你的业务 git 仓库）：

| 平台 | 命令 |
|------|------|
| **全部**（Cursor + Claude + pre-commit） | `python sonar-guard/scripts/install.py --platform all --repo .` |
| Cursor | `python sonar-guard/scripts/install.py --platform cursor --repo .` |
| Claude Code | `python sonar-guard/scripts/install.py --platform claude --repo .` |
| Codex | `python sonar-guard/scripts/install.py --platform codex --repo .` |

无 `sonar-project.properties` 时示例：

```bash
python sonar-guard/scripts/install.py --platform all --repo . \
  --host-url https://sonar.example.com --project-key my-project
```

**移除：**

```bash
python sonar-guard/scripts/uninstall.py --platform all --repo .
python sonar-guard/scripts/uninstall.py --platform all --repo . --purge-config
```

兼容旧命令：`install_cursor.py` / `uninstall_cursor.py` 仍可用（内部调用统一安装器）。

装完后**新开一条 Agent 对话**。

---

## 在哪执行

先记住一件事：**`--repo` = 要被 Sonar 读配置的 git 仓库根**（该目录下的 `.sonarguard.json` 或 `sonar-project.properties`）。**你当前在哪个目录敲命令，可以和 `--repo` 不是同一个仓库。**

| 操作 | 在哪个目录执行 | 脚本在哪 |
|------|----------------|----------|
| **安装** | `<skills_creator>` 根目录 | `sonar-guard/scripts/install.py` |
| **B1 全项目扫描** | 任意目录均可；脚本路径指向 skills_creator | `sonar-guard/scripts/scan.py` |
| **pre-commit** | 不用手敲 | 目标仓库 `.git/hooks/sonarguard/`（`git commit` 自动跑） |

### 场景 A：扫 skills_creator 自身

```bash
cd <skills_creator>
python sonar-guard/scripts/scan.py --repo . --scope full
```

### 场景 B：在 skills_creator 里，扫另一个业务仓库（常用）

```bash
cd <skills_creator>
python sonar-guard/scripts/scan.py --repo <business-repo> --scope full
```

`<business-repo>` 须已安装 sonar-guard（`install.py --repo <business-repo>`）且配好 `.sonarguard.json` + 本机 `SONAR_TOKEN`。

### 场景 C：已在业务仓库里，不依赖 skills_creator 路径

装过 pre-commit 后，hook 目录里有 `sonar_api.py`（**没有** `scan.py`），等价 B1：

```bash
cd <business-repo>
python .git/hooks/sonarguard/sonar_api.py issues --repo . --all
```

### 场景 D：在 Cursor / Claude / Codex 里

打开**业务仓库**，对 Agent 说：「扫一下全项目的 sonar 问题」。Agent 应把 `--repo` 设为当前项目根，并执行 `scan.py --scope full` 或 hook 内 `issues --all`。

---

## 扫描模式

| 想做什么 | 命令 |
|----------|------|
| **B1 全项目**（Sonar 服务器全部未解决 issue） | 见上 **「在哪执行」**；或 `python sonar-guard/scripts/scan.py --repo <目标仓库> --scope full` |
| 增量（指定文件） | `python sonar-guard/scripts/scan.py --repo <目标仓库> --scope files --files src/Foo.java` |
| 提交前（暂存区） | `python sonar-guard/scripts/scan.py --repo <目标仓库> --scope staged` |
| 探测连通性 | `python sonar-guard/scripts/sonar_api.py status --repo <目标仓库>` |

B1 前提：项目在 Sonar 上至少被 CI/扫描器分析过一次。新写、尚未进 CI 的代码不会出现在 `--all` 结果中。

对 AI 说：「扫一下全项目的 sonar 问题」→ Agent 跑 `--scope full` 并出报告。

---

## 三平台能力（对齐后）

| 能力 | Claude Code | Cursor | Codex |
|------|-------------|--------|-------|
| 对话内审查 + 修复风险 | ✅ | ✅ | ✅ |
| Sonar API / B1 全项目 issue | ✅ | ✅ | ✅ |
| pre-commit 暂存区检查 | ✅ | ✅ | ✅ |

pre-commit 与 AI 工具无关，装一次全团队受益。

---

## 两个检查阶段

1. **开发阶段**：改完代码 → `status` → `scan --scope full|files` → 报告（见 `references/workflow.md`）
2. **提交阶段**：`git commit` → pre-commit 检查暂存区（本地启发式 + 服务器存量 issue）

---

## 目录结构

```
sonar-guard/
├── README.md
├── references/workflow.md       三端共享工作流
├── scripts/
│   ├── sonar_api.py             Sonar API（status / issues --all / rules）
│   ├── check_staged.py          pre-commit 检查
│   ├── scan.py                  full | staged | files
│   ├── install.py / uninstall.py
│   ├── install_cursor.py        兼容包装
│   └── lib/install_lib.py
├── claude-code/sonar-guard/     Claude Code Skill
├── cursor/rules/                Cursor .mdc 规则
└── codex/AGENTS.md
```

---

## 注意事项

- B1 issue 是 Sonar **上次扫描**结果，有滞后；最终以 CI 为准。
- 离线启发式是保守子集，不等价于完整 Sonar 引擎。
- 脚本均为 **Python 3** 标准库，需本机 `python` 或 `python3`。
- token 永不写入仓库或 `.sonarguard.json`。
