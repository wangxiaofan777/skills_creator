## Why

sonar-guard 经过多轮迭代(报告格式、输出目录、`/sonar-scan` 命令等),功能已超出原说明文档覆盖范围,`README.md` 缺一份结构完整、可作为唯一权威入口的说明;同时黑客松提交物散落在 `doc/`,需要一并整理归档,避免后人看不懂这些文件是什么。

## What Changes

- **把 `sonar-guard/README.md` 刷新为权威主文档**:补全到当前完整功能集(两阶段检查、`--format md/html/json`、`.sonarguard/reports/` 时间戳归档、HTML 自动打开、`/sonar-scan` 命令、render 渲染层、离线 fallback、支持语言),并约定清晰的章节结构(简介 → 快速开始 → 配置 → 使用 → 架构 → 排障 → FAQ)。
- **对齐 root `README.md` 索引**:更新 sonar-guard 一句话定位,反映新能力(报告多格式 + 一键命令)。
- **整理 `doc/` 提交物**:新增 `doc/README.md` 索引,说明各文件(submission.md、四张配图、出图脚本)用途与重生成方式。
- **收口忽略项**:确保 `.gitignore` 覆盖临时产物(`__pycache__/`、`*.pyc`、`.sonarguard/reports/`),避免噪声进库。
- 上一个 change `sonar-guard-report-formats` 已在本轮归档(specs 已落库),不在本提案的实现任务内。

## Capabilities

### New Capabilities
<!-- 无新增能力;均为现有文档能力的完善 -->

### Modified Capabilities
- `sonar-guard-usage-docs`: 新增「README 为结构完整的权威说明」与「root README 索引保持对齐」「doc/ 提交物带索引说明」三条文档要求。

## Impact

- **文档**:`sonar-guard/README.md`(主体刷新)、root `README.md`(索引一句话)、新增 `doc/README.md`。
- **仓库卫生**:`.gitignore` 追加 `__pycache__/`、`*.pyc`(`.sonarguard/reports/` 已在上轮加入)。
- **不改代码行为**:纯文档与仓库整理,不触碰 `scripts/` 下任何脚本逻辑。
