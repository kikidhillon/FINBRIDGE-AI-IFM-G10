# FinBridge AI — Exact requirement-to-evidence map

**This maps the *implemented application* and supplied preparatory artifacts to the UTP course brief. It does not claim the unrecorded video or screenshot placeholders are final.**

| UTP brief requirement / 100-mark rubric | Concrete evidence in deliverable | Verification/remaining work |
|---|---|---|
| **35** Analysis & financial accuracy: interest/inflation/FX, calculations, directions, assumptions, limitations | `finance_engine.py`: IRP, PPP, Fisher and IFE formulas; `app.py` Scenario Engine/CLO3 diagram and interpretive text; `docs/REPORT.md` section 4–5 | Independent Decimal + parity checks; `pytest` test baseline, MY inflation and interest shocks. Check live UI |
| **15** Real-world problem & relevance | Non-finance MY university student, USD tuition expense, FX interpretation misconceptions in Learning Hub and About & Sources | Scenario figures illustrative; no claim of measured student need or research study |
| **15** Prototype functionality & learning design | Five interactive views, sidebar controls, guided numerical example, 3 scenario presets, 4-variable sensitivity, charts, context tutor, quiz, CSV/JSON | Source compiled; tests passed; must install Streamlit and demo locally |
| **10** Marketability & feasibility | About & Sources; REPORT section 7: audience, alternative products, differentiation, pilot strategy, costs and improvement opportunities | No invented market size, pricing conversion or user testing |
| **10** Poster & references | A3 one-page poster PDF draft; citations to CFA Institute/IMF/Fed/CME with traceable URLs; complete poster content structure | **INCOMPLETE until team replaces member placeholders and adds a genuine prototype screenshot** |
| **10** Recorded video | `VIDEO_PLAN.md` 10-minute segment-by-segment roles/script; demo steps, 3 verified scenarios, references | **Not delivered: actual recording with every member's role/voice, MP4 and playback check are required** |
| **5** Teamwork & integrity | `REPORT.md` attribution placeholders, exported calculations, `TEST_EVIDENCE.md`, `AI_USE_DISCLOSURE.md` | **INCOMPLETE until team enters actual names/IDs/programmes/contributions and retains proof** |

## Mandatory application features

- **Problem statement:** Learning Hub and About & Sources; REPORT §1.
- **Working demo prototype:** runnable `app.py` + requirements, interactive controls, testable pure engine; screenshot not yet captured (must run Streamlit on member's computer).
- **Finance logic:** mathematical definitions, units, formulas/substitutions, directional explanation, separate independent checks, traceable citations.
- **Learning value:** guided USD tuition example, preset baseline and shocks, personalized contextual tutoring, 6 multiple-choice questions with reasons, adaptive topic revision and live prediction.
- **Marketability:** target, alternatives, differentiated positioning, pilot and feasible extensions.
- **Evidence:** official/institutional URLs, fabricated values explicitly labeled synthetic, test log and exported calculations.
- **Minimum scenarios:** ≥2 (actually 3) numerical scenarios, transparent parameters, sensitivity, MYR interpretation.
- **Variable integration:** MY and US nominal interest rates, expected inflation, MYR/USD FX all appear in one unified interface and calculation chain; explicit IFE/IRP distinction.
- **Responsible AI:** no private data, optional external model off by default, local canonical calculations and clear disclosure.

## Pre-submission items not automatable without the group

1. Enter genuine student names, IDs, programme (IT/IS/CS), group number and actual contributions in poster/report, and in the recorded video credits.
2. Install dependencies, run actual Streamlit UI in a browser, personally verify interactions and take **genuine** screenshot(s) for the poster.
3. Record a group video (approximately 9:30–10:00, never over 10:30 including credits) with attributable part for each member. Verify audio/video and MP4 or accessible link permissions.
4. Add any actual group-run usability results only if properly collected; do not invent pre/post metrics.
5. Ensure group leader alone submits both artifacts before Monday 16 November 2026, **11:59 PM MYT**, and every group member retains all records.
