import test from "node:test";
import assert from "node:assert/strict";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";

const sdk = process.env.PI_SDK_ROOT ?? path.join(os.homedir(), ".local/lib/node_modules/@earendil-works/pi-coding-agent");
const available = existsSync(path.join(sdk, "dist/core/extensions/loader.js"));

test("Pi's real loader registers file guards, denies missing UI, and retains allowed write behavior", { skip: !available }, async () => {
  const scratch = mkdtempSync(path.join(os.tmpdir(), "pi-permission-loader-"));
  try {
    const installed = path.join(scratch, ".local/lib/pi-agentic-local/permissions");
    cpSync(new URL("../../pi/permissions", import.meta.url), installed, { recursive: true });
    const { loadExtensions } = await import(pathToFileURL(path.join(sdk, "dist/core/extensions/loader.js")));
    const loaded = await loadExtensions([path.join(installed, "index.ts")], scratch);
    assert.deepEqual(loaded.errors, []);
    const tools = loaded.extensions[0].tools;
    const ctx = { cwd: scratch, hasUI: false };
    for (const name of ["write", "edit"]) {
      await assert.rejects(tools.get(name).definition.execute("deny", { path: "/outside-agentic-local-denied", content: "denied", edits: [] }, undefined, undefined, ctx), /denied|unavailable/);
    }
    await assert.rejects(tools.get("bash_unrestricted").definition.execute("deny", { command: "exit 99" }, undefined, undefined, ctx), /denied|unavailable/);
    const target = path.join(scratch, "allowed-file");
    await tools.get("write").definition.execute("write", { path: target, content: "before" }, undefined, undefined, ctx);
    await tools.get("edit").definition.execute("edit", { path: target, edits: [{ oldText: "before", newText: "after" }] }, undefined, undefined, ctx);
    const { readFileSync } = await import("node:fs");
    assert.equal(readFileSync(target, "utf8"), "after");
    const blocked = await loaded.extensions[0].handlers.get("tool_call")[0]({ toolName: "foreign_mcp", input: {} }, ctx);
    assert.equal(blocked.block, true);
    let approvalDetail;
    const approveCtx = { ...ctx, hasUI: true, ui: { confirm: async (_title, detail) => { approvalDetail = detail; return true; } } };
    const approved = await loaded.extensions[0].handlers.get("tool_call")[0]({ toolName: "foreign_mcp", input: { path: "/synthetic/outside", operation: "write" } }, approveCtx);
    assert.equal(approved, undefined);
    assert.match(approvalDetail, /foreign_mcp/);
    assert.match(approvalDetail, /\/synthetic\/outside/);
    assert.match(approvalDetail, /write/);
  } finally { rmSync(scratch, { recursive: true, force: true }); }
});

test("real Pi file tools deny relative symlink targets whose traversal escapes a writable root", { skip: !available }, async () => {
  const scratch = mkdtempSync(path.join(os.tmpdir(), "pi-permission-relative-link-"));
  try {
    const installed = path.join(scratch, ".local/lib/pi-agentic-local/permissions");
    cpSync(new URL("../../pi/permissions", import.meta.url), installed, { recursive: true });
    const allowed = path.join(scratch, "allowed");
    const outside = path.join(scratch, "outside");
    mkdirSync(allowed);
    mkdirSync(path.join(outside, "subdir"), { recursive: true });
    writeFileSync(path.join(installed, "profile.json"), JSON.stringify({ name: "agentic-local", writeRoots: [allowed] }));
    symlinkSync(path.join(outside, "subdir"), path.join(allowed, "nested"));
    symlinkSync("nested/../victim", path.join(allowed, "alias"));
    const victim = path.join(outside, "victim");
    writeFileSync(victim, "outside original");
    const { loadExtensions } = await import(pathToFileURL(path.join(sdk, "dist/core/extensions/loader.js")));
    const loaded = await loadExtensions([path.join(installed, "index.ts")], scratch);
    assert.deepEqual(loaded.errors, []);
    const tools = loaded.extensions[0].tools;
    const ctx = { cwd: allowed, hasUI: false };
    for (const name of ["write", "edit"]) {
      await assert.rejects(tools.get(name).definition.execute("denied", { path: "alias", content: "outside overwritten", edits: [{ oldText: "outside original", newText: "outside overwritten" }] }, undefined, undefined, ctx), /Outside-scope file write denied/);
      assert.equal(readFileSync(victim, "utf8"), "outside original");
    }
  } finally { rmSync(scratch, { recursive: true, force: true }); }
});

test("real Pi RPC emits confirmation, honors denial, and allows one fresh manual exception", { skip: !available, timeout: 30_000 }, async () => {
  const scratch = mkdtempSync(path.join(os.tmpdir(), "pi-permission-rpc-"));
  let child;
  try {
    const installed = path.join(scratch, ".local/lib/pi-agentic-local/permissions");
    cpSync(new URL("../../pi/permissions", import.meta.url), installed, { recursive: true });
    const agent = path.join(scratch, "agent");
    mkdirSync(agent);
    writeFileSync(path.join(agent, "settings.json"), "{}");
    const probe = path.join(scratch, "probe.ts");
    writeFileSync(probe, `import activate from ${JSON.stringify(path.join(installed, "index.ts"))};
export default function(pi) {
  const tools = new Map();
  activate(new Proxy(pi, { get(target, name) {
    if (name === 'registerTool') return (tool) => { tools.set(tool.name, tool); pi.registerTool(tool); };
    return target[name];
  }}));
  pi.registerCommand('permission-test', { description: 'Synthetic permission RPC test', async handler(_, ctx) {
    try {
      const result = await tools.get('bash_unrestricted').execute('probe', {command: 'printf approved'}, undefined, undefined, ctx);
      ctx.ui.notify('probe-allowed:' + result.content[0].text, 'info');
    } catch { ctx.ui.notify('probe-denied', 'info'); }
  }});
}`);
    child = spawn(process.execPath, [path.join(sdk, "dist/cli.js"), "--mode", "rpc", "--no-session", "--no-extensions", "--no-skills", "--no-prompt-templates", "--no-themes", "-e", probe], { cwd: scratch, env: { ...process.env, PI_CODING_AGENT_DIR: agent, HOME: scratch }, stdio: ["pipe", "pipe", "pipe"] });
    let stderr = "";
    child.stderr.on("data", (data) => { stderr += data; });
    const lines = createInterface({ input: child.stdout });
    const observed = [];
    let confirmations = 0;
    let resolveDone;
    const done = new Promise((resolve) => { resolveDone = resolve; });
    const send = (value) => child.stdin.write(JSON.stringify(value) + "\n");
    lines.on("line", (line) => {
      const event = JSON.parse(line);
      observed.push(event);
      if (event.type === "extension_ui_request" && event.method === "confirm") {
        confirmations++;
        assert.match(event.message, /printf approved/);
        send({ type: "extension_ui_response", id: event.id, confirmed: confirmations === 2 });
      }
      if (event.method === "notify" && event.message === "probe-denied") send({ type: "prompt", message: "/permission-test", id: "second" });
      if (event.method === "notify" && event.message === "probe-allowed:approved") resolveDone();
    });
    const exited = new Promise((_, reject) => child.once("exit", (code) => reject(new Error(`Pi exited ${code}: ${stderr}`))));
    send({ type: "prompt", message: "/permission-test", id: "first" });
    await Promise.race([done, exited, new Promise((_, reject) => setTimeout(() => reject(new Error(`RPC timeout: ${stderr}\n${JSON.stringify(observed)}`)), 15_000).unref())]);
    assert.equal(confirmations, 2);
    assert.equal(observed.some((event) => event.type === "agent_start"), false);
  } finally {
    if (child) { child.kill("SIGTERM"); await new Promise((resolve) => child.once("exit", resolve)); }
    rmSync(scratch, { recursive: true, force: true });
  }
});
