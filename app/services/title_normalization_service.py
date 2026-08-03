import re

SOURCE_SUFFIXES = [
    "associated press",
    "ap news",
    "al jazeera",
    "al jazeera english",
    "bloomberg",
    "bloomberg com",
    "washingtonpost com",
    "the washington post",
    "hindustan times",
]


def normalize_title(title: str) -> str:
    normalized = title.lower()

    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    for source in SOURCE_SUFFIXES:
        normalized = normalized.replace(source, "")

    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized