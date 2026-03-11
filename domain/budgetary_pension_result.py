from __future__ import annotations

from dataclasses import dataclass

from .enums import BudgetaryPensionMode, BudgetaryPensionStatus


@dataclass(frozen=True)
class BudgetaryPensionResult:
    mode: BudgetaryPensionMode
    shared_ratio: float | None
    transfer_ratio: float | None
    shared_service_period_days: int | None
    total_service_period_days: int | None
    expected_monthly_pension: float | None
    shared_monthly_pension: float | None
    gross_shared_value: float | None
    status: BudgetaryPensionStatus
    block_reason: str | None
    manual_review_required: bool


__all__ = ["BudgetaryPensionResult"]

