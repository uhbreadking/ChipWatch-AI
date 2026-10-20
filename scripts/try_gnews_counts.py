import time

from src.fetch_gnews import count_articles_on_day

query = "TSMC semiconductor"

for day in ["2026-10-12", "2026-10-15"]:
    count = count_articles_on_day(query, day)
    print(f"{day}: {count} articles")
    time.sleep(2)