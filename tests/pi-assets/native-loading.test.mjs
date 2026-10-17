import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtemp, mkdir, copyFile, readFile, writeFile, rm, rename } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { tmpdir, homedir } from 'node:os';
import { pathToFileURL, fileURLToPath } from 'node:url';

const repo = fileURLToPath(new URL('../../', import.meta.url));
const root = process.env.PI_SDK_ROOT || join(homedir(), '.local/lib/node_modules/@earendil-works/pi-coding-agent');
const { loadSkills, formatSkillsForPrompt } = await import(pathToFileURL(join(root, 'dist/core/skills.js')));
const { loadProjectContextFiles } = await import(pathToFileURL(join(root, 'dist/core/resource-loader.js')));
const sharedIds = ['design-experiment', 'docker-optimize', 'logging-optimize', 'piecemeal-growth', 'review-experiment', 'skill-lifecycle'];
const piIds = ['architecture-review', 'archify', 'ask-chatgpt-pro', 'diagnose', 'distill-source', 'explain', 'integrate-research', 'review-change', 'surface-unknowns'];

async function materialize(t) {
  const scratch = await mkdtemp(join(tmpdir(), 'pi-assets-native-'));
  t.after(() => rm(scratch, { recursive: true, force: true }));
  const files = JSON.parse(execFileSync('python3', ['-c', `
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(sys.argv[1]) / 'scripts'))
from agent_catalog import load_catalog, desired_files
repo = pathlib.Path(sys.argv[1])
assets = load_catalog(repo)
print(json.dumps({platform: {target: str(item.source) for target, item in desired_files(repo, assets, platform).items()} for platform in ['agents', 'pi']}))
`, repo], { encoding: 'utf8' }));
  for (const [platform, mapping] of Object.entries(files)) {
    for (const [target, source] of Object.entries(mapping)) {
      const path = join(scratch, platform, target);
      await mkdir(dirname(path), { recursive: true });
      await copyFile(source, path);
    }
  }
  const project = join(scratch, 'project');
  await mkdir(project);
  return { scratch, project, files, agentDir: join(scratch, 'pi'), sharedDir: join(scratch, 'agents') };
}

function discover({ project, agentDir, sharedDir }) {
  return loadSkills({ cwd: project, agentDir, includeDefaults: false, skillPaths: [join(agentDir, 'skills'), join(sharedDir, 'skills')] });
}

test('all admitted catalog skills parse natively with one complete implementation per name', async t => {
  const fixture = await materialize(t);
  const { skills, diagnostics } = discover(fixture);
  assert.deepEqual(diagnostics, []);
  assert.deepEqual(skills.map(s => s.name).sort(), [...sharedIds, ...piIds].sort());
  assert.equal(new Set(skills.map(s => s.name)).size, skills.length);
  for (const skill of skills) {
    const home = sharedIds.includes(skill.name) ? fixture.sharedDir : fixture.agentDir;
    assert.equal(skill.filePath, join(home, 'skills', skill.name, 'SKILL.md'));
    assert.equal(skill.disableModelInvocation, skill.name === 'surface-unknowns');
  }
  const prompt = formatSkillsForPrompt(skills);
  for (const skill of skills) assert.equal(prompt.includes(`<name>${skill.name}</name>`), skill.name !== 'surface-unknowns');
  // Native metadata visibility does not relax piecemeal-growth's user-only trigger.
  assert.match(skills.find(s => s.name === 'piecemeal-growth').description, /only when the user names this skill or explicitly requests/);
});

test('operative docs closure travels with each consumer without a Codex installation', async t => {
  const fixture = await materialize(t);
  for (const [platform, mapping] of Object.entries(fixture.files)) {
    const targets = new Set(Object.keys(mapping));
    for (const target of targets) {
      if (!target.endsWith('.md')) continue;
      const text = await readFile(join(fixture.scratch, platform, target), 'utf8');
      const skillRoot = target.startsWith('skills/') ? target.split('/').slice(0, 2).join('/') : '';
      for (const line of text.split('\n')) {
        if (line.includes('example-only:') || line.includes('(example-only)')) continue;
        for (const match of line.matchAll(/(?<!\/)docs\/[A-Za-z0-9/_.-]+\.md/g)) {
          const required = skillRoot ? `${skillRoot}/${match[0]}` : match[0];
          assert.ok(targets.has(required), `${platform}/${target} requires ${required}`);
        }
      }
    }
  }
  assert.ok(fixture.files.pi['AGENTS.md']);
  for (const name of ['context-file-authoring', 'skill-authoring-principles', 'claim-discipline', 'experiment-protocol-readout-contract']) assert.ok(fixture.files.pi[`docs/${name}.md`]);
  assert.equal(Object.keys(fixture.files.pi).some(path => path === 'SYSTEM.md'), false);
});

test('native context loading retains global instructions and existing project AGENTS without conversion', async t => {
  const fixture = await materialize(t);
  await copyFile(join(repo, 'AGENTS.md'), join(fixture.project, 'AGENTS.md'));
  const nested = join(fixture.project, 'subsystem');
  await mkdir(nested);
  await writeFile(join(nested, 'AGENTS.md'), '# Synthetic subsystem boundary\n');
  const initial = loadProjectContextFiles({ cwd: fixture.project, agentDir: fixture.agentDir });
  assert.ok(initial.some(file => file.path === join(fixture.agentDir, 'AGENTS.md') && file.content.includes('# Global Pi Instructions')));
  const project = initial.find(file => file.path === join(fixture.project, 'AGENTS.md'));
  assert.equal(project.content, await readFile(join(repo, 'AGENTS.md'), 'utf8'));
  assert.equal(initial.some(file => file.path === join(nested, 'AGENTS.md')), false);
  const scoped = loadProjectContextFiles({ cwd: nested, agentDir: fixture.agentDir });
  assert.ok(scoped.some(file => file.path === join(nested, 'AGENTS.md')));
});

test('Pi frontmatter preserves explicit-only invocation while retaining the explicit command resource', async t => {
  const fixture = await materialize(t);
  const explicit = join(fixture.scratch, 'explicit-example');
  await mkdir(explicit);
  await writeFile(join(explicit, 'SKILL.md'), '---\nname: explicit-example\ndescription: Synthetic user-only action.\ndisable-model-invocation: true\n---\nOnly act when explicitly invoked.\n');
  const { skills, diagnostics } = loadSkills({ cwd: fixture.project, agentDir: fixture.agentDir, includeDefaults: false, skillPaths: [explicit] });
  assert.deepEqual(diagnostics, []);
  assert.equal(skills.length, 1);
  assert.equal(skills[0].disableModelInvocation, true);
  assert.equal(formatSkillsForPrompt(skills), '');
});


test('native default discovery finds both homes and project trust gates skills while retaining context', async t => {
  const fixture = await materialize(t);
  await rename(fixture.sharedDir, join(fixture.scratch, '.agents'));
  await copyFile(join(repo, 'AGENTS.md'), join(fixture.project, 'AGENTS.md'));
  for (const [directory, name] of [['.pi', 'synthetic-pi-project'], ['.agents', 'synthetic-agents-project']]) {
    const path = join(fixture.project, directory, 'skills', name);
    await mkdir(path, { recursive: true });
    await writeFile(join(path, 'SKILL.md'), `---\nname: ${name}\ndescription: Synthetic project trust qualification.\n---\nRead only synthetic project evidence.\n`);
  }
  const probe = fileURLToPath(new URL('./default-discovery-probe.mjs', import.meta.url));
  const result = JSON.parse(execFileSync(process.execPath, [probe, fixture.agentDir, fixture.project], {
    cwd: fixture.project,
    env: { ...process.env, HOME: fixture.scratch, PI_CODING_AGENT_DIR: fixture.agentDir, PI_SDK_ROOT: root, XDG_CONFIG_HOME: join(fixture.scratch, 'config'), XDG_CACHE_HOME: join(fixture.scratch, 'cache') },
    encoding: 'utf8',
  }));
  assert.deepEqual(result.untrusted.names, [...sharedIds, ...piIds].sort());
  assert.deepEqual(result.trusted.names, [...sharedIds, ...piIds, 'synthetic-pi-project', 'synthetic-agents-project'].sort());
  for (const state of [result.untrusted, result.trusted]) {
    assert.deepEqual(state.diagnostics, []);
    assert.deepEqual(state.explicitOnly, ['surface-unknowns']);
    assert.equal(state.prompt.includes('<name>surface-unknowns</name>'), false);
    assert.equal(state.globalContext, true);
    assert.equal(state.projectContext, true);
  }
});
