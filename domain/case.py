from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

from .asset import Asset


@dataclass
class Case:
    id: str
    case_number: str
    party_a_name: str
    party_b_name: str
    marriage_date: date
    separation_date: date | None
    valuation_date: date
    created_at: datetime
    assets: list[Asset] = field(default_factory=list)


__all__ = ["Case"]

