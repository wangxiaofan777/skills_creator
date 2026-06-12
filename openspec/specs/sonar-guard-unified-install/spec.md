# sonar-guard-unified-install Specification

## Purpose

Unified one-click install and uninstall for sonar-guard across Claude Code, Cursor, and Codex, with project config collection and pre-commit hooks.

## Requirements

### Requirement: Unified install script for all platforms

The package SHALL provide `sonar-guard/scripts/install.py` accepting `--platform cursor|claude|codex|all` and `--repo <git-repo>`.

#### Scenario: Install all platforms

- **WHEN** the user runs `python sonar-guard/scripts/install.py --platform all --repo <git-repo>` from the skills_creator root
- **THEN** Cursor rules are installed to `{userHome}/.cursor/rules/`
- **AND** Claude Code skill is copied to `{userHome}/.claude/skills/sonar-guard/`
- **AND** pre-commit hooks are installed under `<git-repo>/.git/hooks/sonarguard/` unless `--no-hook`
- **AND** `.sonarguard.json` is created or preserved per existing rules
- **AND** the script exits with code 0

#### Scenario: Install single platform

- **WHEN** the user runs `install.py --platform cursor --repo <git-repo>`
- **THEN** only Cursor rules and optional hook steps run
- **AND** Claude and Codex paths are not modified

### Requirement: Project config collection without sonar-project.properties

When `--repo` has no `sonar-project.properties` and no existing `.sonarguard.json` with both `hostUrl` and `projectKey`, the installer SHALL accept project info via CLI or interactive prompt.

#### Scenario: CLI provides project info

- **WHEN** the user runs `install.py --repo <repo> --host-url https://sonar.example.com --project-key my-project`
- **THEN** `.sonarguard.json` is written with those values

#### Scenario: Interactive prompt on TTY

- **WHEN** no project info is available from properties or CLI
- **AND** stdin is a TTY
- **THEN** the installer prompts for `hostUrl` and `projectKey`
- **AND** empty answers result in `{}` for offline use

#### Scenario: Non-interactive fallback

- **WHEN** no project info is available and stdin is not a TTY
- **THEN** the installer writes `.sonarguard.json` as `{}`
- **AND** prints a hint to set `hostUrl` and `projectKey` later

### Requirement: Unified uninstall script

The package SHALL provide `sonar-guard/scripts/uninstall.py` with `--platform cursor|claude|codex|all` and `--repo <git-repo>`.

#### Scenario: Uninstall all

- **WHEN** the user runs `uninstall.py --platform all --repo <git-repo>`
- **THEN** Cursor rules from the install manifest are removed
- **AND** `{userHome}/.claude/skills/sonar-guard/` is removed if present
- **AND** pre-commit sonar-guard block and `hooks/sonarguard/` are removed
- **AND** `.sonarguard.json` is kept unless `--purge-config`

### Requirement: Backward-compatible Cursor entry points

`install_cursor.py` and `uninstall_cursor.py` SHALL remain as thin wrappers delegating to the unified install/uninstall with `--platform cursor`.

#### Scenario: Existing Cursor install command still works

- **WHEN** the user runs `python sonar-guard/scripts/install_cursor.py --repo <repo>`
- **THEN** behavior is equivalent to `install.py --platform cursor --repo <repo>`

### Requirement: Cross-platform documentation

`sonar-guard/README.md` SHALL present Claude Code, Cursor, and Codex with equal prominence (not Cursor-first), document the two required configuration items (`SONAR_TOKEN` and project `hostUrl`/`projectKey`), and use repository-relative or `~` paths only.

#### Scenario: Three-platform install table

- **WHEN** a user reads the install section
- **THEN** they see install commands for all three platforms referencing `install.py --platform ...`
- **AND** a capability comparison table shows server-mode issue fetch for all three after configuration
