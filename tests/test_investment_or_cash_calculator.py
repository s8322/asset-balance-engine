from datetime import date

import pytest

from domain.calculators.investment_or_cash import InvestmentOrCashCalculator
from domain.shared_period import SharedPeriod


def test_investment_or_cash_calculator_full_overlap() -> None:
    calculator = InvestmentOrCashCalculator()
    asset_period = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 12, 31))
    marriage_period = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 12, 31))
    current_balance = 1000.0

    result = calculator.calculate(
        current_balance=current_balance,
        asset_period=asset_period,
        marriage_period=marriage_period,
    )

    assert result.total_days == asset_period.days()
    assert result.shared_days == asset_period.days()
    assert result.shared_ratio == pytest.approx(1.0)
    assert result.gross_shared_value == pytest.approx(current_balance)


def test_investment_or_cash_calculator_partial_overlap() -> None:
    calculator = InvestmentOrCashCalculator()
    asset_period = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 12, 31))
    marriage_period = SharedPeriod(start=date(2020, 7, 1), end=date(2020, 12, 31))
    current_balance = 1200.0

    result = calculator.calculate(
        current_balance=current_balance,
        asset_period=asset_period,
        marriage_period=marriage_period,
    )

    assert 0.0 < result.shared_ratio < 1.0
    assert result.shared_days == asset_period.overlap_days(marriage_period)
    assert result.total_days == asset_period.days()
    assert result.gross_shared_value == pytest.approx(
        round(current_balance * result.shared_ratio, 2)
    )


def test_investment_or_cash_calculator_no_overlap() -> None:
    calculator = InvestmentOrCashCalculator()
    asset_period = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 6, 30))
    marriage_period = SharedPeriod(start=date(2020, 7, 1), end=date(2020, 12, 31))
    current_balance = 1500.0

    result = calculator.calculate(
        current_balance=current_balance,
        asset_period=asset_period,
        marriage_period=marriage_period,
    )

    assert result.shared_ratio == 0.0
    assert result.shared_days == 0
    assert result.gross_shared_value == 0.0

