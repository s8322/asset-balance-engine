from __future__ import annotations

from dataclasses import dataclass

from .anomaly_enums import AnomalyCode, AnomalySeverity, AnomalyStatus


@dataclass(frozen=True)
class AnomalyItem:
    id: str
    document_id: str | None
    extracted_field_id: str | None
    review_item_id: str | None
    severity: AnomalySeverity
    status: AnomalyStatus
    code: AnomalyCode
    message: str
    note: str | None


__all__ = ["AnomalyItem"]
