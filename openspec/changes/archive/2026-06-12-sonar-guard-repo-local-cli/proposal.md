## Why

用户在业务仓库（如 `metis`）内直接复制 README 命令时全部失败：`sonar-guard/scripts/` 只存在于 skills_creator；`.git/hooks/sonarguard/` 仅在执行 `install.py --repo` 后才存在，且当前未复制 `scan.py`。文档把「从 skills_creator 扫别的仓库」放在前面，导致用户误以为在业务仓库 cwd 也能跑相同路径。

## What Changes

- 安装时在目标仓库创建 **`.sonarguard/`** 目录，复制 `sonar_api.py`、`check_staged.py`、`scan.py`（与 hook 目录同步刷新）
- hook 目录同样复制 `scan.py`，使 `issues --all` 与 `scan --scope full` 在 hook 路径均可跑
- 卸载时移除 `.sonarguard/`（若为本工具安装）
- README / workflow / post-install 提示改为：**先 install 一次 → 在业务仓库用 `.sonarguard/` 命令**
- 新增「命令跑不通」排障表（file not found 两类原因）

## Capabilities

### New Capabilities

- `sonar-guard-repo-local-cli`: 业务仓库内可发现的 CLI 入口与安装/卸载行为

### Modified Capabilities

- `sonar-guard-unified-install`: 安装产物扩展为 hook + `.sonarguard/` 双份脚本
- `sonar-guard-usage-docs`: 执行上下文文档以业务仓库命令为主路径

## Impact

- `sonar-guard/scripts/lib/install_lib.py`
- `sonar-guard/README.md`、`references/workflow.md`
- Cursor rule / Claude skill 中的命令示例（指向 `.sonarguard/` 优先）
