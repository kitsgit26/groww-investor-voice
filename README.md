# Groww Investor Voice

An independent AI-powered customer-discovery prototype exploring first-time mutual fund investor experiences. This is an academic prototype and is not affiliated with Groww.

## Features
- CSV feedback upload
- Rule-based thematic classification
- Optional AI classification
- Evidence quotation validation
- Rule-based fallback for invalid AI output
- Human review workflow
- Theme frequency analysis
- CSV export

## Technology
- Python
- Streamlit
- Pandas
- OpenAI API

## Research integrity
The built-in R01–R10 records and their labels are illustrative practice data. They are not verified Groww customer feedback, public reviews, or interviews. The current evaluation scores describe only this small illustrative dataset and must not be presented as real-world model accuracy.

## Safety
This tool supports qualitative research analysis, not investment advice. It does not recommend mutual funds or stocks. AI outputs are provisional and require human review.

## Run locally
Install dependencies:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Evaluate the illustrative classifier predictions
Run:

```bash
python evaluate.py --gold golden_set.csv --predictions predictions.csv
```

The evaluator checks dataset integrity and record matching, then reports per-theme precision/recall/F1, micro F1, macro F1, and exact-match accuracy. Macro F1 excludes themes with neither reference nor predicted examples. The configured thresholds are demonstration thresholds only; human review remains mandatory.
