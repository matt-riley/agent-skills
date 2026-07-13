#!/usr/bin/env node

import { access, readFile, readdir } from "node:fs/promises";
import { constants as fsConstants } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseDocument } from "yaml";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(SCRIPT_DIR, "../../..");
const SKILLS_ROOT = path.join(REPO_ROOT, "skills");

const CANONICAL_HEADINGS = [
  "## Use this skill when",
  "## Do not use this skill when",
  "## Inputs to gather",
  "## First move",
  "## Workflow",
  "## Guardrails",
  "## Validation",
  "## Examples",
  "## Reference files",
];

const VALID_KINDS = new Set(["task", "reference"]);

// Metadata contract: only these top-level keys are permitted in skill frontmatter.
// See skills/skill-authoring/references/metadata-contract.md for rationale.
// `license` is allowed because this catalog is GPL-licensed and AGENTS.md requires it in skill frontmatter.
const ALLOWED_TOP_LEVEL_KEYS = new Set([
  "name",
  "description",
  "metadata",
  "license",
  "compatibility",
]);

// Upstream provenance keys that must not appear inside the metadata block.
// `version` is intentionally omitted: release-managed skills mirror their version
// into `metadata.version` via Release Please, which is the repo's versioning contract.
const FORBIDDEN_METADATA_KEYS = new Set([
  "github-path",
  "github-ref",
  "github-repo",
  "github-tree-sha",
  "author",
  "inspired-by",
  "enhancements",
]);

function normalize(text) {
  return text.replace(/\r\n?/g, "\n");
}

// fallow-ignore-next-line complexity
function parseFrontmatter(text) {
  const normalized = normalize(text);
  if (!normalized.startsWith("---\n")) {
    throw new Error("missing frontmatter block");
  }

  const endIndex = normalized.indexOf("\n---\n", 4);
  if (endIndex === -1) {
    throw new Error("unterminated frontmatter block");
  }

  const frontmatterText = normalized.slice(4, endIndex);
  const body = normalized.slice(endIndex + 5);
  const document = parseDocument(frontmatterText, { uniqueKeys: true });
  if (document.errors.length > 0) {
    throw new Error(`invalid YAML frontmatter: ${document.errors[0].message}`);
  }
  const frontmatter = document.toJS();
  if (!frontmatter || typeof frontmatter !== "object" || Array.isArray(frontmatter)) {
    throw new Error("frontmatter must be a YAML mapping");
  }

  return { frontmatter, body };
}

function parseOpeningFence(line) {
  const trimmed = line.trimStart();
  const match = trimmed.match(/^(?:[-+*]|\d+\.)?\s*(`{3,}|~{3,})/);
  if (!match) {
    return null;
  }

  return {
    marker: match[1][0],
    length: match[1].length,
  };
}

function isClosingFence(line, openingFence) {
  const trimmed = line.trimStart();
  const match = trimmed.match(/^(?:[-+*]|\d+\.)?\s*(`{3,}|~{3,})\s*$/);
  if (!match) {
    return false;
  }

  return (
    match[1][0] === openingFence.marker &&
    match[1].length >= openingFence.length
  );
}

// fallow-ignore-next-line complexity
function stripFencedCodeBlocks(body) {
  const lines = body.split("\n");
  const strippedLines = [];
  const errors = [];
  let openingFence = null;
  let openingFenceLine = -1;

  for (const [index, line] of lines.entries()) {
    if (!openingFence) {
      const fence = parseOpeningFence(line);
      if (fence) {
        openingFence = fence;
        openingFenceLine = index + 1;
        strippedLines.push("");
        continue;
      }

      strippedLines.push(line);
      continue;
    }

    if (isClosingFence(line, openingFence)) {
      openingFence = null;
      openingFenceLine = -1;
      strippedLines.push("");
      continue;
    }

    strippedLines.push("");
  }

  if (openingFence) {
    errors.push(
      `unterminated fenced code block starting on line ${openingFenceLine}`,
    );
  }

  return {
    searchableBody: strippedLines.join("\n"),
    errors,
  };
}

function findHeadingLineIndex(lines, heading) {
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const leadingSpaces = line.length - line.trimStart().length;
    const normalizedHeadingLine = line.trim().replace(/\s+#+\s*$/, "");
    if (leadingSpaces < 4 && normalizedHeadingLine === heading) {
      return index;
    }
  }

  return -1;
}

function getSectionText(body, heading) {
  const { searchableBody } = stripFencedCodeBlocks(body);
  const lines = searchableBody.split("\n");
  const startIndex = findHeadingLineIndex(lines, heading);
  if (startIndex === -1) {
    return null;
  }

  let endIndex = lines.length;
  for (let index = startIndex + 1; index < lines.length; index += 1) {
    const line = lines[index];
    if (/^#{1,6}\s+/.test(line.trim())) {
      endIndex = index;
      break;
    }
  }

  return lines.slice(startIndex + 1, endIndex).join("\n");
}

function sectionHasConcreteContent(sectionText) {
  if (sectionText === null) {
    return false;
  }

  // fallow-ignore-next-line complexity
  return sectionText.split("\n").some((line) => {
    const trimmed = line.trim();
    if (!trimmed) {
      return false;
    }
    if (trimmed === "..." || trimmed === "…") {
      return false;
    }
    if (/^(\*|-|\d+\.)\s*(\.\.\.|…)?\s*$/.test(trimmed)) {
      return false;
    }
    return true;
  });
}

function collectReferenceTargets(sectionText) {
  const targets = new Set();
  if (sectionText === null) {
    return targets;
  }

  const markdownLinkPattern = /\[[^\]]*]\(([^)]+)\)/g;
  const backtickPattern = /`([^`\n]+)`/g;

  for (const pattern of [markdownLinkPattern, backtickPattern]) {
    addReferenceTargetsFromPattern(sectionText, pattern, targets);
  }

  return targets;
}

function addReferenceTargetsFromPattern(sectionText, pattern, targets) {
  for (const match of sectionText.matchAll(pattern)) {
    const cleanedTarget = normalizeLocalReferenceTarget(match[1]);
    if (cleanedTarget) {
      targets.add(cleanedTarget);
    }
  }
}

// fallow-ignore-next-line complexity
function normalizeLocalReferenceTarget(rawTargetValue) {
  const rawTarget = rawTargetValue.trim();
  if (!rawTarget || isExternalReferenceTarget(rawTarget)) {
    return null;
  }

  const cleanedTarget = rawTarget.split("#", 1)[0].split("?", 1)[0].trim();
  if (!cleanedTarget || /<[^>]+>/.test(cleanedTarget)) {
    return null;
  }

  return isLocalReferencePath(cleanedTarget) ? cleanedTarget : null;
}

function isExternalReferenceTarget(rawTarget) {
  return (
    rawTarget.startsWith("http://") ||
    rawTarget.startsWith("https://") ||
    rawTarget.startsWith("mailto:") ||
    rawTarget.startsWith("#")
  );
}

function isLocalReferencePath(cleanedTarget) {
  return (
    cleanedTarget.startsWith("./") ||
    cleanedTarget.startsWith("../") ||
    (cleanedTarget.includes("/") && /\.[A-Za-z0-9]+$/.test(cleanedTarget))
  );
}

async function pathExists(targetPath) {
  try {
    await access(targetPath, fsConstants.F_OK);
    return true;
  } catch {
    return false;
  }
}

// fallow-ignore-next-line complexity
async function listSkillFiles() {
  const entries = await readdir(SKILLS_ROOT, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    if (!entry.isDirectory() || entry.name.startsWith(".")) {
      continue;
    }

    const skillPath = path.join(SKILLS_ROOT, entry.name, "SKILL.md");
    if (await pathExists(skillPath)) {
      files.push(skillPath);
    }
  }

  return files.sort();
}

async function resolveSkillFiles(args) {
  if (args.length === 0) {
    return listSkillFiles();
  }

  return args.map((filePath) => path.resolve(REPO_ROOT, filePath));
}

async function listSupportFilesInDir(dir) {
  const files = [];
  const entries = await readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith(".")) {
      continue;
    }
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      const subFiles = await listSupportFilesInDir(fullPath);
      files.push(...subFiles);
    } else {
      files.push(fullPath);
    }
  }
  return files;
}

async function validateOrphanedSupportFiles(filePath, body, errors) {
  const skillDir = path.dirname(filePath);
  const allFiles = await listSupportFilesInDir(skillDir);
  const supportFiles = allFiles.filter(
    (f) =>
      path.basename(f) !== "SKILL.md" &&
      path.basename(f) !== "PROVENANCE.md" &&
      path.basename(f) !== "README.md" &&
      !path.relative(skillDir, f).startsWith("agents" + path.sep) &&
      !path.relative(skillDir, f).startsWith("agents/") &&
      !path.relative(skillDir, f).startsWith("evals" + path.sep) &&
      !path.relative(skillDir, f).startsWith("evals/") &&
      !path.relative(skillDir, f).startsWith("assets" + path.sep) &&
      !path.relative(skillDir, f).startsWith("assets/") &&
      !path.relative(skillDir, f).startsWith(path.join("scripts", "tests") + path.sep) &&
      !path.relative(skillDir, f).startsWith("scripts/tests/"),
  );

  if (supportFiles.length === 0) {
    return;
  }

  const allRefs = collectReferenceTargets(body);
  const resolvedRefs = new Set(
    [...allRefs].map((ref) => path.resolve(skillDir, ref)),
  );

  for (const supportFile of supportFiles) {
    if (!resolvedRefs.has(supportFile)) {
      const relPath = path
        .relative(skillDir, supportFile)
        .replace(/\\/g, "/");
      errors.push(
        `orphaned support file not referenced in SKILL.md: ${relPath}`,
      );
    }
  }
}

async function validateSkillContent(filePath, frontmatter, body) {
  const errors = [];
  const skillDir = path.basename(path.dirname(filePath));

  validateSkillName(frontmatter, skillDir, errors);
  validateSkillDescription(frontmatter, errors);
  validateTopLevelFrontmatterKeys(frontmatter, errors);
  validateLicense(frontmatter, errors);
  validateSkillMetadata(frontmatter.metadata, errors);

  const { searchableBody, errors: fenceErrors } = stripFencedCodeBlocks(body);
  errors.push(...fenceErrors);
  validateRequiredHeadings(searchableBody, frontmatter.metadata, errors);
  const examplesSection = getSectionText(body, "## Examples");
  if (examplesSection !== null && !sectionHasConcreteContent(examplesSection)) {
    errors.push("examples section is empty or placeholder-only");
  }

  const referenceSection = getSectionText(body, "## Reference files");
  if (referenceSection !== null && !sectionHasConcreteContent(referenceSection)) {
    errors.push("reference files section is empty or placeholder-only");
  }

  if (referenceSection !== null) {
    await validateReferenceTargets(filePath, referenceSection, errors);
  }
  await validateOrphanedSupportFiles(filePath, body, errors);

  return errors;
}

function validateSkillName(frontmatter, skillDir, errors) {
  if (!frontmatter.name) {
    errors.push("missing frontmatter key name");
    return;
  }

  if (frontmatter.name !== skillDir) {
    errors.push(
      `frontmatter name ${frontmatter.name} does not match directory ${skillDir}`,
    );
  }
}

// fallow-ignore-next-line complexity
function validateSkillDescription(frontmatter, errors) {
  if (!frontmatter.description || !String(frontmatter.description).trim()) {
    errors.push("missing frontmatter key description");
    return;
  }

  const desc = String(frontmatter.description).trim();
  if (desc.length < 20) {
    errors.push("description is too short; provide a meaningful description");
  }

  if (frontmatter.metadata?.maturity === "draft") {
    validateDraftDescriptionTriggerPhrase(desc, errors);
  }
}

function validateDraftDescriptionTriggerPhrase(desc, errors) {
  const descLower = desc.toLowerCase();
  const hasTriggerPhrase =
    descLower.includes("when ") ||
    descLower.includes("use this") ||
    descLower.includes("use when");

  if (!hasTriggerPhrase) {
    errors.push(
      'description does not include a trigger phrase ("when", "use this", or "use when"); describe when an agent should activate this skill',
    );
  }
}

function validateTopLevelFrontmatterKeys(frontmatter, errors) {
  for (const key of Object.keys(frontmatter)) {
    if (!ALLOWED_TOP_LEVEL_KEYS.has(key)) {
      errors.push(
        `forbidden top-level frontmatter key: ${key}; allowed keys are name, description, license, compatibility, metadata — see skills/skill-authoring/references/metadata-contract.md`,
      );
    }
  }
}

function validateLicense(frontmatter, errors) {
  if (frontmatter.license !== "GNU GPL v3") {
    errors.push("license must be GNU GPL v3 for every catalog skill");
  }
}

function validateSkillMetadata(metadata, errors) {
  if (metadata === undefined) {
    return;
  }
  if (
    metadata === null ||
    typeof metadata !== "object" ||
    Array.isArray(metadata) ||
    Object.values(metadata).some((value) => typeof value !== "string")
  ) {
    errors.push("metadata must be a string-to-string map");
    return;
  }

  validateForbiddenMetadataKeys(metadata, errors);
  validateMetadataKind(metadata, errors);
  validateDraftMetadataKindRequirement(metadata, errors);
}

function validateForbiddenMetadataKeys(metadata, errors) {
  for (const key of Object.keys(metadata)) {
    if (!FORBIDDEN_METADATA_KEYS.has(key)) {
      continue;
    }
    errors.push(
      `forbidden provenance key metadata.${key}; remove upstream attribution fields from frontmatter — see skills/skill-authoring/references/metadata-contract.md`,
    );
  }
}

function validateMetadataKind(metadata, errors) {
  if (!("kind" in metadata) || VALID_KINDS.has(metadata.kind)) {
    return;
  }

  errors.push(
    `invalid metadata.kind ${metadata.kind || "<missing>"}; expected one of task, reference`,
  );
}

function validateDraftMetadataKindRequirement(metadata, errors) {
  if (metadata.maturity !== "draft" || "kind" in metadata) {
    return;
  }

  errors.push(
    'metadata.kind is required for draft skills; set to "task" or "reference" — see skills/skill-authoring/references/metadata-contract.md',
  );
}

function validateRequiredHeadings(searchableBody, metadata, errors) {
  const lines = searchableBody.split("\n");
  validateHeadingOrder(lines, CANONICAL_HEADINGS, errors);
}

function validateHeadingOrder(lines, requiredHeadings, errors) {
  let previousIndex = -1;
  for (const heading of requiredHeadings) {
    const index = findHeadingLineIndex(lines, heading);
    if (index === -1) {
      continue;
    }
    if (index < previousIndex) {
      errors.push(`heading out of order ${heading}`);
      continue;
    }
    previousIndex = index;
  }
}

async function validateReferenceTargets(filePath, referenceSection, errors) {
  const referenceTargets = collectReferenceTargets(referenceSection);
  for (const rawTarget of referenceTargets) {
    const targetPath = path.resolve(path.dirname(filePath), rawTarget);
    const repoRelativePath = path.resolve(REPO_ROOT, rawTarget);
    if (!(await pathExists(targetPath)) && !(await pathExists(repoRelativePath))) {
      errors.push(`missing referenced file ${rawTarget}`);
    }
  }
}

async function validateFile(filePath) {
  const absolutePath = path.resolve(filePath);
  const text = await readFile(absolutePath, "utf8");
  const { frontmatter, body } = parseFrontmatter(text);
  const errors = await validateSkillContent(absolutePath, frontmatter, body);

  if (errors.length > 0) {
    return {
      ok: false,
      message: `FAIL ${absolutePath}\n${errors.map((error) => `- ${error}`).join("\n")}`,
    };
  }

  return {
    ok: true,
    message: `OK ${absolutePath}`,
  };
}

// fallow-ignore-next-line complexity
async function collectValidationOutput(files) {
  const messages = [];
  let hasFailure = false;

  for (const filePath of files) {
    try {
      const result = await validateFile(filePath);
      messages.push(result.message);
      if (!result.ok) {
        hasFailure = true;
      }
    } catch (error) {
      hasFailure = true;
      const message = error instanceof Error ? error.message : String(error);
      messages.push(`FAIL ${path.resolve(filePath)}\n- ${message}`);
    }
  }

  return { output: messages.join("\n"), hasFailure };
}

async function main() {
  const files = await resolveSkillFiles(process.argv.slice(2));
  if (files.length === 0) {
    console.error("no SKILL.md files found");
    process.exitCode = 1;
    return;
  }

  const { output, hasFailure } = await collectValidationOutput(files);
  if (hasFailure) {
    console.error(output);
    process.exitCode = 1;
    return;
  }

  console.log(output);
}

await main();
