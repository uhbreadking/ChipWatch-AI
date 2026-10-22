import time
from pathlib import Path

import pandas as pd

from src.fetch_gnews import count_articles_on_day
from src.queries import build_query

OUTPUT = Path("data/attention_counts.csv")
COLUMNS = ["company_id", "date", "query", "count", "fetched_at"]
DAYS = 30
MAX_REQUESTS = 80  # stays under the free plan's 100/day, leaving room for testing


def load_existing():
    if OUTPUT.exists():
        return pd.read_csv(OUTPUT)
    return pd.DataFrame(columns=COLUMNS)


def main():
    companies = pd.read_csv("data/companies.csv")
    existing = load_existing()
    done = set(zip(existing["company_id"], existing["date"], existing["query"]))

    # Skip today and yesterday: the free plan's ~12-hour delay means they're incomplete.
    today = pd.Timestamp.now(tz="UTC").normalize()
    days = []
    for i in range(2, DAYS + 2):
        days.append((today - pd.Timedelta(days=i)).strftime("%Y-%m-%d"))

    new_rows = []
    requests_made = 0

    try:
        for _, company in companies.iterrows():
            query = build_query(company)
            for day in days:
                if (company["company_id"], day, query) in done:
                    continue
                if requests_made >= MAX_REQUESTS:
                    break
                try:
                    count = count_articles_on_day(query, day)
                except RuntimeError as exc:
                    print(f"\nStopped early: {exc}")
                    return                
                requests_made += 1
                new_rows.append({
                    "company_id": company["company_id"],
                    "date": day,
                    "query": query,
                    "count": count,
                    "fetched_at": pd.Timestamp.now(tz="UTC"),
                })
                print(f"{company['company_id']:<10} {day}  {count}")
                time.sleep(1.5)
    finally:
        total = len(existing)
        if new_rows:
            new = pd.DataFrame(new_rows)
            combined = new if existing.empty else pd.concat([existing, new], ignore_index=True)
            combined = combined.drop_duplicates(subset=["company_id", "date"], keep="last")
            combined = combined.sort_values(["company_id", "date"])
            combined.to_csv(OUTPUT, index=False)
            total = len(combined)
        print(f"\nRequests used: {requests_made}. New rows saved: {len(new_rows)}.")
        print(f"Total rows in {OUTPUT}: {total}.")


if __name__ == "__main__":
    main()