# Rewrite mode scenarios

Use these scenarios to keep mode selection honest and to make blocker routing obvious.

| Scenario | Correct mode | Expected move |
| --- | --- | --- |
| User asks, "Improve this prompt only: fix the broken workflow in `ci.yml`." | `rewrite-and-return` | Return the sharpened prompt and stop before doing the workflow work. |
| User asks, "Before you start, sharpen my prompt and then implement it." | `rewrite-and-proceed` | Rewrite the brief internally and continue into the requested phase. |
| User asks to change code, not the wording of the request. | do not use this skill | Skip reverse-prompt and go straight to the requested work. |
| The target file, directory, or repo surface is missing and cannot be inferred safely. | blocked | Surface the missing target instead of inventing one. |
| The request mixes prompt help with a broad policy or always-on automation idea. | blocked / hand off | Keep the skill reusable and route stateful orchestration elsewhere. |
| The rewritten prompt would need a different next phase than the user implied. | `rewrite-and-return` | Return the better brief plus the recommended next phase instead of guessing. |

## Maintenance loop

- Update this file whenever the mode-selection rules or blocker thresholds change.
- If a new rewrite pattern becomes common, add one row here before expanding the top-level skill text.
