# Graph Report - task-353930ae-6673-4b1c-b84b-6368eda7b93b  (2026-07-27)

## Corpus Check
- 18 files · ~6,865 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 134 nodes · 205 edges · 13 communities (11 shown, 2 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 39 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f631c7d9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- coding.md
- planning.md
- architecture.md
- integrating.md
- Daedalus Project Instructions
- README.md
- main.py
- test_main.py
- architecture.md
- integrating.md
- Daedalus Project Instructions
- community-intelligence-engine
- __init__.py

## God Nodes (most connected - your core abstractions)
1. `crawl()` - 16 edges
2. `FakeRedditReader` - 14 edges
3. `RedditClientError` - 10 edges
4. `PrawRedditReader` - 10 edges
5. `CrawlResult` - 9 edges
6. `PostObservation` - 9 edges
7. `CrawlConfig` - 8 edges
8. `RedditReader` - 8 edges
9. `RedditCredentials` - 7 edges
10. `post()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `config()` --calls--> `CrawlConfig`  [INFERRED]
  tests/test_community_graph_crawler.py → src/community_graph/config.py
- `FakeRedditReader` --uses--> `CrawlConfig`  [INFERRED]
  tests/test_community_graph_crawler.py → src/community_graph/config.py
- `FakeRedditReader` --uses--> `TerminationReason`  [INFERRED]
  tests/test_community_graph_crawler.py → src/community_graph/crawler.py
- `test_each_hard_ceiling_stops_without_overshooting()` --calls--> `crawl()`  [INFERRED]
  tests/test_community_graph_crawler.py → src/community_graph/crawler.py
- `FakeRedditReader` --uses--> `PostObservation`  [INFERRED]
  tests/test_community_graph_crawler.py → src/community_graph/reddit_client.py

## Import Cycles
- None detected.

## Communities (13 total, 2 thin omitted)

### Community 0 - "coding.md"
Cohesion: 0.21
Nodes (14): Counter, StrEnum, CrawlConfig, _begin_observation(), CrawlResult, Bounded breadth-first traversal of subreddit and user relationships., TerminationReason, _truncate() (+6 more)

### Community 1 - "planning.md"
Cohesion: 0.15
Nodes (13): Protocol, RuntimeError, PostObservation, PrawRedditReader, Small read-only boundary around PRAW., Raised when Reddit cannot serve a requested listing., RedditClientError, RedditReader (+5 more)

### Community 2 - "architecture.md"
Cohesion: 0.31
Nodes (11): crawl(), FakeRedditReader, post(), test_breadth_first_traversal_respects_depth_and_counts_boundary_users(), test_deleted_authors_are_skipped(), test_duplicate_submission_ids_do_not_inflate_any_counter(), test_each_hard_ceiling_stops_without_overshooting(), test_exhausted_queue_completes() (+3 more)

### Community 3 - "integrating.md"
Cohesion: 0.29
Nodes (6): Community Knowledge Graph Discovery, Dev Mode, Key Points, Relevant Files, State Log, Summary

### Community 4 - "Daedalus Project Instructions"
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 5 - "README.md"
Cohesion: 0.08
Nodes (24): 1. Outreach plan, 2. Draft posts, 3. Validation report, Bounded Reddit Community Discovery, Community Discovery, Community Discovery, Community Graph, Community Intelligence Engine (+16 more)

### Community 6 - "main.py"
Cohesion: 0.22
Nodes (11): Path, main(), Singular entrypoint for bounded Reddit community discovery., ConfigurationError, load_crawl_config(), load_reddit_credentials(), normalize_identity(), Load community discovery parameters and Reddit credentials. (+3 more)

### Community 7 - "test_main.py"
Cohesion: 0.29
Nodes (6): 4-Stage Development Lifecycle, Alignment, Debugging, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 8 - "architecture.md"
Cohesion: 0.33
Nodes (5): 4-Stage Development Lifecycle, Evidence Extraction, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 9 - "integrating.md"
Cohesion: 0.40
Nodes (4): 4-Stage Development Lifecycle, Execution Boundaries (CRITICAL), Feature File Automation, Parameter File Centralization

### Community 10 - "Daedalus Project Instructions"
Cohesion: 0.50
Nodes (3): Daedalus Project Instructions, graphify, Task mode

## Knowledge Gaps
- **49 isolated node(s):** `community-intelligence-engine`, `Execution Boundaries (CRITICAL)`, `Evidence Extraction`, `Feature File Automation`, `Parameter File Centralization` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PrawRedditReader` connect `planning.md` to `main.py`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `main()` connect `main.py` to `coding.md`, `planning.md`, `architecture.md`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `crawl()` connect `architecture.md` to `coding.md`, `planning.md`, `main.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `crawl()` (e.g. with `main()` and `normalize_identity()`) actually correct?**
  _`crawl()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `FakeRedditReader` (e.g. with `PostObservation` and `CrawlConfig`) actually correct?**
  _`FakeRedditReader` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `RedditClientError` (e.g. with `RedditCredentials` and `FakeReddit`) actually correct?**
  _`RedditClientError` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `PrawRedditReader` (e.g. with `RedditCredentials` and `main()`) actually correct?**
  _`PrawRedditReader` has 5 INFERRED edges - model-reasoned connections that need verification._