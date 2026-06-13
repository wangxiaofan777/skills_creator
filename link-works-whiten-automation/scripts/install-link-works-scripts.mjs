#!/usr/bin/env node
/**
 * Distribute Link Works whitening scripts into a target git repository's scripts/.
 *
 * Usage (from skills_creator repo root):
 *   node link-works-whiten-automation/scripts/install-link-works-scripts.mjs --repo <target-repo>
 *
 * Copies this package's canonical whitening scripts into <target-repo>/scripts/.
 * Only this tool's own link-works-* artifacts are written; other files in the
 * target scripts/ directory are left untouched. Node built-in modules only.
 */
import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));

// --- parse --repo <path> | --repo=<path> ---
const argv = process.argv.slice(2);
let repoArg = null;
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--repo') {
    repoArg = argv[i + 1];
    i++;
  } else if (argv[i].startsWith('--repo=')) {
    repoArg = argv[i].slice('--repo='.length);
  }
}

if (!repoArg) {
  console.error('Usage: node install-link-works-scripts.mjs --repo <target-repo>');
  process.exit(1);
}

const repoRoot = resolve(repoArg);
if (!existsSync(repoRoot) || !statSync(repoRoot).isDirectory()) {
  console.error(`Target repo not found or not a directory: ${repoRoot}`);
  process.exit(1);
}

// Runtime artifacts shipped into the target repo (test file is dev-only, excluded).
const FILES = [
  'link-works-whiten-all.ps1',
  'link-works-pre-commit-whiten.ps1',
  'link-works-invoke-run-commands.ps1',
  'install-link-works-pre-commit-hook.ps1',
  'link-works-whiten-all-keybinding.snippet.json',
  'lib/link-works-stats.mjs',
];

const targetScripts = join(repoRoot, 'scripts');
mkdirSync(join(targetScripts, 'lib'), { recursive: true });

const copied = [];
for (const rel of FILES) {
  const src = join(scriptDir, rel);
  if (!existsSync(src)) {
    console.error(`Source script missing: ${src}`);
    process.exit(1);
  }
  const dst = join(targetScripts, rel);
  copyFileSync(src, dst);
  copied.push(dst);
}

console.log(`Installed ${copied.length} Link Works script(s) into ${targetScripts}:`);
for (const p of copied) console.log(`  ${p}`);
console.log(
  'Next (in the target repo, optional): run scripts/install-link-works-pre-commit-hook.ps1 to enable the opt-in pre-commit whitening hook.'
);
