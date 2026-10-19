import re

KEYWORDS = {
    "Manufacturing": ["shutdown", "outage", "halts production", "production halt", "fab fire", "factory fire", "earthquake"],
    "Geopolitical": ["export control", "export restriction", "sanction", "tariff", "trade ban"],
    "Logistics": ["port closure", "shipping delay", "shipping disruption"],
    "Financial": ["bankruptcy", "liquidity crisis", "debt restructuring"],
}


def classify_headline(title):
    """Return (candidate_category, matched_terms) for a headline."""
    text = str(title)
    categories = []
    matched_terms = []

    for category, terms in KEYWORDS.items():
        for term in terms:
            if re.search(r"\b" + re.escape(term), text, flags=re.IGNORECASE):
                matched_terms.append(term)
                if category not in categories:
                    categories.append(category)

    if len(categories) == 0:
        label = "No signal"
    elif len(categories) == 1:
        label = categories[0]
    else:
        label = "Needs review"

    return label, matched_terms