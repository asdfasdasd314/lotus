# Graph Report - task-b1f356a9-e4f1-49d6-9be5-1edee6958010  (2026-07-27)

## Corpus Check
- 9 files · ~3,304 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 34 nodes · 26 edges · 8 communities (7 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `65f0d190`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- coding.md
- planning.md
- architecture.md
- integrating.md
- Daedalus Project Instructions
- README.md

## God Nodes (most connected - your core abstractions)
1. `Daedalus Project Instructions` - 3 edges
2. `Execution Boundaries (CRITICAL)` - 1 edges
3. `Evidence Extraction` - 1 edges
4. `Feature File Automation` - 1 edges
5. `Parameter File Centralization` - 1 edges
6. `4-Stage Development Lifecycle` - 1 edges
7. `Execution Boundaries (CRITICAL)` - 1 edges
8. `Feature File Automation` - 1 edges
9. `Parameter File Centralization` - 1 edges
10. `4-Stage Development Lifecycle` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (8 total, 1 thin omitted)

### Community 0 - "coding.md"
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 1 - "planning.md"
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 2 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 3 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 4 - "Daedalus Project Instructions"
Cohesion: 0.50
Nodes (3): Daedalus Project Instructions, graphify, Task mode

## Knowledge Gaps
- **24 isolated node(s):** `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Feature File Automation`, `Parameter File Centralization`, `4-Stage Development Lifecycle` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Feature File Automation` to the rest of the system?**
  _24 weakly-connected nodes found - possible documentation gaps or missing edges._