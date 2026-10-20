from src.fetch_gdelt import historical_attention
#go into src/fetch_news.py and bring the historical_attention function into this file so I can use it here
query = "TSMC semiconductor"

timeline = historical_attention(query, days=30)

print(f"Number of rows: {len(timeline)}")
print(timeline.head())
print(timeline.dtypes)

timeline.to_csv("data/sample_timeline_tsmc.csv", index=False)
print("Saved to data/sample_timeline_tsmc.csv")