## MODIFIED Requirements

### Requirement: Report truncation for large issue lists

Full-project reports SHALL always include complete severity summary counts. Detailed issue listings SHALL follow truncation rules to avoid overwhelming context. These truncation rules SHALL be implemented deterministically by the `scan.py` renderer (see `sonar-guard-report-render`), not performed ad hoc by the agent at report-writing time.

#### Scenario: Large project issue set

- **WHEN** `issues --all` returns more than 50 issues
- **THEN** the report includes a summary table with counts per severity (BLOCKER, CRITICAL, MAJOR, MINOR, INFO)
- **AND** lists all BLOCKER and CRITICAL issues in detail
- **AND** lists at most 20 MAJOR issues in detail
- **AND** states MINOR and INFO counts without listing every item unless the user asks

#### Scenario: Truncation is produced by the script

- **WHEN** a user runs `scan.py --scope full` directly (without an agent)
- **THEN** the rendered report already applies the truncation rules
- **AND** the agent does not need to re-truncate when surfacing the report

### Requirement: Optional scan.py scope alias

The package SHALL provide `sonar-guard/scripts/scan.py` mapping user-friendly scopes to underlying commands, and scan.py SHALL render results in the format selected by `--format` (default `md`) for all scopes.

#### Scenario: Full scope alias

- **WHEN** the user runs `python sonar-guard/scripts/scan.py --repo . --scope full`
- **THEN** the underlying data is equivalent to `sonar_api.py issues --repo . --all`
- **AND** the result is rendered in the selected format (default Markdown)

#### Scenario: Staged scope alias renders via scan.py

- **WHEN** the user runs `scan.py --repo . --scope staged --format md`
- **THEN** scan.py performs the staged-area check and renders a Markdown report
- **AND** the pre-commit hook's `check_staged.py` colored terminal output and exit codes remain unchanged
- **AND** staged-check logic is shared between `scan.py` and `check_staged.py` to avoid divergence

#### Scenario: Files scope alias

- **WHEN** the user runs `scan.py --repo . --scope files --files src/Foo.java`
- **THEN** scan.py queries those files' issues and renders them in the selected format
