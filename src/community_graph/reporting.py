"""Deterministic text reporting for crawl results."""

from __future__ import annotations

from collections import Counter

from community_graph.crawler import CrawlResult


def render_report(result: CrawlResult) -> str:
    termination = result.termination_reason.value.replace("_reached", " reached")
    lines = [
        "Community discovery complete",
        "",
        f"Termination: {termination}",
        f"Truncated: {'yes' if result.truncated else 'no'}",
        f"Maximum depth reached: {result.maximum_depth_reached}",
        "",
        f"Unique subreddits discovered: {len(result.subreddit_names)}",
        f"Subreddits processed: {len(result.processed_subreddits)}",
        f"Unique users discovered: {len(result.user_names)}",
        f"Users expanded: {len(result.expanded_users)}",
        f"Post observations: {result.post_observation_count}",
        f"Subreddit fetches: {result.subreddit_fetch_count}",
        f"User-history fetches: {result.user_fetch_count}",
        f"Deleted authors skipped: {result.deleted_author_count}",
    ]
    if result.truncated:
        lines.extend(
            [
                "",
                "Results describe a bounded sample, not the complete reachable network.",
            ]
        )

    lines.extend(
        [
            "",
            "Subreddit encounters",
            *_render_frequency_table(
                "subreddit", result.subreddit_encounters, result.subreddit_names
            ),
            "",
            "User encounters",
            *_render_frequency_table(
                "username", result.user_encounters, result.user_names
            ),
        ]
    )
    return "\n".join(lines)


def _render_frequency_table(
    entity_header: str, encounters: Counter[str], display_names: dict[str, str]
) -> list[str]:
    rows = sorted(encounters.items(), key=lambda item: (-item[1], item[0]))
    count_width = max([5, *(len(str(count)) for _, count in rows)])
    name_width = max(
        [len(entity_header), *(len(display_names[identity]) for identity, _ in rows)]
    )
    rendered = [
        f"{'count':<{count_width}}  {entity_header}",
        f"{'-' * count_width}  {'-' * name_width}",
    ]
    rendered.extend(
        f"{count:<{count_width}}  {display_names[identity]}"
        for identity, count in rows
    )
    return rendered
