## ADDED Requirements

### Requirement: README is a complete authoritative guide with a defined structure

`sonar-guard/README.md` SHALL serve as the single authoritative guide and SHALL be organized into a clear, ordered section structure: 简介 / 快速开始 / 配置 / 使用 / 架构 / 支持语言 / 排障·FAQ. It SHALL cover the current full feature set, including the two-stage check, `--format md|html|json`, the `.sonarguard/reports/` timestamped output, HTML auto-open, the `/sonar-scan` command, the render layer, offline fallback, and supported languages.

#### Scenario: New reader builds a full picture

- **WHEN** a new reader opens `sonar-guard/README.md`
- **THEN** they find an ordered structure (简介 → 快速开始 → 配置 → 使用 → 架构 → 支持语言 → 排障/FAQ)
- **AND** each shipped feature (两阶段检查、报告多格式、报告目录、/sonar-scan、离线 fallback、支持语言) is documented or linked from the relevant section

#### Scenario: Detail lives in README, others reference it

- **WHEN** `workflow.md`, SKILL, AGENTS, or the cursor base rule needs to mention execution context, configuration, or output formats
- **THEN** it stays concise and points to the corresponding README section
- **AND** no shipped feature is described only outside README

### Requirement: Root README index stays aligned with sonar-guard capabilities

The repository root `README.md` index entry for sonar-guard SHALL reflect the current capabilities, including multi-format reports and the one-click `/sonar-scan` command.

#### Scenario: Index one-liner matches reality

- **WHEN** a user reads the sonar-guard row in the root `README.md` skills 一览
- **THEN** the one-line positioning mentions multi-format report output and/or the one-click scan command
- **AND** the "详细文档" link points to `sonar-guard/README.md`

### Requirement: doc/ submission materials carry an index

The `doc/` directory SHALL contain a `doc/README.md` index that explains each submission artifact (`submission.md`, the generated images, the image generator script) and how to regenerate the images.

#### Scenario: Maintainer opens doc/

- **WHEN** a maintainer opens the `doc/` directory
- **THEN** `doc/README.md` lists each file with its purpose
- **AND** it documents regenerating images via `python doc/_gen_images.py`
- **AND** it notes the report-sample image uses illustrative data that can be replaced with a real Sonar screenshot
