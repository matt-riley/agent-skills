# Context-map examples

## Example 1: multi-file feature scoping

**Prompt**

`Before editing, map the files, tests, and patterns involved in adding a new skill under @skills/.`

**Why this should trigger**

- The request is explicitly pre-edit.
- The work may span a new skill package, README catalog updates, and nearby reference files.
- The user is asking for file/test/pattern discovery, not a full implementation plan yet.

## Example 2: pre-refactor discovery

**Prompt**

`Create a context map for this refactor before we plan it: move duplicated planner-handoff guidance out of two skills and into one shared reference.`

**Why this should trigger**

- The task likely spans multiple skill packages.
- Dependencies and reference patterns matter before planning the refactor.
- The next useful output is a scoped map, not immediate code changes.

## Near-miss example

**Prompt**

`Fix the broken markdown link in @skills/reverse-prompt/SKILL.md.`

**Why this should not trigger**

- The file is already named.
- The scope is narrow and ready for direct execution.
