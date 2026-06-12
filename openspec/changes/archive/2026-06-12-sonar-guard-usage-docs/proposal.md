## Why

`sonar-guard-unified-platform` 落地后，README 与 workflow 已列出安装、配置与 `scan.py` 命令，但未明确说明 **脚本在哪执行、`--repo` 指向哪个仓库、扫业务仓库时的完整示例**。用户反复困惑「`scan.py --scope full` 在哪跑」，需在文档中单独成节并三端引用一致。

## What Changes

- 在 `sonar-guard/README.md` 新增 **「在哪执行」** 小节：安装 vs 扫描的执行目录、`--repo` 语义、本仓库/业务仓库/Cursor Agent 三种场景
- 补充业务仓库内 hook 等价命令（`sonar_api.py issues --all`，因 hook 不复制 `scan.py`）
- 同步更新 `references/workflow.md`、Claude `references/workflow.md`
- 在 Cursor 基础规则与 Codex `AGENTS.md` 中增加一句执行上下文（指向 README 或 workflow）
- 根 `README.md` sonar-guard 一行描述无需大改（可选微调）

## Capabilities

### New Capabilities

- `sonar-guard-usage-docs`: 执行上下文与扫描命令的使用说明文档要求（安装目录、扫描目录、`--repo`、等价命令、Agent 触发）

### Modified Capabilities

- （无）仅文档与 AI 规则引用，不改变脚本行为

## Impact

- `sonar-guard/README.md`
- `sonar-guard/references/workflow.md`
- `sonar-guard/claude-code/sonar-guard/references/workflow.md`
- `sonar-guard/cursor/rules/00-sonar-guard-base.mdc`
- `sonar-guard/codex/AGENTS.md`
