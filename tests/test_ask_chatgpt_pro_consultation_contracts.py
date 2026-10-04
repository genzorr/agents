"""Structural and static safety checks; not behavioral or outcome evaluation.

The historical conformance readouts remain historical records. Run the scoped behavioral cases when changing consultation meaning, authority, or transport.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "shared" / "skills" / "ask-chatgpt-pro"


class AskChatGPTProConsultationContractsTest(unittest.TestCase):
    def test_entrypoint_metadata_is_loadable(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        metadata, separator, body = text[4:].partition("\n---\n")
        self.assertTrue(separator, "YAML frontmatter is not terminated")
        fields = {}
        for line in metadata.splitlines():
            key, colon, value = line.partition(":")
            self.assertTrue(colon, f"Invalid metadata field: {line!r}")
            self.assertNotIn(key, fields)
            fields[key] = value.strip()
        self.assertEqual(fields.get("name"), "ask-chatgpt-pro")
        self.assertTrue(fields.get("description"))
        self.assertTrue(body.strip())

    def test_both_route_references_are_present(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        links = set(re.findall(r"\]\(([^)]+)\)", text))
        for route in ("pro-consult.md", "plain-research.md"):
            relative = "references/" + route
            self.assertIn(relative, links)
            self.assertTrue((SKILL / relative).is_file())

    def test_local_markdown_links_and_heading_fragments_resolve(self) -> None:
        for source in SKILL.rglob("*.md"):
            text = source.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("mailto:"):
                    continue
                path, _, fragment = target.partition("#")
                destination = (source.parent / path).resolve() if path else source
                with self.subTest(source=source.name, target=target):
                    self.assertTrue(destination.is_file())
                    if fragment:
                        headings = re.findall(r"^#{1,6} (.+)$", destination.read_text(encoding="utf-8"), re.MULTILINE)
                        anchors = {re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-") for h in headings}
                        self.assertIn(fragment, anchors)

    def test_markdown_fences_are_balanced(self) -> None:
        for source in SKILL.rglob("*.md"):
            opener = None
            for line in source.read_text(encoding="utf-8").splitlines():
                match = re.match(r"^(`{3,}|~{3,})(.*)$", line)
                if not match:
                    continue
                fence, suffix = match.groups()
                if opener is None:
                    opener = fence
                elif fence[0] == opener[0] and len(fence) >= len(opener) and not suffix.strip():
                    opener = None
            self.assertIsNone(opener, f"Unclosed code fence in {source}")

    def test_mode_interface_names_remain_available_once_in_table(self) -> None:
        text = (SKILL / "references" / "pro-consult.md").read_text(encoding="utf-8")
        modes = re.findall(r"^\| \*\*([A-Za-z]+)\*\* \|", text, re.MULTILINE)
        self.assertCountEqual(modes, ["Discover", "Verify", "Refine", "Decide", "Execute"])


    def test_context_authority_keeps_the_existing_distinctions(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for category in (
            "Primary evidence", "User requirements and constraints", "Working synthesis",
            "Hypotheses", "Selected decisions", "Preferences and decision criteria",
            "Assumptions and unknowns",
        ):
            self.assertIn(category, text)

    def test_research_stage_preserves_baseline_fidelity_and_requested_scouts(self) -> None:
        entrypoint = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        plain = (SKILL / "references" / "plain-research.md").read_text(encoding="utf-8")
        for stage in (
            "baseline selection", "baseline establishment", "faithful reproduction",
            "adaptation", "diagnosis", "novel improvement",
        ):
            self.assertIn(stage, entrypoint.lower())
            self.assertIn(stage, plain.lower())
        self.assertIn("An established baseline does not need to be novel", entrypoint)
        self.assertIn("instead of stripping components to fit", entrypoint)
        self.assertIn("A causal scout or small discriminator remains legitimate", entrypoint)

    def test_research_recommendations_can_challenge_but_not_replace_user_authority(self) -> None:
        entrypoint = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("challenge an unsound framing explicitly and with evidence", entrypoint)
        self.assertIn("does not itself change the user's goal, selected baseline, method semantics, requested deliverable, or implementation authority", entrypoint)

if __name__ == "__main__":
    unittest.main()
