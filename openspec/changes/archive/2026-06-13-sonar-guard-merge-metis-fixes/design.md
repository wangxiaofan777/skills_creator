## Context

sonar-guard 双向分叉:skills_creator 包有 render/`--format`/`/sonar-scan`/collect_findings;Metis 的 `.sonarguard/` 有三项独有改进(暂存 issue 查询修复、`pre-commit-entry.py`、健壮 hook 探测)。Metis 源已删除,但改动已从 Metis 的 `.git/hooks/sonarguard/sonar_api.py`(仍存,12679B,含修复)与本对话历史完整捕获:

- `cmd_issues` 新版(`_norm_repo_path`、`componentKeys`+`onComponentOnly`、`rel_set` 客户端过滤)—— 已逐行确认。
- `pre-commit-entry.py` —— 全文已读取捕获。
- `HOOK_SNIPPET`(`python→py→py -3→python3` + 调 `.sonarguard/pre-commit-entry.py`)—— 已捕获。

## Goals / Non-Goals

**Goals:**
- 把 Metis 三项改进回流进 skills_creator,消除分叉。
- 降低 pre-commit 对老仓库的误拦(精确 issue 匹配)。
- hook 在 Windows(含商店版 python3 占位)下稳定。

**Non-Goals:**
- 不回退本包已有的 report/`--format`/`/sonar-scan`。
- 不改 `cmd_issues_all`(已用 componentKeys)。
- 不触碰 Metis 仓库(其清理由用户负责)。
- 本提案不含「只拦本次新引入」的更大改动(可作后续 change)。

## Decisions

### D1. sonar_api.py 只合并 `cmd_issues` + `_norm_repo_path`
精确匹配:`componentKeys` + `onComponentOnly=true` 限定只查组件自身;返回后再用归一化路径在 `rel_set` 里过滤,剔除 Sonar 偶发的跨组件/路径变体命中。`cmd_issues_all` 维持原样。

### D2. hook 入口改用 pre-commit-entry.py(融入 install_lib,不新增并行安装器)
采用 Metis 的 `pre-commit-entry.py` 间接层 + 健壮探测 `HOOK_SNIPPET`,但**融进 skills_creator 既有的 `install_lib.hook_snippet()` / `copy_hook_scripts()`**,而**不**引入 Metis 的独立 `install_hook.py`(避免两套安装路径)。
- `pre-commit-entry.py` 加入 `HOOK_SCRIPT_NAMES` → 随安装拷贝到 `.sonarguard/` 与 `.git/hooks/sonarguard/`。
- `hook_snippet()` 调 `$REPO_ROOT/.sonarguard/pre-commit-entry.py`;entry 内部再从两处解析 `check_staged.py`。
**备选**:照搬 Metis `install_hook.py` 独立安装器 → 否决,会与 `install_lib` 重复维护两套 hook 安装逻辑。

### D3. 解释器探测顺序 `python → py → py -3 → python3`
逐个 `-c "import sys"` 验证可运行,跳过 Windows 商店版 `python3` 占位程序。比当前包里 `python`/`python3` 二选一更稳,且与上一轮 `hook_snippet` 修复同向但更全面。

### D4. 迁移来源以 `.git/hooks/sonarguard/sonar_api.py` 为准
Metis `.sonarguard/` 已删;实施时从 `D:\AI_Coding\metis\.git\hooks\sonarguard\sonar_api.py` 取 `cmd_issues`/`_norm_repo_path`(若届时也被删,则用本 design 与对话历史中已逐行记录的内容重建)。

## Risks / Trade-offs

- **Metis 源继续被删,实施时取不到** → 关键内容已逐行落在本对话/设计中,可纯靠记录重建;`pre-commit-entry.py` 全文亦已捕获。
- **精确过滤过严,漏掉真实 issue** → `onComponentOnly` 是 Sonar 官方参数,语义就是"仅该组件";过滤仅剔除路径不匹配的,属保守收紧;以真实 Metis 提交回归验证。
- **hook 入口改动影响已装仓库** → 仅影响重装后的仓库;`pre-commit-entry.py` 缺失时 entry/snippet 都有明确报错,不会静默。
- **与上轮 `hook_snippet` 手改冲突** → 本次以 D3 完整版覆盖,统一为一种探测逻辑。

## Migration Plan

1. 合并 `cmd_issues` + `_norm_repo_path` 进 `sonar_api.py`。
2. 新增 `pre-commit-entry.py`,加入 `HOOK_SCRIPT_NAMES`。
3. 重写 `hook_snippet()` 为 D3 版本(调 entry)。
4. 冒烟:临时 git 仓库装 hook,验证解释器探测 + entry 解析 + check_staged 调起。
5. 重装到系统/业务仓库并测试提交(本提案外)。

回滚:三处改动相互独立,可单独还原;不影响 report/`--format` 路径。

## Open Questions

- 是否同时做「pre-commit 只拦本次新引入、不拦存量」?倾向单开 change,本次先消除分叉 + 精确匹配。
