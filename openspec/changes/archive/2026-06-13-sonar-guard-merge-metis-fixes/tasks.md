## 1. 合并 sonar_api.py 暂存 issue 查询修复

- [x] 1.1 新增 `_norm_repo_path(path)`(反斜杠→正斜杠、去 `./` 前缀)
- [x] 1.2 重写 `cmd_issues()`:`componentKeys` + `onComponentOnly=true`,返回后用 `_norm_repo_path` 在 `rel_set` 中客户端过滤;`cmd_issues_all()` 不动
- [x] 1.3 从 `D:\AI_Coding\metis\.git\hooks\sonarguard\sonar_api.py` 比对核实(若已删则按 design 记录重建)

## 2. 新增跨平台 hook 入口

- [x] 2.1 新增 `sonar-guard/scripts/pre-commit-entry.py`(sys.executable 调 check_staged;从 .git/hooks/sonarguard/ 或 .sonarguard/ 解析;缺失报错非零)
- [x] 2.2 `lib/install_lib.py` 的 `HOOK_SCRIPT_NAMES` 加入 `pre-commit-entry.py`

## 3. 健壮 hook 解释器探测

- [x] 3.1 重写 `install_lib.hook_snippet()`:`python → py → py -3 → python3`(逐个验证)+ 调 `$REPO_ROOT/.sonarguard/pre-commit-entry.py`;缺 entry 明确报错
- [x] 3.2 确认 `install_pre_commit_hook()` / `install_repo_cli()` 会把 entry 拷到两处(依赖 HOOK_SCRIPT_NAMES)

## 4. 验证

- [x] 4.1 临时 git 仓库装 hook:验证解释器探测跳过商店版 python3、entry 解析、check_staged 调起、退出码正确
- [x] 4.2 确认 report/`--format`/`/sonar-scan` 路径未受影响(scan staged md/json 冒烟)
- [x] 4.3 `openspec validate sonar-guard-merge-metis-fixes` 通过

## 5. 更新到系统(apply 后的运行步骤)

- [x] 5.1 用合并后的版本重装到 skills_creator 自身(刷新 .sonarguard/ 与 .git/hooks)
- [x] 5.2 提醒用户:如需在业务仓库生效,重跑 install;测试一次真实提交确认不再误拦/不再静默失败
