## ADDED Requirements

### Requirement: Cross-platform Node install script

The package SHALL provide `link-works-whiten-automation/scripts/install-cursor-skill.mjs` that installs the Cursor user skill on Windows and macOS using only Node.js built-in modules (`fs`, `path`, `os`).

#### Scenario: Install from repository root on Windows

- **WHEN** the user runs `node link-works-whiten-automation/scripts/install-cursor-skill.mjs` from the `skills_creator` repository root on Windows
- **THEN** the file `cursor/skills/link-works-whiten-automation/SKILL.md` is copied to `{userHome}/.cursor/skills/link-works-whiten-automation/SKILL.md`
- **AND** the script prints the destination path and exits with code 0

#### Scenario: Install from repository root on macOS

- **WHEN** the user runs the same `node` command from the repository root on macOS
- **THEN** the skill is copied to `~/.cursor/skills/link-works-whiten-automation/SKILL.md`
- **AND** the script exits with code 0

#### Scenario: Missing source skill

- **WHEN** the source `SKILL.md` does not exist relative to the package root
- **THEN** the script writes a clear error message to stderr
- **AND** exits with a non-zero code

### Requirement: No PowerShell install script

The package SHALL NOT ship `install-cursor-skill.ps1` after this change; the Node script is the sole automated installer.

#### Scenario: PowerShell installer removed

- **WHEN** a consumer looks for install automation under `link-works-whiten-automation/scripts/`
- **THEN** only `install-cursor-skill.mjs` is provided for Cursor skill installation

### Requirement: Portable documentation

Installation and canonical-source documentation SHALL use paths relative to the `skills_creator` repository root or the `~` home-directory prefix. Documentation MUST NOT include machine-specific absolute paths (e.g. `D:\skills_creator`).

#### Scenario: README install section

- **WHEN** a user reads `link-works-whiten-automation/README.md`
- **THEN** the install command uses a relative path to `install-cursor-skill.mjs`
- **AND** the destination is documented as `~/.cursor/skills/link-works-whiten-automation/SKILL.md`
- **AND** no Metis wrapper script or `SKILLS_CREATOR_ROOT` default is documented

#### Scenario: SKILL canonical sources

- **WHEN** a user reads the Canonical sources section in any of the three platform SKILL files
- **THEN** the install instruction references `node link-works-whiten-automation/scripts/install-cursor-skill.mjs` from the `skills_creator` root
- **AND** no `D:\` or Metis-specific install paths appear

### Requirement: Repository-wide OS platform rule

The root `skills_creator/README.md` development rules SHALL state that install scripts and documentation examples must support Windows and macOS, and must not use machine-specific absolute paths.

#### Scenario: Root README development rules

- **WHEN** a contributor reads the development rules in the root README
- **THEN** OS dual-platform support and the no-absolute-path rule are explicitly stated

### Requirement: Decentralized script map wording

Agent SKILL files SHALL describe whitening scripts as living in the target git repository's `scripts/` directory, without naming Metis as the distribution source for the install flow.

#### Scenario: Script map section title and scope

- **WHEN** a user reads the script map in Cursor, Claude Code, or Codex SKILL files
- **THEN** the section describes scripts expected in the target repository (e.g. `scripts/link-works-whiten-all.ps1`)
- **AND** does not instruct users to install the Cursor skill via Metis
