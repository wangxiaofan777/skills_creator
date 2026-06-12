## Context

`sonar-guard/README.md` 已有「你只需要配 2 样」摘要和「在哪执行」，但用户反馈无法从 README 自助完成配置：缺少可复制 JSON 示例、`status` 字段解释、合并优先级与 unreachable 排障。实现逻辑已在 `sonar_api.py` 的 `load_config()` / `cmd_status()` 中稳定，本次仅补文档。

## Goals / Non-Goals

**Goals:**

- README 新增自包含的「配置参考」：最小配置、完整可选字段、个人 token、properties 替代
- 用表格说明 `status` 输出字段与 `project_state` 含义及下一步操作
- 说明配置合并顺序与环境变量
- `workflow.md` §4 改为指向 README 配置章节（保留一行摘要）

**Non-Goals:**

- 不改 `load_config()` 行为、不新增 CLI 子命令
- 不写 Sonar 管理员手册（权限申请流程仅一句指引）
- 不重复「在哪执行」大段内容

## Decisions

1. **配置章节放在「在哪执行」之后、「扫描模式」之前**  
   用户先知道在哪跑命令，再查怎么配；配好后用 `status` 验证，再跑 B1。

2. **示例 hostUrl 用占位符 `https://sonar.example.com`**  
   避免绑定公司内部域名；与现有 install 示例一致。

3. **`status` 字段表与 `cmd_status()` 一一对应**  
   文档来源以代码为准，包含 `ok` / `no_auth` / `unreachable` / `not_found` / `no_permission` 及 ApiError kind。

4. **合并优先级单独小节**  
   顺序：`.sonarguard.json` + `sonar-project.properties`（projectKey/hostUrl 互补）→ `~/.config/sonarguard/config.json` → 环境变量（`SONAR_TOKEN`、`SONAR_HOST_URL` 覆盖 token/hostUrl）。

5. **workflow.md 轻量更新**  
   §4 保留两行摘要 + 链接 README §配置参考；§1 增加「字段含义见 README」一句，避免双份维护。

## Risks / Trade-offs

- [文档与代码 drift] → 字段表注明「以 `sonar_api.py load_config/cmd_status` 为准」；变更配置逻辑时同步 README
- [README 变长] → 用折叠式小节（最小配置 / 高级 hook / 排障）保持可扫读
