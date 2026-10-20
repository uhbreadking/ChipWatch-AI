from src.fetch_gnews import get_gnews_articles

articles, total = get_gnews_articles("TSMC semiconductor")

print(f"Total matching articles: {total}")
print(f"Articles returned: {len(articles)}")
print(articles[["published_at", "source", "title"]].to_string())