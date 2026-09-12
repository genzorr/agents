#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { renderD2, validateD2 } from '../renderers/shared/d2.mjs';
import { validateSchema } from '../renderers/shared/validator.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillRoot = path.resolve(__dirname, '..');

const TYPES = new Set(['architecture', 'workflow', 'sequence', 'dataflow', 'lifecycle']);

function usage() {
  return `Usage:
  archify render <type> <input.json> [output.html] [--format html|d2|html+d2] [--presentation editorial|interactive|classic]
  archify validate <type> <input.json> [--json]
  archify check <output.html>
  archify examples

Types:
  architecture, workflow, sequence, dataflow, lifecycle
`;
}

function fail(message, code = 2) {
  console.error(message);
  process.exit(code);
}

function rendererPath(type) {
  if (!TYPES.has(type)) {
    fail(`Unknown diagram type "${type}". Expected one of: ${[...TYPES].join(', ')}`);
  }
  return path.join(skillRoot, 'renderers', type, `render-${type}.mjs`);
}

function runNode(args, options = {}) {
  return spawnSync(process.execPath, args, {
    cwd: options.cwd || process.cwd(),
    encoding: 'utf8',
    env: options.env || process.env,
    stdio: options.stdio || 'inherit',
  });
}

function exitFrom(result) {
  if (result.error) fail(result.error.message, 1);
  process.exit(result.status ?? 1);
}

function parseRenderArgs(args) {
  let format = 'html';
  let presentation = 'editorial';
  let sawFormat = false;
  let sawPresentation = false;
  const positional = [];
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === '--format' || arg === '--presentation') {
      const value = args[index + 1];
      if (!value || value.startsWith('--')) fail(usage());
      if (arg === '--format') {
        if (sawFormat) fail(usage());
        format = value;
        sawFormat = true;
      } else {
        if (sawPresentation) fail(usage());
        presentation = value;
        sawPresentation = true;
      }
      index += 1;
      continue;
    }
    if (arg.startsWith('--')) fail(`Unknown render option "${arg}".\n\n${usage()}`);
    positional.push(arg);
  }
  if (!['html', 'd2', 'html+d2'].includes(format)) fail(`Unknown format "${format}". Expected one of: html, d2, html+d2`);
  if (!['editorial', 'interactive', 'classic'].includes(presentation)) fail(`Unknown presentation "${presentation}". Expected one of: editorial, interactive, classic`);
  const [type, input, output] = positional;
  if (!type || !input || positional.length > 3) fail(usage());
  if (format === 'd2' && sawPresentation) fail('The --presentation selector applies only to HTML output.');
  return { type, input, output, format, presentation };
}

function artifactPaths(type, input, output, format) {
  const diagram = output ? null : JSON.parse(fs.readFileSync(input, 'utf8'));
  const configured = output || diagram?.meta?.output;
  if (format === 'html') return { html: path.resolve(process.cwd(), configured || `${type}.html`) };
  const base = path.resolve(process.cwd(), configured || `${type}.${format === 'd2' ? 'd2' : 'html'}`);
  const ext = path.extname(base).toLowerCase();
  if (format === 'd2') {
    if (ext === '.html') {
      if (output) fail('D2 output paths cannot use the .html extension.');
      return { d2: `${base.slice(0, -'.html'.length)}.d2` };
    }
    return { d2: ext === '.d2' ? base : `${base}.d2` };
  }
  if (ext === '.d2') fail('Combined output paths must use a .html extension or a stem.');
  const html = ext === '.html' ? base : `${base}.html`;
  return { html, d2: `${html.slice(0, -'.html'.length)}.d2` };
}

function publishFiles(files) {
  const staged = [];
  try {
    for (const { destination, content } of files) {
      fs.mkdirSync(path.dirname(destination), { recursive: true });
      const temp = path.join(path.dirname(destination), `.${path.basename(destination)}.archify-${process.pid}-${Math.random().toString(16).slice(2)}`);
      fs.writeFileSync(temp, content);
      staged.push({ destination, temp, backup: null, published: false });
    }
  } catch (error) {
    for (const item of staged) try { fs.unlinkSync(item.temp); } catch {}
    throw error;
  }
  try {
    for (const [index, item] of staged.entries()) {
      if (fs.existsSync(item.destination)) {
        item.backup = `${item.destination}.archify-backup-${process.pid}`;
        fs.renameSync(item.destination, item.backup);
      }
      fs.renameSync(item.temp, item.destination);
      item.published = true;
      if (process.env.ARCHIFY_TEST_FAIL_AFTER_PUBLISH === '1' && index === 0) throw new Error('injected publication failure');
    }
  } catch (error) {
    for (const item of staged) {
      try { if (item.published && fs.existsSync(item.destination)) fs.unlinkSync(item.destination); } catch {}
      try { if (item.backup && fs.existsSync(item.backup)) fs.renameSync(item.backup, item.destination); } catch {}
      try { if (fs.existsSync(item.temp)) fs.unlinkSync(item.temp); } catch {}
    }
    throw error;
  }
  // Backup cleanup is post-commit housekeeping. A cleanup failure must not roll back
  // already-published siblings or turn a successful publication into a partial restore.
  for (const item of staged) {
    if (!item.backup) continue;
    try { fs.unlinkSync(item.backup); } catch (error) { console.error(`Warning: could not remove backup ${item.backup}: ${error.message}`); }
  }
}

function commandRender(args) {
  const { type, input, output, format, presentation } = parseRenderArgs(args);
  const paths = artifactPaths(type, input, output, format);
  const renderEnv = { ...process.env, ARCHIFY_PRESENTATION: presentation };
  if (format === 'html') {
    const result = runNode([rendererPath(type), input, paths.html], { env: renderEnv });
    if (result.status !== 0) exitFrom(result);
    return;
  }
  const diagram = JSON.parse(fs.readFileSync(input, 'utf8'));
  let d2;
  try {
    validateSchema(type, diagram);
    d2 = validateD2(renderD2(diagram, type), type);
  } catch (error) {
    fail(error.message, 1);
  }
  if (format === 'd2') {
    try { publishFiles([{ destination: paths.d2, content: d2.source }]); } catch (error) { fail(`Could not publish D2 output: ${error.message}`, 1); }
    console.log(paths.d2);
    return;
  }
  const htmlTmp = path.join(os.tmpdir(), `archify-html-${process.pid}-${Math.random().toString(16).slice(2)}.html`);
  const render = runNode([rendererPath(type), input, htmlTmp], { stdio: 'pipe', env: renderEnv });
  if (render.status !== 0) {
    if (render.stderr) process.stderr.write(render.stderr);
    try { fs.unlinkSync(htmlTmp); } catch {}
    fail('HTML rendering failed; combined output was not published.', render.status ?? 1);
  }
  let publishError = null;
  try {
    publishFiles([
      { destination: paths.html, content: fs.readFileSync(htmlTmp, 'utf8') },
      { destination: paths.d2, content: d2.source },
    ]);
  } catch (error) {
    publishError = error;
  } finally {
    try { fs.unlinkSync(htmlTmp); } catch {}
  }
  if (publishError) fail(`Could not publish combined output: ${publishError.message}`, 1);
  console.log(`${paths.html}\n${paths.d2}`);
}

function commandCheck(args) {
  const [html] = args;
  if (!html) fail(usage());
  const result = runNode([path.join(skillRoot, 'scripts/check-render-output.mjs'), html]);
  if (result.status !== 0) exitFrom(result);
}

function commandExamples() {
  const result = runNode([path.join(skillRoot, 'test/render-examples.mjs')], { cwd: skillRoot });
  if (result.status !== 0) exitFrom(result);
}

function commandValidate(args) {
  const json = args.includes('--json');
  const rest = args.filter((arg) => arg !== '--json');
  const [type, input] = rest;
  if (!type || !input) fail(usage());

  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'archify-validate-'));
  const out = path.join(tmp, `${type}.html`);
  let exitCode = 0;

  try {
    const render = runNode([rendererPath(type), input, out], { stdio: 'pipe' });
    if (render.status !== 0) {
      if (render.stderr) process.stderr.write(render.stderr);
      if (render.stdout) process.stdout.write(render.stdout);
      exitCode = render.status ?? 1;
    } else {
      const check = runNode([path.join(skillRoot, 'scripts/check-render-output.mjs'), out], { stdio: 'pipe' });
      if (check.status !== 0) {
        if (check.stdout) process.stdout.write(check.stdout);
        if (check.stderr) process.stderr.write(check.stderr);
        exitCode = check.status ?? 1;
      } else {
        const result = JSON.parse(check.stdout);
        if (json) {
          console.log(JSON.stringify({
            ok: true,
            type,
            input: path.resolve(input),
            checks: result.checks,
          }, null, 2));
        } else {
          console.log(`ok ${type} ${path.resolve(input)} (${result.checks.length} checks)`);
        }
      }
    }
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }

  if (exitCode !== 0) process.exit(exitCode);
}

const [command, ...args] = process.argv.slice(2);

switch (command) {
  case undefined:
  case '-h':
  case '--help':
  case 'help':
    console.log(usage());
    break;
  case 'render':
    commandRender(args);
    break;
  case 'validate':
    commandValidate(args);
    break;
  case 'check':
    commandCheck(args);
    break;
  case 'examples':
    commandExamples();
    break;
  default:
    fail(`Unknown command "${command}".\n\n${usage()}`);
}
