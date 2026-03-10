from __future__ import annotations

from datetime import date

from domain.asset import Asset
from domain.asset_track_mapping import map_asset_type_to_track_type
from domain.calculation_orchestrator import run_calculation_for_asset
from domain.calculation_result import CalculationResult
from domain.enums import AssetType, CalculationTrackType
from domain.shared_period import SharedPeriod

from .case_calculation_result import CaseCalculationResult
from .case_metrics import CaseMetrics


class CaseCalculationService:
    def calculate_case(
        self,
        assets: list[Asset],
        marriage_period: SharedPeriod,
        valuation_date: date,
        balance_by_asset_id: dict[str, float] | None = None,
    ) -> CaseCalculationResult:
        balance_by_asset_id = balance_by_asset_id or {}
        results: list[CalculationResult] = []
        calculated_asset_ids: list[str] = []
        skipped_asset_ids: list[str] = []
        by_asset_type: dict[AssetType, int] = {}
        by_track_type: dict[CalculationTrackType, int] = {}

        for asset in assets:
            by_asset_type[asset.asset_type] = (
                by_asset_type.get(asset.asset_type, 0) + 1
            )
            track_type = map_asset_type_to_track_type(asset.asset_type)
            by_track_type[track_type] = by_track_type.get(track_type, 0) + 1
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
                calculated_asset_ids.append(asset.id)
            else:
                skipped_asset_ids.append(asset.id)

        metrics = CaseMetrics(
            total_assets=len(assets),
            calculated_count=len(calculated_asset_ids),
            skipped_count=len(skipped_asset_ids),
            by_asset_type=by_asset_type,
            by_track_type=by_track_type,
        )
        return CaseCalculationResult(
            results=results,
            calculated_asset_ids=calculated_asset_ids,
            skipped_asset_ids=skipped_asset_ids,
            metrics=metrics,
        )
