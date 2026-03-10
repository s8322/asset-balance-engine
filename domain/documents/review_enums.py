from __future__ import annotations

from enum import Enum


class ReviewStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DEFERRED = "DEFERRED"


class ReviewOutcome(str, Enum):
    ACCEPTED_AS_IS = "ACCEPTED_AS_IS"
    ACCEPTED_WITH_CORRECTION = "ACCEPTED_WITH_CORRECTION"
    REJECTED = "REJECTED"
    NOT_REVIEWED = "NOT_REVIEWED"


__all__ = [
    "ReviewStatus",
    "ReviewOutcome",
]
