from __future__ import annotations

from dataclasses import dataclass

from domain.enums import AssetType
from domain.liability_metadata import LiabilityMetadata


@dataclass
class LiabilityInput:
    total_amount: float
    asset_type: AssetType
    metadata: LiabilityMetadata | None


__all__ = ["LiabilityInput"]

