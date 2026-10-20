import xml.etree.ElementTree as ET

import pandas as pd
import requests

RSS_URL = "https://news.google.com/rss/search"
HEADERS = {"User-Agent": "ChipWatch-AI/0.1 (student portfolio project)"}


def get_rss_articles(query):
    """Recent article metadata from Google News RSS.
    For personal, non-commercial local development only (per the feed's terms)."""
    params = {"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"}
    resp = requests.get(RSS_URL, params=params, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    root = ET.fromstring(resp.content)
    rows = []
    for item in root.iter("item"):
        rows.append({
            "title": item.findtext("title"),
            "url": item.findtext("link"),
            "source": item.findtext("source"),
            "published_at": item.findtext("pubDate"),
        })

    columns = ["title", "raw_title", "url", "source", "published_at", "fetched_at"]
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=columns)

    df = df.dropna(subset=["title", "url"]).drop_duplicates(subset=["url"])
    df["raw_title"] = df["title"]
    df["title"] = df["title"].str.rsplit(" - ", n=1).str[0]
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce", utc=True)
    df["fetched_at"] = pd.Timestamp.now(tz="UTC")
    df = df.sort_values("published_at", ascending=False)
    return df.reindex(columns=columns).reset_index(drop=True)