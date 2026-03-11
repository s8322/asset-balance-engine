from __future__ import annotations

from datetime import date

from domain.asset import Asset
from domain.enums import AssetType
from domain.liability_calculation_result import LiabilityCalculationResult
from domain.liability_metadata import LiabilityMetadata
from domain.shared_period import SharedPeriod

from .case_calculation_result import CaseCalculationResult
from .case_calculation_service import CaseCalculationService
from .case_full_calculation_result import CaseFullCalculationResult
from .liability_calculation_service import LiabilityCalculationService


class CaseFullCalculationService:
    def calculate_full_case(
        self,
        assets: list[Asset],
        liabilities: list[tuple[float, AssetType, LiabilityMetadata | None]],
        marriage_period: SharedPeriod,
        valuation_date: date,
        balance_by_asset_id: dict[str, float] | None = None,
    ) -> CaseFullCalculationResult:
        asset_service = CaseCalculationService()
        asset_calculation: CaseCalculationResult = asset_service.calculate_case(
            assets=assets,
            marriage_period=marriage_period,
            valuation_date=valuation_date,
            balance_by_asset_id=balance_by_asset_id,
        )

        liability_service = LiabilityCalculationService()
        liability_results: list[LiabilityCalculationResult] = []
        for total_amount, asset_type, metadata in liabilities:
            result = liability_service.calculate_liability(
                total_amount=total_amount,
                asset_type=asset_type,
                metadata=metadata,
            )
            liability_results.append(result)

        total_assets_shared_value = asset_calculation.total_gross_shared_value
        total_liabilities_shared_value = sum(
            r.shared_amount for r in liability_results
        )
        net_shared_value = total_assets_shared_value - total_liabilities_shared_value

        return CaseFullCalculationResult(
            asset_calculation=asset_calculation,
            liability_results=liability_results,
            total_assets_shared_value=total_assets_shared_value,
            total_liabilities_shared_value=total_liabilities_shared_value,
            net_shared_value=net_shared_value,
        )


__all__ = ["CaseFullCalculationService"]

