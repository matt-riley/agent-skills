# Type test scenarios

Use this reference when choosing the lightest durable type-test shape.

## Prefer inline assertions when

- the contract is one helper, alias, or inference edge
- the repository's nearest existing type test uses inline assertions
- the check can live next to the public surface without setup noise
- the first pass is one positive case and one negative case

## Prefer fixtures or bootstrap when

- the case depends on multiple files, package resolution, or ambient setup
- the repository needs a dedicated compile command or directory pattern
- repeated setup would make inline assertions harder to read
- the regression is about a tool boundary, not just one exported helper

## Scenario checklist

| Scenario | Preferred shape | Keep it small by... |
| --- | --- | --- |
| One exported helper with a narrow inference bug | inline assertions | assert the exact happy path and one failure mode |
| Public type alias or generic contract | inline assertions | compare the minimum shape that proves assignability |
| Several related cases sharing setup | fixture or bootstrap | centralize setup once and keep cases table-driven |
| No existing type-test convention | lightweight fixture bootstrap | reuse the nearest existing typecheck command first |
| Regression depends on path or package resolution | fixture or bootstrap | encode the resolution shape, not unrelated runtime behavior |

## Do-not-widen cases

- Do not add runtime tests just because the type check is awkward.
- Do not introduce a new assertion library if the repository already has a working pattern.
- Do not broaden the file until the first positive and negative cases are stable.
- Do not turn a focused type regression into a full API rewrite.

## Maintenance loop

- If the repository's type-test convention changes, update this file before broadening examples.
- If a new pattern becomes the local default, reflect it in `SKILL.md` and keep the checklist aligned.
