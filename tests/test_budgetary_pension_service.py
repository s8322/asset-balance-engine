from datetime import date

from application.budgetary_pension_service import BudgetaryPensionService
from domain.budgetary_pension_input import BudgetaryPensionInput
from domain.enums import BudgetaryPensionMode, BudgetaryPensionStatus


def test_budgetary_pension_service_calculate_wiring() -> None:
    input_data = BudgetaryPensionInput(
        service_start_date=date(2010, 1, 1),
        separation_date=date(2020, 1, 1),
        marriage_start_date=date(2015, 1, 1),
        owner_party="A",
        expected_monthly_pension=10000.0,
        salary_base=None,
        pension_rate=None,
        retirement_date=None,
    )

    service = BudgetaryPensionService()
    result = service.calculate(input_data)

    assert result.mode in {
        BudgetaryPensionMode.LAW,
        BudgetaryPensionMode.CAPITALIZATION,
    }
    assert result.status in {
        BudgetaryPensionStatus.OK,
        BudgetaryPensionStatus.PARTIAL,
    }

