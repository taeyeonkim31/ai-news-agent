import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional

from news_fetcher import Article


@dataclass
class ArticleBriefing:
    title: str
    url: str
    source: str
    curator_reason: str
    market: str
    tech: str
    society: str
    user: str


@dataclass
class DailyBriefing:
    date: str
    article_count: int
    articles: list[ArticleBriefing]


def synthesize(
    selected: list[tuple[Article, str]],
    lens_results: dict[str, dict],
) -> DailyBriefing:
    """Assembles per-article briefings from lens outputs. No Claude call — pure assembly."""

    # build lookup: lens_key → {article_index → analysis}
    lens_lookup: dict[str, dict[int, str]] = {}
    for lens_key, result in lens_results.items():
        lens_lookup[lens_key] = {
            item["index"]: item["analysis"]
            for item in result["articles"]
        }

    articles = []
    for i, (article, curator_reason) in enumerate(selected):
        articles.append(ArticleBriefing(
            title=article.title,
            url=article.url,
            source=article.source,
            curator_reason=curator_reason,
            market=lens_lookup.get("market", {}).get(i, ""),
            tech=lens_lookup.get("tech", {}).get(i, ""),
            society=lens_lookup.get("society", {}).get(i, ""),
            user=lens_lookup.get("user", {}).get(i, ""),
        ))

    return DailyBriefing(
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        article_count=len(articles),
        articles=articles,
    )


def save_briefing(briefing: DailyBriefing, output_dir: str = "output") -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{briefing.date}.json")
    with open(path, "w") as f:
        json.dump(asdict(briefing), f, indent=2, ensure_ascii=False)
    return path


def load_latest_briefing(output_dir: str = "output") -> Optional[DailyBriefing]:
    if not os.path.exists(output_dir):
        return None
    files = sorted([f for f in os.listdir(output_dir) if f.endswith(".json")])
    if not files:
        return None
    path = os.path.join(output_dir, files[-1])
    with open(path) as f:
        data = json.load(f)
    return DailyBriefing(
        date=data["date"],
        article_count=data["article_count"],
        articles=[ArticleBriefing(**a) for a in data["articles"]],
    )
