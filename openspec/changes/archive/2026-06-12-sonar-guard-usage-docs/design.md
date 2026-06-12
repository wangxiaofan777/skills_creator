## Context

`sonar-guard/README.md` 扫描命令使用 `--repo .`，隐含「在当前仓库根目录执行」，未说明：
- 安装命令在 **skills_creator 根目录** 跑，`--repo` 指向**目标业务仓库**
- 扫描命令的 **脚本路径** 在 `skills_creator/sonar-guard/scripts/`，`--repo` 指向**被扫项目**
- 业务仓库已装 hook 后，可用 `.git/hooks/sonarguard/sonar_api.py issues --all` 等价 B1

## Goals / Non-Goals

**Goals:**

- README 新增「在哪执行」：安装 / 扫描 / Agent 三场景，各给完整可复制命令
- workflow.md 与 README 内容一致，避免 drift
- AI 规则一句指向 README §在哪执行

**Non-Goals:**

- 修改 install 行为（例如把 scan.py 复制进 hook）
- 新增脚本或 CLI 参数

## Decisions

### 1. 文档结构：README 新增独立小节

**选择**：在「扫描模式」之前插入 **「在哪执行」**，用表格 + 3 个代码块（扫本仓库 / 扫业务仓库 / 业务仓库内 hook 等价）。

**备选**：只改 workflow.md — 用户先看 README，不够显眼。

### 2. `--repo` 术语统一

全文统一表述：**`--repo` = 要被 Sonar 检查配置的 git 仓库根**（读 `.sonarguard.json` 处），与 **当前 shell 工作目录** 可以不同。

### 3. 路径示例

使用 `<skills_creator>`、`<business-repo>` 占位符，禁止 `D:\` 等机器路径（符合仓库开发规则）。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 文档变长 | 小节控制在半屏；详细报告格式仍在 workflow.md |
| 用户无 skills_creator 克隆 | 说明需保留 skills_creator 或只用 hook 内 sonar_api |

## Migration Plan

纯文档更新，无迁移。改完即生效。

## Open Questions

（无）
