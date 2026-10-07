# Stage 3: Reader Testing

**Goal:** Test the document with a fresh perspective to catch blind spots — things that make sense to the authors but confuse or mislead readers. This stage verifies the document actually works for its intended audience before publication or handoff.

## Why Reader Testing Matters

Authors become **context-saturated**: after working on a document for hours, you know the background, the decisions, the rationale, and the unstated assumptions so well that they feel obvious. You may skip explanations that readers need, gloss over ambiguities, or make logical jumps that are only clear in your head.

A **fresh reader** — someone without your context — catches these blind spots immediately. They will:
- Ask "What does this term mean?" when you thought it was obvious
- Notice logical gaps or unsupported claims
- Find contradictions between sections you wrote at different times
- Spot generic filler sentences that don't carry weight
- Identify places where the doc assumes knowledge the audience doesn't have

**By testing before others read it**, you fix these issues in a low-stakes environment instead of discovering them during actual publication, board meetings, or customer reviews.

---

## Predicting Reader Questions

Before testing, brainstorm what questions readers would realistically ask when encountering your document. These are questions that would lead them to paste the doc into Claude or ask a colleague "What does this mean?"

### How to Generate Predictions

Based on the document content, audience, and context from Stage 1, predict **5–10 realistic reader questions**. Think about:

- **Clarification questions** — "What exactly is X?" or "How is X different from Y?"
- **Evidence questions** — "Why should we believe this?" or "Where's the proof?"
- **Feasibility questions** — "Can this actually work?" or "What's the risk?"
- **Scope questions** — "Does this apply to us?" or "What's not included?"
- **Next-step questions** — "What happens after this?" or "Who does X?"
- **Assumption questions** — "What's this doc assuming about readers?"

### Example: Predicting Reader Questions for a Proposal

If your doc is a proposal to migrate to a new database, readers might ask:

1. "What's wrong with our current database?"
2. "Why this specific new database over alternatives like [X] and [Y]?"
3. "What's the migration timeline and will it affect production?"
4. "Who will do this work and how long will it take?"
5. "What happens to existing data during migration?"
6. "If this is such a good idea, why haven't we done it before?"
7. "What's the cost, and does it fit our budget?"
8. "How will this impact performance?"
9. "What's the rollback plan if something goes wrong?"
10. "When do we need to decide on this?"

These questions guide your testing approach.

---

## Testing Approaches

### Approach 1: Testing with Sub-Agent Access

If you have access to sub-agents (e.g., any LLM-based agent harness that supports spawning sub-instances), you can perform reader testing directly without user involvement.

**Step 1: Invoke Sub-Agent with Document Only**

For each predicted reader question, invoke a fresh sub-agent with:
- **Only the document content** (no conversation context)
- **Only the specific reader question**
- Instructions to answer the question and note any ambiguities

The sub-agent acts as a fresh reader who has not been part of the document development.

**Step 2: Summarize Results**

For each question, record:
- **What Reader Claude got right** — The correct answer to the question
- **What Reader Claude got wrong or misinterpreted** — Places where the doc caused confusion
- **Ambiguities or unclear language** — Terms or phrasing that tripped up the reader
- **Missing context** — Knowledge the doc assumes readers have but may not

### Approach 2: Testing Without Sub-Agent Access (Manual)

If you don't have sub-agent access (e.g., on Claude.ai web interface), the user performs the testing manually.

**Step 1: Provide Testing Instructions to User**

Provide clear instructions for manual testing:

1. **Open a fresh Claude conversation:** https://claude.ai (or use a separate session/workspace)
2. **Share the document:**
   - If using a shared doc platform with connectors enabled: Provide the link directly
   - Otherwise: Paste the document content into the new conversation
3. **Test each predicted reader question:**
   - Ask Reader Claude the question
   - Have Reader Claude provide the answer, note any ambiguities, and describe what context/assumptions the doc appears to make

For each question, ask Reader Claude to respond with:
- The answer to the question
- Whether anything was ambiguous or unclear
- What prior knowledge or context the doc assumes readers already have

**Step 2: Additional Checks**

Ask Reader Claude to check for:
- **Ambiguity:** "What terms or phrasing in this doc might be ambiguous or unclear?"
- **Assumptions:** "What knowledge or context does this doc assume readers already have?"
- **Contradictions:** "Are there any internal contradictions or inconsistencies?"
- **Generic filler:** "Are there sentences that don't carry weight or could be cut?"

**Step 3: Report Back**

The user reports what Reader Claude got right, wrong, or struggled with. You then decide which sections need refinement.

---

## Testing Procedure

### For Each Question

1. **Invoke the reader (sub-agent or manual process)** with the document and question
2. **Record the response** — What did the reader say? Did they get it right?
3. **Note gaps** — What was ambiguous, misinterpreted, or missing?
4. **Categorize the issue:**
   - **Clarity issue** — Reader didn't understand the explanation
   - **Evidence issue** — Reader questioned whether the claim is supported
   - **Assumption issue** — Reader didn't have the assumed context
   - **Scope issue** — Reader was confused about what's included/excluded
   - **Contradiction** — Reader noticed an internal inconsistency

### Summary Template

After testing each question, capture:

| Question | Reader's Answer | Got It Right? | Issues Found |
|----------|-----------------|---------------|----|
| "What's wrong with X?" | [Answer] | ✓ or ✗ | Clarity: assumed knowledge of Y |
| "Why this approach?" | [Answer] | ✓ or ✗ | Evidence: no justification for alternative |
| ... | ... | ... | ... |

---

## Additional Validation Checks

Beyond predicted questions, run these checks to catch blind spots:

### 1. Ambiguity Check

**Explicit and actionable — Reader Claude should identify:**

- **Undefined terms:** Are there technical terms, acronyms, or domain-specific jargon that aren't defined?
- **Vague pronouncements:** Phrases like "soon," "most," "significantly," or "often" that lack specificity
- **Pronouns with unclear antecedents:** "It" or "this" that refer to multiple things
- **Sentences with multiple interpretations:** Phrases that could mean different things to different readers

**Example:** "We'll scale horizontally to improve performance" is ambiguous if "scale horizontally" isn't defined. "We'll add more server nodes to the cluster" is clear.

### 2. False Assumptions Check

**Reader Claude should identify:**

- **Claims without evidence:** "X is the best approach" without justification or data
- **Assumed knowledge:** "As everyone knows..." when "everyone" might not know this
- **Implicit trade-offs:** Presenting benefits without acknowledging costs
- **Unsupported leaps:** Jumping from problem A to solution B without showing the connection

**Example:** "We should use this tool because it's modern" is unsupported. "We should use this tool because it reduces build time by 40%, as shown in [benchmark link]" is supported.

### 3. Contradiction Check

**Reader Claude should identify:**

- **Internal inconsistencies:** Section A says X, but Section B says not-X
- **Timeline conflicts:** "We'll start next month" but later "We started last week"
- **Scope creep:** Early sections limit scope, later sections expand it without acknowledgment
- **Tone inconsistencies:** Professional tone in one section, casual in another

### 4. Generic Filler Check

**Reader Claude should identify:**

- **Sentences that don't carry weight:** "In today's world..." or "It's important to note..."
- **Obvious statements:** "Communication is key" or "We need to be careful"
- **Padding:** Sentences added for length rather than substance
- **Redundancy:** The same point stated multiple times without new information

---

## Issue Reporting

### How to Present Issues to User

When issues are found, structure your report clearly:

**Issues Summary:**

1. **Clarity issues** (X found)
   - Issue: [Specific location and description]
   - Reader struggled with: [What confused them]
   - Suggested fix: Rewrite [section] to define X before using it

2. **Evidence issues** (Y found)
   - Issue: [Specific location and description]
   - Reader questioned: [What wasn't supported]
   - Suggested fix: Add data/source for [claim]

3. **Assumption issues** (Z found)
   - Issue: [Specific location and description]
   - Reader lacked context: [What knowledge is assumed]
   - Suggested fix: Add background paragraph on [topic]

4. **Contradiction issues** (if any)
   - Issue: [Section A] says X, [Section B] says not-X
   - Suggested fix: Reconcile the statements

**Ask the user:** "Which issues should we fix before testing again? Or should I fix all of them?"

---

## Looping Back to Stage 2

When issues are identified, you loop back to **Stage 2: Refinement & Structure** to fix specific sections.

### Routing to Stage 2

Map each issue type to a concrete refinement action:

| Issue Type | Routing | Action |
|------------|---------|--------|
| **Clarity** — Undefined terms, vague language | Stage 2 | Rewrite section to define terms early, use specific language |
| **Evidence** — Unsupported claims | Stage 2 | Add data, citations, or justification for claims |
| **Assumption** — Missing context | Stage 2 | Add background paragraph or prerequisites |
| **Contradiction** — Internal inconsistencies | Stage 2 | Reconcile sections, ensure consistency |
| **Generic filler** — Padding or obvious statements | Stage 2 | Cut weak sentences, tighten language |

**Example refinement request to user:**

> "Reader Claude struggled with [section], specifically: 'The acronym DPI isn't defined.' Let's go back to Stage 2 and add a definition in the introduction. Should I add it as a footnote or work it into the intro paragraph?"

### Decision Point: Fix All or Prioritize?

Ask the user:

- **Fix all issues:** Continue until no further issues surface
- **Fix critical issues only:** Address clarity and evidence issues, defer non-critical refinements
- **Fix specific sections:** User chooses which issues to address

If the user chooses to fix only some issues, re-test those sections afterward before declaring Stage 3 complete.

---

## Completion Signals

Stage 3 reader testing is complete when:

- **No further issues surface:** Reader Claude consistently answers all predicted questions correctly
- **No new ambiguities emerge:** Additional validation checks (ambiguity, assumptions, contradictions) find nothing
- **All identified issues have been fixed and re-tested:** Refinements from Stage 2 loop-back have been validated
- **User confirms readiness:** "That looks good" or "I'm satisfied with the document"

### Incomplete Signals (Keep Testing)

If any of these occur, continue testing:

- Reader Claude misinterprets a question or gives an incorrect answer
- Reader Claude surfaces a new ambiguity not caught by predicted questions
- A contradiction or false assumption is still present
- Generic filler sentences remain

---

## Final Validation and Transition

When reader testing is complete:

### Step 1: Recommend Final User Review

Ask the user to do one final read-through themselves. They own this document and are responsible for its quality. Suggest they:
- Verify all facts, links, and technical details
- Check that the document achieves the impact they wanted (from Stage 1)
- Make any final cuts or rewrites they feel are needed

### Step 2: Offer One More Review

Ask: "Do you want me to do a final full review, or are you satisfied with the document?"

- If **yes**: Provide a final editorial pass (tone, flow, completeness)
- If **no**: Proceed to completion

### Step 3: Completion Confirmation

When the user confirms they're ready, announce:

> "Your document has passed reader testing and is ready for publication or handoff. Before you share it, remember: consider adding a link to this conversation in an appendix so readers can see how the document was developed. Use appendices to add depth without bloating the main doc. And update the document as you receive feedback from real readers."

---

## Common Testing Pitfalls

### Pitfall: Only Testing Obvious Questions

**What to avoid:** Testing only the headline questions ("Does this explain the proposal?") without testing detailed edge cases.

**What to do:** Include 5–10 questions that cover edge cases, scope boundaries, and assumptions. Test for specifics, not just "Does this make sense overall?"

### Pitfall: Skipping Additional Validation Checks

**What to avoid:** Testing only predicted questions and skipping the ambiguity, assumption, and contradiction checks.

**What to do:** Always run the four additional checks (ambiguity, false assumptions, contradictions, generic filler) even if reader questions were answered correctly.

### Pitfall: Not Fixing Issues Before Declaring Success

**What to avoid:** Testing finds issues, but the user decides "it's good enough" and doesn't fix them.

**What to do:** Emphasize that unfixed issues will confuse real readers. Loop back to Stage 2 for at least the critical clarity and evidence issues. Re-test afterward.

### Pitfall: Testing with Partial Context

**What to avoid:** When using sub-agents or manual testing, accidentally including conversation context or prior knowledge.

**What to do:** Ensure the reader receives only the document content and the specific question. No background, no prior assumptions, no conversation history.

---

## Notes for Completion

### What Happens After Stage 3

When reader testing is complete and the document passes:

1. **The document is publication-ready** — It has been tested by a fresh reader (real or simulated) and passes validation checks
2. **Handoff context available** — You can provide the user with:
   - A link to this entire conversation (shows how the doc was developed)
   - A summary of changes made during Stage 3
   - Recommendations for collecting feedback from real readers after publication

3. **Feedback loop for real readers** — Advise the user: "As real readers encounter this doc, collect their questions and feedback. Those gaps will surface naturally. Update the doc when patterns of confusion emerge."

---

## Exit Checklist

Use this checklist to confirm Stage 3 reader testing is complete:

- [ ] 5–10 predicted reader questions have been generated
- [ ] Each question has been tested (sub-agent or manual)
- [ ] Results summarized: what Reader Claude got right/wrong
- [ ] Additional validation checks completed (ambiguity, assumptions, contradictions, filler)
- [ ] Issues have been identified and categorized
- [ ] Identified issues have been routed back to Stage 2 for refinement (or explicitly deferred)
- [ ] Refinements from Stage 2 have been re-tested to confirm fixes
- [ ] Reader Claude now answers all predicted questions correctly
- [ ] No new ambiguities or contradictions emerge
- [ ] User confirms satisfaction with the final document
- [ ] User has done a final personal review of facts and impact

Once complete, the document is ready for publication or handoff.
