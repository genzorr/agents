import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillRoot = path.resolve(__dirname, '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'archify-smoke-'));

const targets = [
  ['workflow', 'agent-tool-call.workflow.json', 'workflow-agent-tool-call-rendered.html'],
  ['sequence', 'cache-miss-request.sequence.json', 'sequence-cache-miss-request.html'],
  ['dataflow', 'product-analytics.dataflow.json', 'dataflow-product-analytics.html'],
  ['lifecycle', 'agent-run.lifecycle.json', 'lifecycle-agent-run.html'],
  ['architecture', 'web-app.architecture.json', 'web-app-rendered.html'],
];

try {
  for (const [mode, input, output] of targets) {
    const html = path.join(tmp, output);
    execFileSync('node', [
      path.join(skillRoot, `renderers/${mode}/render-${mode}.mjs`),
      path.join(skillRoot, 'examples', input),
      html,
    ], { stdio: 'inherit' });
    execFileSync('node', [
      path.join(skillRoot, 'scripts/check-render-output.mjs'),
      html,
    ], { stdio: 'inherit' });
  }
  console.log('archify smoke render passed');
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
