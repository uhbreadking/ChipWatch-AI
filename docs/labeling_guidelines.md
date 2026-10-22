# ChipWatch AI: Headline Labeling Guidelines

**Version:** 1.3 (October 2026)  
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

**Unclear is an abstention label, not a model training class.** Exclude unresolved headlines from training and evaluation until reviewed. Use Unclear only when the rules below genuinely cannot decide a headline; if a rule decides it, apply the rule.

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

**Definition of Potential:** the headline must name a specific company, facility, or region **and** describe a concrete official action or warning, such as an evacuation order, a typhoon or storm warning, or a production precaution. Speculation, analyst predictions, industry "fears," and questions do not qualify.

**Event status is a descriptive annotation, not a prediction target.** Models are trained and evaluated on `label` only. `event_status` is recorded for analysis and dashboard filtering.

**Label and status pairing:**

| If label is... | Then event_status is... |
|---|---|
| Not a disruption | None |
| Manufacturing, Geopolitical, Logistics, or Financial | Active, Announced, Potential, Recovery, or Resolved |
| Unclear | Unclear |

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
"Samsung and SK hynix shares fall sharply" → Not a disruption / None. Analyst price targets and buy/sell ratings are covered by this rule.

**Rule 2 — Routine earnings, forecasts, and shortages without a stated cause are not disruptions.**  
"Analysts forecast memory shortage through 2028" → Not a disruption / None.  
A shortage is labeled by its stated cause: "Fab fire worsens memory shortage" → Manufacturing / Active. If no disruptive cause is named, or the cause is demand, label Not a disruption / None.

**Rule 3 — Negation matters.**  
"TSMC avoids factory shutdown after power grid recovery" → Not a disruption / None. If a credible ongoing operational threat is explicitly established, consider Potential (see Rule 14).

**Rule 4 — Distinguish speculation from credible threats.**  
"Will sanctions affect ASML?" → Not a disruption / None.  
"Typhoon warning prompts fabs to prepare emergency operations" → Manufacturing / Potential.

**Rule 5 — Announced future restrictions count; commentary does not.**  
"US announces chip equipment export controls effective next month" → Geopolitical / Announced.  
Policy proposals, opinion pieces, and calls for action are not announcements, even when they discuss restrictions. "Strengthening America's AI Chip Export Controls" (think-tank essay) → Not a disruption / None. Headlines built around "should," "must," or a proposal are a strong sign of commentary.

**Rule 6 — Recovery headlines retain their category.**  
"TSMC resumes fabrication operations after earthquake" → Manufacturing / Recovery.

**Rule 7 — Removed or lifted restrictions are Resolved.**  
"Government removes restrictions on equipment exports" → Geopolitical / Resolved. Always use Resolved (not Recovery) when a restriction ends; Recovery is reserved for operations improving after a disruption. Record "risk-reducing" in notes.

**Rule 8 — Drills and simulations are not disruptions.**  
"Semiconductor industrial park conducts earthquake drill" → Not a disruption / None.

**Rule 9 — Choose the primary cause or action when categories overlap.**  
"New export controls delay semiconductor equipment shipments" → Geopolitical, with Logistics noted as secondary. Use Unclear if the primary category cannot reasonably be established.

**Rule 10 — The semiconductor link must be stated in the headline.**  
"Port strike delays vehicle shipments" → Not a disruption / None.  
"Port strike delays chipmaking equipment shipments" → Logistics / Active.  
Vague terms such as "critical supplies," "supply shock," or "key materials" do not establish a semiconductor link on their own. The search query that retrieved an article is not evidence, because search engines match on article text the classifier never sees.  
"Iran war squeezes critical supplies and global alliances" → Not a disruption / None.  
"Iran war disrupts helium supplies used in chipmaking" → Geopolitical / Active.

**Rule 11 — Financial distress must credibly threaten operations.**  
Include bankruptcy, operationally significant defaults, and liquidity crises affecting delivery obligations. Exclude ordinary debt refinancing, stock declines, and routine earnings weakness without evidence of operational consequences.

**Rule 12 — Company mentions do not prove exposure.**  
A headline mentioning TSMC and AMD does not establish that AMD is affected by a TSMC disruption.

**Rule 13 — Label the event, not the company.**  
Disruptions at semiconductor companies outside the six monitored companies are labeled the same way. "Sony halts Kumamoto chip plant operations after Japan earthquake" → Manufacturing / Active. Company relevance is handled by company matching, not by the label.  
Confirm the facility makes semiconductors or chip equipment: "Snyder of Berlin plant to close" (snack food) → Not a disruption / None.

**Rule 14 — Precautions after a hazard are Potential; a clean all-clear is not a disruption.**  
If a headline reports official precautionary actions at a named facility (evacuations, inspections, suspended operations pending checks), label the hazard's category with status Potential, even if no damage is reported.  
"Quake spares TSMC Kumamoto as Japan evacuates staff and inspects plants" → Manufacturing / Potential.  
If the headline reports no impact and no ongoing precautions, label Not a disruption / None, even if a hazard occurred.  
"TSMC's leading-edge chip plant suffers 90% voltage drop – production unaffected says firm" → Not a disruption / None.  
A company's claim of no impact is recorded as reported; verifying it is part of event verification (Section 9), not labeling.

## 5. Sampling

Disruption headlines are rare in ordinary company news. In early testing, 1 of 100 TSMC headlines and 0 of 72 Samsung headlines were disruption-related. A randomly gathered set of 150–200 headlines would contain too few disruption examples to evaluate or train a classifier.

The labeling set is therefore built from two sources:

| Source | How headlines are gathered | Purpose |
|---|---|---|
| **Ordinary sample** | Each monitored company's standard news query | Represents typical news the dashboard sees |
| **Enriched sample** | Targeted queries likely to return disruption headlines (e.g., `chip export controls`, `semiconductor fab fire`, `port strike semiconductors`) | Provides enough examples of each disruption category |

Record each headline's origin in the `sample_source` column.

**Reporting rule:** metrics measured on the combined set show how well the rules or model **distinguish** disruption headlines from ordinary ones. They do **not** represent real-world flag accuracy, because disruptions are far less common in ordinary feeds. Report results separately for the ordinary sample where possible, and state the sampling method alongside every metric.

Enriched queries can return off-topic results (for example, `chip plant shutdown` returned a snack food plant closure). Keep these and label them normally; they are useful negative examples.

## 6. Duplicate Event Handling

Different publications may describe the same event.

| Headline | Event Group |
|---|---|
| TSMC suspends production after earthquake | EVT001 |
| Earthquake forces TSMC to halt operations | EVT001 |
| Taiwan earthquake disrupts TSMC production | EVT001 |
| ASML announces new equipment restrictions | EVT002 |

- Assign matching event-group IDs to articles clearly describing the same incident.
- Leave `event_group_id` blank for headlines with no duplicate.
- Keep each event group entirely within training or testing.
- Do not automatically assign identical statuses to every headline in a group.
- Separate events when evidence indicates different incidents.

## 7. Labeling Dataset

| Column | Filled by | Required? | Purpose |
|---|---|---|---|
| headline_id | Script | Yes | Unique headline identifier |
| title | Script | Yes | Original headline (never edited) |
| source | Script | Yes | Publisher |
| published_at | Script | Yes | Publication date |
| search_company | Script | Yes | Company or query that retrieved the article |
| sample_source | Script | Yes | `ordinary` or `enriched` (see Section 5) |
| label | Reviewer | Yes | Primary event category |
| event_status | Reviewer | Yes | Event lifecycle status |
| event_group_id | Reviewer | For duplicates | Groups articles describing the same event |
| notes | Reviewer | For hard cases | Reasoning, secondary categories, Unclear reasons |
| mentioned_companies | Reviewer | Optional | Companies named in the headline; fill only when evaluating the company matcher |

**Do not look at keyword-rule predictions while creating ground-truth labels.**

**Notes convention:** mark any headline you hesitated on with `HARD`, followed by the rule that decided it and a short reason, for example: `HARD (Rule 14): plant spared, but evacuation and inspections are official actions`. Citing the rule confirms it was checked and shows which rules are used most.

**Technical note:** `None` is a valid status value, but pandas reads the text "None" as a missing value by default. Always read label files with `keep_default_na=False`.

## 8. Labeling Quality Assurance

### Pilot

1. Manually label 30–50 diverse headlines, including both ordinary and enriched samples.
2. Document ambiguous cases.
3. Refine definitions.
4. Re-label 10 randomly selected headlines without seeing original labels.
5. Calculate agreement and review disagreements.
6. Freeze the guidelines version before final evaluation.

Because disruption labels are rare, a random re-label sample may contain only Not a disruption headlines. After the full set is labeled, run a second consistency check sampled from disruption-labeled headlines.

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

**Event verification:** Reviews article content, company disclosures, and supporting sources, and records which companies are actually affected.

**Disruption prioritization:** Evaluates evidence, severity, operational relevance, and uncertainty to identify events needing further investigation.

A Manufacturing classification does not automatically establish that an actual manufacturing shutdown has been independently verified.

## 10. Pilot Results

| Measure | Result |
|---|---|
| Headlines labeled in pilot | 40 of 201 |
| Consistency check (10 headlines re-labeled blind) | Label agreement 10/10; status agreement 10/10 |
| Hard cases recorded | 6 |

**Caveat:** all 10 re-labeled headlines were Not a disruption, so the check confirms consistency on ordinary news but not yet on disruption labels (see Section 8).

**Hard-case themes and resulting changes:**

| Theme | Example | Change |
|---|---|---|
| No stated semiconductor link | "Iran war squeezes critical supplies and global alliances" | Rule 10 clarified |
| Commentary and opinion | "China's tightening grip on its most advanced AI should be a warning signal for India" | Rule 5 extended |
| Hazards with or without precautions | Kumamoto quake evacuation; voltage drop with production unaffected | Rule 14 added |

## 11. Change Log

- **1.0 (October 2026):** Initial headline labeling guidelines.
- **1.1 (October 2026):** Added event lifecycle statuses, credible developing threats, recovery tracking, refined financial criteria, event-group handling, company attribution, and evaluation controls.
- **1.2 (October 2026):** Added sampling section (ordinary and enriched samples, reporting rule) and `sample_source` column; clarified that labels describe topic and status describes direction; made `event_status` an annotation rather than a training target; fixed Rule 7 to always use Resolved for lifted restrictions; added a concrete definition of Potential; made `mentioned_companies` and `affected_company` optional.
- **1.3 (October 2026):** Updated after the 40-headline pilot. Removed `affected_company` (determining exposure requires reading the article, so it moves to event verification). Clarified Rule 1 (analyst price targets), Rule 2 (shortages labeled by stated cause), Rule 5 (commentary is not an announcement), and Rule 10 (semiconductor link must be stated in the headline). Added Rule 13 (label the event, not the company) and Rule 14 (precautions after a hazard). Added label/status pairing table, notes convention, technical note on reading "None," a second consistency check for disruption labels, and pilot results.