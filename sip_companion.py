"""Groww SIP Companion — educational, synthetic-data MVP (separate from discovery engine)."""
import re
import streamlit as st

st.set_page_config(page_title="SIP Companion | Prototype", page_icon="🌱", layout="wide")

STATES = {
    "Successful": ("Your example instalment was received.", "The payment succeeded. Unit allotment and NAV information may appear separately after processing."),
    "Pending": ("Your example instalment is being processed.", "A pending status is not confirmation of payment or unit allotment. Check your actual platform and bank records."),
    "Failed": ("Your example instalment did not complete.", "Check the transaction reason in your actual account. Possible causes include mandate or bank-processing issues; do not assume the cause."),
    "Cancelled": ("Your example future SIP instruction is cancelled.", "Stopping future instalments does not necessarily redeem units already held. Verify effective dates and any pending transactions with your provider."),
}

GLOSSARY = {
    "What is NAV?": "Net Asset Value (NAV) is the per-unit value of a mutual fund at a particular valuation point. NAV is not the same as your total portfolio value.",
    "What are units?": "Mutual fund units represent your holding. For a simplified illustration, units allotted = invested amount ÷ applicable NAV. Actual allotment depends on applicable rules and processing.",
    "Why does my portfolio value change?": "The market value of your holdings changes with the fund's NAV and the number of units you own. Market movement does not by itself tell you whether to continue or stop investing.",
    "What happens if an instalment fails?": "An unsuccessful instalment may require checking your mandate, bank balance or provider's transaction details. The precise reason and any charges must be confirmed with your bank and platform.",
    "Can I pause or cancel my SIP?": "SIP controls and effective dates depend on the platform and fund. Pausing or cancelling future contributions is different from redeeming existing holdings. Check the platform's confirmed status.",
}

def educational_answer(question):
    q = question.lower().strip()
    if not q:
        return "Choose a common question or enter a question about SIP terminology or transaction states."
    advice = ["should i invest", "which fund", "best fund", "buy", "sell", "guaranteed", "predict", "how much return", "continue my sip", "stop my sip", "recommend", "tax advice"]
    if any(x in q for x in advice):
        return "I can't recommend investments, predict returns, or decide whether you should continue, stop, or change a SIP. I can explain transaction terms and controls. Consider a qualified adviser for personalised decisions."
    if "nav" in q:
        return GLOSSARY["What is NAV?"]
    if "unit" in q:
        return GLOSSARY["What are units?"]
    if any(x in q for x in ["cancel", "pause", "stop"]):
        return GLOSSARY["Can I pause or cancel my SIP?"]
    if any(x in q for x in ["fail", "miss", "deduct", "pending", "payment", "status"]):
        return GLOSSARY["What happens if an instalment fails?"]
    if any(x in q for x in ["return", "portfolio", "market", "loss", "value"]):
        return GLOSSARY["Why does my portfolio value change?"]
    return "I don't have a grounded explanation for that question in this prototype. Try NAV, units, failed instalments, portfolio value, or SIP cancellation. For account-specific issues, consult your provider."

st.title("🌱 SIP Companion")
st.caption("First-time investor clarity • separate customer-facing MVP")
st.info("Independent educational prototype, not affiliated with Groww. All transaction data is fictional. No account connections, payment actions, investment recommendations or return predictions.")

tab1, tab2, tab3 = st.tabs(["🧾 SIP status explainer", "📘 NAV & units", "💬 SIP assistant"])

with tab1:
    st.subheader("Understand an instalment status")
    st.write("Explore how a status could be explained. This is **not your real SIP status**.")
    state = st.selectbox("Example transaction status", list(STATES))
    heading, detail = STATES[state]
    st.success(heading) if state == "Successful" else st.warning(heading)
    st.write(detail)
    st.caption("Always verify actual payment, mandate, allotment and cancellation details in your investment platform or bank.")

with tab2:
    st.subheader("NAV and units — illustrated")
    amount = st.number_input("Illustrative invested amount (₹)", min_value=100.0, max_value=1000000.0, value=2000.0, step=100.0)
    nav = st.number_input("Illustrative applicable NAV (₹/unit)", min_value=0.01, max_value=100000.0, value=50.0, step=1.0)
    units = amount / nav
    a, b, c = st.columns(3)
    a.metric("Example amount", f"₹{amount:,.2f}")
    b.metric("Example NAV", f"₹{nav:,.2f}")
    c.metric("Calculated units", f"{units:,.4f}")
    st.write("**Formula:** illustrative units = amount ÷ NAV. This is a simplified educational calculation, not a live allotment or portfolio valuation.")
    st.write("**Example:** A fall in NAV can change the displayed market value of existing units. It does not automatically indicate an error in deduction or allotment.")

with tab3:
    st.subheader("Ask a SIP question")
    choice = st.selectbox("Common question", ["Type my own question"] + list(GLOSSARY))
    question = st.text_input("Your question (no personal or account information)", value="" if choice == "Type my own question" else choice)
    if st.button("Explain", type="primary"):
        st.write(educational_answer(question))
        st.caption("Answer mode: approved, rule-routed educational knowledge base. No generative AI request was made.")
    with st.expander("Why is this called an MVP?"):
        st.write("It tests whether plain-language explanations reduce confusion around SIP status, NAV, units and controls. The separate Investor Voice discovery engine finds problems; this prototype demonstrates a possible investor-facing solution.")

st.divider()
st.caption("SIP Companion | Synthetic demo | Educational only | No investment advice")
