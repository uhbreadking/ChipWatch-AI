"""GNews API fetcher. Free plan: about 100 requests/day, up to 10 articles per request."""
import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://gnews.io/api/v4/search"


def _api_key():
    key = os.getenv("GNEWS_API_KEY")
    if not key:
        raise RuntimeError("GNEWS_API_KEY not found. Add it to your .env file.")
    return key


def get_gnews_articles(query, max_articles=10):
    """Return (articles_table, total_matching_articles) for a search."""
    params = {
        "q": query,
        "lang": "en",
        "max": max_articles,
        "sortby": "publishedAt",
        "apikey": _api_key(),
    }
    resp = requests.get(URL, params=params, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"GNews request failed (status {resp.status_code}): {resp.text[:200]}")
    payload = resp.json()

    rows = []
    for article in payload.get("articles", []):
        rows.append({
            "title": article.get("title"),
            "url": article.get("url"),
            "source": article.get("source", {}).get("name"),
            "published_at": article.get("publishedAt"),
        })

    total = payload.get("totalArticles", 0)
    columns = ["title", "url", "source", "published_at", "fetched_at"]
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=columns), total

    df = df.dropna(subset=["title", "url"]).drop_duplicates(subset=["url"])
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce", utc=True)
    df["fetched_at"] = pd.Timestamp.now(tz="UTC")
    df = df.sort_values("published_at", ascending=False)
    return df.reindex(columns=columns).reset_index(drop=True), total