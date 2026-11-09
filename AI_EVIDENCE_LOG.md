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
| Dataset | R01–R10 |
| Number of records | 10 |
| Data type | Illustrative practice data |
| Original collection source | User-provided practice dataset |
| Collection period | Not applicable |
| Verified public feedback | None |
| Verified interviews | None |

**Research integrity:** R01–R10 are illustrative practice records. They must not be represented as actual Groww customers, verified interviews, or feedback collected from public platforms.

Potential future sources include Google Play Store reviews, Apple App Store reviews, Reddit investing communities, TradingQ&A, public YouTube comments, and public personal-finance forums. No collection from these platforms is claimed at this stage.

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

The current golden set contains ten human-approved **illustrative** labels in `golden_set.csv`. These are practice annotations, not independently validated labels or findings about actual investors.

## 6. Evaluation methodology and results

The evaluation compares `predictions.csv` with `golden_set.csv` using record IDs. It calculates:
- Per-theme precision, recall and F1 across all five themes.
- Micro precision, recall and F1.
- Macro F1, averaging themes with at least one reference or predicted example. Themes with neither are unassessed and excluded.
- Exact-match accuracy.

Current results on the ten illustrative records:

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

- Only ten illustrative records are available.
- No verified public feedback has been collected.
- No actual interview findings are included.
- The sample cannot represent all first-time investors or Groww customers.
- Reference labels have not been independently validated.
- Some themes have too few or no examples for meaningful assessment.
- Confidence scores are not calibrated.
- Multilingual performance is unknown.
- Classification metrics do not test groundedness, factual accuracy, safety, or appropriate refusal.
- No causal relationship between product usage and SIP continuation has been demonstrated.

## 9. Research integrity statement

This project demonstrates a technical workflow using illustrative practice data. It does not claim verified customer findings, completed public-platform collection, actual investor interviews, improved SIP continuation, or production-level AI accuracy.

## 10. Next steps

1. Collect permitted public feedback and record source URLs and collection dates.
2. Anonymise records and preserve provenance.
3. Expand the golden set to approximately 20 or more genuine feedback items.
4. Have labels independently reviewed and disagreements adjudicated.
5. Evaluate groundedness, factual accuracy, safety, and fallback separately.
6. Conduct and document primary research if participants can be recruited.
7. Test the product with target users and record actual results.
