from datetime import datetime, timedelta, timezone

import requests

from app.database.config import NEWS_API_KEY

TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
EVERYTHING_URL = "https://newsapi.org/v2/everything"

REQUEST_TIMEOUT_SECONDS = 20

# These are discovery searches, not editorial rules.
# The editorial engine still decides Critical / Watch / Background.
WORLD_CRITICAL_QUERIES = [
    (
        "war OR invasion OR ceasefire OR coup OR missile "
        "OR sanctions OR military"
    ),
    (
        "earthquake OR tsunami OR hurricane OR cyclone "
        "OR wildfire OR evacuation OR \"power outage\""
    ),
    (
        "outbreak OR pandemic OR epidemic OR "
        "\"public health emergency\" OR \"drug-resistant\""
    ),
    (
        "\"interest rate\" OR recession OR \"financial crisis\" "
        "OR cyberattack OR \"state of emergency\" "
        "OR \"president resigns\" OR \"prime minister resigns\""
    ),
]


def _request_articles(
    url: str,
    params: dict,
) -> list[dict]:
    response = requests.get(
        url,
        params=params,
        headers={"X-Api-Key": NEWS_API_KEY},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    data = response.json()

    if data.get("status") != "ok":
        message = data.get("message", "Unknown NewsAPI error")
        raise RuntimeError(f"NewsAPI request failed: {message}")

    return data.get("articles", [])


def fetch_top_headlines(
    page_size: int = 50,
) -> list[dict]:
    return _request_articles(
        TOP_HEADLINES_URL,
        {
            "country": "us",
            "category": "general",
            "pageSize": min(page_size, 100),
            "page": 1,
        },
    )


def fetch_topic_articles(
    query: str,
    page_size: int = 50,
    lookback_days: int = 3,
) -> list[dict]:
    oldest_time = datetime.now(timezone.utc) - timedelta(
        days=lookback_days
    )

    return _request_articles(
        EVERYTHING_URL,
        {
            "q": query,
            "searchIn": "title,description",
            "language": "en",
            "from": oldest_time.isoformat(timespec="seconds"),
            "sortBy": "publishedAt",
            "pageSize": min(page_size, 100),
            "page": 1,
        },
    )


def fetch_world_news(
    page_size: int = 50,
) -> list[dict]:
    articles: list[dict] = []

    # General U.S. breaking headlines.
    articles.extend(
        fetch_top_headlines(page_size=page_size)
    )

    # Broader international and topic-based discovery.
    for query in WORLD_CRITICAL_QUERIES:
        articles.extend(
            fetch_topic_articles(
                query=query,
                page_size=page_size,
            )
        )

    # One story can appear in several searches.
    # Keep only one copy of each URL.
    unique_articles: dict[str, dict] = {}

    for article in articles:
        url = article.get("url")

        if not url:
            continue

        unique_articles[url] = article

    return list(unique_articles.values())