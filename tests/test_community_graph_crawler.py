from dataclasses import replace

import pytest

from community_graph.config import CrawlConfig
from community_graph.crawler import TerminationReason, crawl
from community_graph.reddit_client import PostObservation


def post(
    submission_id: str,
    author: str | None = "author",
    subreddit: str = "seed",
) -> PostObservation:
    return PostObservation(submission_id, author, subreddit)


class FakeRedditReader:
    def __init__(self, subreddits=None, users=None):
        self.subreddits = subreddits or {}
        self.users = users or {}
        self.subreddit_calls = []
        self.user_calls = []

    def get_recent_subreddit_posts(self, subreddit, limit):
        self.subreddit_calls.append((subreddit, limit))
        return self.subreddits.get(subreddit.casefold(), [])[:limit]

    def get_recent_user_posts(self, username, limit):
        self.user_calls.append((username, limit))
        return self.users.get(username.casefold(), [])[:limit]


@pytest.fixture
def config():
    return CrawlConfig(
        seed_subreddits=("Seed",),
        subreddit_post_limit=10,
        user_post_limit=10,
        max_depth=3,
        max_subreddits=20,
        max_users=20,
        max_subreddit_fetches=20,
        max_user_fetches=20,
        max_post_observations=100,
    )


def test_seed_names_are_normalized_and_processed_once(config):
    reader = FakeRedditReader()

    result = crawl(
        reader,
        replace(config, seed_subreddits=("Seed", " seed ", "SEED")),
    )

    assert reader.subreddit_calls == [("Seed", 10)]
    assert result.subreddit_names == {"seed": "Seed"}
    assert result.subreddit_encounters == {"seed": 1}
    assert result.termination_reason is TerminationReason.COMPLETED


def test_repeated_user_encounters_have_one_history_fetch(config):
    reader = FakeRedditReader(
        subreddits={
            "seed": [
                post("s1", "Alice"),
                post("s2", "ALICE"),
            ]
        },
        users={"alice": []},
    )

    result = crawl(reader, config)

    assert result.user_encounters == {"alice": 2}
    assert result.user_names == {"alice": "Alice"}
    assert reader.user_calls == [("Alice", 10)]


def test_repeated_subreddit_encounters_have_one_queue_entry_and_fetch(config):
    reader = FakeRedditReader(
        subreddits={
            "seed": [post("s1", "Alice"), post("s2", "Bob")],
            "shared": [],
        },
        users={
            "alice": [post("a1", subreddit="Shared")],
            "bob": [post("b1", subreddit="SHARED")],
        },
    )

    result = crawl(reader, config)

    assert result.subreddit_encounters["shared"] == 2
    assert result.subreddit_names["shared"] == "Shared"
    assert [call[0].casefold() for call in reader.subreddit_calls].count("shared") == 1
    assert len(result.processed_subreddits) == 2


def test_breadth_first_traversal_respects_depth_and_counts_boundary_users(config):
    reader = FakeRedditReader(
        subreddits={
            "seed": [post("s1", "Alice")],
            "levelone": [post("l1", "Bob", "LevelOne")],
            "leveltwo": [post("l2", "Carol", "LevelTwo")],
        },
        users={
            "alice": [post("a1", subreddit="LevelOne")],
            "bob": [post("b1", subreddit="LevelTwo")],
            "carol": [post("c1", subreddit="TooDeep")],
        },
    )

    result = crawl(reader, replace(config, max_depth=1))

    assert [call[0] for call in reader.subreddit_calls] == ["Seed", "LevelOne"]
    assert reader.user_calls == [("Alice", 10)]
    assert result.user_encounters == {"alice": 1, "bob": 1}
    assert "bob" not in result.expanded_users
    assert "leveltwo" not in result.subreddit_names
    assert result.maximum_depth_reached == 1


def test_deleted_authors_are_skipped(config):
    reader = FakeRedditReader(
        subreddits={"seed": [post("s1", None), post("s2", "  ")]}
    )

    result = crawl(reader, config)

    assert result.deleted_author_count == 2
    assert result.user_names == {}
    assert reader.user_calls == []


def test_duplicate_submission_ids_do_not_inflate_any_counter(config):
    duplicate = post("same", "Alice")
    reader = FakeRedditReader(
        subreddits={"seed": [duplicate, duplicate]},
        users={"alice": [post("same", subreddit="Other")]},
    )

    result = crawl(reader, config)

    assert result.post_observation_count == 1
    assert result.user_encounters == {"alice": 1}
    assert "other" not in result.subreddit_names
    assert result.observed_submission_ids == {"same"}


@pytest.mark.parametrize(
    ("changes", "reader", "reason"),
    [
        (
            {"max_subreddits": 1},
            FakeRedditReader(
                subreddits={"seed": [post("s1", "Alice")]},
                users={"alice": [post("a1", subreddit="New")]},
            ),
            TerminationReason.MAX_SUBREDDITS_REACHED,
        ),
        (
            {"max_users": 1},
            FakeRedditReader(
                subreddits={"seed": [post("s1", "Alice"), post("s2", "Bob")]}
            ),
            TerminationReason.MAX_USERS_REACHED,
        ),
        (
            {"max_subreddit_fetches": 1},
            FakeRedditReader(
                subreddits={"seed": [post("s1", "Alice")]},
                users={"alice": [post("a1", subreddit="New")]},
            ),
            TerminationReason.MAX_SUBREDDIT_FETCHES_REACHED,
        ),
        (
            {"max_user_fetches": 1},
            FakeRedditReader(
                subreddits={"seed": [post("s1", "Alice"), post("s2", "Bob")]},
                users={"alice": [], "bob": []},
            ),
            TerminationReason.MAX_USER_FETCHES_REACHED,
        ),
        (
            {"max_post_observations": 1},
            FakeRedditReader(
                subreddits={"seed": [post("s1", "Alice"), post("s2", "Bob")]},
                users={"alice": []},
            ),
            TerminationReason.MAX_POST_OBSERVATIONS_REACHED,
        ),
    ],
)
def test_each_hard_ceiling_stops_without_overshooting(
    config, changes, reader, reason
):
    result = crawl(reader, replace(config, **changes))

    assert result.termination_reason is reason
    assert result.truncated is True
    assert len(result.subreddit_names) <= changes.get(
        "max_subreddits", config.max_subreddits
    )
    assert len(result.user_names) <= changes.get("max_users", config.max_users)
    assert result.subreddit_fetch_count <= changes.get(
        "max_subreddit_fetches", config.max_subreddit_fetches
    )
    assert result.user_fetch_count <= changes.get(
        "max_user_fetches", config.max_user_fetches
    )
    assert result.post_observation_count <= changes.get(
        "max_post_observations", config.max_post_observations
    )


def test_exhausted_queue_completes(config):
    result = crawl(FakeRedditReader(), config)

    assert result.termination_reason is TerminationReason.COMPLETED
    assert result.truncated is False
    assert result.subreddit_fetch_count == 1
    assert result.user_fetch_count == 0
