# Discoverability Filter: Deep Dive

## Why Discoverability Matters

Instruction files succeed when they capture non-obvious operational knowledge that agents *cannot* discover by reading the repository. The moment instruction files start duplicating what's already visible in code, config, or project documentation, they become maintenance burden, stale traps, and noise.

The Discoverability Filter is a simple heuristic: **Before adding a line, ask whether an agent can find this information by reading the repository itself.** If the answer is yes, do not include it. If no, and it materially affects task success, include it.

This principle keeps instruction files focused, low-maintenance, and high-signal.

## What Does "Discoverable from the Repository" Mean?

An agent reading the repository means:
- Skimming the README and main docs
- Reading relevant config files (tsconfig.json, package.json, .github/workflows/, terraform modules, Go mod files, etc.)
- Reading the source code and comments in the relevant area
- Looking at scripts and tooling configuration
- Scanning the directory tree and file organization
- Searching for similar patterns in existing code

It does NOT mean:
- Intuiting undocumented conventions
- Guessing at deployment or signing procedures
- Reverse-engineering institutional knowledge
- Discovering security policies or operational gates
- Inferring project history or learning from past mistakes

## Examples of Discoverable vs. Non-Discoverable

### Example: Tech Stack

**"The repository uses TypeScript with Node.js 20.x and React 18."**

**Discoverable?** Yes — visible in package.json, README, and .nvmrc or volta config.

**Include in instructions?** No. Delete it.

---

### Example: Type Checking

**"Avoid `any` in source code; use `unknown` at boundaries and narrow with type guards."**

**Discoverable?** Partially — `"noImplicitAny": true` is visible in tsconfig.json, but the *pattern* of using `unknown` at boundaries is a convention, not a rule that a tool enforces.

**Include in instructions?** Yes, because the pattern is learned behavior, not enforced by the tooling alone.

---

### Example: Signing Requirement

**"All commits must be signed via 1Password SSH signing. Unsigned commits will be rejected."**

**Discoverable?** No — this is a security gate that is not mentioned in the Git config, the README, or any inline documentation. It's an institutional policy.

**Include in instructions?** Yes, because it materially affects whether a commit will be accepted, and an agent cannot find this by reading the repository.

---

### Example: Directory Structure

**"The repository has src/, tests/, docs/, and scripts/. Use src/ for source code, tests/ for test files."**

**Discoverable?** Yes — directory names are self-documenting and visible in the tree.

**Include in instructions?** No. Delete it.

---

### Example: Error Handling Pattern

**"Go handlers should return (statusCode int, body interface{}). Use the shared errorResponse() helper to wrap errors."**

**Discoverable?** Partially — looking at a few handler implementations will show the pattern, and the errorResponse() helper is defined in the codebase.

**Include in instructions?** It depends on adoption. If every handler in the repository already follows this pattern, agents will see it quickly. If it's a new or inconsistently applied pattern, include it to guide agents to the right approach.

---

### Example: Learned Rule

**"When bumping Terraform to 1.6+, migrate all S3 backend `assume_role` config from flat attributes to a nested object. Terraform 1.6 removed the flat top-level form."**

**Discoverable?** No — an agent would only learn this by hitting the compiler error `unexpected attribute "role_arn"` or by reading the Terraform 1.6 release notes (not in the repository).

**Include in instructions?** Yes, because it prevents a painful mistake specific to this repository's Terraform version and usage.

---

## The Three-Part Test

For each candidate instruction, ask:

### 1. Is it non-discoverable?

Look for these signals that something is non-discoverable:
- **No mention in code or config:** The pattern is not visible anywhere in the repository.
- **Institutional knowledge:** The rule is learned behavior or operational policy, not a code pattern.
- **Edge case or version-specific:** The guidance is specific to a Terraform version, Node version, or tool combination that is not obvious.
- **Security or operational gate:** Signing requirements, deployment procedures, access controls.
- **Learned lesson from a mistake:** A lesson captured in prior sessions or corrections that an agent would otherwise repeat.

### 2. Is it accurate?

- **File paths:** Do they actually exist in the repository right now?
- **Commands:** Will they work as written?
- **Tool versions or behavior:** Has the behavior changed in a recent update?
- **Learned rules:** Have they been validated, or are they still speculation?

If you are not sure, test it. If you find it is inaccurate, fix it or delete it.

### 3. Does it materially reduce mistakes?

- **High impact:** Following this instruction prevents a large class of mistakes or unlocks a significant capability.
- **Medium impact:** It prevents occasional mistakes or improves workflow efficiency.
- **Low impact:** It's a nice-to-know but does not meaningfully change outcomes.

Delete low-impact lines. Keep high and medium impact.

## Common Pitfalls

### Pitfall 1: Documenting the Directory Tree

"The src/ directory contains application code. The test/ directory contains test files. The docs/ directory contains documentation."

**Why it fails:** The directory names are self-documenting. An agent does not need to be told what src/ and tests/ are.

**What to do instead:** Delete it. If the structure is complex or non-obvious, add a note to the README or create a CONTRIBUTING guide, but do not clog instruction files with this.

### Pitfall 2: Repeating What Tooling Enforces

"Always use oxfmt for formatting and oxlint for linting. Commits that do not pass linting will fail CI."

**Why it fails (partly):** The fact that oxfmt and oxlint are used is discoverable from scripts and CI config. The fact that CI will fail is also discoverable.

**What to include instead:** "Prefer oxfmt and oxlint over prettier or eslint in this repo because the project values Rust-native tooling." This explains the *why*, not the *what*, and it is non-obvious.

### Pitfall 3: Adding Tutorials

"To add a new API endpoint, create a file in routes/, define a handler, export it, and import it in the router."

**Why it fails:** This is a tutorial. An agent can learn this by reading a few handler files.

**What to do instead:** If the pattern is not obvious or varies from common conventions, say so: "Routes are defined individually in routes/ and explicitly imported into index.ts (not auto-discovered), so remember to add the import after creating a new handler."

### Pitfall 4: Generic Best Practices

"Write clean, maintainable code. Add comments where logic is complex. Test thoroughly."

**Why it fails:** This is a platitude. Tooling and code review already enforce this.

**What to do instead:** Replace it with specific, actionable guidance: "Complex recursive algorithms need comments explaining the base case and recurrence relation; see sorting.go for an example."

### Pitfall 5: Motivational Statements

"Code quality is important, so always review your changes before committing."

**Why it fails:** This is motivational, not actionable. It does not tell an agent what to do or how this repository differs from others.

**What to do instead:** "Before committing, run `npm run test && npm run lint` to catch issues that CI would catch later."

## When to Err on the Side of Inclusion

There are a few cases where you should include an instruction even if it might be discoverable, because the cost of agents missing it is very high:

1. **Security gates or signing requirements:** If the repository requires commit signing, specific secret handling, or deployment approvals, include it even if it might be inferred from CI config.

2. **Learned lessons from past mistakes:** If you have several sessions showing agents hitting the same mistake, include a rule to prevent it, even if the mistake is theoretically avoidable by careful reading.

3. **Version-specific behavior:** If the repository is pinned to a specific tool version and that version has a non-obvious behavior or requirement, include it.

4. **Operational procedures:** If the repository has a specific deployment flow, testing procedure, or approval gate, include it. These are institutional knowledge that are not visible in the code.

5. **Tool or library choices with strong opinions:** If the repository has a non-obvious reason for choosing one tool over a common alternative (e.g., "We use Bun instead of Node because our infrastructure requires it"), include it so agents do not waste time proposing the obvious alternative.

## Evaluation Checklist

Before finalizing an instruction file, go through each line and answer:

- [ ] Is this non-discoverable from the repository itself?
- [ ] Is this accurate as of today?
- [ ] Does this materially reduce mistakes or improve outcomes?
- [ ] Is this actionable (specific and concrete)?
- [ ] Does this avoid duplicating tooling, config, or automated checks?

If any answer is "no," delete the line or rewrite it until all answers are "yes."
