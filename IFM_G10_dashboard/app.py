"""FinBridge AI | Finance Tutor + Scenario Engine.

Run: streamlit run app.py
All default market-like figures are clearly HYPOTHETICAL teaching assumptions.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from finance_engine import (Inputs, calculate, independent_check, as_record,
                            with_change, depreciation_sentence)
from learning_content import QUIZ, assess
from tutor import TOPICS, generate_ai_explanation, offline_tutor

st.set_page_config(page_title="FinBridge AI | Finance Tutor", page_icon="🌐",
                   layout="wide", initial_sidebar_state="expanded")

COLORS = {"teal": "#38e6bf", "blue": "#63a8ff", "yellow": "#f9c874",
          "muted": "#9fb2c9", "slate": "#101d30"}
PRESETS = {
    "01 · Baseline semester": dict(spot=4.50, my_rate=4.0, us_rate=5.0,
                                   my_inflation=3.0, us_inflation=2.0, years=1,
                                   usd_expense=12000.0),
    "02 · Malaysia inflation shock": dict(spot=4.50, my_rate=4.0, us_rate=5.0,
                                            my_inflation=6.5, us_inflation=2.0,
                                            years=1, usd_expense=12000.0),
    "03 · Malaysia interest shock": dict(spot=4.50, my_rate=7.0, us_rate=5.0,
                                           my_inflation=3.0, us_inflation=2.0,
                                           years=1, usd_expense=12000.0),
}
RISK_NOTES = [
    "**Covered IRP:** presumes matching-maturity investable rates, financing access, no transaction costs, taxes, capital restrictions, credit risk, or cross-currency basis. The result is an *implied* forward price, not a live dealer quote.",
    "**Relative PPP:** assumes price differentials ultimately transmit into the exchange rate. Non-traded services, structural changes, tariffs and short-run capital flows can cause major departures.",
    "**Fisher:** derives a real rate from nominal rates and *expected* inflation; realized inflation can differ, and real rates need not match between economies.",
    "**IFE / uncovered interest parity:** uses nominal interest differentials as an *expected spot* hypothesis under additional equilibrium and risk assumptions. It is not a contract, not a guaranteed forecast, and can fail empirically.",
    "**Scenario horizon:** annual effective rates and expected inflation are assumed constant and compounded for the selected years; no stochastic path, changing term structure, bid-ask spread, fees, volatility or live data is modeled.",
]

st.markdown("""
<style>
.block-container {max-width: 1430px; padding-top: 1.8rem; padding-bottom: 3rem;}
[data-testid="stSidebar"] {background: #0b1829; border-right: 1px solid #203551;}
[data-testid="stSidebar"] .stMarkdown h3 {color: #eef5ff;}
.hero {padding: 32px 35px 28px; background: linear-gradient(115deg,#102b3a 0%,#102846 57%,#17244a 100%);
 border:1px solid #315273; border-radius:20px; margin-bottom:20px;}
.hero-eyebrow {color:#4bf2cb;font-size:12px;font-weight:800;letter-spacing:2.1px;}
.hero-title {font-size:2.7rem; font-weight:800; color:#f6faff; line-height:1.1; margin:10px 0;}
.hero-sub {color:#b8cbe0;max-width:820px;font-size:1.06rem;line-height:1.6;}
.chip {display:inline-block;background:#1d4352;color:#80f1d8;border:1px solid #2a6772;
 padding:7px 11px;border-radius:30px;font-size:12px;margin:12px 8px 0 0;}
.section-kicker {color:#48dbbd; font-size:.81rem; font-weight:800; letter-spacing:1.5px; margin:8px 0;}
.callout {background:#12273a;border-left:4px solid #3ce5bd;padding:14px 17px;border-radius:8px;color:#d8e8f3;margin:12px 0;}
.small-quiet {color:#9cb5ca;font-size:12px;}
div[data-testid="stMetric"] {background:#11233a;border:1px solid #2b4862;padding:18px;border-radius:14px;}
div[data-testid="stMetricLabel"]{color:#bccfe4;}
h1,h2,h3 {letter-spacing:-.025em;}
[data-testid="stDownloadButton"] button {width:100%;}
footer {visibility:hidden;}
</style>""", unsafe_allow_html=True)


def apply_preset():
    vals = PRESETS[st.session_state.preset]
    for key, value in vals.items():
        st.session_state["setting_" + key] = value


if "preset" not in st.session_state:
    st.session_state.preset = next(iter(PRESETS))
    apply_preset()
if "page" not in st.session_state:
    st.session_state.page = "Learning Hub"
if "goal" not in st.session_state:
    st.session_state.goal = "Understand finance concepts"

with st.sidebar:
    st.markdown("### 🌐 FinBridge AI")
    st.caption("GFB3043 / GEB3043  ·  International Financial Management")
    st.divider()
    st.radio("Explore the dashboard",
             ["Learning Hub", "Scenario Engine", "AI Tutor", "Knowledge Check", "About & Sources"],
             key="page")
    st.divider()
    st.markdown("### ⚙️ Scenario controls")
    st.selectbox("Choose a guided case", list(PRESETS.keys()), key="preset", on_change=apply_preset)
    st.number_input("Spot exchange rate · MYR per USD", min_value=0.01, max_value=25.0,
                    step=0.05, format="%.4f", key="setting_spot")
    lcol, rcol = st.columns(2)
    with lcol:
        st.number_input("MY interest · % p.a.", min_value=-5.0, max_value=25.0,
                        step=0.5, format="%.2f", key="setting_my_rate")
        st.number_input("MY inflation · % p.a.", min_value=-5.0, max_value=25.0,
                        step=0.5, format="%.2f", key="setting_my_inflation")
    with rcol:
        st.number_input("US interest · % p.a.", min_value=-5.0, max_value=25.0,
                        step=0.5, format="%.2f", key="setting_us_rate")
        st.number_input("US inflation · % p.a.", min_value=-5.0, max_value=25.0,
                        step=0.5, format="%.2f", key="setting_us_inflation")
    st.slider("Planning horizon · years", 1, 5, key="setting_years")
    st.number_input("Future USD expense", min_value=0.0, max_value=10000000.0,
                    step=500.0, format="%.2f", key="setting_usd_expense")
    st.warning("ILLUSTRATIVE inputs only — **not live rates**.", icon="⚠️")

p = Inputs(spot=st.session_state.setting_spot,
           my_rate=st.session_state.setting_my_rate / 100,
           us_rate=st.session_state.setting_us_rate / 100,
           my_inflation=st.session_state.setting_my_inflation / 100,
           us_inflation=st.session_state.setting_us_inflation / 100,
           years=st.session_state.setting_years,
           usd_expense=st.session_state.setting_usd_expense)
r = calculate(p)
check = independent_check(p, r)


def hero(kicker: str, title: str, summary: str):
    st.markdown(
        f'<div class="hero"><div class="hero-eyebrow">{kicker}</div>'
        f'<div class="hero-title">{title}</div>'
        f'<div class="hero-sub">{summary}</div>'
        '<span class="chip">MYR / USD</span><span class="chip">INTERACTIVE MODELS</span>'
        '<span class="chip">BEGINNER FRIENDLY</span></div>', unsafe_allow_html=True)


def movement_text(change: float) -> str:
    if abs(change) < 1e-8:
        return "MYR unchanged"
    return "MYR depreciation" if change > 0 else "MYR appreciation"


def display_model_cards():
    a, b, c = st.columns(3)
    with a:
        st.metric("Covered IRP · implied forward", f"{r.irp_forward:.4f} MYR/USD",
                  f"{r.irp_change_pct:+.2f}% vs spot", delta_color="off")
        st.caption("Derived from the MY and US **nominal interest rates**; NOT future spot.")
    with b:
        st.metric("Relative PPP · expected spot", f"{r.ppp_future:.4f} MYR/USD",
                  f"{r.ppp_change_pct:+.2f}% vs spot", delta_color="off")
        st.caption("Conditional model scenario derived from **inflation differentials**.")
    with c:
        st.metric("Fisher · MY real interest", f"{r.my_real_rate_pct:.2f}% p.a.",
                  f"US: {r.us_real_rate_pct:.2f}% p.a.", delta_color="off")
        st.caption("Inflation-adjusted implied **real** annual interest rates.")


def comparison_chart():
    names = ["Spot today", "PPP future spot*", "IFE expected spot*", "IRP forward*"]
    values = [r.spot, r.ppp_future, r.ife_future, r.irp_forward]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=names, y=values, marker_color=["#7285a5", COLORS["teal"],
                    COLORS["yellow"], COLORS["blue"]],
                    text=[f"{v:.4f}" for v in values], textposition="outside",
                    hovertemplate="%{x}<br>%{y:.4f} MYR/USD<extra></extra>"))
    lo = min(values) * 0.96
    hi = max(values) * 1.045
    fig.update_layout(height=355, margin=dict(l=8, r=12, t=14, b=20),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#dbe7f7"),
                      yaxis=dict(title="MYR per USD", range=[lo, hi],
                                 gridcolor="#284159", zeroline=False),
                      xaxis=dict(tickfont=dict(size=12)),
                      showlegend=False)
    return fig


if st.session_state.page == "Learning Hub":
    hero("THE FINANCE CLASSROOM, REIMAGINED", "Make sense of money across borders.",
         "A hands-on international finance tutor for non-finance university students. "
         "Explore how interest rates, inflation and foreign exchange interact—without treating "
         "theory as a guaranteed currency forecast.")
    st.markdown("<div class='section-kicker'>YOUR CURRENT SCENARIO · VERIFIED ENGINE</div>", unsafe_allow_html=True)
    display_model_cards()
    left, right = st.columns([1.35, 1], gap="large")
    with left:
        st.markdown("### How the three variables connect")
        st.markdown("""
**Inflation differences** → **Relative PPP** → conditional exchange-rate change.

**Expected inflation + real returns** → **Fisher relation** → nominal interest rates.

**Nominal interest differences** → **Covered IRP** → theoretical forward exchange rate.

**Interest-rate differentials + additional expectations assumptions** → **IFE/UIP** → hypothetical *future spot* change.
""")
        st.markdown('<div class="callout"><b>Reading the quote:</b> MYR/USD ↑ means USD becomes more expensive in ringgit; MYR <b>depreciates</b>. MYR/USD ↓ means MYR <b>appreciates</b>.</div>', unsafe_allow_html=True)
        st.info(depreciation_sentence(r.ppp_change_pct, "PPP"))
    with right:
        st.markdown("### Guided example · overseas tuition")
        st.write(f"Imagine a student owing **USD {p.usd_expense:,.0f}** in **{p.years} year(s)**. "
                 "With the selected illustrative rates:")
        st.metric("Today's MYR equivalent", f"RM {r.spot_budget_myr:,.2f}")
        st.metric("PPP-modeled future MYR budget", f"RM {r.ppp_budget_myr:,.2f}")
        st.metric("IRP theoretical forward-equivalent", f"RM {r.irp_budget_myr:,.2f}")
        st.caption("These are teaching comparisons, not a payment quote. PPP is a conditional forecast, while an FX forward would lock a rate only if actually quoted and contracted.")
        def navigate_to_scenario():
            # Streamlit callbacks execute before widget creation on the next rerun.
            st.session_state.page = "Scenario Engine"

        st.button("Explore the complete scenario →", use_container_width=True,
                  type="primary", on_click=navigate_to_scenario)
    st.divider()
    st.markdown("### Three ready-to-demonstrate numerical scenarios")
    rows = []
    for label, vals in PRESETS.items():
        x = Inputs(spot=vals["spot"], my_rate=vals["my_rate"] / 100,
                   us_rate=vals["us_rate"] / 100,
                   my_inflation=vals["my_inflation"] / 100,
                   us_inflation=vals["us_inflation"] / 100,
                   years=vals["years"], usd_expense=vals["usd_expense"])
        y = calculate(x)
        rows.append({"Scenario": label, "MY rate (%)": vals["my_rate"],
                     "MY inflation (%)": vals["my_inflation"],
                     "IRP forward (MYR/USD)": round(y.irp_forward, 4),
                     "PPP future (MYR/USD)": round(y.ppp_future, 4),
                     "PPP MYR move (%)": round(y.ppp_change_pct, 2)})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.caption("All sample inputs are invented for learning, not sourced from live financial markets. Compare case 02 against baseline to isolate an inflation shock, and case 03 to isolate an interest-rate shock.")
    st.markdown("**Learning objective CLO3:** Analyse, not merely memorize, the relationships among interest rates, inflation rates and foreign exchange movements.")

elif st.session_state.page == "Scenario Engine":
    hero("INTERACTIVE SANDBOX / 02", "Scenario Engine", "Change the assumptions in the sidebar and observe model-based exchange rates, overseas budgets and sensitivity in real time.")
    display_model_cards()
    st.markdown("### Model comparison · one quote convention")
    l, rr = st.columns([1.4, 1], gap="large")
    with l:
        st.plotly_chart(comparison_chart(), use_container_width=True)
        st.caption("*PPP and IFE: conditional future spot hypotheses. IRP: no-arbitrage forward pricing. They should not be interpreted as interchangeable forecast accuracy measurements.")
    with rr:
        st.markdown("#### Plain-English interpretations")
        st.info(depreciation_sentence(r.ppp_change_pct, "relative PPP"))
        st.info(depreciation_sentence(r.irp_change_pct, "covered IRP forward pricing"))
        st.markdown(f"**Nominal rate gap:** {(p.my_rate-p.us_rate)*100:+.2f} percentage points (Malaysia minus US).")
        st.markdown(f"**Inflation gap:** {(p.my_inflation-p.us_inflation)*100:+.2f} percentage points.")
        st.markdown(f"**Exact Fisher real-rate gap:** {r.real_rate_gap_pp:+.2f} percentage points.")
        st.warning("A higher nominal interest rate does not automatically mean an appreciating currency. Changes in rates, risk, expectations and the initial FX quote matter.")
    st.divider()
    st.markdown("### Formula transparency & assumptions")
    with st.expander("See all formulas, substitutions, and quote direction", expanded=True):
        a, b = st.columns(2)
        with a:
            st.markdown("**Covered Interest Rate Parity (CIP / IRP)**")
            st.latex(r"F_{MYR/USD}=S_{MYR/USD}\left(\frac{1+i_{MY}}{1+i_{US}}\right)^T")
            st.code(f"F = {p.spot:.4f} × ((1 + {p.my_rate:.4f}) / (1 + {p.us_rate:.4f})) ^ {p.years}\n  = {r.irp_forward:.6f} MYR/USD")
            st.markdown("**Relative Purchasing Power Parity (PPP)**")
            st.latex(r"E[S_T]_{PPP}=S_0\left(\frac{1+\pi_{MY}}{1+\pi_{US}}\right)^T")
            st.code(f"PPP = {p.spot:.4f} × ((1 + {p.my_inflation:.4f}) / (1 + {p.us_inflation:.4f})) ^ {p.years}\n    = {r.ppp_future:.6f} MYR/USD")
        with b:
            st.markdown("**Exact Fisher equation (separate economies)**")
            st.latex(r"1+i=(1+r)(1+\pi^e)\quad\Rightarrow\quad r=\frac{1+i}{1+\pi^e}-1")
            st.code(f"MY: 1.0 + {p.my_rate:.4f} over 1.0 + {p.my_inflation:.4f} → r = {r.my_real_rate_pct:.4f}%\nUS: 1.0 + {p.us_rate:.4f} over 1.0 + {p.us_inflation:.4f} → r = {r.us_real_rate_pct:.4f}%")
            st.markdown("**IFE / UIP expected-spot hypothesis**")
            st.latex(r"E[S_T]_{IFE}=S_0\left(\frac{1+i_{MY}}{1+i_{US}}\right)^T")
            st.code(f"IFE = {r.ife_future:.6f} MYR/USD (hypothesis, NOT contract)")
        st.caption("T is years; all i and π are annual effective decimal rates (4%=0.04). Spot is MYR per USD. Compounding assumes constant annual inputs and matching horizon. For IRP, rates are theoretical investable yields over that term.")
    st.divider()
    st.markdown("### Sensitivity lab · change ONE assumption")
    col_a, col_b = st.columns([1, 1])
    names = {"Malaysian inflation": "my_inflation", "US inflation": "us_inflation",
             "Malaysian nominal interest": "my_rate", "US nominal interest": "us_rate"}
    with col_a:
        selected = st.selectbox("Variable to shock", list(names.keys()))
    with col_b:
        shock = st.slider("Increase / decrease · percentage points", min_value=-2.5,
                          max_value=2.5, step=0.5, value=2.0)
    shocked = with_change(p, names[selected], shock)
    changed = calculate(shocked)
    sl, sr, sc = st.columns(3)
    sl.metric("PPP baseline → shocked", f"{changed.ppp_future:.4f}",
              f"{(changed.ppp_future-r.ppp_future):+.4f} MYR/USD", delta_color="off")
    sr.metric("IRP baseline → shocked", f"{changed.irp_forward:.4f}",
              f"{(changed.irp_forward-r.irp_forward):+.4f} MYR/USD", delta_color="off")
    sc.metric("Tuition under PPP · changed", f"RM {changed.ppp_budget_myr:,.2f}",
              f"RM {(changed.ppp_budget_myr-r.ppp_budget_myr):+,.2f}", delta_color="off")
    deltas = [j * 0.5 for j in range(-5, 6)]
    rates_ppp, rates_irp = [], []
    for d in deltas:
        outcome = calculate(with_change(p, names[selected], d))
        rates_ppp.append(outcome.ppp_future)
        rates_irp.append(outcome.irp_forward)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=deltas, y=rates_ppp, name="PPP future spot", mode="lines+markers",
                             line=dict(color=COLORS["teal"], width=3)))
    fig.add_trace(go.Scatter(x=deltas, y=rates_irp, name="IRP implied forward", mode="lines+markers",
                             line=dict(color=COLORS["blue"], width=3)))
    fig.add_vline(x=shock, line_dash="dot", line_color=COLORS["yellow"],
                  annotation_text="Selected shock", annotation_position="top right")
    fig.update_layout(height=345, margin=dict(l=10,r=10,t=32,b=15),
                      xaxis_title="Change in selected input (percentage points)",
                      yaxis_title="Model output (MYR/USD)",
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#e2ebf4"), legend=dict(orientation="h", y=1.15),
                      xaxis=dict(gridcolor="#294056"), yaxis=dict(gridcolor="#294056"))
    st.plotly_chart(fig, use_container_width=True)
    if names[selected].endswith("inflation"):
        st.success("Sensitivity insight: changing only inflation moves PPP, not IRP, because IRP takes *nominal interest* as its inputs. Fisher-implied real rates adjust when nominal rates are held fixed.")
    else:
        st.success("Sensitivity insight: changing only nominal interest moves IRP/IFE, not PPP, because PPP takes *expected inflation* as its inputs. The Fisher-implied real rate adjusts when inflation is held fixed.")
    st.divider()
    st.markdown("### Independent calculation checks & export")
    if check["passed"]:
        st.success("6 / 6 validation checks passed: independent Decimal formulas and the covered-interest parity identity.")
    else:
        st.error("Validation failed — do not use these outputs until investigated.")
    with st.expander("See arithmetic verification evidence"):
        st.dataframe(pd.DataFrame([{"Test": k, "Status": "PASS" if v else "FAIL"}
                                   for k,v in check["checks"].items()]),
                     hide_index=True, use_container_width=True)
        st.caption(f"Maximum check difference: {check['max_reference_difference_myr_per_usd']:.3g} MYR/USD. Mathematical checks do not validate real-world forecasts.")
    snapshot = {"scenario": as_record(p, r), "change_variable": names[selected],
                "change_pp": shock, "changed_output": asdict(changed),
                "verification": check, "data_notice": "Hypothetical classroom data; not live market rates."}
    b1, b2 = st.columns(2)
    with b1:
        st.download_button("Download this scenario · JSON", data=json.dumps(snapshot, indent=2),
                           file_name="finbridge_verified_scenario.json", mime="application/json")
    with b2:
        st.download_button("Download numbers · CSV", data=pd.DataFrame([
            {"scenario": "baseline", **as_record(p,r)},
            {"scenario": "sensitivity", **as_record(shocked,changed)}]).to_csv(index=False),
            file_name="finbridge_scenarios.csv", mime="text/csv")

elif st.session_state.page == "AI Tutor":
    hero("CONTEXT-AWARE STUDENT SUPPORT / 03", "Meet your finance tutor.",
         "Ask a question about the exact scenario on your screen. Get a beginner-friendly explanation and see the verified values beside it.")
    left, right = st.columns([1.4,1], gap="large")
    with left:
        st.selectbox("What are you learning for?",
                     ["Understand finance concepts", "Plan overseas study expenses",
                      "Prepare for an international finance exam"], key="goal")
        suggested = st.selectbox("Start with a common question", TOPICS)
        if st.button("Use this suggested question"):
            st.session_state.tutor_question = suggested
        st.text_area("Or write your own question", key="tutor_question", height=115,
                     placeholder="Why does MYR depreciation increase my tuition cost?", max_chars=500)
        api_ready = bool(os.getenv("OPENAI_API_KEY"))
        if api_ready:
            st.success("Optional AI explanation service configured. Verified finance numbers remain local.")
            use_gen = st.toggle("Use generative AI for the explanation (optional)", value=False)
        else:
            use_gen = False
            st.info("**Offline tutor ready.** Add `OPENAI_API_KEY` in your deployment environment to optionally enable generative AI explanations. Offline teaching feedback works without any API key.")
        if st.button("Explain this to me", type="primary", use_container_width=True):
            question = st.session_state.tutor_question.strip()
            if not question:
                st.warning("Please enter or select a finance question.")
            else:
                if use_gen:
                    try:
                        with st.spinner("Generating a context-aware explanation…"):
                            answer = generate_ai_explanation(question, p, r, st.session_state.goal)
                        st.session_state.tutor_mode = "AI-generated narrative · verify with fact panel"
                    except Exception as exc:
                        answer = offline_tutor(question, p, r, st.session_state.goal)
                        st.session_state.tutor_mode = "Offline fallback after API error"
                        st.warning(f"AI service unavailable; switched to verified offline coaching ({type(exc).__name__}).")
                else:
                    answer = offline_tutor(question, p, r, st.session_state.goal)
                    st.session_state.tutor_mode = "Deterministic, rule-based offline feedback"
                st.session_state.tutor_answer = answer
        if st.session_state.get("tutor_answer"):
            st.markdown("#### Tutor response")
            st.caption(st.session_state.get("tutor_mode", "Teaching feedback"))
            st.markdown(st.session_state.tutor_answer)
            st.caption("Narrative explanations are for education; rely on the independently checked finance engine for numerical outputs.")
    with right:
        st.markdown("### Your verified scenario facts")
        st.metric("MYR/USD spot", f"{p.spot:.4f}")
        st.metric("PPP future spot (model)", f"{r.ppp_future:.4f}")
        st.metric("IRP forward (theoretical)", f"{r.irp_forward:.4f}")
        st.metric("Fisher real · MY / US", f"{r.my_real_rate_pct:.2f}% / {r.us_real_rate_pct:.2f}%")
        st.caption("Values calculated locally by finance_engine.py, not generated by AI text.")
        st.markdown("**Need a hint?** Try comparing scenario 01 to 02, then ask why PPP reacts but the IRP forward does not.")

elif st.session_state.page == "Knowledge Check":
    hero("ACTIVE LEARNING / 04", "Test your finance intuition.",
         "Six concept questions plus a live prediction challenge. Each submission gives immediate, topic-specific feedback.")
    st.markdown("### 6-question concept quiz")
    st.caption("Select your answer to every question, then check your understanding. No registration or external storage.")
    with st.form("quiz_form"):
        chosen = []
        for j,q in enumerate(QUIZ):
            st.markdown(f"**Q{j+1}. {q.question}**")
            option = st.radio("Select one", q.options, key=f"quiz_{j}", index=None,
                              label_visibility="collapsed")
            chosen.append(q.options.index(option) if option is not None else None)
        submit = st.form_submit_button("Grade my quiz", type="primary")
    if submit:
        if any(x is None for x in chosen):
            st.warning("Answer all six questions before grading.")
        else:
            score, details = assess(chosen)
            st.session_state.quiz_result = (score, details)
    if "quiz_result" in st.session_state:
        score, details = st.session_state.quiz_result
        st.progress(score/len(QUIZ), text=f"You scored {score}/{len(QUIZ)}  ·  {100*score/len(QUIZ):.0f}%")
        for j, d in enumerate(details):
            if d["correct"]:
                st.success(f"Q{j+1} · {d['topic']}: Correct — {d['explanation']}")
            else:
                st.error(f"Q{j+1} · {d['topic']}: Review this — {d['explanation']} Correct answer: {d['expected']}")
        weak = sorted({d["topic"] for d in details if not d["correct"]})
        if weak:
            st.info("**Your personalized revision topics:** " + ", ".join(weak) + ". Open AI Tutor to ask about these concepts, then retake the quiz.")
        else:
            st.balloons()
            st.success("Excellent integration: you distinguished spot, forwards, inflation and nominal/real rates.")
    st.divider()
    st.markdown("### Dynamic prediction challenge")
    moved = calculate(with_change(p, "my_inflation", 1.0))
    st.markdown("**What happens to the PPP-implied MYR/USD rate if expected Malaysian inflation rises by 1 percentage point, holding all other inputs fixed?**")
    choice = st.radio("Your prediction", ["MYR/USD increases", "MYR/USD decreases", "MYR/USD does not change"],
                      index=None, key="dynamic_prediction")
    if st.button("Check my prediction"):
        if choice is None:
            st.warning("Please select your prediction.")
        elif choice == "MYR/USD increases":
            st.success(f"Correct. PPP changes from {r.ppp_future:.4f} to {moved.ppp_future:.4f} MYR/USD. The ringgit depreciates in this model when its inflation is higher.")
        else:
            st.error(f"Reconsider the quotation. Relative PPP rises from {r.ppp_future:.4f} to {moved.ppp_future:.4f} MYR/USD because the MY inflation numerator increases.")
    st.caption("This classroom prediction is an exact *within-model* directional statement, not a claim about actual spot price reactions.")

else:
    hero("PROJECT BRIEF / 05", "Methods, market fit & evidence.",
         "Everything the assessor needs to trace the learning problem, CLO3, theoretical models, risks, references and responsible use of AI.")
    st.markdown("### Who is this for — and what problem does it solve?")
    st.markdown("""
**Learners:** Non-finance Malaysian university students facing international tuition payments, overseas travel budgets or a first international finance module.

**Learning problem:** Introductory learners often mix up *a weaker currency* with a lower MYR/USD quote, or confuse an IRP-derived forward with a spot forecast. Formula-only materials lack immediate changes-of-input and misconception diagnosis.

**Solution:** A no-login Streamlit web application combining transparent arithmetic, preset financial scenarios, an interactive sensitivity experiment, an offline contextual tutor, optional generative feedback, self-tests, and downloadable numerical audit trails.

**CLO3 connection:** Connect expected inflation → PPP exchange-rate adjustment, inflation and real returns → Fisher nominal interest, and nominal interest differentials → IRP pricing / IFE exchange-rate hypotheses. Explicitly distinguish model-implied outputs, assumptions and risks.
""")
    st.markdown("### Marketability & realistic adoption")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("#### Target & alternatives")
        st.write("University intro-finance courses and peer-led study groups. Alternatives include static lecture slides, formula calculators, generic chatbot answers and advanced professional terminals.")
    with c2:
        st.markdown("#### Distinctive value")
        st.write("MYR/USD quote clarity, linked IRP/PPP/Fisher outputs, assumption-sensitive charts, independently checked arithmetic, exam-ready feedback, and an offline-first prototype with no compulsory subscription.")
    with c3:
        st.markdown("#### Pilot & iteration")
        st.write("Run a classroom pilot, measure pre/post concept quiz improvement with consent, refine misconceptions, add accessibility and mobile refinements, then consider institution-hosted deployment.")
    st.caption("No market size, learning improvement, user-testing, or adoption statistics are claimed; the above is a proposed feasibility strategy.")
    st.markdown("### Assumptions and limitations")
    for note in RISK_NOTES:
        st.markdown("- " + note)
    st.markdown("### Finance accuracy and source trail")
    st.write("The calculations use exact discrete-compounding formulas and independent Decimal reference calculations, plus a parity identity. References:")
    st.markdown("""
1. CFA Institute (2026). *Currency Exchange Rates: Understanding Equilibrium Value.* [CFA Institute](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/currency-exchange-rates-understanding-equilibrium-value). IRP, PPP, International Fisher and forecasting limitations.
2. CME Group / Rogerson, M. (2024). *Covered Interest Parity, Implied Forward FX Swaps, Cross-Currency Basis.* [CME Group](https://www.cmegroup.com/articles/whitepapers/covered-interest-parity-implied-forward-foreign-exchange-swaps-cross-currency-basis-and-cme-estr-futures.html). Forward FX pricing.
3. Callen, T. / IMF (2018). *Purchasing Power Parity: Weights Matter.* [IMF](https://www.imf.org/en/publications/fandd/issues/series/back-to-basics/purchasing-power-parity-ppp). PPP concept.
4. Federal Reserve Bank of St. Louis (2023). *Adjusting for Inflation.* [St. Louis Fed](https://www.stlouisfed.org/publications/page-one-economics/2023/01/03/adjusting-for-inflation). Nominal versus real rates.
5. CFA Institute (2021). *Investment Governance for Climate Change* (International Fisher Effect conversion and limitations). [CFA Institute PDF](https://www.cfainstitute.org/sites/default/files/-/media/documents/book/rf-publication/2021/igcc-summary-edition-2021.pdf).
6. Universiti Teknologi PETRONAS, Department of Management (2026). *FinBridge AI Innovation Challenge*, GFB3043 / GEB3043. **Course-provided assignment brief**.
""")
    st.markdown("### Financial verification status")
    st.success(f"Independent checks: {sum(check['checks'].values())} / {len(check['checks'])} PASS" if check["passed"] else "One or more calculations failed validation.")
    with st.expander("Open verification details"):
        for desc, ok in check["checks"].items():
            st.write(("✅" if ok else "❌") + " " + desc)
    st.markdown("### Responsible AI and privacy")
    st.markdown("""
- The finance engine and all numerical results are deterministic, not computed by an LLM. The offline tutor uses transparent keyword/rule matching and **is not represented as generative AI**.
- Optional generative explanation requires a separately configured API key. If enabled, the current **synthetic** scenario, learning goal and learner question are sent to an external model. Do not enter names, student IDs, bank information or private financial data.
- AI narrative is **not independently fact-checked sentence by sentence**; users must verify any financial claims against the fixed fact panel and source equations. It must not substitute for the verified calculation engine.
- All market-like inputs are explicitly hypothetical; no real-time data, empirical forecast accuracy, human testing or deployment availability is claimed.
- See `docs/AI_USE_DISCLOSURE.md`, `docs/REPORT.md`, and unit tests supplied with the source package.
""")

st.divider()
st.caption("FINBRIDGE AI · FINANCE TUTOR & SCENARIO ENGINE  |  UTP GFB3043 / GEB3043 · CLO3  |  All numeric scenarios illustrative; educational only.")
