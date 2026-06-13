## ADDED Requirements

### Requirement: Cross-platform pre-commit entry script

The package SHALL ship `pre-commit-entry.py` and include it in the hook scripts copied into both `.sonarguard/` and `.git/hooks/sonarguard/`. The installed pre-commit hook SHALL invoke `.sonarguard/pre-commit-entry.py`, which resolves `check_staged.py` from `.git/hooks/sonarguard/` or `.sonarguard/` and runs it via the current Python interpreter.

#### Scenario: Entry runs the staged check

- **WHEN** a commit triggers the pre-commit hook in an installed repo
- **THEN** the hook calls `.sonarguard/pre-commit-entry.py`
- **AND** the entry resolves and runs `check_staged.py` against the repo root

#### Scenario: Entry missing is reported, not silent

- **WHEN** `.sonarguard/pre-commit-entry.py` is absent
- **THEN** the hook prints a clear error to stderr and exits non-zero (no silent failure)

### Requirement: Robust Python interpreter detection in the hook

The pre-commit hook snippet SHALL detect a working interpreter in the order `python`, `py`, `py -3`, `python3`, verifying each can actually run before use, so that a non-functional `python3` shim (e.g. the Windows Store alias) does not cause the hook to fail silently.

#### Scenario: Windows Store python3 shim is skipped

- **WHEN** `python3` resolves to a non-functional shim but `python` works
- **THEN** the hook selects `python`
- **AND** the staged check runs normally rather than aborting the commit with no output
