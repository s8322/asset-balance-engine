from __future__ import annotations

from domain.budgetary_pension_input import BudgetaryPensionInput
from domain.budgetary_pension_result import BudgetaryPensionResult
from domain.calculation_orchestrator import run_budgetary_pension_calculation


class BudgetaryPensionService:
    def calculate(
        self,
        input: BudgetaryPensionInput,
    ) -> BudgetaryPensionResult:
        return run_budgetary_pension_calculation(input)


__all__ = ["BudgetaryPensionService"]

