import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const TEST_DIR = path.dirname(fileURLToPath(import.meta.url));
const SCRIPT = path.resolve(TEST_DIR, "../validate-skill-library.mjs");
const FIXTURES = path.join(TEST_DIR, "fixtures");

function validate(...fixtureNames) {
  return spawnSync(
    process.execPath,
    [SCRIPT, ...fixtureNames.map((name) => path.join(FIXTURES, name, "SKILL.md"))],
    { encoding: "utf8" },
  );
}

test("accepts canonical YAML and optional sections", () => {
  const result = validate("valid-yaml-and-optional-sections");
  assert.equal(result.status, 0, result.stderr);
});

test("accepts an inter-skill-only Reference files section", () => {
  const result = validate("valid-inter-skill-reference");
  assert.equal(result.status, 0, result.stderr);
});

test("rejects headings that are present in the wrong semantic order", () => {
  const result = validate("invalid-heading-order");
  assert.equal(result.status, 1);
  assert.match(result.stderr, /heading out of order/);
});

test("rejects Guardrails in the wrong semantic position", () => {
  const result = validate("invalid-guardrails-order");
  assert.equal(result.status, 1);
  assert.match(result.stderr, /heading out of order ## Guardrails/);
});

test("rejects missing local support links", () => {
  const result = validate("invalid-support-link");
  assert.equal(result.status, 1);
  assert.match(result.stderr, /missing referenced file references\/missing\.md/);
});

test("rejects unsupported metadata", () => {
  const result = validate("invalid-metadata");
  assert.equal(result.status, 1);
  assert.match(result.stderr, /forbidden top-level frontmatter key: unknown-key/);
});

for (const fixture of [
  "invalid-metadata-scalar",
  "invalid-metadata-list",
  "invalid-metadata-nested",
]) {
  test(`rejects invalid metadata shape: ${fixture}`, () => {
    const result = validate(fixture);
    assert.equal(result.status, 1);
    assert.match(result.stderr, /metadata must be a string-to-string map/);
  });
}

test("rejects duplicate YAML keys", () => {
  const result = validate("invalid-duplicate-key");
  assert.equal(result.status, 1);
  assert.match(result.stderr, /Map keys must be unique|duplicate/i);
});

for (const fixture of ["invalid-missing-license", "invalid-wrong-license"]) {
  test(`requires GNU GPL v3 license: ${fixture}`, () => {
    const result = validate(fixture);
    assert.equal(result.status, 1);
    assert.match(result.stderr, /license must be GNU GPL v3/);
  });
}
