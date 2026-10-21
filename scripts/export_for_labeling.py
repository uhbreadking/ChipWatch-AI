import time
from pathlib import Path

import pandas as pd

from src.fetch_rss import get_rss_articles
from src.queries import build_query

OUTPUT = Path("data/labels/to_label.csv")
SEED = 42
ORDINARY_PER_COMPANY = 17
ENRICHED_PER_QUERY = 10

ENRICHED_QUERIES = [
    "semiconductor fab fire",
    "chip plant shutdown",
    "semiconductor earthquake production",
    "chip factory power outage",
    "chip export controls",
    "semiconductor sanctions",
    "chip tariffs",
    "semiconductor shipping disruption",
    "port strike semiconductors",
    "semiconductor supplier bankruptcy",
]

REVIEWER_COLUMNS = ["label", "event_status", "event_group_id", "notes", "mentioned_companies", "affected_company"]


def take_sample(articles, n):
    """Pick n random articles, or all of them if there are fewer than n."""
    if len(articles) <= n:
        return articles
    return articles.sample(n=n, random_state=SEED)


def main():
    if OUTPUT.exists():
        raise SystemExit(f"{OUTPUT} already exists. Move or rename it first so your labels are never overwritten.")

    companies = pd.read_csv("data/companies.csv")
    parts = []

    for _, company in companies.iterrows():
        articles = get_rss_articles(build_query(company))
        sample = take_sample(articles, ORDINARY_PER_COMPANY).copy()
        sample["search_company"] = company["company_id"]
        sample["sample_source"] = "ordinary"
        parts.append(sample)
        print(f"ordinary  {company['company_id']:<35} {len(sample)} of {len(articles)}")
        time.sleep(1.5)

    for query in ENRICHED_QUERIES:
        articles = get_rss_articles(query)
        sample = take_sample(articles, ENRICHED_PER_QUERY).copy()
        sample["search_company"] = f"query: {query}"
        sample["sample_source"] = "enriched"
        parts.append(sample)
        print(f"enriched  {query:<35} {len(sample)} of {len(articles)}")
        time.sleep(1.5)

    combined = pd.concat(parts, ignore_index=True)
    combined = combined.drop_duplicates(subset=["title"])
    combined = combined.sample(frac=1, random_state=SEED).reset_index(drop=True)

    combined["headline_id"] = [f"H{i:03d}" for i in range(1, len(combined) + 1)]
    combined["published_at"] = combined["published_at"].dt.strftime("%Y-%m-%d")
    for column in REVIEWER_COLUMNS:
        combined[column] = ""

    columns = [
        "headline_id", "title", "source", "published_at", "search_company",
        "label", "event_status", "event_group_id", "notes",
        "mentioned_companies", "affected_company", "sample_source",
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    combined[columns].to_csv(OUTPUT, index=False, encoding="utf-8-sig")

    print(f"\nSaved {len(combined)} headlines to {OUTPUT}")
    print(combined["sample_source"].value_counts().to_string())


if __name__ == "__main__":
    main()