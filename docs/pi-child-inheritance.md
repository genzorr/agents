# Pi child inheritance

The agentic-local child integration is qualified against Pi `@earendil-works/pi-coding-agent` 1.3.0 and `pi-subagents` 0.78.0 and 0.79.0. Permission-extension loading, global/project instructions, skills, and conversation history are separate mechanisms. Requiring the permission extension does not force instruction or skill inheritance and does not copy parent transcripts.

## Required permission extension

`pi/permissions/child-inheritance.mjs` resolves the public `pi-subagents/required-child-extensions` export from Pi's npm installation at `<agentDir>/npm/node_modules`. `<agentDir>` comes from Pi's `getAgentDir()` and normally means `~/.pi/agent`. The synthetic `createRequire` anchor `<agentDir>/npm/package.json` need not exist. A package installed only through another location is not automatically discovered by this integration. The source accepts only the qualified pi-subagents versions 0.78.0 and 0.79.0; upgrading that dependency requires requalification before the subagent tool can operate.

On `session_start` (startup, reload, new, resume or fork), the extension disposes its previous registration and calls `registerRequiredChildExtensions({ sessionId, extensions: [{ id: "agentic-local", path: <canonical index.ts> }], requireForAllRunners: true })`. The returned handle is held for that session and disposed on `session_shutdown`. Disposal or a newer start invalidates pending asynchronous API loading; stale success cannot register late, and stale failure cannot dispose or replace a newer registration or its status. The API permits one registration owner per session. A conflicting registration is preserved; the integration reports unavailable inheritance and blocks `subagent` tool calls rather than overwrite another host's requirements. Missing package/API, incompatible version and invalid registration also block that tool. Ordinary parent file/bash enforcement remains active. `/agentic-local` shows registration availability alongside its bash dependency probe.

The required snapshot is consumed by native child planning independently of ambient extension loading. In these qualified releases, foreground children otherwise disable ambient extensions. Background children normally enable them unless an explicit agent `extensions` list or capability ceiling disables them. A required path survives `extensions: []`, and a ceiling that denies required extensions rejects the launch. With `requireForAllRunners: true`, the plugin rejects external runners and machine placement because those routes cannot load the required native Pi extension. Parent approval of the `subagent` tool is still required, and the permission gates keep their existing manual exception behavior. A child without a UI cannot approve outside-scope writes or unrestricted bash; this feature adds no forwarding of child approval dialogs to the parent.

Requiring an extension ensures its native loader path, not whole-process confinement. The Pi process, pi-subagents implementation, extension setup/background work, MCP internals and other host APIs remain outside the bash filesystem sandbox. Custom extensions or host code can bypass tool events; plugin slash commands are host-code entrypoints and are not a replacement for the guarded `subagent` tool when registration is unavailable. Manual delegation approval still authorizes the plugin's host-user effects. Existing path-race, hardlink, socket and trusted-code limitations in [Pi permissions](pi-permissions.md#enforcement-boundary) remain.

## Instructions and skills

Pi loads its global agent context and repository context natively, but pi-subagents filters the child's prompt inputs according to the agent definition. Custom agents start with narrow defaults; a new Pi global instruction counterpart alone does not ensure that every custom agent receives the operator's global rules.

| Agent field | Effect in pi-subagents 0.78.0 |
| --- | --- |
| `inheritProjectContext: true` | Retains repository context files such as project `AGENTS.md`; built-in agents opt in by default. |
| `inheritGlobalContext: true` | Retains global context from Pi's agent directory only when project context inheritance is also enabled. Defaults to false. |
| `inheritSkills: true` | Retains Pi's discovered skills catalog. The pi-subagents orchestration skill is removed from a child's inherited catalog. |
| `skills` / `skillPath` | Selects explicit child skills independently of discovered-catalog inheritance. |
| `systemPromptMode: append` | Appends the role prompt to Pi's base prompt; does not by itself enable global/project instructions or the skills catalog. |

To request the global rules and discovered skills for a particular custom agent, explicitly set `inheritProjectContext: true`, `inheritGlobalContext: true`, and `inheritSkills: true` in its definition. Choose `systemPromptMode` separately for that role. This feature does not change agent definitions, inheritance defaults, model/effort, transcript selection or delegation authority.

## Evidence and limits

`tests/pi-permissions/child-inheritance.test.mjs` runs synthetic probes through the installed native source and actual Pi extension/resource loaders. It verifies normal npm-path resolution without an npm package manifest, public registration/disposal across session IDs, delayed-API success/failure after shutdown or a newer start, preservation of a foreign registration, missing/unqualified API behavior, and actual handler rejection before a manual approval could grant unregistered delegation. It builds both native foreground and background launch configurations with ambient discovery enabled/disabled, verifies the required extension loads exactly once, executes its session hook, confirms the child registry contains its entrypoint, and verifies an outside write fails without a UI. It also checks required-extension/capability-ceiling conflict and external/machine admission rejection without launching those routes. The actual native child prompt hook is exercised on synthetic global/project context and skill inputs to prove their separate filters.

Native child execution with model inference, detached-process recovery, appended workflows, nested delegation and live T3 dialogs were not run. Propagation through those retained/nested/recovery paths is supported by the 0.78.0 API documentation and source, not by these tests. Source references are the installed package's `docs/agents.md`, public `src/api/required-child-extensions.js`, `src/shared/required-child-extensions.js`, and `src/runs/shared/{child-launch,child-tool-plan,child-session,subagent-prompt-runtime}.js`. The public export exposes registration/disposal only; tests inspect the package's internal resolver to verify snapshots, while production uses the public API.

Run the focused checks without a login or model request:

```bash
node --test tests/pi-permissions/*.test.mjs
```

Pi-dependent probes skip if the SDK/plugin source is unavailable. Set `PI_SDK_ROOT` and `PI_SUBAGENTS_ROOT` to qualify another installation; production still requires the normal Pi npm package layout. All fixtures use temporary homes. Updating the source checkout does not activate extension changes: reconcile through the optional setup installer after authorization, then start a fresh idle Pi/T3 process.

For native package updates, use the bounded source range and child extension allowlist in [Pi automatic updates](pi-auto-update.md). The allowlist excludes the updater from ordinary children while retaining the existing subagent/permission capabilities; mandatory required-child registration remains separate. Tests use fresh in-memory children, not forked parent conversation history.
