from pathlib import Path
import pandas as pd
import streamlit as st
from src.fetch_rss import get_rss_articles
from src.pipeline import enrich_articles
from src.match_companies import load_aliases, match_companies
from src.classify_rules import classify_headline
from src.queries import build_query

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

ATTENTION_FILE = Path("data/attention_counts.csv")


@st.cache_data(ttl=600)
def load_attention():
    if not ATTENTION_FILE.exists():
        return pd.DataFrame(columns=["company_id", "date", "query", "count", "fetched_at"])
    return pd.read_csv(ATTENTION_FILE)


attention = load_attention()
current_query = build_query(company)
cutoff_day = (pd.Timestamp.now(tz="UTC").normalize() - pd.Timedelta(days=31)).strftime("%Y-%m-%d")

company_counts = attention[
    (attention["company_id"] == company["company_id"])
    & (attention["query"] == current_query)
    & (attention["date"] >= cutoff_day)
].sort_values("date")

if company_counts.empty:
    st.info("No attention data collected yet for this company. Run `python -m scripts.collect_attention`.")
else:
    peak = company_counts.loc[company_counts["count"].idxmax()]
    m1, m2, m3 = st.columns(3)
    m1.metric("Peak day", peak["date"])
    m2.metric("Articles on peak day", int(peak["count"]))
    m3.metric("Days collected", f"{len(company_counts)} of 30")
    total_articles = int(company_counts["count"].sum())
    if total_articles < 10:
        st.warning(
            f"Only {total_articles} matching articles in this period. GNews's free index has little "
            "coverage of this company, so this chart is too sparse to show meaningful trends."
        )

    chart_data = company_counts.copy()
    chart_data["date"] = pd.to_datetime(chart_data["date"])
    st.bar_chart(chart_data, x="date", y="count", x_label="Date", y_label="Matching articles")

    st.caption(
        f"Daily count of GNews articles matching `{current_query}`. "
        "This measures coverage, not risk: a spike can come from earnings, a product launch, "
        "or repeated coverage of one story."
    )

st.subheader("Recent articles")


@st.cache_data(ttl=3600)
def load_articles(query):
    return get_rss_articles(query)


query = build_query(company)


try:
    articles = load_articles(query)
except Exception as exc:
    st.error(f"Could not load articles: {exc}")
    articles = None

if articles is not None and not articles.empty:
    articles = enrich_articles(articles, load_aliases())

    cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=30)
    articles = articles[articles["published_at"] >= cutoff]

    only_flagged = st.checkbox("Show only flagged headlines")
    if only_flagged:
        articles = articles[articles["category"] != "No signal"]

    st.caption(f"{len(articles)} articles from the last 30 days · Source: Google News RSS (local development only)")
    st.dataframe(
        articles[["published_at", "source", "title", "companies", "category", "matched_terms", "review_status", "url"]],
        column_config={
            "published_at": st.column_config.DatetimeColumn("Published", format="YYYY-MM-DD HH:mm"),
            "source": "Publisher",
            "title": "Headline",
            "companies": "Companies",
            "category": "Candidate category",
            "matched_terms": "Why flagged",
            "review_status": "Status",
            "url": st.column_config.LinkColumn("Link", display_text="Open"),
        },
        hide_index=True,
    )
elif articles is not None:
    st.info("No articles found for this company.")

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