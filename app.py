
import streamlit as st
import pandas as pd
import json
import re
from io import StringIO

st.set_page_config(
    page_title="Groww Investor Voice",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Groww Investor Voice")
st.caption("AI-powered customer discovery and thematic analysis")

st.warning(
    "Research integrity: The built-in R01–R10 records are "
    "illustrative practice data, not verified investor interviews "
    "or public customer feedback."
)

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

THEMES = {
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

def classify_rules(text):
    text = str(text).lower()
    result = []
    for theme, keywords in THEMES.items():
        if any(word in text for word in keywords):
            result.append(theme)
    return result or ["Unclassified"]

def safe_fallback(text):
    return {
        "themes": classify_rules(text),
        "sentiment": "Not assessed",
        "emotion": ["Not established"],
        "lifecycle_stage": "Unclear",
        "explicit_evidence": str(text),
        "root_cause_hypothesis": "Requires human review",
        "confidence": 0.0,
        "review_status": "Fallback - human review required"
    }

def classify_ai(client, text):
    prompt = f"""
You are a cautious qualitative research assistant.

Analyse this anonymised investor feedback item.

INPUT:
{text}

Return ONLY valid JSON with these fields:
{{
 "themes": ["one or more relevant themes"],
 "sentiment": "positive, negative, neutral, mixed, or unclear",
 "emotion": ["explicitly expressed emotions, or not stated"],
 "lifecycle_stage": "starting, early continuation, ongoing,
 pause consideration, discontinuation, or unclear",
 "explicit_evidence": "an exact short quotation from the input",
 "root_cause_hypothesis": "clearly marked hypothesis",
 "confidence": 0.0,
 "review_status": "pending human review"
}}

Rules:
- Use multiple themes where justified.
- Never invent facts.
- Never infer age, income, gender or sensitive characteristics.
- Distinguish explicit statements from hypotheses.
- Do not give investment advice.
- If evidence is insufficient, say unclear.
- Confidence is a model estimate, not a calibrated probability.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You perform careful qualitative research classification."
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    return json.loads(response.choices[0].message.content)

def validate_result(result, original):
    errors = []

    quote = str(result.get("explicit_evidence", ""))
    if not quote.strip() or quote.lower() not in original.lower():
        errors.append("Evidence quotation is not present in original text")

    themes = result.get("themes")
    if not isinstance(themes, list) or not themes:
        errors.append("Missing valid theme list")

    confidence = result.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        errors.append("Invalid confidence value")

    # Conservative check for potentially advisory output.
    hypothesis = str(result.get("root_cause_hypothesis", "")).lower()
    unsafe_phrases = [
        "buy this fund",
        "sell this fund",
        "invest in this stock",
        "switch to this fund",
        "time the market"
    ]

    if any(p in hypothesis for p in unsafe_phrases):
        errors.append("Potential investment advice")

    return errors

# Sidebar
st.sidebar.header("Research controls")

mode = st.sidebar.radio(
    "Analysis mode",
    ["Practice / Rule-based", "AI classification"]
)

st.sidebar.info(
    "AI mode sends the selected feedback text to the configured "
    "AI provider. Use only anonymised, non-sensitive text."
)

api_key = ""
if mode == "AI classification":
    api_key = st.sidebar.text_input(
        "OpenAI API key",
        type="password"
    )

uploaded = st.file_uploader(
    "Upload your feedback CSV (optional)",
    type=["csv"]
)

if uploaded:
    df = pd.read_csv(uploaded)
    st.success("CSV uploaded successfully")
else:
    df = SAMPLE.copy()
    st.info("Using the built-in illustrative practice dataset.")

st.subheader("1. Feedback dataset")
st.dataframe(df, use_container_width=True)

text_column = st.selectbox(
    "Select the column containing feedback text",
    df.columns,
    index=list(df.columns).index("confusion")
    if "confusion" in df.columns else 0
)

if st.button("Analyse feedback", type="primary"):
    results = []

    client = None

    if mode == "AI classification":
        if not api_key:
            st.error("Enter an API key to use AI mode.")
            st.stop()

        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
        except Exception as e:
            st.error(f"Could not initialise AI client: {e}")
            st.stop()

    progress = st.progress(0)

    for i, row in df.iterrows():
        original = str(row[text_column])

        if mode == "AI classification":
            try:
                result = classify_ai(client, original)
                errors = validate_result(result, original)

                if errors:
                    result = safe_fallback(original)
                    result["gate_errors"] = errors
                else:
                    result["review_status"] = "Pending human review"
                    result["gate_errors"] = []

            except Exception as e:
                result = safe_fallback(original)
                result["gate_errors"] = [str(e)]

        else:
            result = safe_fallback(original)
            result["review_status"] = "Rule-based demonstration"
            result["gate_errors"] = []

        result["record_id"] = str(row.get("ID", i))
        result["original_text"] = original
        results.append(result)

        progress.progress((len(results)) / len(df))

    st.session_state["results"] = pd.DataFrame(results)
    st.session_state["source_data"] = df.copy()

if "results" in st.session_state:
    results = st.session_state["results"]

    st.divider()
    st.subheader("2. Analysis overview")

    total = len(results)
    fallback = results["review_status"].astype(str).str.contains(
        "Fallback"
    ).sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Records analysed", total)
    c2.metric("Fallback records", int(fallback))
    c3.metric("Human review required", total)

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
        "review_status"
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

    st.subheader("5. Human validation")

    st.write(
        "AI classifications are provisional. A human researcher "
        "must review each record before it is used as a research finding."
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
