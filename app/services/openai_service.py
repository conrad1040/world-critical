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

def generate_event_update(
    current_summary: str | None,
    current_latest_development: str | None,
    current_why_it_matters: str | None,
    current_what_happens_next: str | None,
    new_articles: list[dict[str, str]],
    source_count: int,
    article_count: int,
    category: str,
    importance_score: int,
) -> dict[str, str]:

    article_text = "\n\n".join(
        (
            f"Title: {article['title']}\n"
            f"Description: {article['description']}"
        )
        for article in new_articles
    )

    response = client.responses.create(
        model="gpt-5-mini",
        input=(
            "You are the senior editor for World Critical.\n\n"

            "You are maintaining an existing news event.\n"
            "Do NOT rewrite everything.\n"
            "Preserve wording that is still accurate.\n"
            "Only update sections that materially changed.\n\n"

            "Editorial Priority Rules\n\n"

            "Do not increase editorial priority simply because additional "
            "articles confirmed an event.\n"

            "Additional confirmation should usually increase confidence, "
            "not editorial priority.\n"

            "A story becomes more important only if the new reporting "
            "materially changes its significance or consequences.\n"

            "Deaths, violence, famous people, or an event occurring in a "
            "national capital do not automatically justify Critical.\n"

            "Critical is reserved for events a broadly informed adult "
            "would likely regret completely missing today.\n"

            "If uncertain between Critical and Watch, prefer Watch.\n\n"

            "CURRENT EVENT\n\n"

            f"Summary:\n{current_summary or 'None'}\n\n"
            f"Latest Development:\n"
            f"{current_latest_development or 'None'}\n\n"
            f"Why It Matters:\n"
            f"{current_why_it_matters or 'None'}\n\n"
            f"What Happens Next:\n"
            f"{current_what_happens_next or 'None'}\n\n"

            "NEW REPORTING\n\n"
            f"{article_text}\n\n"

            "Editorial Context\n\n"
            f"Independent Sources: {source_count}\n"
            f"Articles: {article_count}\n"
            f"Category: {category}\n"
            f"Importance Score: {importance_score}\n\n"

            "Update the event only where necessary.\n"
            "If nothing important changed, keep the existing wording.\n"

            "If the new reporting only confirms previously known facts, "
            "leave the summary largely unchanged and update confidence "
            "instead.\n\n"
            "Return only valid JSON with exactly these fields:\n"
            "{"
            '"summary":"...",'
            '"latest_development":"...",'
            '"why_it_matters":"...",'
            '"what_happens_next":"...",'
            '"impact_scope":"Global|National|Regional|Industry|Limited",'
            '"confidence":"High|Medium|Developing",'
            '"editorial_priority":"Critical|Watch|Background",'
            '"reasoning":"..."'
            "}"
        ),
    )

    data = json.loads(response.output_text)

    return {
        "summary": str(data["summary"]),
        "latest_development": str(
            data["latest_development"]
        ),
        "why_it_matters": str(
            data["why_it_matters"]
        ),
        "what_happens_next": str(
            data["what_happens_next"]
        ),
        "impact_scope": str(
            data["impact_scope"]
        ),
        "confidence": str(
            data["confidence"]
        ),
        "editorial_priority": str(
            data["editorial_priority"]
        ),
        "reasoning": str(
            data["reasoning"]
        ),
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

def generate_world_critical_decision(
    article_title: str,
    article_description: str | None,
) -> dict[str, str | bool]:
    response = client.responses.create(
        model="gpt-5-mini",
        input=(
            "You are the first editor for World Critical.\n\n"
            "World Critical exists because modern news overwhelms readers "
            "with stories that do not meaningfully improve their understanding "
            "of the world.\n\n"
            "Your job is not to decide whether the article is technically "
            "newsworthy. Your job is to decide whether it deserves to enter "
            "the World Critical event pipeline at all.\n\n"
            "Ask this question:\n"
            "\"If a busy adult completely missed this story, would they likely "
            "be meaningfully less informed about the world?\"\n\n"
            "Most articles should be rejected.\n\n"
            "Approve only articles that describe a concrete development with "
            "meaningful national or international consequences, or a realistic "
            "chance of becoming broadly consequential.\n\n"
            "Reject articles that are primarily:\n"
            "- sports results, trades, recruiting, previews, or commentary\n"
            "- entertainment or celebrity news\n"
            "- consumer advice, health advice, relationship advice, or Q&A\n"
            "- reviews, rankings, trivia, listicles, or how-to articles\n"
            "- opinion, editorials, commentary, or vague analysis\n"
            "- routine earnings, stock commentary, or narrow industry news\n"
            "- product launches, software releases, package listings, or auctions\n"
            "- local crime or local politics without broader consequences\n"
            "- routine weather information without major disruption\n\n"
            "Do not approve something merely because it involves death, "
            "violence, a famous person, politics, health, technology, or money.\n\n"
            "Base the decision only on what the headline clearly establishes. "
            "Do not invent or assume wider consequences, scale, severity, or public impact.\n\n"

            "Routine company financial harm is not enough to approve an article. "
            "A food-safety story should be approved only when the headline clearly shows "
            "a major outbreak, widespread illness, deaths, a large recall, government "
            "action, or substantial public-health consequences. A story mainly about "
            "damage to a company's sales, stock, earnings, or reputation should usually "
            "be rejected.\n\n"
            "Examples:\n"
            '- "WHO declares global public health emergency" -> approve\n'
            '- "Major hospital network disrupted by ransomware" -> approve\n'
            '- "Taco Bell outbreak hurts parent company earnings" -> reject\n'
            '- "Restaurant chain recalls food after hundreds become ill" -> approve\n'
            '- "Company shares fall after disappointing trial" -> reject unless the '
            "headline establishes major public-health consequences\n\n"
            "When uncertain, reject it. Preserving the reader's attention is "
            "more important than being comprehensive.\n\n"
            "Use neutral language in the reason. Avoid loaded labels, emotional "
            "framing, political characterizations, or telling the reader what "
            "to think.\n\n"
            f"Article title:\n{article_title}\n\n"
            f"Article description:\n"
            f"{article_description or 'No description available.'}\n\n"
            "Return only valid JSON with exactly these fields:\n"
            "{"
            '"should_create_event": true,'
            '"reason": "A concise explanation.",'
            '"rejection_category": "Sports|Entertainment|Celebrity|Consumer Advice|Opinion|Routine Business|Routine Politics|Software Release|Local News|Weather|Other"'
            "}"
        ),
    )



    data = json.loads(response.output_text)

    should_create_event = data["should_create_event"]

    if not isinstance(should_create_event, bool):
        raise ValueError(
            "World Critical decision must return a Boolean value, "
            f"received: {should_create_event!r}"
        )

    return {
    "should_create_event": should_create_event,
    "reason": str(data["reason"]),
    "rejection_category": str(
        data.get(
            "rejection_category",
            "",
        )
    ),
}

def generate_event_merge_decision(
    event_a_title: str,
    event_a_summary: str,
    event_b_title: str,
    event_b_summary: str,
) -> dict[str, str | bool]:
    response = client.responses.create(
        model="gpt-5-mini",
        input=(
            "You are the senior editor for World Critical.\n\n"
            "Determine whether these two Event objects represent "
            "the SAME evolving real-world event.\n\n"
            "Merge events when they describe different reporting, "
            "updates, or perspectives on the same underlying "
            "development.\n\n"
            "Do NOT merge events merely because they involve the "
            "same country, person, company, conflict, or topic.\n\n"
            "Examples that SHOULD merge:\n"
            "- Trump pauses Iran strikes\n"
            "- Congress lacks briefing on Iran strike plans\n\n"
            "- Helicopters collide fighting Greece wildfires\n"
            "- Two firefighters killed after firefighting helicopters collide\n\n"
            "Examples that should NOT merge:\n"
            "- Greece wildfire\n"
            "- Greece earthquake\n\n"
            "- Trump tariffs\n"
            "- Trump immigration order\n\n"
            "- Russia sanctions\n"
            "- Russia earthquake\n\n"
            f"Event A Title:\n{event_a_title}\n\n"
            f"Event A Summary:\n{event_a_summary}\n\n"
            f"Event B Title:\n{event_b_title}\n\n"
            f"Event B Summary:\n{event_b_summary}\n\n"
            "Return ONLY valid JSON:\n"
            "{"
            '"merge": true,'
            '"confidence": "High|Medium|Low",'
            '"reasoning": "..."'
            "}"
        ),
    )

    data = json.loads(response.output_text)

    confidence = str(data["confidence"])

    if confidence not in {
        "High",
        "Medium",
        "Low",
    }:
        raise ValueError(
            f"Invalid merge confidence: {confidence}"
        )

    merge = data["merge"]

    if not isinstance(merge, bool):
        raise ValueError(
            f"Merge must be Boolean, got {merge!r}"
        )

    return {
        "merge": merge,
        "confidence": confidence,
        "reasoning": str(data["reasoning"]),
    }