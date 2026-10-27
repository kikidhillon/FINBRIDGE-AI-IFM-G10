from dataclasses import replace
import math
import pytest
from finance_engine import (Inputs, calculate, exact_fisher_real, independent_check,
                            with_change, depreciation_sentence)
from learning_content import QUIZ, assess
from tutor import offline_tutor


def test_baseline_formulas_and_units():
    p = Inputs()
    r = calculate(p)
    assert r.irp_forward == pytest.approx(4.5 * 1.04 / 1.05)
    assert r.ppp_future == pytest.approx(4.5 * 1.03 / 1.02)
    assert r.my_real_rate_pct == pytest.approx(((1.04 / 1.03) - 1)*100)
    assert r.spot_budget_myr == 54000
    assert r.ppp_budget_myr == pytest.approx(12000*r.ppp_future)
    assert r.ife_future == pytest.approx(r.irp_forward)
    assert independent_check(p,r)["passed"]


def test_inflation_shock_moves_ppp_not_irp():
    p = Inputs()
    a,b = calculate(p),calculate(with_change(p,"my_inflation",3.5))
    assert b.ppp_future > a.ppp_future
    assert b.irp_forward == pytest.approx(a.irp_forward)
    assert b.my_real_rate_pct < a.my_real_rate_pct


def test_interest_shock_moves_irp_not_ppp():
    p=Inputs()
    a,b=calculate(p),calculate(with_change(p,"my_rate",3))
    assert b.irp_forward > a.irp_forward
    assert b.ppp_future == pytest.approx(a.ppp_future)


def test_reverse_us_shocks():
    p=Inputs()
    x=calculate(p)
    assert calculate(with_change(p,"us_rate",1)).irp_forward < x.irp_forward
    assert calculate(with_change(p,"us_inflation",1)).ppp_future < x.ppp_future


@pytest.mark.parametrize("spot,ir_my,ir_us,pi_my,pi_us,years", [
    (4.50,.04,.05,.03,.02,1), (4.50,.07,.05,.03,.02,1),
    (4.50,.04,.05,.065,.02,1), (4.10,.02,.04,.01,.03,3),
    (5.21,.01,.01,.05,.05,5), (1.0,-.02,.03,-.01,.02,2)
])
def test_decimal_independent_checks(spot,ir_my,ir_us,pi_my,pi_us,years):
    p=Inputs(spot,ir_my,ir_us,pi_my,pi_us,years)
    assert independent_check(p)["passed"]


def test_direction_in_myr_usd_quote():
    assert "depreciates" in depreciation_sentence(2,"PPP")
    assert "appreciates" in depreciation_sentence(-2,"PPP")


@pytest.mark.parametrize("changes", [dict(spot=0),dict(my_rate=-1),
                                    dict(usd_expense=-1),dict(years=0),dict(spot=math.nan)])
def test_invalid_inputs(changes):
    with pytest.raises(ValueError):
        calculate(replace(Inputs(),**changes))


def test_quiz_answer_key_and_feedback():
    assert len(QUIZ) == 6
    result, details = assess([q.correct for q in QUIZ])
    assert result == 6 and all(d["correct"] for d in details)
    result, details = assess([(q.correct + 1)%4 for q in QUIZ])
    assert result == 0 and all(not d["correct"] for d in details)


def test_offline_tutor_uses_verified_results():
    p=Inputs(); r=calculate(p)
    txt=offline_tutor("what is PPP and inflation?",p,r)
    assert f"{r.ppp_future:.4f}" in txt
    assert "PPP" in txt
