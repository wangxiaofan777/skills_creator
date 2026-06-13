# sonar-guard — 两阶段 SonarQube 合规检查

开发时 + 提交时对照 SonarQube 规范检查代码，带修复风险评估。支持 Java、Python、JS/TS（含 Vue/React）、Go。

> **平台覆盖**：✅ Claude Code ✅ Cursor ✅ Codex（三端对齐：服务器模式 + B1 全项目 issue + 离线 fallback）

> **阅读路径**：简介 → [快速开始](#三平台一键安装) → [配置](#配置参考) → [使用](#扫描模式) → [架构](#架构) → [支持语言](#支持语言) → [排障](#命令跑不通)

## 你只需要配 2 样

| # | 配置 | 放哪里 | 不配会怎样 |
|---|------|--------|------------|
| ① | **个人 token** | `SONAR_TOKEN` 或 `~/.config/sonarguard/config.json` | 离线模式 |
| ② | **项目 hostUrl + projectKey** | 目标仓库 `.sonarguard.json`（或 `sonar-project.properties`） | 离线模式 |

安装时可传入 `--host-url` / `--project-key`，或在交互提示中填写。`hook.*` 等有默认值，一般不用管。

---

## 三平台一键安装

文档里的路径都是**占位符**，请换成你本机实际目录（clone 在哪都行，**不要**写死 `D:\...`）：

| 占位符 | 含义 |
|--------|------|
| `<skills_creator>` | 本仓库 clone 到的**任意**目录 |
| `<business-repo>` | 业务 git 仓库根（例如 metis） |

> **重要**：`sonar-guard/scripts/install.py` 只存在于 `<skills_creator>` 里。在业务仓库内**不能**写 `python sonar-guard/scripts/install.py`（会 file not found）。

### 方式 A：推荐（任意电脑，相对路径）

clone 后 **cd 进 skills_creator**，用相对路径 install，**不依赖盘符**：

```powershell
cd <skills_creator>
python sonar-guard/scripts/install.py --platform all --repo <business-repo> --host-url https://sonar.example.com --project-key YOUR_KEY
```

装 **skills_creator 自身**时：把 `<business-repo>` 写成 `.`。

### 方式 B：在业务仓库里 install（先配一次环境）

适合「人已经在 `<business-repo>` 里、不想 cd」——先在本机配置 skills_creator 位置（**每台电脑一次**）：

```powershell
cd <skills_creator>
powershell -File sonar-guard/scripts/setup-env.ps1
```

`setup-env` 会写入 `~/.config/sonarguard/config.json` 并设置用户级 `SONARGUARD_HOME`。**新开终端**后：

```powershell
cd <business-repo>
python "$env:SONARGUARD_HOME/sonar-guard/scripts/install_bootstrap.py" --platform all --repo . --host-url https://sonar.example.com --project-key YOUR_KEY
```

Linux/macOS：用 `sonar-guard/scripts/setup-env.sh`，之后 `python "$SONARGUARD_HOME/sonar-guard/scripts/install_bootstrap.py" ...`。

### 方式 C：业务仓库已装过（升级 / 重装）

```powershell
cd <business-repo>
python .sonarguard/install.py --platform all --repo .
```

依赖本机 `~/.config/sonarguard/config.json` 里的 `packageRoot`（方式 A/B 成功 install 后会自动写入）。

| 平台 | 参数 |
|------|------|
| **全部** | `--platform all` |
| Cursor | `--platform cursor` |
| Claude Code | `--platform claude` |
| Codex | `--platform codex` |

**移除（业务仓库内）：**

```powershell
python .sonarguard/uninstall.py --platform all --repo .
python .sonarguard/uninstall.py --platform all --repo . --purge-config
```

### 开放给其他开发者 / 换电脑

| 角色 | 做什么 |
|------|--------|
| **第一次接入的人** | clone `<skills_creator>` → **方式 A** install 到 `<business-repo>`；可选把生成的 `.sonarguard/` **提交到业务仓库** |
| **后续同事（只扫 Sonar）** | clone 业务仓库 → 配 `SONAR_TOKEN` → `python .sonarguard/scan.py --repo . --scope full`（若 `.sonarguard/` 已在 git 里） |
| **后续同事（Cursor + pre-commit）** | 各自 clone `<skills_creator>` → **方式 A** 再跑一遍（规则装在本机 `~/.cursor`，hook 在本机 `.git`） |

`packageRoot` 在 **`~/.config/sonarguard/config.json`（每人本机）**，路径互不影响；文档示例不出现固定盘符。

兼容旧命令：`install_cursor.py` / `uninstall_cursor.py` 仍可用（内部调用统一安装器）。

装完后**新开一条 Agent 对话**。

---

## 快速开始（业务仓库）

### 第一次安装

**推荐（任意电脑）：**

```powershell
cd <skills_creator>
python sonar-guard/scripts/install.py --platform all --repo <business-repo> --host-url https://sonar.example.com --project-key YOUR_KEY
```

已在业务仓库、且配好 `SONARGUARD_HOME` 时，见上文 **方式 B**。

### 日常扫描（install 后）

```powershell
cd <business-repo>
python .sonarguard/sonar_api.py status --repo .
python .sonarguard/scan.py --repo . --scope full
python .sonarguard/scan.py --repo . --scope staged
```

> `.sonarguard/` 由 `install.py` 写入业务仓库根目录；未 install 前不存在。

### 命令跑不通？

| 报错 | 原因 | 解决 |
|------|------|------|
| `can't open file '...\metis\sonar-guard\scripts\install.py'` | 在业务仓库里用了相对路径 `sonar-guard/scripts/` | **方式 A**：`cd <skills_creator>` 再 install；或 **方式 B** + `SONARGUARD_HOME` |
| `can't open file '...\sonar-guard\scripts\...'`（scan/status） | 在业务仓库里用了 skills_creator 的扫描路径 | 用 `.sonarguard/scan.py`；或先 install |
| `Unexpected token 'host-url'`（PowerShell） | 用了 bash 的 `\` 续行 | 改成 **单行**命令（见上方示例） |
| `can't open file '...\.sonarguard\...'` | 未 install | 先跑 `install_bootstrap.py` |

---

## 在哪执行

先记住一件事：**`--repo` = 要被 Sonar 读配置的 git 仓库根**（该目录下的 `.sonarguard.json` 或 `sonar-project.properties`）。**你当前在哪个目录敲命令，可以和 `--repo` 不是同一个仓库。**

| 操作 | 在哪个目录执行 | 脚本在哪 |
|------|----------------|----------|
| **安装（每个业务仓库一次）** | `<skills_creator>` 根目录 | `sonar-guard/scripts/install.py --repo <业务仓库>` |
| **status / B1 / 增量 / 暂存区** | **业务仓库**根目录（install 后） | `.sonarguard/sonar_api.py`、`.sonarguard/scan.py` |
| **未 install 时远程扫** | `<skills_creator>` 根目录 | `sonar-guard/scripts/scan.py --repo <业务仓库>` |
| **pre-commit** | 不用手敲 | `.git/hooks/sonarguard/`（`git commit` 自动跑） |

### 场景 A：业务仓库内（install 后）

```powershell
cd <business-repo>
python .sonarguard/sonar_api.py status --repo .
python .sonarguard/scan.py --repo . --scope full
```

### 场景 B：在 skills_creator 里扫另一个业务仓库

```powershell
cd <skills_creator>
python sonar-guard/scripts/scan.py --repo <business-repo> --scope full
```

`<business-repo>` 须已 `install.py --repo <business-repo>` 且配好 `.sonarguard.json` + 本机 `SONAR_TOKEN`。

### 场景 C：扫 skills_creator 自身

```bash
cd <skills_creator>
python .sonarguard/scan.py --repo . --scope full
# 或（未 install 时）python sonar-guard/scripts/scan.py --repo . --scope full
```

### 场景 D：hook 路径（与 `.sonarguard/` 同脚本，可选）

```bash
cd <business-repo>
python .git/hooks/sonarguard/sonar_api.py issues --repo . --all
python .git/hooks/sonarguard/scan.py --repo . --scope full
```

### 场景 E：在 Cursor / Claude / Codex 里

打开**业务仓库**，对 Agent 说：「扫一下全项目的 sonar 问题」。Agent 应在项目根执行 `python .sonarguard/scan.py --repo . --scope full`（install 后）。

---

## 配置参考

### 最小配置（目标仓库根目录 `.sonarguard.json`）

```json
{
  "hostUrl": "https://sonar.example.com",
  "projectKey": "my-project-key"
}
```

- **不要**把 token 写进此文件；token 仅放本机（见下）。
- 空对象 `{}` = 未配置项目 → `status` 会报 `unreachable`（离线模式）。

### 个人 token（二选一）

**方式 A — 环境变量（推荐，CI/本机通用）：**

```bash
# PowerShell
$env:SONAR_TOKEN = "squ_xxxxxxxx"

# bash
export SONAR_TOKEN=squ_xxxxxxxx
```

**方式 B — 用户配置文件：**

`~/.config/sonarguard/config.json`（Windows: `%USERPROFILE%\.config\sonarguard\config.json`）

```json
{
  "token": "squ_xxxxxxxx"
}
```

可选在同一文件写默认 `hostUrl`（会被仓库 `.sonarguard.json` 覆盖，除非未配置）：

```json
{
  "token": "squ_xxxxxxxx",
  "hostUrl": "https://sonar.example.com"
}
```

### 用 `sonar-project.properties` 代替（可选）

若仓库已有 Sonar 扫描配置，可只配 token，项目侧用 properties：

```properties
sonar.projectKey=my-project-key
sonar.host.url=https://sonar.example.com
```

`.sonarguard.json` 中的同名字段优先于 properties。

### 完整 `.sonarguard.json`（含 pre-commit hook 选项）

一般不用改；默认值如下：

```json
{
  "hostUrl": "https://sonar.example.com",
  "projectKey": "my-project-key",
  "hook": {
    "mode": "severity",
    "blockSeverities": ["BLOCKER", "CRITICAL"],
    "localChecks": true
  }
}
```

| 字段 | 含义 | 默认 |
|------|------|------|
| `hook.mode` | pre-commit 拦截策略 | `"severity"` |
| `hook.blockSeverities` | 达到这些级别则阻止提交 | `["BLOCKER","CRITICAL"]` |
| `hook.localChecks` | 是否跑本地启发式检查 | `true` |

### 配置合并优先级

`load_config()` 读取顺序（后者覆盖前者，仅 token / hostUrl）：

1. 目标仓库 `.sonarguard.json`
2. 目标仓库 `sonar-project.properties`（补 `projectKey` / `hostUrl`）
3. `~/.config/sonarguard/config.json`（`token`；`hostUrl` 仅当仓库未配时）
4. 环境变量：`SONAR_TOKEN`、`SONAR_HOST_URL`

验证配置（**`--repo` = 目标 git 仓库根**）：

```bash
python sonar-guard/scripts/sonar_api.py status --repo <目标仓库>
```

### `status` 输出说明

| 字段 | 含义 |
|------|------|
| `hostUrl` | 合并后的 Sonar 地址；未配则为 `null` |
| `projectKey` | 合并后的项目 key |
| `tokenConfigured` | 是否已有 token（不展示 token 本身） |
| `project_state` | 连通/权限结论（见下表） |
| `hint` | 人类可读说明或排障提示 |
| `project.name` / `project.lastAnalysis` | 仅 `ok` 时有：项目名、上次分析时间 |
| `qualityGate` | 仅 `ok` 且有权时：如 `OK` / `ERROR` |
| `configError` | `.sonarguard.json` 解析失败时的错误信息 |
| `hook` | 生效的 pre-commit 配置 |

| `project_state` | 含义 | 下一步 |
|-----------------|------|--------|
| `unreachable` | 缺 `hostUrl` 或 `projectKey`，或网络不可达 | 补 `.sonarguard.json` / properties；检查 VPN 与 URL |
| `no_auth` | 未配置 token | 设置 `SONAR_TOKEN` 或用户 `config.json` |
| `ok` | 服务器可达、项目存在 | 可跑 B1：`scan.py --scope full` |
| `not_found` | Sonar 上无此 projectKey（从未扫描） | 确认 key 正确；等 CI 首次扫描；暂用离线模式 |
| `no_permission` | token 无 Browse 权限 | 找 Sonar 管理员授权；暂用离线模式 |

**常见排障流程：**

1. `hostUrl: null` → 在目标仓库写 `.sonarguard.json` 的 `hostUrl`（或 properties / `SONAR_HOST_URL`）
2. `tokenConfigured: false` → 设置 `SONAR_TOKEN`
3. `project_state: ok` 后再跑 `scan.py --scope full`

### 可选环境变量

| 变量 | 作用 | 默认 |
|------|------|------|
| `SONAR_TOKEN` | 个人访问 token | — |
| `SONAR_HOST_URL` | 覆盖 hostUrl | — |
| `SONARGUARD_TIMEOUT` | API 超时（秒） | `5` |
| `SONARGUARD_MAX_ISSUE_PAGES` | B1 `--all` 最多拉取页数（每页 500 条） | `20` |

B1 结果若含 `"truncated": true`，提高 `SONARGUARD_MAX_ISSUE_PAGES` 后重跑。

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

### 输出格式与报告目录

`scan.py --format md|html|json`（默认 `md`），报告由脚本确定性生成，落盘到 `<repo>/.sonarguard/reports/<scope>-<时间戳>.<ext>`：

| format | 行为 |
|--------|------|
| `md`（默认） | 渲染 Markdown，打到 stdout（进对话框）并落盘 |
| `html` | 渲染 HTML，落盘并自动在浏览器打开（headless 时仅打印 `file://` 路径） |
| `json` | 透传底层 `sonar_api` 原始 JSON，供脚本 / 自动化消费 |

- `--top N`：调整 MAJOR 详情上限（默认 20）。
- 报告产物已在 install 时加入 `.gitignore`（`.sonarguard/reports/`）。
- 一键：Claude Code 里用 `/sonar-scan [full|staged|files]` 触发扫描并把报告显示在对话框，再由 SKILL 叠加修复建议。

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

## 架构

数据流（底层 JSON 契约 → 渲染 → 输出）：

```
sonar_api.py   SonarQube 开放 API 封装，输出 JSON（机器契约：钩子 import、外部脚本）
   │
scan.py        友好入口，--format md/html/json + 落盘 .sonarguard/reports/
   ├── render.py        零依赖渲染（md/html）+ 确定性截断（BLOCKER/CRITICAL 全列、MAJOR ≤20…）
   └── check_staged.py  pre-commit 钩子：彩色拦截/警告 + 服务器 3s 超时降级离线
   │
输出           对话框 Markdown · .sonarguard/reports/ 时间戳归档 · HTML 自动打开
```

- **报告事实由脚本确定性生成**（汇总表 + issue 清单 + 截断）；SKILL/AI 只在其上叠加「怎么修 + 风险 🟢🟡🔴」，不重复截断。
- `sonar_api.py` 永远输出 JSON，是 pre-commit 钩子与外部脚本依赖的机器契约。
- 一键入口 `/sonar-scan` 触发 `scan.py --format md` 并把报告渲染进对话框。
- 架构总览图见 [`doc/01-architecture.png`](../doc/01-architecture.png)。

## 支持语言

| 语言 | 服务器模式 | 离线启发式（高置信子集） |
|------|-----------|--------------------------|
| Java | ✅ | 空 catch、字符串 `==`、`System.out`、`printStackTrace`、硬编码密钥… |
| Python | ✅ | 裸 `except:`、`print` 调试残留… |
| JS/TS（含 Vue/React） | ✅ | `debugger`、`console.log`、`==`/`!=`… |
| Go | ✅ | 忽略 `err`、硬编码密钥… |

各语言修复方法与风险见 `claude-code/sonar-guard/references/rules-*.md`；离线启发式定义在 `scripts/check_staged.py`。

## 目录结构

```
sonar-guard/
├── README.md
├── references/workflow.md       三端共享工作流
├── scripts/
│   ├── sonar_api.py             Sonar API（status / issues --all / rules）→ JSON 契约
│   ├── check_staged.py          pre-commit 检查（彩色拦截/警告）
│   ├── scan.py                  full | staged | files，--format md/html/json
│   ├── render.py                零依赖 md/html 渲染 + 确定性截断
│   ├── install.py / uninstall.py   安装时写入目标仓库 .sonarguard/
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
