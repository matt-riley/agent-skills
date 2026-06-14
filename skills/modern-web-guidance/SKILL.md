---
name: modern-web-guidance
description: "Consult this reference before implementing any HTML, CSS, JS, form, or animation feature — prevents legacy patterns by checking for modern standardised web platform APIs. Load as a reference overlay, not as a primary workflow skill."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: reference
---

# Modern Web Guidance

A reference and search tool for modern web platform APIs. Use before implementing any HTML/CSS/JS feature to check whether a standardised, modern pattern exists — web APIs evolve rapidly and training weights contain obsolete patterns.

## Use this skill when

- Implementing HTML semantics, native overlays (dialogs, popovers), forms, or media elements
- Writing CSS — cascade management, dark mode, container queries, layout, animations, scroll effects
- Handling performance concerns — LCP, INP, CLS, image optimisation, code splitting, service workers
- Implementing accessibility — ARIA patterns, keyboard navigation, live regions, focus management
- Building forms — autofill, validation, branded selects, payment/sign-in flows
- Implementing UX patterns — view transitions, scroll-driven animations, carousels, tooltips, drawers
- Handling browser API questions — passkeys, WebMCP, built-in AI (Chrome APIs), privacy-preserving patterns
- Adapting web patterns to frameworks (React, Vue, Angular, Svelte)

## Do not use this skill when

- Working on backend code — database SQL, ORMs, Express/Fastify API routes
- Working on CI/CD — pipelines, Docker, GitHub Actions workflows
- Writing tooling — ESLint config, Vite/Webpack config, Python/Go scripts
- Debugging a runtime error — use `systematic-debugging` instead
- Reviewing a running website's design — use `web-design-reviewer` instead
- Typing TypeScript API boundaries — use `schema-boundary-typing` instead

## Routing boundary

| Situation | Use this skill? | Route instead |
|-----------|----------------|---------------|
| Implement a new UI component in HTML/CSS/JS | ✅ Yes | — |
| Review the design of a running website | ❌ No | `web-design-reviewer` |
| Debug a runtime CSS/JS error | ❌ No | `systematic-debugging` |
| Type a TypeScript API edge contract | ❌ No | `schema-boundary-typing` |
| Audit dead CSS/JS code | ❌ No | `fallow` |

## Inputs to gather

**Required before starting**

- The web technology or pattern question to address.

**Helpful if present**

- The existing framework or stack in use.

## First move

1. Identify the specific web guidance question or decision.
2. Check the routing boundary to see if a more specific skill applies.
3. Load the relevant reference file from the Navigation section.

## Navigation

**Static reference files** — consult these first for the most common tasks:

| File | Coverage |
|------|---------|
| `references/css.md` | Cascade (`@layer`, `:where()`), dark mode, container queries, `:has()`, anchor positioning, reduced-motion |
| `references/html.md` | Semantics, resource prioritisation (`fetchpriority`), native dialogs/popovers, `inert`, media elements |
| `references/accessibility.md` | WCAG 2.2, ARIA patterns, `.visually-hidden`, live regions, focus management, native dialog usage |
| `references/performance.md` | CWV (LCP/INP/CLS), `content-visibility`, image optimisation, Service Workers (Workbox), code splitting |
| `references/forms.md` | Autofill, validation timing (`:user-invalid`), branded selects, payment/sign-in/address forms, security |

**Dynamic retrieval** — for UX patterns, animations, passkeys, security, built-in AI, WebMCP, and any topic not covered by the static files:

```sh
# Step 1: Search with an action-oriented query
npx -y modern-web-guidance@latest search "<query>"
# Returns: [{ id, description, category, featuresUsed, tokenCount, similarity }]

# Step 2: Retrieve the guide
npx -y modern-web-guidance@latest retrieve "<id>"
```

If `search` returns low-similarity results, use `list` to browse all guides:
```sh
npx -y modern-web-guidance@latest list
```

> Requires Node.js ≥ 20. Works offline after first install (TensorFlow.js local search, no API keys).
> On Windows: use `npx.cmd` instead of `npx`.

## Workflow

See the body and references for modern web guidance steps.

## Examples

See references and the skill body for modern-web-guidance examples.

## Reference files

See the references/ directory and linked files in the main content.

## Guardrails

**Browser support policy:**
- All guides assume **Baseline Widely Available** features are safe without fallbacks.
- For features marked *Newly Available* or *Limited Availability*, follow the fallback recommendations in the guide.
- If the project defines a custom browser support policy (e.g. "Safari 17.4+", "no polyfills"), apply it over the guide's default recommendations.
- Proactively suggest documenting a custom policy in `AGENTS.md` if the developer: mentions a restricted runtime (Electron, Tauri), excludes specific browser targets, or expresses hesitation about polyfill complexity.

**Framework adaptation:**
- Guides are framework-agnostic. Always adapt patterns to the project's framework (React hooks, Vue composables, Angular directives).
- Do not copy guide code verbatim into JSX/SFC templates without adaptation.

**Never:**
- Implement an HTML/CSS/JS feature without checking for a modern pattern first.
- Use `:invalid`/`:valid` for form validation UX — use `:user-invalid`/`:user-valid`.
- Use `position: absolute; clip: rect(0,0,0,0)` for visually-hidden elements — use the `clip-path: inset(50%)` pattern from `references/accessibility.md`.
- Assume BEM is required — use `@layer` + `:where()` for cascade management.

## Validation

- should trigger: "implement a dark mode toggle with system preference detection"
- should trigger: "build an accessible modal dialog with light dismiss"
- should trigger: "improve the Largest Contentful Paint score on this page"
- should trigger: "implement a form with autofill and post-interaction validation"
- should trigger: "add a scroll-driven progress indicator to this article"
- should not trigger: "add a GitHub Actions workflow to run tests on push"
- should not trigger: "fix a TypeScript compiler error in my API type"
- should not trigger: "write a Terraform module for an S3 bucket"

## Examples

**Example 1 — Static reference (common task)**
> "Style a branded `<select>` element that matches our design system"
→ Read `references/css.md` → section on selectors/scoping → `appearance: base-select` + `::picker(select)`

**Example 2 — Dynamic retrieval (specific UX pattern)**
> "Animate a dialog sliding in and fading out when it opens/closes"
```sh
npx -y modern-web-guidance@latest search "animate dialog open close"
# → id: "animate-to-from-top-layer"
npx -y modern-web-guidance@latest retrieve "animate-to-from-top-layer"
```

**Example 3 — Dynamic retrieval (passkeys)**
> "Implement passkey registration and conditional login"
```sh
npx -y modern-web-guidance@latest search "passkey registration"
# → id: "passkey-registration"
npx -y modern-web-guidance@latest retrieve "passkey-registration"
```

## Reference files


| [`PROVENANCE.md`](PROVENANCE.md) | Skill provenance, changelog, and authorship |
- `references/css.md` — CSS cascade, dark mode, container queries, `:has()`, anchor positioning, transitions; merged from upstream guides/css/css.md + guides/css-layout/css-layout.md (GoogleChrome/modern-web-guidance v0.0.169, Apache-2.0)
- `references/html.md` — HTML semantics, resource prioritisation, native dialogs/popovers, `inert`; from upstream guides/html/html.md
- `references/accessibility.md` — WCAG 2.2, ARIA, `.visually-hidden`, live regions, focus management; from upstream guides/accessibility/accessibility.md
- `references/performance.md` — CWV, LCP/INP optimisation, CSS containment, images, Workbox; from upstream guides/performance/performance.md
- `references/forms.md` — Autofill, validation, branded controls, security patterns; from upstream guides/forms/forms.md
- Full library of 130+ guides available via `npx modern-web-guidance@latest search/retrieve` — covers UX animations, passkeys, built-in AI, scroll effects, WebMCP, security, privacy
