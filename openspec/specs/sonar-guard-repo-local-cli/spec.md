# sonar-guard-repo-local-cli Specification

## Purpose

Repository-local CLI entry points under `.sonarguard/` so business-repo developers can run scan and status without skills_creator-relative paths.

## Requirements

### Requirement: Install creates repo-local CLI directory

When `install.py` runs for a target repository, it SHALL copy `sonar_api.py`, `check_staged.py`, and `scan.py` into both `.git/hooks/sonarguard/` and a repository-root `.sonarguard/` directory, copy bootstrap scripts as `.sonarguard/install.py` and `.sonarguard/uninstall.py`, and SHALL write `.sonarguard/.installed-by-sonar-guard` to mark managed installs.

#### Scenario: User runs scan from business repo after install

- **WHEN** a user has run `install.py --repo <business-repo>` and `cd` into that repository
- **THEN** `python .sonarguard/scan.py --repo . --scope full` executes successfully without referencing skills_creator paths
- **AND** `python .sonarguard/sonar_api.py status --repo .` executes successfully

#### Scenario: Reinstall refreshes repo-local scripts

- **WHEN** install runs again on the same repository
- **THEN** files in `.sonarguard/` and `.git/hooks/sonarguard/` are overwritten with current package scripts

### Requirement: Uninstall removes repo-local CLI directory

`uninstall.py` SHALL remove `.sonarguard/` when it contains `.installed-by-sonar-guard`, in addition to removing hook scripts.

#### Scenario: Clean uninstall

- **WHEN** a user runs `uninstall.py --repo <business-repo>`
- **THEN** `.sonarguard/` managed by sonar-guard is removed
- **AND** `.git/hooks/sonarguard/` is removed

### Requirement: Documentation prioritizes business-repo commands

`sonar-guard/README.md` SHALL document a two-step flow: install once from skills_creator, then run commands from `.sonarguard/` inside the business repository, and SHALL include a troubleshooting table for `No such file or directory` when using wrong script paths.

#### Scenario: User in business repo without install

- **WHEN** a user reads README after failed commands in a business repo
- **THEN** they find that `sonar-guard/scripts/` paths require running from skills_creator OR installing first
- **AND** they find the exact install command with `--repo` pointing to their business repo
