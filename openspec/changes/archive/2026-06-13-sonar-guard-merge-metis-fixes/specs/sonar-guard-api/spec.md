## ADDED Requirements

### Requirement: Precise staged/file issue matching

`cmd_issues()` SHALL query Sonar using `componentKeys` with `onComponentOnly=true`, and SHALL additionally filter returned issues client-side by a path-normalized set of the requested files, so that only issues belonging to the requested files themselves are returned. Path normalization SHALL convert backslashes to forward slashes and strip a leading `./`.

#### Scenario: Windows path does not over-match

- **WHEN** `cmd_issues()` is called for a staged file whose path contains backslashes or a `./` prefix
- **THEN** the request uses `componentKeys` + `onComponentOnly=true`
- **AND** each returned issue is kept only if its normalized file path is in the requested set
- **AND** issues on other components are not included

#### Scenario: Full-project query unchanged

- **WHEN** `cmd_issues_all()` runs a B1 full-project scan
- **THEN** its query behavior is unchanged by this change
