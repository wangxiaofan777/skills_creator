## ADDED Requirements

### Requirement: Bootstrap install runs from any working directory

The package SHALL provide `install_bootstrap.py` that locates the skills_creator package root and delegates to `sonar-guard/scripts/install.py`, resolving the root via `--package`, environment variable `SONARGUARD_HOME`, or persisted `packageRoot` in `~/.config/sonarguard/config.json`.

#### Scenario: User installs from metis without cd skills_creator

- **WHEN** a user runs `python <absolute-path>/install_bootstrap.py --platform all --repo .` from a business repository root
- **THEN** installation completes and creates `.sonarguard/` in that repository
- **AND** `packageRoot` is saved to user config for subsequent runs

#### Scenario: User reinstalls from business repo after first install

- **WHEN** `.sonarguard/install.py` exists from a prior installation
- **THEN** `python .sonarguard/install.py --platform all --repo .` delegates to the canonical installer without requiring skills_creator-relative paths

### Requirement: Bootstrap uninstall mirrors install

The package SHALL provide `uninstall_bootstrap.py` and copy it to `.sonarguard/uninstall.py` with the same package-root resolution behavior.

#### Scenario: Uninstall from business repo

- **WHEN** a user runs `python .sonarguard/uninstall.py --repo .`
- **THEN** sonar-guard is removed from that repository using the resolved package root
