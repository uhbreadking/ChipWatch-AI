# ChipWatch AI
### AI-Powered Semiconductor Supply Disruption Intelligence Platform

**Project Status:** In Development  
**Focus:** Semiconductor Supply Chain | AI & Machine Learning | Risk Intelligence | Data Analytics

## Project Overview

ChipWatch AI is an AI-powered external semiconductor supply disruption intelligence platform designed to help supply chain professionals identify, monitor, and investigate potential disruptions across the global semiconductor industry.

The platform uses publicly available industry news, natural language processing (NLP), and data analytics to identify relevant companies, classify potential disruption events, analyze historical trends, and prioritize developments requiring further investigation.

By transforming fragmented external information into structured, actionable intelligence, ChipWatch AI aims to improve supply chain visibility and support proactive risk management.

## Problem Statement

Semiconductor supply chain analysts must monitor fragmented external information to identify developments that may affect manufacturing, supplier availability, or logistics.

Important developments can emerge across multiple news sources, company announcements, and industry publications. Manually collecting, evaluating, and organizing this information can be time-consuming and inconsistent.

ChipWatch AI explores the following question:

**How can AI help semiconductor supply chain professionals detect, prioritize, and investigate external supply disruptions faster and more systematically?**

## Proposed Solution

ChipWatch AI is designed to:

1. Automatically collect semiconductor industry news from publicly available sources.
2. Identify relevant semiconductor companies and potential disruption events.
3. Classify developments into meaningful supply chain risk categories.
4. Visualize historical news activity and detected disruption trends.
5. Prioritize developments for further investigation using transparent, evidence-based criteria.
6. Provide supporting sources and contextual information to assist analyst review.

The platform is intended to support human decision-making rather than replace professional risk assessments.

## Business Value

ChipWatch AI aims to deliver value in three areas:

- **Improve efficiency:** Reduce the manual effort required to screen and organize semiconductor industry news.
- **Increase visibility:** Provide a centralized view of external developments affecting semiconductor manufacturing, equipment, memory, and packaging.
- **Support proactive investigation:** Help analysts identify and prioritize potentially significant events for further verification.

Project performance will be evaluated using measurable indicators such as article classification accuracy, company identification precision, and news-screening efficiency.

## Project Scope

ChipWatch AI focuses exclusively on publicly available data and evidence-based external risk intelligence.

The platform does not claim to have access to confidential supplier relationships, private inventory levels, customer-specific sourcing information, or undisclosed manufacturing capacity.

**Important limitations:**

- News coverage does not necessarily indicate actual supplier risk.
- Increased article volume does not automatically mean increased disruption severity.
- Company mentions do not prove that a company is directly affected by an event.
- Disruption priority scores represent analyst review priorities, not probabilities of supplier failure.
- The platform does not predict verified inventory shortages or production losses.

Hypothetical supply chain simulations are excluded from the initial MVP and may be explored as a separate future enhancement.

## Semiconductor Companies Monitored

The initial platform will focus on six real companies representing different stages of the semiconductor supply chain.

| Company | Supply Chain Segment |
|---|---|
| TSMC | Semiconductor Foundry |
| ASML | Semiconductor Manufacturing Equipment |
| SK hynix | Memory Manufacturing |
| Micron Technology | Memory Manufacturing |
| Amkor Technology | Semiconductor Assembly, Packaging & Testing |
| Samsung Electronics | Memory & Foundry Manufacturing |

Company information will be verified using official disclosures, investor relations materials, and publicly available sources.

## Core Features

### 1. Automated Semiconductor News Monitoring

Collect and organize relevant news articles using the GDELT API.

**Planned capabilities:**
- Retrieve news about monitored semiconductor companies.
- Capture article titles, publication dates, publishers, and source URLs.
- Identify company mentions using name and alias matching.
- Filter news by company, date, and topic.
- Deduplicate repeated article records.

### 2. AI-Powered Disruption Classification

Use natural language processing and machine learning to identify articles describing potential semiconductor supply disruptions.

**Classification categories:**
- Manufacturing disruptions
- Geopolitical and trade restrictions
- Logistics and transportation disruptions
- Financial or supplier stability concerns
- Non-disruptive industry developments

The initial prototype will use rule-based classification, followed by a trained machine learning classifier.

Model effectiveness will be evaluated using precision, recall, accuracy, and F1-score.

### 3. Historical News & Disruption Trend Analysis

Analyze historical semiconductor news activity and distinguish general media attention from identified disruption events.

**Planned capabilities:**
- Visualize semiconductor news coverage over time.
- Compare news attention across monitored companies.
- Identify changes in coverage patterns.
- Analyze the frequency of categorized disruption events.
- Group multiple articles covering the same event.

Historical news volume will be labeled separately from distinct, reviewed disruption event counts.

### 4. Evidence-Based Disruption Prioritization

Develop a transparent framework for prioritizing potential disruption events.

**Evaluation factors:**
- Event severity
- Evidence reliability
- Event recency
- Operational relevance

The resulting indicators will help analysts identify developments that deserve additional investigation.

Scores will include source references, explanations, and relevant limitations.

### 5. Interactive Risk Intelligence Dashboard

Develop an interactive Streamlit application to visualize external semiconductor supply chain developments.

**Planned dashboard components:**
- Semiconductor company selector
- News monitoring feed
- Historical news attention charts
- Disruption category filters
- Event investigation queue
- Evidence and source links
- Event prioritization indicators

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and application logic |
| pandas | Data cleaning and transformation |
| scikit-learn | NLP classification and machine learning |
| Streamlit | Interactive web dashboard |
| Plotly | Historical trends and visualizations |
| GDELT API | News retrieval and historical news activity |
| Git & GitHub | Version control and documentation |
| Visual Studio Code | Development environment |

## Data Sources

The project will use publicly available industry information.

- [GDELT Project](https://www.gdeltproject.org/) — Global news monitoring and historical coverage
- [TSMC Investor Relations](https://investor.tsmc.com/) — Company disclosures
- [ASML Investor Relations](https://www.asml.com/en/investors) — Equipment industry and company disclosures
- [SEC EDGAR](https://www.sec.gov/edgar/search/) — Public company filings

Additional sources will be documented as they are incorporated.

## Development Roadmap

### Phase 1 — Data Collection & Historical Dashboard
- [ ] Configure Python development environment
- [ ] Create project structure
- [ ] Build semiconductor company database
- [ ] Connect to the GDELT API
- [ ] Retrieve real semiconductor news articles
- [ ] Build 30-day historical news attention visualizations
- [ ] Display source-linked news articles in Streamlit

### Phase 2 — Disruption Identification
- [ ] Define disruption categories
- [ ] Implement initial keyword-based classification
- [ ] Identify relevant companies in headlines
- [ ] Manually review and label news samples
- [ ] Train an NLP classification model
- [ ] Evaluate classification performance

### Phase 3 — Risk Intelligence
- [ ] Identify and group distinct disruption events
- [ ] Develop evidence-based prioritization framework
- [ ] Add historical disruption event analysis
- [ ] Build analyst investigation queue
- [ ] Add source verification and event explanations

### Phase 4 — Deployment & Evaluation
- [ ] Finalize Streamlit dashboard
- [ ] Validate event categorization and scoring
- [ ] Measure model performance
- [ ] Benchmark manual versus automated news screening
- [ ] Deploy application using Streamlit Community Cloud
- [ ] Document findings and limitations

## Project Success Metrics

ChipWatch AI will evaluate:

| Metric | Purpose |
|---|---|
| Articles processed | Measure news monitoring coverage |
| Companies monitored | Measure company coverage |
| Classification precision and recall | Evaluate disruption detection quality |
| Macro F1-score | Evaluate performance across categories |
| Company matching precision | Assess correct company identification |
| Duplicate event rate | Evaluate event grouping quality |
| News-screening time | Compare manual and automated workflows |
| Source traceability | Verify that flagged events have supporting evidence |

Actual results will be added as the project progresses.

## Future Enhancements

Potential enhancements include:

- Automated daily news ingestion
- Advanced event extraction using large language models
- AI-generated executive risk intelligence briefs
- Source reliability analysis
- Expanded semiconductor company coverage
- Automatic event alerts
- Supply chain network dependency analysis
- Optional scenario simulations using clearly identified operational assumptions

## Project Purpose

ChipWatch AI is an independent technical portfolio project combining semiconductor industry research, supply chain management, machine learning, and business intelligence.

The goal is to develop a functional, evidence-based external risk intelligence application that demonstrates practical AI development, analytical problem-solving, and the ability to translate unstructured industry information into useful supply chain insights.