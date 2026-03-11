from __future__ import annotations

from domain.enums import AssetType
from domain.liability_calculation_result import LiabilityCalculationResult
from domain.liability_metadata import LiabilityMetadata
from domain.liability_sharing_decider import decide_liability_sharing_candidate


class LiabilityCalculator:
    def calculate(
        self,
        total_amount: float,
        asset_type: AssetType,
        metadata: LiabilityMetadata | None,
    ) -> LiabilityCalculationResult:
        is_candidate = decide_liability_sharing_candidate(asset_type, metadata)
        shared_amount = total_amount if is_candidate else 0.0
        return LiabilityCalculationResult(
            total_amount=total_amount,
            is_candidate_for_sharing=is_candidate,
            shared_amount=shared_amount,
        )


__all__ = ["LiabilityCalculator"]

