from __future__ import annotations

from dataclasses import dataclass

from domain.enums import AssetType, CalculationTrackType


@dataclass
class CaseMetrics:
    total_assets: int
    calculated_count: int
    skipped_count: int
    by_asset_type: dict[AssetType, int]
    by_track_type: dict[CalculationTrackType, int]
    gross_shared_value_by_asset_type: dict[AssetType, float]


__all__ = ["CaseMetrics"]
