from __future__ import annotations

from dataclasses import dataclass

from .enums import DocumentType
from .extraction_enums import FieldKey


@dataclass(frozen=True)
class FieldRequirement:
    field_key: FieldKey
    required: bool


@dataclass(frozen=True)
class DocumentExtractionSchema:
    document_type: DocumentType
    field_requirements: tuple[FieldRequirement, ...]


__all__ = [
    "FieldRequirement",
    "DocumentExtractionSchema",
]
