## MODIFIED Requirements

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
- **THEN** install commands are documented as run from `<skills_creator>` root exactly once per business repo
- **AND** scan commands clarify that after install, scripts live under `.sonarguard/` in the business repo
