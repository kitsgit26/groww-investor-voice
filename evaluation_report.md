Groww Investor Voice - Evaluation Report
1. Evaluation Purpose

Evaluate the multi-label theme classification pipeline using the illustrative R01–R10 practice dataset.

The evaluation compares downloaded AI-generated theme predictions against human-approved illustrative reference labels.

2. Dataset
Total records: 10
Dataset type: Illustrative practice data
Reference labels: Human-approved illustrative labels
Prediction type: AI-generated theme predictions
Model: GPT-4o-mini
Evaluation date: 9 November 2026

These records are not verified investor interviews or publicly collected customer feedback.

3. Overall Results
Metric	Result
Records evaluated	10
Micro Precision	1.000
Micro Recall	0.917
Micro F1	0.957
Macro F1	0.733
Exact Match Accuracy	0.900
4. Per-Theme Results
Theme	Precision	Recall	F1	Support
Performance uncertainty	1.000	1.000	1.000	5
Operational understanding	1.000	1.000	1.000	3
Investment knowledge	1.000	1.000	1.000	2
Financial flexibility	1.000	0.500	0.667	2
External guidance seeking	N/A	N/A	N/A	0

External guidance seeking had no positive reference examples, so its classification performance could not be evaluated.

5. Error Analysis
Record R06

Feedback: Automatic deduction concerns

Reference labels:

Operational understanding
Financial flexibility

AI prediction:

Operational understanding

Error: One false negative. The AI missed the Financial flexibility label.

Interpretation: The AI identified the operational concern but did not predict the additional human-approved theme.

The reference label itself should also be reviewed because the short feedback statement does not explicitly establish financial difficulty or affordability concerns.

6. Evaluation Thresholds

Predeclared demonstration thresholds:

Micro F1 >= 0.80
Exact Match Accuracy >= 0.70

Observed results:

Micro F1: 0.957
Exact Match Accuracy: 0.900

Both numerical thresholds were met on this illustrative evaluation dataset.

Meeting these thresholds does not establish production readiness.

7. Limitations
Only ten illustrative records were evaluated.
The dataset is not representative of Groww customers.
Reference labels were created for practice purposes.
The small dataset limits confidence in per-theme metrics.
External guidance seeking had zero positive examples.
The reference labels have not been independently validated.
This evaluation covers theme classification only.
Sentiment, emotion, lifecycle classification, groundedness and safety were not independently evaluated.
Confidence calibration has not been tested.
The evaluation does not establish production safety or reliability.
8. Conclusion

The AI classification pipeline successfully generated predictions and the evaluation script calculated multi-label classification metrics.

The system achieved:

Micro F1: 0.957
Macro F1: 0.733
Exact Match Accuracy: 0.900

One missed Financial flexibility label was identified in R06.

These results demonstrate preliminary technical functionality on illustrative practice data, not validated AI classification accuracy on real investors.

Further evaluation using diverse, authentic feedback and independently reviewed reference labels is required.

9. Next Steps
Review the R06 reference label.
Expand the golden evaluation dataset.
Include positive examples for every theme.
Test multilingual feedback.
Evaluate hallucination and unsafe investment-advice behaviour separately.
Establish an evaluation gate with a safe fallback.
Conduct human validation before using AI classifications as research findings.

Research Integrity Statement: All reported results refer exclusively to the ten illustrative practice records. No real investor research findings are claimed.
