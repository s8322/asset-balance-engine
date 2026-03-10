from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .asset import Asset


@dataclass
class Case:
    id: str
    name: str
    created_at: datetime
    assets: list[Asset] = field(default_factory=list)


__all__ = ["Case"]

