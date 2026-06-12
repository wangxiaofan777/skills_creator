## MODIFIED Requirements

### Requirement: Python one-click install for Cursor

The package SHALL provide Cursor installation via `sonar-guard/scripts/install.py --platform cursor` and MAY retain `install_cursor.py` as a backward-compatible wrapper. Both SHALL install sonar-guard for Cursor on Windows and macOS using only Python 3 standard library modules.

#### Scenario: Install from repository root

- **WHEN** the user runs `python sonar-guard/scripts/install_cursor.py --repo <git-repo>` OR `python sonar-guard/scripts/install.py --platform cursor --repo <git-repo>` from the `skills_creator` repository root
- **THEN** all six files from `sonar-guard/cursor/rules/` are copied to `{userHome}/.cursor/rules/`
- **AND** `<git-repo>/.sonarguard.json` is created if missing, or preserved if it already exists (unless `--force-config`)
- **AND** pre-commit hook scripts are installed under `<git-repo>/.git/hooks/sonarguard/` from `sonar-guard/scripts/` unless `--no-hook` is passed
- **AND** the script prints post-install hints for optional `SONAR_TOKEN` and project configuration
- **AND** the script exits with code 0

#### Scenario: Auto-fill project config from sonar-project.properties

- **WHEN** `--repo` points to a git repository that contains `sonar-project.properties` with `sonar.host.url` and `sonar.projectKey`
- **AND** `.sonarguard.json` does not yet exist
- **THEN** the installer writes `.sonarguard.json` containing `hostUrl` and `projectKey` parsed from that file

#### Scenario: Project config via CLI when no properties file

- **WHEN** `--repo` has no `sonar-project.properties`
- **AND** the user passes `--host-url` and `--project-key` to the unified installer
- **THEN** the installer writes `.sonarguard.json` with those values instead of `{}`

#### Scenario: Minimal config when no Sonar properties file and no CLI

- **WHEN** `--repo` has no `sonar-project.properties`, no CLI project args, and interactive input is skipped or empty
- **THEN** the installer writes `.sonarguard.json` as `{}` to enable offline review

#### Scenario: Missing rule source

- **WHEN** a required `.mdc` file is missing under `sonar-guard/cursor/rules/`
- **THEN** the installer writes a clear error to stderr
- **AND** exits with a non-zero code

### Requirement: Pre-commit hook is non-destructive

The installer SHALL append a marked `sonar-guard` snippet to an existing `pre-commit` hook rather than replacing unrelated hook logic.

#### Scenario: Refresh scripts when hook already present

- **WHEN** `pre-commit` already contains a `sonar-guard` block
- **THEN** the installer updates `check_staged.py` and `sonar_api.py` under `hooks/sonarguard/` from `sonar-guard/scripts/`
- **AND** replaces the marked block with the current snippet if its text changed

### Requirement: Minimal-configuration documentation

`sonar-guard/README.md` SHALL document that after install the user only needs optional personal `SONAR_TOKEN` and optional project `hostUrl`/`projectKey` when connecting to Sonar; all hook defaults SHALL be documented as automatic. Documentation SHALL NOT lead with Cursor-only quick start as the sole primary path.

#### Scenario: README quick start

- **WHEN** a user reads the Quick Start section
- **THEN** install commands cover all three platforms via `install.py --platform ...`
- **AND** a table lists the two configuration items (token + project) as required for server mode
- **AND** documents B1 full-project scan via `issues --all` or `scan.py --scope full`
- **AND** paths are relative to the repository root or use `~` (no machine-specific absolute paths)

## ADDED Requirements

### Requirement: Cursor rules support server mode

Cursor base rule `00-sonar-guard-base.mdc` SHALL instruct the agent to run `sonar-guard/scripts/sonar_api.py` for server connectivity and issue fetch when `.sonarguard.json` and credentials are configured, with offline fallback when server mode is unavailable.

#### Scenario: Server mode in Cursor after install

- **WHEN** the user has completed install and configured token and project
- **AND** starts a new Cursor Agent session in the repository
- **THEN** the base rule does not restrict the agent to offline-only mode
- **AND** full-project scan uses `issues --all` per the shared workflow
