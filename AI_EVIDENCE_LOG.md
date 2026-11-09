# Groww Investor Voice — AI Evidence Log

Project: AI-powered customer discovery for first-time mutual fund investors  
Business context: Groww Growth Team (independent academic prototype)  
Evaluation date: 9 November 2026  
Research status: Preliminary technical demonstration

## 1. Research objective

Explore challenges faced by first-time mutual fund investors during their first year of SIP investing. The broader business objective is to understand opportunities to improve 12-month active SIP continuation.

The discovery engine is intended to organise qualitative feedback, identify recurring themes, support AI-assisted classification, and keep human review visible.

## 2. Evidence sources and provenance

| Attribute | Current status |
|---|---|
| Dataset | R01–R10 illustrative; P11–P20 public-post paraphrases |
| Number of records | 20 (10 illustrative + 10 public-post paraphrases) |
| Data type | Mixed: 10 illustrative records and 10 sourced Reddit-post paraphrases |
| Original collection source | Practice data + individually linked public Reddit posts |
| Collection period | Public posts dated 2024–2026; reviewed 9 November 2026 |
| Verified public feedback | 10 publicly accessible Reddit discussion posts; provenance links in public_feedback_records.csv |
| Verified interviews | None |

**Research integrity:** R01–R10 are illustrative practice records. They must not be represented as actual Groww customers, verified interviews, or feedback collected from public platforms.

Other potential sources include Google Play Store reviews, Apple App Store reviews, Reddit investing communities, TradingQ&A, public YouTube comments, and public personal-finance forums. Only the ten linked Reddit posts are claimed as public-source collection; other platforms have not been collected.

## 3. Classification taxonomy

The current application taxonomy contains five multi-label themes:
- Performance uncertainty
- Operational understanding
- Investment knowledge
- Financial flexibility
- External guidance seeking

A feedback item may receive more than one theme when the evidence supports it. Missing information must remain unknown rather than inferred.

## 4. AI classification workflow

- Model configured in the application: GPT-4o-mini.
- Application: Streamlit; language: Python.
- User uploads a CSV or selects the built-in illustrative practice data.
- The user selects the feedback text column.
- In AI mode, the text is sent to the model and a structured JSON response is requested.
- The application checks required fields, allowed theme labels, evidence quotation grounding, confidence range, and a limited set of unsafe investment-advice phrases.
- Invalid responses trigger a rule-based fallback.
- Results remain provisional and require human review.

The model's confidence field is an uncalibrated estimate, not a probability that the classification is correct. The current safety phrase screen is limited and is not a comprehensive safety evaluation.

## 5. Golden evaluation dataset

The expanded `golden_set.csv` contains 20 rows: R01–R10 illustrative practice labels and P11–P20 analyst-labelled paraphrases of linked public Reddit posts. The new labels are provisional and have not been independently adjudicated. `public_feedback_records.csv` preserves source links and dates. This is **not** a 20-person first-time-investor sample; the public posts' first-time status is mostly unknown.

## 6. Evaluation methodology and results

The evaluation compares `predictions.csv` with `golden_set.csv` using record IDs. It calculates:
- Per-theme precision, recall and F1 across all five themes.
- Micro precision, recall and F1.
- Macro F1, averaging themes with at least one reference or predicted example. Themes with neither are unassessed and excluded.
- Exact-match accuracy.

**Historical baseline, R01–R10 only:**

| Metric | Result |
|---|---:|
| Micro precision | 1.000 |
| Micro recall | 0.917 |
| Micro F1 | 0.957 |
| Macro F1 | 0.917 |
| Exact-match accuracy | 0.900 |

Per-theme results:

| Theme | Precision | Recall | F1 | Reference support |
|---|---:|---:|---:|---:|
| Performance uncertainty | 1.000 | 1.000 | 1.000 | 5 |
| Operational understanding | 1.000 | 1.000 | 1.000 | 3 |
| Investment knowledge | 1.000 | 1.000 | 1.000 | 2 |
| Financial flexibility | 1.000 | 0.500 | 0.667 | 2 |
| External guidance seeking | N/A | N/A | N/A | 0 |

External guidance seeking has no reference or predicted examples, so its performance is unassessed. R06 has one false-negative Financial flexibility label; the reference label itself is ambiguous because “Automatic deduction concerns” does not explicitly establish financial difficulty.

Pre-declared demonstration thresholds are micro F1 ≥ 0.80 and exact-match accuracy ≥ 0.70. Both are met on this small illustrative dataset only. These metrics do not establish production readiness, factual accuracy, groundedness, or AI safety.

## 7. Human validation

Human reviewers should verify:
- Whether evidence quotations exactly match the original feedback.
- Whether each theme is justified by the text.
- Whether hypotheses are clearly separated from explicit evidence.
- Whether any unsupported experience or motivation has been invented.
- Whether ambiguous reference labels should be revised or adjudicated.

## 8. Limitations and bias

- The combined file has 20 rows, of which only 10 are sourced public feedback; 10 remain illustrative.
- Ten public Reddit discussions were sourced and paraphrased; they are not verified Groww customers or necessarily first-time SIP investors.
- No actual interview findings are included.
- The sample cannot represent all first-time investors or Groww customers.
- Reference labels have not been independently validated.
- Some themes have too few or no examples for meaningful assessment.
- Confidence scores are not calibrated.
- Multilingual performance is unknown.
- Classification metrics do not test groundedness, factual accuracy, safety, or appropriate refusal.
- No causal relationship between product usage and SIP continuation has been demonstrated.

## 9. Research integrity statement

This project demonstrates a technical workflow using illustrative practice data plus ten linked public Reddit discussions. It does not claim verified Groww customer findings, actual investor interviews, improved SIP continuation, or production-level AI accuracy.

## 10. Next steps

1. Collect permitted public feedback and record source URLs and collection dates.
2. Anonymise records and preserve provenance.
3. Expand the golden set to approximately 20 or more genuine feedback items.
4. Have labels independently reviewed and disagreements adjudicated.
5. Evaluate groundedness, factual accuracy, safety, and fallback separately.
6. Conduct and document primary research if participants can be recruited.
7. Test the product with target users and record actual results.

## 11. Public feedback expansion (9 November 2026)

Ten public Reddit discussion posts were added as P11–P20. Each record is an **analyst paraphrase**, not a verbatim quote. Exact post URLs and original dates are recorded in `public_feedback_records.csv`. They represent self-reported public experiences, not verified events or platform performance facts. They were manually assigned provisional multi-label reference themes, requiring independent review.

The expanded `predictions.csv` adds **deterministic keyword-rule predictions**, not GPT-4o-mini outputs. The previous 0.957 micro-F1 / 0.900 exact-match scores apply **only to the earlier 10 illustrative records**; they must not be presented as 20-record results. Run `python evaluate.py` to obtain new mixed-set rule-baseline metrics. The mixed set is not a valid estimate of model accuracy on genuine first-time Groww customers.

