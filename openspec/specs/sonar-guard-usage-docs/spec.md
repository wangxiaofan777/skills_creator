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

`sonar-guard/references/workflow.md` and `claude-code/sonar-guard/references/workflow.md` SHALL document the same execution-context rules as README, including hook equivalent for B1.

#### Scenario: Workflow mentions hook path

- **WHEN** a maintainer reads `references/workflow.md`
- **THEN** B1 full scan documents both `scan.py --scope full` and hook-local `sonar_api.py issues --all`

### Requirement: AI rules point to execution documentation

Cursor base rule and Codex `AGENTS.md` SHALL reference the README execution-context section (or workflow) so agents run commands with correct `--repo` and script paths.

#### Scenario: Cursor agent full-project scan

- **WHEN** a Cursor agent performs B1 full-project scan per base rule
- **THEN** instructions indicate using `python .sonarguard/scan.py --repo . --scope full` when installed, or skills_creator/bootstrap paths otherwise
- **AND** `--repo` is set to the opened project root
