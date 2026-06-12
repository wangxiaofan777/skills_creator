## Context

`install.py` 与 `sonar-guard/` 目录绑定在 skills_creator 仓库。业务仓库用户复制 README 相对路径会得到 `[Errno 2] No such file or directory`。

## Goals / Non-Goals

**Goals:**

- 从 `D:\AI_Coding\metis` 一条命令完成 install（无需 cd skills_creator）
- 已 install 仓库可用 `python .sonarguard/install.py --repo .` 升级/重装
- PowerShell 示例用单行，不用 bash `\` 续行

**Non-Goals:**

- 不发布 pip 包
- 不把 skills_creator 整包复制进 metis

## Decisions

1. **bootstrap 脚本自包含（仅 stdlib）**  
   复制到 `.sonarguard/` 后仍可独立运行，不依赖 `lib/`。

2. **packageRoot 解析顺序**  
   `--package` > `SONARGUARD_HOME` > `config.json` 的 `packageRoot` > 交互输入并保存。

3. **install.py 成功结束时写入 packageRoot**  
   与 bootstrap 共用同一路径逻辑。

4. **README 安装首选：metis 内绝对路径 bootstrap**  
   ```powershell
   python D:\skills_creator\sonar-guard\scripts\install_bootstrap.py --platform all --repo . --host-url ... --project-key ...
   ```

## Risks / Trade-offs

- [packageRoot 移动后失效] → 文档说明用 `--package` 重指；bootstrap 交互可修复
