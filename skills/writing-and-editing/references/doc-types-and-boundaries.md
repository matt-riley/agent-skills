# Document types and boundaries

Use this file when the task sounds like writing work but the routing is ambiguous.

## Draft mode owns

- proposals
- technical specs and design docs
- RFCs
- READMEs
- decision docs / ADRs
- migration guides
- onboarding docs
- runbooks

## Route elsewhere when

| Task | Route to | Why |
| --- | --- | --- |
| Implementation plan, rollout plan, or reviewer-gated plan | `plan-review` | Planning is the deliverable |
| Repo-grounded execution brief, rewritten prompt, or contract-shaped prompt | `reverse-prompt` | The output is for execution, not a reader-facing document |
| GitHub profile or repo presentation audit | `github-presence` | The task is broader than the writing itself |
| Code, config, or generated-file changes | specialist engineering skill | The output is not a writing deliverable |

## Internal split inside writing-and-editing

| If the user wants... | Use mode... |
| --- | --- |
| A document created or restructured | `draft` |
| An audit of multi-paragraph prose | `readability-audit` |
| A review of titles, descriptions, bios, or other short strings | `metadata-audit` |

## Sequencing rules

- Draft first, then readability review.
- Review metadata strings in batches after the relevant fields exist.
- Do not broaden a metadata audit into a full document rewrite unless the user asks.
