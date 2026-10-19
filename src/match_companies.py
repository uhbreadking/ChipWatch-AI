import re
import pandas as pd


def load_aliases(path="data/companies.csv"):
    """Read companies.csv and return {company_id: [alias, alias, ...]}."""
    companies = pd.read_csv(path)
    aliases = {}

    for _, row in companies.iterrows():
        names = []
        for name in row["aliases"].split(";"):
            names.append(name.strip())
        aliases[row["company_id"]] = names

    return aliases

def match_companies(headline, aliases):
    """Return a list of company_ids whose aliases appear in the headline."""
    text = str(headline)
    found = []

    for company_id, names in aliases.items():
        for name in names:
            pattern = r"\b" + re.escape(name) + r"\b"
            if re.search(pattern, text, flags=re.IGNORECASE):
                found.append(company_id)
                break

    return found