# Expanded 20-record mixed-source evaluation — 9 November 2026

## Important qualification
This is an **analyst-labelled, provisional** mixed dataset: 10 illustrative practice records (R01–R10) and 10 paraphrases of linked public Reddit posts (P11–P20). The public posts are not verified Groww users and may not be first-time SIP investors. No independent second annotator has adjudicated the labels.

Predictions in `predictions.csv` are a **deterministic keyword-rule baseline**, not GPT-4o-mini predictions. The earlier 10-record results are not comparable as AI model quality evidence.

## Computed multi-label baseline (20 records)
| Metric | Value |
|---|---:|
| Micro precision | 1.000 |
| Micro recall | 0.630 |
| Micro F1 | 0.773 |
| Macro F1 | 0.760 |
| Exact match | 0.650 |

| Theme | TP | FP | FN | F1 |
|---|---:|---:|---:|---:|
| Performance uncertainty | 5 | 0 | 0 | 1.000 |
| Operational understanding | 8 | 0 | 4 | 0.800 |
| Investment knowledge | 2 | 0 | 2 | 0.667 |
| Financial flexibility | 1 | 0 | 4 | 0.333 |
| External guidance seeking | 1 | 0 | 0 | 1.000 |

These figures were computed by matching the two CSV files on record_id and evaluating each allowed theme as a binary label. This is **not** a measured AI-model evaluation or a production-readiness assessment.

## Provenance
See `public_feedback_records.csv` for ten individually linked Reddit source posts, dates and analyst paraphrases. Posts were manually labelled by the project assistant as a first pass; a second human reviewer should check them against the original posts. The old `evaluation_report.md` covers the earlier ten illustrative records only.

## Follow-up
Independently adjudicate all 20 labels, verify the source posts remain accessible, evaluate actual GPT-4o-mini predictions on the 20-record set, and test groundedness, unsafe advice and fallback separately.
