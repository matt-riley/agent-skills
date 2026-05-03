  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed
  0      0   0      0   0      0      0      0                              0# Smoke Test Prompts

These are the manual test scenarios for validating the `/plan-review-loop` skill before it is considered production-ready. Each scenario covers a specific review workflow path.

## Test Environment

All tests are **manual and interactive**. They require:
1. A live Copilot CLI session with the skill loaded
2. Running `/skills reload` to refresh the skill inventory
3. Invoking `/skills info plan-review-loop` to confirm discoverability
4. Running each test scenario by hand and recording the outcomes

No automated/scripted validation is possible because the skill depends on interactive reviewer agents.

## Scenario 1: Approve Path (Both Reviewers Approve in Round 1)

### Setup

Create or use an existing simple plan (e.g., a 2-3 task deployment plan).

### Invocation

```
Use the /plan-review-loop skill to review and refine the current plan.
```

### Expected Outcome

- Jason reviews the plan
- Jason returns `[PLAN-APPROVED]` (with brief reasoning)
- Freddy reviews the plan
- Freddy returns `[PLAN-APPROVED]` (with brief reasoning)
- Skill reports: ✅ **Plan approved! Ready to proceed.**

### Evidence to Capture

- Jason's response (must contain `[PLAN-APPROVED]`)
- Freddy's response (must contain `[PLAN-APPROVED]`)
- Skill's final status message

### Pass Criteria

- Both reviewers return `[PLAN-APPROVED]`
- Skill exits after Round 1 and reports approval

---

## Scenario 2: Revise Path (One Reviewer Requests Revision)

### Setup

Create a plan with a known gap (e.g., missing rollback procedure or unclear validation steps).

### Invocation (Round 1)

```
Use the /plan-review-loop skill to review and refine the current plan.
```

### Expected Outcome (Round 1)

- Jason reviews and returns `[PLAN-REVISE-NEEDED]` (with feedback on the gap)
- Freddy reviews and returns `[PLAN-APPROVED]` (accepts the overall structure)
- Skill reports: ❌ **Plan not approved (Jason needs revision). Update the plan and request another round.**

### Update

You edit the plan to address Jason's feedback (e.g., add rollback procedure).

### Invocation (Round 2)

```
Updated the plan with rollback procedure. Use the /plan-review-loop skill again.
```

### Expected Outcome (Round 2)

- Jason reviews the updated plan and returns `[PLAN-APPROVED]` (acknowledging the fix)
- Freddy reviews again and returns `[PLAN-APPROVED]` (confirms no regression)
- Skill reports: ✅ **Plan approved! Ready to proceed.**

### Evidence to Capture

- Round 1: Jason's `[PLAN-REVISE-NEEDED]` feedback
- Round 1: Freddy's `[PLAN-APPROVED]` response
- Round 1: Skill's "not approved" status
- Round 2: Jason's updated `[PLAN-APPROVED]` response
- Round 2: Freddy's `[PLAN-APPROVED]` response
- Round 2: Skill's approval status

### Pass Criteria

- Round 1 produces mixed verdict (one revise, one approve) and skill reports "not approved"
- Plan is updated
- Round 2 produces unanimous approval and skill reports "approved"

---

## Scenario 3: Mixed Verdict (One Approves, One Needs Revision)

### Setup

Create a plan that satisfies one reviewer's criteria but not the other's (e.g., good execution details but loose on architecture).

### Invocation (Round 1)

```
Use the /plan-review-loop skill to review and refine the current plan.
```

### Expected Outcome (Round 1)

- Jason returns `[PLAN-APPROVED]` (execution is solid)
- Freddy returns `[PLAN-REVISE-NEEDED]` (architecture lacks clarity)
- Skill reports: ❌ **Plan not approved (Freddy needs revision).**

### Evidence to Capture

- Jason's `[PLAN-APPROVED]` response
- Freddy's `[PLAN-REVISE-NEEDED]` feedback (with specific architectural concerns)
- Skill's "not approved" status

### Pass Criteria

- Skill correctly recognizes the mixed verdict and blocks approval
- Skill correctly identifies Freddy as the blocker
- Skill reports that another round is needed

---

## Scenario 4: Max Rounds Stop (3 Rounds Without Unanimous Approval)

### Setup

Create a deliberately challenging plan that requires extensive revision (or create three separate plans to simulate three rounds).

### Invocation & Execution

- **Round 100   7799 100   7799   0      0 215.1k      0                              0100   7799 100   7799   0      0 214.7k      0                              0100   7799 100   7799   0      0 214.3k      0                              0
1**: Invoke skill. One or both reviewers request revision.
- **Round 2**: Update plan. Invoke skill again. At least one reviewer still needs revision.
- **Round 3**: Update plan. Invoke skill one final time.

### Expected Outcome (Round 3)

- Reviewers return verdicts (approved or revision needed)
- If any reviewer still requests revision or no unanimous approval is reached: Skill exits with message: ⏱️ **Max rounds (3) reached. Plan not approved. Reviewers: Jason [approved/revised], Freddy [approved/revised]. Decide next steps manually.**

### Evidence to Capture

- All three round invocations and reviewer responses
- Final skill message indicating max rounds reached
- Current approval status (approved vs. not approved)

### Pass Criteria

- Skill stops after exactly 3 rounds
- Skill does not loop or ask for a 4th round
- Skill correctly reports the final verdict of each reviewer
- User can proceed or manually accept the plan as desired

---

## Scenario 5: Persona Customization Swap

### Setup

Create two custom persona files in `references/personas/` (e.g., `alice.md` and `bob.md`) with different review focuses than Jason and Freddy.

**Example:** Create `alice.md` (Security Reviewer) and `bob.md` (Performance Reviewer).

### Pre-Test Configuration

Rename or delete `jason.md` and `freddy.md` temporarily (or keep them and have 4 reviewers total).

```bash
# Option 1: Replace all reviewers
mv references/personas/jason.md references/personas/jason.md.bak
mv references/personas/freddy.md references/personas/freddy.md.bak
# Now only alice.md and bob.md exist
```

### Reload and Verify

In Copilot CLI:

```
/skills reload
/skills info plan-review-loop
```

Verify that the skill description mentions Alice and Bob (or lists custom reviewers).

### Invocation

```
Use the /plan-review-loop skill to review and refine the current plan.
```

### Expected Outcome

- Alice reviews the plan from her persona (e.g., security focus)
- Alice returns `[PLAN-APPROVED]` or `[PLAN-REVISE-NEEDED]`
- Bob reviews the plan from his persona (e.g., performance focus)
- Bob returns `[PLAN-APPROVED]` or `[PLAN-REVISE-NEEDED]`
- Skill proceeds normally with Alice and Bob as reviewers (not Jason and Freddy)

### Evidence to Capture

- Alice's response (with her unique review focus visible)
- Bob's response (with his unique review focus visible)
- Skill's final status (reflects approval/revision based on Alice + Bob)

### Pass Criteria

- Custom personas are loaded and used instead of defaults
- Reviewers' responses reflect their custom personas and rubrics
- Skill treats custom reviewers the same as default personas (same verdict tokens, same round logic)

---

## Evidence Artifact

All captured evidence should be collected in a single session document:

**Path:** `session-state/f5e72e83-0817-4f8a-8e3d-2e4efc9c93f4/files/plan-review-loop-smoke-test.md`

**Format:**

```markdown
# Smoke Test Results

## Scenario 1: Approve Path
- Date: YYYY-MM-DD
- Jason response: [copied text]
- Freddy response: [copied text]
- Skill final status: [copied text]
- Result: ✅ PASS / ❌ FAIL

## Scenario 2: Revise Path
...
```

## Validation Gate

The skill is considered **production-ready** if:

1. ✅ All 5 scenarios are executed manually
2. ✅ All scenarios produce expected outcomes
3. ✅ All verdict tokens are recognized correctly
4. ✅ Round logic (unanimous approval, revision blocking, max-rounds stop) works as documented
5. ✅ Persona customization works (custom personas load and are used)
6. ✅ Evidence is captured in the session artifact

If any scenario fails or produces unexpected behavior, investigate and update the skill before deletion of the old extensions.
