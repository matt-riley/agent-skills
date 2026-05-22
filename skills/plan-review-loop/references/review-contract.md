# Review Contract

This document defines the formal contract between the `/plan-review-loop` skill and configured reviewers.

## Verdict Tokens

The skill recognizes exactly two verdict tokens:

- **`[PLAN-APPROVED]`** — reviewer approves the plan in this round
- **`[PLAN-REVISE-NEEDED]`** — reviewer requests revision before approval

Any other format is not recognized as a valid verdict.

## Token Parsing Rules

1. **Exact match required** — tokens must appear in the response exactly as written (case-sensitive, no variations like `[PLAN-APPROVED]` vs `[Approved]`)
2. **Text anywhere in response** — tokens can appear anywhere in the reviewer's response (start, middle, or end)
3. **One token per reviewer** — each reviewer's response contains exactly one verdict token per round
4. **No ambiguous responses** — if both tokens appear in a single response, the response is rejected as ambiguous; the reviewer must choose one verdict
5. **Missing token = rejection** — if a response contains no recognized token, it is treated as a rejection (plan not approved)

## Round Structure

Each review round follows this sequence:

1. **Reviewer initialization** — all configured reviewers are notified of the plan to review
2. **Parallel or sequential review** — reviewers analyze the plan independently (implementation may parallelize or sequence)
3. **Response collection** — each reviewer submits their verdict with optional reasoning
4. **Round outcome determination**:
   - ✅ **All reviewers return `[PLAN-APPROVED]`** in the same round → **plan approved**, skill exits
   - ❌ **Any reviewer returns `[PLAN-REVISE-NEEDED]`** → **plan not approved**, user updates plan and requests another round
   - ❌ **Any reviewer's response is missing a token or contains both tokens** → treated as rejection, plan not approved

## Approval Criteria

The plan is **approved** if and only if:
- **All configured reviewers return `[PLAN-APPROVED]` in the same round**
- **No reviewer requests revision**

The plan is **not approved** if:
- Any reviewer returns `[PLAN-REVISE-NEEDED]`
- Any reviewer's response contains no verdict token
- Any reviewer's response contains both tokens (ambiguous)
- The maximum number of rounds (3) has been reached without unanimous approval

## Round Limit

The skill stops after **3 complete review rounds**.

- **Round 1** → all reviewers review and return verdicts
- **Round 2** (if needed) → user updates plan, all reviewers review again
- **Round 3** (if needed) → user updates plan again, all reviewers review one final time

After **Round 3**, if the plan is not unanimously approved, the skill exits and flags the plan as "not approved (max rounds reached)". The user then decides whether to:
- Manually review and accept the plan despite not having unanimous approval
- Continue revising outside the skill
- Accept one reviewer's concerns and request a 4+ round manually

## Reviewer Responsibilities

### Reviewer Output Format

Each reviewer must return:

```
[PLAN-APPROVED] <reasoning (optional)>
```

or

```
[PLAN-REVISE-NEEDED] <feedback explaining why (optional)>
```

The reasoning/feedback is optional but recommended for clarity.

### Reviewer Conduct

- Reviewers must evaluate the same plan during the same round (no cross-round interpretation)
- Reviewers must maintain consistency within a round (if they approve in Round 1, they shouldn't ask for the same fix again in Round 2 without the user having a chance to revise)
- Reviewers should acknowledge when they approve a revised plan even if their earlier feedback wasn't incorporated (the plan is evaluated on its current merits, not historical feedback)

## User Responsibilities

### Between Rounds

- User updates the plan based on reviewer feedback
- User invokes the skill again to run the next review round
- User does not re-request the same round; each invocation starts a new round

### Interpretation

- User interprets reviewer feedback and decides which changes to make
- User can ignore low-priority feedback but should address all blocking feedback (marked as `[PLAN-REVISE-NEEDED]`)

## Edge Cases

### No Reviewers Configured

If no reviewer persona files exist, the skill cannot run and exits with an error.

### Single Reviewer

If only one reviewer is configured (e.g., only Jason), approval requires that one reviewer to return `[PLAN-APPROVED]`.

### Custom Reviewer Added Mid-Workflow

If the user adds a new persona file (e.g., "alice.md") after Round 1, the next round includes all reviewers including Alice. Alice is a new reviewer and her approval is required from that round onward.

### Reviewer Response is Too Long or Malformed

The skill parses the response for the verdict token regardless of length or formatting. As long as the token appears somewhere, the verdict is recognized. If the response is corrupted or the token is missing, it defaults to rejection.

## Migration from Orchestrator

This contract replaces the older passive orchestrator contract, which used the same tokens but in a hook-based passive context. Key differences:

- **Old (Orchestrator):** passive hooks ran on `/plan` automatically; verdicts were parsed from runtime child output
- **New (Skill):** explicit invocation after `/plan` completion; verdicts are collected from configured reviewers via the skill

The verdict tokens remain unchanged for backward compatibility, but the activation model is now explicit and user-controlled.
