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

