import os
import sys
from dotenv import load_dotenv

load_dotenv()

from news_fetcher import fetch_all_articles
from agents.curator import curate
from agents.lenses import run_all_lenses
from agents.synthesizer import synthesize, save_briefing


def run_pipeline() -> str:
    print("=== AI News Briefing Pipeline ===\n")

    print("Step 1/4: Fetching articles...")
    articles = fetch_all_articles()
    print(f"  Fetched {len(articles)} articles\n")

    print("Step 2/4: Curating...")
    selected = curate(articles)
    print(f"  Selected {len(selected)} articles:")
    for article, reason in selected:
        print(f"  • {article.title[:70]}")
    print()

    print("Step 3/4: Running 4 lenses in parallel...")
    selected_articles = [a for a, _ in selected]
    lens_results = run_all_lenses(selected_articles)
    print(f"  Lenses complete: {', '.join(lens_results.keys())}\n")

    print("Step 4/4: Synthesizing...")
    briefing = synthesize(selected, lens_results)
    path = save_briefing(briefing)
    print(f"  Briefing saved to {path}\n")

    print("=== Done ===")
    print(f"Date: {briefing.date}")
    print(f"Articles: {briefing.article_count}")
    print()

    for article in briefing.articles:
        print(f"{'='*60}")
        print(f"{article.title}")
        print(f"Source: {article.source} | {article.url}")
        print(f"\nMarket:  {article.market}")
        print(f"\nTech:    {article.tech}")
        print(f"\nSociety: {article.society}")
        print(f"\nUser:    {article.user}")
        print()

    return path


if __name__ == "__main__":
    run_pipeline()
