## 1. Install script

- [x] 1.1 Create `link-works-whiten-automation/scripts/install-cursor-skill.mjs` using `fs`, `path`, `os` only; resolve package root via `import.meta.url`; copy to `{homedir}/.cursor/skills/link-works-whiten-automation/SKILL.md`
- [x] 1.2 Handle missing source with stderr message and non-zero exit code; print success path and reload hint on success
- [x] 1.3 Delete `link-works-whiten-automation/scripts/install-cursor-skill.ps1`
- [x] 1.4 Verify on Windows: run from repo root and confirm skill file at `%USERPROFILE%\.cursor\skills\link-works-whiten-automation\SKILL.md`

## 2. link-works-whiten-automation README

- [x] 2.1 Rewrite install section: single `node link-works-whiten-automation/scripts/install-cursor-skill.mjs` command from repo root; destination `~/.cursor/skills/...`; manual copy fallback
- [x] 2.2 Remove Metis wrapper, `SKILLS_CREATOR_ROOT`, and `D:\` absolute path examples
- [x] 2.3 Update directory structure to list `install-cursor-skill.mjs`; add Node.js 18+ to prerequisites
- [x] 2.4 Clarify in 常用操作: whitening `.ps1` scripts live in target repos; macOS may need `pwsh` for those scripts
- [x] 2.5 Remove or replace Metis-centric intro line (skill vs target-repo scripts scope)

## 3. Root README

- [x] 3.1 Update `link-works-whiten-automation/` tree in directory structure (`install-cursor-skill.mjs`)
- [x] 3.2 Add development rule: install scripts and docs must support Windows and macOS; no machine-specific absolute paths in docs

## 4. SKILL.md sync (three platforms)

- [x] 4.1 Update `cursor/skills/link-works-whiten-automation/SKILL.md`: Canonical sources, script map title/wording, remove `D:\` and Metis install references
- [x] 4.2 Apply same Canonical sources and script map updates to `claude-code/link-works-whiten-automation/SKILL.md`
- [x] 4.3 Apply same updates to `codex/SKILL.md`

## 5. Final check

- [x] 5.1 Grep repo for `install-cursor-skill.ps1`, `D:\\skills_creator`, and Metis install wrapper references; fix any stragglers in this package
- [x] 5.2 Confirm `openspec/changes/link-works-cross-platform-install/specs` requirements are satisfied by the above work
