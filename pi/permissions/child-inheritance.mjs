import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";

export async function loadRequiredChildApi(agentDir) {
  const require = createRequire(path.join(agentDir, "npm", "package.json"));
  const manifest = JSON.parse(readFileSync(path.join(path.dirname(require.resolve("pi-subagents")), "package.json"), "utf8"));
  if (manifest.name !== "pi-subagents" || manifest.version !== "0.78.0") {
    throw new Error("agentic-local child inheritance requires qualified pi-subagents 0.78.0");
  }
  const entry = require.resolve("pi-subagents/required-child-extensions");
  const api = await import(pathToFileURL(entry).href);
  if (typeof api.registerRequiredChildExtensions !== "function") {
    throw new Error("pi-subagents required-child-extensions API is unavailable");
  }
  return api;
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

  dispose() {
    this.generation++;
    this.registration?.dispose();
    this.registration = undefined;
    this.sessionId = undefined;
    this.problem = "not registered for this session";
  }
}
