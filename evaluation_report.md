
# Groww Investor Voice - Evaluation Report

## 1. Evaluation purpose

Test the multi-label evaluation pipeline using the illustrative
R01-R10 practice dataset.

## 2. Dataset

- Total records: 10
- Dataset type: Illustrative practice data
- Reference labels: Human-approved illustrative labels
- Prediction type: Manually prepared rule-based baseline
- Evaluation date: 9 November 2026

## 3. Overall results

| Metric | Result |
|---|---:|
| Micro Precision | 1.000 |
| Micro Recall | 0.917 |
| Micro F1 | 0.957 |
| Exact Match Accuracy | 0.900 |

## 4. Per-theme results

| Theme | Precision | Recall | F1 |
|---|---:|---:|---:|
| Performance uncertainty | 1.000 | 1.000 | 1.000 |
| Operational understanding | 1.000 | 1.000 | 1.000 |
| Investment knowledge | 1.000 | 1.000 | 1.000 |
| Financial flexibility | 1.000 | 0.500 | 0.667 |

## 5. Error analysis

Record R06 was missing the Financial flexibility label.

Reference:
Operational understanding; Financial flexibility

Prediction:
Operational understanding

This represents one false negative.

## 6. Evaluation thresholds

Predeclared demonstration thresholds:

- Micro F1 >= 0.80
- Exact match >= 0.70

Both numerical thresholds were met.

## 7. Limitations

1. Only ten illustrative records were evaluated.
2. Predictions were manually prepared.
3. Reference labels were created for practice purposes.
4. Predictions and reference labels were not independently produced.
5. Results do not establish actual AI model performance.
6. Results do not establish production safety or reliability.

## 8. Conclusion

The evaluation pipeline successfully calculated
multi-label classification metrics and identified
a missing Financial flexibility label.

This is a technical demonstration, not evidence
of validated AI classification quality.

The next evaluation must use actual AI-generated
predictions against independently reviewed labels.
