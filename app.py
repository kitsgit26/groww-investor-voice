
import streamlit as st
import pandas as pd
import json
import re
from openai import OpenAI

# -----------------------------------------
# APPLICATION CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="Groww Investor Voice",
    page_icon="📊",
    layout="wide"
)

MODEL = "gpt-4o-mini"

THEMES = [
    "Performance uncertainty",
    "Operational understanding",
    "Investment knowledge",
    "Financial flexibility",
    "External guidance seeking"
]

SENTIMENTS = [
    "positive", "negative", "neutral", "mixed", "unclear"
]

LIFECYCLE_STAGES = [
    "starting",
    "early continuation",
    "ongoing",
    "pause consideration",
    "discontinuation",
    "unclear"
]

SAMPLE = pd.DataFrame([
    ["R01", "Negative portfolio returns", "Google search", "Yes", "Daily"],
    ["R02", "Units not visible", "Asked friend", "No", "After deduction"],
    ["R03", "NAV confusion", "YouTube", "No", "Weekly"],
    ["R04", "Market fluctuations", "Reviewed portfolio", "No", "Monthly"],
    ["R05", "Other funds showing better returns", "Compared funds online", "Yes", "Daily"],
    ["R06", "Automatic deduction concerns", "App support", "Yes", "After notifications"],
    ["R07", "Unexpected family expenses", "Reviewed monthly budget", "Yes", "Monthly"],
    ["R08", "Confusion about fund categories", "Searched online", "No", "Tax season"],
    ["R09", "Uncertainty about performance", "Online community", "Yes", "Weekly"],
    ["R10", "Frequent market declines", "Checked portfolio", "Yes", "Market falls"],
], columns=[
    "ID", "confusion", "workaround",
    "considered_stopping", "checking"
])

RULES = {
    "Performance uncertainty": [
        "negative", "market fluctuation", "market decline",
        "performance", "returns"
    ],
    "Operational understanding": [
        "nav", "units", "deduction", "transaction",
        "payment", "status"
    ],
    "Investment knowledge": [
        "fund categor", "comparison", "better returns",
        "investment knowledge"
    ],
    "Financial flexibility": [
        "family expenses", "monthly expenses",
        "budget", "affordability", "cash flow"
    ],
    "External guidance seeking": [
        "google", "youtube", "friend",
        "online community", "searched"
    ]
}

# -----------------------------------------
# CLASSIFICATION AND FALLBACK
# -----------------------------------------

def classify_rules(text):
    text = str(text).lower()
    found = []

    for theme, keywords in RULES.items():
        if any(word in text for word in keywords):
            found.append(theme)

    return found or ["Unclassified"]


def safe_fallback(text, reason="AI validation failed"):
    return {
        "themes": classify_rules(text),
        "sentiment": "unclear",
        "emotion": ["Not established"],
        "lifecycle_stage": "unclear",
        "explicit_evidence": str(text),
        "root_cause_hypothesis": "Requires human review",
        "confidence": 0.0,
        "review_status": "Fallback - human review required",
        "gate_status": "FAIL - fallback activated",
        "gate_errors": [reason]
    }


# -----------------------------------------
# AI CLASSIFICATION
# -----------------------------------------

def classify_ai(client, text):

    system_prompt = """
You are a cautious qualitative research analyst.

Your job is to classify anonymised investor feedback.
You are NOT an investment adviser.

Use only these themes:
- Performance uncertainty
- Operational understanding
- Investment knowledge
- Financial flexibility
- External guidance seeking

Return a JSON object with:

{
  "themes": [],
  "sentiment": "positive/negative/neutral/mixed/unclear",
  "emotion": [],
  "lifecycle_stage": "starting/early continuation/ongoing/pause consideration/discontinuation/unclear",
  "explicit_evidence": "",
  "root_cause_hypothesis": "",
  "confidence": 0.0
}

Rules:

1. Use multiple themes only when supported.
2. Evidence must be copied exactly from the input.
3. Never invent user experiences or motivations.
4. Separate explicit evidence from hypotheses.
5. Never infer age, income, gender or sensitive characteristics.
6. Do not recommend mutual funds, stocks or portfolio changes.
7. Do not predict investment returns.
8. Use unclear when evidence is insufficient.
9. Confidence is an uncalibrated model estimate.
10. Do not treat an AI hypothesis as a verified finding.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": "Classify this feedback:\n" + str(text)
            }
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("AI returned an empty response")

    return json.loads(content)


# -----------------------------------------
# OUTPUT VALIDATION GATE
# -----------------------------------------

def validate_result(result, original):

    errors = []

    required_fields = [
        "themes",
        "sentiment",
        "emotion",
        "lifecycle_stage",
        "explicit_evidence",
        "root_cause_hypothesis",
        "confidence"
    ]

    for field in required_fields:
        if field not in result:
            errors.append("Missing field: " + field)

    if errors:
        return errors

    if not isinstance(result["themes"], list):
        errors.append("Themes must be a list")
    else:
        if not result["themes"]:
            errors.append("No themes provided")

        unknown = [
            t for t in result["themes"]
            if t not in THEMES
        ]

        if unknown:
            errors.append("Unknown themes returned")

    if result["sentiment"] not in SENTIMENTS:
        errors.append("Invalid sentiment")

    if not isinstance(result["emotion"], list):
        errors.append("Emotion must be a list")

    if result["lifecycle_stage"] not in LIFECYCLE_STAGES:
        errors.append("Invalid lifecycle stage")

    quote = result["explicit_evidence"]

    if not isinstance(quote, str) or not quote.strip():
        errors.append("Missing evidence quotation")
    elif quote.lower() not in str(original).lower():
        errors.append("Evidence quotation not grounded in original text")

    hypothesis = result["root_cause_hypothesis"]

    if not isinstance(hypothesis, str):
        errors.append("Invalid root cause hypothesis")

    confidence = result["confidence"]

    if (
        not isinstance(confidence, (int, float))
        or isinstance(confidence, bool)
        or not 0 <= confidence <= 1
    ):
        errors.append("Invalid confidence value")

    # Conservative safety screening
    all_text = json.dumps(result).lower()

    unsafe_phrases = [
        "buy this fund",
        "sell this fund",
        "invest in this stock",
        "switch to this fund",
        "time the market",
        "guaranteed returns",
        "you should invest"
    ]

    if any(p in all_text for p in unsafe_phrases):
        errors.append("Potential investment advice detected")

    return errors


# -----------------------------------------
# API CLIENT
# -----------------------------------------

def get_client():

    try:
        api_key = st.secrets["OPENAI_API_KEY"]

        if not api_key:
            return None

        return OpenAI(api_key=api_key)

    except Exception:
        return None


# -----------------------------------------
# INTERFACE
# -----------------------------------------

st.title("📊 Groww Investor Voice")

st.caption(
    "AI-powered customer discovery and thematic analysis"
)

st.warning(
    "Research integrity: Built-in R01-R10 records are "
    "illustrative practice data, not verified investor interviews "
    "or public customer feedback."
)

st.info(
    "Independent academic prototype. Not affiliated with Groww. "
    "This tool does not provide investment advice."
)

st.sidebar.header("Research controls")

mode = st.sidebar.radio(
    "Analysis mode",
    ["Practice / Rule-based", "AI classification"]
)

if mode == "AI classification":
    st.sidebar.success(
        "API credentials are loaded securely from Streamlit Secrets."
    )

uploaded = st.file_uploader(
    "Upload your feedback CSV (optional)",
    type=["csv"]
)

try:
    if uploaded:
        df = pd.read_csv(uploaded)
        st.success("CSV uploaded successfully.")
    else:
        df = SAMPLE.copy()
        st.info("Using illustrative practice dataset.")

except Exception as e:
    st.error("Could not read CSV: " + str(e))
    st.stop()

if df.empty:
    st.error("The uploaded dataset is empty.")
    st.stop()

st.subheader("1. Feedback dataset")

st.dataframe(df, use_container_width=True)

text_column = st.selectbox(
    "Select the column containing feedback text",
    df.columns,
    index=(
        list(df.columns).index("confusion")
        if "confusion" in df.columns else 0
    )
)

if st.button("Analyse feedback", type="primary"):

    client = None

    if mode == "AI classification":

        client = get_client()

        if client is None:
            st.error(
                "OpenAI API key not found. Check Streamlit "
                "Community Cloud → App settings → Secrets."
            )
            st.stop()

    results = []

    progress = st.progress(0)

    for i, row in df.iterrows():

        original = str(row[text_column])

        if not original.strip() or original.lower() == "nan":
            result = safe_fallback(
                original,
                "Empty feedback text"
            )

        elif mode == "AI classification":

            try:
                ai_result = classify_ai(client, original)

                errors = validate_result(ai_result, original)

                if errors:
                    result = safe_fallback(
                        original,
                        "; ".join(errors)
                    )

                else:
                    result = ai_result

                    result["review_status"] = (
                        "Pending human review"
                    )

                    result["gate_status"] = (
                        "PASS - output validation checks passed"
                    )

                    result["gate_errors"] = []

            except Exception:
                result = safe_fallback(
                    original,
                    "AI request or response processing failed"
                )

        else:

            result = safe_fallback(
                original,
                "Rule-based demonstration"
            )

            result["review_status"] = (
                "Rule-based demonstration"
            )

            result["gate_status"] = (
                "Not evaluated as AI"
            )

            result["gate_errors"] = []

        result["record_id"] = str(row.get("ID", i))
        result["original_text"] = original

        results.append(result)

        progress.progress(
            len(results) / len(df)
        )

    st.session_state["results"] = pd.DataFrame(results)
    st.session_state["source_data"] = df.copy()
    st.session_state["analysis_mode"] = mode


# -----------------------------------------
# RESULTS
# -----------------------------------------

if "results" in st.session_state:

    results = st.session_state["results"]

    st.divider()
    st.subheader("2. Analysis overview")

    total = len(results)

    fallback_count = results[
        "review_status"
    ].astype(str).str.contains(
        "Fallback"
    ).sum()

    passed = results[
        "gate_status"
    ].astype(str).str.startswith("PASS").sum()

    c1, c2, c3 = st.columns(3)

    c1.metric("Records analysed", total)
    c2.metric("Validated AI outputs", int(passed))
    c3.metric("Fallback records", int(fallback_count))

    if st.session_state.get("analysis_mode") == "AI classification":

        if fallback_count == 0:
            st.success(
                "All individual outputs passed the configured "
                "structural, evidence and safety screening checks. "
                "Human review is still required."
            )
        else:
            st.warning(
                "Some AI outputs failed validation and were "
                "replaced with rule-based fallback results."
            )

    else:
        st.info(
            "Practice mode uses rule-based classification. "
            "No AI quality claim is made."
        )

    st.subheader("3. Classification results")

    display_columns = [
        "record_id",
        "themes",
        "sentiment",
        "emotion",
        "lifecycle_stage",
        "explicit_evidence",
        "root_cause_hypothesis",
        "confidence",
        "review_status",
        "gate_status"
    ]

    st.dataframe(
        results[display_columns],
        use_container_width=True
    )

    st.subheader("4. Theme frequency")

    exploded = results.explode("themes")

    counts = (
        exploded.groupby("themes")["record_id"]
        .nunique()
        .sort_values(ascending=False)
    )

    if not counts.empty:
        st.bar_chart(counts)

    st.caption(
        "Theme counts can overlap because classification is multi-label."
    )

    st.subheader("5. Validation errors")

    for _, row in results.iterrows():

        errors = row.get("gate_errors", [])

        if isinstance(errors, list) and errors:
            with st.expander(
                "Record " + str(row["record_id"])
            ):
                for error in errors:
                    st.write("- " + str(error))

    st.subheader("6. Human validation")

    st.write(
        "All classifications remain provisional. "
        "Review original feedback before using any output "
        "as a research finding."
    )

    st.download_button(
        "Download classification results",
        data=results.to_csv(index=False),
        file_name="investor_voice_analysis.csv",
        mime="text/csv"
    )

    st.download_button(
        "Download original dataset",
        data=st.session_state["source_data"].to_csv(index=False),
        file_name="investor_voice_source_data.csv",
        mime="text/csv"
    )

st.divider()

st.caption(
    "Groww Investor Voice | Independent academic prototype | "
    "Not affiliated with Groww | Not investment advice"
)
