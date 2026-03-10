from __future__ import annotations

from dataclasses import dataclass

from .extraction_enums import ExtractedValueType, ExtractionMethod


@dataclass(frozen=True)
class ExtractedField:
    id: str
    document_id: str
    field_name: str
    raw_value: str | None
    normalized_value: str | None
    value_type: ExtractedValueType
    confidence: float | None
    source_page: int | None
    source_snippet: str | None
    extraction_method: ExtractionMethod


__all__ = ["ExtractedField"]
