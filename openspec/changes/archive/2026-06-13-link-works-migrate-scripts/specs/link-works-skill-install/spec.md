## ADDED Requirements

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

## REMOVED Requirements

### Requirement: Decentralized script map wording

**Reason**: 模型反转——脚本不再由各目标仓库自备,而是由本包作为权威源自带并通过安装器分发。
**Migration**: 见新增「Package ships whitening execution scripts」与「Node distribution installer copies scripts into a target repo」;SKILL 的 script map 改为描述本包自带、经 `install-link-works-scripts.mjs` 分发到目标仓库 `scripts/` 的脚本。
