from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class BudgetaryPensionInput:
    service_start_date: date | None
    separation_date: date | None
    marriage_start_date: date | None
    owner_party: str | None
    expected_monthly_pension: float | None
    salary_base: float | None
    pension_rate: float | None
    retirement_date: date | None


__all__ = ["BudgetaryPensionInput"]

