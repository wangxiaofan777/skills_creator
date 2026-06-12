## ADDED Requirements

### Requirement: Python one-click install for Cursor

The package SHALL provide `sonar-guard/scripts/install_cursor.py` that installs sonar-guard for Cursor on Windows and macOS using only Python 3 standard library modules.

#### Scenario: Install from repository root

- **WHEN** the user runs `python sonar-guard/scripts/install_cursor.py --repo <git-repo>` from the `skills_creator` repository root
- **THEN** all six files from `sonar-guard/cursor/rules/` are copied to `{userHome}/.cursor/rules/`
- **AND** `<git-repo>/.sonarguard.json` is created if missing, or preserved if it already exists (unless `--force-config`)
- **AND** pre-commit hook scripts are installed under `<git-repo>/.git/hooks/sonarguard/` unless `--no-hook` is passed
- **AND** the script prints post-install hints for optional `SONAR_TOKEN` and project configuration
- **AND** the script exits with code 0

#### Scenario: Auto-fill project config from sonar-project.properties

- **WHEN** `--repo` points to a git repository that contains `sonar-project.properties` with `sonar.host.url` and `sonar.projectKey`
- **AND** `.sonarguard.json` does not yet exist
- **THEN** the installer writes `.sonarguard.json` containing `hostUrl` and `projectKey` parsed from that file

#### Scenario: Minimal config when no Sonar properties file

- **WHEN** `--repo` has no `sonar-project.properties` and no existing `.sonarguard.json`
- **THEN** the installer writes `.sonarguard.json` as `{}` (empty object) to enable offline Cursor review

#### Scenario: Missing rule source

- **WHEN** a required `.mdc` file is missing under `sonar-guard/cursor/rules/`
- **THEN** the installer writes a clear error to stderr
- **AND** exits with a non-zero code

### Requirement: Python one-click uninstall for Cursor

The package SHALL provide `sonar-guard/scripts/uninstall_cursor.py` that reverses the Cursor install and optional repository hook setup.

#### Scenario: Uninstall rules and hook

- **WHEN** the user runs `python sonar-guard/scripts/uninstall_cursor.py --repo <git-repo>`
- **THEN** sonar-guard rule files installed via the manifest are removed from `{userHome}/.cursor/rules/`
- **AND** the `sonar-guard` block is removed from `<git-repo>/.git/hooks/pre-commit` if present
- **AND** `<git-repo>/.git/hooks/sonarguard/` is deleted
- **AND** `.sonarguard.json` is kept unless `--purge-config` is passed
- **AND** the script exits with code 0

### Requirement: Install manifest for clean uninstall

The installer SHALL record installed rule file names and target directory in `{userHome}/.config/sonarguard/cursor-install.json` and the uninstaller SHALL use that manifest when removing rules.

#### Scenario: Manifest written on install

- **WHEN** install completes successfully
- **THEN** `cursor-install.json` lists the six rule basenames and `rulesDir`
- **AND** includes an ISO-8601 `installedAt` timestamp

#### Scenario: Uninstall without manifest falls back to defaults

- **WHEN** `cursor-install.json` is missing
- **THEN** the uninstaller removes the six known default rule filenames from `{userHome}/.cursor/rules/`

### Requirement: Pre-commit hook is non-destructive

The installer SHALL append a marked `sonar-guard` snippet to an existing `pre-commit` hook rather than replacing unrelated hook logic.

#### Scenario: Append to existing pre-commit

- **WHEN** `<git-repo>/.git/hooks/pre-commit` exists and does not yet contain `sonar-guard`
- **THEN** the installer appends a block delimited by `# >>> sonar-guard >>>` and `# <<< sonar-guard <<<`
- **AND** preserves existing hook content

#### Scenario: Refresh scripts when hook already present

- **WHEN** `pre-commit` already contains a `sonar-guard` block
- **THEN** the installer updates `check_staged.py` and `sonar_api.py` under `hooks/sonarguard/`
- **AND** replaces the marked block with the current snippet if its text changed

### Requirement: No Node.js install scripts

The package SHALL NOT ship Node.js-based Cursor install scripts; `install_cursor.py` and `uninstall_cursor.py` are the sole automated installers.

#### Scenario: Node installers absent

- **WHEN** a consumer looks under `sonar-guard/scripts/` for install automation
- **THEN** only `install_cursor.py` and `uninstall_cursor.py` are provided (plus `lib/cursor_install_lib.py`)

### Requirement: Minimal-configuration documentation

`sonar-guard/README.md` SHALL document that after one-click install the user only needs optional personal `SONAR_TOKEN` and optional project `hostUrl`/`projectKey` when connecting to Sonar; all hook defaults SHALL be documented as automatic.

#### Scenario: README quick start

- **WHEN** a user reads the Quick Start section
- **THEN** the primary install command uses `python sonar-guard/scripts/install_cursor.py --repo <path>`
- **AND** a table or section lists required vs optional configuration
- **AND** states that `{}` in `.sonarguard.json` is sufficient for offline use
- **AND** paths are relative to the repository root or use `~` (no machine-specific absolute paths)

#### Scenario: Root README index

- **WHEN** a user reads the root `skills_creator/README.md` directory structure
- **THEN** `sonar-guard/scripts/install_cursor.py` is listed under the sonar-guard package
