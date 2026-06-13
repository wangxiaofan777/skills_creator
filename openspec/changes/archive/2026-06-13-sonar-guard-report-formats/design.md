## Context

sonar-guard 现有数据流:`sonar_api.py`(底层,标准库,输出 JSON)← `scan.py`(友好 scope 别名,目前也只透传 JSON)← pre-commit 钩子 `check_staged.py`(直接 `import sonar_api` 调函数,输出彩色终端文本)。报告的可读形态当前完全由 AI(SKILL/Cursor/Codex 规则)在拿到 JSON 后临场拼装,既不可复现,也强制用户走 AI 才能得到友好结果。

关键约束:
- **零依赖红线**:全套脚本标榜"仅标准库、钩子零依赖",渲染不得引入 jinja2 等第三方库。
- **机器契约**:`check_staged.py` 通过 `import sonar_api` 调 `cmd_status()/cmd_issues()` 拿 dict,**不解析 scan.py 的 stdout**;外部自动化可能消费 scan.py 的 JSON。
- **多端一致**:Claude / Cursor / Codex 共享 `references/workflow.md`,文档需同步避免漂移。

## Goals / Non-Goals

**Goals:**
- scan.py 默认产出人类友好的 MD 报告,正文确定性、不依赖 AI。
- 支持 `md / html / json` 三种格式,报告可落盘到 `.sonarguard/reports/` 并带时间戳。
- `/sonar-scan` 在对话框一键触发,报告回显,SKILL 接力修复建议。
- 报告截断规则从 AI 下沉为脚本确定性实现。

**Non-Goals:**
- 不改 `sonar_api.py` 的 JSON 输出契约(底层保持纯 JSON)。
- 不改 pre-commit 钩子 `check_staged.py` 的彩色终端输出与退出码行为。
- 不引入任何第三方依赖。
- 不让脚本生成"修复建议/风险评估"——那仍是 SKILL(AI)的职责。

## Decisions

### D1. 渲染层放在 scan.py,sonar_api.py 保持纯 JSON
**选择**:只给 `scan.py` 加 `--format`;`sonar_api.py` 永远 JSON。
**理由**:`sonar_api.py` 是钩子 import 和外部脚本依赖的机器契约,松动它风险最高。scan.py 是面向人的友好别名,渲染天然属于这一层。
**备选**:两层都加渲染 → 否决,契约松动 + 双份维护。

### D2. 默认格式 = md(而非 json)
**选择**:`--format` 默认 `md`。
**理由**:经核实,改 scan.py 默认输出**不破坏任何内部消费者**——钩子 import 函数不读 stdout;LLM 原生可读 MD。人直接跑 scan.py 即得友好报告。
**备选**:默认 json(安全但不友好)、默认按 TTY 智能切换(优雅但隐式魔法、难推理)→ 均否决,显式默认 md 最直观。`--format json` 保留给外部自动化。

### D3. 报告事实由脚本生成,SKILL 只叠加建议
**分层**:
- scan.py 产出「哪里有问题」的事实:严重级汇总表 + issue 清单 + 截断。确定性、可复现。
- SKILL 在事实之上叠加「怎么修 + 风险 🟢🟡🔴 + 区分本次/存量 + 动手修」。需读 `references/rules-*.md` 与上下文推理。
**理由**:满足"脚本输出不依赖 AI",同时保留 SKILL 的真正价值(修复建议),两者互补不竞争。

### D4. 输出目录 `.sonarguard/reports/` + 时间戳
**选择**:报告落 `.sonarguard/reports/`,文件名 `<scope>-<YYYYMMDD-HHMM>.{md,html}`;`.gitignore` 追加 `.sonarguard/reports/`。
**理由**:`.sonarguard/` 已存在(自包含脚本),报告同处便于管理,一行 gitignore 即可。时间戳保留历史。
**输出行为**:`md` 同时打 stdout(进对话框)并落盘;`html` 仅落盘(终端无法阅读)。

### D5. HTML 自动在浏览器打开
**选择**:生成 HTML 后用 `webbrowser`(标准库)打开;非交互/无 DISPLAY 环境优雅降级为仅打印 `file://` 路径。
**理由**:零依赖且跨平台;CI/headless 不应阻塞。

### D6. staged scope 统一进 scan.py 渲染(方案 A)
**选择**:`scan.py --scope staged --format ...` 由 scan.py 自己渲染暂存区检查结果;pre-commit 钩子里的 `check_staged.py` 彩色输出与退出码**不变**。
**理由**:三个 scope 渲染一致;钩子的"快/拦截"职责与"出报告"职责分离。
**实现取向**:抽出暂存区检查的共用逻辑(取 staged files + server/local findings),scan.py 与 check_staged.py 复用,避免双份规则。

### D7. 截断规则下沉脚本
**选择**:汇总各严重级数量必全;详情 BLOCKER/CRITICAL 全列、MAJOR ≤20、MINOR/INFO 仅计数——由渲染层实现,可选 `--top N` 调节。
**理由**:确定性、人直接跑也得到规范报告;原 workflow.md §3 的"AI 执行截断"改为脚本执行。

### D8. 渲染实现位置
**选择**:新增 `scripts/lib/render.py`(stdlib only),提供 `to_markdown(result)` / `to_html(result)`;scan.py 按 `--format` 分发。HTML 用内联字符串模板,无第三方库。
**理由**:集中渲染逻辑,full/files/staged 共用。

### D9. /sonar-scan slash 命令
**选择**:`.claude/commands/sonar-scan.md`,内容指示 AI 运行 `.sonarguard/scan.py --scope <arg|full> --format md` 并回显报告,再按 SKILL 叠加建议。随 install 拷贝进业务仓库(纳入安装流程)。
**理由**:这是用户明确要的"命令方式触发、对话框看结果",比依赖 SKILL 描述匹配更确定。

## Risks / Trade-offs

- **默认翻成 md 影响外部脚本** → 提供 `--format json`;在文档/CHANGELOG 明确"默认变更",外部自动化显式加 `--format json`。
- **staged 逻辑抽取引入回归** → 共用逻辑提取后,以现有 `check_staged.py` 行为(退出码 0/1、彩色输出)为回归基线测试,确保钩子不变。
- **HTML 自动打开在 CI/headless 报错** → `webbrowser` 调用包裹异常,失败仅打印路径,不影响退出码。
- **截断下沉与 AI 报告重复截断** → SKILL 文档改为"在脚本报告上叠加",不再自行截断,避免双重逻辑。
- **`.sonarguard/reports/` 未入 gitignore 被误提交** → 安装/文档确保追加该行;报告文件名固定前缀便于忽略。

## Migration Plan

1. 加 `render.py` + scan.py `--format`(默认仍可先灰度为 json,联调通过后切 md)。
2. 抽取 staged 共用逻辑,scan.py 接入;回归钩子行为。
3. 加 `/sonar-scan` 命令与安装拷贝;追加 `.gitignore`。
4. 同步三端文档 + workflow.md;SKILL 改为"叠加建议"。
5. 回滚:`--format` 默认可改回 json;命令文件与 reports 目录可独立移除,不影响既有 JSON/钩子路径。

## Open Questions

- 报告历史是否需要清理策略(如只保留最近 N 份)?当前倾向不自动清理,留给用户。
- `/sonar-scan` 是否同时提供用户级安装(`~/.claude/commands/`)?当前倾向随 install 进项目级 `.claude/commands/`,跟仓库走、可共享。
