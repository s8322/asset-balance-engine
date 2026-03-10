from __future__ import annotations

from datetime import date

from domain.asset import Asset
from domain.calculation_orchestrator import run_calculation_for_asset
from domain.calculation_result import CalculationResult
from domain.shared_period import SharedPeriod


class CaseCalculationService:
    def calculate_case(
        self,
        assets: list[Asset],
        marriage_period: SharedPeriod,
        valuation_date: date,
        balance_by_asset_id: dict[str, float] | None = None,
    ) -> list[CalculationResult]:
        balance_by_asset_id = balance_by_asset_id or {}
        results: list[CalculationResult] = []

        for asset in assets:
            balance = balance_by_asset_id.get(asset.id, 0.0)
            result = run_calculation_for_asset(
                asset_type=asset.asset_type,
                source_dates=asset.source_dates,
                current_balance=balance,
                valuation_date=valuation_date,
                marriage_period=marriage_period,
            )
            if result is not None:
                results.append(result)

        return results
