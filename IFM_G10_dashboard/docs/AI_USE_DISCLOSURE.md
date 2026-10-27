# Responsible AI / digital tool disclosure

This project was produced with substantial assistance from OpenAI ChatGPT (GPT-6) for software design, Streamlit/Python source code, UI copy, explanation drafting, finance-model review, automated unit-test design, report/poster preparation and citation discovery. The **group must review and independently verify** all supplied text, references, calculations and outputs before academic submission and follow the lecturer's policy for acknowledging AI use.

**What is and is not AI:**

- The default **offline tutor** (`tutor.py`) uses a deterministic rule/keyword system tailored to current user inputs. This is *digital feedback*, not a generative language model.
- An actual **generative AI** narrative explanation is possible only if the group configures `OPENAI_API_KEY` and manually enables the optional switch. The `openai` SDK's Responses API is used. This optional connection was not live-tested without credentials.
- **All financial numbers** in the charts, cards, budget tables, downloads and independently checked panels are produced by the pure Python finance module, not by generative AI.
- Prompts tell the generative tutor to rely on verified numbers and state theoretical limitations, but **its prose is not automatically fact-checked line by line**. Users should cross-check any claim against the model, formulas and cited institutional theory.
- Hypothetical interest, inflation, FX quotes, USD amounts and examples are not live facts. No user analytics, learning gain, sample sizes, endorsements or external user tests are fabricated.

**Privacy:** No account/ID required; no personal or banking data is intentionally stored by the app. In optional generative AI mode, the user's free-text question, chosen learning goal and current synthetic scenario are transmitted to the external AI provider for processing. Users are explicitly warned against entering any personal or sensitive data. The group must evaluate provider privacy terms and obtain consent before using that mode in live classroom research.

**Sources:** CFA Institute (2026, 2021), CME Group (2024), IMF (2018), Federal Reserve Bank of St. Louis (2023), and UTP (2026 project brief). Full URLs in README and About & Sources.
