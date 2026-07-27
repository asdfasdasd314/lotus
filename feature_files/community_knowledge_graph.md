# Community Knowledge Graph Discovery

## Summary

This feature discovers Reddit communities in memory by following subreddit-to-author-to-subreddit relationships with a bounded breadth-first crawl. It owns traversal, encounter counting, resource ceilings, and the console discovery report; Reddit access is isolated behind a read-only adapter.

## Key Points

- Seeds, sampling sizes, traversal depth, and independent hard ceilings come from the matching read-only TOML parameter file.
- The singular entrypoint loads Reddit credentials from the root `.env` file at startup without overriding credentials already present in the process environment.
- Subreddits and users are compared case-insensitively while their first observed spelling is retained for display.
- Encounter counts are independent from expansion deduplication, and globally observed submission IDs prevent duplicate observations from inflating frequencies.
- A subreddit is fetched at most once and a user history is fetched at most once.
- The crawler retains identifiers and counters only. Persistent graph storage, ranking, post content, comments, and outreach are outside this feature's ownership boundary.
- Reaching a ceiling stops before the corresponding limit can be exceeded and marks the in-memory result as truncated.

## Relevant Files

- `parameter_files/community_knowledge_graph.toml`: Seeds, sampling sizes, depth, and crawl ceilings.
- `.env.example`: Non-secret template for the required Reddit credentials.
- `src/community_graph/config.py`: Parameter and credential loading.
- `src/community_graph/reddit_client.py`: Project-owned read-only Reddit adapter.
- `src/community_graph/crawler.py`: Bounded breadth-first traversal and result model.
- `src/community_graph/reporting.py`: Deterministic console report.
- `src/main.py`: Singular orchestration entrypoint.
- `tests/test_community_graph_crawler.py`: Fixture-driven traversal and ceiling verification.
- `tests/test_community_graph_reporting.py`: Stable report verification.

## Dev Mode

HACKING

## State Log

- 2026-07-27: Implemented the initial bounded, in-memory Reddit community discovery crawler with deterministic reporting and fixture-only verification.
- 2026-07-27: Added project-root `.env` credential loading during entrypoint startup while preserving process-environment precedence.
