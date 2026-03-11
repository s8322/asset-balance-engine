from __future__ import annotations

from dataclasses import dataclass

from .anomaly_models import AnomalyItem
from .builtin_schemas import get_builtin_schema
from .enums import DocumentType
from .extraction_models import ExtractedField
from .models import Document
from .schema_validation import SchemaValidationResult, validate_extraction
from .validation_to_anomaly import anomalies_from_validation


@dataclass(frozen=True)
class DocumentProcessingResult:
    document_id: str
    document_type: DocumentType
    schema_applied: bool
    validation_result: SchemaValidationResult | None
    anomalies: tuple[AnomalyItem, ...]


def process_document_schema_validation(
    document: Document,
    extracted_fields: tuple[ExtractedField, ...],
) -> DocumentProcessingResult:
    schema = get_builtin_schema(document.document_type)
    if schema is None:
        return DocumentProcessingResult(
            document_id=document.id,
            document_type=document.document_type,
            schema_applied=False,
            validation_result=None,
            anomalies=(),
        )
    validation_result = validate_extraction(schema, extracted_fields)
    anomalies = anomalies_from_validation(validation_result, document.id)
    return DocumentProcessingResult(
        document_id=document.id,
        document_type=document.document_type,
        schema_applied=True,
        validation_result=validation_result,
        anomalies=anomalies,
    )


__all__ = [
    "DocumentProcessingResult",
    "process_document_schema_validation",
]
