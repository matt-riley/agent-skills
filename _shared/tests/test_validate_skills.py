import importlib.util
import tempfile
import unittest
import json
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "validate-skills.py"
SPEC = importlib.util.spec_from_file_location("validate_skills", MODULE_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateSkillsRegressionTests(unittest.TestCase):
    def test_load_skill_accepts_multiline_yaml_and_compatibility(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = Path(temp_dir) / "SKILL.md"
            skill.write_text(
                "---\nname: example\ndescription: >-\n  Use when validating\n  multiline YAML.\n"
                "compatibility: Requires Python 3.\nmetadata:\n  kind: reference\n---\n# Example\n"
            )
            frontmatter, _ = VALIDATOR.load_skill(skill)
            self.assertEqual(frontmatter["description"], "Use when validating multiline YAML.")
            self.assertEqual(frontmatter["compatibility"], "Requires Python 3.")

    def test_optional_headings_are_allowed_but_present_headings_are_ordered(self):
        errors = []
        VALIDATOR.validate_canonical_headings(Path("SKILL.md"), "## Validation\n", errors)
        self.assertEqual(errors, [])

        VALIDATOR.validate_canonical_headings(
            Path("SKILL.md"), "## Validation\n\n## Use this skill when\n", errors
        )
        self.assertTrue(any("out of order" in error for error in errors))

    def test_missing_support_link_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir)
            errors = []
            VALIDATOR.validate_support_links(
                skill_dir,
                skill_dir / "SKILL.md",
                "## Reference files\n\n- [Missing](references/missing.md)\n",
                errors,
            )
            self.assertTrue(any("referenced support file missing" in error for error in errors))

    def test_load_skill_rejects_duplicate_yaml_keys(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = Path(temp_dir) / "SKILL.md"
            skill.write_text("---\nname: first\nname: second\n---\n")
            with self.assertRaisesRegex(Exception, "duplicate key"):
                VALIDATOR.load_skill(skill)

    def test_frontmatter_schema_rejects_invalid_metadata_shapes(self):
        for metadata in ("invalid", ["invalid"], {"nested": {"value": "invalid"}}):
            with self.subTest(metadata=metadata):
                errors = []
                VALIDATOR.validate_frontmatter_schema(
                    Path("SKILL.md"),
                    {"license": "GNU GPL v3", "metadata": metadata},
                    errors,
                )
                self.assertTrue(any("string-to-string map" in error for error in errors))

    def test_frontmatter_schema_requires_canonical_license(self):
        for license_value in (None, "MIT"):
            with self.subTest(license=license_value):
                errors = []
                frontmatter = {} if license_value is None else {"license": license_value}
                VALIDATOR.validate_frontmatter_schema(Path("SKILL.md"), frontmatter, errors)
                self.assertTrue(any("license must be GNU GPL v3" in error for error in errors))

    def make_catalog(self, root, skill_names=("one", "two")):
        skills = root / "skills"
        skills.mkdir()
        for name in skill_names:
            skill = skills / name
            (skill / "agents").mkdir(parents=True)
            (skill / "SKILL.md").write_text(f"---\nname: {name}\n---\n")
            (skill / "agents" / "openai.yaml").write_text("interface: {}\n")
        (skills / "README.md").write_text("\n".join(f"- `{name}`" for name in skill_names))
        packages = {".": {}, **{f"skills/{name}": {} for name in skill_names}}
        (root / "release-please-config.json").write_text(json.dumps({"packages": packages}))
        (root / ".release-please-manifest.json").write_text(
            json.dumps({key: "0.1.0" for key in packages})
        )
        return skills

    def test_catalog_invariants_require_openai_metadata(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills = self.make_catalog(root)
            (skills / "two" / "agents" / "openai.yaml").unlink()
            errors = []
            VALIDATOR.validate_catalog_invariants(root, skills, {"one", "two"}, errors)
            self.assertTrue(any("missing agents/openai.yaml" in error for error in errors))

    def test_catalog_invariants_require_chooser_coverage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills = self.make_catalog(root)
            (skills / "README.md").write_text("- `one`\n")
            errors = []
            VALIDATOR.validate_catalog_invariants(root, skills, {"one", "two"}, errors)
            self.assertTrue(any("chooser is missing active skill 'two'" in error for error in errors))

    def test_catalog_invariants_require_matching_release_keysets(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills = self.make_catalog(root)
            (root / ".release-please-manifest.json").write_text(json.dumps({".": "0.1.0"}))
            errors = []
            VALIDATOR.validate_catalog_invariants(root, skills, {"one", "two"}, errors)
            self.assertTrue(any("release package keysets differ" in error for error in errors))

    def test_catalog_invariants_require_existing_release_paths_but_allow_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills = self.make_catalog(root)
            config = json.loads((root / "release-please-config.json").read_text())
            config["packages"]["skills/missing"] = {}
            (root / "release-please-config.json").write_text(json.dumps(config))
            manifest = json.loads((root / ".release-please-manifest.json").read_text())
            manifest["skills/missing"] = "0.1.0"
            (root / ".release-please-manifest.json").write_text(json.dumps(manifest))
            errors = []
            VALIDATOR.validate_catalog_invariants(root, skills, {"one", "two"}, errors)
            self.assertTrue(any("release package path does not exist" in error for error in errors))
            self.assertFalse(any("'.'" in error and "does not exist" in error for error in errors))

    def test_catalog_invariants_require_root_release_package_in_both_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills = self.make_catalog(root)
            config = json.loads((root / "release-please-config.json").read_text())
            del config["packages"]["."]
            (root / "release-please-config.json").write_text(json.dumps(config))
            manifest = json.loads((root / ".release-please-manifest.json").read_text())
            del manifest["."]
            (root / ".release-please-manifest.json").write_text(json.dumps(manifest))
            errors = []
            VALIDATOR.validate_catalog_invariants(root, skills, {"one", "two"}, errors)
            self.assertTrue(any("root release package '.' is required" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
