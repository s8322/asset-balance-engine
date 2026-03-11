from __future__ import annotations

from dataclasses import dataclass

from .enums import DocumentType
from .extraction_enums import FieldKey
from .extraction_models import ExtractedField
from .schema_models import DocumentExtractionSchema


@dataclass(frozen=True)
class ExtraFieldsResult:
    document_type: DocumentType
    extra_field_keys: tuple[FieldKey, ...]


def detect_extra_fields(
    schema: DocumentExtractionSchema,
    extracted_fields: tuple[ExtractedField, ...],
) -> ExtraFieldsResult:
    schema_keys = {fr.field_key for fr in schema.field_requirements}
    present_keys = {ef.field_key for ef in extracted_fields}
    extra = present_keys - schema_keys
    return ExtraFieldsResult(
        document_type=schema.document_type,
        extra_field_keys=tuple(sorted(extra, key=lambda k: k.value)),
    )


__all__ = [
    "ExtraFieldsResult",
    "detect_extra_fields",
]
