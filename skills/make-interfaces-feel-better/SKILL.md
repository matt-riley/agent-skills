---
name: make-interfaces-feel-better
description: Polish existing interfaces when the UI feels off through better radius, shadows, typography, motion, and micro-interactions.
metadata:
  version: 1.0.0 # x-release-please-version
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

## Guardrails

- **Must** preserve the existing visual system unless the user explicitly asks to change it.
- **Must** prefer existing tokens, utilities, and motion libraries over introducing new styling patterns or dependencies.
- **Must not** add a motion dependency just to implement icon or state transitions.
- **Must not** use `transition: all` or `will-change: all`.
- **Must not** replace layout-separation borders such as dividers with shadows meant for depth.
- **Should** use exact, concrete values where this skill specifies them, especially for contextual icon animation and press-scale behavior.
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

## Core principles

### 1. Concentric border radius

Outer radius = inner radius + padding. Mismatched radii on nested elements is the most common thing that makes interfaces feel off.

### 2. Optical over geometric alignment

When geometric centering looks off, align optically. Buttons with icons, play triangles, and asymmetric icons often need manual adjustment.

### 3. Shadows over borders

For depth on buttons, cards, and containers, prefer layered transparent `box-shadow` values over solid borders. Keep actual borders for dividers, separators, and accessibility outlines.

### 4. Interruptible animations

Use CSS transitions for interactive state changes so motion can reverse or retarget mid-animation. Reserve keyframes for staged sequences that run once.

### 5. Split and stagger enter animations

Do not animate a single large container. Break content into semantic chunks and stagger each with roughly `100ms` delay.

### 6. Subtle exit animations

Use a small fixed `translateY` instead of the full container height. Exits should be softer than enters.

### 7. Contextual icon animations

Animate icons with `opacity`, `scale`, and `blur` instead of toggling visibility. Use exactly these values:

- `scale`: `0.25` to `1`
- `opacity`: `0` to `1`
- `blur`: `4px` to `0px`

If the project already uses `motion` or `framer-motion`, use `transition: { type: "spring", duration: 0.3, bounce: 0 }`. Otherwise keep both icons in the DOM and cross-fade them with CSS using `cubic-bezier(0.2, 0, 0, 1)`.

### 8. Font smoothing

Apply `-webkit-font-smoothing: antialiased` to the root layout on macOS for crisper text.

### 9. Tabular numbers

Use `font-variant-numeric: tabular-nums` for dynamically updating numbers to prevent layout shift.

### 10. Text wrapping

Use `text-wrap: balance` on headings. Use `text-wrap: pretty` for short-to-medium body text to reduce orphans.

### 11. Image outlines

Add a subtle `1px` outline to images for consistent depth. Use pure black in light mode (`rgba(0, 0, 0, 0.1)`) and pure white in dark mode (`rgba(255, 255, 255, 0.1)`), never tinted neutrals.

### 12. Scale on press

A subtle `scale(0.96)` on press gives buttons tactile feedback. Always use `0.96`; anything below `0.95` feels exaggerated. Add a `static` prop when motion would be distracting.

### 13. Skip animation on page load

Use `initial={false}` on `AnimatePresence` to prevent default-state enter animations on first render. Verify it does not break intentional entrance motion.

### 14. Never use `transition: all`

Always specify exact properties. Tailwind's `transition-transform` covers transform-related properties and is usually the right choice for tap or hover scale.

### 15. Use `will-change` sparingly

Only use `will-change` for compositor-friendly properties such as `transform`, `opacity`, and `filter`, and only when you observe first-frame stutter.

### 16. Minimum hit area

Interactive elements should have at least a `40x40px` hit area and preferably `44x44px` where space allows. Extend with a pseudo-element if the visible control is smaller, and never let hit areas overlap.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Same border radius on parent and child | Calculate `outerRadius = innerRadius + padding` |
| Icons look off-center | Adjust optically with padding or fix SVG directly |
| Hard borders used for depth | Use layered `box-shadow` with transparency |
| Jarring enter/exit motion | Split, stagger, and keep exits subtle |
| Numbers cause layout shift | Apply `tabular-nums` |
| Heavy text on macOS | Apply `antialiased` to the root |
| Animation plays on page load | Add `initial={false}` to `AnimatePresence` where appropriate |
| `transition: all` on elements | Specify exact properties |
| First-frame animation stutter | Add `will-change` only to compositor-friendly properties |
| Tiny hit areas on small controls | Extend with a pseudo-element to at least 40x40px |

## Review output format

Always present changes as a markdown table with **Before** and **After** columns. Include every change made, not just a subset. Group changes by principle using a heading above each table, and keep each row focused on a single diff so the reader can scan quickly.

### Example

#### Concentric border radius

| Before | After |
| --- | --- |
| `rounded-xl` on card + `rounded-xl` on inner button (`p-2`) | `rounded-2xl` on card (`12 + 8`), `rounded-lg` on inner button |
| `border-radius: 16px` on both nested surfaces | Outer `24px`, inner `16px` with `8px` padding |

#### Tabular numbers

| Before | After |
| --- | --- |
| `<span>{count}</span>` on animated counter | `<span className="tabular-nums">{count}</span>` |
| Default numerals on timer | Added `font-variant-numeric: tabular-nums` to root |

#### Scale on press

| Before | After |
| --- | --- |
| `<button className="...">` | Added `active:scale-[0.96] transition-transform` |
| `scale(0.9)` on press | Raised to `scale(0.96)` — anything below `0.95` feels exaggerated |

Rows should cite the specific file and property when it is not obvious from the snippet. If a principle was reviewed but nothing needed to change, omit that table entirely.

## Review checklist

- [ ] Nested rounded elements use concentric border radius.
- [ ] Icons are optically centered, not just geometrically.
- [ ] Shadows replace borders used only for depth.
- [ ] Enter animations are split and staggered.
- [ ] Exit animations are subtle.
- [ ] Dynamic numbers use tabular numbers where needed.
- [ ] Font smoothing is applied at the root when appropriate.
- [ ] Headings use `text-wrap: balance`.
- [ ] Images have subtle neutral outlines.
- [ ] Buttons use `scale(0.96)` on press where appropriate.
- [ ] `AnimatePresence` uses `initial={false}` for default-state elements where appropriate.
- [ ] No `transition: all`; only specific properties transition.
- [ ] `will-change` is limited to compositor-friendly properties.
- [ ] Interactive elements have at least a 40x40px hit area.

## Validation

- Confirm the task is really about interface feel and not a broader product-design or accessibility problem.
- Read the relevant reference file before making or recommending a change in that category.
- If a recommended motion pattern depends on a library, confirm the library already exists before using it.

## Reference files

- [references/typography.md](references/typography.md) — text wrapping, font smoothing, tabular numbers
- [references/surfaces.md](references/surfaces.md) — border radius, optical alignment, shadows, image outlines, hit areas
- [references/animations.md](references/animations.md) — interruptible animations, enter/exit transitions, icon animations, scale on press
- [references/performance.md](references/performance.md) — transition specificity and `will-change` usage
