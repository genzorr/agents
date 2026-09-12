---
name: archify
description: Create exportable technical diagrams for architecture, workflows, sequences, data flows, and state machines from prose or Mermaid. Deliver standalone HTML/SVG or editable D2; use explain for explanations and architecture-review for critiques.
---

# Archify Skill

Create professional technical diagrams as self-contained HTML files with inline SVG. HTML is the default artifact; the explicit renderer selector also supports validated editable D2 source with `--format d2` or sibling HTML+D2 with `--format html+d2` when a local `d2` executable is available.

Based on `tt-a1i/archify` 2.8, MIT licensed, which is based on `Cocoon-AI/architecture-diagram-generator` v1.0, MIT licensed. Keep `LICENSE` with copied or substantial portions.

The default `editorial` presentation is light, static, dependency-free, and minimally framed: warm paper, dark ink, one restrained green accent, serif page title, sans-serif names, monospace technical labels, low-radius geometry, no pulse, no toolbar, and no visible product branding. Use `--presentation interactive` only when the user wants a dark/light toggle or built-in PNG/JPEG/WebP/SVG export controls. Use `--presentation classic` only for compatibility with the prior dark neon viewer, including its legacy footer. The presentation selector affects HTML and leaves the typed input and D2 semantics unchanged.

When understanding is the goal, use `/explain` even when a diagram makes the mental model clearer; pair the visual with a textual trace and evidence anchors. When the user asks for an architecture critique or system map rather than a diagram artifact, use `/architecture-review` or `/zoom-out` first. Use Archify when the requested deliverable is an exportable technical diagram artifact itself or when another skill's output should become one.

## Setup (one-time, renderer modes only)

The five typed renderers validate JSON against schemas via `ajv`. From this skill's folder:

```bash
npm install
```

Without it the renderers still run — they print a warning and skip schema validation, keeping their own layout checks. The **generated HTML never has dependencies**; only the renderers do.

If you have no shell access at all (e.g. the skill was added as project knowledge), fall back to architecture mode for every request: hand-place SVG into `assets/template.html` following the Design System below, and run the self-review checklist before delivering.

## Choosing a Diagram Type

| Type | Use for | How |
|------|---------|-----|
| `architecture` | System components, cloud resources, services, security boundaries, infrastructure | `renderers/architecture/render-architecture.mjs` + JSON (or hand-place SVG when renderers can't run) |
| `workflow` | Technical flows, approval gates, tool calls, runbooks, CI/CD, incident response | `renderers/workflow/render-workflow.mjs` + JSON |
| `sequence` | API call chains, request lifecycles, cache fallback, async traces, return paths | `renderers/sequence/render-sequence.mjs` + JSON |
| `dataflow` | Pipelines, ETL/ELT, PII isolation, lineage, warehouse sync, consumers | `renderers/dataflow/render-dataflow.mjs` + JSON |
| `lifecycle` | State machines, status transitions, wait states, retries, terminal states | `renderers/lifecycle/render-lifecycle.mjs` + JSON |

Trigger phrases: "architecture/system/cloud diagram" → `architecture` (unless clearly process-oriented). "workflow/flow/process/runbook/approval/CI-CD/incident" → `workflow`. "sequence/interaction/call chain/who calls whom" → `sequence`. "data flow/pipeline/ETL/lineage/PII/governance" → `dataflow`. "state/status/lifecycle/state machine/retry/terminal" → `lifecycle`.

## Mermaid as an Input Dialect

When the user pastes Mermaid code, do NOT try to render or parse it mechanically — read it for structure and **lay out from scratch** in the matching archify mode:

| Mermaid | Archify mode | Mapping |
|---------|--------------|---------|
| `flowchart` / `graph` | `workflow` (or `architecture` if it's a component map) | `subgraph` → lane or region boundary; node shape `{}` (diamond) → decision/security node; `-->` labels → edge labels (use sparingly); `classDef`/`style` → nearest semantic type |
| `sequenceDiagram` | `sequence` | `participant` → participants (pick semantic `type` from the name); `->>` → message, `-->>` → `return` variant; `Note` → message `note`; `rect` blocks → segments |
| `stateDiagram` | `lifecycle` | states → states (pick `start`/`active`/`waiting`/`success`/`failure` from names); `[*]` start/end → `start` type / `terminal` lane; transition labels → event-like labels |

Drop Mermaid styling; keep only the topology and meaning. You choose grouping, lane order, and what deserves emphasis — that judgment is the product.

## Renderer Modes (architecture / workflow / sequence / dataflow / lifecycle)

Read [references/output-fidelity.md](references/output-fidelity.md) when choosing destination, audience, detail, compression, or dual-format fidelity. Read [references/semantic-patterns.md](references/semantic-patterns.md) when behavior-rich content needs a nearest-type semantic pattern. The D2 adapter uses the same typed JSON authority as HTML, encodes all input strings safely, validates with local `d2 fmt --check`, `d2 validate`, and an ephemeral compile, and publishes no compiled derivative.

All five modes follow the same loop:

1. **Read first**: the schema (`schemas/<type>.schema.json`) and the complete worked example (`examples/*.{architecture,workflow,sequence,dataflow,lifecycle}.json`) — copy its patterns instead of guessing field shapes.
2. Write `<name>.<type>.json`.
3. Render the static editorial default: `node bin/archify.mjs render <type> <input>.json <output>.html` (paths relative to this skill's folder). Add `--presentation interactive` for theme/export controls or `--presentation classic` only for legacy compatibility.
4. Validate the generated artifact: `node bin/archify.mjs validate <type> <input>.json --json`, or check an existing HTML file with `node bin/archify.mjs check <output>.html`. This catches malformed SVG output, non-finite SVG values, two-point diagonal arrows, shared-edge fanout, overlapping edge segments, connector labels crossed by other paths, and arrows crossing the legend.
5. If either step fails, the error names the JSON path or the fix (thresholds, valid ranges, which knob to change). Fix the JSON and re-run; never edit the renderer.

Schema violations exit non-zero with path-prefixed messages like `/nodes/3 (id/label: "router") must NOT have additional properties`. The renderers additionally fail fast on layout problems: node/state overlap (including cross-lane), labels colliding with nodes or other labels, labels wider than their node, out-of-range columns/rows, too-short edges, workflow edges crossing unrelated nodes, shared connector trunks, edge-segment overlap, connector-label clearance, and legends outside the viewBox. CJK text is measured at double width automatically.

Set `meta.animation: "trace"` only when the user asks for motion or a presentation/demo view. It adds lightweight SVG/CSS trace animation to renderer-marked arrows and nodes, respects `prefers-reduced-motion`, and leaves the default static output unchanged.

### Mode guidance

The complete typed inputs live in `examples/*.json`, and the renderer READMEs carry detailed layout language for workflow, sequence, dataflow, and lifecycle. Read the matching schema and canonical example before the first diagram; read the mode README where one exists. These bundled files are the canonical examples, so this entrypoint keeps only the constraints that prevent common layout mistakes.

Keep density near an editorial figure, not an operations dashboard. Prefer one reading direction, orthogonal paths, distinct attachment sides for fan-in/fan-out, short event-like connector labels, and whitespace over extra decoration. Do not route multiple relationships along the same segment or let a path pass through another connector's label; use explicit sides, `via`, channels, or label offsets until `archify check` passes.

- **Workflow**: use lanes, optional phases and groups, and an optional ordered `mainPath`; reserve labels for cross-lane transitions, approvals, asynchronous work, and returns. The six columns are at x positions `[88, 220, 300, 430, 500, 625]`; adjacent columns 1↔2 and 3↔4 are too close for default-width nodes in one lane. Omit `meta.viewBox` so height follows lane count, and use exception lanes for retry or fallback paths.
- **Sequence**: keep participants to the available width (x = 62 + index×108, at most eight in the default viewBox), keep messages at least 28px apart on shared spans and at least 60px across, and remember that segment and activation `from`/`to` values are y coordinates. Keep labels short and event-like.
- **Dataflow**: use 2–5 stages, rows 0–4, and labeled flows; put sensitivity in `classification` and use `emphasis`, `security`, or `dashed` for primary, policy-sensitive, or asynchronous paths. The default grid uses x = 100 + stage×215 and y = `[128, 242, 356, 470, 584]`.
- **Lifecycle**: use the required `main` lane for phases and `terminal` for outcomes; other lanes share the middle event band. Keep transition labels sparse and event-like, and use state tags or step numbers for detail.
- **Architecture**: place components with free `pos` coordinates, describe boundaries with `wraps`, and route connections with explicit sides or orthogonal routes. Use the renderer's overlap, collision, and off-canvas diagnostics rather than hand-tuning around them.

## Architecture Mode

Architecture has the same read-schema-then-render loop as the other modes — prefer it. Hand-placed SVG is the fallback for when renderers can't run.

Use the canonical `examples/web-app.architecture.json` input when you need a concrete architecture shape.

Render: `node renderers/architecture/render-architecture.mjs <input>.json <output>.html`.

**The renderer does the mechanical work that used to be hand-tuned**, so you only choose coordinates and meaning:

- **Free coordinates** — `pos: [x, y]` is the component's top-left; `size: [w, h]` defaults to `[120, 60]`. Unlike the typed modes there is no lane/stage grid — asymmetric placement is yours to choose. `meta.viewBox` is optional (auto-fitted to your components + a legend row).
- **Boundaries from `wraps`** — list the component ids a `region` (dashed amber) or `security-group` (dashed rose) encloses; the renderer computes the box with correct 30/50 padding automatically. Never hand-arithmetic a boundary again.
- **Connections** route like edges (`variant`, `fromSide`/`toSide`, `route: straight|orthogonal-h|orthogonal-v|auto`, `via`, `labelDx/labelDy/labelAt`). For a vertical labeled connection, push the label into the gap with `labelDy` (the validator will tell you if it lands on a box).
- The renderer auto-emits the two-rect `c-mask` pattern, draws arrows before boxes (z-order), builds the legend from the component types you used, and **fails fast on component overlap, off-canvas components/boundaries, unknown wraps/connection ids, label-vs-component collisions, and non-finite coordinates** — the same reliability the other four modes already had.

### Hand-placed fallback (no renderer available)

When Node/ajv can't run, copy `assets/template.html` and place SVG by hand. Study the worked diagram inside the template and `examples/web-app.architecture.json` for coordinate idioms, follow the Design System below, and run the self-review checklist before delivering. For the static default, remove all three `ARCHIFY:INTERACTIVE_*` marked blocks. Retain their contents and change `data-presentation` to `interactive` only when controls were requested.

### The Cardinal Rule: CSS classes, not inline colors

The editorial and classic palettes use CSS custom properties, and interactive output switches them through `data-theme`. Hardcoded `fill="rgba(...)"` or `stroke="#22d3ee"` will not follow the selected presentation. Always use the class system:

```svg
<rect x="X" y="Y" width="W" height="H" rx="6" class="c-mask"/>
<rect x="X" y="Y" width="W" height="H" rx="6" class="c-backend" stroke-width="1.5"/>
<text x="CX" y="CY" class="t-primary" font-size="11" font-weight="600" text-anchor="middle">API Server</text>
<text x="CX" y="CY+16" class="t-muted" font-size="9" text-anchor="middle">FastAPI :8000</text>
```

### Design system

Component fills `c-frontend` (clients/UI), `c-backend` (services/APIs), `c-database` (stores/caches), `c-cloud` (managed infra), `c-security` (auth/secrets), `c-messagebus` (Kafka/queues), `c-external` (3rd parties); text roles `t-<same>` plus neutrals `t-primary` / `t-muted` / `t-dim`. The editorial skin maps these roles to one accent plus ink/muted tonal variants instead of a rainbow. Arrows `a-default`, `a-emphasis` (primary path), `a-security` (dashed), `a-dashed` (async) — always set `stroke-width` and pair `marker-end="url(#arrowhead[-variant])"` with the matching class. Boundaries: `c-security-group`, `c-region`, `c-lane`.

The page title uses a system serif, component names use system sans, and technical sublabels, ports, events, and annotations use system monospace. No remote font is required. Sizes: 11–12px component names, 9px sublabels, 8px annotations, 7px tiny labels.

### Hard layout rules

- **Two-rect pattern everywhere**: opaque `c-mask` rect first, styled `c-<type>` rect on top — semi-transparent fills otherwise let arrows bleed through.
- **Arrows before components** in document order (SVG paints in order; arrows must sit behind boxes).
- **Vertical stacking**: ≥40px gap between components; inline connectors (message buses, 20px tall) live inside the gap, never overlapping boxes.
- **Boundary padding**: boundary `y` = inner `y` − 30, boundary `height` = inner `height` + 50, label baseline 18px below the boundary top.
- **Legend placement**: outside ALL boundary boxes, ≥20px below the lowest one; grow the viewBox if needed.

### Self-review checklist (run before delivering)

1. `grep -E 'fill="(#|rgb)|stroke="(#|rgb)' out.html` inside the SVG returns nothing except the template's own defs (Cardinal Rule).
2. Every `c-<type>` rect has an identical-geometry `c-mask` rect immediately before it.
3. All `<line>`/`<path>` arrows appear before all component rects in document order.
4. Compute max(y + height) over all SVG elements: viewBox height must exceed it by ≥20px; same for x/width.
5. Legend y is below every boundary's y + height.
6. No two connector routes share a segment, every fan-out gets a distinct visible route, and no connector crosses another connector's label.
7. Static editorial output contains no `<script>`, `.toolbar`, remote font URL, `Built with Archify`, or animation unless the user explicitly requested it.
8. Interactive and classic output retain the three marked blocks and the `:root` / `[data-theme]` CSS unchanged; classic also selects the legacy dark palette, denser frame, and footer.

## Output

A single self-contained `.html` with embedded CSS and inline SVG. The default editorial artifact contains no JavaScript or network dependency. Interactive output additionally embeds the legacy theme/export runtime; raster exports render natively at up to 4× the viewBox (large diagrams step down to 3×/2× to stay under canvas limits), and SVG export is dual-theme and self-contained. Editable D2 remains available through the explicit format selector.
