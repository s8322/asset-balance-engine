from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .enums import AssetType, Currency


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


__all__ = ["Asset"]

