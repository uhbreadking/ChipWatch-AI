import pandas as pd
import streamlit as st
from src.match_companies import load_aliases, match_companies
from src.classify_rules import classify_headline

st.set_page_config(page_title="ChipWatch AI", layout="wide")

companies = pd.read_csv("data/companies.csv")

# ---------- Sidebar ----------
st.sidebar.header("Filters")
company_name = st.sidebar.selectbox("Company", companies["company_name"])
st.sidebar.caption("News attention measures coverage, not risk.")

company = companies[companies["company_name"] == company_name].iloc[0]

# ---------- Main page ----------
st.title("ChipWatch AI")
st.caption("External semiconductor disruption intelligence")

st.header(company["company_name"])

col1, col2, col3 = st.columns(3)
with col1:
    st.write("Segment")
    st.subheader(company["segment"])
with col2:
    st.metric("Search aliases", len(company["aliases"].split(";")))
with col3:
    st.metric("Verified on", company["verified_on"])

st.write(f"**Aliases used for matching:** {company['aliases']}")
st.markdown(f"[Official company profile]({company['evidence_url']})")

st.divider()

st.subheader("30-day news attention")
st.info("Coming soon: daily article counts from GDELT.")

st.subheader("Recent articles")
st.info("Coming soon: source-linked headlines for the selected company.")

st.divider()

st.subheader("Headline tester")
st.caption("Try the company matching and keyword rules on any headline. Results are first-pass leads, not confirmed disruptions.")

headline = st.text_input("Headline", placeholder="e.g. TSMC halts production after earthquake")

if headline:
    aliases = load_aliases()
    matched = match_companies(headline, aliases)
    label, terms = classify_headline(headline)

    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Companies detected**")
        if matched:
            names = companies[companies["company_id"].isin(matched)]["company_name"]
            st.write(", ".join(names))
        else:
            st.write("None")
    with col_b:
        st.write("**Candidate category**")
        st.write(label)

    if terms:
        st.write(f"**Why flagged:** matched {', '.join(terms)}")
    st.caption("Review status: unreviewed")