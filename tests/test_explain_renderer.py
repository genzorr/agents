from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Optional


ROOT = Path(__file__).resolve().parents[1]
CODEX_SKILL = ROOT / "codex" / "skills" / "explain"
CLAUDE_SKILL = ROOT / "claude" / "skills" / "explain"
EXPECTED_CSP = "default-src 'none'; style-src 'unsafe-inline'; img-src 'none'; font-src 'none'; script-src 'none'; connect-src 'none'; media-src 'none'; frame-src 'none'; object-src 'none'; worker-src 'none'; manifest-src 'none'; base-uri 'none'; form-action 'none'"


def minimal_spec() -> dict[str, Any]:
    return {
        "language": "en",
        "title": "Example",
        "mode": "codebase",
        "summary": "A bounded explanation.",
        "scope": "example",
        "sections": [
            {
                "id": "model",
                "title": "Model",
                "blocks": [{"type": "paragraph", "text": "Safe content."}],
            }
        ],
    }


def run_renderer(spec_path: Path, output_path: Path, *, cwd: Optional[Path] = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(CODEX_SKILL / "scripts" / "render_static.py"),
            str(spec_path),
            str(output_path),
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=cwd,
    )


class ExplainRendererTest(unittest.TestCase):
    def test_platform_twins_are_identical_except_codex_metadata(self) -> None:
        for relative in (
            Path("SKILL.md"),
            Path("references/modes.md"),
            Path("references/learning-design.md"),
            Path("references/html-safety.md"),
            Path("scripts/render_static.py"),
        ):
            self.assertEqual(
                (CODEX_SKILL / relative).read_text(encoding="utf-8"),
                (CLAUDE_SKILL / relative).read_text(encoding="utf-8"),
                relative,
            )

    def test_skill_defaults_nontrivial_explanations_to_inert_temporary_html(self) -> None:
        skill = (CODEX_SKILL / "SKILL.md").read_text(encoding="utf-8")
        safety = (CODEX_SKILL / "references" / "html-safety.md").read_text(encoding="utf-8")

        self.assertIn("Default to static HTML for a nontrivial explanation", skill)
        self.assertIn("Save the new artifact under `/tmp`", skill)
        self.assertIn("Use in-chat Markdown alone for a short explanation or when the user requests it", skill)
        self.assertIn("Do not add JavaScript to the default explainer", safety)

    def test_renderer_escapes_source_text_and_emits_inert_html(self) -> None:
        hostile = '</script><script src="https://attacker.invalid/x.js">alert(1)</script>'
        spec = {
            "language": "ru-Latn-RU",
            "title": f"Change {hostile}",
            "mode": "change",
            "summary": "A safe explanation.",
            "scope": "base abc, head def",
            "source_note": hostile,
            "sections": [
                {
                    "id": "mental-model",
                    "title": "Mental model",
                    "blocks": [
                        {"type": "paragraph", "text": hostile},
                        {"type": "bullets", "items": ["one", hostile]},
                        {"type": "numbered", "items": ["first", "second"]},
                        {"type": "code", "language": "html", "text": hostile},
                        {"type": "callout", "title": "Invariant", "text": hostile},
                        {
                            "type": "table",
                            "caption": f"Evidence {hostile}",
                            "headers": ["Source", "Meaning"],
                            "rows": [[hostile, "passive data"]],
                        },
                    ],
                }
            ],
            "questions": [
                {
                    "prompt": hostile,
                    "answer": "It stays text.",
                    "feedback": "The renderer applies contextual HTML escaping.",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            spec_path = temp / "spec.json"
            output_path = temp / "explanation.html"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            result = run_renderer(spec_path, output_path)
            self.assertEqual(result.returncode, 0, result.stderr)
            document = output_path.read_text(encoding="utf-8")

        self.assertNotRegex(document.lower(), r"<(?:script|link|iframe|object|embed|img|form)\b")
        self.assertNotIn('src="https://attacker.invalid', document)
        self.assertNotIn('href="https://attacker.invalid', document)
        self.assertIn("&lt;/script&gt;&lt;script", document)
        self.assertIn(f'content="{EXPECTED_CSP}"', document)
        self.assertIn('<html lang="ru-Latn-RU">', document)
        self.assertIn("<caption>Evidence &lt;/script&gt;", document)
        self.assertIn('<th scope="col">Source</th>', document)
        self.assertIn("white-space: pre-wrap", document)
        self.assertIn("<details>", document)
        self.assertIn('href="#mental-model"', document)

    def test_renderer_rejects_raw_html_blocks(self) -> None:
        spec = {
            "language": "en",
            "title": "Unsafe",
            "mode": "concept",
            "summary": "Rejected input.",
            "scope": "example",
            "sections": [
                {
                    "id": "unsafe",
                    "title": "Unsafe",
                    "blocks": [{"type": "raw-html", "text": "<script>alert(1)</script>"}],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            spec_path = temp / "spec.json"
            output_path = temp / "explanation.html"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            result = run_renderer(spec_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsupported", result.stderr)

    def test_renderer_refuses_to_overwrite_an_existing_file(self) -> None:
        spec = minimal_spec()
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            spec_path = temp / "spec.json"
            output_path = temp / "explanation.html"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            output_path.write_text("keep me", encoding="utf-8")
            result = run_renderer(spec_path, output_path)

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output_path.read_text(encoding="utf-8"), "keep me")

    def test_renderer_rejects_unknown_fields_invalid_language_and_bad_ids(self) -> None:
        unknown = minimal_spec()
        unknown["unexpected"] = True
        invalid_language = minimal_spec()
        invalid_language["language"] = 'en" onclick="alert(1)'
        invalid_id = minimal_spec()
        invalid_id["sections"][0]["id"] = "Bad ID"
        duplicate_id = minimal_spec()
        duplicate_id["sections"].append(
            {
                "id": "model",
                "title": "Duplicate",
                "blocks": [{"type": "paragraph", "text": "Duplicate ID."}],
            }
        )
        cases = (
            ("unknown field", unknown, "unknown fields"),
            ("invalid language", invalid_language, "BCP-47"),
            ("invalid id", invalid_id, "lowercase hyphenated"),
            ("duplicate id", duplicate_id, "duplicated"),
        )

        for label, spec, expected in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                temp = Path(temporary)
                spec_path = temp / "spec.json"
                output_path = temp / "explanation.html"
                spec_path.write_text(json.dumps(spec), encoding="utf-8")
                result = run_renderer(spec_path, output_path)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr)
                self.assertFalse(output_path.exists())

    def test_renderer_rejects_oversized_specs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            spec_path = temp / "spec.json"
            output_path = temp / "explanation.html"
            spec_path.write_bytes(b" " * 2_000_001)
            result = run_renderer(spec_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exceeds 2 MB", result.stderr)

    def test_renderer_validates_output_path_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            spec_path = temp / "spec.json"
            spec_path.write_text(json.dumps(minimal_spec()), encoding="utf-8")
            cases = (
                ("relative", Path("explanation.html"), "absolute path"),
                ("extension", temp / "explanation.txt", ".html extension"),
                ("parent", temp / "missing" / "explanation.html", "parent directory"),
            )
            for label, output_path, expected in cases:
                with self.subTest(label=label):
                    result = run_renderer(spec_path, output_path, cwd=temp)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(expected, result.stderr)


if __name__ == "__main__":
    unittest.main()
