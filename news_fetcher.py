import feedparser
import requests
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass


@dataclass
class Article:
    title: str
    url: str
    source: str
    published: datetime
    summary: str


RSS_SOURCES = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "MIT Technology Review": "https://www.technologyreview.com/feed/",
    "Ars Technica AI": "https://arstechnica.com/ai/feed/",
}

HN_API_URL = "https://hn.algolia.com/api/v1/search_by_date"
HN_AI_KEYWORDS = ["AI", "LLM", "GPT", "Claude", "Gemini", "machine learning",
                   "artificial intelligence", "neural network", "OpenAI", "Anthropic",
                   "deep learning", "language model"]


def _parse_published(entry) -> datetime:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def fetch_rss_articles(hours_back: int = 24) -> list[Article]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_back)
    articles = []

    for source_name, url in RSS_SOURCES.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published = _parse_published(entry)
            if published < cutoff:
                continue
            articles.append(Article(
                title=entry.get("title", "").strip(),
                url=entry.get("link", ""),
                source=source_name,
                published=published,
                summary=entry.get("summary", "")[:500],
            ))

    return articles


def fetch_hn_articles(hours_back: int = 24) -> list[Article]:
    cutoff_ts = int((datetime.now(timezone.utc) - timedelta(hours=hours_back)).timestamp())
    articles = []

    for keyword in HN_AI_KEYWORDS[:5]:  # limit API calls
        params = {
            "query": keyword,
            "tags": "story",
            "numericFilters": f"created_at_i>{cutoff_ts}",
            "hitsPerPage": 20,
        }
        try:
            resp = requests.get(HN_API_URL, params=params, timeout=10)
            resp.raise_for_status()
            hits = resp.json().get("hits", [])
            for hit in hits:
                if not hit.get("url"):
                    continue
                articles.append(Article(
                    title=hit.get("title", "").strip(),
                    url=hit.get("url", ""),
                    source="Hacker News",
                    published=datetime.fromtimestamp(hit["created_at_i"], tz=timezone.utc),
                    summary="",
                ))
        except requests.RequestException:
            continue

    # deduplicate by URL
    seen = set()
    unique = []
    for a in articles:
        if a.url not in seen:
            seen.add(a.url)
            unique.append(a)

    return unique


def fetch_all_articles(hours_back: int = 24) -> list[Article]:
    rss = fetch_rss_articles(hours_back)
    hn = fetch_hn_articles(hours_back)
    all_articles = rss + hn

    # deduplicate across sources by URL
    seen = set()
    unique = []
    for a in all_articles:
        if a.url not in seen:
            seen.add(a.url)
            unique.append(a)

    return sorted(unique, key=lambda a: a.published, reverse=True)


if __name__ == "__main__":
    articles = fetch_all_articles()
    print(f"Fetched {len(articles)} articles\n")
    for a in articles[:10]:
        print(f"[{a.source}] {a.title}")
        print(f"  {a.url}")
        print(f"  {a.published.strftime('%Y-%m-%d %H:%M UTC')}\n")
