import time

from src.fetch_gnews import count_articles_on_day

for query in ["TSMC semiconductor", "TSMC"]:
    count = count_articles_on_day(query, "2026-10-15")
    print(f"{query!r:<25} {count} articles")
    time.sleep(2)