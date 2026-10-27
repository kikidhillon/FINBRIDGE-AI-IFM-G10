# FinBridge AI — Finance Tutor with Scenario Engine

**A runnable Streamlit learning dashboard for non-finance university students**  
GFB3043 / GEB3043 — International Financial Management — UTP FinBridge AI Innovation Challenge  
Course learning outcome **CLO3**: analyse relationships among interest rates, inflation rates and exchange rate movements.

> **All initial inputs and included scenario values are HYPOTHETICAL, educational assumptions, NOT actual or current market rates.** The app works offline without a third-party API. Optional AI narrative explanations require an independent API key and access to an external service. No real-world predictive performance or user testing is claimed.

## 1. Run the Streamlit dashboard

Use Python 3.10+ and an internet connection **when installing dependencies**:

```bash
cd FinBridge_AI_Streamlit
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS / Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Your browser should open at `http://localhost:8501`. The dashboard has five navigable views: **Learning Hub**, **Scenario Engine**, **AI Tutor**, **Knowledge Check**, and **About & Sources**. Change scenario presets and rates in the sidebar.

### Optional generative AI mode

The default tutor is **rule-based**, with scenario-specific responses. For optional generative tutoring, securely configure an environment variable *on your computer or hosting service*:

```bash
# macOS/Linux
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_MODEL="gpt-5.5"  # can change to a compatible model available to your account
streamlit run app.py
```

In Windows PowerShell: `$env:OPENAI_API_KEY="your-api-key-here"`.

Then open **AI Tutor**, switch on **Use generative AI**, and submit a question. Generative mode is disabled by default even when a key is set; if the API fails, the app falls back to deterministic coaching. **Do not store keys in source files or upload personal data.** Additional API charges may apply. The optional mode was not tested against a live API because no credentials were provided.

## 2. Demonstration pathway (3–4 minutes)

1. Open **Learning Hub** and explain the MYR/USD quote (higher quote means MYR depreciation). Point out three linked concepts and the USD 12,000 overseas tuition example.
2. Open **Scenario Engine** with **01 · Baseline semester**. Show PPP **4.544118 MYR/USD** versus IRP forward **4.457143 MYR/USD** and Fisher's Malaysian real rate **0.970874%**.
3. Choose **02 · Malaysia inflation shock** (MY inflation jumps from 3.0% to 6.5% only). PPP goes to **4.698529**, IRP stays **4.457143**. Show that Malaysia's Fisher-implied real rate drops to **−2.347418%**, given nominal rates fixed.
4. Choose **03 · Malaysia interest shock** (MY nominal rate goes from 4% to 7%, inflation unchanged). IRP rises to **4.585714**, while PPP stays **4.544118**. Explain *why higher MYR/USD means forward MYR depreciation* in this spot convention—do not say a rate hike guarantees spot depreciation/appreciation.
5. Choose a **2.0 percentage-point** Malaysian inflation sensitivity; view chart, comparison, independent verification and JSON/CSV export.
6. Ask **AI Tutor** about PPP versus IRP. Then use **Knowledge Check** and show corrective feedback.
7. Open **About & Sources** for target audience, marketability, limitations and citations.

### Verified example results (one year, spot 4.50 MYR/USD, USD expense 12,000)

| Case (all hypothetical) | MY i | US i | MY inflation | US inflation | PPP spot model (MYR/USD) | IRP forward (MYR/USD) | PPP MYR expense |
|---|---:|---:|---:|---:|---:|---:|---:|
| 01 Baseline | 4.0% | 5.0% | 3.0% | 2.0% | 4.544118 | 4.457143 | RM 54,529.41 |
| 02 MY inflation shock | 4.0% | 5.0% | 6.5% | 2.0% | 4.698529 | 4.457143 | RM 56,382.35 |
| 03 MY interest shock | 7.0% | 5.0% | 3.0% | 2.0% | 4.544118 | 4.585714 | RM 54,529.41 |

## 3. Financial model and direction of effects

All spot/forward FX quotes are **MYR per 1 USD**. Domestic (price) currency = MYR; foreign (base) currency = USD. Annual effective rates are provided as decimals in formulas; T is years:

- **Covered IRP / CIP:** `F(MYR/USD) = S * ((1+i_MY)/(1+i_US))^T`, theoretical forward under no-arbitrage conditions. If i_MY rises with other inputs fixed, F rises; MYR's *forward value* depreciates relative to USD. This is **not a future spot forecast**.
- **Relative PPP:** `E[S_T]_PPP = S * ((1+pi_MY)/(1+pi_US))^T`. If expected pi_MY rises, PPP-implied MYR/USD rises, i.e. MYR depreciates. PPP need not hold over a one-year horizon in actual markets.
- **Exact Fisher:** `1+i = (1+r)(1+pi_expected)`, equivalently `r = (1+i)/(1+pi_expected)-1`. This is applied separately to MYR and USD, with *expected* inflation; the app never asserts real rates are automatically equal.
- **International Fisher Effect / uncovered parity illustration:** `E[S_T]_IFE = S*((1+i_MY)/(1+i_US))^T`. This numeric expression matches CIP's forward pricing **in the simplified model** but the *economic object* is different: IFE/UIP posits an **expected future spot** under additional equilibrium and risk assumptions, while covered IRP calculates a **forward contract price**. No empirically guaranteed forecast is implied.
- **Budget illustration:** `MYR cost = USD expense × S_T` for scenario spot estimates, or × theoretical F for a hedged-equivalent forward benchmark. Actual bank forwards involve spreads and contract availability.

Rates are held constant and compounded over the selected 1–5 year horizon. For genuine pricing, rates must be appropriate maturity-matched zero/discount rates rather than assumed short-term policy rates. Market frictions, cross-currency basis, risk premiums, expectations, CPI baskets, fees and politics can invalidate forecasts. The app intentionally uses synthetic values and has **no live FX, CPI or interest-rate feed**.

## 4. Validation & integrity

```bash
pip install pytest
pytest -q
```

The finance engine is separate from the visual interface (`finance_engine.py`) and from the narrative tutor (`tutor.py`). Automated tests cover three sample cases, inverse-direction interpretation, unexpected rates, model separation, boundary cases, self-assessment and tutor outputs. On each calculation, a **separate Decimal-based reference** checks the IRP and PPP arithmetic, exact Fisher relationships and parity-arbitrage identity. The Scenario Engine exposes the validation results, and its JSON/CSV exports preserve units and illustrative status.

These are **calculation** checks, not evidence that theories predict market behavior accurately. Users must check AI text against the locked numerical fact panel. Please review `docs/TEST_EVIDENCE.md`, `docs/AI_USE_DISCLOSURE.md` and `docs/REPORT.md`.

## 5. Remaining group-specific submission tasks

The project includes a **professionally formatted A3 landscape poster draft** in `docs/FinBridge_AI_A3_Poster_DRAFT.pdf` and a `docs/VIDEO_PLAN.md` 10-minute speaking storyboard. The draft poster contains **visible placeholders**, because the team members' names/IDs and an actual Streamlit screenshot were not provided. You MUST add a genuine app screenshot and member details before submission. The group must actually record the MP4 and keep evidence of their individual contributions; these cannot be manufactured from code alone.

Brief deadline: **16 November 2026, before 11:59 PM Malaysia time**. Only the group leader submits one poster PDF and one 10-minute MP4 (or accessible link if upload limits require) via ULearn. Every member retains the final report, poster, video and calculation evidence. No actual group number or identities have been assumed.

## 6. File structure

```text
FinBridge_AI_Streamlit/
├── app.py                    # 5-page interactive Streamlit dashboard
├── finance_engine.py         # pure correct model & independent checks
├── tutor.py                  # transparent offline tutor & optional AI integration
├── learning_content.py       # quiz with answer key and explanations
├── requirements.txt
├── .streamlit/config.toml
├── tests/test_finance_engine.py
├── docs/REPORT.md
├── docs/RUBRIC_MAPPING.md
├── docs/TEST_EVIDENCE.md
├── docs/VIDEO_PLAN.md
├── docs/AI_USE_DISCLOSURE.md
└── docs/FinBridge_AI_A3_Poster_DRAFT.pdf
```

## Core references

1. CFA Institute. (2026). *Currency Exchange Rates: Understanding Equilibrium Value.* https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/currency-exchange-rates-understanding-equilibrium-value
2. Rogerson, M., & CME Group. (2024). *Covered Interest Parity, Implied Forward FX Swaps, Cross-Currency Basis...* https://www.cmegroup.com/articles/whitepapers/covered-interest-parity-implied-forward-foreign-exchange-swaps-cross-currency-basis-and-cme-estr-futures.html
3. Callen, T. (2018). *Purchasing Power Parity: Weights Matter.* IMF. https://www.imf.org/en/publications/fandd/issues/series/back-to-basics/purchasing-power-parity-ppp
4. Federal Reserve Bank of St. Louis. (2023). *Adjusting for Inflation.* https://www.stlouisfed.org/publications/page-one-economics/2023/01/03/adjusting-for-inflation
5. CFA Institute. (2021). *Investment Governance for Climate Change* (International Fisher Effect discussion). https://www.cfainstitute.org/sites/default/files/-/media/documents/book/rf-publication/2021/igcc-summary-edition-2021.pdf
6. Universiti Teknologi PETRONAS, Department of Management. (2026). *FinBridge AI Innovation Challenge*, course assignment brief (user-provided).

To regenerate the A3 draft after editing `generate_poster.py`, install `reportlab` (`pip install reportlab`) and run `python generate_poster.py`. The current draft PDF is already included, so this is not needed for the Streamlit app.
