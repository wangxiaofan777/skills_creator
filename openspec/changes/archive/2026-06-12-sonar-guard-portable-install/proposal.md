## Why

README 与示例大量使用 `D:\skills_creator`、`D:\AI_Coding\metis` 等本机绝对路径，换电脑或开放给其他开发者无法直接复制。需要机器无关的安装/onboarding 流程。

## What Changes

- README 改用占位符 `<skills_creator>`、`<business-repo>`，**推荐方式 A** 为 clone 后 `cd skills_creator` 相对路径 install（零硬编码）
- 新增 `setup-env.ps1` / `setup-env.sh`：一次配置 `SONARGUARD_HOME` + `~/.config/sonarguard/config.json` 的 `packageRoot`
- 文档说明团队场景：业务仓库 `.sonarguard/` 可提交 git，成员 clone 后可直接 scan；install 仍各机器一次（hook/Cursor）
- bootstrap 错误提示指向 setup-env 与方式 A

## Capabilities

### New Capabilities

- `sonar-guard-portable-install`: 跨机器安装 onboarding 与 env 配置

### Modified Capabilities

- `sonar-guard-usage-docs`: 文档禁止硬编码盘符路径，优先相对路径与 env

## Impact

- `sonar-guard/README.md`
- `sonar-guard/scripts/setup-env.ps1`、`setup-env.sh`
- `install_bootstrap.py` 提示文案
