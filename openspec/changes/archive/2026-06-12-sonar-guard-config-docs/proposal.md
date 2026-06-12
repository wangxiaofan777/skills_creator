## Why

README 已说明「在哪执行」和扫描模式，但缺少可复制的配置示例、`status` 输出字段含义、配置合并优先级与常见 unreachable 排障。用户本地跑 `status` 看到 `hostUrl: null` 时无法自助完成配置。

## What Changes

- 在 `sonar-guard/README.md` 新增 **「配置参考」** 章节：最小/完整 `.sonarguard.json`、个人 token 两种写法、`sonar-project.properties` 替代、`hook` 可选字段
- 文档化配置合并优先级（仓库 → 用户 config → 环境变量）
- 文档化 `status` JSON 各字段含义与 `project_state` 枚举及排障步骤
- 文档化可选环境变量（`SONAR_TOKEN`、`SONAR_HOST_URL`、`SONARGUARD_TIMEOUT`、`SONARGUARD_MAX_ISSUE_PAGES`）
- 在 `references/workflow.md` 增加配置验证步骤链接/摘要（与 README 一致，不重复大段正文）

## Capabilities

### New Capabilities

- `sonar-guard-config-docs`: README 与 workflow 中的配置参考、status 输出说明与排障要求

### Modified Capabilities

（无：仅文档补充，不改变脚本行为或 API 契约）

## Impact

- `sonar-guard/README.md`
- `sonar-guard/references/workflow.md`（轻量交叉引用）
- 无脚本、安装器或 spec 行为变更
