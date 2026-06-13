---
name: link-works-whiten-automation
description: >-
  Link Works batch AI line whitening (洗白): run scripts/link-works-whiten-all.ps1,
  pre-commit hook, link-works.whiteningFile via runCommands. Never patch commitReport
  JSON only. Triggers: 洗白, 一键洗白, Link Works, whiteningFile, other lines, manualLine,
  commit AI stats, pre-commit whiten.
license: MIT
compatibility: Requires link-works.link-works >= 2.12.4 and Cursor open on the git repo.
metadata:
  author: skills_creator
  version: "1.1"
---

# Link Works whiten automation

## When to use

- User mentions **洗白**, **一键洗白**, Link Works **其他行数**, or commit **AI 编码率** gaps before commit.
- Before `git commit` when Link Works panel shows **manual / other lines** on staged files.
- Implementing or troubleshooting `scripts/link-works-*.ps1` in a repo that ships this tooling.

**Not for:** lowering AI rate by marking lines human — that is a different Link Works flow (`resyncFromGit` / baseline), not「洗白 AI」.

## Iron rules

1. **MUST** execute whitening through `link-works.whiteningFile` (or `runCommands` chaining it) inside the Cursor extension host.
2. **MUST NOT** treat editing `%APPDATA%\Cursor\User\globalStorage\link-works.link-works\commitReport.*.json` as sufficient — memory stats drive commit attribution while Cursor is open.
3. **MUST NOT** add whitening logic into the target repository's business/application code; keep all tooling under `scripts/`.
4. Prefer repo scripts when present: `{gitRoot}/scripts/link-works-whiten-all.ps1`.

## Whitening semantics

For each file in the current commit cycle:

- `fileInc = max(0, lastAdded - baseline)`
- `manualLine = fileInc - min(perFileAi, fileInc)` (Link Works「其他行数」)
- Whiten sets `perFileAi` to at least `fileInc` via `applyHookWhitening`

## Script map (shipped by this package; install into target repo's `scripts/`)

| Script | Purpose |
|--------|---------|
| `scripts/link-works-whiten-all.ps1` | Whiten all `manualLine > 0` files |
| `scripts/link-works-pre-commit-whiten.ps1` | Whiten staged ∩ pending (git hook) |
| `scripts/link-works-invoke-run-commands.ps1` | Dispatch `vscode://vscode.runCommands?data=...` |
| `scripts/install-link-works-pre-commit-hook.ps1` | Opt-in `.git/hooks/pre-commit` installer |
| `scripts/lib/link-works-stats.mjs` | Read `commitReport.{repoHash}.json`, list pending |

## Execution checklist

1. Confirm **Link Works** extension installed and **Cursor is open** on the repository root.
2. List pending: `node scripts/lib/link-works-stats.mjs list-pending` or `scripts/link-works-whiten-all.ps1 -ListOnly`.
3. If pending > 0: run `scripts/link-works-whiten-all.ps1` **or** Command Palette → **Tasks: Run Task** → `Link Works: Whiten All Pending`.
4. Optional: install pre-commit — `scripts/install-link-works-pre-commit-hook.ps1` (opt-in).
5. Re-check Link Works panel: **其他行数** should be **0** for whitened files before commit.

## Failure triage

| Symptom | Action |
|---------|--------|
| `commit report not found` | Open repo in Cursor; make a small edit so Link Works creates `commitReport.{hash}.json` |
| URI / invoke failed | Keep Cursor running; use Tasks or re-run `link-works-whiten-all.ps1` |
| pre-commit blocked commit | Run step 3 manually, or `git commit --no-verify` after explicit user consent |
| Wrong repo hash on Windows | Stats module tries `path.resolve` + backslash variants (see `repo-info` CLI) |

## Canonical sources

- **Skill package**: `skills_creator/link-works-whiten-automation/` — install Cursor skill from repo root: `node link-works-whiten-automation/scripts/install-cursor-skill.mjs`
- **Whitening scripts**: shipped by this package under `link-works-whiten-automation/scripts/` (canonical source). Distribute into a target repo's `scripts/` via `node link-works-whiten-automation/scripts/install-link-works-scripts.mjs --repo <target>`.
