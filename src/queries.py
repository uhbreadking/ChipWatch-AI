def build_query(company):
    """Return the company's news search query from companies.csv, so every feature measures the same thing."""
    return company["news_query"]