from __future__ import annotations

from .enums import AssetType, BorrowerScope, PurposeScope
from .liability_metadata import LiabilityMetadata


def decide_liability_sharing_candidate(
    asset_type: AssetType,
    metadata: LiabilityMetadata | None,
) -> bool:
    if asset_type is not AssetType.LIABILITY:
        return False

    if metadata is None:
        return False

    if metadata.liability_shared_flag is not None:
        return metadata.liability_shared_flag

    if (
        metadata.borrower_scope is BorrowerScope.JOINT
        and metadata.purpose_scope is PurposeScope.FAMILY_ASSET
    ):
        return True

    return False


__all__ = ["decide_liability_sharing_candidate"]

