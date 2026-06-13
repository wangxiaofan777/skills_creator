## Why

sonar-guard 在业务仓库 Metis 里被并行开发,产生了 skills_creator 包所没有的三项改进:更精确的暂存文件 issue 查询、健壮的跨平台 pre-commit 入口、更稳的 Python 解释器探测。这违背「skills_creator 管 SKILL、业务仓库只消费」的原则,也让两边分叉。要把这些改进回流到 skills_creator(唯一权威源),消除分叉,并顺带缓解「老仓库提交被存量 issue 误拦」的问题。

> 注:Metis 侧 `.sonarguard/` 源文件在本次梳理中已被删除;改动内容已从 Metis 的 `.git/hooks/sonarguard/sonar_api.py` 与本对话历史中完整恢复,迁移不依赖 Metis 仓库继续存在。

## What Changes

- **`sonar_api.py` 暂存 issue 查询修复**:`cmd_issues()` 改用 `componentKeys` + `onComponentOnly=true`,并新增 `_norm_repo_path()` 对返回 issue 的文件路径做归一化后**客户端过滤**(`rel_set`),只保留确属被查文件自身的 issue。修掉旧版 `components=<路径>` 在 Windows 反斜杠 / `./` 前缀下匹配偏宽、导致 pre-commit 误拦的问题。`cmd_issues_all()` 不变。
- **新增 `pre-commit-entry.py`**:跨平台、Windows-safe 的 hook 入口,用 `sys.executable` 调起 `check_staged.py`,并能从 `.git/hooks/sonarguard/` 或 `.sonarguard/` 解析脚本位置。纳入 `HOOK_SCRIPT_NAMES`,随安装拷贝到两处。
- **健壮的 hook 解释器探测**:`install_lib.hook_snippet()` 改为 `python → py → py -3 → python3`(逐个验证可运行)并调用 `.sonarguard/pre-commit-entry.py`,替换当前仅 `python/python3` 二选一的写法。彻底解决 Windows 商店版 `python3` 占位程序导致钩子静默失败的问题。

## Capabilities

### New Capabilities
<!-- 无全新能力;均为现有能力的修复/增强 -->

### Modified Capabilities
- `sonar-guard-api`: `cmd_issues` 暂存/指定文件 issue 查询改为精确匹配(componentKeys + onComponentOnly + 路径归一客户端过滤)。
- `sonar-guard-bootstrap-install`: pre-commit hook 改用 `pre-commit-entry.py` 入口 + 健壮多解释器探测,跨平台/Windows-safe。

## Impact

- **脚本**:`sonar-guard/scripts/sonar_api.py`(cmd_issues + 新增 `_norm_repo_path`);新增 `sonar-guard/scripts/pre-commit-entry.py`;`lib/install_lib.py`(`HOOK_SCRIPT_NAMES` 加 entry、`hook_snippet()` 重写)。
- **行为**:pre-commit 误拦减少;Windows 解释器探测更稳;`sonar_api.py` 的 JSON 契约与 `--all` 路径不变。
- **不改**:report 渲染/`--format`/`/sonar-scan`(本包已有,不回退);不触碰 Metis 仓库。
- **后续**:合并后用更新版重装到系统并测试提交(本提案外的运行步骤)。
