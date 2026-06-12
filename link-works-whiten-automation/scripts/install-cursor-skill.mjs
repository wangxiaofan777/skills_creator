#!/usr/bin/env node
/**
 * Install link-works-whiten-automation Cursor skill to the user skills directory.
 * Copies cursor/skills/link-works-whiten-automation/SKILL.md to
 * ~/.cursor/skills/link-works-whiten-automation/SKILL.md
 */
import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const packageRoot = dirname(scriptDir);
const sourceSkill = join(
  packageRoot,
  'cursor/skills/link-works-whiten-automation/SKILL.md'
);

if (!existsSync(sourceSkill)) {
  console.error(`Skill source not found: ${sourceSkill}`);
  process.exit(1);
}

const targetDir = join(homedir(), '.cursor/skills/link-works-whiten-automation');
mkdirSync(targetDir, { recursive: true });

const targetSkill = join(targetDir, 'SKILL.md');
copyFileSync(sourceSkill, targetSkill);

console.log(`Installed user skill: ${targetSkill}`);
console.log('Restart or start a new Cursor agent chat so description triggers reload.');
