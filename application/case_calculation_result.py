from __future__ import annotations

from dataclasses import dataclass

from domain.calculation_result import CalculationResult

from .case_metrics import CaseMetrics


@dataclass
class CaseCalculationResult:
    results: list[CalculationResult]
    calculated_asset_ids: list[str]
    skipped_asset_ids: list[str]
    total_gross_shared_value: float
    metrics: CaseMetrics


__all__ = ["CaseCalculationResult"]
