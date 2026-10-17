import { readFileSync, realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { createBashToolDefinition, createEditToolDefinition, createLocalBashOperations, createWriteToolDefinition, getAgentDir, type ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { ChildInheritance } from "./child-inheritance.mjs";
import { approve, canonicalPath, existingWriteRoots, mayWrite, normalizeToolPath, sandboxOperations } from "./policy.mjs";

export default function agenticLocal(pi: ExtensionAPI) {
  const childInheritance = new ChildInheritance(getAgentDir(), realpathSync(fileURLToPath(import.meta.url)));
  const profile = JSON.parse(readFileSync(new URL("./profile.json", import.meta.url), "utf8"));
  const roots = existingWriteRoots(profile);
  const local = createLocalBashOperations({ shellPath: "/bin/bash" });
  const sandbox = sandboxOperations(local, roots);
  const cwd = process.cwd();
  const bash = createBashToolDefinition(cwd, { operations: sandbox });
  pi.registerTool({
    ...bash,
    description: `${bash.description}\nagentic-local: Linux filesystem writes are restricted; network and local binding are enabled. Failure never grants an unsandboxed retry.`,
  });
  const unrestricted = createBashToolDefinition(cwd);
  pi.registerTool({
    ...unrestricted,
    name: "bash_unrestricted",
    label: "Bash (manual exception)",
    description: "Request a one-command manual exception to agentic-local. This command runs with all Pi process permissions, without the filesystem sandbox. Requires explicit human approval each time; use only when the user intends an outside-scope action.",
    async execute(id, params, signal, onUpdate, ctx) {
      if (!(await approve(ctx, "agentic-local: run WITHOUT sandbox?", `Working directory: ${ctx.cwd}\nFull host-user permissions for this command:\n${params.command}`, signal))) {
        throw new Error("Unsandboxed command denied or approval unavailable");
      }
      return unrestricted.execute(id, params, signal, onUpdate, ctx);
    },
  });
  for (const factory of [createWriteToolDefinition, createEditToolDefinition]) {
    const tool = factory(cwd);
    pi.registerTool({
      ...tool,
      async execute(id, params, signal, onUpdate, ctx) {
        const target = canonicalPath(normalizeToolPath(params.path, ctx.cwd));
        if (!mayWrite(target, roots) && !(await approve(ctx, `agentic-local: allow outside ${tool.name}?`, `Allow this one file operation with host-user permissions?\n${target}`, signal))) {
          throw new Error("Outside-scope file write denied or approval unavailable");
        }
        return tool.execute(id, params, signal, onUpdate, ctx);
      },
    });
  }
  const builtins = new Set(["bash", "bash_unrestricted", "read", "write", "edit", "grep", "find", "ls"]);
  pi.on("tool_call", async (event, ctx) => {
    if (event.toolName === "subagent" && !childInheritance.active(ctx.sessionManager.getSessionId())) {
      return { block: true, reason: `agentic-local child inheritance unavailable: ${childInheritance.problem ?? "registration missing"}` };
    }
    if (builtins.has(event.toolName)) return;
    if (["subagent", "contact_supervisor", "bg_wait"].includes(event.toolName) && childInheritance.active(ctx.sessionManager.getSessionId())) {
      const tool = pi.getAllTools().find((item) => item.name === event.toolName);
      if (childInheritance.allowsNativeTool(ctx.sessionManager.getSessionId(), tool, event.input, ctx.sessionManager.getBranch())) return;
    }
    if (!(await approve(ctx, "agentic-local: allow extension tool?", `Tool: ${event.toolName}\nArguments: ${JSON.stringify(event.input)}\nExtension/MCP tools run outside this filesystem sandbox. Allow this invocation?`))) {
      return { block: true, reason: "Extension tool denied or approval unavailable" };
    }
  });
  pi.on("tool_result", async (event, ctx) => {
    const input = event.input as Record<string, unknown>;
    const details = event.details as Record<string, unknown> | undefined;
    if (event.toolName !== "subagent" || event.isError || typeof details?.asyncId !== "string" || (input?.action !== undefined && input.action !== "resume")) return;
    const sessionId = ctx.sessionManager.getSessionId();
    if (!childInheritance.active(sessionId)) return;
    const tool = pi.getAllTools().find((item) => item.name === "subagent");
    if (!childInheritance.allowsNativeTool(sessionId, tool, input, ctx.sessionManager.getBranch())) return;
    return { details: { ...details, "agentic-local": { ownerSessionId: sessionId } } };
  });
  pi.on("user_bash", async () => ({ operations: sandbox }));
  pi.on("session_start", async (_event, ctx) => {
    await childInheritance.start(ctx.sessionManager.getSessionId());
    if (!childInheritance.active(ctx.sessionManager.getSessionId())) {
      ctx.ui.notify(`agentic-local: subagent tool blocked; required child inheritance unavailable (${childInheritance.problem}). Parent file/bash guards remain active.`, "warning");
    }
    ctx.ui.setStatus("agentic-local", "agentic-local · bash sandbox required · manual exceptions");
  });
  pi.on("session_shutdown", async () => childInheritance.dispose());
  pi.on("before_agent_start", async (event) => ({
    systemPrompt: `${event.systemPrompt}\n\nagentic-local is active. Read access follows the host user's permissions. Bash writes are restricted to these existing roots: ${roots.join(", ")}. Network and local binding are enabled. File write/edit operations outside those roots require manual approval. For a necessary outside-scope bash operation, request bash_unrestricted, which asks the human for one unsandboxed execution. A failed command is never an approval. With pi-subagents 0.79.0, native subagent list/get/models/guide queries with read-only arguments need no approval. Qualified native subagent direct launches with explicit fresh context may run unattended while required-child inheritance is active; named status, steer, interrupt, resume and stop also require an exact admitted-worker receipt stamped with this session identity, without alternate child selectors or fleet views; external and remote runners are rejected by native admission. Native child contact_supervisor may use its bound immediate-parent channel. Native bg_wait may block on an exact async run id only when this session retains a successful launch/resume receipt stamped with its own identity; use id and optional timeoutMs, without nonBlocking, subscriptions or all. Workflows, configuration changes, host acceptance/output options, and other extension/MCP tools require manual approval and are not filesystem-confined.`,
  }));
  pi.registerCommand("agentic-local", {
    description: "Show agentic-local boundaries and dependency probe",
    async handler(_args, ctx) {
      try {
        let output = "";
        const result = await sandbox.exec("true", ctx.cwd, { onData: (data) => { output += data; }, timeout: 5 });
        ctx.ui.notify(`agentic-local: ${result.exitCode === 0 ? "bash sandbox probe passed" : `bash sandbox UNAVAILABLE (${output.trim()})`}. Writes: ${roots.join(", ")}. Network/local bind enabled. Child inheritance: ${childInheritance.active(ctx.sessionManager.getSessionId()) ? "required for local native children; external/machine launches rejected" : `UNAVAILABLE (${childInheritance.problem})`}. Other tools are not OS-confined.`, result.exitCode === 0 ? "info" : "warning");
      } catch (error) {
        ctx.ui.notify(`agentic-local: bash sandbox UNAVAILABLE (${String(error)}). No automatic fallback.`, "warning");
      }
    },
  });
}
