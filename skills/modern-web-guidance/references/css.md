# CSS: Modern Architecture and Performance

These guidelines provide a high-density reference for writing maintainable, performant, and standard-compliant CSS.

1. [1. Foundations](#1-foundations)
2. [2. Inheritance and The Cascade](#2-inheritance-and-the-cascade)
3. [3. Selectors and scoping](#3-selectors-and-scoping)
   1. [Prefer CSS selectors over JS for complex element targeting](#prefer-css-selectors-over-js-for-complex-element-targeting)
   2. [Use `:is()` (or `:where()`) instead of CSS rule duplication for fallbacks](#use-is-or-where-instead-of-css-rule-duplication-for-fallbacks)
   3. [Avoid overmatching](#avoid-overmatching)
   4. [Nesting and scoping](#nesting-and-scoping)
4. [4. Interactivity](#4-interactivity)
   1. [Focus management](#focus-management)
   2. [Touch targets](#touch-targets)
5. [5. Design Tokens and Theming](#5-design-tokens-and-theming)
   1. [Dark mode](#dark-mode)
   2. [Forced Colors Mode](#forced-colors-mode)
   3. [Generating tints](#generating-tints)
   4. [Theming browser-generated UI](#theming-browser-generated-ui)
6. [6. Responsive design](#6-responsive-design)
   1. [Responsive Typography](#responsive-typography)
7. [7. Typography](#7-typography)
   1. [Text wrapping](#text-wrapping)
8. [8. Visual effects](#8-visual-effects)
   1. [Depth and texture](#depth-and-texture)
   2. [Shapes](#shapes)
   3. [Gradients and `color-mix()`](#gradients-and-color-mix)
   4. [Patterns](#patterns)
9. [9. Transitions \& animations](#9-transitions--animations)
   1. [Performance](#performance)
   2. [Accessibility](#accessibility)
10. [10. Generated content](#10-generated-content)


## 1. Foundations

Be allergic to knowledge duplication. Prefer variables over repetition, but whenever possible, prefer built-in conventions such as:
- `currentColor` instead of defining a variable and setting `color` to it
- The `inherit` keyword instead of defining a variable on the parent and using it on the same property across parent and child.
- `em` units instead of `font-size: var(--size)`
- `cqw`/`cqh` (or their logical versions — `cqi`/`cqb`) units instead of repeating box model values.
- Code duplication is not knowledge duplication. The goal is robustness and maintainability, not saving characters.
- Prefer **logical properties and values** over physical ones (e.g. `margin-inline-start` instead of `margin-left`) so that styles adapt to different writing modes and orientations. Even if the page author does not plan to localize, external translation tools often display translated text in context.
- Do not use logical properties indiscriminately — ask yourself "would I want this to flip in RTL?" — if the answer is no, use the physical property instead.
- Consider different viewing modes (dark mode, high contrast mode), different viewport sizes, and different input modes (touch, keyboard, pointer).

## 2. Inheritance and The Cascade

**Avoid** introducing BEM naming conventions to manage specificity.
Instead, use modern CSS features such as cascade layers and `:where()` to make cascade behavior predictable and follow author intent.

Use cascade layers (`@layer`) to define explicit priority zones (e.g., `reset`, `base`, `theme`, `components`, `utilities`), and declare their order upfront (e.g. `@layer reset, base, theme, components, utilities;`).
Within each layer, use `:where()` to make selectors only compete based on meaningful signals, not incidental filters (`:not()` edge cases, remote ancestors, etc.) or for one-off easily overridable defaults.

Use keywords like `inherit`, `initial`, `unset`, or `revert` instead of explicit values to improve maintainability and better express intent.
Examples:
- When specifying a transition on a child that should match the parent's `transition-*` properties, instead of repeating the transition properties on the child, use `transition: inherit` (reduce duplication, improve maintainability)
- Use `initial` to reset a property to its initial value instead of specifying the value explicitly (clearer expression of intent)

## 3. Selectors and scoping

Modern browser-native selectors reduce the need for preprocessors and complex state-tracking in JS.

### Prefer CSS selectors over JS for complex element targeting

- **DO** use `:has()` to style parents based on child state instead of managing classes in JS (e.g. `label:has(:checked)` instead of a manual `label.has-checked` class) For more information, see the guides at `child-state-based-styling` (via `npx -y modern-web-guidance@latest retrieve "child-state-based-styling"`) and `content-based-styling` (via `npx -y modern-web-guidance@latest retrieve "content-based-styling"`).
- **DO NOT** nest `:has()` or use pseudo-elements inside it (browser API limitation)
- Use `:nth-child(<An+B> of <selector>)` when you need to style every n-th element of a certain type. E.g. `details:nth-child(1 of [open])` will style the first open `<details>` element it finds, whereas `details[open]:first-child` would style only the first child if and only if it was open.

### Use `:is()` (or `:where()`) instead of CSS rule duplication for fallbacks

**DO NOT** duplicate CSS rules to provide fallbacks for pseudo-classes that may not be supported — use `:is()` or `:where()` instead and take advantage of their forgiving parsing rules.

```css
/* BAD: duplicate rules instead of using `:where()` */
[popover]:popover-open {
  /* styles for native popovers */
}
[popover].\:popover-open {
  /* same styles again, for polyfilled popovers */
}

/* GOOD */
[popover]:where(:popover-open, .\:popover-open) {
  /* same styles in one rule */
}
```

Do NOT use this for pseudo-elements, as they are not supported in `:is()` or `:where()`.

### Avoid overmatching

Write selectors in a way that expresses _intent_.

#### Use `:not()` instead of overrides to exclude irrelevant states/targets

When the intent is to exclude certain states or elements that are fundamentally irrelevant, use `:not()`.

For example, to apply bottom borders between list items, don't do this:

```css
.fancy-list li {
  border-bottom: 1px solid silver;
}

.fancy-list li:last-child {
  border-bottom: none;
}
```

This can unintentionally overwrite a desirable `border-bottom` set from another rule.
The actual intent was to only apply the bottom border to the non-last `li`s. The code above is a workaround that poorly expresses this intent. Instead, this expresses intent more clearly:

```css
.fancy-list li:not(:last-child) {
  border-bottom: 1px solid silver;
}
```

Similarly, don't do this:

```css
button:hover {
  background: var(--color-blue);
}

button:disabled {
  background: var(--color-neutral);
}
```

If we reorder the two rules, we will get a hover background on disabled buttons!
Instead, do this:

```css
button:hover:not(:disabled) {
  background: var(--color-blue);
}

button:disabled {
  background: var(--color-neutral);
}
```

This works regardless of reordering, as the first rule does not overmatch.

#### Prefer `@scope` over `:not()` for excluding (potentially deeply nested) subtrees

While `:not()` + descendant selectors can exclude subtrees, this works poorly for deeply nested structures.
For example, `.card :not(.content *)` will not work as expected for nested cards.
`@scope` fixes this as it takes hierarchical proximity into account:

```css
@scope (.card) to (.content) {
  /* styles for elements inside .card but not inside .content */
}
```

This will work as expected even for nested cards.

#### Overrides are fine for specialization

This is fine:

```css
button {
  background: var(--color-neutral);
}

button.primary {
  background: var(--color-blue);
}
```

Both rules express legitimate _intent_: buttons are generally neutral, but primary ones are blue.

#### No global resets

**DO NOT** use global resets (styles on `*`) as they cannot be overridden by web components or lower-priority cascade layers (without `!important`). Instead, apply reset styles to specific element types and/or conditions.

### Nesting and scoping

Use native CSS nesting to group related styles to the extent it improves maintainability and readability.

Prefer `@scope` over nesting when proximity should matter more than pure specificity. This is common in selectors that can be nested in any order, but the closest matching one (in element -> ancestor order) should win, e.g. theming classes.

For example this will not work as expected:
```css
.dark .invert { color-scheme: light }
.light .invert { color-scheme: dark }
```

If `.invert` is nested within _both_ `.dark` and `.light`, it will always resolve to dark mode as both rules have the same specificity.
Using `@scope` fixes this:

```css
@scope (.dark) {
  .invert { color-scheme: light }
}

@scope (.light) {
  .invert { color-scheme: dark }
}
```

## 4. Interactivity

### Focus management

- Use `:focus-visible` to define custom focus rings, not `:focus`.
- Do not remove the browser's default focus rings (via `outline: none`) without providing an alternative visible focus style.
- Prefer `outline` over other properties (e.g. `box-shadow`) for focus rings. If you must rely on `box-shadow` for focus rings, provide an `outline`-based fallback for High Contrast Mode using the `forced-colors` media query.
- Pair focus outlines with `outline-offset` to visually separate the ring from the element.

### Touch targets

- Interactive elements should be at least 24×24 CSS pixels (WCAG 2.5.8 AA). Enforce with `min-block-size` / `min-inline-size` or padding rather than `width` / `height`, so content can grow the target but not shrink it.
- Bump targets up on coarse pointers: `@media (pointer: coarse) { ... }`.
- **DON'T** use `touch-action: none` for custom gestures — it disables page scrolling through the element. Scope to the axis you actually need: `pan-y` for horizontal swipes (page still scrolls vertically), `pan-x` for vertical ones. Reserve `none` for elements where no native touch behavior makes sense (e.g. a drawing canvas).

## 5. Design Tokens and Theming

Use CSS custom properties on `:root` to define core design variables (colors, fonts, sizes, etc) used throughout the design, for visual consistency and to scale UI design across teams.
**DO NOT** specify nontrivial styling values inline. E.g. `background: transparent` or `padding: 0` is ok, but `background: #f06` or `padding: .3em` are not.
One exception is use cases where keeping code small and simple is far more important than long-term maintainability and evolution, such as testcases.

Typically these are organized in tiers, with each tier building upon the previous one. For example:
1. Tier 1: Literal design tokens (e.g. `--color-blue-10`, `--color-gray-90`, `--font-sans-serif`, `--size-xl` etc)
2. Tier 2: Semantic design tokens (e.g. `--color-accent`, `--color-neutral`, `--font-body`, `--font-heading` etc)
3. Tier 3: General UI design tokens (e.g. `--ui-border`, `--surface-bg-subtle` etc)
4. Tier 4: Component-specific design tokens (e.g. `--button-bg-primary-hover`, `--button-border-color-secondary` etc)

The smaller the scope of the use case, the fewer tiers it needs. E.g. a quick demo or toy app are fine with one tier. Do not overengineer.
Check for any existing conventions around naming and levels before inventing your own.

### Dark mode

- Use `color-scheme: light dark` on `:root` to enable dark mode support that automatically adapts to the system setting. You can also specify `color-scheme` on individual elements to force a different value for that subtree (`light`/`dark` or `light dark` for the system default)
- Use `light-dark()` to provide alternatives that automatically resolve based on the element's `color-scheme`.
Typically this happens in Tier 2 or Tier 3 tokens.
- IMPORTANT: When using `light-dark()` on an inherited `<color>` property, it will resolve to a specific color based on that element's `color-scheme` and inherit as that resolved color, not as a `light-dark()` value. It will NOT adapt to any descendant-specific `color-scheme` overrides. To keep `light-dark()` color tokens dynamic resolve them as late as possible by only passing them around as unregistered custom properties and avoid relying on inherited color values across `color-scheme` boundaries.

See `dark-mode` (via `npx -y modern-web-guidance@latest retrieve "dark-mode"`) for tips & best practices on supporting dark mode switching and `component-specific-light-dark-theme` (via `npx -y modern-web-guidance@latest retrieve "component-specific-light-dark-theme"`) for more on applying different `color-scheme` modes than the page-wide setting on certain elements.

### Forced Colors Mode

In Forced Colors Mode (High Contrast on Windows), the browser overrides author colors with system keywords and strips `background-image`, `box-shadow`, and `border-image`.

- Define system color fallbacks for color tokens using `@media (forced-colors: active)`.
- **DON'T** rely on `background-image`, `box-shadow`, or `border-image` to convey borders, separators, or state — they disappear in forced colors (and often in print too). If you must, ensure there's an alternative in forced colors mode, such as `outline` or `border` with system color keywords (`CanvasText`, `LinkText`, `ButtonText`, `Highlight`, `GrayText`, etc.).
- Use `forced-color-adjust: none` where color is essential information (syntax highlighter, color picker swatch). **DON'T** use `forced-color-adjust: none` just to preserve aesthetics.


### Generating tints

Before generating tints dynamically, check if you can use an existing, predefined, design token. This allows much more designer control and ensures consistency.

If you need to generate lighter or darker colors dynamically:
- **DO NOT** just adjust the lightness channel in `oklch`/`oklab` or `lch`/`lab`, e.g. `oklab(from var(--primary) 0.9 a b)`. While that is theoretically the correct way, browsers do not yet implement gamut mapping, so the resulting color is unpredictable.
- You can use `color-mix()` to mix with white or black (preferably in `oklab`). This keeps the color safely in gamut, but tends to over-desaturate colors and produce washed out tints and shades.
- You MAY combine lightness adjustment with any of the other methods (e.g. `color-mix(in oklab, oklch(from var(--primary) 0.9 c h), white 30%)`) for a balance between the two, but avoid going above 30% for the lightness adjustment.

### Theming browser-generated UI

Most browser-generated UI can be customized to some extent using CSS.
Even if it requires modern features, it degrades gracefully in older browsers, and thus often does not require a polyfill or fallback.

Before re-creating browser UI (form controls, scrollbars, selections, error messages, etc), first verify that:
1. the browser UI cannot be customized enough for your needs, even with modern CSS,
2. the desired customization is sufficiently critical to justify the tradeoffs of re-creating built-in UI — most notably losing accessible semantics, keyboard handling, IME, and AT integration that the native UI provides for free.

Example customizations that are possible:
- Use `::selection` to customize highlighted text colors.
- **DON'T** apply `user-select: none` to content text — breaks copy-paste, translation tools, and AT "read from here" gestures. Limit it to chrome (drag handles, toolbars, redundant button labels).
- Use `accent-color` to apply the page's accent color to any browser-generated UI.
- Use `color-scheme` to have browser UI adapt to light/dark mode.
- Use `scrollbar-color` to customize scrollbar colors and `scrollbar-width` to control scrollbar thickness — keep the thumb visibly distinct from the track (≥3:1), and don't set `scrollbar-width: none` on scrollable regions (use it only when scrolling is fully replaced by another affordance).
- Use `:user-invalid` / `:user-valid` for validity styling, **not** `:invalid` / `:valid` — they only match after the user has interacted with the field, avoiding the hostile default of flagging required-empty fields as errors on page load.
- Buttons and text fields (including `<textarea>`) can generally be styled as normal elements.
- Use `font-size` to scale and other textual properties to control typography

#### Styling textual fields (`<input>` & `<textarea>`)

For most styling purposes (e.g. colors, borders, backgrounds, typography, etc) treat these elements as normal text containers.

- Use `:placeholder-shown` and `::placeholder` to style input placeholders.
- Use `field-sizing: content` to make text fields size to content.
- For `<textarea>` elements, use `resize: vertical` to disable horizontal resizing or `resize: none` to disable all resizing.

#### Multiple choice controls (select, radios, checkboxes)

- To select one among many options presented in a dropdown: Use a `<select>` + `appearance: base-select` + `::picker(select)`. For more info see `branded-select-styling` (via `npx -y modern-web-guidance@latest retrieve "branded-select-styling"`)
- Selecting one or more among multiple options laid out inline in the page: Use a `<input type=checkbox>` or `<input type=radio>` inside a `<label>` for each option. Style via `label:has(:checked)`.
- Style checkboxes, radios and switches via `appearance: none` + generated content (`::before`/`::after`) or background images to draw the checked state.
<!-- Customizable select listbox version currently buggy + this has much better browser support -->

#### Non-textual `<input>`s (buttons, sliders, file inputs etc.)

- File inputs: Use `::file-selector-button` to style the button.
- Do not use `<input>` with a `type` of `button`, `submit` or `reset`. Use `<button>` instead and style it as a regular element.
- Sliders: Use `appearance: none` + thumb pseudo-elements (`::-webkit-slider-thumb`, `::-moz-range-thumb`, etc) and track pseudo-elements (`::-webkit-slider-runnable-track`, `::-moz-range-track`, etc) for more granular control.

## 6. Responsive design

- Use `@container` queries to create component-driven responsive layouts that adapt to their parent container's size rather than the viewport.
- Use dynamic viewport units (`dvh`, `dvw`) instead of `vh`/`vw` to prevent layout breakage when mobile browser UI elements (like address bars) appear or disappear.
- Use `aspect-ratio` for media elements (like `<img>` and `<video>`) to reserve space during loading and prevent Cumulative Layout Shift (CLS).

### Responsive Typography

- **DO** combine viewport-relative and font-relative units in `clamp()` for font sizes that scale with the viewport size while ensuring they stay within a desired range. For example, `clamp(2rem, 1rem + 5vw, 4rem)`. Adjust the proportion of viewport-relative and font-relative units to control how quickly the font-size changes.
- **DON'T** use `vw` alone for font-size without `clamp()`, as it can scale text too small or too large on extreme screens.

## 7. Typography

- Use unitless numbers for `line-height` (e.g., `1.5`) to ensure relative scaling during font-size inheritance.
- Use `overflow-wrap: break-word` (or `anywhere`) to contain long URLs.
- **DON'T** use `px` for font-size. Prefer `rem` to honor the user's browser font-size preferences (root font size), or `em` for contextual sizing.

### Text wrapping

- Use `text-wrap: balance` for balanced headlines and headline-like content (e.g. `<th>`)
- Use `text-wrap: pretty` for long-form body text (paragraphs, blockquotes, etc.)
- Use `text-wrap: balance` or `text-wrap: pretty` deliberately, **DO NOT** apply it on `*` as it does have a performance cost.
- Avoid `text-wrap: balance` on elements with a visible box (backgrounds, borders, shadows, etc) as it does not change the container's width, it only affects how text wraps *within* that width. This can leave empty space at the end of the container, which is usually undesirable.

## 8. Visual effects

### Depth and texture

- Layer multiple shadows for realistic soft depth effects.
- Use `filter: drop-shadow()` instead of `box-shadow` for non-rectangular shapes or transparent PNGs.
- Use `mix-blend-mode` and `background-blend-mode` for lighting overlays (limit scope with `isolation: isolate`)

```css
.hero {
  background-image: url('texture.png'), linear-gradient(to bottom, #fff, #eee);
  background-blend-mode: soft-light;
}
```

### Shapes

- Use `corner-shape: squircle` for more aesthetically pleasing curves as a progressive enhancement over regular rounded corners.
- Use elliptical `border-radius` (e.g., `10px / 20px`) for proportional curves without extra elements.

### Gradients and `color-mix()`

Use `in oklch` or `in oklab` to explicitly specify the interpolation color space for gradients or `color-mix()`.
- `in oklch` preserves chroma better, but can more easily get out of device gamut, especially for bigger differences between colors
- `in oklab` stays in gamut more easily (assuming in-gamut endpoints) but can create washed out desaturated colors in the middle, especially when interpolating between opposite hues.
- *DON'T* use `in srgb` unless you have a specific reason to do so (e.g. you are building a color picker that needs to interpolate in srgb).

#### Fallback

Some pre-2024 browsers do not support gradient color interpolation space.
To support these browsers, use the token only when its usage is safe by defining a variable:

```css
:root {
  --in-oklab: ;
  --in-oklch: ;
}

@supports (linear-gradient(in oklab, white, black)) {
  :root {
    --in-oklab: in oklab;
    --in-oklch: in oklch;
  }
}
```

Then use like:

```css
.card {
  background: linear-gradient(to bottom var(--in-oklab), var(--accent-color), var(--darker));
}
```

- **Important:** If you use this technique, make sure there is always a non-empty gradient preamble without it, otherwise it will be a syntax error in older browsers.
- You do NOT need this for `color-mix()`. If a browser supports `color-mix()`, it also supports its `in <color-space>` argument.

### Patterns

Many patterns can be created via CSS gradients + hard stops, and these can be more flexible and performant than SVGs or external images as they can have access to CSS variables and lengths from the surrounding context.
You don't need to repeat the position twice — just use `0` or `0%` and gradient fixup will auto-adjust it.

Examples below.

Vertical stripes of `1em` width each:

```css
background: linear-gradient(to right, var(--color-1) 50%, var(--color-2) 0) 0 / 2em;
```

Diagonal stripes of `1em` width each:

```css
background: repeating-linear-gradient(-45deg, var(--color-1) 0 1em, var(--color-2) 0 2em);
```

Checkerboard pattern with `1em` squares:

```css
background: repeating-conic-gradient(var(--color-1) 0 25%, var(--color-2) 0 50%) 0 / 2em 2em;
```

Polka dot with `.5em` radius dots spaced `2em` apart (horizontally/vertically — multiply by `sqrt(2)` for diagonal distance):

```css
--distance: 2em;
--radius: .5em;
--polka: radial-gradient(circle, var(--color-1) var(--radius), transparent calc(var(--radius) + 1px));
background: var(--polka) 0 0, var(--polka) var(--distance) var(--distance) var(--color-2);
background-size: calc(var(--distance) * 2) calc(var(--distance) * 2);
```

Simple pie chart:

```css
.pie {
  --p: 80%;
  width: 60px;
  aspect-ratio: 1;
  border-radius: 50%;
  background: conic-gradient(var(--color-1) var(--p), transparent 0%) var(--color-2);
}
```

**Important:** When using gradients to render charts, ensure there is a textual fallback for screen readers. MANDATORY: You MUST provide a semantic data table as an accessible alternative, as detailed in `accessibility` (via `npx -y modern-web-guidance@latest retrieve "accessibility"`) under the alternate text and media guidelines.

## 9. Transitions & animations

- Use `clip-path` and `mask-image` for custom geometric reveals and smooth fade-outs.
- Use **Scroll-Driven Animations** (`animation-timeline: scroll()`) for non-essential scroll-bound effects instead of JS listeners.
- Use **View Transitions** to animate between complex layout states seamlessly.

### Performance

Rendering performance is critical for smooth user experiences, especially in heavy DOM trees.

- Prefer to animate `opacity` and `transform` (including individual transform properties, e.g. `translate` instead of `left/right/top/bottom`) to ensure animations stay on the compositor thread.
- Use `transition-behavior: allow-discrete` + `@starting-style` to animate layout properties like `display` or `<dialog>` state natively.
- Always pair `content-visibility` with `contain-intrinsic-size` to prevent scrollbar jumps (CLS).
- When setting `contain-intrinsic-size` use the `auto` keyword and a value that’s derived from what is known about the contents (i.e. text size, spacing, size of graphics, character count). Preferably use units such as `rem`, `lh`, `cap`, or `ch` that match values used for the elements within the contents rather than `px`. If the content for items in a group is not consistently sized, then use an average size.
- Use `contain: layout style paint` to isolate component rendering updates.

#### Code Example: Render Optimization

```css
.large-section {
  content-visibility: auto;
  contain-intrinsic-block-size: auto 800px;
}

.row {
  --row-gap: .4rem;
  --title-height: 1lh;
  --description-height: 0.85lh;

  display: grid;
  row-gap: var(--row-gap);
  content-visibility: auto;
  /* The sum of the title height, row gap, and description height should be the size of the contents when skipped for rendering. */
  contain-intrinsic-block-size: auto calc(var(--title-height) + var(--row-gap) + var(--description-height));
}

.popover-reveal {
  /* Allow discrete animations for display transitions */
  transition: display 0.2s allow-discrete;
}
```

### Accessibility

Use `prefers-reduced-motion` media queries to turn off heavy motion for users who prefer it.

**DO NOT** globally apply `animation-duration: 0.01ms;` globally as it can cause certain animations to become _more_ jarring.
Either apply reduced motion versions on a case by case basis, or use a custom property like:

```css
@property --animation-reduced {
  syntax: "*";
  inherits: false;
  initial-value: none;
}

@media (prefers-reduced-motion: reduce) {
  * {
    animation: var(--animation-reduced) !important;
  }
}
```

Then, reduced motion versions can be kept together with the original animations:

```css
progress:not([value]) {
  animation: slide 1s infinite linear;
  --animation-reduced: slide 20s infinite linear;
}
```

## 10. Generated content

- **DON'T** use `content` to convey meaningful text (labels, state, instructions) — keep that in the DOM (WCAG F87). The alt text argument is harm reduction for cases where decoration accidentally carries meaning, not a license.
- Use the alternative text argument of `content` to provide alt text for screen readers. E.g. `content: url(cloud.svg) / "Save";`
- Use `content: "text" / "";` to prevent purely decorative text from being announced to screen readers.
- **DON'T** use an empty alt text argument for images — they're already presentational by default. E.g. this is wrong: `content: url(cloud.svg) / "";`.
- **DON'T** use the alt text argument to describe emojis unless the description differs from the official emoji name. E.g. don't do `content: "🎉" / "celebration";`, but `content: "🎉" / "Yay!";` is fine.

**ONLY** use the alt text argument when the text is different than the primary value and is not already present in the DOM. I.e. this is wrong:

HTML:
```html
<button class="save">Save</button>
```

CSS:
```css
button.save::before {
  content: url(cloud.svg) / "Save";
}
```

A screen reader would read it out as "Save save".

---

# CSS Layouts and Responsive Design

1. [1 Fundamentals](#1-fundamentals)
   1. [Which layout mode to use?](#11-which-layout-mode-to-use)
   2. [Working principles](#12-working-principles)
2. [2 Flexbox](#2-flexbox)
3. [3 Grid and subgrid](#3-grid-and-subgrid)
   1. [Code example: grid and subgrid](#31-code-example-grid-and-subgrid)
4. [4 Container queries](#4-container-queries)
   1. [Code example: fluid typography using container query units](#41-code-example-fluid-typography-using-container-query-units)
5. [5 Native overlays, anchor positioning, and stacking contexts](#5-native-overlays-anchor-positioning-and-stacking-contexts)
6. [6 Overflow tracking and layout stability](#6-overflow-tracking-and-layout-stability)
7. [7 Viewport mechanics and track distribution](#7-viewport-mechanics-and-track-distribution)
8. [8 Grid lanes (aka masonry)](#8-grid-lanes-aka-masonry)

## 1 Fundamentals

Lean on the browser's layout engine when possible for better performance. Reach for intrinsic sizing, logical properties, and `aspect-ratio` before resorting to hardcoded dimensions or complicated media-queries.

### 1.1 Which layout mode to use?

Walk the decision tree top-to-bottom and stop at the first match. Note that layouts can be nested within each-other and each decision is based on the use-case for that container.

1. **Is it a simple row OR column of items?** Use **flexbox** — 1D, content-first, content distributes along a single axis.
2. **Does a nested element need to line up with its grandparent grid's tracks?** Use **subgrid** — 2D, relationship-first, inherits parent tracks so grandchildren can align across siblings.
3. **Is it a complex page or component structure with rows AND columns?** Use **grid** — 2D, layout-first, you define the skeleton and content fills it.
4. **Is the content a long flow of prose that should split into balanced columns?** Use **multi-column** — 1D flow, newspaper-style.
5. **Are items of varied heights that need to be packed tightly?** Use **grid** with `grid-auto-flow: dense` today; reach for native masonry (aka "grid lanes") only when it ships in your Baseline target (see [§8](#8-grid-lanes-aka-masonry)).
6. **Does an element need to float above the page and stay spatially tethered to a trigger, even across DOM boundaries or stacking contexts?** Use **anchor positioning** — `anchor-name` on the trigger, `position-anchor` on the overlay (see [§5](#5-native-overlays-anchor-positioning-and-stacking-contexts)).

### 1.2 Working principles

**Do:**

- Use logical properties (`inline-size`, `block-size`, `margin-inline`, `padding-block`, `inset-inline-start`) for layout dimensions and spacing — see `css` (via `npx -y modern-web-guidance@latest retrieve "css"`) for full coverage.
- Apply the content-first vs layout-first mental model: flexbox when items dictate flow, grid when you define the skeleton first.
- Use the `place-*` shorthands (`place-content`, `place-items`, `place-self`) to align across both axes in one declaration.
- Reach for intrinsic sizing (`min-content`, `max-content`, `fit-content()`) and flexible tracks (`fr`, `minmax()`) before fixed `width`/`height` — fewer media queries, more resilient layouts.
- Use `aspect-ratio` to reserve space for media and prevent layout shift before assets load.

```css
.sidebar       { inline-size: max-content; }    /* Size to longest unbreakable token. */
.main-content  { inline-size: fit-content; }    /* Grow to available space, no further. */
.media         { aspect-ratio: 16 / 9; inline-size: 100%; block-size: auto; }
body.centered  { display: grid; place-content: center; min-block-size: 100dvb; }
```

> For `calc-size()` and constraint-aware intrinsic sizing, see `calculate-with-intrinsic-sizes` (via `npx -y modern-web-guidance@latest retrieve "calculate-with-intrinsic-sizes"`).

## 2 Flexbox

One-dimensional layout — items flow along a single **main** axis with alignment on the **cross** axis. Reach for it for navbars, toolbars, item rows, and any single-row-or-column distribution.

**Do:**

- Establish a context with `display: flex` and set the main axis with `flex-direction` (`row` default).
- Use `flex-wrap: wrap` whenever overflow is a possibility — `nowrap` without `overflow: auto/hidden` will spill on narrow viewports.
- Use the `flex` shorthand `<grow> <shrink> <basis>` (e.g., `flex: 1 1 250px`) on items rather than setting `flex-grow`/`flex-shrink`/`flex-basis` individually.
- Use `gap` (or the `row-gap`/`column-gap` longhand) for spacing between items instead of child margins.
- Prefix positional alignment with `safe` (e.g., `align-items: safe center`) so focusable content isn't clipped when the container is narrower than its content.
- Push a single item to the far end of the main axis with `margin-inline-start: auto` (or `margin-block-start: auto`) — that's the standard escape hatch.
- Override cross-axis alignment per item with `align-self`.
- Use `align-items` to center all items on the cross axis; use `margin: auto` on a single item to center it on both axes independently; use `align-content` only when the container wraps and has extra space across rows.
- Set `min-inline-size: 0` (or `min-width: 0`) on flex items that contain long unbreakable content (URLs, code, long strings) — flex items won't shrink below their content size by default, causing overflow.

**Do not:**

- Don't reach for `justify-self` on flex items — it only works on grid, block, and absolutely-positioned layouts. Use auto margins instead.
- Don't use `order` or `flex-direction: *-reverse` to reorder interactive content. They change visual order only; the DOM order still drives sequential focus, so keyboard tab flow won't match what the user sees.
- Don't confuse `space-around` (half-gap at the ends) with `space-evenly` (equal gaps before, between, and after).
- Don't forget the axis flip: when `flex-direction: column`, `justify-content` aligns on the block axis and `align-items` aligns on the inline axis — the opposite of the default.
- Don't size both the container and its children to fill each other — that's a common source of overflow and surprising results. Give one side a definite size.
- Don't set both `flex-basis` and `width`/`inline-size` on the same item — `flex-basis` takes precedence in a flex context and `width` is ignored. Use `flex-basis` (or the `flex` shorthand) as the single source of truth for sizing flex items.

```css
.card-grid        { display: flex; flex-flow: row wrap; gap: 1rem; }
.card-item        { flex: 1 1 250px; }                  /* grow, shrink, basis */
.card-item-action { margin-inline-start: auto; }        /* Push to main-axis end. */
.toolbar          { display: flex; align-items: safe center; }
```

## 3 Grid and subgrid

Baseline status for Subgrid: Widely available. It's been Baseline since 2023-09-15.
Supported by: Chrome 117 (Sep 2023), Edge 117 (Sep 2023), Firefox 71 (Dec 2019), and Safari 16 (Sep 2022).

Two-dimensional layout — define rows AND columns explicitly, or let the engine derive them. Subgrid lets a nested grid inherit its parent's tracks so grandchildren align across siblings.

**Choosing grid features:**

- Do you know exactly how many columns you need?
  - **Yes** — use explicit tracks (`grid-template-columns: 200px 1fr`, `repeat(3, 1fr)`, etc.)
    - Do different columns need different sizes (sidebar + main, header spanning all)? → use `grid-template-areas` for named, readable regions
    - Are all columns uniform or positioned purely by line number? → use `repeat(N, ...)` or named lines
  - **No** (responsive, unknown item count) — use `repeat(auto-fit, minmax(min, 1fr))`
    - Should items on the last row stretch to fill remaining space? → `auto-fit`
    - Should empty last-row tracks hold their min size (preserving column ghost slots)? → `auto-fill`
- Do you need to place an item at a specific location?
  - **Yes** — use `grid-column: <start> / <end>` or `grid-area: <name>`
  - **No** (just spanning multiple tracks, flow position doesn't matter) — use `grid-column: span <n>`
- Do child elements need to inherit the parent grid's track sizes (ragged-edge alignment across siblings)?
  - **Yes** — use subgrid on the affected axis
    - Is the number of children per cell variable? → subgrid **one axis only**; use `grid-auto-rows`/`grid-auto-columns` for the other
    - Is the child count fixed? → subgrid on both axes is fine
  - **No** — standard grid, no subgrid needed

**Do:**

- Establish a context with `display: grid`.
- Use `grid-template-areas` for complex page-level layouts — area names are self-documenting and the declaration can be aligned in rows and columns for at-a-glance readability.
- Use `repeat(auto-fit, minmax(200px, 1fr))` for responsive card grids that stretch filled tracks to fill the row, or `auto-fill` to preserve empty repeated tracks at their min size.
- Use `fr` for proportional track distribution and `minmax(min, max)` for flexible-but-bounded tracks.
- Position items with `grid-column: span <n>` to size across tracks, `grid-column: <start> / <end>` to place at specific lines, or `grid-area: <name>` for named regions.
- Use subgrid (`grid-template-columns: subgrid` or `grid-template-rows: subgrid`) to solve the "ragged edge" problem in card lists — internal elements like titles, metadata, and CTAs line up across siblings.
- Pair a subgrid declaration with a preceding explicit `grid-template-rows`/`-columns` declaration as a same-cascade fallback for older browsers.

**Do not:**

- Don't expect `auto-fit`/`auto-fill` track size to come from item content — it comes from the `repeat()` size argument.
- Don't use `grid-auto-flow: dense` on interactive content. It packs items efficiently but reorders them visually, breaking DOM-order keyboard tab flow.
- Don't apply subgrid to both axes when the child count is variable. Extras land in the last track; use `grid-auto-rows`/`grid-auto-columns` for the implicit axis instead.
- Don't confuse `justify-items`/`align-items` (aligns item content *within its track*) with `justify-content`/`align-content` (aligns the grid tracks *within the container*). Using the wrong one silently has no effect.
- Don't use `repeat(auto-fit/auto-fill, ...)` without a definite `inline-size` on the container — inside `display: inline-grid` or an unsized flex item, the container has no width to divide, making track counts unpredictable.

### 3.1 Code example: grid and subgrid

Page shell: `<main class="page-layout">` contains `<header>`, `<aside>`, a `<section class="card-grid">` with `<div class="card">` children, and `<footer>`.

```css
/* Align grid-template-areas in rows and columns for readability. */
.page-layout {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-areas:
    "header  header  header"
    "sidebar main    main"
    "footer  footer  footer";
  gap: 1.5rem;
}

header  { grid-area: header; }
aside   { grid-area: sidebar; }
footer  { grid-area: footer; }

.card-grid {
  grid-area: main;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  grid-template-rows: auto 1fr; /* title block, body block */
  gap: 1rem;
}

.card {
  grid-row: span 2;
  display: grid;
  /* Same-cascade fallback: ignored when subgrid is supported. */
  grid-template-rows: auto 1fr;
  grid-template-rows: subgrid;
}
```

## 4 Container queries

Baseline status for Container queries: Widely available. It's been Baseline since 2023-02-14.
Supported by: Chrome 105 (Sep 2022), Edge 105 (Sep 2022), Firefox 110 (Feb 2023), and Safari 16 (Sep 2022).

Query the size (or computed style) of an ancestor container rather than the viewport. Mental model: container queries = component context; media queries = global page layout and user preferences (`prefers-color-scheme`, `prefers-reduced-motion`).

**Do:**

- Establish a containment context with `container-type: inline-size` (width-only queries) or `container-type: size` (both axes) on a wrapper before its descendants can be queried.
- Name containers with `container-name` (or the `container` shorthand: `container: inline-size card`) when nested contexts could collide.
- Include container query units in calculating fluid type and spacing: `cqi`/`cqb` (logical inline/block), `cqw`/`cqh` (physical), `cqmin`/`cqmax`.
- Give the container a definite `block-size` whenever `container-type: size` is used — without one, descendants collapse because size containment forces the container to ignore its content.

**Do not:**

- Don't use `block-size` as a `container-type` value — it isn't valid. Use `size` for both axes.
- Don't expect children's intrinsic size to influence the container after declaring `container-type`. The container is computed as if it has no children once containment is active.
- Don't rely on container query units inside descendants of a non-qualifying ancestor; they fall back to the small viewport (`svw`/`svh`).

### 4.1 Code example: fluid typography using container query units

```css
.card-wrapper {
  container: inline-size / card; /* shorthand for container-type + container-name */
}

@container card (inline-size > 400px) {
  .content {
    display: flex;
    gap: 2rem;
  }
}

.title {
  /* Fluid type bound to the container width, not the viewport. */
  font-size: clamp(1rem, 4cqi, 2rem);
}
```

> For component-driven responsive styling patterns, see `size-aware-styling` (via `npx -y modern-web-guidance@latest retrieve "size-aware-styling"`) and `fluid-scaling` (via `npx -y modern-web-guidance@latest retrieve "fluid-scaling"`).

## 5 Native overlays, anchor positioning, and stacking contexts

Baseline status for <dialog>: Widely available. It's been Baseline since 2022-03-14.
Supported by: Chrome 37 (Aug 2014), Edge 79 (Jan 2020), Firefox 98 (Mar 2022), and Safari 15.4 (Mar 2022).
Baseline status for Popover: Newly available. It's been Baseline since 2025-01-27.
Supported by: Chrome 116 (Aug 2023), Edge 116 (Aug 2023), Firefox 125 (Apr 2024), Safari 17 (Sep 2023), and Safari iOS 18.3 (Jan 2025).
Anchor positioning is not natively supported by any major browser yet.

**When to use each overlay primitive:**

- Use `popover` for transient, non-modal UI (flyouts, toasts, tooltips) — lives in the top layer, no `z-index` management needed.
- Use `<dialog>` with `.showModal()` for modal interactions that require focus trapping and an inert backdrop.
- Don't combine `popover` and `.showModal()` on the same element — they're mutually exclusive runtime states.

**Anchor positioning (spatial layout of overlays):**

- Use `position-area` (or `anchor()` on insets) and `anchor-size()` to position and size an overlay relative to its trigger.
- Use `position-try-fallbacks: flip-block` (or `flip-inline`) to let the browser reposition when the overlay overflows the viewport.
- Don't mix physical and logical keywords in a single `position-area` value — pick one coordinate system.
- Feature-detect with `@supports (anchor-name: --x)` and provide an absolute-position fallback.

> For full implementation detail, polyfill strategies, and `popover` value reference, see `declarative-dialog-popover-control` (via `npx -y modern-web-guidance@latest retrieve "declarative-dialog-popover-control"`) and `position-aware-tooltips` (via `npx -y modern-web-guidance@latest retrieve "position-aware-tooltips"`). For anchor positioning applied to menus and tab indicators, see `resilient-context-menus-and-nested-dropdowns` (via `npx -y modern-web-guidance@latest retrieve "resilient-context-menus-and-nested-dropdowns"`) and `anchor-positioning-tab-underline` (via `npx -y modern-web-guidance@latest retrieve "anchor-positioning-tab-underline"`).

## 6 Overflow tracking and layout stability

Baseline status for scrollbar-gutter: Newly available. It's been Baseline since 2024-12-11.
Supported by: Chrome 94 (Sep 2021), Edge 94 (Sep 2021), Firefox 97 (Feb 2022), and Safari 18.2 (Dec 2024).
line-clamp is not natively supported by any major browser yet.

Manage layout shifts, scrollbars, and clipping predictably.

**Do:**

- Use `overflow: auto` so scrollbars appear only when content actually overflows.
- Use `overflow: clip` to clip content **without** establishing a scroll container; opt into spillover with `overflow-clip-margin`.
- Use `scrollbar-gutter: stable` to reserve space for scrollbars and prevent layout shifts when content grows.
- Use `overscroll-behavior: contain` (or `none`) on scrollable containers to stop scroll chains from bubbling into the parent or document.
- Use the `-webkit-line-clamp` + `display: -webkit-box` + `-webkit-box-orient: vertical` triad for multi-line truncation — despite the prefix, this pattern is fully specified and not deprecated. Declare the unprefixed `line-clamp` shorthand alongside it; browsers that don't yet support it ignore the property harmlessly.
**Do not:**

- Don't use `overflow: scroll` when `auto` will do — `scroll` forces scrollbars even when there's nothing to scroll.
- Don't reach for `overflow: hidden` when you only want to clip — `hidden` establishes a scroll container that can be programmatically scrolled.

```css
.scrollable-list {
  max-block-size: 400px;
  overflow-y: auto;
  scrollbar-gutter: stable;       /* Reserve scrollbar space. */
  overscroll-behavior: contain;   /* No scroll chaining into the page. */
}

.snippet {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  line-clamp: 3;                  /* Ignored where unsupported. */
  overflow: clip;
}
```

> For `overflow: clip` and `overflow-clip-margin` in depth, see `overflow-clipping-control` (via `npx -y modern-web-guidance@latest retrieve "overflow-clipping-control"`). For scrollbar color, sizing, and theming, see `customize-scrollbar-color-and-thickness` (via `npx -y modern-web-guidance@latest retrieve "customize-scrollbar-color-and-thickness"`), `dark-mode` (via `npx -y modern-web-guidance@latest retrieve "dark-mode"`), and `adapt-scrollbar-to-contrast-preferences` (via `npx -y modern-web-guidance@latest retrieve "adapt-scrollbar-to-contrast-preferences"`).

## 7 Viewport mechanics and track distribution

Baseline status for Small, large, and dynamic viewport units: Widely available. It's been Baseline since 2022-12-05.
Supported by: Chrome 108 (Nov 2022), Edge 108 (Dec 2022), Firefox 101 (May 2022), and Safari 15.4 (Mar 2022).

- Use `dvh`/`dvw` for mobile layout containers that must account for browser UI shifting (URL bar collapse/expand).
- Don't use `100vw` for full-width layout — it ignores scrollbar width and causes horizontal overflow. Use `100%`, `100dvw`, or `100svw` instead.

> For the full viewport unit reference (`svh`, `lvh`, `dvi`, `dvb`, etc.), see `css` (via `npx -y modern-web-guidance@latest retrieve "css"`).

## 8 Grid lanes (aka masonry)

Masonry is not natively supported by any major browser yet.

The spec is in development. The currently agreed-upon name is "grid lanes" (e.g., `display: grid-lanes`). Firefox ships `grid-template-rows: masonry` behind a flag; no other engines ship it in stable as of this writing.

**Do:**

- Use grid with `grid-auto-flow: dense` for tight packing today, accepting that DOM order may not match visual order.
- Use multi-column (`columns: 3; column-gap: 1rem`) for content-heavy masonry-like flow when items are document fragments rather than equal-weight cards.
- Treat `grid-template-rows: masonry` as a progressive enhancement only — feature-detect with `@supports`.

**Do not:**

- Don't ship `grid-template-rows: masonry` as a hard requirement until your Baseline target catches up.

```css
.gallery       { columns: 3 200px; column-gap: 1rem; }
.gallery > *   { break-inside: avoid; margin-block-end: 1rem; }

@supports (grid-template-rows: masonry) {
  .gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    grid-template-rows: masonry;
    gap: 1rem;
    columns: unset;
  }
}
```
