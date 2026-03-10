from datetime import date

from domain.enums import AssetType, BorrowerScope, PurposeScope
from domain.liability_metadata import LiabilityMetadata
from domain.liability_sharing_decider import decide_liability_sharing_candidate


def test_non_liability_asset_type_returns_false() -> None:
    metadata = LiabilityMetadata(
        liability_inception_date=date(2020, 1, 1),
        borrower_scope=BorrowerScope.JOINT,
        purpose_scope=PurposeScope.FAMILY_ASSET,
        linked_asset_id="asset-1",
        liability_shared_flag=True,
    )

    result = decide_liability_sharing_candidate(
        asset_type=AssetType.PENSION,
        metadata=metadata,
    )

    assert result is False


def test_metadata_none_returns_false() -> None:
    result = decide_liability_sharing_candidate(
        asset_type=AssetType.LIABILITY,
        metadata=None,
    )

    assert result is False


def test_liability_shared_flag_true_overrides_to_true() -> None:
    metadata = LiabilityMetadata(liability_shared_flag=True)

    result = decide_liability_sharing_candidate(
        asset_type=AssetType.LIABILITY,
        metadata=metadata,
    )

    assert result is True


def test_liability_shared_flag_false_overrides_to_false() -> None:
    metadata = LiabilityMetadata(liability_shared_flag=False)

    result = decide_liability_sharing_candidate(
        asset_type=AssetType.LIABILITY,
        metadata=metadata,
    )

    assert result is False


def test_joint_borrower_and_family_asset_returns_true() -> None:
    metadata = LiabilityMetadata(
        borrower_scope=BorrowerScope.JOINT,
        purpose_scope=PurposeScope.FAMILY_ASSET,
    )

    result = decide_liability_sharing_candidate(
        asset_type=AssetType.LIABILITY,
        metadata=metadata,
    )

    assert result is True


def test_joint_borrower_and_personal_purpose_returns_false() -> None:
    metadata = LiabilityMetadata(
        borrower_scope=BorrowerScope.JOINT,
        purpose_scope=PurposeScope.PERSONAL_A,
    )

    result = decide_liability_sharing_candidate(
        asset_type=AssetType.LIABILITY,
        metadata=metadata,
    )

    assert result is False


def test_non_joint_borrower_even_with_family_purpose_returns_false() -> None:
    metadata = LiabilityMetadata(
        borrower_scope=BorrowerScope.PARTY_A,
        purpose_scope=PurposeScope.FAMILY_ASSET,
    )

    result = decide_liability_sharing_candidate(
        asset_type=AssetType.LIABILITY,
        metadata=metadata,
    )

    assert result is False


