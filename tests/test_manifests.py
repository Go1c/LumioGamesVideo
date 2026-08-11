from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "write-game-video-prompt",
    "use-zealman-autodl-workflows",
    "generate-game-cinematic",
    "localize-character-performance",
    "animate-game-menu",
    "create-in-game-loop-media",
    "previsualize-gameplay",
    "create-game-marketing-video",
    "prompt-to-2d-animation",
}


class ManifestTests(unittest.TestCase):
    def test_portable_agent_plugin_manifest(self) -> None:
        manifest = json.loads((REPO_ROOT / "plugin.json").read_text(encoding="utf-8"))
        allowed = {
            "$schema",
            "name",
            "version",
            "description",
            "author",
            "homepage",
            "repository",
            "license",
            "keywords",
            "extensions",
        }
        self.assertEqual(
            manifest["$schema"],
            "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        )
        self.assertFalse(set(manifest) - allowed)
        self.assertRegex(
            manifest["name"],
            re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$"),
        )

    def test_codex_manifest_points_to_real_skill(self) -> None:
        manifest = json.loads(
            (REPO_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["name"], "lumio-games-video")
        self.assertEqual(manifest["skills"], "./skills/")
        skill_root = REPO_ROOT / "skills"
        discovered = {
            path.parent.name for path in skill_root.glob("*/SKILL.md") if path.is_file()
        }
        self.assertEqual(discovered, EXPECTED_SKILLS)

    def test_all_skills_have_matching_metadata(self) -> None:
        for name in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=name):
                root = REPO_ROOT / "skills" / name
                skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
                self.assertRegex(skill_text, rf"(?m)^name: {re.escape(name)}$")
                self.assertNotIn("[TODO", skill_text)
                openai_text = (root / "agents" / "openai.yaml").read_text(
                    encoding="utf-8"
                )
                self.assertIn("$" + name, openai_text)

    def test_skill_relative_links_exist(self) -> None:
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for name in sorted(EXPECTED_SKILLS):
            skill_path = REPO_ROOT / "skills" / name / "SKILL.md"
            skill_text = skill_path.read_text(encoding="utf-8")
            for raw_target in link_pattern.findall(skill_text):
                if "://" in raw_target or raw_target.startswith("#"):
                    continue
                target = (skill_path.parent / raw_target.split("#", 1)[0]).resolve()
                with self.subTest(skill=name, target=raw_target):
                    self.assertTrue(target.exists(), f"missing linked resource: {target}")

    def test_examples_are_valid_json(self) -> None:
        paths = [
            REPO_ROOT / "plugin.json",
            REPO_ROOT / ".codex-plugin" / "plugin.json",
            REPO_ROOT
            / "skills"
            / "prompt-to-2d-animation"
            / "assets"
            / "animation-job.schema.json",
            REPO_ROOT
            / "skills"
            / "prompt-to-2d-animation"
            / "assets"
            / "sequence-manifest.schema.json",
            REPO_ROOT
            / "skills"
            / "prompt-to-2d-animation"
            / "assets"
            / "animation-job.example.json",
            REPO_ROOT
            / "skills"
            / "write-game-video-prompt"
            / "assets"
            / "game-video-job.schema.json",
            REPO_ROOT
            / "skills"
            / "write-game-video-prompt"
            / "assets"
            / "game-video-job.example.json",
        ]
        paths.extend(
            sorted(
                (
                    REPO_ROOT
                    / "skills"
                    / "write-game-video-prompt"
                    / "assets"
                    / "examples"
                ).glob("*.json")
            )
        )
        for path in paths:
            with self.subTest(path=path):
                json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
