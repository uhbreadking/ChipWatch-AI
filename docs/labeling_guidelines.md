# ChipWatch AI: Headline Labeling Guidelines

**Version:** 1.2 (October 2026)  
**Purpose:** Establish consistent manual labeling rules for evaluating keyword-based classification and training a machine learning model to identify semiconductor supply disruption signals.

---

## 1. Core Classification Question

For each headline, answer:

**Does this headline report a real event, formally announced action, or credible developing threat relevant to semiconductor manufacturing, equipment availability, supplier operations, or logistics?**

Label using the **headline only**. Do not open the full article to determine the classification.

Headline classification is not independent verification of the underlying event. Article-level source verification occurs separately.

## 2. Primary Classification Labels

Each headline receives exactly one primary label.

| Label | Definition |
|---|---|
| **Manufacturing** | Actual or credible potential interruptions to semiconductor fabrication, assembly, packaging, testing, or manufacturing operations |
| **Geopolitical** | Government or geopolitical actions affecting semiconductor trade, equipment access, exports, imports, or relevant supply operations |
| **Logistics** | Transportation, shipping, port, border, or distribution disruptions relevant to semiconductor supply |
| **Financial** | Financial distress that directly threatens semiconductor supplier operations or delivery obligations |
| **Not a disruption** | Headlines without a specific disruption, credible supply threat, or relevant disruption lifecycle development |
| **Unclear** | Headline lacks sufficient information for a defensible classification |

**Unclear is an abstention label, not a model training class.** Exclude unresolved headlines from training and evaluation until reviewed.

**The label describes the topic of the event, not whether the news is good or bad.** A lifted restriction is still Geopolitical; its direction is captured by its event status (Section 3). The dashboard uses status, not label alone, to decide what to highlight as urgent.

## 3. Event Status

For relevant disruption headlines, assign one status.

| Status | Definition |
|---|---|
| **Active** | Reported disruption currently affecting operations |
| **Announced** | Specific future restriction or action formally announced |
| **Potential** | Credible developing threat without established operational interruption (see definition below) |
| **Recovery** | Operations improving after an earlier disruption |
| **Resolved** | Previously reported disruption or restriction has ended |
| **None** | No relevant disruption event or lifecycle update |
| **Unclear** | Insufficient information to determine status |

**Definition of Potential:** the headline must name a specific company, facility, or region **and** describe a concrete official action or warning, such as an evacuation order, a typhoon or storm warning, or a production precaution. Speculation, analyst predictions, and questions do not qualify.

**Event status is a descriptive annotation, not a prediction target.** Models are trained and evaluated on `label` only. `event_status` is recorded for analysis and dashboard filtering.

Examples:

| Headline | Label | Status |
|---|---|---|
| TSMC halts production after earthquake | Manufacturing | Active |
| TSMC resumes operations after earthquake | Manufacturing | Recovery |
| US announces new export controls effective next month | Geopolitical | Announced |
| Typhoon warning prompts semiconductor fabs to prepare emergency operations | Manufacturing | Potential |
| US lifts semiconductor equipment export restrictions | Geopolitical | Resolved |
| ASML reports record quarterly earnings | Not a disruption | None |

Event status reflects the headline's claim, not independently verified operational status.

## 4. Decision Rules

**Rule 1 — Stock prices are not disruptions.**  
"Samsung and SK hynix shares fall sharply" → Not a disruption / None.

**Rule 2 — Routine earnings and forecasts are not disruptions.**  
"Analysts forecast memory shortage through 2028" → Not a disruption / None.

**Rule 3 — Negation matters.**  
"TSMC avoids factory shutdown after power grid recovery" → Not a disruption / None. If a credible ongoing operational threat is explicitly established, consider Potential.

**Rule 4 — Distinguish speculation from credible threats.**  
"Will sanctions affect ASML?" → Not a disruption / None.  
"Typhoon warning prompts fabs to prepare emergency operations" → Manufacturing / Potential.

**Rule 5 — Announced future restrictions count.**  
"US announces chip equipment export controls effective next month" → Geopolitical / Announced.

**Rule 6 — Recovery headlines retain their category.**  
"TSMC resumes fabrication operations after earthquake" → Manufacturing / Recovery.

**Rule 7 — Removed or lifted restrictions are Resolved.**  
"Government removes restrictions on equipment exports" → Geopolitical / Resolved. Always use Resolved (not Recovery) when a restriction ends; Recovery is reserved for operations improving after a disruption. Record "risk-reducing" in notes.

**Rule 8 — Drills and simulations are not disruptions.**  
"Semiconductor industrial park conducts earthquake drill" → Not a disruption / None.

**Rule 9 — Choose the primary cause or action when categories overlap.**  
"New export controls delay semiconductor equipment shipments" → Geopolitical, with Logistics noted as secondary. Use Unclear if the primary category cannot reasonably be established.

**Rule 10 — Require semiconductor relevance.**  
"Port strike delays vehicle shipments" → Not a disruption / None.  
"Port strike delays chipmaking equipment shipments" → Logistics / Active.

**Rule 11 — Financial distress must credibly threaten operations.**  
Include bankruptcy, operationally significant defaults, and liquidity crises affecting delivery obligations. Exclude ordinary debt refinancing, stock declines, and routine earnings weakness without evidence of operational consequences.

**Rule 12 — Company mentions do not prove exposure.**  
A headline mentioning TSMC and AMD does not establish that AMD is affected by a TSMC disruption.

**Rule 13 — Label the event, not the company.**  
Disruptions at semiconductor companies outside the six monitored companies are labeled the same way. "Sony halts Kumamoto chip plant operations after earthquake" → Manufacturing / Active. Company relevance is handled by company matching, not by the label.

## 5. Sampling

Disruption headlines are rare in ordinary company news. In early testing, 1 of 100 TSMC headlines and 0 of 72 Samsung headlines were disruption-related. A randomly gathered set of 150–200 headlines would contain too few disruption examples to evaluate or train a classifier.

The labeling set is therefore built from two sources:

| Source | How headlines are gathered | Purpose |
|---|---|---|
| **Ordinary sample** | Each monitored company's standard news query | Represents typical news the dashboard sees |
| **Enriched sample** | Targeted queries likely to return disruption headlines (e.g., `TSMC earthquake`, `chip export controls`, `semiconductor fab fire`, `port strike semiconductors`) | Provides enough examples of each disruption category |

Record each headline's origin in the `sample_source` column.

**Reporting rule:** metrics measured on the combined set show how well the rules or model **distinguish** disruption headlines from ordinary ones. They do **not** represent real-world flag accuracy, because disruptions are far less common in ordinary feeds. Report results separately for the ordinary sample where possible, and state the sampling method alongside every metric.

## 6. Duplicate Event Handling

Different publications may describe the same event.

| Headline | Event Group |
|---|---|
| TSMC suspends production after earthquake | EVT001 |
| Earthquake forces TSMC to halt operations | EVT001 |
| Taiwan earthquake disrupts TSMC production | EVT001 |
| ASML announces new equipment restrictions | EVT002 |

- Assign matching event-group IDs to articles clearly describing the same incident.
- Keep each event group entirely within training or testing.
- Do not automatically assign identical statuses to every headline in a group.
- Separate events when evidence indicates different incidents.

## 7. Labeling Dataset

| Column | Filled by | Required? | Purpose |
|---|---|---|---|
| headline_id | Script | Yes | Unique headline identifier |
| title | Script | Yes | Original headline |
| source | Script | Yes | Publisher |
| published_at | Script | Yes | Publication date |
| search_company | Script | Yes | Company or query that retrieved the article |
| sample_source | Script | Yes | `ordinary` or `enriched` (see Section 5) |
| label | Reviewer | Yes | Primary event category |
| event_status | Reviewer | Yes | Event lifecycle status |
| event_group_id | Reviewer | Yes | Groups articles describing the same event |
| notes | Reviewer | Yes, for hard cases | Ambiguity, secondary categories, reasoning |
| mentioned_companies | Reviewer | Optional in v1.2 | Companies named in the headline; fill only when evaluating the company matcher |
| affected_company | Reviewer | Optional in v1.2 | Directly affected company; fill only when clear from the headline |

**Do not look at keyword-rule predictions while creating ground-truth labels.**

## 8. Labeling Quality Assurance

### Pilot

1. Manually label 30–50 diverse headlines, including both ordinary and enriched samples.
2. Document ambiguous cases.
3. Refine definitions.
4. Re-label 10 randomly selected headlines without seeing original labels.
5. Calculate agreement and review disagreements.
6. Freeze the guidelines version before final evaluation.

### Machine Learning Evaluation

- Remove exact duplicate headlines.
- Group near-duplicate coverage of the same event.
- Prevent event-group overlap between training and testing.
- Train and evaluate on `label` only; exclude Unclear.
- Compare the model against a simple baseline and the keyword rules.
- Measure precision, recall, macro F1-score, and confusion matrix.
- Report the sampling method with every metric (Section 5).
- Document known limitations and difficult cases.

## 9. Classification vs. Event Verification

**Headline classification:** Identifies what a headline appears to report.

**Event verification:** Reviews article content, company disclosures, and supporting sources.

**Disruption prioritization:** Evaluates evidence, severity, operational relevance, and uncertainty to identify events needing further investigation.

A Manufacturing classification does not automatically establish that an actual manufacturing shutdown has been independently verified.

## 10. Change Log

- **1.0 (October 2026):** Initial headline labeling guidelines.
- **1.1 (October 2026):** Added event lifecycle statuses, credible developing threats, recovery tracking, refined financial criteria, event-group handling, company attribution, and evaluation controls.
- **1.2 (October 2026):** Added sampling section (ordinary and enriched samples, reporting rule) and `sample_source` column; clarified that labels describe topic and status describes direction; made `event_status` an annotation rather than a training target; fixed Rule 7 to always use Resolved for lifted restrictions; added a concrete definition of Potential; made `mentioned_companies` and `affected_company` optional.
- **1.3 (October 2026):** Added Rule 13: disruptions are labeled regardless of which company they affect.