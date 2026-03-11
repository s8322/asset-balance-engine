from __future__ import annotations

from domain.enums import AssetType
from domain.liability_calculation_result import LiabilityCalculationResult
from domain.liability_metadata import LiabilityMetadata
from domain.calculation_orchestrator import run_liability_calculation


class LiabilityCalculationService:
    def calculate_liability(
        self,
        total_amount: float,
        asset_type: AssetType,
        metadata: LiabilityMetadata | None,
    ) -> LiabilityCalculationResult:
        return run_liability_calculation(
            total_amount=total_amount,
            asset_type=asset_type,
            metadata=metadata,
        )


__all__ = ["LiabilityCalculationService"]

