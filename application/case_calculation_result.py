from __future__ import annotations

from dataclasses import dataclass

from domain.calculation_result import CalculationResult


@dataclass
class CaseCalculationResult:
    results: list[CalculationResult]
    calculated_asset_ids: list[str]
    skipped_asset_ids: list[str]
    total_assets: int
    calculated_count: int
    skipped_count: int


__all__ = ["CaseCalculationResult"]
