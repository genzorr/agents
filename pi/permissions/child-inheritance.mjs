import { readFileSync, realpathSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { isDeepStrictEqual } from "node:util";

const QUALIFIED_PI_SUBAGENTS_VERSIONS = Object.freeze(["0.78.0", "0.79.0"]);

function unattendedSubagentInput(sessionId, input, branch) {
  if (!input || typeof input !== "object" || Array.isArray(input)) return false;
  const { options = {}, ...topLevel } = input;
  if (!options || typeof options !== "object" || Array.isArray(options)) return false;
  for (const [key, value] of Object.entries(options)) {
    if (key === "options" || (topLevel[key] !== undefined && !isDeepStrictEqual(topLevel[key], value))) return false;
  }
  const params = { ...topLevel, ...options };
  if (params.action !== undefined) {
    const missionFields = {
      "mission.create": ["mission", "missionStatus"],
      "mission.list": ["missionScope"],
      "mission.show": ["missionId"],
      "mission.update": ["missionId", "missionUpdate"],
      "mission.resolve-decision": ["missionId", "id", "summary"],
      "mission.attach-run": ["missionId", "id", "runId", "runMode", "dir", "agent", "runStatus"],
      "mission.close": ["missionId", "missionStatus", "summary"],
    }[params.action];
    if (Array.isArray(missionFields)) {
      if (!Object.keys(params).every((key) => ["action", ...missionFields].includes(key))) return false;
      if (params.missionScope !== undefined && !["project", "global"].includes(params.missionScope)) return false;
      if (params.action === "mission.close" && params.missionStatus !== undefined && !["completed", "failed", "cancelled"].includes(params.missionStatus)) return false;
      for (const [field, keys] of [["mission", ["title", "summary", "objective", "labels"]], ["missionUpdate", ["title", "objective", "summary", "labels", "artifacts", "receipts", "decisions", "status"]]]) {
        if (params[field] !== undefined && (!params[field] || typeof params[field] !== "object" || Array.isArray(params[field]) || !Object.keys(params[field]).every((key) => keys.includes(key)))) return false;
      }
      return true;
    }
    if (["list", "get", "models"].includes(params.action)) {
      const fields = params.action === "list" ? ["agent", "agentScope", "capabilities"] : ["agent", "agentScope"];
      return Object.keys(params).every((key) => ["action", ...fields].includes(key)) && (params.agent === undefined || typeof params.agent === "string") && (params.agentScope === undefined || ["user", "project", "both"].includes(params.agentScope)) && (params.capabilities === undefined || typeof params.capabilities === "boolean");
    }
    if (params.action === "guide") return Object.keys(params).every((key) => ["action", "topic"].includes(key)) && (params.topic === undefined || typeof params.topic === "string");
    if (params.action === "doctor") return Object.keys(params).every((key) => ["action", "context", "sessionDir"].includes(key)) && (params.context === undefined || ["fresh", "fork", "profile"].includes(params.context)) && (params.sessionDir === undefined || typeof params.sessionDir === "string");
    if (params.action === "children.list") return Object.keys(params).length === 1;
    if (!["status", "debug.run", "command.status", "steer", "interrupt", "resume", "stop"].includes(params.action) || !ownedWorkerReceipt(sessionId, params.id, branch)) return false;
    const permitted = params.action === "status" ? ["view", "lines"] : params.action === "command.status" ? ["toolCallId"] : params.action === "steer" ? ["mode", "ackTimeoutMs", "steeringRecovery"] : [];
    return Object.keys(params).every((key) => ["action", "id", "message", ...permitted].includes(key)) && (params.view === undefined || params.view === "transcript") && (params.mode === undefined || ["steer", "follow_up", "auto"].includes(params.mode)) && (params.steeringRecovery === undefined || params.steeringRecovery === false);
  }
  const limits = ["context", "timeoutMs", "maxRuntimeMs", "toolTimeoutMs", "toolBudget", "checkpointBeforeDeadlineMs", "agentScope"];
  return typeof params.agent === "string" && Boolean(params.agent.trim()) && Object.keys(params).every((key) => ["agent", "task", "async", "model", "cwd", ...limits].includes(key)) && params.context === "fresh" && (params.agentScope === undefined || ["user", "project", "both"].includes(params.agentScope));
}

function ownedWorkerReceipt(sessionId, id, branch) {
  return typeof id === "string" && Boolean(id) && branch.some((entry) => entry.type === "message" && entry.message.role === "toolResult" && entry.message.toolName === "subagent" && !entry.message.isError && entry.message.details?.asyncId === id && entry.message.details?.["agentic-local"]?.ownerSessionId === sessionId);
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
      if (!input || !Object.keys(input).every((key) => ["id", "timeoutMs", "nonBlocking", "all"].includes(key)) || !ownedWorkerReceipt(sessionId, input.id, branch) || (input.nonBlocking !== undefined && input.nonBlocking !== false) || (input.all !== undefined && input.all !== false)) return false;
      if (source?.source === "inline" && source.path === "<inline:pi-subagents:prompt-runtime>") return true;
    } else if (tool?.name === "subagent_supervisor") {
      if (!input || typeof input !== "object" || Array.isArray(input)) return false;
      if (["list", "pending", "status"].includes(input.action)) {
        if (Object.keys(input).length !== 1) return false;
      } else if (input.action !== "reply" || !Object.keys(input).every((key) => ["action", "replyTo", "message"].includes(key)) || typeof input.replyTo !== "string" || !input.replyTo.trim() || typeof input.message !== "string" || !input.message.trim()) return false;
      if (source?.source === "inline" && ["<inline:pi-subagents:prompt-runtime>", "<inline:pi-subagents:fanout-child>"].includes(source.path)) return true;
    } else {
      if (tool?.name !== "subagent" || !unattendedSubagentInput(sessionId, input, branch)) return false;
      if (source?.source === "inline" && source.path === "<inline:pi-subagents:fanout-child>") return true;
    }
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
