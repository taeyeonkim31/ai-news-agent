import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import anthropic
from news_fetcher import Article


LENS_CONFIGS = {
    "market": {
        "name": "Market",
        "focus": "market, investment, and business impact",
        "angle": "What does this mean for the industry? Who gains competitive advantage? What business models shift? Follow the money.",
        "others": "Tech (technical novelty), Society (ethics/policy), and User (everyday impact)",
    },
    "tech": {
        "name": "Tech",
        "focus": "technical novelty and actual capability changes",
        "angle": "What is genuinely new here vs. what already existed? Is the claimed capability real or overstated? Separate signal from hype.",
        "others": "Market (business impact), Society (ethics/policy), and User (everyday impact)",
    },
    "society": {
        "name": "Society",
        "focus": "social, ethical, and policy implications",
        "angle": "Who benefits and who is harmed? What power dynamics shift? What regulatory or governance questions arise?",
        "others": "Market (business impact), Tech (technical novelty), and User (everyday impact)",
    },
    "user": {
        "name": "User",
        "focus": "impact on everyday people and how they work",
        "angle": "How does this change what ordinary people can do, or how they spend their time? What becomes easier, harder, or different?",
        "others": "Market (business impact), Tech (technical novelty), and Society (ethics/policy)",
    },
}

LENS_PROMPT = """You are the {name} Lens in a four-perspective AI news briefing tool.

Your focus: {focus}
Your angle: {angle}

The other three lenses ({others}) will cover their own angles independently. Assume they exist — do not repeat what they would cover. Stay in your lane and go deep on yours.

Analyze each of the following articles strictly from your lens. For each article:
- Write one insight line that captures what this news actually reveals from your angle. Frame it as an observation, not a conclusion — the reader decides what to do with it. Start with "The real point here is..." or "What this actually reveals is..." or similar.
- Then write exactly 3 bullets: detail, evidence, context. Each bullet max 2 sentences. Be specific — no filler, no hedging.

Articles:
{articles_text}

Return a JSON object with this exact structure:
{{
  "lens": "{lens_key}",
  "articles": [
    {{
      "index": <original index number>,
      "insight": "<one insight line from the {name} perspective>",
      "bullets": ["<bullet 1>", "<bullet 2>", "<bullet 3>"]
    }}
  ]
}}

Include every article. Return only the JSON object, no other text."""


def _format_articles(articles: list[Article]) -> str:
    lines = []
    for i, a in enumerate(articles):
        lines.append(f"[{i}] {a.title}")
        lines.append(f"    Source: {a.source}")
        if a.summary:
            lines.append(f"    Summary: {a.summary[:300]}")
        lines.append("")
    return "\n".join(lines)


def _parse_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def _run_lens(lens_key: str, articles: list[Article]) -> dict:
    config = LENS_CONFIGS[lens_key]
    client = anthropic.Anthropic()

    prompt = LENS_PROMPT.format(
        lens_key=lens_key,
        name=config["name"],
        focus=config["focus"],
        angle=config["angle"],
        others=config["others"],
        articles_text=_format_articles(articles),
    )

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    return _parse_json(message.content[0].text)


def run_all_lenses(articles: list[Article]) -> dict[str, dict]:
    """Runs all 4 lenses in parallel. Returns {lens_key: lens_output}."""
    results = {}

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(_run_lens, key, articles): key
            for key in LENS_CONFIGS
        }
        for future in as_completed(futures):
            key = futures[future]
            results[key] = future.result()

    return results


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    from news_fetcher import fetch_all_articles
    from agents.curator import curate

    print("Fetching articles...")
    articles = fetch_all_articles()

    print(f"Fetched {len(articles)} articles. Running curator...")
    selected = curate(articles)
    selected_articles = [a for a, _ in selected]

    print(f"Curator selected {len(selected_articles)} articles. Running 4 lenses in parallel...\n")
    lens_results = run_all_lenses(selected_articles)

    for lens_key, result in lens_results.items():
        print(f"=== {lens_key.upper()} LENS ===")
        for item in result["articles"]:
            print(f"[{item['index']}] {selected_articles[item['index']].title[:60]}...")
            print(f"    {item['analysis']}\n")
