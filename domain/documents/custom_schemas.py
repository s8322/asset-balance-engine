from __future__ import annotations

from dataclasses import dataclass

from .enums import DocumentType
from .extraction_enums import FieldKey
from .builtin_schemas import get_builtin_schema
from .schema_models import DocumentExtractionSchema, FieldRequirement


@dataclass(frozen=True)
class ActuaryDocumentSchemaOverride:
    document_type: DocumentType
    extra_required_field_keys: frozenset[FieldKey]


def apply_actuary_override(
    schema: DocumentExtractionSchema,
    override: ActuaryDocumentSchemaOverride | None,
) -> DocumentExtractionSchema:
    if override is None:
        return schema
    if override.document_type != schema.document_type:
        return schema
    effective_required: set[FieldKey] = {
        fr.field_key for fr in schema.field_requirements if fr.required
    }
    effective_required |= set(override.extra_required_field_keys)
    schema_keys = {fr.field_key for fr in schema.field_requirements}
    new_requirements: list[FieldRequirement] = [
        FieldRequirement(fr.field_key, fr.field_key in effective_required)
        for fr in schema.field_requirements
    ]
    for key in override.extra_required_field_keys:
        if key not in schema_keys:
            new_requirements.append(FieldRequirement(key, True))
    return DocumentExtractionSchema(
        document_type=schema.document_type,
        field_requirements=tuple(new_requirements),
    )


def get_effective_schema(
    document_type: DocumentType,
    override: ActuaryDocumentSchemaOverride | None,
) -> DocumentExtractionSchema | None:
    builtin_schema = get_builtin_schema(document_type)
    if builtin_schema is not None:
        return apply_actuary_override(builtin_schema, override)
    if (
        builtin_schema is None
        and override is not None
        and override.document_type == document_type
    ):
        return DocumentExtractionSchema(
            document_type=document_type,
            field_requirements=tuple(
                FieldRequirement(key, True) for key in override.extra_required_field_keys
            ),
        )
    return None


__all__ = [
    "ActuaryDocumentSchemaOverride",
    "apply_actuary_override",
    "get_effective_schema",
]
