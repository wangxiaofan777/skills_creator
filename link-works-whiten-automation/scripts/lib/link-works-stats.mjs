#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const EXTENSION_ID = 'link-works.link-works';

export function normalizePathKey(filePath) {
  return filePath.replace(/\\/g, '/').toLowerCase();
}

export function getRepoRoot(cwd = process.cwd()) {
  try {
    return execSync('git rev-parse --show-toplevel', {
      cwd,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
  } catch {
    throw new Error('Not inside a git repository (git rev-parse --show-toplevel failed).');
  }
}

export function repoHashCandidates(repoRoot) {
  const trimmed = repoRoot.trim();
  const resolved = path.resolve(trimmed);
  const unique = new Set([trimmed, resolved]);
  if (process.platform === 'win32') {
    unique.add(trimmed.replace(/\//g, '\\'));
    unique.add(resolved.replace(/\//g, '\\'));
  }
  return [...unique];
}

export function repoHash(repoRoot) {
  const candidates = repoHashCandidates(repoRoot);
  for (const candidate of candidates) {
    const reportPath = commitReportPathForHash(
      crypto.createHash('sha1').update(candidate).digest('hex').slice(0, 8),
    );
    if (fs.existsSync(reportPath)) {
      return crypto.createHash('sha1').update(candidate).digest('hex').slice(0, 8);
    }
  }
  const primary = candidates[1] ?? candidates[0];
  return crypto.createHash('sha1').update(primary).digest('hex').slice(0, 8);
}

export function globalStorageRoot() {
  if (process.platform === 'win32') {
    const appData = process.env.APPDATA;
    if (!appData) {
      throw new Error('APPDATA is not set; cannot locate Cursor globalStorage.');
    }
    return path.join(appData, 'Cursor', 'User', 'globalStorage', EXTENSION_ID);
  }
  const home = os.homedir();
  return path.join(home, '.config', 'Cursor', 'User', 'globalStorage', EXTENSION_ID);
}

export function commitReportPathForHash(hash) {
  return path.join(globalStorageRoot(), `commitReport.${hash}.json`);
}

export function resolveCommitReportPath(repoRoot) {
  const candidates = repoHashCandidates(repoRoot);
  for (const candidate of candidates) {
    const hash = crypto.createHash('sha1').update(candidate).digest('hex').slice(0, 8);
    const reportPath = commitReportPathForHash(hash);
    if (fs.existsSync(reportPath)) {
      return { reportPath, hash, repoKey: candidate };
    }
  }
  const hash = repoHash(repoRoot);
  return {
    reportPath: commitReportPathForHash(hash),
    hash,
    repoKey: candidates[1] ?? candidates[0],
  };
}

export function loadCommitReport(repoRoot) {
  const { reportPath, hash, repoKey } = resolveCommitReportPath(repoRoot);
  if (!fs.existsSync(reportPath)) {
    const err = new Error(`Link Works commit report not found: ${reportPath}`);
    err.code = 'ENOENT';
    throw err;
  }
  const raw = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
  return { report: raw, reportPath, hash, repoKey };
}

export function computeFileMetrics(report, fileKey) {
  const lastAdded = Number(report.lastAddedPerFile?.[fileKey] ?? 0);
  const baseline = Number(report.baselinePerFile?.[fileKey] ?? 0);
  const perFileAi = Number(report.perFileAi?.[fileKey] ?? 0);
  const fileInc = Math.max(0, lastAdded - baseline);
  const aiLine = Math.min(Math.max(0, perFileAi), fileInc);
  const manualLine = fileInc - aiLine;
  return { fileKey, lastAdded, baseline, perFileAi, fileInc, aiLine, manualLine };
}

export function absolutePathFromReportKey(fileKey, repoRoot) {
  const normalizedRepo = normalizePathKey(repoRoot);
  const normalizedKey = normalizePathKey(fileKey);
  if (normalizedKey.startsWith(normalizedRepo)) {
    const suffix = fileKey.slice(normalizedRepo.length).replace(/^\//, '');
    return path.join(repoRoot, suffix.split('/').join(path.sep));
  }
  return fileKey;
}

export function listPendingWhitenFiles(report, repoRoot) {
  const keys = new Set([
    ...Object.keys(report.lastAddedPerFile ?? {}),
    ...Object.keys(report.baselinePerFile ?? {}),
    ...Object.keys(report.perFileAi ?? {}),
  ]);
  const pending = [];
  for (const fileKey of keys) {
    const metrics = computeFileMetrics(report, fileKey);
    if (metrics.manualLine > 0) {
      pending.push({
        ...metrics,
        absolutePath: absolutePathFromReportKey(fileKey, repoRoot),
      });
    }
  }
  pending.sort((a, b) => a.fileKey.localeCompare(b.fileKey));
  return pending;
}

export function stagedRelativePaths(cwd = process.cwd()) {
  const output = execSync('git diff --cached --name-only --diff-filter=ACMR', {
    cwd,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'ignore'],
  });
  return output
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
}

export function filterByStagedPaths(pendingFiles, stagedRelPaths, repoRoot) {
  if (!stagedRelPaths.length) {
    return [];
  }
  const stagedKeys = new Set(
    stagedRelPaths.map((rel) => normalizePathKey(path.join(repoRoot, rel))),
  );
  return pendingFiles.filter((entry) => stagedKeys.has(normalizePathKey(entry.fileKey)));
}

function printJson(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

function main() {
  const [command = 'list-pending', ...args] = process.argv.slice(2);
  const repoRoot = getRepoRoot();

  if (command === 'repo-info') {
    const resolved = resolveCommitReportPath(repoRoot);
    printJson({
      repoRoot,
      ...resolved,
      exists: fs.existsSync(resolved.reportPath),
    });
    return;
  }

  const { report, reportPath, hash } = loadCommitReport(repoRoot);

  if (command === 'list-pending') {
    printJson({
      repoRoot,
      reportPath,
      hash,
      pending: listPendingWhitenFiles(report, repoRoot),
    });
    return;
  }

  if (command === 'list-staged-pending') {
    const staged = args.length ? args : stagedRelativePaths(repoRoot);
    const pending = listPendingWhitenFiles(report, repoRoot);
    const filtered = filterByStagedPaths(pending, staged, repoRoot);
    printJson({
      repoRoot,
      reportPath,
      hash,
      staged,
      pending: filtered,
    });
    return;
  }

  process.stderr.write(
    `Usage: node link-works-stats.mjs <repo-info|list-pending|list-staged-pending> [staged paths...]\n`,
  );
  process.exit(2);
}

const isMain =
  process.argv[1] &&
  path.resolve(fileURLToPath(import.meta.url)) === path.resolve(process.argv[1]);

if (isMain) {
  try {
    main();
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exit(1);
  }
}
