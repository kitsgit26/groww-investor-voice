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

## Optional grounded AI explanation mode

The approved-text mode continues to work without credentials. For optional LLM-powered rephrasing, open the **SIP Companion deployment's** Streamlit settings → Secrets and add:

```toml
OPENAI_API_KEY = "your_api_key"
```

Never commit the secret. The user must explicitly consent before submitting a non-sensitive question to OpenAI. The AI is instructed to rephrase only the approved educational answer; each result is checked for schema, source quote, word count, numerical inventions and some investment-advice phrases. Invalid responses or API errors fall back to approved text. These checks are limited and **do not prove factual accuracy or financial safety**.

For local tests:

```bash
python -m unittest test_sip_companion_ai.py
```

Offline unit tests use **mock AI responses** and must not be called real-model accuracy evaluation. Actual end-to-end model evaluation and usability tests must be run separately before making quality claims.

## Suggested usability test
Ask at least 3 first-time SIP investors to perform: interpret a pending deduction; calculate example units; explain what cancelling future instalments does. Record task success, confusion, time, and any unsafe or inaccurate explanations. No tests of this separate MVP are claimed yet.
