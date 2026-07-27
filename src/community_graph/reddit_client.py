"""Small read-only boundary around PRAW."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from community_graph.config import RedditCredentials


@dataclass(frozen=True)
class PostObservation:
    submission_id: str
    author_name: str | None
    subreddit_name: str


class RedditReader(Protocol):
    def get_recent_subreddit_posts(
        self, subreddit: str, limit: int
    ) -> list[PostObservation]: ...

    def get_recent_user_posts(
        self, username: str, limit: int
    ) -> list[PostObservation]: ...


class RedditClientError(RuntimeError):
    """Raised when Reddit cannot serve a requested listing."""


class PrawRedditReader:
    def __init__(self, credentials: RedditCredentials) -> None:
        try:
            import praw
        except ImportError as error:
            raise RedditClientError(
                "The 'praw' package is required. Install project dependencies first."
            ) from error

        self._reddit = praw.Reddit(
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            user_agent=credentials.user_agent,
            check_for_async=False,
        )
        self._reddit.read_only = True

    def get_recent_subreddit_posts(
        self, subreddit: str, limit: int
    ) -> list[PostObservation]:
        try:
            submissions = self._reddit.subreddit(subreddit).new(limit=limit)
            return [self._to_observation(submission) for submission in submissions]
        except Exception as error:
            raise RedditClientError(
                f"Could not fetch recent posts for r/{subreddit}: {error}"
            ) from error

    def get_recent_user_posts(
        self, username: str, limit: int
    ) -> list[PostObservation]:
        try:
            submissions = self._reddit.redditor(username).submissions.new(limit=limit)
            return [self._to_observation(submission) for submission in submissions]
        except Exception as error:
            response = getattr(error, "response", None)
            if getattr(response, "status_code", None) == 404:
                return []
            raise RedditClientError(
                f"Could not fetch recent posts for u/{username}: {error}"
            ) from error

    @staticmethod
    def _to_observation(submission: object) -> PostObservation:
        author = getattr(submission, "author", None)
        subreddit = getattr(submission, "subreddit")
        subreddit_name = getattr(subreddit, "display_name", str(subreddit))
        return PostObservation(
            submission_id=str(getattr(submission, "id")),
            author_name=str(author) if author is not None else None,
            subreddit_name=str(subreddit_name),
        )
