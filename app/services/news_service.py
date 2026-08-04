from datetime import datetime, timedelta, timezone

import requests

from app.database.config import NEWS_API_KEY

TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
EVERYTHING_URL = "https://newsapi.org/v2/everything"

REQUEST_TIMEOUT_SECONDS = 20


class NewsApiRateLimitError(RuntimeError):
    """NewsAPI quota or rate limit exceeded."""

# These queries improve discovery only.
# The editorial engine still decides Critical / Watch / Background.
WORLD_CRITICAL_QUERIES = [
    # Conflict, war, and national security
    (
        "war OR invasion OR ceasefire OR coup OR missile "
        "OR sanctions OR military OR airstrike OR hostage"
    ),

    # Natural disasters and major infrastructure disruption
    (
        "earthquake OR tsunami OR hurricane OR cyclone "
        "OR wildfire OR evacuation OR \"power outage\" "
        "OR flood OR landslide"
    ),

    # Public health
    (
        "outbreak OR pandemic OR epidemic OR "
        "\"public health emergency\" OR \"drug-resistant\" "
        "OR WHO OR CDC"
    ),

    # Economy and financial systems
    (
        "\"interest rate\" OR recession OR inflation OR "
        "\"financial crisis\" OR \"central bank\" "
        "OR \"bank failure\""
    ),

    # Major government and legal developments
    (
        "\"state of emergency\" OR \"president resigns\" OR "
        "\"prime minister resigns\" OR election OR coup OR "
        "\"supreme court\" OR \"constitutional court\""
    ),

    # Cybersecurity and critical technology
    (
        "cyberattack OR ransomware OR \"critical infrastructure\" "
        "OR \"data breach\" OR \"power grid\""
    ),
]


def _request_articles(
    url: str,
    params: dict,
) -> list[dict]:
    if not NEWS_API_KEY:
        raise RuntimeError(
            "NEWS_API_KEY is missing. Add it to your .env file."
        )

    response = requests.get(
        url,
        params=params,
        headers={"X-Api-Key": NEWS_API_KEY},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    if response.status_code == 429:
        raise NewsApiRateLimitError(
            "NewsAPI rate limit reached."
        )

    response.raise_for_status()

    data = response.json()

    if data.get("status") != "ok":
        message = data.get(
            "message",
            "Unknown NewsAPI error",
        )
        raise RuntimeError(
            f"NewsAPI request failed: {message}"
        )

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
    oldest_time = (
        datetime.now(timezone.utc)
        - timedelta(days=lookback_days)
    )

    return _request_articles(
        EVERYTHING_URL,
        {
            "q": query,
            "searchIn": "title,description",
            "language": "en",
            "from": oldest_time.isoformat(
                timespec="seconds"
            ),
            "sortBy": "publishedAt",
            "pageSize": min(page_size, 100),
            "page": 1,
        },
    )


def fetch_world_news(
    page_size: int = 50,
) -> list[dict]:
    articles: list[dict] = []

    try:
        articles.extend(
            fetch_top_headlines(
                page_size=page_size,
            )
        )
    except NewsApiRateLimitError:
        print(
            "NewsAPI rate limit reached. "
            "Skipping ingestion for this run."
        )
        return []

    for query in WORLD_CRITICAL_QUERIES:
        try:
            articles.extend(
                fetch_topic_articles(
                    query=query,
                    page_size=page_size,
                )
            )
        except NewsApiRateLimitError:
            print(
                "NewsAPI rate limit reached. "
                "Using articles fetched so far."
            )
            break

    # The same article may appear in several searches.
    # Deduplicate by URL before ingestion.
    unique_articles: dict[str, dict] = {}

    for article in articles:
        url = article.get("url")

        if not url:
            continue

        unique_articles[url] = article

    return list(unique_articles.values())