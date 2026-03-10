from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class CalculationTrack:
    id: str
    case_id: str
    name: str
    created_at: datetime
    description: Optional[str] = None
    run_ids: list[str] = field(default_factory=list)


__all__ = ["CalculationTrack"]

