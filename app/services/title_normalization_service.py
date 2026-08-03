import re

SOURCE_SUFFIXES = [
    "associated press",
    "ap news",
    "al jazeera",
    "al jazeera english",
    "bloomberg",
    "bloomberg com",
    "cnn",
    "bbc",
    "bbc news",
    "cbs news",
    "nbc news",
    "abc news",
    "fox news",
    "reuters",
    "the guardian",
    "the washington post",
    "washingtonpost com",
    "hindustan times",
    "new york times",
    "the new york times",
]

NOISE_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "live",
    "latest",
    "near",
    "of",
    "on",
    "says",
    "say",
    "the",
    "to",
    "update",
    "updates",
    "with",
}

TOKEN_ALIASES = {
    "wildfires": "wildfire",
    "fires": "fire",

    "explosions": "explosion",
    "blasts": "explosion",
    "blast": "explosion",

    "killed": "kill",
    "kills": "kill",
    "deaths": "death",

    "injured": "injury",
    "injuries": "injury",

    "evacuate": "evacuation",
    "evacuated": "evacuation",
    "evacuates": "evacuation",
    "evacuations": "evacuation",

    "destroy": "destroy",
    "destroys": "destroy",
    "destroyed": "destroy",
    "destruction": "destroy",

    "building": "structure",
    "buildings": "structure",
    "structures": "structure",

    "spread": "spread",
    "spreads": "spread",
    "spreading": "spread",
}


def _remove_source_suffix(title: str) -> str:
    cleaned = title.strip()

    for source in SOURCE_SUFFIXES:
        pattern = rf"\s*[-|:]\s*{re.escape(source)}\s*$"
        cleaned = re.sub(
            pattern,
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

    return cleaned


def _normalize_token(token: str) -> str:
    return TOKEN_ALIASES.get(token, token)


def normalize_title(title: str) -> str:
    normalized = _remove_source_suffix(title)
    normalized = normalized.lower()

    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    tokens = [
        _normalize_token(token)
        for token in normalized.split()
        if token not in NOISE_WORDS
    ]

    return " ".join(tokens)