import test from "node:test";
import assert from "node:assert/strict";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { ChildInheritance, loadRequiredChildApi } from "../../pi/permissions/child-inheritance.mjs";

const sdk = process.env.PI_SDK_ROOT ?? path.join(os.homedir(), ".local/lib/node_modules/@earendil-works/pi-coding-agent");
const plugin = process.env.PI_SUBAGENTS_ROOT ?? path.join(os.homedir(), ".pi/agent/npm/node_modules/pi-subagents");
const available = existsSync(path.join(plugin, "src/shared/required-child-extensions.js")) && existsSync(path.join(sdk, "dist/index.js"));
const unattendedAvailable = available && JSON.parse(readFileSync(path.join(plugin, "package.json"), "utf8")).version === "0.79.0";

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

async function sourceExports(f, relative, names, packageRoot = plugin) {
  const probe = path.join(f.root, "source-probe.ts");
  const sources = Array.isArray(relative) ? relative : [{ relative, names }];
  names = sources.flatMap((source) => source.names);
  writeFileSync(probe, `${sources.map((source) => `import { ${source.names.join(", ")} } from ${JSON.stringify(path.join(packageRoot, source.relative))};`).join("\n")}
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
  if (!unattendedAvailable) assert.equal(inheritance.allowsNativeTool("synthetic-first", { name: "subagent", sourceInfo: { path: path.join(plugin, "index.js") } }, { agent: "worker", task: "Synthetic task", context: "fresh" }), false);
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

test("unattended native controls require qualified provenance, a current registration and restricted inputs", { skip: !unattendedAvailable }, async () => isolated(async (f) => {
  const inheritance = new ChildInheritance(f.agent, f.entry);
  const native = { name: "subagent", sourceInfo: { source: "inline", path: "<inline:pi-subagents:fanout-child>" } };
  const launch = { agent: "worker", task: "Synthetic task", async: false, model: "openai/gpt-5:high", cwd: f.root, options: { context: "fresh", timeoutMs: 5_000, toolBudget: { hard: 20 } } };
  assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, launch), false);
  await inheritance.start("synthetic-policy");
  try {
    assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, launch), true);
    assert.equal(inheritance.allowsNativeTool("synthetic-policy", { name: "subagent", sourceInfo: { path: path.join(plugin, "index.js") } }, launch), true);
    const wait = { name: "bg_wait", sourceInfo: { source: "inline", path: "<inline:pi-subagents:prompt-runtime>" } };
    const receipt = { type: "message", message: { role: "toolResult", toolName: "subagent", toolCallId: "synthetic-resume", isError: false, details: { asyncId: "owned-run", "agentic-local": { ownerSessionId: "synthetic-policy" } } } };
    const branch = [receipt];
    for (const action of ["status", "steer", "interrupt", "resume", "stop"]) {
      const input = { action, id: "owned-run", message: "Synthetic correction" };
      assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, input, branch), true);
      for (const entries of [[], [{ ...receipt, message: { ...receipt.message, isError: true } }], [{ ...receipt, message: { ...receipt.message, details: { asyncId: "owned-run" } } }], [{ ...receipt, message: { ...receipt.message, details: { asyncId: "owned-run", "agentic-local": { ownerSessionId: "foreign-owner" } } } }]]) {
        assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, input, entries), false);
      }
      for (const id of ["foreign-run", "owned", "synthetic-resume"]) assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, { ...input, id }, branch), false);
      for (const options of [{ index: 0 }, { childId: "foreign-child" }, { view: "fleet" }]) assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, { ...input, options }, branch), false);
      assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, { ...input, runId: "foreign-run" }, branch), false);
      assert.equal(inheritance.allowsNativeTool("synthetic-policy", { ...native, sourceInfo: { path: f.entry } }, input, branch), false);
      assert.equal(inheritance.allowsNativeTool("different-session", native, input, branch), false);
    }
    for (const input of [{ action: "children.list" }, { action: "status" }, { action: "status", options: { view: "fleet" } }]) assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, input, branch), false);
    assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, { action: "status", id: "owned-run", options: { view: "transcript", lines: 10 } }, branch), true);
    assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, { action: "steer", id: "owned-run", message: "Synthetic correction", options: { mode: "follow_up", ackTimeoutMs: 100 } }, branch), true);
    assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, { action: "steer", id: "owned-run", options: { mode: "plan" } }, branch), false);
    assert.equal(inheritance.allowsNativeTool("synthetic-policy", wait, { id: "owned-run", timeoutMs: 1_000 }, branch), true);
    for (const [input, entries] of [[{ id: "owned-run" }, []], [{ id: "foreign-run" }, branch], [{ id: "owned-run", nonBlocking: true }, branch], [{ id: "owned-run" }, [{ ...receipt, message: { ...receipt.message, details: { asyncId: "owned-run" } } }]], [{ id: "owned-run" }, [{ ...receipt, message: { ...receipt.message, isError: true } }]], [{ id: "owned-run" }, [{ ...receipt, message: { ...receipt.message, details: { asyncId: "owned-run", "agentic-local": { ownerSessionId: "foreign-owner" } } } }]]]) {
      assert.equal(inheritance.allowsNativeTool("synthetic-policy", wait, input, entries), false);
    }
    assert.equal(inheritance.allowsNativeTool("different-session", wait, { id: "owned-run" }, branch), false);
    assert.equal(inheritance.allowsNativeTool("synthetic-policy", { ...wait, sourceInfo: { path: f.entry } }, { id: "owned-run" }, branch), false);
    assert.equal(inheritance.allowsNativeTool("different-session", native, launch), false);
    assert.equal(inheritance.allowsNativeTool("synthetic-policy", { name: "subagent", sourceInfo: { path: f.entry } }, launch), false);
    assert.equal(inheritance.allowsNativeTool("synthetic-policy", { name: "contact_supervisor", sourceInfo: { path: path.join(plugin, "index.js") } }, {}), false);
    const { topLevelSupervisorTool } = await sourceExports(f, "src/intercom/native-supervisor-channel.js", ["topLevelSupervisorTool"]);
    const topLevelContact = await topLevelSupervisorTool().execute("synthetic-top-level", { reason: "progress_update", message: "Must not send" });
    assert.equal(topLevelContact.isError, true);
    assert.match(topLevelContact.content[0].text, /no supervisor/);
    for (const input of [{ workflow: true }, { workflow: "./workflow.js" }, { agent: "worker", context: "fresh", worktree: true }, { agent: "worker", context: "fresh", options: { acceptance: { level: "verified", verify: [{ command: "exit 99" }] } } }, { action: "resume", id: "synthetic-run", options: { model: "override" } }]) {
      assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, input), false);
    }
  } finally { inheritance.dispose(); }
  assert.equal(inheritance.allowsNativeTool("synthetic-policy", native, launch), false);
}));

test("new unattended launches require explicit fresh context despite native configured fork preference", { skip: !unattendedAvailable }, async () => isolated(async (f) => {
  const { resolveSubagentLaunchContext, canPreferFork, loadConfig, getConfigPath, flattenSubagentToolOptions } = await sourceExports(f, [
    { relative: "src/shared/fork-context.js", names: ["resolveSubagentLaunchContext", "canPreferFork"] },
    { relative: "src/extension/config.js", names: ["loadConfig", "getConfigPath"] },
    { relative: "src/extension/subagent-options.js", names: ["flattenSubagentToolOptions"] },
  ]);
  mkdirSync(path.dirname(getConfigPath()), { recursive: true });
  writeFileSync(getConfigPath(), JSON.stringify({ defaultSubagentContext: "fork" }));
  const { SessionManager } = await import(pathToFileURL(path.join(sdk, "dist/index.js")));
  const manager = SessionManager.create(f.root, path.join(f.root, "sessions"));
  manager.appendMessage({ role: "user", content: "Synthetic parent context that must not be forked implicitly", timestamp: Date.now() });
  assert.equal(canPreferFork(manager), true);
  const preference = { defaultSubagentContext: loadConfig().defaultSubagentContext, agentDefaultContext: "fresh", canUseImplicitFork: canPreferFork(manager) };
  const inheritance = new ChildInheritance(f.agent, f.entry);
  const native = { name: "subagent", sourceInfo: { source: "inline", path: "<inline:pi-subagents:fanout-child>" } };
  await inheritance.start(manager.getSessionId());
  try {
    for (const [contextInput, resolved, admitted] of [
      [{}, "fork", false],
      [{ context: "fresh" }, "fresh", true],
      [{ options: { context: "fresh" } }, "fresh", true],
      [{ context: "fresh", options: { context: "fresh" } }, "fresh", true],
      [{ context: "fork" }, "fork", false],
      [{ options: { context: "fork" } }, "fork", false],
    ]) {
      const input = { agent: "worker", task: "Synthetic task", ...contextInput };
      const flattened = flattenSubagentToolOptions(input);
      assert.equal(resolveSubagentLaunchContext({ ...preference, explicitContext: flattened.context }), resolved);
      assert.equal(inheritance.allowsNativeTool(manager.getSessionId(), native, input), admitted);
    }
    for (const contextInput of [{ context: "fresh", options: { context: "fork" } }, { context: "fork", options: { context: "fresh" } }]) {
      const input = { agent: "worker", task: "Synthetic task", ...contextInput };
      assert.throws(() => flattenSubagentToolOptions(input), /different values/);
      assert.equal(inheritance.allowsNativeTool(manager.getSessionId(), native, input), false);
    }
    const receipt = { type: "message", message: { role: "toolResult", toolName: "subagent", isError: false, details: { asyncId: "retained-worker", "agentic-local": { ownerSessionId: manager.getSessionId() } } } };
    assert.equal(inheritance.allowsNativeTool(manager.getSessionId(), native, { action: "resume", id: "retained-worker" }, [receipt]), true);
  } finally { inheritance.dispose(); }
}));

for (const version of ["0.77.0", "0.79.1", "0.80.0", "0.79.0-rc.1"]) test(`unqualified pi-subagents ${version} leaves delegation inheritance unavailable`, async () => {
  const root = mkdtempSync(path.join(os.tmpdir(), "pi-child-api-version-"));
  try {
    const installed = path.join(root, "npm/node_modules/pi-subagents");
    mkdirSync(installed, { recursive: true });
    writeFileSync(path.join(installed, "package.json"), JSON.stringify({ name: "pi-subagents", version, main: "index.js" }));
    writeFileSync(path.join(installed, "index.js"), "");
    const inheritance = new ChildInheritance(root, "/unused/index.ts");
    await inheritance.start("synthetic-old-api");
    assert.equal(inheritance.active("synthetic-old-api"), false);
    assert.match(inheritance.problem, /qualified pi-subagents 0.78.0/);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test("a qualified package with an incompatible public API cannot enable child inheritance", async () => {
  const root = mkdtempSync(path.join(os.tmpdir(), "pi-child-api-capability-"));
  try {
    const installed = path.join(root, "npm/node_modules/pi-subagents");
    mkdirSync(installed, { recursive: true });
    writeFileSync(path.join(installed, "package.json"), JSON.stringify({ name: "pi-subagents", version: "0.79.0", type: "module", exports: { ".": "./index.js", "./required-child-extensions": "./api.js" } }));
    writeFileSync(path.join(installed, "index.js"), "");
    writeFileSync(path.join(installed, "api.js"), "export const unsupported = true;");
    const inheritance = new ChildInheritance(root, "/unused/index.ts");
    await inheritance.start("synthetic-incompatible-api");
    assert.equal(inheritance.active("synthetic-incompatible-api"), false);
    assert.match(inheritance.problem, /required-child-extensions API is unavailable/);
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

test("the released native child session factory binds required permissions and rejects required startup failures without inference", { skip: !available }, async () => isolated(async (f) => {
  const offline = process.env.PI_OFFLINE;
  process.env.PI_OFFLINE = "1";
  const inheritance = new ChildInheritance(f.agent, f.entry);
  let factory;
  try {
    await inheritance.start("synthetic-factory-parent");
    const api = await import(pathToFileURL(path.join(plugin, "src/shared/required-child-extensions.js")));
    const { buildInProcessChildLaunch } = await sourceExports(f, "src/runs/shared/child-launch.js", ["buildInProcessChildLaunch"]);
    const { createDefaultChildSessionFactory } = await sourceExports(f, "src/runs/shared/child-session.js", ["createDefaultChildSessionFactory"]);
    const pi = await import(pathToFileURL(path.join(sdk, "dist/index.js")));
    factory = createDefaultChildSessionFactory({ loadPiCodingAgent: async () => pi });
    for (const host of ["parent", "runner"]) {
      const launch = buildInProcessChildLaunch({ host, cwd: f.root, parentSessionId: "synthetic-factory-parent", childAgentName: "synthetic", childIndex: 0, extensions: [], tools: ["read", "write", "edit", "bash"], inheritProjectContext: false, inheritGlobalContext: false, inheritSkills: false });
      const child = await factory.create(launch.session);
      try {
        assert.equal(child.sessionFile, undefined);
        assert.equal(api.resolveRequiredChildExtensions(child.sessionId)[0].path, f.entry);
      } finally { await child.dispose(); }
      assert.deepEqual(api.resolveRequiredChildExtensions(child.sessionId), []);
    }
    const broken = path.join(f.root, "required-startup-failure.ts");
    writeFileSync(broken, 'export default (pi) => pi.on("session_start", () => { throw new Error("synthetic required startup failure"); });');
    const launch = buildInProcessChildLaunch({ host: "parent", cwd: f.root, parentSessionId: "synthetic-factory-parent", childAgentName: "synthetic", childIndex: 0, extensions: [], tools: ["read"], inheritProjectContext: false, inheritGlobalContext: false, inheritSkills: false, requiredExtensions: [...api.resolveRequiredChildExtensions("synthetic-factory-parent"), { id: "synthetic-failure", path: broken, requireForAllRunners: true }] });
    await assert.rejects(factory.create(launch.session), /Required child extension failed during startup.*synthetic required startup failure/);
  } finally {
    await factory?.dispose();
    inheritance.dispose();
    if (offline === undefined) delete process.env.PI_OFFLINE;
    else process.env.PI_OFFLINE = offline;
  }
}));

test("required agentic-local permits native child delegation and bound parent contact while preserving manual boundaries", { skip: !unattendedAvailable }, async () => isolated(async (f) => {
  const names = ["HOME", "TMPDIR", "PI_OFFLINE", "npm_config_cache"];
  const previous = new Map(names.map((name) => [name, process.env[name]]));
  process.env.HOME = f.root;
  process.env.TMPDIR = path.join(f.root, "tmp");
  process.env.PI_OFFLINE = "1";
  process.env.npm_config_cache = path.join(f.root, "npm-cache");
  mkdirSync(process.env.TMPDIR);
  const inheritance = new ChildInheritance(f.agent, f.entry);
  let factory;
  let resetFactory;
  let supervisorDir;
  try {
    const parentId = `synthetic-headless-${path.basename(f.root)}`;
    const runId = `${parentId}-run`;
    await inheritance.start(parentId);
    assert.equal(inheritance.active(parentId), true);
    const api = await import(pathToFileURL(path.join(plugin, "src/shared/required-child-extensions.js")));
    const { buildInProcessChildLaunch, createDefaultChildSessionFactory, setChildSessionFactory, createNativeSupervisorChannel, createChildSafeState } = await sourceExports(f, [
      { relative: "src/runs/shared/child-launch.js", names: ["buildInProcessChildLaunch"] },
      { relative: "src/runs/shared/child-session.js", names: ["createDefaultChildSessionFactory", "setChildSessionFactory"] },
      { relative: "src/intercom/native-supervisor-channel.js", names: ["createNativeSupervisorChannel"] },
      { relative: "src/extension/fanout-child.js", names: ["createChildSafeState"] },
    ]);
    const pi = await import(pathToFileURL(path.join(sdk, "dist/index.js")));
    const { AuthStorage } = await import(pathToFileURL(path.join(sdk, "dist/core/auth-storage.js")));
    const modelRuntime = await pi.ModelRuntime.create({ credentials: AuthStorage.inMemory(), modelsPath: null, refreshOnCreate: false, allowModelNetwork: false });
    let providerCalls = 0;
    for (const method of ["getAuth", "checkAuth", "stream", "streamSimple", "complete", "completeSimple", "getAvailable", "login", "logout", "refresh"]) {
      modelRuntime[method] = () => { providerCalls++; throw new Error(`Forbidden provider/auth operation: ${method}`); };
    }
    const model = modelRuntime.getModel("openai", "gpt-5");
    assert.ok(model);
    const allowed = path.join(f.root, "allowed");
    mkdirSync(allowed);
    writeFileSync(path.join(f.installed, "profile.json"), JSON.stringify({ name: "agentic-local", writeRoots: [allowed] }));
    mkdirSync(path.join(f.agent, "agents"));
    writeFileSync(path.join(f.agent, "agents/synthetic-leaf.md"), "---\nname: synthetic-leaf\ndescription: Synthetic native leaf.\ntools: read,write,edit,bash\nextensions: []\n---\nDo no work.\n");
    let session;
    factory = createDefaultChildSessionFactory({ loadPiCodingAgent: async () => ({ ...pi, ModelRuntime: { create: async () => modelRuntime }, createAgentSession: async (options) => {
      const created = await pi.createAgentSession({ ...options, modelRuntime, model });
      session = created.session;
      return created;
    } }) });
    const launch = buildInProcessChildLaunch({ host: "parent", runId, orchestratorIntercomTarget: "synthetic-owner", cwd: f.root, parentSessionId: parentId, childAgentName: "synthetic-owner", childIndex: 0, extensions: [], tools: ["read", "write", "edit", "bash", "bash_unrestricted", "subagent", "contact_supervisor"], inheritProjectContext: false, inheritGlobalContext: false, inheritSkills: false });
    supervisorDir = launch.session.runtime.supervisorChannelDir;
    const child = await factory.create(launch.session);
    try {
      assert.equal(session.extensionRunner.hasUI(), false);
      assert.equal(api.resolveRequiredChildExtensions(child.sessionId)[0].path, f.entry);
      assert.equal(typeof session.agent.beforeToolCall, "function");
      const ownerSession = session;
      const call = (name, args) => ownerSession.agent.beforeToolCall({ toolCall: { type: "toolCall", id: `synthetic-${name}`, name, arguments: args }, args });
      for (const [name, args, source] of [["subagent", { agent: "synthetic-leaf", task: "Synthetic task", async: false, options: { context: "fresh", timeoutMs: 5_000 } }, "<inline:pi-subagents:fanout-child>"], ["contact_supervisor", { reason: "progress_update", message: "Synthetic parent-channel message" }, "<inline:pi-subagents:prompt-runtime>"]]) {
        const tool = session.agent.state.tools.find((item) => item.name === name);
        assert.ok(tool, `${name} is registered and active`);
        assert.equal(session.getAllTools().find((item) => item.name === name).sourceInfo.path, source);
        assert.equal((await call(name, args))?.block, undefined);
      }
      resetFactory = () => setChildSessionFactory(undefined);
      let descendants = 0;
      setChildSessionFactory({ async create(input) {
        const descendant = await factory.create(input);
        descendants++;
        assert.equal(api.resolveRequiredChildExtensions(descendant.sessionId)[0].path, f.entry);
        assert.ok(session.getAllTools().find((tool) => tool.name === "write").sourceInfo.path.endsWith("permissions/index.ts"));
        const write = session.agent.state.tools.find((tool) => tool.name === "write");
        const target = path.join(allowed, "descendant-write");
        await write.execute("synthetic-allowed", { path: target, content: "Synthetic descendant write" });
        assert.equal(readFileSync(target, "utf8"), "Synthetic descendant write");
        await assert.rejects(write.execute("synthetic-outside", { path: path.join(f.root, "descendant-outside"), content: "denied" }), /Outside-scope file write denied/);
        // Replace only inference: discovery, native admission, child creation and permission startup are real.
        const listeners = new Set();
        const subscribe = descendant.subscribe.bind(descendant);
        descendant.subscribe = (listener) => {
          listeners.add(listener);
          const unsubscribe = subscribe(listener);
          return () => { listeners.delete(listener); unsubscribe(); };
        };
        descendant.prompt = async () => {
          const message = { role: "assistant", content: [{ type: "text", text: "Synthetic leaf result" }], stopReason: "stop", api: model.api, provider: model.provider, model: model.id, usage: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, totalTokens: 0, cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, total: 0 } }, timestamp: Date.now() };
          for (const listener of listeners) listener({ type: "message_end", message });
        };
        return descendant;
      }, async dispose() {} });
      const delegation = await ownerSession.agent.state.tools.find((tool) => tool.name === "subagent").execute("synthetic-delegation", { agent: "synthetic-leaf", task: "Synthetic task", async: false, options: { context: "fresh", timeoutMs: 5_000 } });
      assert.equal(delegation.isError, undefined, JSON.stringify(delegation));
      assert.ok(delegation.content.some((item) => item.text?.includes("Synthetic leaf result")));
      assert.equal(descendants, 1);
      const contact = await ownerSession.agent.state.tools.find((tool) => tool.name === "contact_supervisor").execute("synthetic-contact", { reason: "progress_update", message: "Synthetic parent-channel message" });
      assert.equal(contact.details.delivered, true);
      const request = JSON.parse(readFileSync(path.join(supervisorDir, "requests", readdirSync(path.join(supervisorDir, "requests"))[0]), "utf8"));
      assert.equal(request.orchestratorSessionId, parentId);
      assert.equal(request.runId, runId);
      assert.equal(request.orchestratorTarget, "synthetic-owner");
      assert.equal(request.message, "Synthetic parent-channel message");
      await assert.rejects(ownerSession.agent.state.tools.find((tool) => tool.name === "contact_supervisor").execute("synthetic-unanswered", { reason: "need_decision", message: "Synthetic decision without a parent listener" }, AbortSignal.timeout(50)), /cancel/i);
      assert.equal(readdirSync(path.join(supervisorDir, "requests")).length, 1);
      const parentTools = new Map();
      const parentApi = { events: pi.createEventBus(), getAllTools: () => [...parentTools.values()], registerTool: (tool) => parentTools.set(tool.name, tool), on: () => () => {}, sendMessage: () => true };
      const parentState = createChildSafeState();
      parentState.currentSessionId = parentId;
      parentState.supervisorOwnerSessionId = parentId;
      const parentChannel = createNativeSupervisorChannel(parentApi, parentState, { getChannelDirs: () => ({ dirs: [supervisorDir], retire() {} }) });
      parentChannel.registerTools();
      const foreignTools = new Map();
      const foreignState = createChildSafeState();
      foreignState.currentSessionId = `${parentId}-foreign`;
      foreignState.supervisorOwnerSessionId = foreignState.currentSessionId;
      const foreignChannel = createNativeSupervisorChannel({ ...parentApi, getAllTools: () => [...foreignTools.values()], registerTool: (tool) => foreignTools.set(tool.name, tool) }, foreignState, { getChannelDirs: () => ({ dirs: [supervisorDir], retire() {} }) });
      foreignChannel.registerTools();
      const decisionAbort = new AbortController();
      const decision = ownerSession.agent.state.tools.find((tool) => tool.name === "contact_supervisor").execute("synthetic-decision", { reason: "need_decision", message: "Synthetic decision for the immediate parent" }, AbortSignal.any([decisionAbort.signal, AbortSignal.timeout(2_000)]));
      decision.catch(() => {});
      const previousUI = ownerSession.extensionRunner.getUIContext();
      try {
        const foreignPending = await foreignTools.get("subagent_supervisor").execute("synthetic-foreign", { action: "pending" });
        assert.deepEqual(foreignPending.details.pending, []);
        const parentTool = parentTools.get("subagent_supervisor");
        const pending = await parentTool.execute("synthetic-pending", { action: "pending" });
        assert.equal(pending.details.pending.length, 1);
        const replyTo = pending.details.pending[0].id;
        await assert.rejects(foreignTools.get("subagent_supervisor").execute("synthetic-foreign-reply", { action: "reply", replyTo, message: "Wrong parent" }), /No pending supervisor request/);
        await assert.rejects(parentTool.execute("synthetic-unknown-reply", { action: "reply", replyTo: "unknown-request", message: "Unknown request" }), /No pending supervisor request/);
        const reply = { action: "reply", replyTo, message: "Synthetic manually approved decision" };
        assert.equal((await call("subagent_supervisor", reply)).block, true);
        let confirmations = 0;
        ownerSession.extensionRunner.setUIContext({ ...previousUI, confirm: async () => { confirmations++; return true; } });
        assert.equal((await call("subagent_supervisor", reply))?.block, undefined);
        assert.equal(confirmations, 1);
        await parentTool.execute("synthetic-parent-reply", reply);
        const settled = await decision;
        assert.equal(settled.details.requestId, replyTo);
        assert.match(settled.content[0].text, /Synthetic manually approved decision/);
      } finally {
        ownerSession.extensionRunner.setUIContext(previousUI);
        decisionAbort.abort();
        await decision.catch(() => {});
        parentChannel.dispose();
        foreignChannel.dispose();
      }
      for (const args of [{ action: "create", name: "unattended-config" }, { workflow: true }, { agent: "synthetic-leaf", context: "fresh", options: { gate: "touch /outside" } }, { agent: "synthetic-leaf", context: "fresh", output: "/outside" }, { agent: "synthetic-leaf", context: "fresh", options: { machine: "remote" } }, { action: "resume", id: "synthetic-run", model: "override" }]) {
        assert.equal((await call("subagent", args)).block, true);
      }
      assert.equal((await call("foreign_mcp", {})).block, true);
      for (const name of ["write", "bash_unrestricted"]) {
        const args = name === "write" ? { path: path.join(f.root, "outside"), content: "denied" } : { command: "exit 99" };
        await assert.rejects(ownerSession.agent.state.tools.find((tool) => tool.name === name).execute("synthetic-denied", args), /denied|approval unavailable/);
      }
      assert.equal(providerCalls, 0);
    } finally { await child.dispose(); }
  } finally {
    resetFactory?.();
    await factory?.dispose();
    if (supervisorDir) rmSync(supervisorDir, { recursive: true, force: true });
    inheritance.dispose();
    for (const [name, value] of previous) {
      if (value === undefined) delete process.env[name];
      else process.env[name] = value;
    }
  }
}));

test("native retained resume receipts authorize only owned blocking waits and survive session reopening", { skip: !unattendedAvailable, timeout: 45_000 }, async () => isolated(async (f) => {
  const names = ["HOME", "TMPDIR", "PI_OFFLINE", "npm_config_cache", "PI_SUBAGENT_CHILD", "PI_SUBAGENTS_PI_CODING_AGENT_PACKAGE_ROOT"];
  const previous = new Map(names.map((name) => [name, process.env[name]]));
  process.env.HOME = f.root;
  process.env.TMPDIR = path.join(f.root, "tmp");
  process.env.PI_OFFLINE = "1";
  process.env.npm_config_cache = path.join(f.root, "npm-cache");
  process.env.PI_SUBAGENTS_PI_CODING_AGENT_PACKAGE_ROOT = sdk;
  delete process.env.PI_SUBAGENT_CHILD;
  mkdirSync(process.env.TMPDIR);
  let session;
  try {
    const nativePlugin = path.join(f.root, "pi-subagents");
    cpSync(plugin, nativePlugin, { recursive: true, filter: (source) => path.basename(source) !== "node_modules" });
    symlinkSync(existsSync(path.join(plugin, "node_modules")) ? path.join(plugin, "node_modules") : path.dirname(plugin), path.join(nativePlugin, "node_modules"));
    rmSync(path.join(f.agent, "npm/node_modules/pi-subagents"));
    symlinkSync(nativePlugin, path.join(f.agent, "npm/node_modules/pi-subagents"));
    const provider = path.join(f.root, "synthetic-provider.ts");
    const faux = path.join(sdk, "node_modules/@earendil-works/pi-ai/dist/providers/faux.js");
    writeFileSync(provider, `import { fauxProvider, fauxAssistantMessage } from ${JSON.stringify(faux)};
export default pi => { const f = fauxProvider({provider:"local-qualification",api:"local-qualification-api",models:[{id:"leaf"}],tokensPerSecond:100000}); f.setResponses(Array.from({length:20},()=>fauxAssistantMessage("Synthetic native leaf result"))); pi.registerProvider(f.provider); };`);
    mkdirSync(path.join(f.agent, "agents"));
    writeFileSync(path.join(f.agent, "agents/synthetic-leaf.md"), `---\nname: synthetic-leaf\ndescription: Synthetic local provider leaf\nmodel: local-qualification/leaf\ntools: read,write\nextensions: ${provider}\ninheritProjectContext: false\ninheritGlobalContext: false\ninheritSkills: false\n---\nReturn the synthetic result.\n`);
    const settings = { extensions: [f.installed, path.join(nativePlugin, "index.js"), provider], cacheWarming: "off", subagents: { disableBuiltins: true, defaultModel: "local-qualification/leaf" } };
    writeFileSync(path.join(f.agent, "settings.json"), JSON.stringify(settings));
    const pi = await import(pathToFileURL(path.join(sdk, "dist/index.js")));
    const { AuthStorage } = await import(pathToFileURL(path.join(sdk, "dist/core/auth-storage.js")));
    const modelRuntime = await pi.ModelRuntime.create({ credentials: AuthStorage.inMemory(), modelsPath: null, refreshOnCreate: false, allowModelNetwork: false });
    const manager = pi.SessionManager.create(f.root, path.join(f.root, "sessions"));
    manager.appendMessage({ role: "user", content: "Synthetic local native pipeline", timestamp: Date.now() });
    async function open(sessionManager) {
      const settingsManager = pi.SettingsManager.inMemory(settings);
      const loader = new pi.DefaultResourceLoader({ cwd: f.root, agentDir: f.agent, settingsManager, noSkills: true, noPromptTemplates: true, noThemes: true, noContextFiles: true });
      await loader.reload();
      assert.deepEqual(loader.getExtensions().errors, []);
      const created = await pi.createAgentSession({ cwd: f.root, agentDir: f.agent, settingsManager, resourceLoader: loader, sessionManager, modelRuntime, model: modelRuntime.getModel("openai", "gpt-5") });
      await created.session.bindExtensions({ mode: "print" });
      await created.session.setModel(modelRuntime.getModel("local-qualification", "leaf"));
      created.session.setActiveToolsByName([...created.session.getActiveToolNames(), "subagent", "bg_wait"]);
      return created.session;
    }
    session = await open(manager);
    let serial = 0;
    async function invoke(name, args) {
      const id = `synthetic-call-${++serial}`;
      const call = { type: "toolCall", id, name, arguments: args };
      session.sessionManager.appendMessage({ role: "assistant", content: [call], timestamp: Date.now() });
      const admission = await session.agent.beforeToolCall({ toolCall: call, args });
      assert.equal(admission?.block, undefined, JSON.stringify(admission));
      const result = await session.agent.state.tools.find((tool) => tool.name === name).execute(id, args);
      const finalized = await session.agent.afterToolCall({ toolCall: call, args, result, isError: result.isError === true });
      const consumed = { ...result, ...finalized };
      session.sessionManager.appendMessage({ role: "toolResult", toolCallId: id, toolName: name, content: consumed.content, details: consumed.details, isError: consumed.isError === true, timestamp: Date.now() });
      return consumed;
    }
    const initial = await invoke("subagent", { agent: "synthetic-leaf", task: "Initial local synthetic leaf", async: true, options: { context: "fresh", timeoutMs: 10_000 } });
    const retainedId = initial.content.map((item) => item.text ?? "").join("\n").match(/Async:.*\[([^\]]+)\]/)?.[1];
    assert.ok(retainedId, JSON.stringify(initial.details));
    assert.equal(initial.details["agentic-local"].ownerSessionId, manager.getSessionId());
    await invoke("bg_wait", { id: retainedId, timeoutMs: 15_000 });
    const refusedControl = async (args) => {
      const result = await session.agent.beforeToolCall({ toolCall: { type: "toolCall", id: "synthetic-control-refusal", name: "subagent", arguments: args }, args });
      assert.equal(result.block, true, JSON.stringify(args));
    };
    for (const action of ["status", "steer", "interrupt", "resume", "stop"]) {
      for (const id of ["foreign-run", retainedId.slice(0, 8), "synthetic-call-1"]) await refusedControl({ action, id });
      for (const options of [{ index: 0 }, { childId: "foreign-child" }, { view: "fleet" }]) await refusedControl({ action, id: retainedId, options });
    }
    await refusedControl({ action: "status" });
    await refusedControl({ action: "children.list" });
    manager.appendMessage({ role: "toolResult", toolCallId: "synthetic-legacy-workflow", toolName: "subagent", content: [{ type: "text", text: "Synthetic legacy workflow receipt" }], details: { asyncId: "legacy-workflow" }, isError: false, timestamp: Date.now() });
    for (const action of ["status", "steer", "interrupt", "resume", "stop"]) await refusedControl({ action, id: "legacy-workflow" });
    const previousUI = session.extensionRunner.getUIContext();
    let confirmations = 0;
    try {
      session.extensionRunner.setUIContext({ ...previousUI, confirm: async () => { confirmations++; return true; } });
      for (const args of [{ action: "resume", id: "foreign-run" }, { action: "resume", id: "legacy-workflow" }, { workflow: true }]) {
        const call = { type: "toolCall", id: `synthetic-manual-${++serial}`, name: "subagent", arguments: args };
        const admitted = await session.agent.beforeToolCall({ toolCall: call, args });
        assert.equal(admitted?.block, undefined);
        // Inject only the successful result: a per-call manual approval must not mint future unattended authority.
        const result = { content: [{ type: "text", text: "Synthetic manually approved native result" }], details: { asyncId: `unqualified-${serial}` } };
        const finalized = await session.agent.afterToolCall({ toolCall: call, args, result, isError: false });
        const consumed = { ...result, ...finalized };
        assert.equal(consumed.details["agentic-local"], undefined);
        manager.appendMessage({ role: "toolResult", toolCallId: call.id, toolName: "subagent", ...consumed, isError: false, timestamp: Date.now() });
      }
      assert.equal(confirmations, 3);
    } finally { session.extensionRunner.setUIContext(previousUI); }
    const unqualifiedReceipts = manager.getBranch().filter((entry) => entry.type === "message" && entry.message.details?.asyncId?.startsWith("unqualified-"));
    assert.equal(unqualifiedReceipts.length, 3);
    for (const entry of unqualifiedReceipts) {
      await refusedControl({ action: "resume", id: entry.message.details.asyncId });
      const args = { id: entry.message.details.asyncId };
      const denied = await session.agent.beforeToolCall({ toolCall: { type: "toolCall", id: "synthetic-laundered-wait", name: "bg_wait", arguments: args }, args });
      assert.equal(denied.block, true);
    }
    const ownStatus = await invoke("subagent", { action: "status", id: retainedId });
    assert.equal(ownStatus.isError, undefined);
    const resumed = await invoke("subagent", { action: "resume", id: retainedId, message: "Continue the synthetic leaf" });
    const asyncId = resumed.content.map((item) => item.text ?? "").join("\n").match(/Revived run: ([^\s]+)/)?.[1];
    assert.ok(asyncId, JSON.stringify(resumed.details));
    assert.equal(resumed.details["agentic-local"].ownerSessionId, manager.getSessionId());
    const refused = async (args) => {
      const result = await session.agent.beforeToolCall({ toolCall: { type: "toolCall", id: "synthetic-wait-refusal", name: "bg_wait", arguments: args }, args });
      assert.equal(result.block, true);
    };
    for (const args of [{ id: "unknown-run" }, { id: asyncId.slice(0, 8) }, { id: asyncId, nonBlocking: true }, { all: true }, { id: asyncId, observer: true }]) await refused(args);
    const waited = await invoke("bg_wait", { id: asyncId, timeoutMs: 15_000 });
    assert.ok(waited.details.completions?.some((completion) => completion.id === asyncId || completion.runId === asyncId), JSON.stringify(waited));
    const status = await invoke("subagent", { action: "status", id: asyncId });
    assert.ok(status.content.some((item) => /complete|Synthetic native leaf result/i.test(item.text ?? "")), JSON.stringify(status));
    const file = manager.getSessionFile();
    const ownerId = manager.getSessionId();
    await session.extensionRunner.emit({ type: "session_shutdown", reason: "quit" });
    session.dispose();
    session = await open(pi.SessionManager.open(file));
    assert.equal(session.sessionManager.getSessionId(), ownerId);
    const terminalAdmission = await session.agent.beforeToolCall({ toolCall: { type: "toolCall", id: "synthetic-reopened-wait", name: "bg_wait", arguments: { id: asyncId } }, args: { id: asyncId } });
    assert.equal(terminalAdmission?.block, undefined);
    const terminal = await invoke("bg_wait", { id: asyncId, timeoutMs: 1_000 });
    assert.ok(terminal.content.some((item) => /terminal|complete/i.test(item.text ?? "")));
    await session.extensionRunner.emit({ type: "session_shutdown", reason: "quit" });
    session.dispose();
    const fork = pi.SessionManager.forkFrom(file, f.root, path.join(f.root, "fork-sessions"));
    session = await open(fork);
    assert.notEqual(session.sessionManager.getSessionId(), ownerId);
    await refused({ id: asyncId });
    for (const action of ["status", "steer", "interrupt", "resume", "stop"]) await refusedControl({ action, id: asyncId });
  } finally {
    if (session) { await session.extensionRunner.emit({ type: "session_shutdown", reason: "quit" }); session.dispose(); }
    for (const [name, value] of previous) {
      if (value === undefined) delete process.env[name];
      else process.env[name] = value;
    }
  }
}));

test("native defaultExtensions isolates ambient startup while retaining explicit subagent and permission capabilities", { skip: !available }, async () => isolated(async (f) => {
  const names = ["HOME", "TMPDIR", "PI_OFFLINE", "PI_SUBAGENT_CHILD", "npm_config_cache"];
  const previous = new Map(names.map((name) => [name, process.env[name]]));
  const counterKey = `pi-permission-ambient-${f.root}`;
  const counter = Symbol.for(counterKey);
  globalThis[counter] = 0;
  let factory;
  const inheritance = new ChildInheritance(f.agent, f.entry);
  try {
    // Fresh package modules keep plugin maintenance and caches inside this fixture.
    process.env.HOME = f.root;
    process.env.TMPDIR = path.join(f.root, "tmp");
    process.env.PI_OFFLINE = "1";
    process.env.npm_config_cache = path.join(f.root, "npm-cache");
    delete process.env.PI_SUBAGENT_CHILD;
    mkdirSync(process.env.TMPDIR);
    const copiedPlugin = path.join(f.root, "pi-subagents");
    cpSync(plugin, copiedPlugin, { recursive: true, filter: (source) => path.basename(source) !== "node_modules" });
    symlinkSync(existsSync(path.join(plugin, "node_modules")) ? path.join(plugin, "node_modules") : path.dirname(plugin), path.join(copiedPlugin, "node_modules"));
    rmSync(path.join(f.agent, "npm/node_modules/pi-subagents"));
    symlinkSync(copiedPlugin, path.join(f.agent, "npm/node_modules/pi-subagents"));
    const ambient = path.join(f.root, "ambient-startup.ts");
    writeFileSync(ambient, `export default (pi) => pi.on("session_start", () => { globalThis[Symbol.for(${JSON.stringify(counterKey)})]++; });`);
    mkdirSync(path.join(f.agent, "agents"));
    writeFileSync(path.join(f.agent, "agents/normal.md"), "---\nname: normal\ndescription: Synthetic child selection.\n---\nDo no work.\n");
    writeFileSync(path.join(f.agent, "agents/explicit.md"), `---\nname: explicit\ndescription: Synthetic explicit override.\nextensions: ${ambient}\n---\nDo no work.\n`);
    const subEntry = path.join(copiedPlugin, "index.js");
    const selected = [subEntry, f.entry];
    const { discoverAgents, clearAgentDiscoveryCache } = await sourceExports(f, "src/agents/agents.js", ["discoverAgents", "clearAgentDiscoveryCache"], copiedPlugin);
    const { buildInProcessChildLaunch } = await sourceExports(f, "src/runs/shared/child-launch.js", ["buildInProcessChildLaunch"], copiedPlugin);
    const { createDefaultChildSessionFactory } = await sourceExports(f, "src/runs/shared/child-session.js", ["createDefaultChildSessionFactory"], copiedPlugin);
    const pi = await import(pathToFileURL(path.join(sdk, "dist/index.js")));
    let session;
    factory = createDefaultChildSessionFactory({ loadPiCodingAgent: async () => ({ ...pi, createAgentSession: async (options) => {
      const created = await pi.createAgentSession(options);
      session = created.session;
      return created;
    } }) });
    await inheritance.start("synthetic-ambient-parent");
    for (const setting of ["defaultExtensions", "defaultSubagentOnlyExtensions"]) {
      writeFileSync(path.join(f.agent, "settings.json"), JSON.stringify({ extensions: [ambient, ...selected], subagents: { [setting]: selected } }));
      clearAgentDiscoveryCache();
      const discovered = discoverAgents(f.root, "user", undefined, { globalNpmRoot: path.join(f.root, "empty-global") });
      const normal = discovered.agents.find((agent) => agent.name === "normal");
      assert.ok(normal);
      assert.deepEqual(discovered.agents.find((agent) => agent.name === "explicit").extensions, [ambient]);
      const input = { host: "runner", cwd: f.root, parentSessionId: "synthetic-ambient-parent", childAgentName: normal.name, childIndex: 0, extensions: normal.extensions, subagentOnlyExtensions: normal.subagentOnlyExtensions, inheritProjectContext: false, inheritGlobalContext: false, inheritSkills: false };
      const selection = { name: "mcp__synthetic__ping", selector: "mcp:synthetic/ping", serverName: "synthetic", toolName: "ping" };
      const mcpPlan = buildInProcessChildLaunch({ ...input, mcpDirectTools: [selection.selector], builtinMcpTools: [selection] });
      assert.deepEqual(mcpPlan.session.builtinMcpTools, [selection]);
      const launch = buildInProcessChildLaunch(input);
      assert.equal(launch.session.ambientExtensions, setting !== "defaultExtensions");
      for (const entry of selected) assert.ok(launch.session.extensionPaths.includes(entry));
      assert.equal(launch.session.requiredExtensions[0].path, f.entry);
      const child = await factory.create(launch.session);
      try {
        assert.equal(globalThis[counter], setting === "defaultExtensions" ? 0 : 1);
        const tools = new Set(session.getAllTools().map((tool) => tool.name));
        for (const name of ["subagent", "contact_supervisor", "bg_wait", "subagents_enable", "write", "edit", "bash_unrestricted"]) assert.ok(tools.has(name), name);
      } finally { await child.dispose(); }
    }
  } finally {
    await factory?.dispose();
    inheritance.dispose();
    delete globalThis[counter];
    for (const name of names) {
      if (previous.get(name) === undefined) delete process.env[name];
      else process.env[name] = previous.get(name);
    }
  }
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
