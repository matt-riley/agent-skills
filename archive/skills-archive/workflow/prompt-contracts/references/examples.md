# Examples for Prompt contracts

Use these as concrete patterns when the skill should activate.

## Example 1 - Definition of done before implementation

User says: "Before we touch this migration, define success criteria, constraints, output format, and failure conditions."

Expected behaviour:
- The response produces a structured contract with the four required sections and keeps the clauses concrete enough to guide implementation.

Key checks:
- Uses GOAL, CONSTRAINTS, FORMAT, and FAILURE explicitly.
- Makes the clauses testable rather than aspirational.
- Treats the contract as an execution spec, not just brainstorming.

## Example 2 - Contract as a gate

User says: "What does done look like for this auth refactor? I want a prompt contract before anyone writes code."

Expected behaviour:
- The response writes or refines a contract that can gate execution and clarifies any material ambiguity instead of skipping straight to code.

Key checks:
- Defines a durable definition of done.
- Includes failure conditions that would catch fake-done implementations.
- Notes any material ambiguity that still needs user confirmation.
