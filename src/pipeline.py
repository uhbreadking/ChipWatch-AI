from src.match_companies import match_companies
from src.classify_rules import classify_headline


def enrich_articles(articles, aliases):
    """Add companies, category, matched_terms, and review_status columns to an articles table."""
    articles = articles.copy()
    companies_found = []
    categories = []
    evidence = []

    for title in articles["title"]:
        companies_found.append(", ".join(match_companies(title, aliases)))
        label, terms = classify_headline(title)
        categories.append(label)
        evidence.append(", ".join(terms))

    articles["companies"] = companies_found
    articles["category"] = categories
    articles["matched_terms"] = evidence
    articles["review_status"] = "Unreviewed"
    return articles