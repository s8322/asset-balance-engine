from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .review_enums import ReviewOutcome, ReviewStatus


@dataclass(frozen=True)
class ReviewItem:
    id: str
    document_id: str
    extracted_field_id: str
    status: ReviewStatus
    outcome: ReviewOutcome | None
    corrected_value: str | None
    reviewed_at: datetime | None
    note: str | None


__all__ = ["ReviewItem"]
