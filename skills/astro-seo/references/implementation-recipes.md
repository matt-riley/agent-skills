# Astro SEO — Implementation recipes

Detailed code recipes for Phase 2 (Improve). Read this file when you need to implement a specific fix flagged by the audit. The parent `SKILL.md` has the workflow and audit checklist.

## Install or upgrade `@jdevalk/astro-seo-graph`

If not installed:

```sh
npm install @jdevalk/astro-seo-graph
```

If installed but behind the latest npm version (checked in Phase 0):

```sh
npm install @jdevalk/astro-seo-graph@latest
```

Read the package's [changelog](https://github.com/jdevalk/seo-graph/blob/main/packages/astro-seo-graph/CHANGELOG.md) between the installed and latest version before upgrading — new defaults may need explicit opt-out if the project relied on old behavior.

**1.0.0 migration note.** `<Seo>` is now a first-party component (drops the `astro-seo` dep) and `buildAstroSeoProps` / the `AstroSeoProps` type were removed. If the project called `buildAstroSeoProps` directly, migrate to `buildSeoContext` (returns a flat `SeoContext`). Sites using `<Seo>` through the normal prop interface need no code change — the upgrade also fixes three silent bugs (`articlePublisher` now renders, canonical no longer leaks on `noindex` pages, single `og:image` and single `<meta name="robots">` per page).

## Integration config

```js
// astro.config.mjs
import seoGraph from '@jdevalk/astro-seo-graph/integration';

// Only submit to IndexNow on the production host. Local `npm run build`
// and preview deploys should not ping the endpoint with URLs the host
// hasn't served yet — that gets the key rejected (403) and forces rotation.
const isProductionBuild =
    process.env.CF_PAGES === '1' && process.env.CF_PAGES_BRANCH === 'main';
    // Vercel: process.env.VERCEL_ENV === 'production'
    // Netlify: process.env.CONTEXT === 'production'

export default defineConfig({
    site: 'https://example.com',
    integrations: [
        seoGraph({
            validateH1: true,
            validateUniqueMetadata: true,
            validateImageAlt: true,
            validateMetadataLength: true,
            validateInternalLinks: {
                // ≥ 1.1.1 recognises non-HTML files from public/ as valid
                // link targets automatically. `skip` is still useful for
                // SSR-only routes, wildcards, and `[slug]` params.
                skip: (href) => href.startsWith('/api/'),
            },
            ...(isProductionBuild && {
                indexNow: {
                    key: process.env.INDEXNOW_KEY,
                    host: 'example.com',
                    siteUrl: 'https://example.com',
                },
            }),
            llmsTxt: {
                title: 'Example',
                siteUrl: 'https://example.com',
            },
            // Emit <link rel="alternate" type="text/markdown"> on every
            // page. Only enable once `createMarkdownEndpoint` is wired at
            // the matching path (see § Markdown alternates below),
            // otherwise the link 404s. Requires ≥ 1.2.0.
            markdownAlternate: true,
        }),
    ],
});
```

## `BaseHead.astro`

Replace whatever head metadata the project has with a single `<Seo>` call. The component handles title, description, canonical, Open Graph, Twitter, JSON-LD graph, and extra links in one place.

## Content collection schema

```ts
// src/content/config.ts
import { defineCollection, z } from 'astro:content';
import { seoSchema } from '@jdevalk/astro-seo-graph';

export const collections = {
    blog: defineCollection({
        schema: ({ image }) => z.object({
            title: z.string(),
            excerpt: z.string(),
            publishDate: z.coerce.date(),
            seo: seoSchema(image).optional(),
        }),
    }),
};
```

## Per-collection sitemap + git lastmod

```js
import sitemap from '@astrojs/sitemap';
import { execSync } from 'node:child_process';

function gitLastmod(filePath) {
    try {
        const log = execSync(`git log -1 --format="%cI" -- "${filePath}"`, { encoding: 'utf-8' }).trim();
        return log ? new Date(log) : null;
    } catch { return null; }
}

sitemap({
    entryLimit: 1000,
    chunks: {
        posts: (item) => isBlogPost(new URL(item.url).pathname) ? item : undefined,
    },
    serialize: (item) => {
        // attach gitLastmod for the source file that produced this URL
        return item;
    },
});
```

## OG image route

The goal: every page has a 1200×675 JPEG OG image with a deterministic URL derived from the slug, generated at build time. No manual upload step, no runtime rendering.

**Pick the renderer.**

- **Text-heavy cards** (title + subtitle + site name over a solid or gradient background) — use [`satori`](https://github.com/vercel/satori) to render JSX/HTML to SVG, then [`sharp`](https://sharp.pixelplumbing.com/) to rasterize to JPEG. This is the common case. Satori doesn't support every CSS feature — stick to flexbox, basic typography, absolute positioning.
- **Photo-heavy cards** (hero image with a title overlay) — skip satori. Use `sharp`'s composite pipeline: load the hero from `public/`, resize to 1200×675, composite an SVG overlay for the title band, encode JPEG. Faster and avoids satori's CSS limits.

**Build-time route vs. build script.**

A route at `src/pages/og/[...slug].jpg.ts` that runs in `getStaticPaths` is the cleanest fit for Astro: one file, colocated with the content, no external build step, per-page URLs just work. Use a standalone Node build script that writes to `dist/og/` only when you need to share the renderer across sites or run it outside Astro. Default to the route.

**Fonts.**

Satori needs font buffers, not CSS. Commit a `woff2` (or TTF — satori accepts both) under `src/fonts/` and read it with `fs.readFileSync` at build time. For text that might contain glyphs the primary font doesn't cover (CJK, emoji, extended Latin), pass multiple fonts in the `satori({ fonts: [...] })` array — satori falls back through them in order. Don't rely on system fonts; the build environment won't have them.

**Localized sites.**

Include the locale in the slug (`/og/en/<slug>.jpg`, `/og/nl/<slug>.jpg`) and resolve per-locale strings (site name, tagline) inside the route. If the primary font doesn't cover the target language, add a locale-appropriate fallback font to the `fonts` array before rendering.

**Minimal satori route sketch:**

```ts
// src/pages/og/[...slug].jpg.ts
import satori from 'satori';
import sharp from 'sharp';
import fs from 'node:fs';
import { getCollection } from 'astro:content';

const font = fs.readFileSync('src/fonts/Inter-Bold.woff2');

export async function getStaticPaths() {
    const posts = await getCollection('blog');
    return posts.map((post) => ({ params: { slug: post.slug }, props: { post } }));
}

export async function GET({ props }) {
    const svg = await satori(
        {
            type: 'div',
            props: {
                style: { /* flex, padding, colors, etc. */ },
                children: [/* title + subtitle nodes */],
            },
        },
        { width: 1200, height: 675, fonts: [{ name: 'Inter', data: font, weight: 700, style: 'normal' }] }
    );
    const jpg = await sharp(Buffer.from(svg)).jpeg({ quality: 90 }).toBuffer();
    return new Response(jpg, { headers: { 'Content-Type': 'image/jpeg' } });
}
```

Wire the URL into `<Seo>` as the `openGraph.image` value.

**If the project already has an OG route,** verify: output is 1200×675 JPEG (not WebP/AVIF/PNG — social platforms don't all support those), the URL is deterministic from the slug, and the route runs at build time (not SSR on request — that's a per-crawl cost).

## Schema endpoints and schema map

Each endpoint collects every entry in a content collection, builds the JSON-LD graph per entry, and serves the combined result as `application/ld+json`. Don't hand-write the mapper — the full implementation with entity builders (`buildWebPage`, `buildArticle`, etc.) and their expected arguments is documented in the [`astro-seo-graph` schema endpoints docs](https://github.com/jdevalk/seo-graph/tree/main/packages/astro-seo-graph#schema-endpoints). Copy from there. Then add `/schemamap.xml` listing every endpoint, and a `Schemamap:` directive in `robots.txt`.

## `llms.txt`

Pass an options object to `llmsTxt` on the `seoGraph()` integration (requires `@jdevalk/astro-seo-graph` ≥ 0.9.0). Required fields: `title` (the H1 for the file) and `siteUrl` (used to resolve crawled HTML paths). Optional: `summary` (rendered as a blockquote), `details` (extra paragraphs), `sections` (user-supplied sections; when given, no pages are auto-collected), `filter` / `autoSectionName` / `outputPath` to tune the auto-generated output. For rendering outside the integration hook, import `renderLlmsTxt` from the package.

## Markdown alternates

Serve clean markdown copies of every page at a parallel `.md` URL for AI agents (Claude, ChatGPT, Perplexity, Cloudflare's crawlers) to consume without HTML parsing. Requires `@jdevalk/astro-seo-graph` ≥ 1.2.0. Two pieces:

1. **The route.** Create `src/pages/[...slug].md.ts` (or whatever path shape you need) and export `createMarkdownEndpoint`. It serves a YAML frontmatter block (title, canonical, pubDate, updatedDate, author, description, tags, categories) followed by the markdown body, with `Content-Type: text/markdown; charset=utf-8`, `X-Robots-Tag: noindex, follow`, `X-Markdown-Tokens: <n>`, and a `Link: <canonical>; rel="canonical"` header pointing crawlers back at the HTML. Token count defaults to `chars/4`; swap in `gpt-tokenizer` or `@anthropic-ai/tokenizer` via `estimateTokens` for accuracy.
2. **The discovery link.** Set `markdownAlternate: true` on the `seoGraph()` integration (see the integration config above). `<Seo>` will emit `<link rel="alternate" type="text/markdown" href="…">` on every page, derived from the canonical (`/blog/post/` → `/blog/post.md`). **Only turn this on after the route is wired** at the matching path — otherwise the link 404s.

**Content negotiation on a static host.** On Cloudflare Pages, add a Transform Rule that rewrites `Accept: text/markdown` requests to the `.md` path and responds with `Vary: Accept`, so the same URL serves HTML or markdown based on the client. No SSR or middleware. The `astro-seo-graph` README has the exact rule config; copy from there.

For rendering outside the route, import `renderMarkdownAlternate` — pure renderer, same frontmatter + body + token-count output.

## RSS feed

If no feed exists, add `@astrojs/rss`:

```sh
npm install @astrojs/rss
```

Create `src/pages/feed.xml.ts` that pulls the blog collection and renders full post bodies (not excerpts) — truncated feeds frustrate readers and give AI agents less to work with. Advertise the feed in the `<Seo>` component's `extraLinks` with `rel="alternate"` and `type="application/rss+xml"`.

## Redirects and FuzzyRedirect

Seeding `_redirects` from scratch is the unpleasant part. Practical approach:

- If migrating from WordPress or another CMS, export the old URL list from the source (WP-CLI `wp post list`, database dump, or the old sitemap via Wayback Machine).
- Diff old URLs against the current sitemap; every URL in the old set not in the new set needs a redirect entry.
- Commit the table once, maintain it going forward whenever you change a slug.

Syntax depends on the host:

- **Cloudflare Pages / Netlify:** `public/_redirects` — `/old-path /new-path 301` per line.
- **Vercel:** `vercel.json` with a `redirects` array.
- **Other hosts:** server config (nginx, Apache, etc.).

Then add `<FuzzyRedirect>` to the 404 page. Confirm the 404 page returns a 404 status, not 200 — platform-specific behavior, check the deployed response.

## Performance headers

Syntax depends on the host. Pick the one matching Phase 0's detected deployment target.

**Cloudflare Pages / Netlify** — `public/_headers`:

```text
/_astro/*
  Cache-Control: public, max-age=31536000, immutable

/*
  No-Vary-Search: key-order, params=("utm_source" "utm_medium" "utm_campaign" "utm_content" "utm_term")
```

**Vercel** — `vercel.json`:

```json
{
    "headers": [
        {
            "source": "/_astro/(.*)",
            "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
        },
        {
            "source": "/(.*)",
            "headers": [{ "key": "No-Vary-Search", "value": "key-order, params=(\"utm_source\" \"utm_medium\" \"utm_campaign\" \"utm_content\" \"utm_term\")" }]
        }
    ]
}
```

**Other hosts** — configure equivalents in server config; syntax varies.

## Broken link checker in CI

Add a [lychee](https://github.com/lycheeverse/lychee-action) workflow at `.github/workflows/link-check.yml`:

```yaml
name: Link Check
on:
  push:
    paths:
      - 'src/content/**'
      - 'src/pages/**'
      - '*.md'
  schedule:
    - cron: '0 9 * * 1'  # Weekly, Mondays 09:00 UTC — catches link rot
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lycheeverse/lychee-action@v2
        with:
          args: --no-progress './**/*.md' './**/*.astro' './**/*.mdx'
          fail: true
```

Push-triggered runs block broken links from shipping. The weekly run catches external link rot.
