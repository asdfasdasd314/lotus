"""Bounded breadth-first traversal of subreddit and user relationships."""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass, field
from enum import StrEnum

from community_graph.config import CrawlConfig, normalize_identity
from community_graph.reddit_client import RedditReader


class TerminationReason(StrEnum):
    COMPLETED = "completed"
    MAX_SUBREDDITS_REACHED = "max_subreddits_reached"
    MAX_USERS_REACHED = "max_users_reached"
    MAX_SUBREDDIT_FETCHES_REACHED = "max_subreddit_fetches_reached"
    MAX_USER_FETCHES_REACHED = "max_user_fetches_reached"
    MAX_POST_OBSERVATIONS_REACHED = "max_post_observations_reached"


@dataclass
class CrawlResult:
    subreddit_encounters: Counter[str] = field(default_factory=Counter)
    user_encounters: Counter[str] = field(default_factory=Counter)
    processed_subreddits: set[str] = field(default_factory=set)
    expanded_users: set[str] = field(default_factory=set)
    observed_submission_ids: set[str] = field(default_factory=set)
    subreddit_names: dict[str, str] = field(default_factory=dict)
    user_names: dict[str, str] = field(default_factory=dict)
    subreddit_fetch_count: int = 0
    user_fetch_count: int = 0
    post_observation_count: int = 0
    deleted_author_count: int = 0
    maximum_depth_reached: int = 0
    termination_reason: TerminationReason = TerminationReason.COMPLETED
    truncated: bool = False


def crawl(reader: RedditReader, config: CrawlConfig) -> CrawlResult:
    result = CrawlResult()
    queue: deque[tuple[str, int]] = deque()
    queued_subreddits: set[str] = set()

    for seed in config.seed_subreddits:
        normalized = normalize_identity(seed)
        if normalized in queued_subreddits:
            continue
        result.subreddit_names[normalized] = seed.strip()
        result.subreddit_encounters[normalized] += 1
        queued_subreddits.add(normalized)
        queue.append((normalized, 0))

    while queue:
        subreddit_identity, depth = queue.popleft()
        if subreddit_identity in result.processed_subreddits:
            continue
        if result.subreddit_fetch_count >= config.max_subreddit_fetches:
            return _truncate(result, TerminationReason.MAX_SUBREDDIT_FETCHES_REACHED)

        subreddit_name = result.subreddit_names[subreddit_identity]
        submissions = reader.get_recent_subreddit_posts(
            subreddit_name, config.subreddit_post_limit
        )
        result.subreddit_fetch_count += 1
        result.processed_subreddits.add(subreddit_identity)
        result.maximum_depth_reached = max(result.maximum_depth_reached, depth)

        users_to_expand: list[str] = []
        users_scheduled: set[str] = set()
        for submission in submissions:
            if not _begin_observation(result, submission.submission_id, config):
                if result.truncated:
                    return result
                continue

            if not submission.author_name or not submission.author_name.strip():
                result.deleted_author_count += 1
                continue

            user_identity = normalize_identity(submission.author_name)
            if user_identity not in result.user_names:
                if len(result.user_names) >= config.max_users:
                    return _truncate(result, TerminationReason.MAX_USERS_REACHED)
                result.user_names[user_identity] = submission.author_name.strip()
            result.user_encounters[user_identity] += 1

            if (
                depth < config.max_depth
                and user_identity not in result.expanded_users
                and user_identity not in users_scheduled
            ):
                users_scheduled.add(user_identity)
                users_to_expand.append(user_identity)

        if depth >= config.max_depth:
            continue

        for user_identity in users_to_expand:
            if user_identity in result.expanded_users:
                continue
            if result.user_fetch_count >= config.max_user_fetches:
                return _truncate(result, TerminationReason.MAX_USER_FETCHES_REACHED)

            username = result.user_names[user_identity]
            user_submissions = reader.get_recent_user_posts(
                username, config.user_post_limit
            )
            result.user_fetch_count += 1
            result.expanded_users.add(user_identity)

            for submission in user_submissions:
                if not _begin_observation(result, submission.submission_id, config):
                    if result.truncated:
                        return result
                    continue

                subreddit_name = submission.subreddit_name.strip()
                if not subreddit_name:
                    continue
                discovered_identity = normalize_identity(subreddit_name)
                if discovered_identity not in result.subreddit_names:
                    if len(result.subreddit_names) >= config.max_subreddits:
                        return _truncate(
                            result, TerminationReason.MAX_SUBREDDITS_REACHED
                        )
                    result.subreddit_names[discovered_identity] = subreddit_name

                result.subreddit_encounters[discovered_identity] += 1
                if (
                    discovered_identity not in queued_subreddits
                    and discovered_identity not in result.processed_subreddits
                ):
                    queued_subreddits.add(discovered_identity)
                    queue.append((discovered_identity, depth + 1))

    return result


def _begin_observation(
    result: CrawlResult, submission_id: str, config: CrawlConfig
) -> bool:
    if submission_id in result.observed_submission_ids:
        return False
    if result.post_observation_count >= config.max_post_observations:
        _truncate(result, TerminationReason.MAX_POST_OBSERVATIONS_REACHED)
        return False
    result.observed_submission_ids.add(submission_id)
    result.post_observation_count += 1
    return True


def _truncate(
    result: CrawlResult, reason: TerminationReason
) -> CrawlResult:
    result.termination_reason = reason
    result.truncated = True
    return result
