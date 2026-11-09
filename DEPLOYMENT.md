# Deploy Groww Investor Voice

This repository contains an independent academic prototype. It is not affiliated with Groww and does not provide investment advice.

## Deploy with Streamlit Community Cloud

1. Push or merge the project branch into the repository branch you want to deploy.
2. Sign in to Streamlit Community Cloud using the GitHub account that can access this repository.
3. Choose **Create app**, select `kitsgit26/groww-investor-voice`, select the deployment branch, and set the main file path to `app.py`.
4. Deploy the app. The practice/rule-based mode does not require an API key.
5. If you want to enable AI classification, open the app's **Settings → Secrets** and add:

```toml
OPENAI_API_KEY = "your_api_key"
```

6. Save the secret and reboot the app. Never commit API keys, passwords, customer data, or a `.streamlit/secrets.toml` file to GitHub.
7. Test the deployed app using the built-in illustrative records first. Confirm the rule-based mode, upload flow, downloads, and AI fallback behaviour before sharing the URL.

## Before sharing

- Clearly disclose that R01–R10 are illustrative practice records.
- Do not upload identifiable or sensitive financial information.
- AI mode sends the selected feedback text to the OpenAI API. Obtain appropriate permission and anonymise data before use.
- Treat every AI result as provisional; review the original feedback and evidence quotation.
- The configured output checks are not a comprehensive safety, factuality, or production-readiness evaluation.
- Do not use the prototype to recommend funds, predict returns, or tell a person whether to start, stop, or modify an investment.

## Deployment verification checklist

- [ ] App opens without errors.
- [ ] Practice mode runs without an API key.
- [ ] Empty feedback produces a visible fallback.
- [ ] AI mode remains unavailable when the secret is missing.
- [ ] AI mode requires the privacy/authorisation confirmation.
- [ ] Invalid AI output triggers fallback.
- [ ] Results and source CSV downloads work.
- [ ] Public page includes the independent-prototype and no-investment-advice disclaimers.

Deployment is not complete until the live URL has been opened and these checks have been performed.
