from src.match_companies import load_aliases, match_companies

aliases = load_aliases()

headlines = [
    "Micron halts production at Hiroshima plant",
    "TSMC and Samsung Foundry race for 2nm customers",
    "SK HYNIX shares jump on HBM demand",
    "New study links micronutrients to better sleep",
    "Samsung unveils new Galaxy phone",
    "Stock market closes higher on Friday",
    "Researchers build a 5-micron optical sensor",
]

for headline in headlines:
    print(match_companies(headline, aliases), "<-", headline)