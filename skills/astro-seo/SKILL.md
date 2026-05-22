---
name: astro-seo
description: "Audit and improve SEO for Astro sites, including metadata, structured data, sitemaps, indexing, Open Graph images, schema endpoints, and related search visibility setup."
metadata:
  maturity: draft
  kind: task
---

# Astro SEO

## Use this skill when

- The user wants to audit, set up, or improve SEO in an Astro project.
- The task mentions head metadata, canonicals, structured data, JSON-LD, Open Graph images, sitemaps, indexing, IndexNow, schema endpoints, `llms.txt`, NLWeb, or hreflang in an Astro site.
- The user wants a practical Astro SEO implementation path rather than generic SEO advice.
- The work should route through `@jdevalk/astro-seo-graph` when that package is a good fit.

## Do not use this skill when

- The project is not an Astro site.
- The main task is reviewing short strings like titles, descriptions, or bios rather than the SEO system. Use [`writing-and-editing`](../writing-and-editing/SKILL.md) in metadata-audit mode.
- The main task is auditing multi-paragraph prose quality rather than the site's technical or structural SEO. Use [`writing-and-editing`](../writing-and-editing/SKILL.md) in readability-audit mode.
- The user only wants a broad content marketing strategy with no repository or implementation work.

## Inputs to gather

**Required before editing**

- `astro.config.*`, especially `site`, adapter, integrations, and any i18n setup.
- `package.json` scripts, Astro version, deployment target, and whether `@jdevalk/astro-seo-graph` is already installed.
- Current content layout (`src/content`, `src/pages`, layouts, head components, SEO helpers).
- Existing sitemap, robots, RSS, OG image, and schema wiring.

**Helpful if present**

- Whether the site is multilingual.
- Whether the site already publishes RSS, schema endpoints, or markdown alternates.
- Existing CI validation, broken-link checks, or build-time SEO validation.

**Only investigate if encountered**

- Search Console, Bing Webmaster Tools, analytics, or other manual post-file setup.
- Host-specific redirect and header behavior for Vercel, Netlify, Cloudflare, or static hosting.

## First move

1. Confirm this is an Astro site and read `astro.config.*` before proposing any SEO change.
2. Treat a missing or local-only `site` config as a blocking issue because canonicals, sitemaps, and OG URLs depend on it.
3. Check whether `@jdevalk/astro-seo-graph` is already installed and, if so, whether the project should upgrade before deeper auditing.

## Workflow

1. Detect the project shape: deployment target, content model, locales, and current SEO implementation path.
2. Audit the site across the major SEO surfaces:
   - head metadata and canonical behavior
   - structured data / JSON-LD
   - content schema and collection validation
   - Open Graph images
   - sitemaps, robots, RSS, and indexing
   - agent-discovery surfaces such as schema endpoints, schema maps, `llms.txt`, and markdown alternates
   - performance and redirect hygiene
   - build-time validation and link checking
3. Recommend the smallest coherent implementation path:
   - upgrade or install `@jdevalk/astro-seo-graph` when it materially simplifies the missing pieces
   - preserve an existing hand-rolled setup when it already satisfies the important requirements
4. Implement the missing pieces, using `references/implementation-recipes.md` for concrete code recipes when needed.
5. Run [`writing-and-editing`](../writing-and-editing/SKILL.md) in metadata-audit mode on any short SEO strings you generated or rewrote, such as titles, descriptions, schema descriptions, FAQ answers, or frontmatter excerpts.
6. If the task also produced long-form prose, mention [`writing-and-editing`](../writing-and-editing/SKILL.md) in readability-audit mode as a follow-up rather than trying to audit the whole content corpus inline.

## Outputs

- SEO audit findings tied to the actual Astro files and routes that control metadata, canonicals, schema, sitemap, robots, and OG output.
- Implemented or recommended Astro SEO changes such as config/component updates or an `@jdevalk/astro-seo-graph` install/upgrade path.
- Validation evidence from representative pages or generated artifacts showing the expected canonical, metadata, schema, and crawl-surface output.


## Guardrails

- **Must not** proceed with canonical, sitemap, or OG URL work without verifying the production `site` origin.
- **Must not** assume every audit finding requires replacing the existing SEO stack.
- **Must not** add SSR or client hydration to solve SEO problems a static Astro build already handles well.
- **Must not** treat metadata-string review as the same task as technical SEO implementation.
- **Should** prefer `@jdevalk/astro-seo-graph` as the default spine when the project needs head metadata, schema, IndexNow, redirects, and build-time validation in one path.
- **Should** branch on the current state: install when missing, upgrade when outdated, and selectively wire features when the package is already present.
- **Should** quote real code or config when reporting audit findings instead of giving generic SEO advice.
- **Should** call out any manual setup the repo cannot automate, such as Search Console registration, Bing Webmaster Tools, analytics, or IndexNow key management.

## Validation

- Run the project's existing Astro validation path first, typically `astro check` and/or `npm run build`.
- Confirm the resulting HTML has correct canonical and metadata output on representative pages.
- Verify sitemap, robots, RSS, schema, and OG routes or generated files where relevant.
- If build-time SEO validation is wired, surface warnings explicitly rather than hiding them behind a passing build.

## Examples

- "Audit the SEO on my Astro blog."
- "Set up structured data, sitemap, and OG images for this Astro site."
- "Help me add schema endpoints and `llms.txt` to my Astro project."
- "Our Astro site has weak metadata and indexing. Fix the setup."

## Reference files

- Read `references/implementation-recipes.md` when you need implementation recipes for installing, upgrading, and wiring the recommended Astro SEO stack.
