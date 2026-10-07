# Stage 2: Refinement & Structure

**Goal:** Build the document section by section through iterative brainstorming, curation, drafting, and refinement. Move from outline to complete draft by working through each section systematically.

---

## Document Structure Determination

Before you start writing, clarify the document's structure with the user.

### If the document structure is clear

Ask which section they'd like to start with. Recommend starting with whichever section has the most unknowns—usually:
- **Decision documents:** The core proposal or decision
- **Specifications:** The technical approach or architecture
- **Proposals:** The main ask or recommendation
- **Summary sections:** Leave these for last (easier after core content exists)

### If the document structure is unclear

Based on the document type and any template from Stage 1, suggest 3–5 sections appropriate for the doc type:

**Examples by document type:**

- **Technical specification:** Problem Statement → Proposed Solution → Technical Approach → Trade-offs & Alternatives → Implementation Plan
- **Decision document:** Context → Options → Recommendation → Implementation Plan → Success Criteria
- **Proposal:** Executive Summary → Problem → Solution → Timeline & Resources → Next Steps
- **RFC (Request for Comments):** Motivation → Proposed Design → Rationale → Drawbacks → Alternatives → Unresolved Questions

Ask if this structure works, or if they want to adjust it.

### Once structure is agreed

Announce that the initial document structure with placeholders for all sections will be created.

**If access to artifacts is available:**
- Use artifact creation to make a markdown scaffold with all section headers and brief placeholder text like `[Content to be written]`
- Provide the artifact link and confirm it's time to fill in each section

**If no access to artifacts:**
- Create a markdown file in the working directory named appropriately (e.g., `proposal.md`, `technical-spec.md`)
- Confirm the filename has been created and indicate it's time to fill in each section

---

## Section-Level Iteration Loop

For each section, follow this six-step procedure:

### Step 1: Clarifying Questions

Announce work will begin on the `[SECTION NAME]` section. Ask 5–10 clarifying questions about what should be included, based on context from Stage 1 and the document's purpose.

**Example clarifying questions for a proposal's "Problem" section:**

1. What is the root cause of this problem? (Not just the symptom.)
2. How is this problem currently being addressed, if at all?
3. What's the business or technical impact of not solving this?
4. Who is affected by this problem? (Team, organization, customers, stakeholders.)
5. How would stakeholders describe the problem if you asked them directly?
6. What constraints prevent solving this problem today?
7. Is this problem new, or has it existed for a while?
8. Have previous attempts been made to solve it? Why didn't they work?

**Delivery tip:** Inform the user they can answer in shorthand or indicate what's important to cover. Don't require formal answers.

### Step 2: Brainstorming

Brainstorm 5–20 points that might be included in the `[SECTION NAME]` section, depending on complexity. Look for:
- Context shared in Stage 1 that might be relevant here
- Angles, considerations, or implications not yet mentioned
- Related decisions or trade-offs that belong in this section

**Format:** Provide a numbered list of options.

At the end, offer to brainstorm more if they want additional options.

### Step 3: Curation

Ask which points should be kept, removed, or combined. Request brief justifications to help you learn their priorities for the next sections.

**Acceptable response formats:**

- Numbered selections: `Keep 1, 4, 7, 9`
- Removal with reasoning: `Remove 3 (duplicates 1)` or `Remove 6 (audience already knows this)`
- Combination: `Combine 11 and 12`
- Freeform: `Looks good` or `I like most of it but remove the third point`

**If user gives freeform feedback instead of numbered selections:**
- Extract their preferences and proceed (parse what they want kept/removed/changed)
- Don't force a numbered format—extract the signal and move forward
- **Capture their rationale** for later use: If they say "Remove this because it's obvious," note that they prefer not to explain obvious things in this section

### Step 4: Gap Check

Based on what they've selected, ask: "Is there anything important missing for the `[SECTION NAME]` section?"

Wait for their response. This catches omissions before drafting.

### Step 5: Drafting

Announce the `[SECTION NAME]` section will now be drafted based on what they've selected.

Use `str_replace` to replace the placeholder text for this section with the actual drafted content.

**After drafting:**

**If using artifacts:**
- Provide the artifact link
- Ask them to read through it and indicate what to change
- **Include this note on the first section:** "Instead of editing the doc directly, let me know what to change. Being specific (e.g., 'Remove the X bullet—already covered by Y' or 'Make the third paragraph more concise') helps me learn your style for future sections."

**If using a local file:**
- Confirm completion
- Ask them to read the `[SECTION NAME]` section and indicate what to change
- Note that specificity helps learning for future sections

### Step 6: Iterative Refinement

As the user provides feedback:

- Use `str_replace` to make targeted edits (never reprint the entire doc)
- **If using artifacts:** Provide the link after each edit
- **If using a file:** Just confirm edits are complete
- **If user edits the doc directly and shares the revised version:** Mentally note the changes they made—this reveals their preferences and should inform future sections without needing to ask repeatedly

**Continue iterating** until the user signals satisfaction with the section. They might say:
- "That's good"
- "Let's move to the next section"
- "This feels right"

---

## Feedback Capture and Preference Learning

Track user feedback patterns across sections to learn their style and apply it to future sections without asking repeatedly.

### What to capture

As you work through sections, note:

1. **Tone preferences:** Do they want formal or conversational? Technical detail or plain language?
2. **Length preferences:** Do they tend to ask for shorter or longer versions? What's the sweet spot?
3. **Structure within sections:** Do they prefer bullet points, paragraphs, examples, or a mix?
4. **Detail level:** Are they asking for more explanation, or asking to remove "obvious" details?
5. **Evidence and examples:** Do they want data, quotes, anecdotes, or abstract reasoning?
6. **Repetition tolerance:** Do they flag duplicate points, or are they okay with reinforcement?

### How to apply learning

After you've drafted 2–3 sections and collected feedback:

- Apply observed preferences to remaining sections **without re-asking for the same feedback**
- For example: If they've consistently asked for shorter paragraphs across sections 1 and 2, write section 3 with shorter paragraphs first
- If they've consistently asked for more examples, include examples in section 3 without being asked
- If they prefer bullet points over prose, use bullets in section 3

### Signaling your learning

When you apply learned preferences, briefly acknowledge it:
- "I noticed you prefer concise points over long paragraphs, so I've drafted this section with shorter bullets."
- "Based on earlier feedback, I've added examples here."

This confirms you're tracking their style and gives them a chance to course-correct if your assumption is wrong.

---

## Quality-Checking Trigger

After 3 consecutive iterations on a section with **no substantial changes**—meaning edits are minor, cosmetic, or the user is fine-tuning wording rather than reshaping content—ask:

> "Can anything be removed from the `[SECTION NAME]` section without losing important information? Sometimes we can tighten by cutting less essential details or examples."

This question surfaces bloat before it becomes a pattern across the document.

---

## Full-Document Review

As you approach completion (80%+ of sections are drafted and refined), announce intention to re-read the entire document and check for:

- **Flow and consistency:** Do sections transition smoothly? Do they feel like one document?
- **Redundancy or contradictions:** Are the same points repeated? Do any sections contradict earlier sections?
- **Generic filler or "slop":** Are there placeholder phrases, padding, or sentences that don't carry weight?
- **Overall coherence:** Does every section serve the document's stated impact and audience?

**After reading the full document:**

Provide feedback on any patterns you notice. For example:
- "I noticed you explain [concept] in Section 2 but also in Section 4—we could tighten this by explaining it once and referencing it in Section 4."
- "Section 3 feels more formal than the rest; should we adjust the tone for consistency?"
- "There are two examples here that make the same point—would one be enough?"

Ask if they want to refine any of these areas, or if the document feels ready to move forward.

---

## Completion Signals

Stage 2 is ready to close when:

- [ ] Document structure has been agreed upon with the user
- [ ] Initial scaffold (artifact or file) has been created with all section headers
- [ ] All sections have been drafted using the six-step procedure (clarify → brainstorm → curate → gap-check → draft → iterate)
- [ ] Each section has been refined through at least one feedback cycle (and usually 2–3 iterations)
- [ ] The full document has been re-read for flow, consistency, and coherence
- [ ] The user signals readiness to move forward (e.g., "This is ready for review" or "Let's move to testing")
- [ ] No major gaps or structural issues remain

---

## Transition to Stage 3

When Stage 2 is complete, confirm readiness:

**Say something like:**

> "All sections are now drafted and refined. Before we share this with readers, I recommend testing it with a fresh perspective to catch any blind spots—things that make sense to us as authors but might confuse someone reading it for the first time. Should we move to Reader Testing (Stage 3), or would you prefer to do something else with the document first?"

**Once confirmed:**

Proceed to [Stage 3: Reader Testing](stage-3-reader-testing.md), where you'll test the document with fresh eyes to verify it works for its intended audience.

---

## Common Patterns and Pitfalls

### Pattern: User wants to skip ahead and write a section themselves

**What to do:**
- Allow it; capture what they wrote and any feedback they have on it
- When you draft the next section, note their style and apply it to subsequent sections
- If their written section differs significantly from your style, ask if they want all sections in their style or a mix

### Pattern: Feedback is very minimal ("looks good")

**What to do:**
- Don't assume it's complete; ask a targeted follow-up: "Anything you'd add, remove, or clarify?"
- If they genuinely feel it's ready, move to the next section
- Mentally note that they're satisfied with less iteration—adjust future sections accordingly

### Pattern: User keeps requesting the same type of change across multiple sections

**What to do:**
- Call this out respectfully: "I've noticed you keep asking for X across sections. Should I just do X automatically for the remaining sections, or would you rather review each one?"
- This respects their input while being efficient

### Pattern: A section becomes very long or complex

**What to do:**
- After clarifying questions and brainstorming, ask: "Should we split this into two sections, or keep it as one?"
- If you draft it and it feels unwieldy, propose splitting it in your feedback

### Pattern: User provides very detailed feedback with new content ideas

**What to do:**
- Incorporate their ideas into the next iteration
- If their feedback suggests you misunderstood their intent, loop back to the clarifying questions or gap-check step before re-drafting

---

## Notes for Effective Guidance

- **Be procedural and clear:** "We'll now brainstorm options for this section—I'll suggest 5–10 points, and you let me know what to keep or change."
- **Don't assume completion:** Even if a section feels good to you, check with the user before moving forward.
- **Preserve user agency:** If they want to edit the document directly, let them—and learn from those edits.
- **Call out blockers:** If you need clarification to draft a section, ask directly rather than proceeding with assumptions.
- **Track the time:** If a section has gone through many iterations with diminishing returns, offer to simplify or move on.
