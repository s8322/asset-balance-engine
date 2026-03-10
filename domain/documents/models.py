from __future__ import annotations

from dataclasses import dataclass

from .enums import DocumentFormat, DocumentSourceType, DocumentStatus, DocumentType


@dataclass(frozen=True)
class Document:
    id: str
    case_id: str
    asset_id: str | None
    document_type: DocumentType
    source_type: DocumentSourceType
    status: DocumentStatus
    file_format: DocumentFormat
    original_filename: str
    stored_path: str
    content_hash: str | None = None
    description: str | None = None


__all__ = ["Document"]
