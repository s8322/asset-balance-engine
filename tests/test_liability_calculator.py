from datetime import date

from domain.calculators.liability import LiabilityCalculator
from domain.enums import AssetType, BorrowerScope, PurposeScope
from domain.liability_metadata import LiabilityMetadata


def test_liability_candidate_true_shared_amount_equals_total() -> None:
    metadata = LiabilityMetadata(
        liability_inception_date=date(2020, 1, 1),
        borrower_scope=BorrowerScope.JOINT,
        purpose_scope=PurposeScope.FAMILY_ASSET,
    )
    calculator = LiabilityCalculator()

    result = calculator.calculate(
        total_amount=1000.0,
        asset_type=AssetType.LIABILITY,
        metadata=metadata,
    )

    assert result.total_amount == 1000.0
    assert result.is_candidate_for_sharing is True
    assert result.shared_amount == 1000.0


def test_liability_candidate_false_shared_amount_zero() -> None:
    metadata = LiabilityMetadata(
        borrower_scope=BorrowerScope.PARTY_A,
        purpose_scope=PurposeScope.PERSONAL_A,
    )
    calculator = LiabilityCalculator()

    result = calculator.calculate(
        total_amount=2000.0,
        asset_type=AssetType.LIABILITY,
        metadata=metadata,
    )

    assert result.total_amount == 2000.0
    assert result.is_candidate_for_sharing is False
    assert result.shared_amount == 0.0


def test_non_liability_asset_type_never_candidate() -> None:
    metadata = LiabilityMetadata(
        borrower_scope=BorrowerScope.JOINT,
        purpose_scope=PurposeScope.FAMILY_ASSET,
    )
    calculator = LiabilityCalculator()

    result = calculator.calculate(
        total_amount=1500.0,
        asset_type=AssetType.PENSION,
        metadata=metadata,
    )

    assert result.total_amount == 1500.0
    assert result.is_candidate_for_sharing is False
    assert result.shared_amount == 0.0

