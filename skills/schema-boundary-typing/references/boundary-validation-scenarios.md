# Boundary validation scenarios

Use these scenarios to verify that the boundary accepts good data, rejects bad data in the repository's expected shape, and keeps the validated type honest.

| Scenario | Success expectation | Failure expectation | Maintenance note |
| --- | --- | --- | --- |
| Valid request or payload shape | Validation succeeds once at the edge and returns the typed value inward | N/A | Update when the boundary shape or schema library changes |
| Invalid field value | The valid path stays unchanged and downstream code receives only the validated type | Field-level errors or the repo's chosen result object reflect the bad field | Keep the failure shape examples aligned with the current validator |
| Malformed JSON or unusable storage record | The parser/guard rejects the payload before consumers see it | Boundary failure is surfaced through the repo's existing error convention | Adjust this row if the repo changes from throw to result-object handling |
| Transport shape differs from domain model | The transport schema validates first, then maps into a separate domain type | Invalid transport data is rejected before mapping happens | Keep mapping explicit so this row stays cheap to maintain |
| Reused boundary across multiple callers | The schema or guard is shared and derived types stay in sync | Callers do not re-parse or cast the same payload again | Refresh when a boundary starts being duplicated in multiple places |

## Checklist

- Validate once at the first untrusted edge.
- Confirm the success path returns the derived or guarded type.
- Confirm invalid input produces the repo's expected error shape.
- Confirm downstream code consumes the validated value instead of re-checking it.
