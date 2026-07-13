---
name: make-interfaces-feel-better
description: "Polish existing interfaces when the UI feels off through better radius, shadows, typography, motion, and micro-interactions."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
  maturity: stable
  kind: task
---

# Make interfaces feel better

## Use this skill when

- The user wants an existing interface, component, or interaction to feel more polished, refined, or intentional.
- The work is about UI detail quality: border radius, optical alignment, shadows, outlines, typography, hit areas, hover states, enter/exit motion, or press feedback.
- A frontend review needs concrete polish fixes rather than high-level product or information-architecture advice.
- The user says things like "make it feel better", "this feels off", "polish this", or "tighten the interactions".

## Do not use this skill when

- The main task is net-new product design, flows, IA, or broad UX strategy rather than detail polish on an existing interface.
- The main task is accessibility compliance, semantics, or keyboard/screen-reader behavior; handle those directly or use a more appropriate specialist.
- The main task is generic frontend implementation with no visual or interaction quality concern.
- There is no existing UI context, screenshot, component, or code to evaluate.

## Inputs to gather

**Required before editing**

- The specific surface to polish: page, component, modal, menu, card, button, or animation.
- Whether the task is review-only or should include implementation changes.
- The current UI stack and styling approach (CSS, Tailwind, Motion/Framer Motion, component library).

**Helpful if present**

- Screenshots, recordings, or a description of what feels off.
- Relevant design-system primitives, tokens, or shared component constraints.
- Whether the component has light and dark mode variants that must stay aligned.

**Only investigate if encountered**

- Whether `package.json` already includes `motion` or `framer-motion` before recommending motion-based patterns.
- Whether the root layout already handles font smoothing, text wrapping, or shared transition utilities.

## First move

1. Inspect the current UI and nearby shared primitives before proposing polish changes.
2. Separate structural issues from detail issues so this skill stays focused on feel, not broad redesign.
3. If reviewing, group findings by principle and present concrete before/after diffs instead of abstract taste notes.

## Outputs

- Component-level polish changes or review findings grouped by principle, with exact before/after deltas instead of generic taste comments.
- Concrete UI refinements to typography, surfaces, spacing, shadows, or motion using the existing design tokens, utilities, and libraries.
- Validation that the work stayed focused on interface feel rather than drifting into a broader redesign or new dependency footprint.


## Workflow

See the body and references for UI polish steps.

## Guardrails

- **Must** preserve the existing visual system unless the user explicitly asks to change it.
- **Must** prefer existing tokens, utilities, and motion libraries over introducing new styling patterns or dependencies.
- **Must not** add a motion dependency just to implement icon or state transitions.
- **Must not** use `transition: all` or `will-change: all`.
- **Must not** replace layout-separation borders such as dividers with shadows meant for depth.
- **Should** use exact, concrete values from the reference files, especially for contextual icon animation and press-scale behavior.
- **Should** keep recommendations actionable at the component level rather than drifting into broad design critique.

## Quick reference

| Category | When to use |
| --- | --- |
| [Typography](references/typography.md) | Text wrapping, font smoothing, tabular numbers |
| [Surfaces](references/surfaces.md) | Border radius, optical alignment, shadows, image outlines, hit areas |
| [Animations](references/animations.md) | Interruptible animations, enter/exit transitions, icon animations, scale on press |
| [Performance](references/performance.md) | Transition specificity, `will-change` usage |

## Workflow

1. Identify the smallest visible details making the interface feel off.
2. Map each issue to a principle in the reference files instead of improvising one-off visual tweaks.
3. Prefer the least invasive change that improves polish while preserving the component's existing structure.
4. If presenting a review, group changes by principle and show exact before/after deltas.

## Review output

When reviewing or reporting changes, group findings by principle and use a markdown table with **Before** and **After** columns. Cite the file, selector, component, or property when it is not obvious from the snippet. Omit categories that were reviewed but did not need changes.

## Checklist

- Nested radii are concentric; icons are optically aligned.
- Depth uses shadows intentionally while dividers and accessibility outlines remain borders.
- Motion is interruptible, subtle, and uses existing libraries or CSS transitions.
- Text, numbers, images, and hit areas use the relevant typography and surface guidance.
- No `transition: all`; `will-change` is limited and evidence-backed.

## Validation

- Confirm the task is really about interface feel and not a broader product-design or accessibility problem.
- Read the relevant reference file before making or recommending a change in that category.
- If a recommended motion pattern depends on a library, confirm the library already exists before using it.

## Reference files

- [references/typography.md](references/typography.md) — text wrapping, font smoothing, tabular numbers
- [references/surfaces.md](references/surfaces.md) — border radius, optical alignment, shadows, image outlines, hit areas
- [references/animations.md](references/animations.md) — interruptible animations, enter/exit transitions, icon animations, scale on press
- [references/performance.md](references/performance.md) — transition specificity and `will-change` usage
