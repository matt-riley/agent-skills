# GitHub presence — implementation recipes

Read this file when the audit already identified the target surface and you need concrete generation patterns.

## Profile surfaces

### Personal profile README

Create the `username/username` repository `README.md`.

Recommended structure:

```markdown
# Hi, I'm [Name]

[One-line hook about what you do and what you care about.]

## What I'm working on
[Current focus areas or projects.]

## Tech stack
[Badges or a concise stack summary.]

## Featured projects
[2-3 strongest projects with links and one-line descriptions.]

## Connect with me
[Email, website, LinkedIn, blog, or other relevant links.]
```

Guidelines:
- Optimize for quick scanning, not maximal badge density.
- Use pinned repositories to reinforce the README story instead of repeating everything in prose.
- Only add stats widgets if they strengthen the profile instead of adding noise.

### Organization profile README

Create `.github/profile/README.md` in the org's `.github` repository.

Focus on:
- what the organization does
- key products or repositories
- how contributors or candidates should engage
- contact, community, or hiring links

## Repository surfaces

### README generation

When writing or rewriting a repository README:
- start with the project name and a clear one-liner
- add the fastest possible getting-started path
- keep examples copy-pasteable
- recommend a screenshot or GIF when the project has a visual component
- keep advanced content below the core onboarding path

### Community health files

Generate only the files the repository actually needs.

Common candidates:
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`
- issue templates
- PR template
- `CODEOWNERS`

Tailor them to the stack and workflow already used by the project.

## Org-wide defaults

If the task is organization-wide rather than repo-local:
- create or update the shared `.github` repository
- keep org defaults generic enough to apply across repositories
- remember that repo-local issue templates override org defaults for that repository

## Writing follow-up

If the generated bio, tagline, repo description, or README prose needs a dedicated copy pass, route that follow-up through `writing-and-editing` instead of duplicating the writing audit rules here.
