# Instruction Examples: Good vs. Bad

This document shows real examples of instruction lines that pass or fail the Discoverability Filter. Each pair demonstrates why one instruction earns a place in the file and why the other should be deleted.

---

## Example 1: TypeScript Type Discipline

### ❌ BAD

**"Always use TypeScript. The project uses TypeScript 5.x. Avoid using `any` type."**

**Why it fails:**
- "Always use TypeScript" — discoverable from the file extension and project structure
- "Project uses TypeScript 5.x" — discoverable from package.json and tsconfig.json
- "Avoid `any`" — discoverable from `"noImplicitAny": true` in tsconfig.json

**Passes Discoverability Filter?** No. All three parts are visible in the repository.

---

### ✅ GOOD

**"Avoid `any` in source files; use `unknown` at module boundaries and narrow with type guards. The tsconfig enforces `noImplicitAny`, so use it as feedback to guide where guards belong."**

**Why it works:**
- The pattern "use `unknown` at boundaries and narrow with guards" is a learned convention, not enforced by tooling alone
- It explains *how* to satisfy noImplicitAny, not just that the rule exists
- An agent reading the tsconfig will see the rule but might not know the idiomatic pattern to satisfy it
- It's non-obvious that the pattern involves `unknown` specifically

**Passes Discoverability Filter?** Yes. It adds actionable guidance that the code and config do not spell out.

---

## Example 2: Terraform Backend State

### ❌ BAD

**"The Terraform backend is configured in backend.hcl. Use the S3 backend. State is stored in an S3 bucket."**

**Why it fails:**
- "Backend is configured in backend.hcl" — discoverable from the file system
- "Uses S3 backend" — visible by reading backend.hcl or terraform/main.tf
- "State is stored in S3 bucket" — obvious from the S3 backend configuration

**Passes Discoverability Filter?** No. An agent can read backend.hcl and see all of this.

---

### ✅ GOOD

**"When bumping Terraform to 1.6+, migrate ALL S3 backend `assume_role` config from flat attributes (`role_arn`, `session_name`) to a nested `assume_role = { role_arn, tags }` object. Terraform 1.6 removed the flat form; missing this causes `unexpected attribute` errors at plan time. This applies to backend.hcl AND `data \"terraform_remote_state\"` blocks."**

**Why it works:**
- Non-discoverable: The Terraform 1.6 migration requirement is not mentioned anywhere in the code or config
- Operationally critical: It directly causes plan failures; an agent will hit this error
- Actionable: It specifies exactly what to migrate and where (backend.hcl and data blocks)
- Prevents a class of mistakes specific to this repository's Terraform version

**Passes Discoverability Filter?** Yes. This is institutional knowledge that an agent cannot find by reading the repo alone.

---

## Example 3: Go Error Handling

### ❌ BAD

**"Write error handling code. Return errors when something goes wrong. Handle error cases in tests."**

**Why it fails:**
- Generic best-practice advice, not specific to this repository
- Agents already know to handle errors; this does not guide them on *how* to do it in this codebase
- Not actionable

**Passes Discoverability Filter?** No. This is boilerplate motivational language.

---

### ✅ GOOD

**"Go handlers should return `(statusCode int, body interface{})`. Use the shared `errorResponse()` helper to wrap errors and set status codes. See handlers.go for examples. New handlers that do not use errorResponse() will fail the code review."**

**Why it works:**
- Non-discoverable: The return signature pattern and the errorResponse() helper are visible in code, but a new agent might not immediately see them
- Specific: It names the actual helper and points to actual file examples
- Actionable: An agent knows to use errorResponse() and where to find an example
- Enforceable: It tells agents what the code review will check

**Passes Discoverability Filter?** Yes. While the pattern is discoverable by reading handlers, this saves an agent from writing incorrect handlers before the code review cycle.

---

## Example 4: Directory Structure

### ❌ BAD

**"The repository has the following directories: src/ contains source code, test/ contains tests, docs/ contains documentation, scripts/ contains utility scripts."**

**Why it fails:**
- Each directory name documents its purpose
- An agent can see this by running `ls -la` or reading the tree output
- This is low-value duplication

**Passes Discoverability Filter?** No. Discoverable from the filesystem.

---

### ✅ GOOD

**"Source files in src/handlers/ are auto-discovered by the test runner, but shared utilities in src/lib/ are not. Always import shared utilities explicitly in tests; do not rely on the test runner to discover them."**

**Why it works:**
- Non-discoverable: The auto-discovery behavior is not obvious from directory names
- Operationally important: Agents might assume all src/ files are discovered
- Actionable: It tells agents how to import utilities correctly

**Passes Discoverability Filter?** Yes. This is a non-obvious convention.

---

## Example 5: Git Signing

### ❌ BAD

**"Use Git to manage version control. Make commits frequently. Write descriptive commit messages."**

**Why it fails:**
- Boilerplate advice; not specific to this repository
- Already enforced by code review and CI checks

**Passes Discoverability Filter?** No. Generic best practice.

---

### ✅ GOOD

**"All commits must be signed via 1Password SSH signing (`op-ssh-sign`). Unsigned or GPG-signed commits will be rejected by the repository. If signing fails, validate the 1Password setup and approve the authorization in the app. See CONTRIBUTING.md for setup."**

**Why it works:**
- Non-discoverable: This security requirement is not mentioned in README, config, or code comments
- Operationally critical: It directly blocks pushes; an agent must know about this
- Actionable: It explains the signing method and what to do if it fails
- Prevents frustration and blocked workflows

**Passes Discoverability Filter?** Yes. This is institutional security policy that must be documented.

---

## Example 6: Package Versions

### ❌ BAD

**"The project uses Node.js 20. Use npm for package management. Install dependencies with npm install."**

**Why it fails:**
- "Node.js 20" — visible in .nvmrc, package.json, or volta config
- "Use npm" — visible in package.json and npm-specific files (package-lock.json)
- "npm install" — standard command that agents already know

**Passes Discoverability Filter?** No. All discoverable.

---

### ✅ GOOD

**"This project uses Volta to pin Node and npm versions. Ensure Volta is installed before running npm commands, or use `volta install node@20` to switch versions. CI enforces version pinning; local version mismatches will cause test failures that do not match the CI results."**

**Why it works:**
- Non-discoverable: The Volta requirement is not obvious from package.json alone; an agent might use a different Node version
- Operationally important: Version mismatches cause real test failures; this prevents wasted debugging
- Actionable: It tells agents how to install Volta and ensure the right version

**Passes Discoverability Filter?** Yes. This explains a non-obvious operational requirement.

---

## Example 7: Learned Rule from Sessions

### ❌ BAD

**"Always verify that your changes work before committing."**

**Why it fails:**
- Generic advice; not specific to this repository
- Does not prevent any concrete mistake

**Passes Discoverability Filter?** No. Boilerplate.

---

### ✅ GOOD

**"When validating TypeScript projects with `tsc --build`, use the exact pinned TypeScript version from node_modules, not a global tsc. Global tsc may be an older version and mask real errors. If you see type errors locally but not in CI, check your tsc version with `npx tsc --version` and compare to package.json."**

**Why it works:**
- Non-discoverable: An agent might not realize that global tsc and local tsc differ
- Based on real sessions: This rule was learned from prior sessions where agents hit this mistake
- Actionable: It includes the exact diagnostic command and explanation
- Prevents a specific class of frustrating debugging cycles

**Passes Discoverability Filter?** Yes. This is a learned operational lesson.

---

## Summary: Signals

| Pattern | Include? | Reason |
|---------|----------|--------|
| Generic best practice | ❌ No | Already implicit; add noise |
| Directory names and purposes | ❌ No | Discoverable from filesystem |
| Tech stack summary | ❌ No | Discoverable from config files |
| Specific tool version requirement | ✅ Yes | Non-obvious; operationally critical |
| Non-obvious convention or pattern | ✅ Yes | Not enforced by tooling alone |
| Security or signing requirement | ✅ Yes | Operational gate; non-discoverable |
| Learned lesson from repeated mistakes | ✅ Yes | Prevents class of known errors |
| How to use a shared helper or library | ✅ Yes | Guides agents to idiomatic usage |
| Tool-enforced rule | ❌ No | Trust the tooling; do not duplicate |

---

## Guideline

When in doubt, ask:

1. **Can an agent find this by reading the code, config, and README?** If yes, do not include.
2. **Would an agent make a mistake or waste time without this?** If no, do not include.
3. **Is this specific and actionable?** If no, rewrite or delete.

If all three answer "no" (do not include, would waste time, and is specific), include the instruction.
