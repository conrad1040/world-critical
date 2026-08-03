import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_event_text(
    article_titles: list[str],
) -> tuple[str, str]:
    headlines = "\n".join(
        f"- {title}"
        for title in article_titles
    )

    response = client.responses.create(
        model="gpt-5-mini",
        input=(
            "Rewrite these related news headlines into one short, neutral "
            "event title and one concise factual summary.\n\n"
            f"Headlines:\n{headlines}\n\n"
            "Return only valid JSON with exactly these fields:\n"
            "{"
            '"title": "...",'
            '"summary": "..."'
            "}"
        ),
    )

    data = json.loads(response.output_text)

    return (
        str(data["title"]),
        str(data["summary"]),
    )


def generate_editorial_evaluation(
    headlines: list[str],
    source_count: int,
    article_count: int,
    category: str,
    importance_score: int,
) -> dict[str, str]:
    headline_text = "\n".join(
        f"- {title}"
        for title in headlines
    )

    response = client.responses.create(
        model="gpt-5-mini",
        input=(
            "You are the editor for World Critical.\n\n"
            "World Critical helps busy adults identify the few events they "
            "genuinely need to know in order to remain informed about the "
            "world.\n\n"
            "Most newsworthy events are not World Critical events. Do not "
            "promote stories merely because they are tragic, violent, widely "
            "reported, politically controversial, or interesting.\n\n"
            "Evaluate the event using exactly one of these editorial "
            "priorities:\n\n"
            "Critical:\n"
            "- The event clearly deserves a place in today's main briefing.\n"
            "- A broadly informed adult would likely regret completely "
            "missing it.\n"
            "- It has established major national, international, economic, "
            "security, scientific, public-health, or societal consequences.\n\n"
            "Watch:\n"
            "- The event could become broadly consequential.\n"
            "- The current scale, evidence, or implications are not yet clear.\n"
            "- New reporting may justify promoting it to Critical.\n\n"
            "Background:\n"
            "- The event is valid news but does not currently require the "
            "attention of a broad general audience.\n"
            "- This includes routine politics, local crime, isolated "
            "accidents, sports, entertainment, ordinary product releases, "
            "company earnings, and narrow industry news.\n\n"
            "Deaths, violence, the involvement of a famous person, or an "
            "event occurring in a national capital do not automatically make "
            "an event Critical.\n\n"
            "If evidence is limited but the event could plausibly become "
            "nationally or globally significant, choose Watch rather than "
            "Critical.\n\n"
            "Ask yourself:\n"
            "\"If a busy working parent reads only a few stories today, does "
            "this clearly deserve one of those spots?\"\n\n"
            "Use a factual, concise, nonpartisan tone.\n"
            "Do not sensationalize.\n"
            "Do not speculate.\n"
            "Do not invent broader significance.\n"
            "Clearly distinguish established facts from uncertainty.\n\n"
            f"Editorial Context\n\n"
            f"Independent Sources: {source_count}\n"
            f"Articles: {article_count}\n"
            f"Category: {category}\n"
            f"Current Significance Score: {importance_score}\n\n"
            f"Headlines:\n{headline_text}\n\n"
            "Use the editorial context when making your recommendation.\n"
            "The significance score is only one signal and should not "
            "determine the outcome by itself.\n"
            "Treat events supported by only one independent source "
            "cautiously.\n"
            "They often belong in Watch until additional reporting confirms "
            "the scale and significance.\n\n"
            "Return only valid JSON with exactly these fields:\n"
            "{"
            '"summary": "...",'
            '"why_it_matters": "...",'
            '"what_happens_next": "...",'
            '"impact_scope": "Global|National|Regional|Industry|Limited",'
            '"confidence": "High|Medium|Developing",'
            '"editorial_priority": "Critical|Watch|Background",'
            '"reasoning": "A concise internal explanation of the editorial decision."'
            "}"
        ),
    )

    data = json.loads(response.output_text)

    valid_priorities = {
        "Critical",
        "Watch",
        "Background",
    }

    valid_scopes = {
        "Global",
        "National",
        "Regional",
        "Industry",
        "Limited",
    }

    valid_confidence = {
        "High",
        "Medium",
        "Developing",
    }

    editorial_priority = str(
        data["editorial_priority"]
    )

    impact_scope = str(
        data["impact_scope"]
    )

    confidence = str(
        data["confidence"]
    )

    if editorial_priority not in valid_priorities:
        raise ValueError(
            "Invalid editorial priority: "
            f"{editorial_priority}"
        )

    if impact_scope not in valid_scopes:
        raise ValueError(
            f"Invalid impact scope: {impact_scope}"
        )

    if confidence not in valid_confidence:
        raise ValueError(
            f"Invalid confidence: {confidence}"
        )

    return {
        "summary": str(data["summary"]),
        "why_it_matters": str(
            data["why_it_matters"]
        ),
        "what_happens_next": str(
            data["what_happens_next"]
        ),
        "impact_scope": impact_scope,
        "confidence": confidence,
        "editorial_priority": editorial_priority,
        "reasoning": str(data["reasoning"]),
    }


def generate_contextual_match(
    article_title: str,
    event_title: str,
    candidate_titles: list[str],
) -> dict[str, str | bool]:
    existing_titles = "\n".join(
        f"- {title}"
        for title in candidate_titles
    )

    if not existing_titles:
        existing_titles = (
            "- No existing article titles available"
        )

    response = client.responses.create(
        model="gpt-5-mini",
        input=(
            "You are an experienced international news editor.\n\n"
            "Determine whether the new article belongs to the same evolving "
            "news event as the existing event.\n\n"
            "Match only when the articles describe the same underlying "
            "incident or continuing development.\n\n"
            "Do not match stories merely because they share a topic, country, "
            "person, industry, disaster type, or conflict.\n\n"
            f"Existing event title:\n{event_title}\n\n"
            f"Existing coverage:\n{existing_titles}\n\n"
            f"New article title:\n{article_title}\n\n"
            "Return only valid JSON with exactly these fields:\n"
            "{"
            '"match": true,'
            '"confidence": "High|Medium|Low",'
            '"reasoning": "A concise explanation of whether this is the same event."'
            "}"
        ),
    )

    data = json.loads(response.output_text)

    confidence = str(
        data["confidence"]
    )

    if confidence not in {
        "High",
        "Medium",
        "Low",
    }:
        raise ValueError(
            "Invalid contextual-match confidence: "
            f"{confidence}"
        )

    match_value = data["match"]

    if not isinstance(match_value, bool):
        raise ValueError(
            "Contextual match must return a Boolean "
            f"value, received: {match_value!r}"
        )

    return {
        "match": match_value,
        "confidence": confidence,
        "reasoning": str(data["reasoning"]),
    }