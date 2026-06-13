# sonar-guard-scan-command Specification

## Purpose
TBD - created by archiving change sonar-guard-report-formats. Update Purpose after archive.
## Requirements
### Requirement: /sonar-scan slash command triggers a scan in the conversation

The package SHALL provide a `/sonar-scan` slash command (a `.claude/commands/sonar-scan.md` card) that instructs the agent to run `scan.py` and surface the Markdown report directly in the conversation, without the user typing shell commands. The command SHALL accept an optional scope argument (`full`, `staged`, or `files`), defaulting to `full`.

#### Scenario: One-click full project scan

- **WHEN** the user types `/sonar-scan` in the conversation
- **THEN** the agent runs `.sonarguard/scan.py --repo . --scope full --format md`
- **AND** renders the resulting Markdown report into the conversation

#### Scenario: Scoped scan via argument

- **WHEN** the user types `/sonar-scan staged`
- **THEN** the agent runs the scan with `--scope staged`
- **AND** renders the staged report into the conversation

#### Scenario: Command falls back to default scope

- **WHEN** the user types `/sonar-scan` with no argument
- **THEN** the agent uses scope `full`

### Requirement: SKILL augments script reports rather than generating them

After the command surfaces the script-generated report, the SKILL SHALL layer fix guidance on top — per-issue remediation, risk level (🟢/🟡/🔴), and distinguishing newly introduced issues from pre-existing ones — rather than re-deriving the report facts.

#### Scenario: Fix guidance follows the report

- **WHEN** the agent has rendered a `/sonar-scan` report
- **THEN** the agent offers remediation and risk assessment for the listed issues
- **AND** does not regenerate or re-truncate the issue listing itself

### Requirement: Command is installed into the business repo

The install flow SHALL place the `/sonar-scan` command into the business repository's project-level `.claude/commands/` so it travels with the repo and can be shared by the team.

#### Scenario: Command available after install

- **WHEN** a user installs sonar-guard into a business repo
- **THEN** `.claude/commands/sonar-scan.md` exists in that repo
- **AND** typing `/sonar-scan` in a session rooted there triggers the scan

