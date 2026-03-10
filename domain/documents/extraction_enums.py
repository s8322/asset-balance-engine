from __future__ import annotations

from enum import Enum


class ExtractedValueType(str, Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    DATE = "DATE"
    DATETIME = "DATETIME"
    BOOLEAN = "BOOLEAN"
    CURRENCY = "CURRENCY"
    PERCENTAGE = "PERCENTAGE"
    UNKNOWN = "UNKNOWN"


class ExtractionMethod(str, Enum):
    RULE_BASED = "RULE_BASED"
    MODEL_BASED = "MODEL_BASED"
    TEMPLATE_BASED = "TEMPLATE_BASED"
    MANUAL_ENTRY = "MANUAL_ENTRY"
    IMPORT = "IMPORT"


__all__ = [
    "ExtractedValueType",
    "ExtractionMethod",
]
