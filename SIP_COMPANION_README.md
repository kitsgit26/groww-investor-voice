# SIP Companion — separate investor-facing MVP

This is a **separate** Streamlit application from the `app.py` AI Discovery Agent.

## Run
```bash
pip install streamlit
streamlit run sip_companion.py
```

## Deploy separately on Streamlit Community Cloud
1. Create a new Streamlit app connected to this GitHub repository.
2. Select the merged `main` branch and entrypoint **`sip_companion.py`** (not `app.py`).
3. Deploy and record the new URL. Do not replace the existing discovery engine deployment.

## Scope
- Synthetic SIP transaction-status explanations.
- NAV/unit calculation with fictional amounts.
- Safe educational SIP Q&A routed to a curated answer bank.
- Refusal of personalised investment recommendations or predictions.
- No user accounts, brokerage connections, transaction actions, or real account data.

**AI qualification:** This MVP is currently **deterministic / knowledge-base powered**, not generative-AI-native. Do not claim an LLM is used here. The separate AI Discovery Agent supports optional GPT-4o-mini classification.

## Suggested usability test
Ask at least 3 first-time SIP investors to perform: interpret a pending deduction; calculate example units; explain what cancelling future instalments does. Record task success, confusion, time, and any unsafe or inaccurate explanations. No tests of this separate MVP are claimed yet.
