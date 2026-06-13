# link-works-skill-install

## Purpose

Cross-platform installation of the Link Works whiten automation Cursor user skill from the `skills_creator` repository, with portable documentation conventions.
## Requirements
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

### Requirement: Package ships whitening execution scripts

The package SHALL ship the Link Works whitening execution scripts under `link-works-whiten-automation/scripts/` as the canonical source, including `link-works-whiten-all.ps1`, `link-works-pre-commit-whiten.ps1`, `link-works-invoke-run-commands.ps1`, `install-link-works-pre-commit-hook.ps1`, `link-works-whiten-all-keybinding.snippet.json`, and `scripts/lib/link-works-stats.mjs` with its test `link-works-stats.test.mjs`.

#### Scenario: Execution scripts present in package

- **WHEN** a user inspects `link-works-whiten-automation/scripts/`
- **THEN** all six execution artifacts and `scripts/lib/link-works-stats.mjs` (+ its test) are present
- **AND** they are the authoritative source, no longer assumed to be supplied by a separate target repository

#### Scenario: Stats unit test passes

- **WHEN** a maintainer runs `node link-works-whiten-automation/scripts/lib/link-works-stats.test.mjs`
- **THEN** the test passes with no Metis-specific fixture paths

### Requirement: Node distribution installer copies scripts into a target repo

The package SHALL provide `link-works-whiten-automation/scripts/install-link-works-scripts.mjs` (Node, built-in modules only) that copies the whitening execution scripts into a target git repository's `scripts/` directory.

#### Scenario: Distribute into a target repo

- **WHEN** the user runs `node link-works-whiten-automation/scripts/install-link-works-scripts.mjs --repo <target-repo>`
- **THEN** the whitening scripts and `lib/link-works-stats.mjs` are copied into `<target-repo>/scripts/`
- **AND** the script prints the destination paths and exits with code 0

#### Scenario: Pre-existing unrelated scripts preserved

- **WHEN** the target repo's `scripts/` already contains unrelated files
- **THEN** the installer overwrites only its own `link-works-*` artifacts
- **AND** leaves other files untouched

### Requirement: SKILL files are free of Metis-specific identifiers

The three platform SKILL files SHALL NOT reference Metis-specific identifiers (e.g. `metis-app-dataagent/`); business-code guidance SHALL be phrased generically as the target business repository.

#### Scenario: Iron rule is generic

- **WHEN** a user reads the iron rules in any platform SKILL file
- **THEN** the rule against adding whitening logic to business code names "the target business repository" rather than `metis-app-dataagent/`

