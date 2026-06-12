## 1. Python 安装脚本

- [x] 1.1 实现 `sonar-guard/scripts/lib/cursor_install_lib.py`（rules 复制、manifest、`.sonarguard.json`、pre-commit 标记块）
- [x] 1.2 实现 `sonar-guard/scripts/install_cursor.py`（`--repo`、`--no-hook`、`--force-config`）
- [x] 1.3 实现 `sonar-guard/scripts/uninstall_cursor.py`（`--repo`、`--purge-config`）
- [x] 1.4 确认已删除 Node 安装脚本（`install-cursor.mjs`、`uninstall-cursor.mjs`、`cursor-install-lib.mjs`）

## 2. 文档

- [x] 2.1 重写 `sonar-guard/README.md`：Quick Start 用 Python 命令；「装完只配什么」表；目录结构更新
- [x] 2.2 更新根 `README.md` 中 `sonar-guard/scripts/` 条目
- [x] 2.3 全文检索无残留 `install-cursor.mjs` / Node 安装说明

## 3. 验证（Windows）

- [x] 3.1 在 `skills_creator` 根目录执行 `python sonar-guard/scripts/install_cursor.py --repo .`，确认 6 条 rules、`.sonarguard.json`、pre-commit 钩子
- [x] 3.2 执行 `python sonar-guard/scripts/uninstall_cursor.py --repo .` 后再安装，确认装/卸循环正常
- [x] 3.3 执行 `python .git/hooks/sonarguard/check_staged.py --repo .`（无暂存变更时 exit 0）

## 4. 归档准备

- [x] 4.1 运行 `openspec validate sonar-guard-cursor-install` 确认 change 有效（CLI 无 `verify` 子命令）
- [ ] 4.2 按需 `openspec archive sonar-guard-cursor-install` 合并 spec 并归档
