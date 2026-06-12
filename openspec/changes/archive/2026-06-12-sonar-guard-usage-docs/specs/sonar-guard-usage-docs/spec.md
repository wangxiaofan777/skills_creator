## ADDED Requirements

### Requirement: README documents execution context for install and scan

`sonar-guard/README.md` SHALL include a dedicated section explaining where to run install vs scan commands, what `--repo` means, and at least three scenarios: scan current repo, scan a business repo from skills_creator, and B1 equivalent via installed hook scripts.

#### Scenario: User reads where to run full scan

- **WHEN** a user opens `sonar-guard/README.md` looking for `scan.py --scope full`
- **THEN** they find a section that states `--repo` is the git repo whose `.sonarguard.json` is used
- **AND** examples show running `scan.py` from `<skills_creator>` with `--repo` pointing to the target project
- **AND** an example shows `python .git/hooks/sonarguard/sonar_api.py issues --repo . --all` inside an installed business repo

#### Scenario: Install execution context is distinct from scan

- **WHEN** a user reads the install section and the execution-context section
- **THEN** install commands are documented as run from `<skills_creator>` root
- **AND** scan commands clarify that the script lives under `sonar-guard/scripts/` while `--repo` may refer to another repository

### Requirement: Workflow reference stays aligned with README

`sonar-guard/references/workflow.md` and `claude-code/sonar-guard/references/workflow.md` SHALL document the same execution-context rules as README, including hook equivalent for B1.

#### Scenario: Workflow mentions hook path

- **WHEN** a maintainer reads `references/workflow.md`
- **THEN** B1 full scan documents both `scan.py --scope full` and hook-local `sonar_api.py issues --all`

### Requirement: AI rules point to execution documentation

Cursor base rule and Codex `AGENTS.md` SHALL reference the README execution-context section (or workflow) so agents run commands with correct `--repo` and script paths.

#### Scenario: Cursor agent full-project scan

- **WHEN** a Cursor agent performs B1 full-project scan per base rule
- **THEN** instructions indicate resolving `scan.py` from skills_creator or `sonar_api.py issues --all` from the target repo hook directory
- **AND** `--repo` is set to the opened project root
