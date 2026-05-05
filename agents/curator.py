import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import anthropic
from news_fetcher import Article


CURATOR_PROMPT = """You are a news curator for an AI briefing tool. Your job is to select 5-7 articles from today's AI news.

Selection criteria:
1. REPRODUCIBILITY: Prefer articles covered by multiple outlets simultaneously — this signals genuine significance, not just one outlet's agenda.
2. DIVERSITY: Across your final selection, ensure variety in subject matter (models, infrastructure, policy, products, research, industry moves). Do NOT enforce a quota — let today's news landscape guide the balance naturally.

You must NOT filter out press releases or promotional content. The tool's identity is "you decide what matters" — curation is about signal strength and variety, not editorial judgment on spin.

Here are today's articles:

{articles_text}

Return a JSON object with this exact structure:
{{
  "selected": [
    {{
      "index": <original index number>,
      "reason": "<one sentence: why this article clears the bar — cite reproducibility signal or diversity contribution>"
    }}
  ]
}}

Select 5-7 articles. Return only the JSON object, no other text."""


def _format_articles(articles: list[Article]) -> str:
    lines = []
    for i, a in enumerate(articles):
        lines.append(f"[{i}] {a.title}")
        lines.append(f"    Source: {a.source}")
        lines.append(f"    URL: {a.url}")
        if a.summary:
            lines.append(f"    Summary: {a.summary[:200]}")
        lines.append("")
    return "\n".join(lines)


def curate(articles: list[Article]) -> list[tuple[Article, str]]:
    """Returns list of (article, reason) tuples for selected articles."""
    client = anthropic.Anthropic()

    articles_text = _format_articles(articles)
    prompt = CURATOR_PROMPT.format(articles_text=articles_text)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    # strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    data = json.loads(raw.strip())

    selected = []
    for item in data["selected"]:
        idx = item["index"]
        reason = item["reason"]
        selected.append((articles[idx], reason))

    return selected


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    from news_fetcher import fetch_all_articles
    print("Fetching articles...")
    articles = fetch_all_articles()
    print(f"Fetched {len(articles)} articles. Running curator...\n")

    selected = curate(articles)
    print(f"Curator selected {len(selected)} articles:\n")
    for article, reason in selected:
        print(f"• [{article.source}] {article.title}")
        print(f"  Reason: {reason}")
        print()
