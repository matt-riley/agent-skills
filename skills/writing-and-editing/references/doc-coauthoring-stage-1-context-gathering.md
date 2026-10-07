# Stage 1: Context Gathering

**Goal:** Close the gap between what you know and what the user knows about the document's purpose, audience, constraints, and landscape. This stage prioritizes understanding over drafting.

## When Context Gathering Is Complete

Stage 1 is ready to close when:

- You can ask questions about edge cases and trade-offs without needing basics explained
- The user has indicated they've provided their primary context dump
- You have sufficient information to suggest document structure
- Any template, existing document, or image reference issues have been surfaced and addressed

**Signal to move forward:** Ask "Any more context you want to provide at this stage, or ready to move to drafting?" When the user confirms readiness, proceed to Stage 2.

---

## Initial Meta-Context Questions

Start by asking for meta-context about the document. These five questions establish the frame:

1. **What type of document is this?**
   - Example answers: technical specification, decision document, proposal, RFC, design document, process guide, policy document
   - Why: Determines appropriate section structure and audience expectations

2. **Who's the primary audience?**
   - Example answers: your team, engineering leadership, customers, board, external partners
   - Why: Shapes tone, depth, assumptions, and what needs explicit explanation

3. **What's the desired impact when someone reads this?**
   - Example answers: approve a decision, align on direction, reference material, understand reasoning, execute a plan
   - Why: Clarifies success criteria and what information is actually necessary

4. **Is there a template or specific format to follow?**
   - Example answers: company template, RFC format, RFC 2119 style, GitHub issue template link
   - Why: Some docs are structured documents; others are freeform

5. **Any other constraints or context to know?**
   - Example answers: timeline pressure, organizational politics, related documents already approved, technical dependencies
   - Why: Catches timing pressures, stakeholder concerns, and organizational dynamics that affect content

**Delivery tip:** Inform the user they can answer in shorthand and that organizing details isn't necessary yet—just get it all out.

---

## Handling Templates and Existing Documents

### If user provides a template

- **Ask if they have the template document to share**
  - If they have a link to a shared document: Use available integration tools (Google Drive, Slack, etc.) to fetch it, or ask them to paste key sections
  - If they describe it from memory: Ask them to fetch and paste it so you have the exact format
- **Review the template for required sections**
  - Ask what sections they feel unsure about or what sections might have different content than the template suggests
  - Identify which sections should be tackled first (usually those with the most unknowns)

### If user mentions editing an existing shared document

- **Use available integrations to read the current state**
  - If integrations are available (Google Drive, Slack, Teams, SharePoint): Fetch the document directly
  - If no integrations: Ask them to paste the document content or share a link that summarizes current state
- **Check for images without alt-text**
  - If images exist without alt-text: Explain that when others use Claude or similar tools to understand the doc, Claude won't be able to see these images
  - Ask if they want alt-text generated
  - If yes: Request they paste each image into chat so you can generate descriptive alt-text that works in Claude

---

## Info Dumping Strategies

Once initial questions are answered, encourage the user to provide all context they have. Don't worry about organization yet—just get everything out.

### What to request

Ask for information in these categories:

- **Background on the project or problem** — What's the context? Why does this doc exist now?
- **Related team discussions or shared documents** — Links to Slack threads, meeting notes, previous docs, or decisions
- **Why alternative solutions aren't being used** — Constraints, trade-offs, rejected approaches
- **Organizational context** — Team dynamics, past incidents, stakeholder concerns, organizational culture
- **Timeline pressures or constraints** — When is this needed? Who needs to approve?
- **Technical architecture or dependencies** — If relevant: system design, dependencies, technical assumptions
- **Stakeholder concerns or known objections** — Who will read this? What do they care about? What might they question?

### Multiple input modes

Offer these options for how to provide context:

1. **Stream-of-consciousness dump** — Just type freely; you'll organize it later
2. **Point to channels or threads** — "See #architecture-discussion" or "Check this Slack thread"
3. **Link to shared documents** — Google Docs, Confluence, wiki pages, or other references
4. **Mix of the above** — Whatever's fastest for them

### Tool availability note

**If integrations are available** (Slack, Teams, Google Drive, SharePoint, or other MCP servers):

- Mention that channels, threads, and documents can be read directly
- Inform them that you'll fetch content now if they point you to it
- If available: mention this can be faster than copy-paste

**If no integrations are detected and in Claude.ai or Claude app:**

- Suggest they can enable connectors in their Claude settings to allow pulling context from messaging apps and document storage directly
- If they haven't already: explain that enabling connectors makes this workflow faster

**If they don't want to enable integrations:**

- Fall back to asking them to paste relevant excerpts or provide summaries
- Proceed normally; the workflow doesn't require integrations

### During context gathering

**If user mentions team channels or shared documents:**
- **If integrations available:** Inform them the content will be read now, then use the appropriate integration
- **If integrations not available:** Explain the lack of access, suggest enabling connectors in Claude settings, or ask them to paste the relevant content directly

**If user mentions entities/projects that are unknown:**
- Ask if connected tools should be searched to learn more (if you have search/integration capabilities)
- Wait for user confirmation before searching—don't assume you should pull additional context automatically

**As user provides context:**
- Track what's being learned and what's still unclear
- Surface gaps proactively: "I notice you mentioned X but not Y—is Y relevant?"

---

## Clarifying Questions Generation

When the user signals they've done their initial context dump (or after substantial context provided), ask clarifying questions to confirm understanding.

### How to generate questions

Create **5–10 numbered questions** based on gaps you've identified:

- Ask about edge cases not yet mentioned
- Ask about trade-offs or decisions not yet explicit
- Ask about stakeholder groups or concerns not covered
- Ask about scope boundaries or what's explicitly out of scope
- Ask about success metrics or how they'll know if the doc worked

**Example clarifying questions for a proposal:**

1. "Are we proposing a full rewrite or an incremental improvement?"
2. "What's the timeline for implementation—is that a constraint on the proposal, or is it flexible?"
3. "Who has veto power on this decision? Are there known objections?"
4. "What's the budget/resource constraint? Is that explicit in the doc or implicit?"
5. "Should the proposal include implementation steps, or is that a follow-on document?"
6. "Are there competing proposals we're explicitly ruling out, or should this stand alone?"
7. "Who needs to approve this before it's shared externally?"
8. "Should the doc include metrics on success, or is that a post-implementation addition?"

### Handling shorthand answers

Inform the user they can use shorthand to answer:

- Numbered list: `1: yes, 2: see #channel, 3: no because backwards compat`
- Links to more docs: "1: yes, 2: see [this Confluence page], 3: ..."
- Point to channels: "1: yes, 2: check #architecture-discussion, 3: ..."
- Or just keep info-dumping: "Let me add to my earlier point..."
- **Whatever's most efficient for them**

### If user gives freeform feedback instead of numbered answers

Parse their preferences and proceed:
- If they say "Looks good" after clarifying questions, extract which answers they're implicitly confirming
- If they provide reasoning ("We can't do that because..."), incorporate the constraint into your model
- Don't force a numbered format—extract the signal and move forward

---

## Exit Checklist

Use this checklist to confirm Stage 1 is ready to close:

- [ ] Initial meta-context questions answered (doc type, audience, impact, constraints)
- [ ] Template or format clarified (if applicable)
- [ ] Images identified and alt-text addressed (if applicable)
- [ ] Context dump completed (user signals no more context to add)
- [ ] Clarifying questions asked and answered (or user signals they're ready despite gaps)
- [ ] You can now ask questions about edge cases without needing basics explained
- [ ] You understand what success looks like for this document
- [ ] You understand the audience's concerns and potential objections

---

## Transition to Stage 2

When checklist is complete, confirm readiness:

**Say something like:**

> "We've got solid context now. I understand [recap: doc type, audience, 1–2 key constraints]. Before we start drafting, do you want to add any more context at this stage, or should we move into building the document structure?"

**Once confirmed:**

Proceed to [Stage 2: Refinement & Structure](stage-2-refinement-structure.md), where you'll determine the document structure and build it section by section.

---

## Common Patterns and Pitfalls

### Pattern: User gives minimal answers to initial questions

**What to do:**
- Don't force exhaustive answers; ask a follow-up that connects to something concrete
- For example, if they say "audience is our team" → ask "Are there specific people on the team who will be skeptical?" or "Will this be read by non-technical people on the team?"
- Build context iteratively rather than hitting a wall

### Pattern: Context dump is very long or scattered

**What to do:**
- You can organize it mentally and call back to specific pieces as needed
- Ask clarifying questions that help you distinguish signal from noise
- Don't ask them to "re-organize" — that's your job

### Pattern: User mentions constraints they're unsure about

**What to do:**
- Ask them to validate or push back on your understanding
- For example: "You mentioned timeline pressure—is Q4 a hard deadline, or flexible?"
- Get confirmation rather than assuming

### Pattern: User says "I don't know" to a clarifying question

**What to do:**
- Move on—it's not blocking
- If it's truly critical, you'll surface it again during drafting when you ask section-level questions
- Avoid creating the expectation that they need to have all answers upfront

### Pattern: Integrations fail to fetch context

**What to do:**
- Don't proceed with speculation
- Clarify with the user: "The connector didn't come through—can you paste the key sections, or should we proceed without it?"
- Document what you're missing so you can ask targeted questions later

---

## Notes for Future Stages

### What you'll need from Stage 1 context for Stage 2

When you move to Stage 2, you'll use this context to:

1. **Suggest document structure** — What sections make sense given the doc type and audience?
2. **Prioritize sections** — Which sections have the most unknowns? Start there.
3. **Ask targeted clarifying questions per section** — What goes in each section given what you now know?
4. **Brainstorm section content** — What options are relevant given audience, impact, constraints?

### Red flag: Insufficient context

If you enter Stage 2 and realize context is still missing (you keep hitting "I don't know" in section-level questions), loop back to clarifying questions here. It's faster to resolve context gaps here than to discover them mid-draft.

