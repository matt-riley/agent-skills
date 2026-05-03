# Workflow contract checklist

Use this checklist before treating a `v1` artifact as ready to hand off.

## Template and version

- The correct template was chosen for the phase.
- `contract_version` is `v1`.
- `contract_type` matches the template.

## Required structure

- All shared frontmatter keys are present.
- All contract-specific frontmatter keys are present.
- All required headings from `contract-spec.md` are present.
- No ad hoc replacement field names were introduced.

## Content quality

- The status is explicit.
- The status value is valid for the chosen contract type.
- Commands, evidence, or blockers are concrete enough for the next phase to act on.
- The artifact is short enough to scan quickly.
- The next action is explicit.

## Migration discipline

- If the source material was legacy prose, the needed information was mapped into the `v1` headings.
- The artifact does not introduce a third format or hidden extra requirements.
