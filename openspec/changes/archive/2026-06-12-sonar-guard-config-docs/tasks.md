## 1. README 配置参考

- [x] 1.1 在 `sonar-guard/README.md` 新增 **配置参考**（位于「在哪执行」与「扫描模式」之间）
- [x] 1.2 写入最小/完整 `.sonarguard.json` 示例与个人 token 两种配置方式
- [x] 1.3 写入 `sonar-project.properties` 替代、`hook` 可选字段及默认值
- [x] 1.4 写入配置合并优先级小节
- [x] 1.5 写入 `status` 输出字段表、`project_state` 含义与排障步骤
- [x] 1.6 写入可选环境变量 `SONARGUARD_TIMEOUT`、`SONARGUARD_MAX_ISSUE_PAGES`

## 2. Workflow 交叉引用

- [x] 2.1 更新 `sonar-guard/references/workflow.md` §4 指向 README 配置参考；§1 增加 status 字段详见 README

## 3. 验证

- [x] 3.1 对照 `sonar_api.py` 的 `load_config()` / `cmd_status()` 核对文档字段与默认值一致
