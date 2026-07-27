from collections import Counter

from community_graph.crawler import CrawlResult, TerminationReason
from community_graph.reporting import render_report


def test_report_contains_summary_warning_and_deterministic_frequency_order():
    result = CrawlResult(
        subreddit_encounters=Counter({"zulu": 2, "alpha": 2, "beta": 1}),
        user_encounters=Counter({"zoe": 3, "amy": 3}),
        processed_subreddits={"alpha", "beta"},
        expanded_users={"amy"},
        observed_submission_ids={"1", "2", "3"},
        subreddit_names={"zulu": "Zulu", "alpha": "Alpha", "beta": "Beta"},
        user_names={"zoe": "Zoe", "amy": "Amy"},
        subreddit_fetch_count=2,
        user_fetch_count=1,
        post_observation_count=3,
        deleted_author_count=1,
        maximum_depth_reached=2,
        termination_reason=TerminationReason.MAX_SUBREDDITS_REACHED,
        truncated=True,
    )

    report = render_report(result)

    assert "Termination: max_subreddits reached" in report
    assert "Truncated: yes" in report
    assert "Maximum depth reached: 2" in report
    assert "Unique subreddits discovered: 3" in report
    assert "Subreddits processed: 2" in report
    assert "Unique users discovered: 2" in report
    assert "Users expanded: 1" in report
    assert "Results describe a bounded sample" in report
    assert report.index("2      Alpha") < report.index("2      Zulu")
    assert report.index("3      Amy") < report.index("3      Zoe")


def test_completed_report_has_no_truncation_warning():
    result = CrawlResult(
        subreddit_encounters=Counter({"seed": 1}),
        subreddit_names={"seed": "Seed"},
    )

    report = render_report(result)

    assert "Termination: completed" in report
    assert "Truncated: no" in report
    assert "bounded sample" not in report
