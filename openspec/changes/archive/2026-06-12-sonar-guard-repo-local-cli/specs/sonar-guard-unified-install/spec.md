## MODIFIED Requirements

### Requirement: Pre-commit hook installs self-contained scripts

The unified installer SHALL copy `check_staged.py`, `sonar_api.py`, and `scan.py` into `.git/hooks/sonarguard/` for the target repository and SHALL append or update a marked pre-commit snippet without overwriting unrelated hook content.

#### Scenario: Hook directory is self-contained

- **WHEN** install completes with hook enabled for a git repository
- **THEN** `.git/hooks/sonarguard/` contains `check_staged.py`, `sonar_api.py`, and `scan.py`
- **AND** pre-commit invokes `check_staged.py` with `--repo` set to the repository root

#### Scenario: Reinstall refreshes hook scripts

- **WHEN** install runs again on the same repository
- **THEN** hook scripts are overwritten with the current package versions
