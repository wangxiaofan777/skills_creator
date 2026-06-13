# sonar-guard-report-render Specification

## Purpose
TBD - created by archiving change sonar-guard-report-formats. Update Purpose after archive.
## Requirements
### Requirement: scan.py supports md/html/json output formats

`sonar-guard/scripts/scan.py` SHALL accept a `--format` option with values `md`, `html`, and `json`, defaulting to `md`. Rendering SHALL use only the Python standard library (no third-party dependencies).

#### Scenario: Default markdown output

- **WHEN** the user runs `scan.py --repo . --scope full` without `--format`
- **THEN** scan.py renders a human-readable Markdown report to stdout
- **AND** the report includes a per-severity summary table (BLOCKER, CRITICAL, MAJOR, MINOR, INFO) with counts

#### Scenario: Explicit JSON for automation

- **WHEN** the user runs `scan.py --repo . --scope full --format json`
- **THEN** scan.py prints the same JSON structure that the underlying `sonar_api.py` produces
- **AND** no Markdown or HTML decoration is added

#### Scenario: Unsupported format value

- **WHEN** the user passes `--format xml`
- **THEN** scan.py rejects the value and exits non-zero with a clear message listing valid formats

### Requirement: Report files are written to a timestamped reports directory

When producing `md` or `html` output, scan.py SHALL write the report to `<repo>/.sonarguard/reports/` using the filename pattern `<scope>-<YYYYMMDD-HHMM>.<ext>`. The `md` format SHALL additionally be printed to stdout; the `html` format SHALL NOT be printed to stdout.

#### Scenario: Markdown report written and echoed

- **WHEN** the user runs `scan.py --repo . --scope full --format md`
- **THEN** a file `.sonarguard/reports/full-<timestamp>.md` is created
- **AND** the same Markdown is printed to stdout
- **AND** the absolute path of the written file is reported to the user

#### Scenario: HTML report written but not echoed

- **WHEN** the user runs `scan.py --repo . --scope files --files src/Foo.java --format html`
- **THEN** a file `.sonarguard/reports/files-<timestamp>.html` is created
- **AND** the HTML content is not dumped to stdout
- **AND** the reports directory is created if it does not exist

#### Scenario: Reports directory is git-ignored

- **WHEN** scan.py writes any report under `.sonarguard/reports/`
- **THEN** the package documents adding `.sonarguard/reports/` to `.gitignore` so report artifacts are not committed

### Requirement: HTML reports open in the browser automatically

When the format is `html`, scan.py SHALL attempt to open the generated file in the default browser via the standard library `webbrowser` module, degrading gracefully in non-interactive or headless environments.

#### Scenario: Interactive desktop run

- **WHEN** scan.py generates an HTML report in an environment with a usable browser
- **THEN** the report opens in the default browser
- **AND** the file path is still printed for reference

#### Scenario: Headless or CI environment

- **WHEN** scan.py generates an HTML report but no browser can be opened
- **THEN** scan.py prints the `file://` path instead of failing
- **AND** the process exit code is unaffected by the open attempt

### Requirement: Deterministic report truncation in the renderer

The Markdown and HTML renderers SHALL apply truncation deterministically: the severity summary counts SHALL always be complete; detailed listings SHALL include all BLOCKER and CRITICAL issues, at most 20 MAJOR issues, and counts only for MINOR and INFO. A `--top N` option MAY override the per-severity detail cap.

#### Scenario: Large issue set rendered

- **WHEN** a full-project result contains more than 50 issues
- **THEN** the rendered report shows complete per-severity counts
- **AND** lists every BLOCKER and CRITICAL issue in detail
- **AND** lists at most 20 MAJOR issues in detail
- **AND** states MINOR and INFO as counts without listing each item

#### Scenario: Detail cap overridden

- **WHEN** the user passes `--top 50`
- **THEN** the renderer lists up to 50 MAJOR issues in detail instead of the default 20

