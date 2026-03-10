from __future__ import annotations

from dataclasses import dataclass

from .enums import DocumentType
from .extraction_enums import FieldKey
from .extraction_models import ExtractedField
from .schema_models import DocumentExtractionSchema


@dataclass(frozen=True)
class SchemaValidationResult:
    document_type: DocumentType
    valid: bool
    missing_required: tuple[FieldKey, ...]
    present_field_keys: tuple[FieldKey, ...]


def validate_extraction(
    schema: DocumentExtractionSchema,
    extracted_fields: tuple[ExtractedField, ...],
) -> SchemaValidationResult:

    required_keys = tuple(
        fr.field_key for fr in schema.field_requirements if fr.required
    )

    present_keys = tuple(dict.fromkeys(ef.field_key for ef in extracted_fields))

    present_set = set(present_keys)

    missing_required = tuple(
        key for key in required_keys if key not in present_set
    )

    return SchemaValidationResult(
        document_type=schema.document_type,
        valid=len(missing_required) == 0,
        missing_required=missing_required,
        present_field_keys=present_keys,
    )


__all__ = [
    "SchemaValidationResult",
    "validate_extraction",
]