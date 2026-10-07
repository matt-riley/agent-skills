# Reviewer prompt templates

Use these when the user asks for implementation review, named reviewer models, or unanimous approval before changes are considered done. Run the Standards and Spec reviewers separately (in parallel when the harness supports subagents) and report their findings under separate headings. Do not merge or re-rank across the two.

When you pick the reviewer model yourself, prefer a different model family from the one that wrote the change.

## Shared context block

```text
Context:
- Repo: <repo>
- User goal: <goal>
- Constraints: <constraints>
- Review target: <branch / PR / commit / diff command>
- Validation status: <tests, build, lint, manual checks>
- Approval rule: all required reviewers participate in every round; the implementation is not final until every required reviewer approves

Return exactly:
1. Verdict: APPROVE or REQUEST_CHANGES
2. Required changes, each as `path:line — severity — finding`
3. Optional suggestions
4. Approval rationale

Focus on materially important issues. Do not edit files.
```

## Standards reviewer

```text
Review the diff against this repo's documented standards: <list of standards files>.
(a) Each place the diff violates a documented standard: cite the file and rule. These can be hard violations.
(b) Any baseline smell below that you spot: name it as "possible <smell>" and quote the hunk. These are always judgement calls, never blockers on their own.
A documented repo standard overrides the baseline. Skip anything tooling (lint, formatter, type checker) already enforces.

Smell baseline:
- Mysterious Name: name does not reveal what it does or holds.
- Duplicated Code: same logic shape in more than one hunk or file.
- Feature Envy: code reaches into another object's data more than its own.
- Data Clumps: the same fields or params keep travelling together.
- Primitive Obsession: a primitive stands in for a domain concept.
- Repeated Switches: the same switch/if-cascade recurs across the change.
- Shotgun Surgery: one logical change forces scattered edits.
- Speculative Generality: hooks, params, or abstraction the spec does not need.
- Middle Man: a function or class that mostly delegates onward.

<shared context block>
```

## Spec reviewer

```text
Review the diff against the originating spec: <issue / plan / PR description path or contents>.
Report, quoting the spec line for each:
(a) requirements missing or only partly implemented;
(b) behaviour in the diff nobody asked for (scope creep);
(c) requirements that look implemented but where the implementation looks wrong.
If no spec exists, return "no spec available" and skip.

<shared context block>
```

## Blast-radius check

The orchestrator owns this, not a reviewer. Name the one fact the change is safe because of, look past the diff for what a symbol search will not show (wire formats, persisted data, flags, other readers of the same bytes), then record how far the fact got:

1. asserted
2. pointed at a real `file:line`
3. walked the bad case and showed it cannot happen
4. ran a script or test that exercises the real code

Anything short of 4 is reported as **unproven**.

## Consolidation rules

- Treat `REQUEST_CHANGES` as blocking.
- Merge duplicate findings within an axis, never across Standards and Spec.
- Preserve reviewer-specific concerns when they are materially different.
- After revising the implementation, send the updated revision back to the full reviewer set.
