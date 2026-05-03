---
name: github-profile
description: Audit and improve GitHub profile pages, including profile README content, metadata fields, pinned repositories, profile widgets, and public profile presentation.
---

# GitHub profile

## Use this skill when

- The user wants to improve, create, review, or optimize a GitHub profile.
- The task mentions a profile README, bio, pinned repositories, GitHub stats widgets, contribution graph, or overall GitHub presence.
- The goal is to make a personal or organization profile more credible, scannable, or conversion-oriented for recruiters, collaborators, contributors, or customers.

## Do not use this skill when

- The main task is improving a repository rather than the account or organization profile page. Use [`github-repo`](../github-repo/SKILL.md).
- The main task is reviewing only a short bio, tagline, or pinned-repo description. Use [`metadata-check`](../metadata-check/SKILL.md).
- The main task is readability review on an already written profile README. Use [`readability-check`](../readability-check/SKILL.md).
- The user wants GitHub account administration outside the profile surface, such as permissions or billing.

## Inputs to gather

**Required before editing**

- Whether this is a personal profile or an organization profile.
- The username or org name, target audience, tone, and what the profile should optimize for.
- Current profile metadata, current README state, and existing pinned repositories.
- The strongest projects, technologies, and proof points worth surfacing.

**Helpful if present**

- GitHub API access through `gh` for pulling current bio, repos, and README state.
- Existing social links, personal website, and other profiles that should cross-link.
- Whether the user wants dynamic widgets, activity feeds, or a lightweight static README.

**Only investigate if encountered**

- Magic-repo existence (`username/username`) for personal profiles.
- Organization-specific details such as `.github/profile/README.md`, member-only profile content, or org-level visibility constraints.

## First move

1. Determine whether the target is a personal or organization profile because the file locations and available surfaces differ.
2. Collect the user's goals, audience, and strongest proof points before writing any README copy.
3. Audit the current profile state so recommendations are grounded in what is actually missing or weak.

## Workflow

1. Gather profile context: identity, audience, goals, tone, strongest repositories, and current GitHub metadata.
2. Audit the current profile surface:
   - README presence and structure
   - metadata quality (bio, company, location, links, status)
   - pinned repository strategy
   - contribution and public-activity signals
3. Generate or improve the profile README using `AGENTS.md` for concrete implementation patterns.
4. Recommend precise metadata and pinned-repo changes, not just vague best practices.
5. Run [`metadata-check`](../metadata-check/SKILL.md) on any GitHub bio or short metadata strings you wrote.
6. Run [`readability-check`](../readability-check/SKILL.md) on the README body when you generated substantial prose.

## Guardrails

- **Must not** treat personal and organization profiles as interchangeable; their file paths and profile surfaces differ.
- **Must not** optimize the profile around generic template filler when the user's real work and goals provide better proof points.
- **Must not** overload the page with too many widgets, badges, or decorative sections that bury the main story.
- **Must not** recommend pinned repositories blindly; tie each recommendation to the user's goals and actual project quality.
- **Should** make the profile scannable in a few seconds, with the strongest signal near the top.
- **Should** keep recommendations concrete: exact bio text, which repos to pin, and what metadata to fill in.
- **Should** mention when a weak pinned repository also needs repository-level cleanup via [`github-repo`](../github-repo/SKILL.md).

## Validation

- Check that the README structure fits the profile type and renders cleanly in GitHub-flavored Markdown.
- Verify widget URLs, badge URLs, usernames, and links.
- Confirm that generated recommendations stay within GitHub surface limits, especially bio length and profile-card readability.

## Examples

- "Make my GitHub profile look professional."
- "Create a profile README for recruiters."
- "Help me improve my pinned repos and GitHub bio."
- "Set up our organization profile page."

## Reference files

- `AGENTS.md` - concrete templates and implementation guidance for personal and organization profile surfaces
