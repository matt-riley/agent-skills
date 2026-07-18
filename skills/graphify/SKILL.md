---
name: graphify
description: Build and query persistent Graphify knowledge graphs from code, documents,
  papers, images, or video. Use when the user asks to graphify a corpus, needs graph-based
  mapping, path, or community analysis, invokes Graphify commands, or asks a corpus
  question when graphify-out/ already exists.
license: GNU GPL v3
metadata:
  version: 0.1.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: experimental
  kind: reference
---

# /graphify

Turn any folder of files into a navigable knowledge graph with community detection, an honest audit trail, and three outputs: interactive HTML, GraphRAG-ready JSON, and a plain-language GRAPH_REPORT.md.

## Use this skill when

- The user asks to build or update a Graphify knowledge graph from code, documents, papers, images, or video.
- The user asks for graph-based mapping, path tracing, community analysis, or Graphify exports.
- The user invokes a Graphify command such as `query`, `path`, `explain`, `add`, `--update`, or `--cluster-only`.
- `graphify-out/graph.json` already exists and the user asks a natural-language question about that graphed corpus.

## Do not use this skill when

- The user wants ordinary codebase explanation, search, or architecture analysis and neither requests a graph artifact nor has an existing `graphify-out/graph.json` to query.
- The task is a routine code edit, bug fix, or feature implementation with no need for Graphify output or graph-based analysis.

## Inputs to gather

- The path, URL, or corpus to graphify
- Whether the user wants a full build or a query against an existing graph
- Any mode flags (`--deep`, `--update`, `--cluster-only`, etc.)

## First move

Check whether `graphify-out/graph.json` already exists. If it does and the user's request is a natural-language question about the codebase, run `graphify query` immediately without rebuilding.

## Workflow

1. Confirm the user wants a persistent Graphify graph artifact, not ad-hoc analysis.
2. For a new graph, follow [`references/default-build-workflow.md`](references/default-build-workflow.md): detect inputs, extract entities, build the graph, export.
3. For an existing graph, load it and answer with graph-oriented queries rather than rebuilding by default.
4. Keep extraction and export settings explicit when the corpus mixes code, docs, and media.
5. Validate that outputs (graph file / exports) exist and answer the user's question from the graph.
6. Warn before heavy viz or rebuilds on large graphs; prefer incremental updates when available.
7. Route pure code navigation or non-graph research to `code-intelligence` / `autoresearch` instead.

## Guardrails

- Never invent an edge — use AMBIGUOUS if unsure
- Never skip the corpus size warning
- Always show token cost in the report
- Never hide cohesion scores behind symbols — show the raw number
- Never run HTML viz on a graph with more than 5,000 nodes without warning the user

## Validation

- Verify that graphify is installed (Step 1)
- Confirm the graph outputs exist on disk after each step
- Check that extraction produced nodes before proceeding to clustering

## Examples

All invocation examples are in `references/default-build-workflow.md`.

## Reference files

- `references/default-build-workflow.md` — Full usage surface and ordered procedure for creating a new graph
- `references/extraction-spec.md` — Subagent prompt template for semantic extraction
- `references/github-and-merge.md` — Clone, cross-repo merge, and monorepo flow
- `references/transcribe.md` — Video and audio transcription
- `references/update.md` — Incremental update and re-cluster flows
- `references/query.md` — Query, path, explain, and NetworkX fallback
- `references/add-watch.md` — Add URL and watch-mode flows
- `references/hooks.md` — Commit hook and native CLAUDE.md integration
- `references/exports.md` — Wiki, Neo4j, SVG, GraphML, MCP, and benchmark exports
- `.graphify_version` — Current graphify version for compatibility checks

## Default build workflow

For a new graph, read [`references/default-build-workflow.md`](references/default-build-workflow.md) and follow it in order. It contains the complete usage surface, installation and interpreter setup, detection and corpus-size checks, semantic extraction rules, graph construction, clustering, labeling, exports, cleanup, reporting, and support message.

Load that reference only for a fresh build, GitHub clone, multi-path merge, or `--help` request. Existing-graph queries and explicit maintenance subcommands use the focused routes below.

## Interpreter guard for subcommands

Before running any subcommand below (`--update`, `--cluster-only`, `query`, `path`, `explain`, `add`), check that `.graphify_python` exists. If it's missing (e.g. user deleted `graphify-out/`), re-resolve the interpreter first:

```bash
if [ ! -f graphify-out/.graphify_python ]; then
    GRAPHIFY_BIN=$(which graphify 2>/dev/null)
    if [ -n "$GRAPHIFY_BIN" ]; then
        PYTHON=$(head -1 "$GRAPHIFY_BIN" | tr -d '#!')
        case "$PYTHON" in *[!a-zA-Z0-9/_.-]*) PYTHON="python3" ;; esac
    else
        PYTHON="python3"
    fi
    mkdir -p graphify-out
    "$PYTHON" -c "import sys; open('graphify-out/.graphify_python', 'w', encoding='utf-8').write(sys.executable)"
fi
```

## For --update and --cluster-only

Both are non-default subcommands. `--update` re-extracts only new or changed files; `--cluster-only` reruns clustering on the existing graph. See `references/update.md` for both flows.

---

## For /graphify query

When `graphify-out/graph.json` already exists and the user asks a question about the corpus, answer from the graph rather than rebuilding it:

```bash
graphify query "<question>"
```

If the `graphify query` CLI is unavailable, fall back to an inline NetworkX traversal of `graphify-out/graph.json`. Answer using only what the graph output contains, and quote `source_location` when citing a specific fact. For the BFS/DFS traversal modes, the `--budget` cap, the NetworkX fallback, `save-result` feedback, and the `/graphify path` and `/graphify explain` flows, see `references/query.md`.

---

## For /graphify add and --watch

Neither is part of the default build. When the user runs `/graphify add <url>` to fetch a URL into the corpus, or passes `--watch` to auto-rebuild on file changes, see `references/add-watch.md`.

---

## For the commit hook and native CLAUDE.md integration

When the user asks to install the post-commit auto-rebuild hook or wire graphify into a project's CLAUDE.md, see `references/hooks.md`.
