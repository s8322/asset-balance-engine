from __future__ import annotations

from datetime import date

from domain.budgetary_pension_input import BudgetaryPensionInput
from domain.budgetary_pension_result import BudgetaryPensionResult
from domain.enums import BudgetaryPensionMode, BudgetaryPensionStatus


class BudgetaryPensionCalculator:
    def calculate_law_mode(self, input: BudgetaryPensionInput) -> BudgetaryPensionResult:
        service_start = input.service_start_date
        separation = input.separation_date
        marriage_start = input.marriage_start_date

        if service_start is None or separation is None or marriage_start is None:
            return BudgetaryPensionResult(
                mode=BudgetaryPensionMode.LAW,
                shared_ratio=None,
                transfer_ratio=None,
                shared_service_period_days=None,
                total_service_period_days=None,
                expected_monthly_pension=None,
                shared_monthly_pension=None,
                gross_shared_value=None,
                status=BudgetaryPensionStatus.BLOCKED,
                block_reason="missing mandatory dates",
                manual_review_required=True,
            )

        if separation < service_start:
            return BudgetaryPensionResult(
                mode=BudgetaryPensionMode.LAW,
                shared_ratio=None,
                transfer_ratio=None,
                shared_service_period_days=None,
                total_service_period_days=None,
                expected_monthly_pension=None,
                shared_monthly_pension=None,
                gross_shared_value=None,
                status=BudgetaryPensionStatus.BLOCKED,
                block_reason="invalid service period",
                manual_review_required=True,
            )

        total_service_period_days = _inclusive_days(service_start, separation)

        shared_start = max(service_start, marriage_start)
        shared_end = separation
        if shared_start > shared_end:
            shared_service_period_days = 0
        else:
            shared_service_period_days = _inclusive_days(shared_start, shared_end)

        if shared_service_period_days == 0:
            return BudgetaryPensionResult(
                mode=BudgetaryPensionMode.LAW,
                shared_ratio=0.0,
                transfer_ratio=0.0,
                shared_service_period_days=0,
                total_service_period_days=total_service_period_days,
                expected_monthly_pension=None,
                shared_monthly_pension=None,
                gross_shared_value=None,
                status=BudgetaryPensionStatus.OK,
                block_reason=None,
                manual_review_required=False,
            )

        shared_ratio = shared_service_period_days / total_service_period_days
        transfer_ratio = shared_ratio / 2

        return BudgetaryPensionResult(
            mode=BudgetaryPensionMode.LAW,
            shared_ratio=shared_ratio,
            transfer_ratio=transfer_ratio,
            shared_service_period_days=shared_service_period_days,
            total_service_period_days=total_service_period_days,
            expected_monthly_pension=None,
            shared_monthly_pension=None,
            gross_shared_value=None,
            status=BudgetaryPensionStatus.OK,
            block_reason=None,
            manual_review_required=False,
        )

    def calculate_capitalization_mode(
        self,
        input: BudgetaryPensionInput,
        shared_ratio: float,
        shared_service_period_days: int,
        total_service_period_days: int,
    ) -> BudgetaryPensionResult:
        expected_monthly_pension = input.expected_monthly_pension

        if expected_monthly_pension is None:
            if input.salary_base is not None and input.pension_rate is not None:
                expected_monthly_pension = input.salary_base * input.pension_rate
            else:
                return BudgetaryPensionResult(
                    mode=BudgetaryPensionMode.CAPITALIZATION,
                    shared_ratio=shared_ratio,
                    transfer_ratio=shared_ratio / 2 if shared_ratio is not None else None,
                    shared_service_period_days=shared_service_period_days,
                    total_service_period_days=total_service_period_days,
                    expected_monthly_pension=None,
                    shared_monthly_pension=None,
                    gross_shared_value=None,
                    status=BudgetaryPensionStatus.BLOCKED,
                    block_reason="missing expected pension / salary base + rate",
                    manual_review_required=True,
                )

        shared_monthly_pension = expected_monthly_pension * shared_ratio

        return BudgetaryPensionResult(
            mode=BudgetaryPensionMode.CAPITALIZATION,
            shared_ratio=shared_ratio,
            transfer_ratio=shared_ratio / 2,
            shared_service_period_days=shared_service_period_days,
            total_service_period_days=total_service_period_days,
            expected_monthly_pension=expected_monthly_pension,
            shared_monthly_pension=shared_monthly_pension,
            gross_shared_value=None,
            status=BudgetaryPensionStatus.PARTIAL,
            block_reason="capitalization pending",
            manual_review_required=True,
        )

    def calculate(self, input: BudgetaryPensionInput) -> BudgetaryPensionResult:
        law_result = self.calculate_law_mode(input)

        if law_result.status is BudgetaryPensionStatus.BLOCKED:
            return law_result

        has_capitalization_inputs = (
            input.expected_monthly_pension is not None
            or (input.salary_base is not None and input.pension_rate is not None)
        )

        if not has_capitalization_inputs:
            return law_result

        if law_result.shared_ratio is None or law_result.shared_service_period_days is None:
            return law_result

        return self.calculate_capitalization_mode(
            input=input,
            shared_ratio=law_result.shared_ratio,
            shared_service_period_days=law_result.shared_service_period_days,
            total_service_period_days=law_result.total_service_period_days
            if law_result.total_service_period_days is not None
            else 0,
        )


def _inclusive_days(start: date, end: date) -> int:
    return (end - start).days + 1


__all__ = ["BudgetaryPensionCalculator"]

