# gitleaks triage patterns

Apply these disposition rules consistently across findings.

## Disposition categories

| Category | Criteria | Required action |
| --- | --- | --- |
| Confirmed secret | Real credential/token/private key pattern with plausible sensitivity | Revoke or rotate externally, remove from repo surface/history per policy |
| Probable secret | High-confidence pattern but sensitivity not yet confirmed | Treat as real until disproven; contain first, then verify ownership |
| Probable false positive | Synthetic fixture or non-sensitive test data with clear evidence | Add narrow allowlist with documented rationale |

## Command stability

- Reproduce with the same `gitleaks` command and config each run.
- Keep output artifacts for reviewer traceability.
- Avoid broad suppressions that hide future true positives.
