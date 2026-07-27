"""Singular entrypoint for bounded Reddit community discovery."""

from community_graph.config import (
    ConfigurationError,
    load_crawl_config,
    load_reddit_credentials,
)
from community_graph.crawler import crawl
from community_graph.reddit_client import PrawRedditReader, RedditClientError
from community_graph.reporting import render_report


def main() -> int:
    try:
        config = load_crawl_config()
        credentials = load_reddit_credentials()
        reader = PrawRedditReader(credentials)
        result = crawl(reader, config)
    except ConfigurationError as error:
        print(f"Configuration/authentication error: {error}")
        return 2
    except RedditClientError as error:
        print(f"Reddit API error: {error}")
        return 3

    print(render_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
