## 1. 安装器

- [x] 1.1 `install_pre_commit_hook` 复制 `scan.py` 到 hook 目录
- [x] 1.2 新增 `install_repo_cli`：同步复制三脚本到 `.sonarguard/` 并写 marker
- [x] 1.3 `uninstall_pre_commit_hook` 删除 `.sonarguard/`（有 marker 时）
- [x] 1.4 `print_post_install_hints` 输出业务仓库 `.sonarguard/` 命令

## 2. 文档与规则

- [x] 2.1 README「快速开始」+ 排障表；`.sonarguard/` 为主路径
- [x] 2.2 更新 `references/workflow.md`、Cursor base rule 命令示例

## 3. 验证

- [x] 3.1 对 skills_creator 自身 `--repo .` 跑 install 后验证 `.sonarguard/` 命令
