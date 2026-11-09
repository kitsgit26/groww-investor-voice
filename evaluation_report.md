# Groww Investor Voice — Evaluation Report

## 1. Evaluation purpose

Evaluate multi-label theme classification using the R01–R10 illustrative practice dataset. Predictions are compared with human-approved illustrative reference labels.

## 2. Dataset

| Attribute | Details |
|---|---|
| Records evaluated | 10 |
| Dataset type | Illustrative practice data |
| Reference labels | Human-approved illustrative labels |
| Prediction source | `predictions.csv` |
| Model recorded in project | GPT-4o-mini |
| Evaluation date | 9 November 2026 |

These records are not verified investor interviews or publicly collected customer feedback.

## 3. Overall results

| Metric | Result |
|---|---:|
| Records evaluated | 10 |
| Micro precision | 1.000 |
| Micro recall | 0.917 |
| Micro F1 | 0.957 |
| Macro F1 | 0.917 |
| Exact-match accuracy | 0.900 |

**Macro F1 definition:** the unweighted mean of per-theme F1 scores for themes with at least one reference or predicted example. A theme with neither reference nor predicted examples is unassessed and excluded, rather than being assigned an artificial zero.

## 4. Per-theme results

| Theme | Precision | Recall | F1 | Reference support |
|---|---:|---:|---:|---:|
| Performance uncertainty | 1.000 | 1.000 | 1.000 | 5 |
| Operational understanding | 1.000 | 1.000 | 1.000 | 3 |
| Investment knowledge | 1.000 | 1.000 | 1.000 | 2 |
| Financial flexibility | 1.000 | 0.500 | 0.667 | 2 |
| External guidance seeking | N/A | N/A | N/A | 0 |

External guidance seeking has no reference or predicted examples in this dataset. Its performance is therefore unassessed.

## 5. Error analysis

**Record R06**

- Feedback: “Automatic deduction concerns”
- Reference labels: Operational understanding; Financial flexibility
- Prediction: Operational understanding
- Error: Financial flexibility was missed (one false negative).

The reference label itself should also be reviewed: the short phrase does not explicitly establish financial difficulty or affordability concerns. This illustrates that disagreement may reflect an ambiguous reference label as well as a model error.

## 6. Evaluation thresholds

Pre-declared demonstration thresholds:

- Micro F1 ≥ 0.80
- Exact-match accuracy ≥ 0.70

The current predictions meet both numerical thresholds on this illustrative dataset. This is a technical demonstration only, not evidence of production readiness.

## 7. Limitations

- Only ten illustrative records were evaluated.
- The dataset is not representative of Groww customers or Indian first-time SIP investors.
- Reference labels were created for practice and have not been independently validated.
- External guidance seeking has no examples and cannot be assessed.
- The small sample makes all metrics unstable and highly sensitive to individual records.
- This evaluation covers theme labels only; it does not evaluate factual accuracy, evidence groundedness, sentiment, emotion, lifecycle classification, safety, refusal behaviour, multilingual performance, or confidence calibration.
- The metrics do not establish any causal relationship between product usage and SIP continuation.

## 8. Conclusion and next steps

The evaluation script now calculates per-theme precision, recall and F1, micro F1, macro F1, and exact-match accuracy across the full five-theme taxonomy. One missed Financial flexibility label is visible in R06.

Next steps:
1. Review ambiguous reference labels, including R06.
2. Build a larger golden set from permitted, genuinely sourced and anonymised public feedback.
3. Have labels independently reviewed and adjudicate disagreements.
4. Include sufficient examples for every theme.
5. Evaluate groundedness, hallucination, unsafe investment advice and appropriate fallback separately.
6. Keep human review mandatory.

**Research integrity statement:** All reported metrics refer exclusively to the ten illustrative practice records. They must not be presented as validated accuracy on real investors.
