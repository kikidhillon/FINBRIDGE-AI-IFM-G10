"""Pure, independently testable international-finance model for FinBridge AI.

Quote convention: S and F = Malaysian ringgit (MYR) per US dollar (USD).
All rates are ANNUAL DECIMALS: 0.04 means 4%/year.
T is a number of years; all horizon rates are constant annual-effective rates.
Values are theoretical and educational, NEVER real-time prices or investment advice.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from decimal import Decimal, localcontext
from math import isfinite


@dataclass(frozen=True)
class Inputs:
    spot: float = 4.50                 # MYR per USD
    my_rate: float = 0.04             # effective annual MYR interest rate
    us_rate: float = 0.05             # effective annual USD interest rate
    my_inflation: float = 0.03        # annual Malaysian expected inflation
    us_inflation: float = 0.02        # annual US expected inflation
    years: int = 1
    usd_expense: float = 12000.0

    def validate(self) -> None:
        values = (self.spot, self.my_rate, self.us_rate,
                  self.my_inflation, self.us_inflation, self.usd_expense)
        if not all(isfinite(x) for x in values):
            raise ValueError("All inputs must be finite numbers.")
        if self.spot <= 0 or self.usd_expense < 0:
            raise ValueError("The MYR/USD spot rate must be positive, and USD expense cannot be negative.")
        if any(x <= -1 for x in (self.my_rate, self.us_rate, self.my_inflation, self.us_inflation)):
            raise ValueError("Annual rates must be greater than -100%.")
        if not isinstance(self.years, int) or not (1 <= self.years <= 30):
            raise ValueError("Horizon must be a whole number between 1 and 30 years.")


@dataclass(frozen=True)
class Results:
    spot: float
    irp_forward: float
    ppp_future: float
    ife_future: float
    irp_change_pct: float
    ppp_change_pct: float
    ife_change_pct: float
    my_real_rate_pct: float
    us_real_rate_pct: float
    real_rate_gap_pp: float
    spot_budget_myr: float
    irp_budget_myr: float
    ppp_budget_myr: float
    ife_budget_myr: float
    forward_minus_ppp_myr: float


def exact_fisher_real(nominal: float, expected_inflation: float) -> float:
    """r = (1+i)/(1+expected inflation) - 1, as a decimal."""
    return (1.0 + nominal) / (1.0 + expected_inflation) - 1.0


def calculate(p: Inputs) -> Results:
    """Exact compound discrete-rate classroom models, no market data."""
    p.validate()
    irp = p.spot * ((1 + p.my_rate) / (1 + p.us_rate)) ** p.years
    ppp = p.spot * ((1 + p.my_inflation) / (1 + p.us_inflation)) ** p.years
    # Uncovered interest parity/IFE model prediction only; NOT the IRP contract rate.
    ife = p.spot * ((1 + p.my_rate) / (1 + p.us_rate)) ** p.years
    my_real = exact_fisher_real(p.my_rate, p.my_inflation)
    us_real = exact_fisher_real(p.us_rate, p.us_inflation)
    return Results(
        spot=p.spot, irp_forward=irp, ppp_future=ppp, ife_future=ife,
        irp_change_pct=(irp / p.spot - 1) * 100,
        ppp_change_pct=(ppp / p.spot - 1) * 100,
        ife_change_pct=(ife / p.spot - 1) * 100,
        my_real_rate_pct=my_real * 100, us_real_rate_pct=us_real * 100,
        real_rate_gap_pp=(my_real - us_real) * 100,
        spot_budget_myr=p.usd_expense * p.spot,
        irp_budget_myr=p.usd_expense * irp,
        ppp_budget_myr=p.usd_expense * ppp,
        ife_budget_myr=p.usd_expense * ife,
        forward_minus_ppp_myr=p.usd_expense * (irp - ppp),
    )


def independent_check(p: Inputs, actual: Results | None = None) -> dict[str, object]:
    """Separate high-precision Decimal computation, not reused float calculation.

    This independently checks the model arithmetic and adds a parity-arbitrage
    identity. It does not empirically validate whether PPP/IFE predicts markets.
    """
    p.validate()
    if actual is None:
        actual = calculate(p)
    with localcontext() as ctx:
        ctx.prec = 35
        d = lambda value: Decimal(str(value))
        s, my, us = d(p.spot), d(p.my_rate), d(p.us_rate)
        m_pi, u_pi = d(p.my_inflation), d(p.us_inflation)
        t = p.years
        check_irp = s * ((Decimal(1) + my) ** t) / ((Decimal(1) + us) ** t)
        check_ppp = s * ((Decimal(1) + m_pi) ** t) / ((Decimal(1) + u_pi) ** t)
        check_my_real = (1 + my) / (1 + m_pi) - 1
        check_us_real = (1 + us) / (1 + u_pi) - 1
        # MYR deposit: S*(1+i_MY)^T; covered USD deposit: F*(1+i_US)^T
        local_myr = s * (1 + my) ** t
        covered_usd_myr = d(actual.irp_forward) * (1 + us) ** t
        tests = {
            "IRP forward (independent Decimal)": abs(actual.irp_forward - float(check_irp)) < 1e-9,
            "PPP future spot (independent Decimal)": abs(actual.ppp_future - float(check_ppp)) < 1e-9,
            "Malaysia Fisher real rate": abs(actual.my_real_rate_pct / 100 - float(check_my_real)) < 1e-12,
            "US Fisher real rate": abs(actual.us_real_rate_pct / 100 - float(check_us_real)) < 1e-12,
            "IRP covered parity identity": abs(float(local_myr - covered_usd_myr)) < 1e-8,
            "IFE equals UIP calculation, not contract": abs(actual.ife_future - actual.irp_forward) < 1e-10,
        }
    return {"passed": all(tests.values()), "checks": tests,
            "max_reference_difference_myr_per_usd": max(
                abs(actual.irp_forward - float(check_irp)),
                abs(actual.ppp_future - float(check_ppp)),
            )}


def with_change(p: Inputs, name: str, change_pp: float) -> Inputs:
    if name not in ("my_rate", "us_rate", "my_inflation", "us_inflation"):
        raise ValueError("Unsupported sensitivity variable")
    new_value = getattr(p, name) + change_pp / 100
    return replace(p, **{name: new_value})


def as_record(p: Inputs, r: Results) -> dict:
    return {**asdict(p), **asdict(r), "rate_units": "annual decimal",
            "exchange_rate_units": "MYR per USD", "data_status": "illustrative only"}


def depreciation_sentence(change_pct: float, theory: str) -> str:
    if abs(change_pct) < 0.000001:
        return f"Under {theory}, MYR/USD is unchanged: neither currency changes relative to the other."
    if change_pct > 0:
        return (f"Under {theory}, MYR/USD increases {change_pct:.2f}%. "
                "It takes more ringgit to buy USD 1, so MYR **depreciates** against USD.")
    return (f"Under {theory}, MYR/USD decreases {abs(change_pct):.2f}%. "
            "It takes fewer ringgit to buy USD 1, so MYR **appreciates** against USD.")
