from types import SimpleNamespace

import pytest

from community_graph.reddit_client import PrawRedditReader, RedditClientError


class FakeUserSubmissions:
    def __init__(self, error):
        self.error = error

    def new(self, limit):
        raise self.error


class FakeReddit:
    def __init__(self, error):
        self.error = error

    def redditor(self, username):
        return SimpleNamespace(submissions=FakeUserSubmissions(self.error))


def reader_with_error(status_code):
    error = RuntimeError(f"received {status_code} HTTP response")
    error.response = SimpleNamespace(status_code=status_code)
    reader = PrawRedditReader.__new__(PrawRedditReader)
    reader._reddit = FakeReddit(error)
    return reader


def test_missing_user_history_is_treated_as_empty():
    reader = reader_with_error(404)

    assert reader.get_recent_user_posts("MissingUser", 10) == []


def test_other_user_history_errors_remain_fatal():
    reader = reader_with_error(500)

    with pytest.raises(
        RedditClientError,
        match="Could not fetch recent posts for u/UnavailableUser",
    ):
        reader.get_recent_user_posts("UnavailableUser", 10)
