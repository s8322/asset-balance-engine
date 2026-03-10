from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .asset_source_dates import AssetSourceDates
from .enums import AssetType, Currency
from .liability_metadata import LiabilityMetadata


@dataclass(frozen=True)
class Asset:
    id: str
    name: str
    asset_type: AssetType
    currency: Currency
    description: Optional[str] = None
    owner_label: str | None = None
    institution_name: str | None = None
    source_type: str | None = None
    source_dates: AssetSourceDates | None = None
    liability_metadata: LiabilityMetadata | None = None


__all__ = ["Asset"]

