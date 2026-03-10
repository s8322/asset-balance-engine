from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class AssetSourceDates:
    account_opened_date: date | None = None
    first_contribution_date: date | None = None
    service_start_date: date | None = None
    grant_date: date | None = None


__all__ = ["AssetSourceDates"]

