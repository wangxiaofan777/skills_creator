# sonar-guard-scan-workflow Specification

## Purpose

Shared scan workflows for Claude Code, Cursor, and Codex: B1 full-project issues, incremental file scan, report truncation, and optional scan.py aliases.

## Requirements

### Requirement: B1 full-project scan workflow

All three AI rule surfaces (Claude Code SKILL, Cursor base `.mdc`, Codex `AGENTS.md`) SHALL document the same full-project scan workflow using Sonar server unresolved issues.

#### Scenario: User requests full project scan

- **WHEN** the user asks to scan the entire repository for Sonar issues
- **AND** `sonar_api.py status --repo .` returns `project_state: ok`
- **THEN** the agent runs `python sonar-guard/scripts/sonar_api.py issues --repo . --all`
- **AND** produces a report titled with mode indicating server B1 full-project scan

#### Scenario: Project never scanned

- **WHEN** the user requests full project scan
- **AND** `status` returns `project_state: not_found`
- **THEN** the agent explains the project has no Sonar analysis yet
- **AND** falls back to offline rule subset for any incremental file review if requested

### Requirement: Incremental scan workflow preserved

The three AI rule surfaces SHALL document incremental scan using changed or staged files with `issues --files` and optional offline rule review for code not yet on the server.

#### Scenario: Session code change review

- **WHEN** the user completes code changes in the session
- **AND** server mode is available
- **THEN** the agent determines changed files via session context or `git diff`
- **AND** runs `issues --files` for those paths
- **AND** distinguishes "issues from last server scan" from "new code not yet on server"

### Requirement: Report truncation for large issue lists

Full-project reports SHALL always include complete severity summary counts. Detailed issue listings SHALL follow truncation rules to avoid overwhelming context.

#### Scenario: Large project issue set

- **WHEN** `issues --all` returns more than 50 issues
- **THEN** the report includes a summary table with counts per severity (BLOCKER, CRITICAL, MAJOR, MINOR, INFO)
- **AND** lists all BLOCKER and CRITICAL issues in detail
- **AND** lists at most 20 MAJOR issues in detail
- **AND** states MINOR and INFO counts without listing every item unless the user asks

### Requirement: Optional scan.py scope alias

The package MAY provide `sonar-guard/scripts/scan.py` mapping user-friendly scopes to underlying commands.

#### Scenario: Full scope alias

- **WHEN** the user runs `python sonar-guard/scripts/scan.py --repo . --scope full`
- **THEN** output is equivalent to `sonar_api.py issues --repo . --all`

#### Scenario: Staged scope alias

- **WHEN** the user runs `scan.py --repo . --scope staged`
- **THEN** behavior matches `check_staged.py --repo .` including exit codes for hook use

### Requirement: Shared workflow reference

The package SHALL maintain a shared workflow reference document under `sonar-guard/` that all three platforms cite or mirror, to prevent drift between Claude SKILL, Cursor rules, and Codex AGENTS.md.

#### Scenario: Workflow document exists

- **WHEN** a maintainer updates scan workflow steps
- **THEN** a single reference file (e.g. `sonar-guard/references/workflow.md`) defines status → issues → report steps
- **AND** platform-specific files point to or reproduce the same steps
