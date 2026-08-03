import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_event_text(article_titles: list[str]) -> tuple[str, str]:
    headlines = "\n".join(f"- {title}" for title in article_titles)

    response = client.responses.create(
        model="gpt-5-mini",
        input=(
            "Organize these news headlines into one neutral event.\n\n"
            f"{headlines}\n\n"
            "Return only JSON with two string fields: "
            '"title" and "summary". '
            "The title should be short and neutral. "
            "The summary should be 2 factual sentences. "
            "Do not mention news organizations or speculate."
        ),
    )

    data = json.loads(response.output_text)

    return data["title"], data["summary"]