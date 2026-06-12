# sonar-guard-config-docs Specification

## Purpose

Documentation requirements for Sonar configuration examples, `status` output fields, merge priority, and troubleshooting in README and workflow references.

## Requirements

### Requirement: README documents complete configuration reference

`sonar-guard/README.md` SHALL include a dedicated **配置参考** section with copy-paste examples for minimal and optional `.sonarguard.json`, personal token setup (`SONAR_TOKEN` and `~/.config/sonarguard/config.json`), and `sonar-project.properties` as an alternative for `projectKey` / `hostUrl`.

#### Scenario: User configures a new business repo

- **WHEN** a user opens README to configure Sonar for a target repository
- **THEN** they find JSON examples showing required `hostUrl` and `projectKey`
- **AND** they find instructions for setting `SONAR_TOKEN` without committing secrets
- **AND** they find optional `hook.mode`, `hook.blockSeverities`, and `hook.localChecks` documented with defaults

#### Scenario: User understands config merge order

- **WHEN** a user has values in `.sonarguard.json`, user config, and environment variables
- **THEN** README states that repo files are read first, then `~/.config/sonarguard/config.json`, then `SONAR_TOKEN` / `SONAR_HOST_URL` override token and hostUrl

### Requirement: README documents status output and troubleshooting

`sonar-guard/README.md` SHALL document `sonar_api.py status --repo` JSON fields (`hostUrl`, `projectKey`, `tokenConfigured`, `project_state`, `hint`, `qualityGate`, `configError`) and recommended next steps for each common `project_state`.

#### Scenario: User sees unreachable on empty config

- **WHEN** a user runs `status` on a repo with `{}` in `.sonarguard.json`
- **THEN** README explains `project_state: unreachable` with hint about missing `hostUrl`
- **AND** README lists steps to add `hostUrl`, `projectKey`, and `SONAR_TOKEN` then re-run `status`

#### Scenario: User sees no_auth or not_found

- **WHEN** `project_state` is `no_auth`, `not_found`, or `no_permission`
- **THEN** README explains the meaning and whether server mode or offline fallback applies

### Requirement: README documents optional environment variables

`sonar-guard/README.md` SHALL list optional environment variables `SONARGUARD_TIMEOUT` and `SONARGUARD_MAX_ISSUE_PAGES` with purpose and defaults referenced from script behavior.

#### Scenario: User truncates B1 issue list

- **WHEN** a full scan returns truncated issues
- **THEN** README points to `SONARGUARD_MAX_ISSUE_PAGES` to fetch more pages

### Requirement: Workflow reference links to configuration docs

`sonar-guard/references/workflow.md` SHALL reference the README configuration section for full detail while keeping a short summary in §配置.

#### Scenario: Maintainer reads workflow only

- **WHEN** a maintainer reads `references/workflow.md` section 4
- **THEN** they are directed to README **配置参考** for examples and status troubleshooting
