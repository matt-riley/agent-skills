# Fresh-reader review loop

Use this checklist once a complete draft exists — before handing it back to the user or transitioning to a readability pass.

## Fresh-reader checklist

Work through these in order. A "no" answer is a gap that needs fixing before the draft is ready.

**Opening and purpose**
- [ ] Can a reader unfamiliar with the context understand the document's purpose from the title and first paragraph alone?
- [ ] Is the core message, decision, or goal stated explicitly — not buried in a middle section or only implied?
- [ ] Is the intended audience identifiable from the opening, either explicitly or by the assumed knowledge level?

**Structure and completeness**
- [ ] Does the section structure match the stated document type? (A runbook should have numbered steps; an ADR should have context, decision, and consequences; a proposal should have problem, solution, and risks.)
- [ ] Are all required sections present and non-empty?
- [ ] Are there sections that are too long relative to their importance? (Flag for cutting or summarizing.)
- [ ] Are there sections that are too short to be useful? (Flag for expanding or merging.)
- [ ] Are action items, decisions, or next steps easy to find — not embedded in running prose?

**References and context**
- [ ] Are references to external docs, prior decisions, or related context linked or cited?
- [ ] Does the document define or link out for any domain-specific jargon a reader outside the author's immediate team might not know?
- [ ] Are assumptions about the reader's prior knowledge made explicit where they would affect comprehension?

**Audience alignment**
- [ ] Would the intended audience be able to act on or use this document without needing to ask clarifying questions?
- [ ] If the document is for a mixed audience (technical + non-technical), are sections scoped appropriately for each?

## Likely reader questions

Before calling the draft complete, test it against these questions a real reader is likely to ask. If any answer is "unclear" or "not covered," flag the section.

1. What problem does this document solve, or what decision does it make?
2. Who is the intended audience, and what do they already need to know?
3. What am I expected to do after reading this?
4. What is explicitly in scope — and what is out of scope?
5. Where do I go for more detail, or to raise a concern?
6. When was this written, and is it still current?

## Hidden-assumption and ambiguity checks

Run these after the fresh-reader checklist. These catch issues that pass a structural review but create confusion during real use.

**Hidden assumptions**
- Does any section assume a decision was already made that is not documented here?
- Does any section assume the reader has context from a meeting, Slack thread, or prior doc that is not linked?
- Does any diagram, table, or code example assume knowledge that the surrounding prose does not provide?
- Would someone joining the team or project six months from now be able to interpret this document correctly?

**Scope ambiguity**
- Is there any section where it is unclear whether something is in scope, out of scope, or to be decided later?
- Are there any "we will handle this later" statements that are not tracked or linked to a follow-up?
- Are there any conditional recommendations ("if X, then Y") where the conditions are not explained?

**Language and framing**
- Are there passive voice statements that obscure ownership or accountability? ("A decision was made" vs. "The team decided")
- Are there weasel phrases that create ambiguity? ("might," "should probably," "could potentially")
- Are there undefined acronyms or initialisms that appear before they are defined?
- Are numeric values, dates, or version numbers specific and unambiguous?

## When to hand off

- **Hand off to `readability-check`** when structure and content are settled and the remaining concern is prose quality, sentence clarity, or ESL accessibility. Do not run a readability audit while the structure is still changing.
- **Hand off to `metadata-check`** when the title, abstract, short description, or tagline needs improvement as a standalone string evaluated on clarity, length, and truncation fit — independent of the full document body.
- **Stay in this skill** when the review reveals structural gaps, missing sections, or content that needs to be rewritten for a different audience. Those are drafting problems, not prose polish problems.
