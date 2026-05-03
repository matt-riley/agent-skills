# Edge cases for Security Basics

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Write a full threat model document for the company."
- "Implement a whole auth system from scratch."
- "Review a feature plan rather than code or security-sensitive behaviour."

## Common edge cases
- If the task is pure feature design with no security-sensitive surface, do not over-apply this skill.
- If the system already has explicit proxy trust configuration, use that source of truth instead of generic assumptions.
- Do not replace deeper security review for high-risk changes; use this as a baseline guardrail layer.

## Reminders
- If the request really matches this shape, the skill should activate: "I am touching authentication and logging code; apply the security guardrails before I ship this."
- If the request really matches this shape, the skill should activate: "Quick security pass on this request handling and sensitive endpoint change."
