import fs from 'node:fs';
import path from 'node:path';
import { applyTemplate, preparePresentation, renderCards, esc } from './utils.mjs';
import { validateSchema } from './validator.mjs';

// Common CLI head: node render-<type>.mjs [input.json] [output.html]
export function loadDiagram({ rendererDir, diagramType, defaultExample }) {
  const skillRoot = path.resolve(rendererDir, '../..');
  const inputPath = path.resolve(process.argv[2] || path.join(skillRoot, 'examples', defaultExample));
  const diagram = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  validateSchema(diagramType, diagram);
  const presentation = process.env.ARCHIFY_PRESENTATION || 'editorial';
  if (!['editorial', 'interactive', 'classic'].includes(presentation)) {
    throw new Error(`Unknown Archify presentation "${presentation}". Expected editorial, interactive, or classic.`);
  }
  const sourceTemplate = fs.readFileSync(path.join(skillRoot, 'assets/template.html'), 'utf8');
  const template = preparePresentation(sourceTemplate, presentation);
  // Optional chaining: in degraded mode (no ajv) malformed input must still
  // reach the renderer's friendly layout checks instead of crashing here.
  const outPath = path.resolve(process.cwd(), process.argv[3] || diagram.meta?.output || `${diagramType}.html`);
  return { diagram, template, outPath };
}

// Common CLI tail: fill the template and write the standalone HTML file.
// The keyboard hint is screen-only — it means nothing on paper.
export function writeDiagram({ outPath, template, meta, footerLabel, svg, cards }) {
  const presentation = template.match(/data-presentation="([^"]+)"/)?.[1] || 'classic';
  const interactionHint = presentation === 'interactive'
    ? '<span class="no-print"> &bull; Press <kbd>T</kbd> for theme and <kbd>E</kbd> for export</span>'
    : '';
  const footer = presentation === 'classic'
    ? `${footerLabel} &bull; Built with Archify<span class="no-print"> &bull; Press <kbd>T</kbd> for theme and <kbd>E</kbd> for export</span>`
    : `${footerLabel}${interactionHint}`;
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, applyTemplate(template, {
    title: meta.title,
    subtitle: meta.subtitle,
    footer,
    svg,
    cards: renderCards(cards),
  }));
  console.log(outPath);
}

function accessibleNameParts(meta, kind) {
  const name = meta.subtitle ? `${meta.title} — ${meta.subtitle}` : meta.title;
  const base = `${name} (${kind})`;
  const hash = [...base].reduce((value, char) => ((value * 33) ^ char.charCodeAt(0)) >>> 0, 5381).toString(36);
  return { base, titleId: `archify-title-${hash}`, descId: `archify-desc-${hash}` };
}

// Accessible name for the generated diagram SVG.
export function svgRootAttrs(meta, kind) {
  const { titleId, descId } = accessibleNameParts(meta, kind);
  const animation = meta.animation === 'trace' ? ' data-animation="trace"' : '';
  return `role="img" aria-labelledby="${titleId} ${descId}"${animation}`;
}

export function svgAccessibleContent(meta, kind) {
  const { base, titleId, descId } = accessibleNameParts(meta, kind);
  const name = meta.subtitle ? `${meta.title} — ${meta.subtitle}` : meta.title;
  const description = meta.description || `Diagram showing ${name}.`;
  return `<title id="${titleId}">${esc(base)}</title><desc id="${descId}">${esc(description)}</desc>`;
}

export function animateAttr(meta, kind, step) {
  if (meta.animation !== 'trace') return '';
  const safeStep = Number.isFinite(step) && step >= 0 ? Math.floor(step) : 0;
  return ` data-animate="${kind}" style="--step:${safeStep}"`;
}
