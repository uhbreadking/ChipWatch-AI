# ChipWatch AI
### Evidence-Linked Semiconductor Supply Disruption Monitoring

**Status:** In development. Phase 1 (data collection and dashboard) is working locally; Phase 2 (labeled dataset and classifier) is underway.  
**Focus:** Semiconductor supply chain · Risk intelligence · Data analytics · Machine learning

ChipWatch AI collects public news about six real semiconductor companies, matches each headline to the companies it mentions, flags headlines that may describe supply disruptions, and charts how much coverage each company receives over time. Every flag links back to its original source and is treated as a lead for human review, not a confirmed risk.

> 📸 *Dashboard screenshot and live demo link will be added once the dashboard is deployed.*

---

## Current Status

| Component | Status |
|---|---|
| Python environment, project structure, and safe API key handling (`.env`) | ✅ Done |
| Verified company reference file with per-company search queries (`data/companies.csv`) | ✅ Done |
| Company name matching (`src/match_companies.py`) | ✅ Done, with tests |
| Keyword-based disruption rules (`src/classify_rules.py`) | ✅ Done, with tests |
| Matching + rules pipeline (`src/pipeline.py`) | ✅ Done |
| Streamlit dashboard: company selector, details, headline tester | ✅ Done |
| Source-linked article table with company matches and flags | ✅ Working locally (Google News RSS) |
| GNews fetcher: articles and daily article counts (`src/fetch_gnews.py`) | ✅ Done |
| 30-day news attention chart in the dashboard | ✅ Done |
| 30-day news attention data collection (`scripts/collect_attention.py`) | 🔄 In progress: TSMC and ASML complete; remaining companies limited by free API quota |
| Headline labeling guidelines (`docs/labeling_guidelines.md`) | ✅ Done |
| Labeling dataset export with ordinary and enriched samples | ✅ Done (201 headlines) |
| Pilot labeling round | ✅ 40 of 201 headlines labeled |
| Full labeled dataset and evaluation of keyword rules | 🔄 In progress |
| Machine learning classifier | ⬜ Planned |
| Public deployment | ⬜ Planned |

---

## Problem

Semiconductor supply chain analysts monitor fragmented external information (manufacturing incidents, trade restrictions, logistics problems, company announcements) spread across many news sources. Collecting and screening this manually is slow and inconsistent.

**Guiding question:** How can AI help supply chain analysts detect, prioritize, and investigate external semiconductor supply disruptions faster and more systematically?

## Solution

ChipWatch AI is designed to:

1. Collect semiconductor industry news from public sources.
2. Identify which monitored companies each headline mentions.
3. Flag headlines that may describe a disruption, starting with transparent keyword rules and later a trained classifier.
4. Show news attention over time separately from reviewed disruption events.
5. Present a source-linked review queue for analysts.

The platform supports human decision-making. It does not replace professional risk assessment.

---

## How It Works

```mermaid
flowchart LR
    CO[(data/companies.csv<br/>aliases + search queries)]
    A[Google News RSS<br/>local development] --> C[fetch_rss.py]
    B[GNews API] --> D[fetch_gnews.py]
    C --> E[pipeline.py<br/>match companies + keyword rules]
    D -.-> E
    CO --> E
    E --> F[Streamlit dashboard<br/>article table + headline tester]
    D --> G[collect_attention.py<br/>daily article counts]
    CO --> G
    G --> H[(attention counts<br/>local only)]
    H --> I[30-day news attention chart]
    I --> F
    C --> L[export_for_labeling.py]
    L --> M[(hand-labeled headlines<br/>local only)]
    M -.-> N[Evaluate rules +<br/>train classifier]

    classDef planned stroke-dasharray: 5 5
    class N planned
```

*Dashed boxes and arrows are planned and not yet built.*

**Pipeline steps:**

1. **Fetch:** retrieve recent headlines, links, publishers, and publication dates for a company's search query.
2. **Match companies:** detect which of the six monitored companies each headline names, using hand-researched aliases and whole-word, case-insensitive matching.
3. **Flag:** check each headline for disruption clue phrases (Manufacturing, Geopolitical, Logistics, Financial). Each flag shows the exact phrases that triggered it. Headlines matching several categories are marked "Needs review."
4. **Review:** every result starts as "Unreviewed" and links to its original source for a human to verify.
5. **Track attention:** daily article counts per company are collected once, cached, and charted, so spikes can be traced to their cause in the article table.

**Key distinction:** a spike in news attention can come from earnings reports, product launches, or repeated coverage of one story. ChipWatch labels article volume as **news attention**, never as risk.

---

## Companies Monitored

| Company | Segment | News search query |
|---|---|---|
| TSMC | Foundry | `TSMC` |
| ASML | Semiconductor Equipment | `ASML` |
| SK hynix | Memory | `SK hynix` |
| Micron | Memory | `Micron Technology` |
| Amkor | Assembly Packaging & Test | `Amkor` |
| Samsung Electronics | Memory; Foundry | `Samsung Electronics AND (chip OR memory OR foundry)` |

Segments are verified against each company's official website, with the source link and verification date stored in `data/companies.csv`. Being in a related segment does not establish a customer-supplier relationship between these companies.

Each company has its own search query because one formula does not fit all names: "Micron" alone matches the unit of measurement, and "Samsung Electronics" alone matches phone and TV news.

---

## Early Findings

These are observations from testing on real data, not formal evaluation results.

- **Filtering works at scale.** Of 100 real TSMC headlines, the keyword rules flagged **1** for review (a plant resuming operations after an earthquake). The other 99 were ordinary business news, such as earnings, share trades, and new fabs.
- **News attention is not risk.** The two largest coverage spikes in the collected data were both earnings reports: TSMC jumped to **51** articles on October 15, and ASML jumped from 0–2 articles a day to **46** on October 14. The article table traced each spike to its cause in seconds.
- **Data-driven alias decision.** Plain "Samsung" was originally excluded from aliases to avoid consumer electronics news. Testing on 67 real Samsung headlines showed this missed **37 (55%)** of relevant articles, because chip journalism usually says just "Samsung." Since the search query already filters out consumer news, plain "Samsung" was added back.
- **Query wording matters.** For TSMC on its earnings day, searching `TSMC` returned **51** articles versus **30** for `TSMC semiconductor`, which led to per-company queries.
- **Duplicate coverage is common.** Wire stories appear many times across publishers (one Samsung story appeared 4 times in a single result set), which is why article counts and event counts must be kept separate.
- **Disruption headlines are rare.** In early samples, 1 of 100 TSMC headlines and 0 of 72 Samsung headlines described a possible disruption. This shaped the labeling plan (see below).

---

## Phase 2: Building a Labeled Dataset

To measure how well the keyword rules perform, and to train a classifier that can improve on them, ChipWatch needs headlines labeled by a human using consistent rules.

**Annotation guidelines.** `docs/labeling_guidelines.md` defines the labeling schema and decision rules for hard cases, developed from real headlines encountered while building the project. Each headline receives:

- a **label** describing the event type: Manufacturing, Geopolitical, Logistics, Financial, Not a disruption, or Unclear;
- an **event status** describing its lifecycle: Active, Announced, Potential, Recovery, Resolved, or None. Status is recorded for analysis and dashboard filtering, not used as a model target.

Examples of decision rules: stock price moves and demand-driven shortages are not disruptions; negated events ("TSMC avoids shutdown") are not disruptions; policy commentary is not an announced restriction; disruptions are labeled the same way whether or not the affected company is one of the six monitored.

**Sampling.** Because disruption headlines are rare, the 201-headline dataset combines:

| Sample | Headlines | How gathered |
|---|---|---|
| Ordinary | 102 | Random sample of each monitored company's standard news query |
| Enriched | 99 | Random sample of targeted queries such as `chip export controls` and `semiconductor fab fire` |

Metrics measured on the combined set show how well the rules or model **distinguish** disruption headlines from ordinary ones. They do not represent real-world flag accuracy, since disruptions are far less common in ordinary news feeds. Results will be reported with the sampling method stated alongside them.

**Labeling process.**

1. **Blind labeling:** headlines are labeled without seeing the keyword rules' predictions, so the evaluation stays fair.
2. **Pilot round:** the first 40 headlines were labeled to test the guidelines; ambiguous "hard cases" were recorded and used to refine the rules.
3. **Consistency check:** a sample of pilot headlines is re-labeled without viewing earlier answers to measure agreement.
4. **Event grouping:** headlines describing the same incident share an event ID, so repeated coverage never appears in both training and test data.

---

## Known Limitations

ChipWatch AI uses only publicly available information. It does not have access to confidential supplier relationships, private inventory levels, customer-specific sourcing, or undisclosed manufacturing capacity.

**Interpretation**
- News coverage does not necessarily indicate actual supply risk, and higher article volume does not mean higher severity.
- A company being mentioned does not prove it is directly affected.
- The platform does not predict shortages or production losses.

**Company matching**
- Matching uses headlines only, so relevant articles that don't name a company in the headline are missed.
- Some names have other meanings (e.g., "micron" as a unit of measurement, "Samsung Electro-Mechanics" as a separate company), producing occasional false matches.

**Keyword rules**
- Rules cannot understand negation ("TSMC avoids shutdown"), paraphrase ("fab halted after blaze"), hypotheticals ("Will new sanctions hit ASML?"), or context ("earthquake drill"). These failures are documented as tests and are the motivation for a trained classifier.

**Labeled data**
- Labels are produced by a single annotator, so they reflect one consistent interpretation of the guidelines rather than multi-person agreement.
- Labels are based on headlines only, matching what the classifier sees, so some events are harder to judge than they would be from the full article.
- Some enriched queries returned off-topic results (for example, `chip plant shutdown` returned a potato chip factory closure). These were kept and labeled as negative examples, since real news feeds contain the same ambiguity.

**Data sources**
- GNews's free plan allows about 100 requests per day and up to 10 articles per request, and delays articles by roughly 12 hours, so the dashboard is not real-time.
- GNews daily counts are much smaller than total coverage, so the attention chart is best read as changes over time for one company, not as a comparison between companies.
- Only article metadata (headlines, links, dates, publishers) is stored, never full article text.
- GNews's free index covers smaller companies thinly: Amkor had only 1 matching article in 30 days, versus 100 recent Amkor headlines from Google News RSS. The dashboard warns when a company's monthly total is too low to show trends.

---

## Data Sources

| Source | Used for | Status |
|---|---|---|
| [GNews API](https://gnews.io/) | Headlines and daily article counts | ✅ In use |
| [Google News RSS](https://news.google.com/) | Recent headlines during local development and labeling | ✅ Local only (feed terms limit use to personal, non-commercial readers) |
| [GDELT DOC 2.0 API](https://www.gdeltproject.org/) | Originally planned for news attention timelines | ⏸️ Paused: persistent rate limiting (Oct 2026). Code kept in `src/fetch_gdelt.py`. |
| Official company websites ([TSMC](https://www.tsmc.com/english/aboutTSMC/company_profile), [ASML](https://www.asml.com/en-us/about-asml/company-profile), and others) | Verifying company segments | ✅ In use |
| [SEC EDGAR](https://www.sec.gov/edgar/search/) | Official company filings | ⬜ Planned |

**Why the data source changed:** GDELT's free API began rejecting requests from every network tested, even after waiting for hours, consistent with an extended cooldown. After comparing five free news APIs (GNews, NewsAPI.org, NewsData.io, Finnhub, Marketaux), GNews was chosen as the only option that could be deployed publicly for non-commercial use, supported keyword search across all six companies, and offered 30 days of history. Google News RSS is used only for local development and labeling.

**What is and isn't committed to this repository.** To respect data source terms, third-party news data is kept local:

| Data | In this repository? |
|---|---|
| Code, tests, company reference file, labeling guidelines | ✅ Yes |
| Collected attention counts (`data/attention_counts.csv`) | ❌ No, until GNews data terms are confirmed |
| Labeled headlines (`data/labels/`) | ❌ No, they contain third-party headlines |
| API keys (`.env`) | ❌ Never |

Evaluation results will be published as summary metrics, which can be shared without redistributing the underlying headlines.

News data provided by [GNews](https://gnews.io/).

---

## Project Structure

```
ChipWatch-AI/
├── app.py                        # Streamlit dashboard
├── requirements.txt              # Python dependencies
├── .env.example                  # Template for the GNews API key (.env itself is not committed)
├── data/
│   ├── companies.csv             # Verified companies, aliases, segments, search queries
│   ├── attention_counts.csv      # Collected daily counts (local only, not committed)
│   └── labels/                   # Hand-labeled headlines (local only, not committed)
├── docs/
│   └── labeling_guidelines.md    # Annotation schema and decision rules
├── src/
│   ├── fetch_gnews.py            # GNews articles and daily counts
│   ├── fetch_rss.py              # Google News RSS (local development only)
│   ├── fetch_gdelt.py            # GDELT fetcher (paused)
│   ├── queries.py                # Shared per-company search query lookup
│   ├── match_companies.py        # Company name matching
│   ├── classify_rules.py         # Keyword-based disruption flags
│   └── pipeline.py               # Runs matching and rules on articles
├── scripts/
│   ├── collect_attention.py      # Resumable 30-day attention count collector
│   ├── export_for_labeling.py    # Builds the ordinary + enriched labeling dataset
│   └── try_*.py                  # Manual test scripts for each component
└── tests/
    ├── test_match_companies.py   # 10 tests
    └── test_classify_rules.py    # 9 tests, including documented limitations
```

---

## Getting Started

Requires Python 3.13 and Git. Commands below are for Windows PowerShell.

**1. Clone and install**

```powershell
git clone https://github.com/uhbreadking/ChipWatch-AI.git
cd ChipWatch-AI
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first (this applies only to the current terminal).

**2. Add your GNews API key**

Get a free key at [gnews.io](https://gnews.io/), copy `.env.example` to a new file named `.env`, and replace the placeholder with your key:

```
GNEWS_API_KEY=your_gnews_api_key_here
```

**3. Run the dashboard**

```powershell
python -m streamlit run app.py
```

**4. Run the tests**

```powershell
python -m pytest
```

**5. Collect news attention data (optional)**

```powershell
python -m scripts.collect_attention
```

The collector stops after 80 requests to stay within the free plan's daily limit. Run it again the next day to continue; it skips data already collected with the current search queries. The chart shows "Days collected" so incomplete data is visible.

**6. Export headlines for labeling (optional)**

```powershell
python -m scripts.export_for_labeling
```

Creates `data/labels/to_label.csv`. The script refuses to run if that file already exists, so existing labels are never overwritten.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Data processing and application logic |
| requests | API calls |
| pandas | Data cleaning, sampling, and transformation |
| Streamlit | Interactive dashboard and charts |
| python-dotenv | Loading the API key from `.env` |
| pytest | Automated testing |
| scikit-learn | Headline classification (planned) |
| Git & GitHub | Version control |

---

## Roadmap

### Phase 1: Data Collection and Dashboard
- [x] Configure Python development environment
- [x] Create project structure
- [x] Build verified company reference file
- [x] Match company names in headlines (with tests)
- [x] Build dashboard layout with company selector and headline tester
- [x] Retrieve real semiconductor news articles (GNews; Google News RSS for local development)
- [x] Display source-linked articles in Streamlit *(working locally)*
- [x] Build 30-day news attention chart
- [ ] Collect 30 days of daily article counts for all six companies *(in progress)*
- [ ] ~~Connect to the GDELT API~~ *(paused: rate limiting)*

### Phase 2: Disruption Identification
- [x] Define disruption categories
- [x] Implement keyword-based classification (with tests documenting known limitations)
- [x] Write labeling guidelines
- [x] Export a 201-headline labeling dataset (ordinary + enriched samples)
- [x] Complete pilot labeling round (40 headlines)
- [ ] Refine guidelines from pilot hard cases and run a consistency check
- [ ] Label the remaining headlines and group duplicate events
- [ ] Measure keyword-rule precision, recall, and F1 against the labels
- [ ] Train a classifier and compare it to the keyword-rule baseline

### Phase 3: Event Review and Prioritization
- [ ] Group duplicate and related articles into distinct events
- [ ] Record affected companies during event verification
- [ ] Build the prioritization framework
- [ ] Build the analyst investigation queue with review status

### Phase 4: Deployment and Evaluation
- [ ] Deploy to Streamlit Community Cloud (API key stored in Streamlit secrets)
- [ ] Benchmark manual vs. assisted news screening time
- [ ] Publish results and limitations

## Evaluation Plan

Formal results will be reported here only after testing on held-out, hand-labeled data, with the sampling method stated alongside every metric.

| Metric | What it measures |
|---|---|
| Precision and recall | How accurately disruption headlines are flagged |
| Macro F1-score | Performance balanced across all categories |
| Confusion matrix | Which categories are mistaken for each other |
| Company match precision and recall | How often company detection is correct, and how many mentions it finds |
| Duplicate event rate | How well repeated coverage is grouped |
| Screening time | Manual vs. tool-assisted review of the same headlines |
| Source traceability | Share of flagged events with working source links |

## Future Enhancements

- Scheduled daily data collection
- Matching on article descriptions, not just headlines
- Collapsing duplicate wire stories into one row with an outlet count
- Dashboard filters by event status (e.g., highlight Active and Announced)
- LLM-assisted event extraction and source-linked briefings
- Expanded company coverage and alerts

---

## About

ChipWatch AI is an independent portfolio project combining semiconductor industry research, supply chain management, machine learning, and business intelligence. Its goal is to show practical AI development and the ability to turn unstructured industry news into useful, evidence-backed supply chain insights.