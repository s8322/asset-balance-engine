from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .enums import AssetClass, Currency


@dataclass(frozen=True)
class Asset:
    id: str
    name: str
    asset_class: AssetClass
    currency: Currency
    description: Optional[str] = None


__all__ = ["Asset"]

