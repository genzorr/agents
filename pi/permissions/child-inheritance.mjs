import { readFileSync, realpathSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";

const QUALIFIED_PI_SUBAGENTS_VERSIONS = Object.freeze(["0.78.0", "0.79.0"]);

function unattendedSubagentInput(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) return false;
  const options = input.options ?? {};
  if (!options || typeof options !== "object" || Array.isArray(options)) return false;
  if (input.action !== undefined) {
    if (input.action === "children.list") return Object.keys(input).every((key) => key === "action");
    if (!["status", "steer", "interrupt", "resume", "stop"].includes(input.action) || (!(input.action === "status" && input.id === undefined) && (typeof input.id !== "string" || !input.id.trim()))) return false;
    return Object.keys(input).every((key) => ["action", "id", "message", "options"].includes(key)) && Object.keys(options).every((key) => ["index", "childId", "view", "lines", "mode", "ackTimeoutMs"].includes(key));
  }
  const limits = ["context", "timeoutMs", "maxRuntimeMs", "toolTimeoutMs", "toolBudget", "checkpointBeforeDeadlineMs"];
  if (typeof input.agent !== "string" || !input.agent.trim() || !Object.keys(input).every((key) => ["agent", "task", "async", "model", "cwd", "options", ...limits].includes(key)) || !Object.keys(options).every((key) => limits.includes(key))) return false;
  return (input.context === "fresh" || options.context === "fresh") && [input.context, options.context].every((context) => context === undefined || context === "fresh");
}

function ownedWaitReceipt(sessionId, input, branch) {
  if (!input || typeof input.id !== "string" || !input.id || !Object.keys(input).every((key) => ["id", "timeoutMs"].includes(key))) return false;
  return branch.some((entry) => entry.type === "message" && entry.message.role === "toolResult" && entry.message.toolName === "subagent" && !entry.message.isError && entry.message.details?.asyncId === input.id && entry.message.details?.["agentic-local"]?.ownerSessionId === sessionId);
}

export async function loadRequiredChildApi(agentDir) {
  const require = createRequire(path.join(agentDir, "npm", "package.json"));
  const nativeSubagentEntry = realpathSync(require.resolve("pi-subagents"));
  const manifest = JSON.parse(readFileSync(path.join(path.dirname(nativeSubagentEntry), "package.json"), "utf8"));
  if (manifest.name !== "pi-subagents" || !QUALIFIED_PI_SUBAGENTS_VERSIONS.includes(manifest.version)) {
    throw new Error(`agentic-local child inheritance requires qualified pi-subagents ${QUALIFIED_PI_SUBAGENTS_VERSIONS.join(" or ")}`);
  }
  const entry = require.resolve("pi-subagents/required-child-extensions");
  const api = await import(pathToFileURL(entry).href);
  if (typeof api.registerRequiredChildExtensions !== "function") {
    throw new Error("pi-subagents required-child-extensions API is unavailable");
  }
  return { ...api, nativeSubagentEntry: manifest.version === "0.79.0" ? nativeSubagentEntry : undefined };
}

export class ChildInheritance {
  constructor(agentDir, extensionPath, loadApi = loadRequiredChildApi) {
    this.agentDir = agentDir;
    this.extensionPath = extensionPath;
    this.loadApi = loadApi;
    this.generation = 0;
    this.problem = "not registered for this session";
  }

  async start(sessionId) {
    this.dispose();
    const generation = this.generation;
    try {
      const api = await this.loadApi(this.agentDir);
      if (generation !== this.generation) return;
      const registration = api.registerRequiredChildExtensions({
        sessionId,
        extensions: [{ id: "agentic-local", path: this.extensionPath }],
        requireForAllRunners: true,
      });
      if (!registration || typeof registration.dispose !== "function") throw new Error("Invalid child extension registration handle");
      this.registration = registration;
      this.nativeSubagentEntry = api.nativeSubagentEntry;
      this.sessionId = sessionId;
      this.problem = undefined;
    } catch (error) {
      if (generation !== this.generation) return;
      this.dispose();
      this.problem = error instanceof Error ? error.message : String(error);
    }
  }

  active(sessionId) {
    return Boolean(this.registration && sessionId === this.sessionId);
  }

  allowsNativeTool(sessionId, tool, input, branch = []) {
    if (!this.active(sessionId) || !this.nativeSubagentEntry) return false;
    const source = tool?.sourceInfo;
    if (tool?.name === "contact_supervisor") {
      return source?.source === "inline" && source.path === "<inline:pi-subagents:prompt-runtime>";
    }
    if (tool?.name === "bg_wait") {
      if (!ownedWaitReceipt(sessionId, input, branch)) return false;
      if (source?.source === "inline" && source.path === "<inline:pi-subagents:prompt-runtime>") return true;
      try { return realpathSync(source?.path ?? "") === this.nativeSubagentEntry; }
      catch { return false; }
    }
    if (tool?.name !== "subagent" || !unattendedSubagentInput(input)) return false;
    if (source?.source === "inline" && source.path === "<inline:pi-subagents:fanout-child>") return true;
    try { return realpathSync(source?.path ?? "") === this.nativeSubagentEntry; }
    catch { return false; }
  }

  dispose() {
    this.generation++;
    this.registration?.dispose();
    this.registration = undefined;
    this.nativeSubagentEntry = undefined;
    this.sessionId = undefined;
    this.problem = "not registered for this session";
  }
}
