import test from "node:test";
import assert from "node:assert/strict";
import { cpSync, existsSync, mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { ChildInheritance, loadRequiredChildApi } from "../../pi/permissions/child-inheritance.mjs";

const sdk = process.env.PI_SDK_ROOT ?? path.join(os.homedir(), ".local/lib/node_modules/@earendil-works/pi-coding-agent");
const plugin = process.env.PI_SUBAGENTS_ROOT ?? path.join(os.homedir(), ".pi/agent/npm/node_modules/pi-subagents");
const available = existsSync(path.join(plugin, "src/shared/required-child-extensions.js")) && existsSync(path.join(sdk, "dist/index.js"));

function fixture() {
  const root = mkdtempSync(path.join(os.tmpdir(), "pi-child-inheritance-"));
  const agent = path.join(root, "agent");
  mkdirSync(path.join(agent, "npm/node_modules"), { recursive: true });
  symlinkSync(plugin, path.join(agent, "npm/node_modules/pi-subagents"));
  const installed = path.join(root, ".local/lib/pi-agentic-local/permissions");
  cpSync(new URL("../../pi/permissions", import.meta.url), installed, { recursive: true });
  writeFileSync(path.join(agent, "settings.json"), JSON.stringify({ extensions: [installed] }));
  return { root, agent, installed, entry: path.join(installed, "index.ts") };
}

async function sourceExports(f, relative, names) {
  const probe = path.join(f.root, "source-probe.ts");
  writeFileSync(probe, `import { ${names.join(", ")} } from ${JSON.stringify(path.join(plugin, relative))};
export default (pi) => pi.registerCommand("source-probe", {description:"Synthetic source probe",handler:(_,ctx)=>ctx.capture({${names.map((name) => name.split(" as ").at(-1)).join(", ")}})});`);
  const { loadExtensions } = await import(pathToFileURL(path.join(sdk, "dist/core/extensions/loader.js")));
  const loaded = await loadExtensions([probe], f.root);
  assert.deepEqual(loaded.errors, []);
  let captured;
  await loaded.extensions[0].commands.get("source-probe").handler("", { capture: (value) => { captured = value; } });
  return captured;
}

async function isolated(fn) {
  const previous = process.env.PI_CODING_AGENT_DIR;
  const f = fixture();
  process.env.PI_CODING_AGENT_DIR = f.agent;
  try { await fn(f); }
  finally {
    if (previous === undefined) delete process.env.PI_CODING_AGENT_DIR;
    else process.env.PI_CODING_AGENT_DIR = previous;
    rmSync(f.root, { recursive: true, force: true });
  }
}

function deferred() {
  let resolve;
  let reject;
  const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
  return { promise, resolve, reject };
}

for (const staleOutcome of ["success", "failure"]) {
  test(`shutdown invalidates a pending API ${staleOutcome} without late registration or status changes`, async () => {
    const pending = deferred();
    let registrations = 0;
    const api = { registerRequiredChildExtensions() { registrations++; return { dispose() {} }; } };
    const inheritance = new ChildInheritance("/synthetic/agent", "/synthetic/index.ts", () => pending.promise);
    const starting = inheritance.start("synthetic-stopped");
    inheritance.dispose();
    const stoppedProblem = inheritance.problem;
    if (staleOutcome === "success") pending.resolve(api);
    else pending.reject(new Error("stale API failure"));
    await starting;
    assert.equal(registrations, 0);
    assert.equal(inheritance.active("synthetic-stopped"), false);
    assert.equal(inheritance.problem, stoppedProblem);
  });

  test(`a stale API ${staleOutcome} cannot replace or dispose a newer session registration`, async () => {
    const older = deferred();
    const newer = deferred();
    const pending = [older, newer];
    const registrations = [];
    const disposals = [];
    const api = { registerRequiredChildExtensions({ sessionId }) {
      registrations.push(sessionId);
      return { dispose() { disposals.push(sessionId); } };
    } };
    const inheritance = new ChildInheritance("/synthetic/agent", "/synthetic/index.ts", () => pending.shift().promise);
    const oldStart = inheritance.start("synthetic-old");
    const newStart = inheritance.start("synthetic-new");
    newer.resolve(api);
    await newStart;
    assert.equal(inheritance.active("synthetic-new"), true);
    if (staleOutcome === "success") older.resolve(api);
    else older.reject(new Error("stale API failure"));
    await oldStart;
    assert.deepEqual(registrations, ["synthetic-new"]);
    assert.deepEqual(disposals, []);
    assert.equal(inheritance.active("synthetic-new"), true);
    assert.equal(inheritance.problem, undefined);
    inheritance.dispose();
    assert.deepEqual(disposals, ["synthetic-new"]);
  });
}

test("required child API resolves from Pi npm layout without npm/package.json; registry follows session lifecycle", { skip: !available }, async () => isolated(async (f) => {
  assert.equal(existsSync(path.join(f.agent, "npm/package.json")), false);
  await loadRequiredChildApi(f.agent);
  const api = await import(pathToFileURL(path.join(plugin, "src/shared/required-child-extensions.js")));
  const inheritance = new ChildInheritance(f.agent, f.entry);
  await inheritance.start("synthetic-first");
  assert.equal(inheritance.active("synthetic-first"), true);
  assert.equal(inheritance.active("other-session"), false);
  assert.equal(api.resolveRequiredChildExtensions("synthetic-first")[0].path, f.entry);
  await inheritance.start("synthetic-second");
  assert.deepEqual(api.resolveRequiredChildExtensions("synthetic-first"), []);
  assert.equal(inheritance.active("synthetic-second"), true);
  const conflict = new ChildInheritance(f.agent, f.entry);
  await conflict.start("synthetic-second");
  assert.equal(conflict.active("synthetic-second"), false);
  assert.match(conflict.problem, /already registered/);
  assert.equal(inheritance.active("synthetic-second"), true);
  inheritance.dispose();
  inheritance.dispose();
  assert.deepEqual(api.resolveRequiredChildExtensions("synthetic-second"), []);
}));

test("missing required-child API leaves inheritance unavailable", async () => {
  const scratch = mkdtempSync(path.join(os.tmpdir(), "pi-no-child-api-"));
  try {
    const inheritance = new ChildInheritance(scratch, "/unused/index.ts");
    await inheritance.start("synthetic-missing");
    assert.equal(inheritance.active("synthetic-missing"), false);
    assert.match(inheritance.problem, /Cannot find module/);
  } finally { rmSync(scratch, { recursive: true, force: true }); }
});

test("an unqualified pi-subagents version leaves delegation inheritance unavailable", async () => {
  const root = mkdtempSync(path.join(os.tmpdir(), "pi-child-api-version-"));
  try {
    const installed = path.join(root, "npm/node_modules/pi-subagents");
    mkdirSync(installed, { recursive: true });
    writeFileSync(path.join(installed, "package.json"), JSON.stringify({ name: "pi-subagents", version: "0.77.0", main: "index.js" }));
    writeFileSync(path.join(installed, "index.js"), "");
    const inheritance = new ChildInheritance(root, "/unused/index.ts");
    await inheritance.start("synthetic-old-api");
    assert.equal(inheritance.active("synthetic-old-api"), false);
    assert.match(inheritance.problem, /qualified pi-subagents 0.78.0/);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test("native foreground/background plans retain the permission extension despite extensions:[] and reject denied/external routes", { skip: !available }, async () => isolated(async (f) => {
  const inheritance = new ChildInheritance(f.agent, f.entry);
  await inheritance.start("synthetic-parent");
  await loadRequiredChildApi(f.agent);
  const api = await import(pathToFileURL(path.join(plugin, "src/shared/required-child-extensions.js")));
  const { buildInProcessChildLaunch } = await sourceExports(f, "src/runs/shared/child-launch.js", ["buildInProcessChildLaunch"]);
  const { DefaultResourceLoader, SettingsManager } = await import(pathToFileURL(path.join(sdk, "dist/index.js")));
  try {
    for (const host of ["parent", "runner"]) for (const extensions of [undefined, []]) {
      const launch = buildInProcessChildLaunch({ host, cwd: f.root, parentSessionId: "synthetic-parent", childAgentName: "synthetic", childIndex: 0, extensions, inheritProjectContext: true, inheritGlobalContext: false, inheritSkills: false });
      assert.equal(launch.session.ambientExtensions, host === "runner" && extensions === undefined);
      assert.ok(launch.session.extensionPaths.includes(f.entry));
      assert.equal(launch.session.requiredExtensions[0].requireForAllRunners, true);
      const loader = new DefaultResourceLoader({ cwd: f.root, agentDir: f.agent, settingsManager: SettingsManager.create(f.root, f.agent), noExtensions: !launch.session.ambientExtensions, noSkills: true, noPromptTemplates: true, noThemes: true, noContextFiles: true, additionalExtensionPaths: launch.session.extensionPaths });
      await loader.reload();
      const loaded = loader.getExtensions();
      assert.deepEqual(loaded.errors, []);
      assert.equal(loaded.extensions.filter((entry) => entry.resolvedPath === f.entry).length, 1);
      const permission = loaded.extensions.find((entry) => entry.resolvedPath === f.entry);
      assert.ok(permission, "required permission extension must actually load");
      for (const name of ["write", "edit", "bash_unrestricted"]) assert.ok(permission.tools.has(name));
      const childSessionId = `synthetic-child-${host}-${extensions === undefined ? "ambient" : "explicit"}`;
      const ctx = { cwd: f.root, hasUI: false, sessionManager: { getSessionId: () => childSessionId }, ui: { setStatus() {}, notify() {} } };
      await permission.handlers.get("session_start")[0]({ reason: "startup" }, ctx);
      assert.equal(api.resolveRequiredChildExtensions(childSessionId)[0].path, f.entry);
      await assert.rejects(permission.tools.get("write").definition.execute("deny", { path: "/synthetic-outside", content: "denied" }, undefined, undefined, ctx), /denied/);
      await permission.handlers.get("session_shutdown")[0]({ reason: "quit" }, ctx);
      assert.deepEqual(api.resolveRequiredChildExtensions(childSessionId), []);
    }
    assert.throws(() => buildInProcessChildLaunch({ host: "parent", cwd: f.root, parentSessionId: "synthetic-parent", childAgentName: "synthetic", childIndex: 0, capabilityCeiling: { version: 1, denyExtensions: true, sources: ["synthetic"] } }), /denies extensions/);
    const required = api.resolveRequiredChildExtensions("synthetic-parent");
    assert.throws(() => api.assertRequiredChildExtensionsAdmitted([required], { agent: "synthetic", runnerType: "external-cli" }), /only local native Pi/);
    assert.throws(() => api.assertRequiredChildExtensionsAdmitted([required], { agent: "synthetic", machine: "synthetic-remote" }), /only local native Pi/);
  } finally { inheritance.dispose(); }
}));

test("actual permission handler blocks delegation when the required-child API is unavailable even with approving UI", { skip: !available }, async () => isolated(async (f) => {
  const { loadExtensions } = await import(pathToFileURL(path.join(sdk, "dist/core/extensions/loader.js")));
  const { extensions, errors } = await loadExtensions([f.entry], f.root);
  assert.deepEqual(errors, []);
  rmSync(path.join(f.agent, "npm/node_modules/pi-subagents"));
  let prompts = 0;
  const notices = [];
  const ctx = { cwd: f.root, hasUI: true, sessionManager: { getSessionId: () => "synthetic-unregistered" }, ui: { confirm: async () => { prompts++; return true; }, setStatus() {}, notify: (message) => notices.push(message) } };
  await extensions[0].handlers.get("session_start")[0]({ reason: "startup" }, ctx);
  assert.ok(notices.some((message) => message.includes("inheritance unavailable")));
  const result = await extensions[0].handlers.get("tool_call")[0]({ toolName: "subagent", input: { task: "synthetic" } }, ctx);
  assert.equal(result.block, true);
  assert.match(result.reason, /inheritance unavailable/);
  assert.equal(prompts, 0);
}));

test("native child prompt hook treats project/global instructions and skills as separate opt-ins", { skip: !available }, async () => isolated(async (f) => {
  const { registerSubagentPromptRuntime } = await sourceExports(f, "src/runs/shared/subagent-prompt-runtime.js", ["default as registerSubagentPromptRuntime"]);
  for (const flags of [
    { inheritProjectContext: true, inheritGlobalContext: false, inheritSkills: false },
    { inheritProjectContext: true, inheritGlobalContext: true, inheritSkills: true },
    { inheritProjectContext: false, inheritGlobalContext: true, inheritSkills: false },
  ]) {
    const handlers = new Map();
    registerSubagentPromptRuntime({ on: (event, handler) => { handlers.set(event, handler); }, events: { on() {} } }, { ...flags, waitTool: { enabled: false } });
    const options = { contextFiles: [{ path: path.join(f.agent, "AGENTS.md"), content: "GLOBAL_SENTINEL" }, { path: path.join(f.root, "AGENTS.md"), content: "PROJECT_SENTINEL" }], skills: [{ name: "synthetic-skill", description: "SKILL_SENTINEL" }] };
    await handlers.get("before_agent_start")({ systemPrompt: "Synthetic Pi base", systemPromptOptions: options });
    assert.equal(options.contextFiles.some((file) => file.content === "GLOBAL_SENTINEL"), flags.inheritProjectContext && flags.inheritGlobalContext);
    assert.equal(options.contextFiles.some((file) => file.content === "PROJECT_SENTINEL"), flags.inheritProjectContext);
    assert.equal(options.skills.some((skill) => skill.name === "synthetic-skill"), flags.inheritSkills);
  }
}));
