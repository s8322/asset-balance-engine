from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .extraction_enums import FieldKey
from .extraction_models import ExtractedField


class ReviewTrigger(str, Enum):
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    FIELD_KEY_REQUIRES_REVIEW = "FIELD_KEY_REQUIRES_REVIEW"


@dataclass(frozen=True)
class FieldReviewDecision:
    needs_review: bool
    triggers: tuple[ReviewTrigger, ...]


def field_review_decision(
    extracted_field: ExtractedField,
    *,
    confidence_threshold: float = 0.8,
    field_keys_requiring_review: frozenset[FieldKey] = frozenset(),
) -> FieldReviewDecision:
    triggers: list[ReviewTrigger] = []
    if (
        extracted_field.confidence is not None
        and extracted_field.confidence < confidence_threshold
    ):
        triggers.append(ReviewTrigger.LOW_CONFIDENCE)
    if extracted_field.field_key in field_keys_requiring_review:
        triggers.append(ReviewTrigger.FIELD_KEY_REQUIRES_REVIEW)
    needs_review = len(triggers) > 0
    return FieldReviewDecision(needs_review=needs_review, triggers=tuple(triggers))


__all__ = [
    "ReviewTrigger",
    "FieldReviewDecision",
    "field_review_decision",
]
