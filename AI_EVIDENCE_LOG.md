Groww Investor Voice — AI Evidence Log

Project: AI-powered customer discovery for first-time mutual fund investors
Business context: Groww Growth Team
Evaluation date: 9 November 2026
Research status: Preliminary technical demonstration

1. Research Objective

Explore the challenges faced by first-time mutual fund investors during their first year of SIP investing.

The broader business objective is to understand opportunities to improve 12-month active SIP continuation.

The discovery engine is designed to:

Organise qualitative feedback.
Identify recurring themes.
Classify investor concerns using AI.
Identify potential product opportunities.
Support human review of AI-generated insights.
2. Evidence Sources
Current dataset
Attribute	Details
Dataset name	R01–R10
Number of records	10
Data type	Illustrative practice data
Original collection source	User-provided practice dataset
Collection period	Not applicable
Verified public feedback	None
Verified interviews	None

Research integrity: The R01–R10 records are illustrative practice data. They must not be represented as actual Groww customers, verified interviews or publicly collected investor feedback.

Future research sources

Potential sources for future collection include:

Google Play Store reviews
Apple App Store reviews
Reddit investing communities
TradingQ&A
Public YouTube comments
Public personal finance forums

No collection from these platforms is claimed at this stage.

3. Dataset Schema

The discovery application supports feedback records containing information such as:

Record ID
Original feedback
Source
Source URL
Collection date
Language
User type
SIP lifecycle stage
Confusion or concern
External workaround
Human validation status

Missing information should remain unknown rather than being inferred.

4. Classification Taxonomy

The current theme taxonomy contains:

Performance uncertainty
Operational understanding
Investment knowledge
Financial flexibility
External guidance seeking

Multi-label classification is supported because one feedback item may contain multiple concerns.

5. AI Classification Methodology

Model: GPT-4o-mini

Application: Streamlit

Programming language: Python

AI provider: OpenAI API

The classification workflow:

User uploads a CSV or selects the built-in practice dataset.
User selects the feedback text column.
Feedback is sent to the AI model when AI mode is selected.
AI generates structured JSON classifications.
The application validates the output.
Invalid outputs use a rule-based fallback.
Results are displayed for human review.
Results can be downloaded as CSV.

AI-generated confidence scores are estimates, not calibrated probabilities.

6. Golden Evaluation Dataset

The current golden dataset contains ten human-approved illustrative labels.

Record	Reference themes
R01	Performance uncertainty
R02	Operational understanding
R03	Operational understanding
R04	Performance uncertainty
R05	Investment knowledge; Performance uncertainty
R06	Operational understanding; Financial flexibility
R07	Financial flexibility
R08	Investment knowledge
R09	Performance uncertainty
R10	Performance uncertainty

These labels are approved practice annotations, not independently verified research findings.

7. Evaluation Methodology

The evaluation script compares AI predictions with reference labels using:

Micro precision
Micro recall
Micro F1
Macro F1
Exact-match accuracy
Per-theme precision, recall and F1

The evaluation uses record IDs to match the reference and prediction datasets.

8. Evaluation Results

Records evaluated: 10

Metric	Result
Micro precision	1.000
Micro recall	0.917
Micro F1	0.957
Macro F1	0.733
Exact match	0.900
Per-theme results
Theme	Precision	Recall	F1
Performance uncertainty	1.000	1.000	1.000
Operational understanding	1.000	1.000	1.000
Investment knowledge	1.000	1.000	1.000
Financial flexibility	1.000	0.500	0.667
External guidance seeking	N/A	N/A	N/A

External guidance seeking had zero positive reference examples.

9. Error Analysis
Record R06

Feedback: Automatic deduction concerns

Reference labels:

Operational understanding
Financial flexibility

AI prediction:

Operational understanding

Error: Financial flexibility was missed.

This is one false negative.

The example demonstrates the importance of multi-label evaluation and human review.

The reference label should also be reviewed because the original statement does not explicitly establish financial hardship.

10. Evaluation Gate Status

The current numerical demonstration thresholds are:

Micro F1: at least 0.80
Exact-match accuracy: at least 0.70

Both thresholds were met on the illustrative evaluation dataset.

However, this does not establish production readiness.

The following still require separate testing:

Groundedness
Factual accuracy
Safety compliance
Hallucination
Appropriate refusal
Multilingual classification
Confidence calibration
11. Human Validation

All AI-generated classifications remain provisional.

Human researchers should verify:

Whether the evidence quotation is accurate.
Whether the assigned themes are justified.
Whether AI has invented information.
Whether inferred root causes are clearly labelled as hypotheses.
Whether the output is suitable for inclusion in research findings.
12. Limitations and Biases
Only ten illustrative records are available.
No verified public feedback has been collected.
No actual interview findings are included.
The practice dataset cannot represent all first-time investors.
Theme frequencies cannot be generalised to Groww customers.
Reference labels have not been independently validated.
Some themes have insufficient examples for meaningful evaluation.
AI confidence scores are not calibrated.
Multilingual performance has not been established.
No causal relationship between product usage and SIP continuation has been demonstrated.
13. Research Integrity Statement

This project currently demonstrates the technical workflow of an AI-powered customer discovery engine using illustrative practice data.

It does not claim:

Verified customer research findings.
Completed public-platform data collection.
Actual investor interview findings.
Improved SIP continuation.
Production-level AI accuracy.

Future findings will be documented with source links, collection dates, anonymised evidence and human validation.

14. Next Steps
Collect permitted public feedback.
Expand the evaluation dataset.
Recruit first-time SIP investors.
Conduct primary research interviews.
Validate discovery hypotheses.
Identify and prioritise a genuine user problem.
Refine the AI evaluation gate.
Test the product with target users.

Document status: Preliminary AI Evidence Log
Last updated: 9 November 2026
