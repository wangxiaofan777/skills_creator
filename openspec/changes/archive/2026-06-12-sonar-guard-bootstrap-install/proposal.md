## Why

用户在业务仓库（metis）内执行 `python sonar-guard/scripts/install.py` 必然失败——该路径只存在于 skills_creator。文档要求「先 cd skills_creator」但用户自然会在当前项目目录安装；PowerShell 多行 `\` 续行还会触发解析错误。

## What Changes

- 新增 **bootstrap 安装器** `install_bootstrap.py` / `uninstall_bootstrap.py`：任意 cwd 可运行，通过 `--package`、`SONARGUARD_HOME` 或 `~/.config/sonarguard/config.json` 的 `packageRoot` 定位 skills_creator
- 首次成功 install 后写入 `packageRoot`，后续从 metis 可直接 `python .sonarguard/install.py --repo .`
- install 时把 bootstrap 复制到 `.sonarguard/install.py` 与 `uninstall.py`
- README 重写安装章节：**metis 内三条可复制命令**（绝对路径 / bootstrap / 已安装后重装）

## Capabilities

### New Capabilities

- `sonar-guard-bootstrap-install`: 跨目录 bootstrap 安装与 packageRoot 持久化

### Modified Capabilities

- `sonar-guard-unified-install`: 安装产物含 `.sonarguard/install.py`
- `sonar-guard-usage-docs`: 文档明确 install 不可在业务仓库用相对路径 `sonar-guard/scripts/`

## Impact

- `sonar-guard/scripts/install_bootstrap.py`、`uninstall_bootstrap.py`
- `install_lib.py`、`install.py`
- `sonar-guard/README.md`
