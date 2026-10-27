# PROJECT REPORT — FinBridge AI: Finance Tutor with Scenario Engine

**Project/course:** GFB3043 / GEB3043, UTP September 2026 semester  
**Group number and team members:** [GROUP XX; COMPLETE FROM ACTUAL MEMBERSHIP]  
**Status:** Functional source code, documented model and automated tests. Streamlit live browser QA and actual classroom/user testing remain to be done in the group's own environment.

## 1. Executive overview and problem statement

Non-finance university students encounter international finance when considering overseas study costs, travel budgets, or coursework. They often struggle to (i) interpret the currency quote MYR/USD, (ii) connect inflation to currency depreciation, (iii) distinguish spot rate expectations from contracted forward rates, and (iv) understand why higher nominal interest rates do not give simple short-term FX predictions. The project solves a **specific learning problem**: explaining and testing these interrelated variables with transparent arithmetic and immediate feedback.

The proposed solution is FinBridge AI: a five-section Streamlit web application for non-finance Malaysian university students. Users select three premade, synthetic scenarios; directly edit spot, Malaysian and US interest and inflation, years and USD cost; inspect formulas and budget consequences; run one-input sensitivity; get contextual tutor feedback; and take a misconception-based quiz. An optional OpenAI-powered *narrative* layer is configurable, but does not replace the deterministic numerical engine.

## 2. Objectives and course alignment

1. Explain the effect of Malaysian and US **inflation** differences on PPP-modeled MYR/USD movements.
2. Compute the theoretical **covered IRP forward** from matching-term **nominal interest rates**, distinct from an actual spot FX forecast.
3. Derive **exact Fisher real returns** and discuss the conditional linkage of nominal interest and expected inflation.
4. Illustrate the **International Fisher Effect / UIP** hypothesis and distinguish it clearly from the forward contract.
5. Compare ≥2 numerical scenarios (supplied baseline plus inflation and interest shock), with sensitivity and precise MYR/USD direction interpretation.
6. Use independent arithmetic checks, source citations, feedback and responsible AI to improve learning reliability.

This realizes CLO3: **analyse the relationship among interest rate, inflation rate and foreign exchange movement**.

## 3. Workflow and interface

**Sidebar:** choose baseline/inflation/interest preset; modify all rates and spot; set horizon from one to five years and USD expense. Hypothetical label shown persistently. **Learning Hub:** concept chain, 3 metrics, guided USD tuition example, numerical scenario comparison. **Scenario Engine:** chart, exact formula/substitution, sensitivity slider (±2.5 percentage points), comparative budgets, validation checks and machine-readable downloads. **AI Tutor:** goal-specific offline feedback, optional API-based generative narrative only when a key is configured, and side-by-side verified numbers. **Knowledge Check:** six independently keyed questions, wrong-answer remediation and scenario-dependent direction challenge. **About & Sources:** marketability, limits, integrity and references.

No user login, external database or private financial-data collection. Inputs held only in Streamlit session state. Optional generative API sends the synthetic current inputs, question and learner goal to the AI provider when enabled; users are instructed not to input personal information.

## 4. Finance methods and theoretical assumptions

The full quote is MYR per USD throughout. Domestic/price currency MYR, foreign/base USD. For a quote that rises, MYR **depreciates** (more MYR required for a USD). Annual effective rates convert from percentage inputs (4% → 0.04). Horizon T is a whole number of years.

**Covered IRP** — `F = S * ((1+i_MY)/(1+i_US))^T`. Derive by equality of MYR and FX-forward-covered USD investments. Example: spot 4.50, Malaysian rate 4%, US rate 5%, T=1 produces **4.457142857 MYR/USD**. Here MYR trades at an IRP-implied forward premium relative to USD (MYR/USD falls), all else constant. It is not a future spot price.

**Relative PPP** — `E[S_T]_PPP = S * ((1+pi_MY)/(1+pi_US))^T`. Example: 4.50 × 1.03/1.02 = **4.544117647 MYR/USD**. Malaysia's higher inflation raises MYR/USD: implied **0.980392% MYR depreciation**. This theory is stronger as a long-horizon equilibrium benchmark than as a short-term forecast.

**Exact Fisher** — `1+i=(1+r)(1+pi_expected)`, so `r=(1+i)/(1+pi_expected)-1`. Baseline Malaysian implied real rate **0.970874%**; US **2.941176%**. The inequality is allowed by the input assumptions; **equal real rates are not silently imposed**.

**IFE / UIP** — under additional expectations/risk assumptions, hypothesized `E[S_T]_IFE = S*((1+i_MY)/(1+i_US))^T`. It is **numerically identical** to an idealized covered forward but conceptually different. Observed forward rates are not guaranteed unbiased future-spot predictors. In reality deviations and risk premiums matter.

**Budget example** — USD 12,000 due in one year. Today at spot: MYR 54,000. PPP illustration: MYR 54,529.41. Implied forward hedge benchmark: MYR 53,485.71 (before spread), which cannot be executed absent an actual forward contract and financial institution. Comparisons are educational, not financial advice.

**Risks:** perfect or near no-arbitrage assumed for IRP, frictionless investment, comparable terms, no fees/taxes/cross-currency basis; PPP requires international price adjustment and expected inflation; IFE relies on restrictive risk/expectations assumptions; no realized inflation or real-world market data supplied. Constant annual inputs for all years, no term-structure or stochastic modelling. Source trail is in README and the app.

## 5. Numerical scenario and sensitivity results

All inputs fictional: S0=4.50 MYR/USD, US nominal i=5%, US inflation pi=2%, horizon 1 year, USD cost 12,000.

| Scenario | MY i | MY pi | IRP F MYR/USD | PPP future MYR/USD | MY exact Fisher r | PPP tuition MYR |
|---|---:|---:|---:|---:|---:|---:|
| 01 baseline | 4.0% | 3.0% | 4.457143 | 4.544118 | 0.970874% | 54,529.41 |
| 02 Malaysia inflation shock | 4.0% | 6.5% | 4.457143 | 4.698529 | −2.347418% | 56,382.35 |
| 03 Malaysia interest shock | 7.0% | 3.0% | 4.585714 | 4.544118 | 3.883495% | 54,529.41 |

**Interpretation:** Holding nominal rates fixed, Malaysian inflation rises from 3% to 6.5%, increasing modeled MYR/USD by **0.154412** and PPP tuition by **MYR 1,852.94**; the IRP forward is unchanged because only inflation changed. Holding inflation fixed and raising MYR nominal i from 4% to 7% raises the IRP-implied forward by **0.128571** while PPP is unchanged. The independent variable comparisons *visibly link* the three concepts without pretending the model forecasts tomorrow's real spot.

The interactive sensitivity chart also sweeps any one of four interest/inflation variables over ±2.5 percentage points and reports actual difference in rate and overseas cost. Every scenario can be saved as JSON/CSV with units and verification status.

## 6. Implementation design and testing

**Architecture:** Streamlit (`app.py`) → pure dataclass-based finance module (`finance_engine.py`) → interactive analytics and display; separate tutor (`tutor.py`), learning question bank (`learning_content.py`) and pytest suite (`tests/test_finance_engine.py`). Calculations are not delegated to a chatbot. Independent `Decimal` calculations verify both model rates and Fisher real yields to tolerances of 1e-9 and 1e-12; a second covered-rate identity verifies no-arbitrage arithmetic. Results can be inspected in-app.

**Completed execution evidence:** 18 automated unit/parameterized tests passed in the build environment, `python -m py_compile` succeeded. **Limitation:** Streamlit is not installed in the build environment and dependency downloading was blocked by network resolution, so interactive GUI execution and actual screenshot capture were **not** verified here. These must be performed before group submission (see `TEST_EVIDENCE.md`). A working source-level prototype is supplied, but this environment could not confirm browser operation.

**Suggested usability tests (not performed):** ask 5–10 eligible students (with consent) to interpret MYR/USD, explain PPP vs IRP, and answer quiz before and after tool use. Measure misunderstanding reduction; do not report any results until collected. Test Windows/macOS and mobile layouts, keyboard controls, PDF poster readability and downloaded scenario integrity.

## 7. Marketability and feasibility

**Primary segment:** university instructors, non-finance students and peer tutors in introductory international finance. **Competitors/substitutes:** textbooks, spreadsheets, formula sites, online articles and generic LLM interfaces. **Differentiation:** a Malaysia-relevant MYR/USD quotation, three interconnected models, coherent worked examples, offline functionality, personalized misconception feedback, math checks and exportable evidence rather than unverifiable prose.

**Adoption pathway:** free classroom pilot delivered through an instructor link → gather structured anonymous feedback → iterate explanations for common misunderstandings → optionally campus-host with institution branding → consider Moodle/ULearn integration or multicurrency extensions. **Costs:** small hosted Streamlit instance and educator time; optional model API usage incurs variable costs; no actual revenue or demand metric claimed. **Improvements:** live official BNM/FRED data with timestamps, accessibility testing, bid-ask/forward bid-ask simulations, hedging extension, multilingual Malay/English tutoring and pre/post competency tracking subject to consent.

## 8. Responsible AI and group contribution

Only synthesized teaching figures used. Offline tutor uses rule-based intent/keyword matching; it is not generative AI. The optional service can generate explanatory prose, but the local verified panel stays the sole source of numerical truth. AI explanations might still contain inaccuracies; it is important to disclose that **sentence-level AI validation is not automated**. See `AI_USE_DISCLOSURE.md` for disclosure and handling of user input.

Group contributions are unfilled pending actual membership. **Complete the table without inventing names or responsibilities**:

| Student full name / ID / programme | Real contribution | Evidence/commit |
|---|---|---|
| [Member 1] | [Real tasks] | [File/git/video reference] |
| [Member 2] | [Real tasks] | [File/git/video reference] |
| [Member 3] | [Real tasks] | [File/git/video reference] |
| [Member 4] | [Real tasks] | [File/git/video reference] |
| [Member 5] | [Real tasks] | [File/git/video reference] |

## 9. Submission and institutional sources

**Course brief:** UTP Department of Management, *FinBridge AI Innovation Challenge* (September 2026 semester; provided PDF). Required output A: one A3 landscape academic poster PDF; output B: a recorded ≈10-minute video with each member speaking/demonstrating. Leader submits before **16 Nov 2026, 11:59 PM MYT**. Retain poster, report, video, mathematical evidence and group attribution. External sources are enumerated with full URLs and dates in the README and About & Sources view. The generated poster draft still requires authentic member data and live screenshot before submission.
