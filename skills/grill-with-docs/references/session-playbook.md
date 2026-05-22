# Session playbook

Lightweight patterns for running an effective interrogation session. These apply to both `grill-me` and `grill-with-docs`, though the doc-maintenance steps are specific to `grill-with-docs`.

## Question sequencing

- **Resolve foundational terms first.** If the plan mentions "orders" and "invoices", clarify what each means before asking how they interact. Dependent decisions cannot be resolved before the concepts they depend on.
- **Walk one branch at a time.** Do not jump between unrelated decision branches. Finish one line of questioning before starting the next.
- **Provide your recommended answer.** Every question should include your best guess at the answer. This gives the user something concrete to react to, which is faster than open-ended questions.

## Scenario construction

- **Invent specific scenarios that probe edge cases.** Do not accept abstract descriptions of how things work — force the user to walk through a concrete example.
- **Pick scenarios that stress concept boundaries.** If the user says "a Customer can cancel an Order", ask: "Customer A places Order 1 with three line items, then cancels one. Is that a partial cancellation of the Order, or a cancellation of a line item? Are those different things?"
- **Use the user's own domain language.** If CONTEXT.md defines terms, use those exact terms in scenarios. Avoid inventing synonyms.

## Contradiction surfacing

- **Cross-reference claims against code.** When the user states how something works, verify it. If the code disagrees, surface the contradiction diplomatically: "Your code does X, but you just said Y — which is the intended behaviour?"
- **Cross-reference claims against existing docs.** If CONTEXT.md or an ADR contradicts what the user just said, call it out: "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"
- **Do not assume the code is right.** The code might be a bug. The point is to force the user to decide which is the source of truth.

## Fuzzy-term resolution

- **Catch overloaded terms immediately.** If the user says "account" and it could mean Customer, User, or BillingAccount, propose a canonical term and ask which they mean.
- **When a term is resolved, update CONTEXT.md immediately** (grill-with-docs only). Do not wait for the session to end. Inline updates ensure nothing is lost.
- **List rejected aliases under _Avoid_.** This prevents future drift back to ambiguous terms.

## When to explore instead of ask

- If the question is "how does X currently work?", explore the codebase instead of asking the user.
- If the question is "should X work this way?", ask the user — that is a design decision, not a fact about the current state.
- When in doubt, check the code first and present what you found, then ask whether the current behaviour is intended.

## When to stop

The session is complete when:
- Every branch of the decision tree has been resolved.
- The user confirms they have a shared understanding of the plan.
- All resolved terms are captured in CONTEXT.md (grill-with-docs only).
- Any qualifying decisions have been offered as ADRs (grill-with-docs only).
