## Decisions

1. **默认推荐：cd skills_creator + 相对路径**  
   任意 clone 位置均可用，文档不出现盘符。

2. **SONARGUARD_HOME 为本机一次配置**  
   写入用户环境变量 + config.json；bootstrap 从 metis 内 install 时用 `$env:SONARGUARD_HOME\...`。

3. **团队 scan 与 per-user install 分离**  
   `.sonarguard/` 脚本可进 git；Cursor 规则、pre-commit 仍 per-user install。

4. **setup-env 脚本**  
   交互输入 clone 路径，校验 `sonar-guard/scripts/install.py` 存在后持久化。

## Non-Goals

- pip 分发、自动 git clone skills_creator
