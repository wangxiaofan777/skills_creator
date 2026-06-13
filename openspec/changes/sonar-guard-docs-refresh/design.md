## Context

文档现状:root `README.md`(skills 总览索引)、`sonar-guard/README.md`(389 行详细文档)、`references/workflow.md` ×2、`SKILL.md`、`AGENTS.md`、cursor base 规则。上一轮 `sonar-guard-report-formats` 已把新功能补进 README/workflow/三端规则,但 README 是逐步堆叠而成,章节结构不够清晰,新读者难以快速建立全貌。`doc/` 下是黑客松提交物(文案 + 配图 + 出图脚本),无索引说明。

约束:本次为纯文档与仓库整理,不改任何脚本逻辑;保持三端文档不漂移(usage-docs 能力已规定 workflow/规则与 README 对齐)。

## Goals / Non-Goals

**Goals:**
- `sonar-guard/README.md` 成为结构完整、覆盖当前全部功能的唯一权威说明。
- root README 索引一句话与实际能力一致。
- `doc/` 有清晰索引,后人知道每个文件是什么、怎么重生成。
- 临时产物不进库。

**Non-Goals:**
- 不重写 SKILL/AGENTS/cursor 的语义(它们已对齐;仅在 README 变化时顺带校对引用)。
- 不新写独立用户手册(用户选择是「刷新补全主文档」,而非另起一份)。
- 不改脚本、不改 specs 之外的代码。

## Decisions

### D1. README 采用固定章节骨架
顺序:**简介 → 快速开始(装 + 扫)→ 配置(2 项)→ 使用(开发阶段 / 提交阶段 / 报告格式 / /sonar-scan)→ 架构 → 支持语言 → 排障 / FAQ**。
理由:让读者按「先跑起来,再了解细节」的路径阅读;现有内容大多已存在,主要是归位与补缺,而非推翻重写。

### D2. README 作为唯一权威,其它文档只做引用
workflow.md / SKILL / AGENTS / cursor 保持精简,涉及「在哪执行、配置、格式」等细节统一指向 README 对应章节,避免多处维护漂移(沿用 usage-docs 既有约束)。

### D3. doc/ 索引而非合并
`doc/` 保留现有文件,新增 `doc/README.md` 说明用途与 `python doc/_gen_images.py` 重生成方式;不把提交文案并入 sonar-guard 主文档(受众不同:一个是产品说明,一个是赛事提交)。

### D4. 仓库卫生最小改动
`.gitignore` 追加 `__pycache__/` 与 `*.pyc`;`.sonarguard/reports/` 已在上轮加入。不删历史已跟踪的 pyc(若有)——留给独立清理,以免本次文档 change 夹带代码层面的 git 操作。

## Risks / Trade-offs

- **README 刷新引入与三端文档的新漂移** → 刷新后按 usage-docs 场景自查:workflow/SKILL/AGENTS/cursor 对「格式、报告目录、/sonar-scan」的表述与 README 一致。
- **doc/ 提交物含示意数据,可能被误当真实结果** → 在 `doc/README.md` 标注报告样例为示意,建议用真实 Sonar 截图替换。
- **章节重排可能丢失原有细节(排障表等)** → 重排以「移动+补充」为原则,保留原有排障/字段表内容,不删减。

## Open Questions

- 是否需要英文版 README?当前默认仅中文,跟随现有文档语言。
