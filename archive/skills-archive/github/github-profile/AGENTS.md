# GitHub Profile — Implementation recipes

Detailed code recipes for Phase 2 (Generate the Profile README). Read this file when you need to implement a specific fix flagged by the audit. The parent `SKILL.md` has the workflow and audit checklist.

## Personal profile README template

Create the `username/username` repo's `README.md`. The structure below is a starting point — adapt it to the person's tone and goals. A creative developer might want something playful. A startup founder might want something that signals credibility. A junior developer might emphasize learning and growth. Don't be afraid to deviate — personality matters more than structure.

```markdown
# Hi, I'm [Name] [optional wave emoji]

[One-liner about what you do and what drives you. This is the hook.]

## What I'm working on

[2-3 sentences about current projects, company, or focus areas.]

## Tech stack

[Badges using shields.io, e.g.:]
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)

## GitHub stats

[Stats cards — see widget section below]

## Featured projects

[Brief descriptions of 2-3 key projects with links, if they want to highlight beyond pins]

## Connect with me

[Badge-style links to email, Twitter/X, LinkedIn, blog]
```

## Stats widgets

Pick the ones that make sense for the person. Don't overload — 2-3 widgets is usually right.

### github-readme-stats (anuraghazra)

The most popular option with 78,000+ stars:

```markdown
![GitHub Stats](https://github-readme-stats.vercel.app/api?username={username}&show_icons=true&theme={theme})
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={username}&layout=compact&theme={theme})
```

Over 30 themes available. Can be self-hosted on Vercel to avoid rate limits.

### github-readme-streak-stats (DenverCoder1)

Contribution streaks:

```markdown
![GitHub Streak](https://streak-stats.demolab.com/?user={username}&theme={theme})
```

### github-profile-trophy (ryo-ma)

Trophy icons:

```markdown
![Trophies](https://github-profile-trophy.vercel.app/?username={username}&theme={theme}&no-frame=true&row=1)
```

## Badges for tech stack and social links

Use **shields.io** combined with **Simple Icons** (3,000+ brand logos):

```text
https://img.shields.io/badge/-{Label}-{Color}?style={style}&logo={logo}&logoColor=white
```

Styles: `flat`, `flat-square`, `plastic`, `for-the-badge`, `social`

For social links, wrap badges in links:

```markdown
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/{handle})
[![Twitter](https://img.shields.io/badge/-Twitter-1DA1F2?style=flat-square&logo=twitter&logoColor=white)](https://twitter.com/{handle})
```

## Dynamic auto-updating content

Optional — requires GitHub Actions. If the person blogs or creates content, suggest these:

- **blog-post-workflow** (gautamkrishnar) — Auto-pulls latest posts from RSS feeds into the README. Uses HTML comment placeholders. Needs a scheduled GitHub Action (daily cron).
- **waka-readme-stats** — Coding time metrics from WakaTime.

Remind them: GitHub stops cron triggers after 60 days of repo inactivity. The blog-post-workflow includes a keepalive feature; others may not.

## Organization profile README

Create `.github/profile/README.md` in the org's `.github` repo.

Organization profile READMEs should be more structured and less personal:

- What the organization does
- Key products or projects (with links to repos)
- How to get involved (contributing, jobs, community)
- Contact and social links

Optionally, create a `.github-private/profile/README.md` for member-only content:

- Internal resources and onboarding links
- Private repo directory
- Team information

Remind the user to **verify their organization's domain** (Settings → Verified & approved domains) for the verified badge.

## Profile generators

If the user wants a faster path, mention these tools:

- **GPRM** (gprm.itsvg.in) — No-code generator with 300+ tech icons
- **rahuldkjain's generator** — Popular fill-in-the-blanks tool
- **readme.so** — Drag-and-drop editor for both profile and project READMEs

Recommendation: start with a generator, then customize to add personality and remove boilerplate.
