from __future__ import annotations

from dataclasses import dataclass

from domain.liability_calculation_result import LiabilityCalculationResult

from .case_calculation_result import CaseCalculationResult


@dataclass
class CaseFullCalculationResult:
    asset_calculation: CaseCalculationResult
    liability_results: list[LiabilityCalculationResult]
    total_assets_shared_value: float
    total_liabilities_shared_value: float
    net_shared_value: float


__all__ = ["CaseFullCalculationResult"]

