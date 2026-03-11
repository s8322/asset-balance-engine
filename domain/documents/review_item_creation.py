from __future__ import annotations

from uuid import uuid4

from .review_enums import ReviewStatus
from .review_models import ReviewItem
from .review_planning import DocumentReviewPlan


def review_items_from_plan(
    plan: DocumentReviewPlan,
) -> tuple[ReviewItem, ...]:
    if not plan.fields_needing_review:
        return ()
    return tuple(
        ReviewItem(
            id=str(uuid4()),
            document_id=plan.document_id,
            extracted_field_id=entry.extracted_field_id,
            status=ReviewStatus.PENDING,
            outcome=None,
            corrected_value=None,
            reviewed_at=None,
            note=None,
        )
        for entry in plan.fields_needing_review
    )


__all__ = ["review_items_from_plan"]

