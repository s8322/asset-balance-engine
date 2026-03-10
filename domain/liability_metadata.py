from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .enums import BorrowerScope, PurposeScope


@dataclass(frozen=True)
class LiabilityMetadata:
    liability_inception_date: date | None = None
    borrower_scope: BorrowerScope | None = None
    purpose_scope: PurposeScope | None = None
    linked_asset_id: str | None = None
    liability_shared_flag: bool | None = None


__all__ = ["LiabilityMetadata"]

