# Slicing guide

Use this guide when breaking plans or PRDs into issue-tracker work.

## Tracer-bullet vertical slices

A good slice is a thin end-to-end path through the system that proves value or behavior, not a thick horizontal chunk from one layer.

### Good slice properties

- Covers the needed layers to deliver one narrow capability.
- Can be demoed, tested, or otherwise verified on its own.
- Has a clear acceptance boundary.
- Can be assigned independently, even if it depends on a prior blocker slice.

## Anti-patterns

Avoid these horizontal or ambiguous breakdowns:

- "Database changes"
- "API work"
- "Frontend implementation"
- "Write tests"
- "Refactor auth module"

These describe layers or vague activity, not independently grabbable behavior.

## Better slice examples

- "Add retry-state persistence and expose it in the existing admin status view"
- "Allow one offline draft to sync successfully after reconnect, with conflict messaging for stale revisions"
- "Support the first billing retry notification from failed payment through visible account status"

Each of these implies cross-layer work but stays narrow enough to verify.

## `AFK` vs `HITL`

### Mark a slice `AFK` when

- It can be implemented, reviewed, and merged without a human decision outside the normal coding workflow.
- The acceptance criteria are concrete and already understood.
- No unresolved design or policy choice blocks implementation.

### Mark a slice `HITL` when

- It requires a design review, architecture decision, stakeholder sign-off, or other explicit human checkpoint.
- The acceptance criteria depend on a choice not yet made.
- The slice is primarily about resolving uncertainty rather than shipping a capability.

Prefer `AFK` unless the slice truly needs human interaction.

## Dependency heuristics

- Block only on slices that must land first for the next slice to be real.
- Prefer shallow dependency chains over wide blocker graphs.
- Publish blocker slices first so later issue bodies can reference real tracker IDs.
- If two slices can be parallelized after a thin enabling slice, keep them separate.
