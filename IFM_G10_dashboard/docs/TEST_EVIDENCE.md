# Test and verification evidence

**Automated unit tests (run during generation):** `18 passed` (pytest); Python compilation succeeded for app, model, offline tutor and quiz modules. Tests are in `tests/test_finance_engine.py`. Deterministic, offline engine requires no web network or market feed.

**Independent checks inside `finance_engine.independent_check`:** six Boolean checks covering independent Decimal precision of covered IRP F, relative PPP projection, Malaysia/US Fisher inversion, covered parity arithmetic identity, and separation of IFE economic meaning with equal idealized algebra. These checks repeat for any valid set of user input values. They validate internal computation, not predictive validity of financial models.

## Reference test vectors

**Baseline**: spot=4.50 MYR/USD; Malaysian/US i=4%/5%; expected inflation=3%/2%; T=1 year; USD expense=12,000. `F_IRP=4.457142857; S_PPP=4.544117647; MY Fisher r=0.970873786%; US Fisher r=2.941176471%; PPP tuition=RM54,529.4118`.

**Inflation shock**: change MY inflation to 6.5%, others unchanged. `S_PPP=4.698529412; F_IRP=4.457142857; MY Fisher r=-2.347417840%; PPP tuition=RM56,382.3529`.

**Interest shock**: change MY interest to 7%, others unchanged. `F_IRP=4.585714286; S_PPP=4.544117647; MY Fisher r=3.883495146%`.

### UI validation that the team MUST complete

- [ ] `pip install -r requirements.txt` succeeds in local Python 3.10+ virtual environment.
- [ ] `streamlit run app.py` opens a live web dashboard at localhost:8501.
- [ ] All five navigation pages render, rates change, presets reset parameters, no exceptions in console.
- [ ] Model chart and sensitivity chart update and agree with numeric changes.
- [ ] For baseline, PPP>spot and IRP<spot with correct MYR appreciation/depreciation descriptions.
- [ ] Changing only MY inflation shifts PPP but not IRP; changing only MY interest shifts IRP but not PPP.
- [ ] Complete quiz: correct and incorrect answers receive expected feedback; live prediction challenge responds.
- [ ] Optional AI mode with a **real, properly funded key** is tested or remains disabled; numbers must come from the fact panel.
- [ ] JSON and CSV download cleanly; a spreadsheet displays the correct numeric units.
- [ ] Capture a **real browser screenshot** of Scenario Engine to replace placeholder on poster.
- [ ] Check keyboard/mobile usability, A3 poster PDF legibility and final video audio/playback/permissions.

**Execution constraint:** Streamlit could not be installed in the provided generation environment because the package network index was unreachable (DNS / no network). Therefore we deliberately do **not** claim a successful full Streamlit browser test or provide an invented screenshot. The project is still source-complete and installation instructions are supplied. The group must complete the UI checklist locally.
