"""Load community discovery parameters and Reddit credentials."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


DEFAULT_PARAMETER_FILE = (
    Path(__file__).resolve().parents[2]
    / "parameter_files"
    / "community_knowledge_graph.toml"
)


class ConfigurationError(ValueError):
    """Raised when startup configuration is missing or invalid."""


def normalize_identity(value: str) -> str:
    return value.strip().casefold()


@dataclass(frozen=True)
class CrawlConfig:
    seed_subreddits: tuple[str, ...]
    subreddit_post_limit: int
    user_post_limit: int
    max_depth: int
    max_subreddits: int
    max_users: int
    max_subreddit_fetches: int
    max_user_fetches: int
    max_post_observations: int


@dataclass(frozen=True)
class RedditCredentials:
    client_id: str
    client_secret: str
    user_agent: str


def load_crawl_config(path: Path = DEFAULT_PARAMETER_FILE) -> CrawlConfig:
    try:
        with path.open("rb") as parameter_file:
            values = tomllib.load(parameter_file)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ConfigurationError(f"Could not load parameter file {path}: {error}") from error

    required_limits = (
        "subreddit_post_limit",
        "user_post_limit",
        "max_subreddits",
        "max_users",
        "max_subreddit_fetches",
        "max_user_fetches",
        "max_post_observations",
    )
    for name in required_limits:
        value = values.get(name)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ConfigurationError(f"{name} must be a positive integer")

    max_depth = values.get("max_depth")
    if not isinstance(max_depth, int) or isinstance(max_depth, bool) or max_depth < 0:
        raise ConfigurationError("max_depth must be a non-negative integer")

    raw_seeds = values.get("seed_subreddits")
    if not isinstance(raw_seeds, list):
        raise ConfigurationError("seed_subreddits must be a list")

    seeds_by_identity: dict[str, str] = {}
    for seed in raw_seeds:
        if not isinstance(seed, str) or not normalize_identity(seed):
            raise ConfigurationError("seed_subreddits must contain non-empty strings")
        normalized = normalize_identity(seed)
        seeds_by_identity.setdefault(normalized, seed.strip())

    seeds = tuple(seeds_by_identity.values())
    if not seeds:
        raise ConfigurationError("seed_subreddits must not be empty")
    if len(seeds) > values["max_subreddits"]:
        raise ConfigurationError(
            "The normalized seed count must not exceed max_subreddits"
        )

    return CrawlConfig(
        seed_subreddits=seeds,
        subreddit_post_limit=values["subreddit_post_limit"],
        user_post_limit=values["user_post_limit"],
        max_depth=max_depth,
        max_subreddits=values["max_subreddits"],
        max_users=values["max_users"],
        max_subreddit_fetches=values["max_subreddit_fetches"],
        max_user_fetches=values["max_user_fetches"],
        max_post_observations=values["max_post_observations"],
    )


def load_reddit_credentials(
    environment: Mapping[str, str] = os.environ,
) -> RedditCredentials:
    variable_names = (
        "REDDIT_CLIENT_ID",
        "REDDIT_CLIENT_SECRET",
        "REDDIT_USER_AGENT",
    )
    missing = [name for name in variable_names if not environment.get(name, "").strip()]
    if missing:
        raise ConfigurationError(
            "Missing required Reddit environment variables: " + ", ".join(missing)
        )

    return RedditCredentials(
        client_id=environment["REDDIT_CLIENT_ID"].strip(),
        client_secret=environment["REDDIT_CLIENT_SECRET"].strip(),
        user_agent=environment["REDDIT_USER_AGENT"].strip(),
    )
