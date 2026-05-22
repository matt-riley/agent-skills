#!/usr/bin/env node

function usage() {
  return [
    "Usage:",
    "  node skills/ast-grep/scripts/scaffold-ast-grep-command.mjs --mode <search|rewrite> --pattern <pattern> [options]",
    "",
    "Options:",
    "  --mode <search|rewrite>     Required. Command mode.",
    "  --pattern <pattern>         Required. ast-grep pattern.",
    "  --lang <language>           Optional. Recommended for both modes.",
    "  --path <path>               Optional. Defaults to .",
    "  --glob <glob>               Optional. Include glob filter.",
    "  --rewrite <rewrite>         Required for --mode rewrite unless --rule is provided.",
    "  --rule <path>               Optional. Rule file path (uses ast-grep scan --rule).",
    "  --json                      Optional. Query mode output as JSON.",
    "",
    "Examples:",
    "  node ... --mode search --pattern 'console.log($X)' --lang ts --path src --glob '**/*.ts'",
    "  node ... --mode rewrite --pattern 'oldFn($A)' --rewrite 'newFn($A)' --lang ts --path src --glob '**/*.ts'",
    "  node ... --mode rewrite --pattern 'oldFn($A)' --rule rules/replace-old-fn.yml --path src",
  ].join("\n");
}

// fallow-ignore-next-line complexity
function parseArgs(argv) {
  const parsed = {
    json: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--json") {
      parsed.json = true;
      continue;
    }
    if (!arg.startsWith("--")) {
      throw new Error(`Unexpected argument: ${arg}`);
    }
    const key = arg.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    parsed[key] = next;
    index += 1;
  }

  return parsed;
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, "'\"'\"'")}'`;
}

function normalizeMode(rawMode) {
  return rawMode === "query" ? "search" : rawMode;
}

function validateRequiredOptions(mode, pattern, rewrite, rule) {
  assertValidMode(mode);
  assertPattern(pattern);
  assertRewriteInputs(mode, rewrite, rule);
}

function assertValidMode(mode) {
  if (mode === "search" || mode === "rewrite") {
    return;
  }

  throw new Error("`--mode` must be `search` or `rewrite`.");
}

function assertPattern(pattern) {
  if (pattern) {
    return;
  }

  throw new Error("`--pattern` is required.");
}

function assertRewriteInputs(mode, rewrite, rule) {
  if (mode !== "rewrite") {
    return;
  }
  if (rewrite || rule) {
    return;
  }

  throw new Error("Rewrite mode requires `--rewrite` or `--rule`.");
}

function buildRuleCommand(rule, targetPath) {
  return ["ast-grep", "scan", "--rule", shellQuote(rule), shellQuote(targetPath)].join(
    " ",
  );
}

// fallow-ignore-next-line complexity
function buildPatternCommand(options) {
  const { mode, pattern, rewrite, lang, glob, json, path: targetPath } = options;
  const parts = ["ast-grep", "--pattern", shellQuote(pattern)];

  if (mode === "rewrite") {
    parts.push("--rewrite", shellQuote(rewrite));
  }
  if (lang) {
    parts.push("--lang", shellQuote(lang));
  }
  if (glob) {
    parts.push("--glob", shellQuote(glob));
  }
  if (mode === "search" && json) {
    parts.push("--json");
  }
  parts.push(shellQuote(targetPath));
  return parts.join(" ");
}

function buildCommand(options) {
  const mode = normalizeMode(options.mode);
  const pattern = options.pattern;
  const targetPath = options.path || ".";
  const rewrite = options.rewrite;
  const rule = options.rule;

  validateRequiredOptions(mode, pattern, rewrite, rule);
  if (mode === "rewrite" && rule) {
    return buildRuleCommand(rule, targetPath);
  }

  return buildPatternCommand({
    mode,
    pattern,
    rewrite,
    lang: options.lang,
    glob: options.glob,
    json: options.json,
    path: targetPath,
  });
}

function main() {
  const argv = process.argv.slice(2);
  if (argv.length === 0 || argv.includes("--help")) {
    console.log(usage());
    return;
  }

  const options = parseArgs(argv);
  const command = buildCommand(options);
  console.log(command);
}

try {
  main();
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`Error: ${message}`);
  console.error("");
  console.error(usage());
  process.exitCode = 1;
}
