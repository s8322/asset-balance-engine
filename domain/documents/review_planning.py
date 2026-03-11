from __future__ import annotations

from dataclasses import dataclass

from .enums import DocumentType
from .extraction_enums import FieldKey
from .extraction_models import ExtractedField
from .models import Document
from .review_policy import FieldReviewDecision, field_review_decision


@dataclass(frozen=True)
class FieldReviewPlanEntry:
    extracted_field_id: str
    decision: FieldReviewDecision


@dataclass(frozen=True)
class DocumentReviewPlan:
    document_id: str
    document_type: DocumentType
    fields_needing_review: tuple[FieldReviewPlanEntry, ...]


def plan_document_review(
    document: Document,
    extracted_fields: tuple[ExtractedField, ...],
    *,
    confidence_threshold: float = 0.8,
    field_keys_requiring_review: frozenset[FieldKey] = frozenset(),
) -> DocumentReviewPlan:
    entries: list[FieldReviewPlanEntry] = []
    for extracted_field in extracted_fields:
        decision = field_review_decision(
            extracted_field,
            confidence_threshold=confidence_threshold,
            field_keys_requiring_review=field_keys_requiring_review,
        )
        if decision.needs_review:
            entries.append(
                FieldReviewPlanEntry(
                    extracted_field_id=extracted_field.id,
                    decision=decision,
                )
            )
    return DocumentReviewPlan(
        document_id=document.id,
        document_type=document.document_type,
        fields_needing_review=tuple(entries),
    )


__all__ = [
    "FieldReviewPlanEntry",
    "DocumentReviewPlan",
    "plan_document_review",
]

