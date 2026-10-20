from src.fetch_rss import get_rss_articles

articles = get_rss_articles("TSMC semiconductor")

print(f"Articles: {len(articles)}")
print(articles[["published_at", "source", "title"]].head(10).to_string())