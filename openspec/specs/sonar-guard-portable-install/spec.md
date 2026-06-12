# sonar-guard-portable-install Specification

## Purpose

Machine-portable install onboarding using placeholders, environment setup scripts, and team documentation without hardcoded drive paths.

## Requirements

### Requirement: Documentation uses portable paths only

`sonar-guard/README.md` SHALL NOT use machine-specific absolute paths (e.g. `D:\skills_creator`) in primary install examples. It SHALL use placeholders `<skills_creator>` and `<business-repo>` and document a recommended install flow using relative paths after `cd <skills_creator>`.

#### Scenario: New developer on another machine

- **WHEN** a developer clones skills_creator to an arbitrary directory
- **THEN** README shows `python sonar-guard/scripts/install.py --repo <business-repo>` without requiring a specific drive letter

### Requirement: One-time environment setup script

The package SHALL provide `setup-env.ps1` and `setup-env.sh` that persist `packageRoot` to `~/.config/sonarguard/config.json` and instruct setting `SONARGUARD_HOME` for bootstrap installs from business repos.

#### Scenario: Developer configures package location once

- **WHEN** a developer runs setup-env with their local skills_creator clone path
- **THEN** subsequent `install_bootstrap.py` invocations resolve the package without hardcoded paths

### Requirement: Team onboarding documents optional committed CLI

README SHALL explain that `.sonarguard/` in a business repo may be committed so teammates can run scan commands after clone, while per-user install remains required for Cursor rules and pre-commit hooks.

#### Scenario: Teammate clones business repo with committed sonarguard CLI

- **WHEN** `.sonarguard/scan.py` exists in the business repository
- **THEN** README states the teammate can run scan after configuring token, without knowing skills_creator location
