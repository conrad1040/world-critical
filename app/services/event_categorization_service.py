CATEGORY_KEYWORDS = {
    "Sports": {
        "wwe",
        "nfl",
        "nba",
        "mlb",
        "espn",
        "game",
        "match",
        "player",
        "dodgers",
        "summerslam",
        "brock lesnar",
    },
    "Conflict": {
        "war",
        "missile",
        "military",
        "strike",
        "strikes",
        "airstrike",
        "airstrikes",
        "invasion",
        "ceasefire",
        "explosion",
        "bomb",
        "gaza",
    },
    "Crime": {
        "shooting",
        "murder",
        "police",
        "gunman",
        "arrest",
    },
    "Natural Disaster": {
        "earthquake",
        "hurricane",
        "tornado",
        "tsunami",
        "wildfire",
        "flood",
        "eruption",
    },
    "Politics": {
        "president",
        "trump",
        "election",
        "government",
        "senate",
        "parliament",
        "minister",
        "court",
        "state department",
        "attorney general",
    },
    "Economy": {
        "stock market",
        "stocks",
        "inflation",
        "interest rate",
        "economy",
        "economic",
        "central bank",
        "federal reserve",
        "kospi",
    },
    "Technology": {
        "software",
        "cyberattack",
        "technology",
        "iphone",
        "pixel",
        "artificial intelligence",
        "computer",
    },
    "Health": {
        "virus",
        "disease",
        "outbreak",
        "vaccine",
        "hospital",
        "health",
    },
    "Entertainment": {
        "actor",
        "movie",
        "music",
        "celebrity",
        "singer",
        "television",
    },
}

import re


def categorize_event(title: str) -> str:
    normalized_title = title.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            pattern = rf"\b{re.escape(keyword)}\b"

            if re.search(pattern, normalized_title):
                return category

    return "Other"

    return "Other"