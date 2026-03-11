from datetime import date

import pytest

from domain.budgetary_pension_input import BudgetaryPensionInput
from domain.budgetary_pension_result import BudgetaryPensionResult
from domain.calculators.budgetary_pension import BudgetaryPensionCalculator
from domain.enums import BudgetaryPensionMode, BudgetaryPensionStatus


def _base_input() -> BudgetaryPensionInput:
    return BudgetaryPensionInput(
        service_start_date=date(2010, 1, 1),
        separation_date=date(2020, 1, 1),
        marriage_start_date=date(2015, 1, 1),
        owner_party="A",
        expected_monthly_pension=None,
        salary_base=None,
        pension_rate=None,
        retirement_date=None,
    )


def test_law_mode_partial_overlap() -> None:
    calculator = BudgetaryPensionCalculator()
    input_data = _base_input()

    result = calculator.calculate_law_mode(input_data)

    assert result.status is BudgetaryPensionStatus.OK
    assert result.mode is BudgetaryPensionMode.LAW
    assert result.shared_ratio is not None
    assert 0.0 < result.shared_ratio < 1.0
    assert result.transfer_ratio == pytest.approx(result.shared_ratio / 2)


def test_law_mode_no_overlap() -> None:
    calculator = BudgetaryPensionCalculator()
    input_data = BudgetaryPensionInput(
        service_start_date=date(2010, 1, 1),
        separation_date=date(2015, 1, 1),
        marriage_start_date=date(2016, 1, 1),
        owner_party="A",
        expected_monthly_pension=None,
        salary_base=None,
        pension_rate=None,
        retirement_date=None,
    )

    result = calculator.calculate_law_mode(input_data)

    assert result.status is BudgetaryPensionStatus.OK
    assert result.mode is BudgetaryPensionMode.LAW
    assert result.shared_ratio == 0.0
    assert result.transfer_ratio == 0.0


def test_law_mode_missing_mandatory_dates_blocked() -> None:
    calculator = BudgetaryPensionCalculator()
    input_data = BudgetaryPensionInput(
        service_start_date=None,
        separation_date=date(2020, 1, 1),
        marriage_start_date=date(2015, 1, 1),
        owner_party="A",
        expected_monthly_pension=None,
        salary_base=None,
        pension_rate=None,
        retirement_date=None,
    )

    result = calculator.calculate_law_mode(input_data)

    assert result.status is BudgetaryPensionStatus.BLOCKED
    assert result.mode is BudgetaryPensionMode.LAW
    assert result.manual_review_required is True
    assert result.block_reason == "missing mandatory dates"


def test_capitalization_using_expected_monthly_pension() -> None:
    calculator = BudgetaryPensionCalculator()
    base_input = _base_input()
    law_result = calculator.calculate_law_mode(base_input)
    assert law_result.shared_ratio is not None
    assert law_result.shared_service_period_days is not None
    assert law_result.total_service_period_days is not None

    cap_input = BudgetaryPensionInput(
        service_start_date=base_input.service_start_date,
        separation_date=base_input.separation_date,
        marriage_start_date=base_input.marriage_start_date,
        owner_party=base_input.owner_party,
        expected_monthly_pension=10000.0,
        salary_base=None,
        pension_rate=None,
        retirement_date=None,
    )

    result = calculator.calculate(cap_input)

    assert result.mode is BudgetaryPensionMode.CAPITALIZATION
    assert result.status is BudgetaryPensionStatus.PARTIAL
    assert result.expected_monthly_pension == pytest.approx(10000.0)
    assert result.shared_monthly_pension == pytest.approx(
        10000.0 * law_result.shared_ratio
    )
    assert result.gross_shared_value is None
    assert result.manual_review_required is True


def test_capitalization_using_salary_base_and_pension_rate() -> None:
    calculator = BudgetaryPensionCalculator()
    base_input = _base_input()

    cap_input = BudgetaryPensionInput(
        service_start_date=base_input.service_start_date,
        separation_date=base_input.separation_date,
        marriage_start_date=base_input.marriage_start_date,
        owner_party=base_input.owner_party,
        expected_monthly_pension=None,
        salary_base=20000.0,
        pension_rate=0.5,
        retirement_date=None,
    )

    result = calculator.calculate(cap_input)

    assert result.mode is BudgetaryPensionMode.CAPITALIZATION
    assert result.status is BudgetaryPensionStatus.PARTIAL
    assert result.expected_monthly_pension == pytest.approx(10000.0)
    assert result.shared_monthly_pension is not None
    assert result.shared_ratio is not None


def test_capitalization_missing_inputs_falls_back_to_law_mode() -> None:
    calculator = BudgetaryPensionCalculator()
    base_input = _base_input()

    # no expected_monthly_pension and no salary_base/pension_rate
    result = calculator.calculate(base_input)

    assert result.mode is BudgetaryPensionMode.LAW
    assert result.status is BudgetaryPensionStatus.OK
    assert result.block_reason is None

