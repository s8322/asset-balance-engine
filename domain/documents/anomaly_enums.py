from __future__ import annotations

from enum import Enum


class AnomalySeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    BLOCKER = "BLOCKER"


class AnomalyStatus(str, Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
    IGNORED = "IGNORED"


class AnomalyCode(str, Enum):
    CORRUPTED_FILE = "CORRUPTED_FILE"
    PASSWORD_REQUIRED = "PASSWORD_REQUIRED"
    MISSING_REQUIRED_VALUE = "MISSING_REQUIRED_VALUE"
    LOW_CONFIDENCE_VALUE = "LOW_CONFIDENCE_VALUE"
    DOCUMENT_ASSET_MISMATCH = "DOCUMENT_ASSET_MISMATCH"
    CONFLICTING_EXTRACTED_VALUES = "CONFLICTING_EXTRACTED_VALUES"
    UNKNOWN_DOCUMENT_TYPE = "UNKNOWN_DOCUMENT_TYPE"
    OTHER = "OTHER"


__all__ = [
    "AnomalySeverity",
    "AnomalyStatus",
    "AnomalyCode",
]
