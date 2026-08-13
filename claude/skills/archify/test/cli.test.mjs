import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillRoot = path.resolve(__dirname, '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'archify-cli-'));
const cli = path.join(skillRoot, 'bin/archify.mjs');

function run(args, options = {}) {
  return spawnSync(process.execPath, [cli, ...args], {
    cwd: options.cwd || skillRoot,
    encoding: 'utf8',
    env: options.env || process.env,
  });
}

test('cli: help lists commands and diagram types', () => {
  const result = run(['--help']);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /archify render <type>/);
  assert.match(result.stdout, /architecture, workflow, sequence, dataflow, lifecycle/);
});

test('cli: render writes a diagram html file', () => {
  const out = path.join(tmp, 'workflow.html');
  const input = path.join(skillRoot, 'examples/agent-tool-call.workflow.json');
  const result = run(['render', 'workflow', input, out]);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(fs.existsSync(out), true);
  assert.match(fs.readFileSync(out, 'utf8'), /Agent Tool Call Workflow/);
});

test('cli: all five schemas accept meta.description and wire it into accessible SVG output', () => {
  const cases = [
    ['architecture', 'web-app.architecture.json'],
    ['workflow', 'agent-tool-call.workflow.json'],
    ['sequence', 'cache-miss-request.sequence.json'],
    ['dataflow', 'product-analytics.dataflow.json'],
    ['lifecycle', 'agent-run.lifecycle.json'],
  ];
  for (const [type, example] of cases) {
    const input = path.join(tmp, `description-${type}.json`);
    const output = path.join(tmp, `description-${type}.html`);
    const doc = JSON.parse(fs.readFileSync(path.join(skillRoot, 'examples', example), 'utf8'));
    doc.meta.description = `Accessible ${type} explanation.`;
    fs.writeFileSync(input, JSON.stringify(doc));
    const result = run(['render', type, input, output]);
    assert.equal(result.status, 0, `${type}: ${result.stderr}`);
    assert.match(fs.readFileSync(output, 'utf8'), new RegExp(`Accessible ${type} explanation\\.`));
  }
});

test('cli: check validates rendered html', () => {
  const out = path.join(tmp, 'workflow-check.html');
  const input = path.join(skillRoot, 'examples/agent-tool-call.workflow.json');
  assert.equal(run(['render', 'workflow', input, out]).status, 0);

  const result = run(['check', out]);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /"ok": true/);
});

test('cli: validate emits structured json without keeping html output', () => {
  const input = path.join(skillRoot, 'examples/agent-tool-call.workflow.json');
  const before = new Set(fs.readdirSync(tmp));
  const result = run(['validate', 'workflow', input, '--json']);
  assert.equal(result.status, 0, result.stderr);
  const parsed = JSON.parse(result.stdout);
  assert.equal(parsed.ok, true);
  assert.equal(parsed.type, 'workflow');
  assert.equal(parsed.checks.length, 5);
  assert.deepEqual(new Set(fs.readdirSync(tmp)), before);
});

test('cli: validate returns renderer errors for bad input', () => {
  const input = path.join(tmp, 'bad.workflow.json');
  const validateTmp = path.join(tmp, 'validate-failure-tmp');
  const doc = JSON.parse(fs.readFileSync(path.join(skillRoot, 'examples/agent-tool-call.workflow.json'), 'utf8'));
  doc.edges[0].to = 'ghost';
  fs.writeFileSync(input, JSON.stringify(doc));
  fs.mkdirSync(validateTmp);

  const result = run(['validate', 'workflow', input], {
    env: { ...process.env, TMPDIR: validateTmp },
  });
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /unknown target "ghost"/);
  assert.deepEqual(fs.readdirSync(validateTmp), []);
});

test('cli: explicit d2 and combined formats publish deterministic siblings', () => {
  const input = path.join(skillRoot, 'examples/agent-tool-call.workflow.json');
  const d2Path = path.join(tmp, 'explicit.d2');
  const d2 = run(['render', 'workflow', input, d2Path, '--format', 'd2']);
  assert.equal(d2.status, 0, d2.stderr);
  assert.ok(parseD2Semantics(fs.readFileSync(d2Path, 'utf8')).entities.includes('Chat Surface — thread + files'));
  assert.equal(fs.existsSync(`${d2Path}.svg`), false);

  const combined = run(['render', 'workflow', input, path.join(tmp, 'combined.html'), '--format', 'html+d2']);
  assert.equal(combined.status, 0, combined.stderr);
  assert.equal(fs.existsSync(path.join(tmp, 'combined.html')), true);
  assert.equal(fs.existsSync(path.join(tmp, 'combined.d2')), true);
});

test('cli: D2 source carries reproducible config and plain compile succeeds', () => {
  const input = path.join(skillRoot, 'examples/agent-tool-call.workflow.json');
  const d2Path = path.join(tmp, 'configured.d2');
  const result = run(['render', 'workflow', input, d2Path, '--format', 'd2']);
  assert.equal(result.status, 0, result.stderr);
  const source = fs.readFileSync(d2Path, 'utf8');
  assert.match(source, /layout-engine: elk/);
  assert.match(source, /theme-id: 0/);
  assert.match(source, /dark-theme-id: 200/);
  const plain = spawnSync('d2', [d2Path, path.join(tmp, 'configured.svg')], { encoding: 'utf8' });
  assert.equal(plain.status, 0, plain.stderr);
});

test('cli: selector and path contract covers omitted, extension, stem, and rejection cases', () => {
  const input = path.join(skillRoot, 'examples/agent-tool-call.workflow.json');
  const cases = [
    ['d2-omitted', 'd2', [], 'examples/workflow-agent-tool-call-rendered.d2'],
    ['d2-extension', 'd2', ['named.d2'], 'named.d2'],
    ['d2-stem', 'd2', ['named'], 'named.d2'],
    ['combined-omitted', 'html+d2', [], 'examples/workflow-agent-tool-call-rendered.html'],
    ['combined-extension', 'html+d2', ['named.html'], 'named.html'],
    ['combined-stem', 'html+d2', ['named'], 'named.html'],
  ];
  for (const [name, format, positional, expected] of cases) {
    const cwd = path.join(tmp, name);
    fs.mkdirSync(cwd);
    const result = run(['render', 'workflow', input, ...positional, '--format', format], { cwd });
    assert.equal(result.status, 0, `${name}: ${result.stderr}`);
    assert.equal(fs.existsSync(path.join(cwd, expected)), true);
    if (format === 'html+d2') assert.equal(fs.existsSync(path.join(cwd, expected.replace(/\.html$/, '.d2'))), true);
  }
  for (const [format, output, message] of [['d2', 'bad.html', /D2 output paths cannot use/], ['html+d2', 'bad.d2', /Combined output paths must use/]]) {
    const result = run(['render', 'workflow', input, path.join(tmp, output), '--format', format]);
    assert.equal(result.status, 2);
    assert.match(result.stderr, message);
  }
  for (const args of [['--format', 'svg'], ['--format', 'd2', '--format', 'd2'], ['--format']]) {
    const result = run(['render', 'workflow', input, ...args]);
    assert.notEqual(result.status, 0);
  }
});

test('cli: schema-optional arrays may be omitted from D2 inputs', () => {
  const cases = [
    ['architecture', 'web-app.architecture.json', 'boundaries'],
    ['architecture', 'web-app.architecture.json', 'connections'],
    ['architecture', 'web-app.architecture.json', 'cards'],
    ['workflow', 'agent-tool-call.workflow.json', 'groups'],
    ['workflow', 'agent-tool-call.workflow.json', 'phases'],
    ['workflow', 'agent-tool-call.workflow.json', 'mainPath'],
    ['workflow', 'agent-tool-call.workflow.json', 'cards'],
    ['sequence', 'cache-miss-request.sequence.json', 'segments'],
    ['sequence', 'cache-miss-request.sequence.json', 'activations'],
    ['sequence', 'cache-miss-request.sequence.json', 'cards'],
    ['dataflow', 'product-analytics.dataflow.json', 'cards'],
    ['lifecycle', 'agent-run.lifecycle.json', 'cards'],
  ];
  for (const [index, [type, example, optionalField]] of cases.entries()) {
    const input = path.join(tmp, `optional-${index}.json`);
    const output = path.join(tmp, `optional-${index}.d2`);
    const doc = JSON.parse(fs.readFileSync(path.join(skillRoot, 'examples', example), 'utf8'));
    delete doc[optionalField];
    fs.writeFileSync(input, JSON.stringify(doc));
    const result = run(['render', type, input, output, '--format', 'd2']);
    assert.equal(result.status, 0, `${type}.${optionalField}: ${result.stderr}`);
    const compile = spawnSync('d2', [output, `${output}.svg`], { encoding: 'utf8' });
    assert.equal(compile.status, 0, `${type}.${optionalField}: ${compile.stderr}`);
    assert.doesNotMatch(fs.readFileSync(output, 'utf8'), /undefined/);
  }
});

test('cli: present-but-non-array optional D2 fields fail closed', () => {
  const cases = [
    ['architecture', 'web-app.architecture.json', 'boundaries'],
    ['workflow', 'agent-tool-call.workflow.json', 'groups'],
    ['workflow', 'agent-tool-call.workflow.json', 'mainPath'],
    ['sequence', 'cache-miss-request.sequence.json', 'segments'],
    ['sequence', 'cache-miss-request.sequence.json', 'activations'],
    ['dataflow', 'product-analytics.dataflow.json', 'cards'],
  ];
  for (const [index, [type, example, optionalField]] of cases.entries()) {
    const input = path.join(tmp, `optional-invalid-${index}.json`);
    const doc = JSON.parse(fs.readFileSync(path.join(skillRoot, 'examples', example), 'utf8'));
    doc[optionalField] = 'invalid';
    fs.writeFileSync(input, JSON.stringify(doc));
    const result = run(['render', type, input, path.join(tmp, `optional-invalid-${index}.d2`), '--format', 'd2'], {
      env: { ...process.env, PATH: path.join(tmp, 'no-d2') },
    });
    assert.notEqual(result.status, 0, `${type}.${optionalField} unexpectedly rendered`);
    assert.match(result.stderr, /must be (an )?array/);
  }
});

test('cli: shuffled and overlapping sequence segments preserve semantic y order once', () => {
  const input = path.join(tmp, 'shuffled.sequence.json');
  const doc = JSON.parse(fs.readFileSync(path.join(skillRoot, 'examples/cache-miss-request.sequence.json'), 'utf8'));
  doc.messages.reverse();
  doc.segments[0].to = 400;
  fs.writeFileSync(input, JSON.stringify(doc));
  const output = path.join(tmp, 'shuffled.d2');
  const result = run(['render', 'sequence', input, output, '--format', 'd2']);
  assert.equal(result.status, 0, result.stderr);
  const source = fs.readFileSync(output, 'utf8');
  assert.ok(source.indexOf('"open page"') < source.indexOf('"200 JSON"'));
  for (const label of ['open page', 'claims ok', 'read cache', '200 JSON']) assert.equal(source.split(`"${label}"`).length - 1, 1);
});

test('cli: absent d2 fails closed without creating d2 artifacts', () => {
  const input = path.join(skillRoot, 'examples/agent-tool-call.workflow.json');
  const destination = path.join(tmp, 'absent.d2');
  const result = run(['render', 'workflow', input, destination, '--format', 'd2'], {
    env: { ...process.env, PATH: path.join(tmp, 'no-d2') },
  });
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /D2 is unavailable/);
  assert.equal(fs.existsSync(destination), false);
});

test('cli: adversarial labels stay encoded D2 text', () => {
  const input = path.join(tmp, 'hostile.workflow.json');
  const doc = JSON.parse(fs.readFileSync(path.join(skillRoot, 'examples/agent-tool-call.workflow.json'), 'utf8'));
  doc.nodes[0].label = '"; @import https://evil { ${secret} ; x -> y';
  fs.writeFileSync(input, JSON.stringify(doc));
  const output = path.join(tmp, 'hostile.d2');
  const result = run(['render', 'workflow', input, output, '--format', 'd2']);
  assert.equal(result.status, 0, result.stderr);
  const source = fs.readFileSync(output, 'utf8');
  assert.match(source, /\\\$\{secret\}/);
  assert.doesNotMatch(source, /^@import/m);
});

test('cli: minimum adversarial label corpus remains inert after real D2 validation', () => {
  const input = path.join(skillRoot, 'examples/agent-tool-call.workflow.json');
  const cases = [
    ['quotes', '"quoted"'],
    ['backslashes', 'path\\to\\file'],
    ['newlines', 'line one\nline two'],
    ['connection', 'foo -> bar'],
    ['comment', '# comment'],
    ['braces', '{ nested }'],
    ['semicolon', 'a; b'],
    ['import', '@import evil'],
    ['substitution', '${secret}'],
  ];
  for (const [name, label] of cases) {
    const hostileInput = path.join(tmp, `hostile-${name}.workflow.json`);
    const output = path.join(tmp, `hostile-${name}.d2`);
    const doc = JSON.parse(fs.readFileSync(input, 'utf8'));
    doc.nodes[0].label = label;
    fs.writeFileSync(hostileInput, JSON.stringify(doc));
    const result = run(['render', 'workflow', hostileInput, output, '--format', 'd2']);
    assert.equal(result.status, 0, `${name}: ${result.stderr}`);
    const source = fs.readFileSync(output, 'utf8');
    assert.doesNotMatch(source, /^\s*@import/m);
    assert.equal(parseD2Semantics(source).edges.length, doc.edges.length);
  }
});

test('cli: combined D2 failure preserves pre-existing siblings', () => {
  const input = path.join(skillRoot, 'examples/agent-tool-call.workflow.json');
  const html = path.join(tmp, 'existing.html');
  const d2 = path.join(tmp, 'existing.d2');
  fs.writeFileSync(html, 'old html');
  fs.writeFileSync(d2, 'old d2');
  const result = run(['render', 'workflow', input, html, '--format', 'html+d2'], {
    env: { ...process.env, PATH: path.join(tmp, 'no-d2') },
  });
  assert.notEqual(result.status, 0);
  assert.equal(fs.readFileSync(html, 'utf8'), 'old html');
  assert.equal(fs.readFileSync(d2, 'utf8'), 'old d2');
});

test('cli: degraded D2 validation rejects unknown relations before D2 lookup', () => {
  const input = path.join(tmp, 'bad-d2.workflow.json');
  const doc = JSON.parse(fs.readFileSync(path.join(skillRoot, 'examples/agent-tool-call.workflow.json'), 'utf8'));
  doc.edges[0].to = 'ghost';
  fs.writeFileSync(input, JSON.stringify(doc));
  const result = run(['render', 'workflow', input, path.join(tmp, 'bad-d2.d2'), '--format', 'd2'], {
    env: { ...process.env, PATH: path.join(tmp, 'no-d2') },
  });
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /Edge references unknown target "ghost"/);
});

test('cli: degraded D2 validation rejects malformed ownership and ordering', () => {
  const cases = [
    ['dataflow', 'product-analytics.dataflow.json', (doc) => { doc.nodes[0].stage = 99; }, /invalid stage 99/],
    ['workflow', 'agent-tool-call.workflow.json', (doc) => { doc.nodes[1].id = doc.nodes[0].id; }, /duplicate id/],
    ['sequence', 'cache-miss-request.sequence.json', (doc) => { doc.segments[1].from = 0; }, /segments must be ordered/],
    ['sequence', 'cache-miss-request.sequence.json', (doc) => { doc.segments[0].to = doc.segments[0].from; }, /invalid range/],
    ['workflow', 'agent-tool-call.workflow.json', (doc) => { doc.mainPath[1] = 'ghost'; }, /mainPath references unknown node/],
  ];
  for (const [index, [type, example, mutate, expected]] of cases.entries()) {
    const input = path.join(tmp, `malformed-${type}-${index}.json`);
    const doc = JSON.parse(fs.readFileSync(path.join(skillRoot, 'examples', example), 'utf8'));
    mutate(doc);
    fs.writeFileSync(input, JSON.stringify(doc));
    const result = run(['render', type, input, path.join(tmp, `malformed-${type}.d2`), '--format', 'd2'], {
      env: { ...process.env, PATH: path.join(tmp, 'no-d2') },
    });
    assert.notEqual(result.status, 0, `${type} malformed input unexpectedly rendered`);
    assert.match(result.stderr, expected);
  }
});

test('cli: architecture and workflow reject ambiguous grouping and malformed ownership ids', () => {
  const cases = [
    ['architecture', 'web-app.architecture.json', (doc) => { doc.boundaries = [{ kind: 'region', label: 'A', wraps: ['lb', 'api'] }, { kind: 'region', label: 'B', wraps: ['api', 'cache'] }]; }, /overlap without strict nesting/],
    ['architecture', 'web-app.architecture.json', (doc) => { doc.boundaries = [{ kind: 'region', label: 'A', wraps: ['lb'] }, { kind: 'region', label: 'B', wraps: ['lb'] }]; }, /overlap without strict nesting/],
    ['workflow', 'agent-tool-call.workflow.json', (doc) => { doc.groups = [{ id: 'a', label: 'A', lane: 'agent', fromCol: 1, toCol: 3 }, { id: 'b', label: 'B', lane: 'agent', fromCol: 2, toCol: 4 }]; }, /belongs to overlapping groups/],
    ['workflow', 'agent-tool-call.workflow.json', (doc) => { doc.lanes[0].id = ''; }, /Workflow lanes ids must be well-formed|must match pattern/],
    ['lifecycle', 'agent-run.lifecycle.json', (doc) => { doc.lanes[1].id = doc.lanes[0].id; }, /Lifecycle lanes contains duplicate id/],
  ];
  for (const [index, [type, example, mutate, expected]] of cases.entries()) {
    const input = path.join(tmp, `ownership-${index}.json`);
    const doc = JSON.parse(fs.readFileSync(path.join(skillRoot, 'examples', example), 'utf8'));
    mutate(doc);
    fs.writeFileSync(input, JSON.stringify(doc));
    const result = run(['render', type, input, path.join(tmp, `ownership-${index}.d2`), '--format', 'd2'], { env: { ...process.env, PATH: path.join(tmp, 'no-d2') } });
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, expected);
  }
});

function decodeD2String(value) {
  return JSON.parse(value.replace(/\\\$\{/g, '${'));
}

function parseD2Semantics(source) {
  const declarations = [];
  const declarationByKey = new Map();
  const declarationGroups = new Map();
  const containerLabelOccurrences = new Map();
  const edges = [];
  const containers = [];
  for (const rawLine of source.split('\n')) {
    const line = rawLine.trimEnd();
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const indent = line.length - line.trimStart().length;
    while (containers.length && indent <= containers.at(-1).indent) containers.pop();
    const containerMatch = trimmed.match(/^([A-Za-z][A-Za-z0-9_-]*):\s*\{$/);
    if (containerMatch) {
      containers.push({ key: containerMatch[1], indent });
      continue;
    }
    if (trimmed === '}') continue;
    const declarationMatch = trimmed.match(/^([A-Za-z][A-Za-z0-9_-]*):\s*("(?:\\.|[^"\\])*")$/);
    if (declarationMatch) {
      const value = decodeD2String(declarationMatch[2]);
      if (declarationMatch[1] === 'label') {
        if (containers.length) {
          const parentPath = containers.slice(0, -1).map((container) => container.semanticIdentity);
          const occurrenceKey = JSON.stringify([parentPath, value]);
          const occurrence = containerLabelOccurrences.get(occurrenceKey) || 0;
          containerLabelOccurrences.set(occurrenceKey, occurrence + 1);
          containers.at(-1).semanticIdentity = [value, occurrence];
        }
      } else {
        const qualifiedKey = [...containers.map((container) => container.key), declarationMatch[1]].join('.');
        const groupKey = JSON.stringify(containers.map((container) => container.semanticIdentity));
        declarations.push(value);
        if (!declarationGroups.has(groupKey)) declarationGroups.set(groupKey, []);
        declarationGroups.get(groupKey).push(value);
        if (!declarationByKey.has(qualifiedKey)) declarationByKey.set(qualifiedKey, value);
      }
      continue;
    }
    const edgeMatch = trimmed.match(/^(.+?)\s+->\s+(.+?)(?::\s*(.+))?$/);
    if (edgeMatch) {
      const label = edgeMatch[3] ? decodeD2String(edgeMatch[3]) : '';
      edges.push({
        from: edgeMatch[1].trim(),
        to: edgeMatch[2].trim(),
        label,
      });
      continue;
    }
  }
  const labelForKey = (key) => declarationByKey.get(key) ?? (() => { throw new Error(`D2 semantic oracle could not resolve endpoint ${key}.`); })();
  return {
    entities: declarations,
    edges: edges.map((edge) => ({ from: labelForKey(edge.from), to: labelForKey(edge.to), label: edge.label })),
    groups: declarationGroups,
  };
}

function sortedD2Edges(edges) {
  return [...edges].sort((left, right) => JSON.stringify(left).localeCompare(JSON.stringify(right)));
}

function assertD2Semantics(source, expectedLabels, expectedEdges, type, expectedGroups = []) {
  const actual = parseD2Semantics(source);
  assert.deepEqual([...actual.entities].sort(), [...expectedLabels].sort(), `${type} entity multiplicity oracle mismatch`);
  assert.deepEqual(sortedD2Edges(actual.edges), sortedD2Edges(expectedEdges), `${type} directed relationship oracle mismatch`);
  for (const [path, values] of expectedGroups) assert.deepEqual(actual.groups.get(JSON.stringify(path)), values, `${type} semantic group oracle mismatch for ${path.map(([label, occurrence]) => `${label}#${occurrence}`).join(' / ') || 'root'}`);
}

const GENERATED_D2_KEY_PATTERN = /\b(?:(?:boundary|lane|group|stage|segment|phase|component|node|participant|state)_\d+(?:_\d+)?|main_path)\b/;

function d2KeyRegions(source) {
  return source.split('\n').filter((line) => !line.trimStart().startsWith('#')).map((line) => {
    const quotedContent = line.indexOf('"');
    return quotedContent === -1 ? line : line.slice(0, quotedContent);
  }).join('\n');
}

function renameGeneratedD2Keys(source) {
  const replacements = new Map();
  return source.split('\n').map((line) => {
    if (line.trimStart().startsWith('#')) return line;
    const quotedContent = line.indexOf('"');
    const keyRegion = quotedContent === -1 ? line : line.slice(0, quotedContent);
    const suffix = quotedContent === -1 ? '' : line.slice(quotedContent);
    return keyRegion.replace(new RegExp(GENERATED_D2_KEY_PATTERN.source, 'g'), (generatedKey) => {
      if (!replacements.has(generatedKey)) replacements.set(generatedKey, `key_${replacements.size + 1}`);
      return replacements.get(generatedKey);
    }) + suffix;
  }).join('\n');
}

function reverseFirstD2Edge(source) {
  let reversed = false;
  const mutated = source.split('\n').map((line) => {
    if (reversed) return line;
    const match = line.match(/^(\s*)([A-Za-z][A-Za-z0-9_.-]*)\s+->\s+([A-Za-z][A-Za-z0-9_.-]*)(.*)$/);
    if (!match) return line;
    reversed = true;
    return `${match[1]}${match[3]} -> ${match[2]}${match[4]}`;
  }).join('\n');
  assert.equal(reversed, true, 'D2 mutation fixture did not find an edge');
  return mutated;
}

function swapD2Labels(source, left, right) {
  const leftToken = JSON.stringify(left);
  const rightToken = JSON.stringify(right);
  const markerToken = JSON.stringify('Archify oracle temporary label');
  assert.equal(source.includes(markerToken), false);
  assert.equal(source.includes(leftToken), true, `D2 label-swap fixture did not find ${leftToken}`);
  assert.equal(source.includes(rightToken), true, `D2 label-swap fixture did not find ${rightToken}`);
  return source
    .replace(leftToken, () => markerToken)
    .replace(rightToken, () => leftToken)
    .replace(markerToken, () => rightToken);
}

test('cli: semantic oracle keeps duplicate-labeled containers and quoted generated-looking text distinct', () => {
  const source = [
    'lane_1: {',
    '  label: "Same lane"',
    '  node_1: "$& node_1 main_path"',
    '}',
    'lane_2: {',
    '  label: "Same lane"',
    '  node_2: "Second"',
    '}',
  ].join('\n');
  const firstGroup = JSON.stringify([["Same lane", 0]]);
  const secondGroup = JSON.stringify([["Same lane", 1]]);
  const parsed = parseD2Semantics(source);
  assert.deepEqual(parsed.groups.get(firstGroup), ['$& node_1 main_path']);
  assert.deepEqual(parsed.groups.get(secondGroup), ['Second']);
  const renamed = renameGeneratedD2Keys(source);
  assert.notEqual(renamed, source);
  assert.doesNotMatch(d2KeyRegions(renamed), GENERATED_D2_KEY_PATTERN);
  assert.deepEqual(parseD2Semantics(renamed).entities, parsed.entities);
  const swapped = parseD2Semantics(swapD2Labels(source, '$& node_1 main_path', 'Second'));
  assert.deepEqual(swapped.groups.get(firstGroup), ['Second']);
  assert.deepEqual(swapped.groups.get(secondGroup), ['$& node_1 main_path']);
});

test('cli: all five D2 adapters preserve entity labels and directed labeled relationships', () => {
  const cases = [
    ['architecture', 'web-app.architecture.json'],
    ['workflow', 'agent-tool-call.workflow.json'],
    ['sequence', 'cache-miss-request.sequence.json'],
    ['dataflow', 'product-analytics.dataflow.json'],
    ['lifecycle', 'agent-run.lifecycle.json'],
  ];
  for (const [type, example] of cases) {
    const input = path.join(skillRoot, 'examples', example);
    const output = path.join(tmp, `semantic-${type}.d2`);
    const doc = JSON.parse(fs.readFileSync(input, 'utf8'));
    const result = run(['render', type, input, output, '--format', 'd2']);
    assert.equal(result.status, 0, `${type}: ${result.stderr}`);
    const source = fs.readFileSync(output, 'utf8');
    const entities = doc.components || doc.nodes || doc.participants || doc.states;
    const labelFor = (entity) => {
      const suffix = type === 'lifecycle' ? [entity.type, entity.tag].filter(Boolean).join(', ') : '';
      return `${entity.sublabel ? `${entity.label} — ${entity.sublabel}` : entity.label}${suffix ? ` [${suffix}]` : ''}`;
    };
    const expectedLabels = entities.map(labelFor);
    if (type === 'workflow') {
      expectedLabels.push(...(doc.phases || []).map((phase) => phase.label));
      if (doc.mainPath) expectedLabels.push(`Main path: ${doc.mainPath.join(' → ')}`);
    }
    const expectedGroups = [];
    if (type === 'workflow') expectedGroups.push([[], [
      ...[...(doc.phases || [])].sort((left, right) => left.fromCol - right.fromCol).map((phase) => phase.label),
      ...(doc.mainPath ? [`Main path: ${doc.mainPath.join(' → ')}`] : []),
    ]]);
    if (type === 'lifecycle') {
      const laneLabelOccurrences = new Map();
      for (const lane of doc.lanes) {
        const occurrence = laneLabelOccurrences.get(lane.label) || 0;
        laneLabelOccurrences.set(lane.label, occurrence + 1);
        expectedGroups.push([[[lane.label, occurrence]], doc.states.filter((state) => state.lane === lane.id).sort((left, right) => left.col - right.col).map(labelFor)]);
      }
    }
    const relations = doc.connections || doc.edges || doc.messages || doc.flows || doc.transitions;
    const expectedEdges = relations.map((relation) => {
      const fromEntity = entities.find((item) => item.id === relation.from);
      const toEntity = entities.find((item) => item.id === relation.to);
      const label = relation.label ? `${relation.label}${relation.classification ? ` — ${relation.classification}` : ''}` : null;
      return { from: labelFor(fromEntity), to: labelFor(toEntity), label: label || '' };
    });
    assertD2Semantics(source, expectedLabels, expectedEdges, type, expectedGroups);
    const renamedSource = renameGeneratedD2Keys(source);
    assert.match(d2KeyRegions(source), GENERATED_D2_KEY_PATTERN, `${type} key-refactor fixture has no generated key to challenge`);
    assert.doesNotMatch(d2KeyRegions(renamedSource), GENERATED_D2_KEY_PATTERN, `${type} key-refactor fixture left a generated key position unchanged`);
    assert.doesNotThrow(() => assertD2Semantics(renamedSource, expectedLabels, expectedEdges, type, expectedGroups), `${type} semantic oracle depends on generated keys`);
    assert.throws(() => assertD2Semantics(reverseFirstD2Edge(source), expectedLabels, expectedEdges, type, expectedGroups), /directed relationship oracle mismatch/, `${type} semantic oracle does not detect reversed direction`);
    assert.throws(() => assertD2Semantics(`${source}\nphantom_vertex: "Unexpected phantom"\n`, expectedLabels, expectedEdges, type, expectedGroups), /entity multiplicity oracle mismatch/, `${type} semantic oracle does not detect an extra entity`);
    if (type === 'workflow') assert.throws(() => assertD2Semantics(swapD2Labels(source, doc.phases[0].label, doc.phases[1].label), expectedLabels, expectedEdges, type, expectedGroups), /semantic group oracle mismatch/, 'workflow semantic oracle does not detect swapped edge-free phase labels');
    if (type === 'lifecycle') assert.throws(() => assertD2Semantics(swapD2Labels(source, labelFor(doc.states[0]), labelFor(doc.states[1])), expectedLabels, expectedEdges, type, expectedGroups), /semantic group oracle mismatch/, 'lifecycle semantic oracle does not detect swapped edge-free state labels');
    const compile = spawnSync('d2', [output, `${output}.svg`], { encoding: 'utf8' });
    assert.equal(compile.status, 0, `${type}: ${compile.stderr}`);
  }
});

test('cli: grouped entities compile without extra shapes', () => {
  const examples = [
    ['architecture', 'web-app.architecture.json'],
    ['workflow', 'agent-tool-call.workflow.json'],
    ['sequence', 'cache-miss-request.sequence.json'],
    ['dataflow', 'product-analytics.dataflow.json'],
    ['lifecycle', 'agent-run.lifecycle.json'],
  ];
  for (const [type, example] of examples) {
    const d2Path = path.join(tmp, `${type}-grouped.d2`);
    const svgPath = path.join(tmp, `${type}-grouped.svg`);
    const input = path.join(skillRoot, 'examples', example);
    const doc = JSON.parse(fs.readFileSync(input, 'utf8'));
    const result = run(['render', type, input, d2Path, '--format', 'd2']);
    assert.equal(result.status, 0, result.stderr);
    const compile = spawnSync('d2', [d2Path, svgPath], { encoding: 'utf8' });
    assert.equal(compile.status, 0, compile.stderr);
    const svg = fs.readFileSync(svgPath, 'utf8');
    const expectedShapeCount = type === 'architecture'
      ? doc.components.length + (doc.boundaries || []).length
      : type === 'workflow'
        ? doc.lanes.length + doc.nodes.length + (doc.groups || []).length + (doc.phases || []).length + (doc.mainPath ? 1 : 0)
        : type === 'sequence'
          ? doc.participants.length
          : type === 'dataflow'
            ? doc.stages.length + doc.nodes.length
            : doc.lanes.length + doc.states.length;
    assert.equal(svg.match(/<g class="[^"]+"><g class="shape"/g)?.length || 0, expectedShapeCount, `${type} compiled an unexpected shape`);
  }
});

test('cli: injected mid-publication failure restores both original siblings', () => {
  const input = path.join(skillRoot, 'examples/agent-tool-call.workflow.json');
  const html = path.join(tmp, 'mid-failure.html');
  const d2 = path.join(tmp, 'mid-failure.d2');
  fs.writeFileSync(html, 'old html');
  fs.writeFileSync(d2, 'old d2');
  const result = run(['render', 'workflow', input, html, '--format', 'html+d2'], {
    env: { ...process.env, ARCHIFY_TEST_FAIL_AFTER_PUBLISH: '1' },
  });
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /injected publication failure/);
  assert.equal(fs.readFileSync(html, 'utf8'), 'old html');
  assert.equal(fs.readFileSync(d2, 'utf8'), 'old d2');
  assert.equal(fs.readdirSync(tmp).some((name) => name.includes('.archify-backup-')), false);
});

test('cli: injected combined failure cleans isolated temp and staging paths', () => {
  const input = path.join(skillRoot, 'examples/agent-tool-call.workflow.json');
  const isolated = path.join(tmp, 'isolated-tmp');
  const outputDir = path.join(tmp, 'isolated-publication');
  fs.mkdirSync(isolated);
  fs.mkdirSync(outputDir);
  const html = path.join(outputDir, 'diagram.html');
  const d2 = path.join(outputDir, 'diagram.d2');
  fs.writeFileSync(html, 'old html');
  fs.writeFileSync(d2, 'old d2');
  const result = run(['render', 'workflow', input, html, '--format', 'html+d2'], { env: { ...process.env, TMPDIR: isolated, ARCHIFY_TEST_FAIL_AFTER_PUBLISH: '1' } });
  assert.notEqual(result.status, 0);
  assert.equal(fs.readFileSync(html, 'utf8'), 'old html');
  assert.equal(fs.readFileSync(d2, 'utf8'), 'old d2');
  assert.deepEqual(fs.readdirSync(isolated), []);
  assert.deepEqual(fs.readdirSync(outputDir).sort(), ['diagram.d2', 'diagram.html']);
});

process.on('exit', () => fs.rmSync(tmp, { recursive: true, force: true }));
