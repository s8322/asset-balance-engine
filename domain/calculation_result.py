from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CalculationResult:
    total_days: int
    shared_days: int
    shared_ratio: float
    gross_shared_value: float


__all__ = ["CalculationResult"]
