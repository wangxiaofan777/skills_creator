# sonar-guard-usage-docs Specification

## Purpose

Documentation requirements for where to run install vs scan commands, `--repo` semantics, and hook-equivalent B1 commands.
## Requirements
### Requirement: README documents execution context for install and scan

`sonar-guard/README.md` SHALL include a dedicated section explaining where to run install vs scan commands, what `--repo` means, and at least three scenarios: scan current repo, scan a business repo from skills_creator, and B1 equivalent via installed hook scripts.

#### Scenario: User reads where to run full scan

- **WHEN** a user opens `sonar-guard/README.md` looking for `scan.py --scope full`
- **THEN** they find a section that states `--repo` is the git repo whose `.sonarguard.json` is used
- **AND** the primary example shows `python .sonarguard/scan.py --repo . --scope full` from an installed business repository
- **AND** examples show running `scan.py` from `<skills_creator>` with `--repo` pointing to the target project when install has not been run
- **AND** an example shows `python .git/hooks/sonarguard/sonar_api.py issues --repo . --all` inside an installed business repo

#### Scenario: Install execution context is distinct from scan

- **WHEN** a user reads the install section and the execution-context section
- **THEN** install commands are documented as run from `<skills_creator>` or via bootstrap/setup-env without hardcoded drive paths
- **AND** scan commands clarify that after install, scripts live under `.sonarguard/` in the business repo

### Requirement: Workflow reference stays aligned with README

`sonar-guard/references/workflow.md` and `claude-code/sonar-guard/references/workflow.md` SHALL document the same execution-context rules as README, including hook equivalent for B1, the `--format` output options, the `.sonarguard/reports/` location, and that report facts are produced deterministically by `scan.py` while the SKILL only layers fix guidance on top.

#### Scenario: Workflow mentions hook path

- **WHEN** a maintainer reads `references/workflow.md`
- **THEN** B1 full scan documents both `scan.py --scope full` and hook-local `sonar_api.py issues --all`

#### Scenario: Workflow describes format and report ownership

- **WHEN** a maintainer reads the report section of `references/workflow.md`
- **THEN** it states scan.py renders `md`/`html`/`json` and owns truncation
- **AND** it states the SKILL augments the script report with remediation and risk, rather than generating the report itself

### Requirement: AI rules point to execution documentation

Cursor base rule and Codex `AGENTS.md` SHALL reference the README execution-context section (or workflow) so agents run commands with correct `--repo` and script paths.

#### Scenario: Cursor agent full-project scan

- **WHEN** a Cursor agent performs B1 full-project scan per base rule
- **THEN** instructions indicate using `python .sonarguard/scan.py --repo . --scope full` when installed, or skills_creator/bootstrap paths otherwise
- **AND** `--repo` is set to the opened project root

### Requirement: Docs cover output formats and the reports directory

`sonar-guard/README.md` and `references/workflow.md` SHALL document the `--format md|html|json` option (default `md`), the `.sonarguard/reports/` output location with timestamped filenames, HTML auto-open behavior, and the need to add `.sonarguard/reports/` to `.gitignore`.

#### Scenario: User looks up how to get a friendly report

- **WHEN** a user reads the docs for producing a readable scan report
- **THEN** they find that `scan.py` defaults to Markdown and writes to `.sonarguard/reports/<scope>-<timestamp>.md`
- **AND** that `--format html` additionally opens the report in a browser
- **AND** that `--format json` is available for automation

### Requirement: Docs cover the /sonar-scan command

The three AI rule surfaces (Claude SKILL, Cursor base rule, Codex `AGENTS.md`) and the README SHALL document the `/sonar-scan [full|staged|files]` command as the in-conversation way to run a scan without typing shell commands.

#### Scenario: User wants a one-click scan in chat

- **WHEN** a user reads how to trigger a scan from the conversation
- **THEN** they find `/sonar-scan` documented with its optional scope argument
- **AND** the docs state the report is rendered into the conversation and then augmented with fix guidance

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

