# Context-map search playbook

Use this order so the map stays focused and repeatable.

## Discovery order

1. **Start with the request nouns**
   - Pull out filenames, directories, feature names, symbols, commands, and user-mentioned surfaces.
   - If the request already names exact files, start there instead of broad searching.

2. **Find likely entry points**
   - Prefer semantic/code-intelligence tools first when available.
   - Then use file-name discovery and targeted text search to find the most relevant files or directories.

3. **Trace direct relationships**
   - From each likely entry point, identify imports, calls, config references, or neighboring modules that constrain the work.
   - Favor direct dependencies over speculative "maybe related" files.

4. **Find nearby tests**
   - Look for unit, integration, or fixture files that cover the same surface.
   - If a file has no nearby tests, note the gap rather than guessing.

5. **Find reference patterns**
   - Look for one or two similar features or files that already do the thing the new work should resemble.
   - Prefer local house patterns over upstream or external examples.

6. **Capture likely risks**
   - Note where the scope could widen: shared helpers, config fan-out, generated files, public contracts, or docs/catalog updates.
   - Keep risks concrete enough that the next phase knows what to verify.

## Stop conditions

- Stop when the next read or edit set is obvious.
- If the map is still ambiguous because one key file has not been read yet, say that directly instead of over-expanding the search.
- Do not turn the map into a full execution plan; route to planning when the file surface is already clear.
