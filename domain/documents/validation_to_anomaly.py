from __future__ import annotations

from uuid import uuid4

from .anomaly_enums import AnomalyCode, AnomalySeverity, AnomalyStatus
from .anomaly_models import AnomalyItem
from .schema_validation import SchemaValidationResult


def anomalies_from_validation(
    result: SchemaValidationResult,
    document_id: str,
) -> tuple[AnomalyItem, ...]:
    if result.valid:
        return ()
    return tuple(
        AnomalyItem(
            id=str(uuid4()),
            document_id=document_id,
            extracted_field_id=None,
            review_item_id=None,
            severity=AnomalySeverity.BLOCKER,
            status=AnomalyStatus.OPEN,
            code=AnomalyCode.MISSING_REQUIRED_VALUE,
            message=f"Missing required field: {field_key.value}",
            note=None,
        )
        for field_key in result.missing_required
    )


__all__ = ["anomalies_from_validation"]
