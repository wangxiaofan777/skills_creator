import assert from 'node:assert/strict';
import test from 'node:test';
import {
  computeFileMetrics,
  filterByStagedPaths,
  listPendingWhitenFiles,
  normalizePathKey,
  repoHash,
} from './link-works-stats.mjs';

const fixtureReport = {
  lastAddedPerFile: {
    'c:/work/app/foo.java': 100,
    'c:/work/app/bar.java': 50,
    'c:/work/app/clean.java': 20,
  },
  baselinePerFile: {
    'c:/work/app/foo.java': 10,
    'c:/work/app/bar.java': 0,
    'c:/work/app/clean.java': 0,
  },
  perFileAi: {
    'c:/work/app/foo.java': 30,
    'c:/work/app/bar.java': 50,
    'c:/work/app/clean.java': 20,
  },
};

test('normalizePathKey lowercases and uses forward slashes', () => {
  assert.equal(normalizePathKey('C:\\work\\app\\Foo.java'), 'c:/work/app/foo.java');
});

test('computeFileMetrics matches Link Works manualLine formula', () => {
  const foo = computeFileMetrics(fixtureReport, 'c:/work/app/foo.java');
  assert.equal(foo.fileInc, 90);
  assert.equal(foo.aiLine, 30);
  assert.equal(foo.manualLine, 60);

  const bar = computeFileMetrics(fixtureReport, 'c:/work/app/bar.java');
  assert.equal(bar.manualLine, 0);

  const clean = computeFileMetrics(fixtureReport, 'c:/work/app/clean.java');
  assert.equal(clean.manualLine, 0);
});

test('listPendingWhitenFiles returns only manualLine > 0', () => {
  const repoRoot = 'C:\\work\\app';
  const pending = listPendingWhitenFiles(fixtureReport, repoRoot);
  assert.equal(pending.length, 1);
  assert.equal(pending[0].fileKey, 'c:/work/app/foo.java');
  assert.equal(pending[0].manualLine, 60);
});

test('filterByStagedPaths intersects staged relative paths', () => {
  const repoRoot = 'C:\\work\\app';
  const pending = listPendingWhitenFiles(fixtureReport, repoRoot);
  const filtered = filterByStagedPaths(pending, ['foo.java', 'bar.java'], repoRoot);
  assert.equal(filtered.length, 1);
  assert.equal(filtered[0].fileKey, 'c:/work/app/foo.java');
});

test('repoHash uses backslash resolved path on Windows', () => {
  if (process.platform !== 'win32') {
    return;
  }
  assert.equal(repoHash('C:/work/app'), '7653f81a');
});
