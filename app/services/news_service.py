import requests

from app.database.config import NEWS_API_KEY

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"


def fetch_top_headlines(page_size: int = 5) -> list[dict]:
    params = {
        "country": "us",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY,
    }

    response = requests.get(
        NEWS_API_URL,
        params=params,
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    return data.get("articles", [])