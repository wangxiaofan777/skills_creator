# sonar-guard-api Specification

## Purpose

Platform-agnostic SonarQube API scripts (`status`, `rules`, `issues --files`, `issues --all`, `rule`) and configuration merge for sonar-guard.

## Requirements

### Requirement: Canonical scripts under sonar-guard/scripts

The package SHALL maintain `sonar_api.py` and `check_staged.py` as canonical sources under `sonar-guard/scripts/`. Pre-commit installation and documentation SHALL reference this path as the single source of truth.

#### Scenario: Hook install copies canonical scripts

- **WHEN** the unified or Cursor installer installs pre-commit hooks for a repository
- **THEN** it copies `sonar_api.py` and `check_staged.py` from `sonar-guard/scripts/` into `<repo>/.git/hooks/sonarguard/`

### Requirement: Issues command supports full project scan

`sonar_api.py` SHALL support fetching all unresolved issues for the configured project via `issues --all`, in addition to the existing per-file `issues --files` mode.

#### Scenario: Full project issues with valid config

- **WHEN** the user runs `python sonar-guard/scripts/sonar_api.py issues --repo <repo> --all`
- **AND** `status` would return `project_state: ok`
- **THEN** the command queries Sonar `/api/issues/search` with `componentKeys=<projectKey>` and `resolved=false`
- **AND** paginates until all issues are retrieved or a configurable page limit is reached
- **AND** prints JSON to stdout with `total`, `bySeverity`, and `issues` array (each issue includes `rule`, `severity`, `message`, `file`, `line`, `status`)

#### Scenario: Files mode unchanged

- **WHEN** the user runs `issues --repo <repo> --files path/to/File.java`
- **THEN** behavior matches the existing per-component batch query
- **AND** `--all` and `--files` are mutually exclusive

#### Scenario: Missing project config

- **WHEN** the user runs `issues --all` without `projectKey` configured
- **THEN** the command outputs JSON with an `error` field describing missing configuration
- **AND** exits with a non-zero code

### Requirement: Configuration merge unchanged in semantics

`load_config()` SHALL continue merging, in order: repository `.sonarguard.json`, `sonar-project.properties`, `~/.config/sonarguard/config.json`, and environment variables `SONAR_TOKEN` / `SONAR_HOST_URL`. Token SHALL NOT be read from `.sonarguard.json`.

#### Scenario: Token from environment only

- **WHEN** `.sonarguard.json` contains `hostUrl` and `projectKey` but no token field
- **AND** `SONAR_TOKEN` is set in the environment
- **THEN** API calls authenticate successfully without storing token in the repository

### Requirement: Stdlib-only Python 3

All scripts under `sonar-guard/scripts/` SHALL use only Python 3 standard library modules.

#### Scenario: No pip dependencies

- **WHEN** a user runs any sonar-guard script on a machine with Python 3 and no extra packages
- **THEN** the script runs without import errors from third-party modules
