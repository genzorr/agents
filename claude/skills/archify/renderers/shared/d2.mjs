import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const D2_TYPES = new Set(['architecture', 'workflow', 'sequence', 'dataflow', 'lifecycle']);

export function d2String(value) {
  return JSON.stringify(String(value ?? '')).replace(/\$\{/g, '\\\${');
}

function key(prefix, index) {
  return `${prefix}_${index + 1}`;
}

function nodeLine(id, value) {
  return `  ${id}: ${d2String(value)}`;
}

function container(id, label, lines) {
  return [`  ${id}: {`, `    label: ${d2String(label)}`, ...lines.map((line) => `  ${line}`), '  }'];
}

function labelFor(item) {
  return item.sublabel ? `${item.label} — ${item.sublabel}` : item.label;
}

function scoped(prefix, id) {
  return [...prefix, id].join('.');
}

function requireKnown(map, value, relation, side) {
  if (!map.has(value)) throw new Error(`${relation} references unknown ${side} "${value}".`);
}

function validateIds(items, label) {
  const ids = new Set();
  for (const item of items) {
    const id = typeof item === 'string' ? item : item?.id;
    if (typeof id !== 'string' || !/^[a-zA-Z][a-zA-Z0-9_-]*$/.test(id)) throw new Error(`${label} ids must be well-formed strings; found ${JSON.stringify(id)}.`);
    if (ids.has(id)) throw new Error(`${label} contains duplicate id "${id}".`);
    ids.add(id);
  }
  return ids;
}

function validateRelations(diagram, type) {
  const requiredArrays = {
    architecture: ['components'],
    workflow: ['lanes', 'nodes', 'edges'],
    sequence: ['participants', 'messages'],
    dataflow: ['stages', 'nodes', 'flows'],
    lifecycle: ['lanes', 'states', 'transitions'],
  }[type];
  const optionalArrays = {
    architecture: ['boundaries', 'connections', 'cards'],
    workflow: ['groups', 'phases', 'mainPath', 'cards'],
    sequence: ['segments', 'activations', 'cards'],
    dataflow: ['cards'],
    lifecycle: ['cards'],
  }[type];
  for (const field of requiredArrays) if (!Array.isArray(diagram[field])) throw new Error(`${type} D2 input must include an array at "${field}".`);
  for (const field of optionalArrays) if (diagram[field] !== undefined && !Array.isArray(diagram[field])) throw new Error(`${type} D2 input field "${field}" must be an array when present.`);
  const entityField = { architecture: 'components', workflow: 'nodes', sequence: 'participants', dataflow: 'nodes', lifecycle: 'states' }[type];
  const entities = diagram[entityField];
  if (!Array.isArray(entities)) throw new Error(`${type} D2 input must include an array at "${entityField}".`);
  const nodes = new Set();
  for (const entity of entities) {
    if (!entity || typeof entity !== 'object' || typeof entity.id !== 'string') throw new Error(`${type} D2 input contains an invalid entity in "${entityField}".`);
    if (!/^[a-zA-Z][a-zA-Z0-9_-]*$/.test(entity.id)) throw new Error(`${type} entity ids must be well-formed strings; found ${JSON.stringify(entity.id)}.`);
    if (nodes.has(entity.id)) throw new Error(`${type} entities contains duplicate id "${entity.id}".`);
    nodes.add(entity.id);
  }
  const relations = { architecture: diagram.connections || [], workflow: diagram.edges, sequence: diagram.messages, dataflow: diagram.flows, lifecycle: diagram.transitions }[type];
  if (!Array.isArray(relations)) throw new Error(`${type} D2 input contains an invalid relation array.`);
  const relationName = { architecture: 'Connection', workflow: 'Edge', sequence: 'Message', dataflow: 'Flow', lifecycle: 'Transition' }[type];
  for (const relation of relations) {
    requireKnown(nodes, relation.from, relationName, 'source');
    requireKnown(nodes, relation.to, relationName, 'target');
  }
  if (type === 'architecture') {
    for (let left = 0; left < (diagram.boundaries || []).length; left += 1) for (let right = left + 1; right < (diagram.boundaries || []).length; right += 1) {
      const a = new Set(diagram.boundaries[left].wraps || []);
      const b = new Set(diagram.boundaries[right].wraps || []);
      const intersection = [...a].filter((id) => b.has(id));
      const nested = intersection.length > 0 && (intersection.length === a.size || intersection.length === b.size);
      if (intersection.length > 0 && (!nested || a.size === b.size)) throw new Error(`Architecture boundaries "${diagram.boundaries[left].label}" and "${diagram.boundaries[right].label}" overlap without strict nesting; make their wraps disjoint or use a strict subset.`);
    }
    for (const boundary of diagram.boundaries || []) {
      if (!Array.isArray(boundary.wraps)) throw new Error(`Boundary "${boundary.label}" must include an array at "wraps".`);
      for (const id of boundary.wraps) requireKnown(nodes, id, 'Boundary', 'component');
    }
  }
  if (type === 'workflow') {
    const lanes = validateIds(diagram.lanes, 'Workflow lanes');
    validateIds(diagram.groups || [], 'Workflow groups');
    validateIds(diagram.phases || [], 'Workflow phases');
    for (const node of diagram.nodes) {
      requireKnown(lanes, node.lane, 'Node', 'lane');
      if (!Number.isInteger(node.col) || node.col < 0 || node.col > 5) throw new Error(`Node "${node.id}" has an invalid column.`);
    }
    for (const group of diagram.groups || []) {
      requireKnown(lanes, group.lane, 'Group', 'lane');
      if (!Number.isInteger(group.fromCol) || !Number.isInteger(group.toCol) || group.fromCol < 0 || group.toCol > 5 || group.toCol < group.fromCol) throw new Error(`Group "${group.id}" has an invalid column range.`);
    }
    const claims = new Map();
    for (const group of diagram.groups || []) for (const node of diagram.nodes) if (node.lane === group.lane && node.col >= group.fromCol && node.col <= group.toCol) {
      const prior = claims.get(node.id);
      if (prior) throw new Error(`Workflow node "${node.id}" belongs to overlapping groups "${prior}" and "${group.id}"; make group ranges disjoint.`);
      claims.set(node.id, group.id);
    }
    for (const phase of diagram.phases || []) if (!Number.isInteger(phase.fromCol) || !Number.isInteger(phase.toCol) || phase.fromCol < 0 || phase.toCol > 5 || phase.toCol < phase.fromCol) throw new Error(`Phase "${phase.id}" has an invalid column range.`);
    if (diagram.mainPath) {
      if (!Array.isArray(diagram.mainPath) || diagram.mainPath.length < 2) throw new Error('Workflow mainPath must contain at least two node ids.');
      for (const id of diagram.mainPath) {
        if (typeof id !== 'string' || !/^[a-zA-Z][a-zA-Z0-9_-]*$/.test(id)) throw new Error(`Workflow mainPath ids must be well-formed strings; found ${JSON.stringify(id)}.`);
        requireKnown(nodes, id, 'Workflow mainPath', 'node');
      }
      for (let index = 1; index < diagram.mainPath.length; index += 1) {
        const from = diagram.mainPath[index - 1];
        const to = diagram.mainPath[index];
        if (!diagram.edges.some((edge) => edge.from === from && edge.to === to)) throw new Error(`Workflow mainPath has no edge from "${from}" to "${to}".`);
      }
    }
  }
  if (type === 'sequence') {
    validateIds(diagram.participants, 'Sequence participants');
    let previousFrom = -Infinity;
    for (const segment of diagram.segments || []) {
      if (!Number.isFinite(segment.from) || !Number.isFinite(segment.to) || segment.to <= segment.from) throw new Error(`Sequence segment "${segment.label}" has an invalid range.`);
      if (segment.from < previousFrom) throw new Error('Sequence segments must be ordered by increasing from position.');
      previousFrom = segment.from;
    }
    for (const message of diagram.messages) if (!Number.isFinite(message.y)) throw new Error(`Sequence message "${message.label}" has an invalid y position.`);
    for (const activation of diagram.activations || []) requireKnown(nodes, activation.participant, 'Activation', 'participant');
  }
  if (type === 'dataflow') {
    for (const node of diagram.nodes) if (!Number.isInteger(node.stage) || node.stage < 0 || node.stage >= diagram.stages.length) throw new Error(`Node "${node.id}" has an invalid stage ${node.stage}.`);
  }
  if (type === 'lifecycle') {
    const lanes = validateIds(diagram.lanes, 'Lifecycle lanes');
    validateIds(diagram.states, 'Lifecycle states');
    for (const state of diagram.states) requireKnown(lanes, state.lane, 'State', 'lane');
  }
}

function renderArchitecture(diagram) {
  const nodes = new Map(diagram.components.map((item, index) => [item.id, { ...item, key: key('component', index) }]));
  const boundaries = diagram.boundaries || [];
  const boundarySets = boundaries.map((boundary) => new Set(boundary.wraps || []));
  const parent = boundaries.map((boundary, index) => boundaries
    .map((candidate, candidateIndex) => ({ candidate, candidateIndex }))
    .filter(({ candidateIndex }) => candidateIndex !== index && boundarySets[candidateIndex].size > boundarySets[index].size && [...boundarySets[index]].every((id) => boundarySets[candidateIndex].has(id)))
    .sort(({ candidate: a }, { candidate: b }) => (a.wraps || []).length - (b.wraps || []).length)[0]?.candidateIndex ?? null);
  const assigned = new Set();
  const scopedKeys = new Map();
  const lines = ['direction: right'];
  function renderBoundary(boundaryIndex, prefix = []) {
    const boundary = boundaries[boundaryIndex];
    const boundaryKey = `boundary_${boundaryIndex + 1}`;
    const boundaryPrefix = [...prefix, boundaryKey];
    const children = [];
    for (const childIndex of parent.flatMap((value, index) => value === boundaryIndex ? [index] : [])) {
      children.push(...renderBoundary(childIndex, boundaryPrefix).map((line) => `  ${line}`));
    }
    const nestedIds = new Set(parent.flatMap((value, index) => value === boundaryIndex ? [...boundarySets[index]] : []));
    for (const id of boundary.wraps || []) {
      if (nestedIds.has(id)) continue;
      const item = nodes.get(id);
      if (!item || assigned.has(id)) continue;
      assigned.add(id);
      scopedKeys.set(id, scoped(boundaryPrefix, item.key));
      children.push(nodeLine(item.key, labelFor(item)).trimStart());
    }
    return container(boundaryKey, boundary.label, children);
  }
  boundaries.forEach((boundary, boundaryIndex) => { if (parent[boundaryIndex] === null) lines.push(...renderBoundary(boundaryIndex)); });
  for (const item of nodes.values()) if (!assigned.has(item.id)) {
    scopedKeys.set(item.id, item.key);
    lines.push(nodeLine(item.key, labelFor(item)));
  }
  for (const edge of diagram.connections || []) lines.push(`  ${scopedKeys.get(edge.from)} -> ${scopedKeys.get(edge.to)}${edge.label ? `: ${d2String(edge.label)}` : ''}`);
  return lines;
}

function renderWorkflow(diagram) {
  const nodes = new Map(diagram.nodes.map((item, index) => [item.id, { ...item, key: key('node', index) }]));
  const groups = diagram.groups || [];
  const lines = ['direction: right'];
  const grouped = new Set();
  const scopedKeys = new Map();
  for (const [laneIndex, lane] of diagram.lanes.entries()) {
    const laneKey = `lane_${laneIndex + 1}`;
    const children = [];
    for (const [groupIndex, group] of groups.filter((item) => item.lane === lane.id).entries()) {
      const groupKey = `group_${laneIndex + 1}_${groupIndex + 1}`;
      const groupChildren = [];
      for (const item of diagram.nodes.filter((node) => node.lane === lane.id && node.col >= group.fromCol && node.col <= group.toCol)) {
        const node = nodes.get(item.id);
        if (!node || grouped.has(item.id)) continue;
        grouped.add(item.id);
        scopedKeys.set(item.id, `${laneKey}.${groupKey}.${node.key}`);
        groupChildren.push(nodeLine(node.key, labelFor(node)).trimStart());
      }
      children.push(...container(groupKey, group.label, groupChildren));
    }
    for (const item of diagram.nodes.filter((node) => node.lane === lane.id)) {
      const node = nodes.get(item.id);
      if (node && !grouped.has(item.id)) {
        scopedKeys.set(item.id, `${laneKey}.${node.key}`);
        children.push(nodeLine(node.key, labelFor(node)).trimStart());
      }
    }
    lines.push(...container(laneKey, lane.label, children));
  }
  for (const phase of diagram.phases || []) lines.push(`  phase_${diagram.phases.indexOf(phase) + 1}: ${d2String(phase.label)}`);
  if (diagram.mainPath) lines.push(`  main_path: ${d2String(`Main path: ${diagram.mainPath.join(' → ')}`)}`);
  for (const edge of diagram.edges || []) lines.push(`  ${scopedKeys.get(edge.from)} -> ${scopedKeys.get(edge.to)}${edge.label ? `: ${d2String(edge.label)}` : ''}`);
  return lines;
}

function renderSequence(diagram) {
  const participants = new Map(diagram.participants.map((item, index) => [item.id, { ...item, key: key('participant', index) }]));
  const lines = ['shape: sequence_diagram'];
  for (const participant of participants.values()) lines.push(nodeLine(participant.key, labelFor(participant)));
  const groupedMessages = new Set();
  const messagesByY = [...diagram.messages].sort((a, b) => a.y - b.y);
  const events = (diagram.segments || []).map((segment, segmentIndex) => {
    const messages = [];
    for (const message of messagesByY) if (!groupedMessages.has(message) && message.y >= segment.from && message.y <= segment.to) {
      const from = participants.get(message.from);
      const to = participants.get(message.to);
      if (!from || !to) continue;
      groupedMessages.add(message);
      messages.push(`    ${from.key} -> ${to.key}: ${d2String(message.label || '')}`);
    }
    return { y: segment.from, lines: [`  segment_${segmentIndex + 1}: {`, `    label: ${d2String(segment.label)}`, ...messages, '  }'] };
  });
  for (const message of messagesByY) if (!groupedMessages.has(message)) {
    const from = participants.get(message.from);
    const to = participants.get(message.to);
    if (from && to) events.push({ y: message.y, lines: [`  ${from.key} -> ${to.key}: ${d2String(message.label || '')}`] });
  }
  for (const event of events.sort((a, b) => a.y - b.y)) lines.push(...event.lines);
  return lines;
}

function renderDataflow(diagram) {
  const nodes = new Map(diagram.nodes.map((item, index) => [item.id, { ...item, key: key('node', index) }]));
  const lines = ['direction: right'];
  const scopedKeys = new Map();
  for (const [stageIndex, stage] of diagram.stages.entries()) {
    const stageKey = `stage_${stageIndex + 1}`;
    const children = diagram.nodes.filter((item) => item.stage === stageIndex).map((item) => {
      scopedKeys.set(item.id, `${stageKey}.${nodes.get(item.id).key}`);
      return nodeLine(nodes.get(item.id).key, labelFor(item)).trimStart();
    });
    lines.push(...container(stageKey, stage.label, children));
  }
  for (const flow of diagram.flows || []) lines.push(`  ${scopedKeys.get(flow.from)} -> ${scopedKeys.get(flow.to)}${flow.label ? `: ${d2String(`${flow.label}${flow.classification ? ` — ${flow.classification}` : ''}`)}` : ''}`);
  return lines;
}

function renderLifecycle(diagram) {
  const states = new Map(diagram.states.map((item, index) => [item.id, { ...item, key: key('state', index) }]));
  const lines = ['direction: right'];
  const scopedKeys = new Map();
  for (const [laneIndex, lane] of diagram.lanes.entries()) {
    const laneKey = `lane_${laneIndex + 1}`;
    const children = diagram.states.filter((item) => item.lane === lane.id).map((item) => {
      scopedKeys.set(item.id, `${laneKey}.${states.get(item.id).key}`);
      const suffix = [item.type, item.tag].filter(Boolean).join(', ');
      return nodeLine(states.get(item.id).key, `${labelFor(item)}${suffix ? ` [${suffix}]` : ''}`).trimStart();
    });
    lines.push(...container(laneKey, lane.label, children));
  }
  for (const transition of diagram.transitions || []) lines.push(`  ${scopedKeys.get(transition.from)} -> ${scopedKeys.get(transition.to)}${transition.label ? `: ${d2String(transition.label)}` : ''}`);
  return lines;
}

export function renderD2(diagram, type) {
  if (!D2_TYPES.has(type)) throw new Error(`Unsupported D2 diagram type "${type}".`);
  validateRelations(diagram, type);
  const renderers = { architecture: renderArchitecture, workflow: renderWorkflow, sequence: renderSequence, dataflow: renderDataflow, lifecycle: renderLifecycle };
  const title = diagram.meta?.title || `${type} diagram`;
  return [
    `# Archify D2 source: ${d2String(title)}`,
    '# Generated from the typed Archify input; presentation-only HTML geometry is intentionally omitted.',
    'vars: {',
    '  d2-config: {',
    '    layout-engine: elk',
    '    theme-id: 0',
    '    dark-theme-id: 200',
    '  }',
    '}',
    ...renderers[type](diagram),
    '',
  ].join('\n');
}

function runD2(args, options = {}) {
  return spawnSync('d2', args, { cwd: options.cwd, encoding: 'utf8', stdio: 'pipe' });
}

export function validateD2(source, label = 'diagram') {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'archify-d2-'));
  const sourcePath = path.join(tempDir, `${label}.d2`);
  const svgPath = path.join(tempDir, `${label}.svg`);
  try {
    const version = runD2(['--version']);
    if (version.error || version.status !== 0) throw new Error('D2 is unavailable; HTML remains available, but D2 output requires a usable local d2 executable on PATH.');
    fs.writeFileSync(sourcePath, source);
    const fmt = runD2(['fmt', sourcePath]);
    if (fmt.status !== 0) throw new Error(`D2 formatting failed: ${(fmt.stderr || fmt.stdout || '').trim()}`);
    const check = runD2(['fmt', '--check', sourcePath]);
    if (check.status !== 0) throw new Error(`D2 format check failed: ${(check.stderr || check.stdout || '').trim()}`);
    const valid = runD2(['validate', sourcePath]);
    if (valid.status !== 0) throw new Error(`D2 validation failed: ${(valid.stderr || valid.stdout || '').trim()}`);
    const compile = runD2([sourcePath, svgPath]);
    if (compile.status !== 0) throw new Error(`D2 compilation failed: ${(compile.stderr || compile.stdout || '').trim()}`);
    return { source: fs.readFileSync(sourcePath, 'utf8'), version: (version.stdout || version.stderr || '').trim() };
  } finally {
    for (const file of [sourcePath, svgPath]) try { fs.unlinkSync(file); } catch {}
    try { fs.rmdirSync(tempDir); } catch {}
  }
}
