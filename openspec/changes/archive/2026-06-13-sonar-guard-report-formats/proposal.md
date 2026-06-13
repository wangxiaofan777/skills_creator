## Why

sonar-guard 当前所有扫描结果只有 JSON 一种输出,人直接看很不友好,而且报告的可读形态依赖 AI 临场拼装、不可复现。用户需要脚本本身就能产出确定性的、便于查看和分享的报告(MD/HTML),并且能在对话框里一键触发,而不是每次手敲 shell 命令。

## What Changes

- **scan.py 新增 `--format {md,html,json}`,默认 `md`**:报告正文由脚本确定性生成(含严重级汇总、issue 清单、截断规则),不再依赖 AI 拼装。
- **底层 `sonar_api.py` 保持纯 JSON 输出不变**:它是机器契约(pre-commit 钩子 `import` 调用、外部脚本消费),不引入渲染。
- **报告落盘到 `.sonarguard/reports/`**,文件名带时间戳(如 `full-20260613-1430.md` / `.html`);`md` 同时打到 stdout 进对话框;`html` 落盘后自动在浏览器打开。
- **三个 scope 统一支持渲染**:`full` / `files` / `staged` 都能 `--format md/html/json`。其中 `staged` 改为也走 scan.py 渲染(原 `check_staged.py` 在 pre-commit 钩子里的彩色终端输出保持不变)。
- **截断规则下沉脚本**:原本由 AI 在写报告时执行的截断(BLOCKER/CRITICAL 全列、MAJOR ≤20、MINOR/INFO 仅计数)改为脚本确定性实现。
- **新增 `/sonar-scan [full|staged|files]` slash 命令**(`.claude/commands/`):一键触发 scan.py 并把 MD 报告贴进对话框,SKILL 随后叠加修复建议。
- **SKILL 职责收敛**:不再负责生成报告事实,改为在脚本报告之上叠加「怎么修 + 风险等级 + 实际修复」。
- `.gitignore` 追加 `.sonarguard/reports/`,报告产物不进版本库。

## Capabilities

### New Capabilities
- `sonar-guard-report-render`: scan.py 的报告渲染能力——`--format md/html/json`、默认 md、落盘到 `.sonarguard/reports/`、时间戳命名、HTML 自动打开、零依赖渲染、确定性截断规则。
- `sonar-guard-scan-command`: `/sonar-scan` slash 命令——在对话框一键调用 scan.py 并回显 MD 报告,支持 `full|staged|files` 参数。

### Modified Capabilities
- `sonar-guard-scan-workflow`: scan.py 增加 `--format` 与输出目录语义;`staged` scope 统一走 scan.py 渲染;报告截断规则从「AI 执行」改为「脚本执行」。
- `sonar-guard-usage-docs`: 三端文档(SKILL / Cursor / Codex)与 workflow.md 更新输出格式、报告目录、`/sonar-scan` 命令用法,并说明 SKILL 由「生成报告」收敛为「叠加修复建议」。

## Impact

- **脚本**:`sonar-guard/scripts/scan.py`(新增 format 分发与落盘/打开);新增渲染模块(如 `scripts/lib/render.py`,stdlib only);`check_staged.py` 钩子彩色输出不变。
- **命令**:新增 `.claude/commands/sonar-scan.md`(及安装时拷贝逻辑,如纳入 install)。
- **文档**:`SKILL.md`、`cursor/rules/00-sonar-guard-base.mdc`、`codex/AGENTS.md`、`references/workflow.md`、`README.md`。
- **配置/产物**:业务仓库 `.sonarguard/reports/` 目录、`.gitignore` 一行。
- **约束**:维持零依赖(MD/HTML 均用标准库字符串渲染,不引入 jinja2 等);`sonar_api.py` JSON 契约与 pre-commit 钩子行为不回归。
