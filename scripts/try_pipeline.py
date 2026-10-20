from src.fetch_rss import get_rss_articles
from src.match_companies import load_aliases, match_companies
from src.classify_rules import classify_headline

aliases = load_aliases()
articles = get_rss_articles("TSMC semiconductor")

companies_found = []
categories = []
evidence = []

for title in articles["title"]:
    companies_found.append(match_companies(title, aliases))
    label, terms = classify_headline(title)
    categories.append(label)
    evidence.append(terms)

articles["companies"] = companies_found
articles["category"] = categories
articles["matched_terms"] = evidence

print("Category counts:")
print(articles["category"].value_counts())

flagged = articles[articles["category"] != "No signal"]
print(f"\nFlagged headlines: {len(flagged)}")
print(flagged[["published_at", "category", "matched_terms", "title"]].to_string())

no_company = articles[articles["companies"].str.len() == 0]
print(f"\nHeadlines with no company match: {len(no_company)}")
print(no_company[["source", "title"]].to_string())