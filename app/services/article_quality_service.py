import re

BLOCKED_KEYWORDS = {
    "bluray",
    "brrip",
    "bdrip",
    "webrip",
    "web-dl",
    "x264",
    "x265",
    "2160p",
    "1080p",
    "720p",
    "hdrip",
    "dvdrip",
    "torrent",
}

BLOCKED_PHRASES = {
    "newsletter",
    "daily digest",
    "live updates",
    "live blog",
    "what to watch",
    "watch live",
    "score updates",
    "box score",
    "game thread",
    "episode recap",
    "movie review",
    "tv review",
}


def should_ingest_article(
    title: str,
    source_name: str,
) -> bool:
    title_lower = title.lower()

    if len(title_lower) < 15:
        return False

    for keyword in BLOCKED_KEYWORDS:
        if keyword in title_lower:
            return False

    for phrase in BLOCKED_PHRASES:
        if phrase in title_lower:
            return False

    if re.search(
        r"\b(x26[45]|2160p|1080p|720p)\b",
        title_lower,
    ):
        return False

    if source_name.lower() == "reddit":
        return False

    return True