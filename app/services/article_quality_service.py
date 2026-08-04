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

    # Package and repository listings
    "added to pypi",
    "released on pypi",
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

    # Reject package/version listings such as:
    # "data-breach-detector 0.3.1"
    if re.search(
        r"\b[a-z0-9_-]+\s+v?\d+\.\d+(?:\.\d+)?\b",
        title_lower,
    ):
        return False

    # Reject technical malware-help or sample-identification posts.
    if (
        "ransomware" in title_lower
        and (
            "extension" in title_lower
            or " ext" in title_lower
            or "originalfilename" in title_lower
            or "ransom note" in title_lower
            or "decrypt" in title_lower
            or "locked-" in title_lower
            or "@" in title_lower
        )
    ):
        return False

    return True