from __future__ import annotations

from dataclasses import dataclass

from domain.enums import AssetType


@dataclass
class CaseMetrics:
    total_assets: int
    calculated_count: int
    skipped_count: int
    by_asset_type: dict[AssetType, int]


__all__ = ["CaseMetrics"]
