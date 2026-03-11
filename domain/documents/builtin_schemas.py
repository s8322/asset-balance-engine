from __future__ import annotations

from .enums import DocumentType
from .extraction_enums import FieldKey
from .schema_models import DocumentExtractionSchema, FieldRequirement

_PENSION_REPORT_SCHEMA = DocumentExtractionSchema(
    document_type=DocumentType.PENSION_REPORT,
    field_requirements=(
        FieldRequirement(FieldKey.BALANCE, True),
        FieldRequirement(FieldKey.REPORT_DATE, True),
        FieldRequirement(FieldKey.INSTITUTION_NAME, True),
        FieldRequirement(FieldKey.ACCOUNT_NUMBER, False),
        FieldRequirement(FieldKey.START_DATE, False),
        FieldRequirement(FieldKey.END_DATE, False),
        FieldRequirement(FieldKey.EMPLOYEE_CONTRIBUTION, False),
        FieldRequirement(FieldKey.EMPLOYER_CONTRIBUTION, False),
        FieldRequirement(FieldKey.EMPLOYER_NAME, False),
        FieldRequirement(FieldKey.OUTSTANDING_BALANCE, False),
        FieldRequirement(FieldKey.WITHDRAWAL, False),
        FieldRequirement(FieldKey.SALARY_BASE, False),
        FieldRequirement(FieldKey.TOTAL_UNITS, False),
        FieldRequirement(FieldKey.POLICY_NUMBER, False),
    ),
)

_SALARY_SLIP_SCHEMA = DocumentExtractionSchema(
    document_type=DocumentType.SALARY_SLIP,
    field_requirements=(
        FieldRequirement(FieldKey.REPORT_DATE, True),
        FieldRequirement(FieldKey.SALARY_BASE, True),
        FieldRequirement(FieldKey.EMPLOYER_NAME, True),
        FieldRequirement(FieldKey.EMPLOYEE_CONTRIBUTION, False),
        FieldRequirement(FieldKey.EMPLOYER_CONTRIBUTION, False),
        FieldRequirement(FieldKey.BALANCE, False),
        FieldRequirement(FieldKey.INSTITUTION_NAME, False),
        FieldRequirement(FieldKey.TOTAL_UNITS, False),
    ),
)

_BANK_STATEMENT_SCHEMA = DocumentExtractionSchema(
    document_type=DocumentType.BANK_STATEMENT,
    field_requirements=(
        FieldRequirement(FieldKey.ACCOUNT_NUMBER, True),
        FieldRequirement(FieldKey.BALANCE, True),
        FieldRequirement(FieldKey.REPORT_DATE, True),
        FieldRequirement(FieldKey.INSTITUTION_NAME, False),
        FieldRequirement(FieldKey.START_DATE, False),
        FieldRequirement(FieldKey.END_DATE, False),
        FieldRequirement(FieldKey.WITHDRAWAL, False),
        FieldRequirement(FieldKey.OUTSTANDING_BALANCE, False),
    ),
)

BUILTIN_SCHEMAS: tuple[DocumentExtractionSchema, ...] = (
    _PENSION_REPORT_SCHEMA,
    _SALARY_SLIP_SCHEMA,
    _BANK_STATEMENT_SCHEMA,
)


def get_builtin_schema(document_type: DocumentType) -> DocumentExtractionSchema | None:
    for schema in BUILTIN_SCHEMAS:
        if schema.document_type == document_type:
            return schema
    return None


__all__ = [
    "BUILTIN_SCHEMAS",
    "get_builtin_schema",
]
