# agent-skills

Portable Agent Skills catalog for:

- GitHub Copilot
- Pi
- OpenAI Codex
- Gemini CLI

The catalog source of truth lives in this repository under `skills/`.
Each skill directory contains the portable `SKILL.md`, any support files under `references/`, `assets/`, or `scripts/`, and harness-specific metadata where needed.

For a task-oriented chooser, start with [`skills/README.md`](skills/README.md).

## Layout

```text
agent-skills/
├── package.json
├── README.md
├── _shared/        # local validation and eval tooling
├── scripts/        # helper scripts for linking and validation
└── skills/         # portable Agent Skills catalog
```

## Install locally for all supported harnesses

The most portable local setup is to expose this repo through `~/.agents/skills`.

From the repo root:

```bash
npm run link:user
```

That script will:

- create `~/.agents/skills -> <repo>/skills`
- create `~/.copilot/skills -> <repo>/skills` for Copilot compatibility
- move any existing non-symlink directory at those paths aside as `*.pre-agent-skills-<timestamp>` before linking

Codex and Gemini CLI both understand `~/.agents/skills`, and Pi can use either the shared `.agents` path or the Pi package manifest in this repo.

## Tool-specific notes

### GitHub Copilot

Supported locations include:

- `~/.agents/skills`
- `~/.copilot/skills`
- repo `.agents/skills`
- repo `.github/skills`

This repo's link script sets up both user-level paths for convenience.

### Pi

Pi can use this repo directly as a package:

```bash
pi install /absolute/path/to/agent-skills
```

For example, from any cloned checkout:

```bash
pi install "$(pwd)"
```

Because `package.json` declares:

```json
{
  "pi": { "skills": ["./skills"] }
}
```

Pi will discover the catalog as a package.

### Codex

Codex reads skills directly from:

- `$HOME/.agents/skills`
- repo `.agents/skills`

So the shared symlink setup is enough.

This catalog also includes Codex-specific UI metadata in `skills/*/agents/openai.yaml` for every active skill. Those files provide display names, short descriptions, and implicit-invocation policy for the Codex app and related surfaces.

### Gemini CLI

Gemini CLI reads skills from:

- `~/.agents/skills`
- `~/.gemini/skills`
- repo `.agents/skills`

The shared `~/.agents/skills` path is the recommended interoperable location.

## Browse and maintain the catalog

- Use [`skills/README.md`](skills/README.md) to choose the right skill for a task.
- Read `skills/<name>/SKILL.md` for the workflow, boundaries, and support-file references for a specific skill.
- Use the `skill-creator` skill when adding a new catalog entry or upgrading an existing one.

## Validate the catalog

From the repo root:

```bash
npm run validate
```

Or directly:

```bash
python _shared/validate-skills.py skills
```

## Release automation

This repo uses Release Please via the shared workflow in `matt-riley-ci`.

- the root package `@matt-riley/agent-skills` is one releasable component
- each `skills/<name>` directory is also a separate releasable component with its own version
- skill versions are tracked in `.release-please-manifest.json` and mirrored into `SKILL.md` frontmatter at `metadata.version`
- the `# x-release-please-version` marker on each skill version line lets Release Please update the frontmatter automatically
- version bumps still follow conventional commits, so `feat:` and `fix:` messages on a skill path drive that skill's next release
- only the root npm package is published, and it is published to GitHub Packages when a root release is created

When adding a new skill, add both:

1. a `metadata.version` line in `skills/<name>/SKILL.md`
2. matching entries in `release-please-config.json` and `.release-please-manifest.json`

## License

This repository is licensed under GNU GPL v3. See `LICENSE`.

## Notes on portability

This repo keeps `SKILL.md` files portable by:

- preferring Agent Skills-compatible wording over harness-specific wording
- avoiding hard-coded install paths inside active skills
- keeping harness-specific installation and packaging details in this repo README instead of the skills themselves

Some skills still depend on environment-specific capabilities, for example:

- `session-store-history` needs a read-only `sql` tool and a `session_store`-style database
- Cloudflare D1 skills assume Wrangler and Workers repositories

Those assumptions are captured in each skill's `compatibility` field rather than hidden in the workflow.
