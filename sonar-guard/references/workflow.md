# Sonar Guard — 共享扫描工作流

三端（Claude Code / Cursor / Codex）共用。详细 **在哪执行、--repo 含义** 见 `sonar-guard/README.md` §在哪执行。

## 0. 执行上下文（摘要）

- **安装（一次）**：在 `<skills_creator>` 跑 `install.py --repo <业务仓库>`。
- **扫描（日常）**：在**业务仓库**根目录跑 `python .sonarguard/scan.py --repo . --scope full`（install 后）。
- **未 install**：从 skills_creator 跑 `sonar-guard/scripts/scan.py --repo <业务仓库>`。
- **hook 等价**：`.git/hooks/sonarguard/` 与 `.sonarguard/` 脚本相同。

详细排障见 `sonar-guard/README.md` §**快速开始**。

## 1. 探测项目状态（每次检查第一步）

```bash
python sonar-guard/scripts/sonar_api.py status --repo <目标仓库路径>
# install 后在业务仓库内:
python .sonarguard/sonar_api.py status --repo .
```

| project_state | 策略 |
|---|---|
| `ok` | 服务器模式 |
| `not_found` / `no_permission` / `no_auth` / `unreachable` | 离线模式 + 说明原因 |

各字段含义、`hint` 与排障步骤见 `sonar-guard/README.md` §**配置参考**。

## 2. 扫描模式

### B1 全项目（Sonar 服务器存量 issue）

```bash
# 业务仓库内（install 后，推荐）
python .sonarguard/scan.py --repo . --scope full

# 从 skills_creator 扫任意已配置仓库
python sonar-guard/scripts/scan.py --repo <目标仓库路径> --scope full

# hook 路径（可选，与 .sonarguard 同脚本）
python .git/hooks/sonarguard/scan.py --repo . --scope full
```

前提：项目已被 Sonar CI/扫描器分析过至少一次。

### 增量（变更文件）

```bash
python sonar-guard/scripts/scan.py --repo <目标仓库> --scope files --files src/a/Foo.java
```

### 提交前（pre-commit，仅暂存区）

```bash
python sonar-guard/scripts/scan.py --repo <目标仓库> --scope staged
```

## 3. 报告格式

### 全项目 B1 报告

- 汇总: 各严重级数量必全
- 详情: BLOCKER/CRITICAL 全列; MAJOR 最多 20 条; MINOR/INFO 仅计数

### 增量报告

区分「服务器存量 issue」与「本次新代码（需对照 rules 审查）」。

## 4. 配置（仅 2 项）

1. **个人**：`SONAR_TOKEN` 或 `~/.config/sonarguard/config.json`
2. **项目**：`.sonarguard.json` 的 `hostUrl` + `projectKey`（或 `sonar-project.properties`）

完整示例、合并优先级、`status` 字段表与环境变量 → **`sonar-guard/README.md` §配置参考**。

## 5. 离线 fallback

服务器不可用时，按各语言 references / 规则卡片审查，报告标题注明「模式: 离线」。
