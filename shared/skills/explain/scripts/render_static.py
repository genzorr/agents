#!/usr/bin/env python3
"""Render a structured explanation spec as inert, self-contained HTML."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any


ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
LANGUAGE_TAG_RE = re.compile(r"^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")
CONTENT_SECURITY_POLICY = "default-src 'none'; style-src 'unsafe-inline'; img-src 'none'; font-src 'none'; script-src 'none'; connect-src 'none'; media-src 'none'; frame-src 'none'; object-src 'none'; worker-src 'none'; manifest-src 'none'; base-uri 'none'; form-action 'none'"
ROOT_KEYS = {"language", "title", "mode", "summary", "scope", "source_note", "sections", "questions"}
SECTION_KEYS = {"id", "title", "blocks"}
QUESTION_KEYS = {"prompt", "answer", "feedback"}
BLOCK_KEYS = {
    "paragraph": {"type", "text"},
    "bullets": {"type", "items"},
    "numbered": {"type", "items"},
    "code": {"type", "text", "language"},
    "callout": {"type", "title", "text"},
    "table": {"type", "caption", "headers", "rows"},
}


class SpecError(ValueError):
    """Raised when the content spec is outside the renderer contract."""


def _object(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SpecError(f"{where} must be an object")
    return value


def _list(value: Any, where: str, *, maximum: int) -> list[Any]:
    if not isinstance(value, list):
        raise SpecError(f"{where} must be an array")
    if len(value) > maximum:
        raise SpecError(f"{where} must contain at most {maximum} items")
    return value


def _text(value: Any, where: str, *, maximum: int = 50_000, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise SpecError(f"{where} must be a string")
    if not allow_empty and not value.strip():
        raise SpecError(f"{where} must not be empty")
    if len(value) > maximum:
        raise SpecError(f"{where} exceeds {maximum} characters")
    return value


def _reject_unknown(obj: dict[str, Any], allowed: set[str], where: str) -> None:
    unknown = sorted(set(obj) - allowed)
    if unknown:
        raise SpecError(f"{where} has unknown fields: {', '.join(unknown)}")


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def _render_block(raw: Any, where: str) -> str:
    block = _object(raw, where)
    kind = _text(block.get("type"), f"{where}.type", maximum=32)
    if kind not in BLOCK_KEYS:
        raise SpecError(f"{where}.type is unsupported: {kind}")
    _reject_unknown(block, BLOCK_KEYS[kind], where)

    if kind == "paragraph":
        return f'<p>{_escape(_text(block.get("text"), f"{where}.text"))}</p>'

    if kind in {"bullets", "numbered"}:
        items = _list(block.get("items"), f"{where}.items", maximum=30)
        if not items:
            raise SpecError(f"{where}.items must not be empty")
        tag = "ul" if kind == "bullets" else "ol"
        rendered = "".join(
            f"<li>{_escape(_text(item, f'{where}.items[{index}]'))}</li>"
            for index, item in enumerate(items)
        )
        return f"<{tag}>{rendered}</{tag}>"

    if kind == "code":
        code = _text(block.get("text"), f"{where}.text", maximum=100_000, allow_empty=True)
        language = _text(
            block.get("language", "text"),
            f"{where}.language",
            maximum=32,
        )
        if not re.fullmatch(r"[A-Za-z0-9_+.-]+", language):
            raise SpecError(f"{where}.language contains unsupported characters")
        return (
            '<div class="code-block">'
            f'<div class="code-label">{_escape(language)}</div>'
            f"<pre><code>{_escape(code)}</code></pre>"
            "</div>"
        )

    if kind == "callout":
        title = _text(block.get("title"), f"{where}.title", maximum=200)
        text = _text(block.get("text"), f"{where}.text")
        return (
            '<aside class="callout">'
            f"<strong>{_escape(title)}</strong>"
            f"<p>{_escape(text)}</p>"
            "</aside>"
        )

    caption_html = ""
    if "caption" in block:
        caption = _text(block.get("caption"), f"{where}.caption", maximum=500)
        caption_html = f"<caption>{_escape(caption)}</caption>"
    headers = _list(block.get("headers"), f"{where}.headers", maximum=12)
    rows = _list(block.get("rows"), f"{where}.rows", maximum=100)
    if not headers:
        raise SpecError(f"{where}.headers must not be empty")
    rendered_headers = "".join(
        f'<th scope="col">{_escape(_text(item, f"{where}.headers[{index}]", maximum=500))}</th>'
        for index, item in enumerate(headers)
    )
    rendered_rows: list[str] = []
    for row_index, raw_row in enumerate(rows):
        row = _list(raw_row, f"{where}.rows[{row_index}]", maximum=len(headers))
        if len(row) != len(headers):
            raise SpecError(f"{where}.rows[{row_index}] must match the header count")
        cells = "".join(
            f"<td>{_escape(_text(cell, f'{where}.rows[{row_index}][{cell_index}]', maximum=5_000, allow_empty=True))}</td>"
            for cell_index, cell in enumerate(row)
        )
        rendered_rows.append(f"<tr>{cells}</tr>")
    return (
        '<div class="table-wrap"><table>'
        f"{caption_html}<thead><tr>{rendered_headers}</tr></thead>"
        f"<tbody>{''.join(rendered_rows)}</tbody>"
        "</table></div>"
    )


def render(spec: dict[str, Any]) -> str:
    _reject_unknown(spec, ROOT_KEYS, "root")
    language = _text(spec.get("language"), "root.language", maximum=63)
    if not LANGUAGE_TAG_RE.fullmatch(language):
        raise SpecError("root.language must use a safe BCP-47 language tag")
    title = _text(spec.get("title"), "root.title", maximum=300)
    mode = _text(spec.get("mode"), "root.mode", maximum=80)
    summary = _text(spec.get("summary"), "root.summary", maximum=2_000)
    scope = _text(spec.get("scope"), "root.scope", maximum=2_000)
    source_note = _text(
        spec.get("source_note", ""),
        "root.source_note",
        maximum=5_000,
        allow_empty=True,
    )

    raw_sections = _list(spec.get("sections"), "root.sections", maximum=20)
    if not raw_sections:
        raise SpecError("root.sections must not be empty")
    seen_ids: set[str] = set()
    toc: list[str] = []
    rendered_sections: list[str] = []
    for section_index, raw_section in enumerate(raw_sections):
        where = f"root.sections[{section_index}]"
        section = _object(raw_section, where)
        _reject_unknown(section, SECTION_KEYS, where)
        section_id = _text(section.get("id"), f"{where}.id", maximum=64)
        if not ID_RE.fullmatch(section_id):
            raise SpecError(f"{where}.id must be a lowercase hyphenated identifier")
        if section_id in seen_ids:
            raise SpecError(f"{where}.id is duplicated: {section_id}")
        seen_ids.add(section_id)
        section_title = _text(section.get("title"), f"{where}.title", maximum=300)
        blocks = _list(section.get("blocks"), f"{where}.blocks", maximum=50)
        if not blocks:
            raise SpecError(f"{where}.blocks must not be empty")
        toc.append(f'<li><a href="#{section_id}">{_escape(section_title)}</a></li>')
        rendered_blocks = "".join(
            _render_block(block, f"{where}.blocks[{block_index}]")
            for block_index, block in enumerate(blocks)
        )
        rendered_sections.append(
            f'<section id="{section_id}"><h2>{_escape(section_title)}</h2>{rendered_blocks}</section>'
        )

    raw_questions = _list(spec.get("questions", []), "root.questions", maximum=8)
    rendered_questions: list[str] = []
    for question_index, raw_question in enumerate(raw_questions):
        where = f"root.questions[{question_index}]"
        question = _object(raw_question, where)
        _reject_unknown(question, QUESTION_KEYS, where)
        prompt = _text(question.get("prompt"), f"{where}.prompt", maximum=2_000)
        answer = _text(question.get("answer"), f"{where}.answer", maximum=5_000)
        feedback = _text(question.get("feedback"), f"{where}.feedback", maximum=5_000)
        rendered_questions.append(
            '<article class="question">'
            f"<h3>{question_index + 1}. {_escape(prompt)}</h3>"
            f'<label for="answer-{question_index}">Write or say your answer before revealing feedback.</label>'
            f'<textarea id="answer-{question_index}" rows="4"></textarea>'
            "<details><summary>Reveal answer and feedback</summary>"
            f"<p><strong>Supported answer:</strong> {_escape(answer)}</p>"
            f"<p><strong>Feedback:</strong> {_escape(feedback)}</p>"
            "</details></article>"
        )
    questions_html = ""
    if rendered_questions:
        questions_html = (
            '<section id="check-your-model"><h2>Check your model</h2>'
            '<p>Retrieve first; reveal the evidence-backed feedback afterward.</p>'
            f"{''.join(rendered_questions)}</section>"
        )
        toc.append('<li><a href="#check-your-model">Check your model</a></li>')

    source_html = (
        f'<p class="source-note"><strong>Evidence note:</strong> {_escape(source_note)}</p>'
        if source_note
        else ""
    )

    return f"""<!doctype html>
<html lang="{_escape(language)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="{CONTENT_SECURITY_POLICY}">
  <title>{_escape(title)}</title>
  <style>
    :root {{ color-scheme: light dark; --bg: #f7f7f4; --panel: #ffffff; --text: #202124; --muted: #62666d; --line: #d8d9dc; --accent: #315efb; --callout: #eef2ff; --code: #151821; }}
    @media (prefers-color-scheme: dark) {{ :root {{ --bg: #101216; --panel: #171a20; --text: #eef0f4; --muted: #a8adb7; --line: #30343d; --accent: #8ba6ff; --callout: #20273a; --code: #0b0d12; }} }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--text); font: 17px/1.65 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    main {{ width: min(900px, calc(100% - 32px)); margin: 0 auto; padding: 56px 0 80px; }}
    header, nav, section {{ background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: clamp(20px, 4vw, 40px); margin-bottom: 20px; }}
    h1 {{ margin: 6px 0 12px; font-size: clamp(2rem, 6vw, 3.6rem); line-height: 1.05; letter-spacing: -0.035em; }}
    h2 {{ margin-top: 0; font-size: clamp(1.4rem, 3vw, 2rem); line-height: 1.2; }}
    h3 {{ line-height: 1.35; }}
    p, li {{ max-width: 75ch; }}
    a {{ color: var(--accent); }}
    .eyebrow {{ color: var(--accent); font-size: 0.78rem; font-weight: 750; letter-spacing: 0.12em; text-transform: uppercase; }}
    .summary {{ font-size: 1.15rem; }}
    .scope, .source-note, footer {{ color: var(--muted); }}
    nav ol {{ columns: 2; padding-left: 1.4rem; }}
    .callout {{ margin: 24px 0; padding: 16px 18px; background: var(--callout); border-left: 4px solid var(--accent); border-radius: 8px; }}
    .callout p {{ margin-bottom: 0; }}
    .code-block {{ margin: 24px 0; overflow: hidden; border-radius: 10px; background: var(--code); color: #edf1f7; }}
    .code-label {{ padding: 8px 14px; border-bottom: 1px solid #343946; color: #aeb8ca; font: 0.78rem/1.2 ui-monospace, SFMono-Regular, Menlo, monospace; }}
    pre {{ margin: 0; padding: 18px; overflow-x: auto; white-space: pre-wrap; }}
    code {{ font: 0.9rem/1.55 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .table-wrap {{ overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; }}
    caption {{ margin-bottom: 8px; font-weight: 700; text-align: left; }}
    th, td {{ padding: 10px 12px; border: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ background: var(--callout); }}
    .question {{ margin: 24px 0; padding-top: 8px; border-top: 1px solid var(--line); }}
    label {{ display: block; margin-bottom: 8px; color: var(--muted); }}
    textarea {{ width: 100%; padding: 12px; color: var(--text); background: var(--bg); border: 1px solid var(--line); border-radius: 8px; font: inherit; }}
    textarea:focus, summary:focus, a:focus {{ outline: 3px solid var(--accent); outline-offset: 3px; }}
    details {{ margin-top: 12px; padding: 12px 14px; border: 1px solid var(--line); border-radius: 8px; }}
    summary {{ cursor: pointer; font-weight: 700; }}
    footer {{ padding: 12px 4px; font-size: 0.85rem; }}
    @media (max-width: 640px) {{ main {{ width: min(100% - 20px, 900px); padding-top: 20px; }} nav ol {{ columns: 1; }} header, nav, section {{ border-radius: 12px; }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <div class="eyebrow">{_escape(mode)} explanation</div>
      <h1>{_escape(title)}</h1>
      <p class="summary">{_escape(summary)}</p>
      <p class="scope"><strong>Scope:</strong> {_escape(scope)}</p>
      {source_html}
    </header>
    <nav aria-label="Table of contents"><h2>Contents</h2><ol>{''.join(toc)}</ol></nav>
    {''.join(rendered_sections)}
    {questions_html}
    <footer>Static local explanation. No network assets or executable scripts.</footer>
  </main>
</body>
</html>
"""


def load_spec(path: Path) -> dict[str, Any]:
    if path.stat().st_size > 2_000_000:
        raise SpecError("spec file exceeds 2 MB")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SpecError(f"cannot read JSON spec: {exc}") from exc
    return _object(value, "root")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="Path to the structured JSON spec")
    parser.add_argument("output", type=Path, help="New absolute .html output path")
    args = parser.parse_args()

    output = args.output
    if not output.is_absolute():
        parser.error("output must be an absolute path")
    if output.suffix.lower() != ".html":
        parser.error("output must use the .html extension")
    if not output.parent.is_dir():
        parser.error("output parent directory must already exist")

    try:
        document = render(load_spec(args.spec))
        with output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(document)
    except (OSError, SpecError) as exc:
        parser.error(str(exc))

    print(output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
