from datetime import date

from domain.calculation_orchestrator import run_liability_calculation
from domain.enums import AssetType, BorrowerScope, PurposeScope
from domain.liability_metadata import LiabilityMetadata


def test_run_liability_calculation_shared_candidate_returns_full_shared_amount() -> None:
    total_amount = 3000.0
    metadata = LiabilityMetadata(
        liability_inception_date=date(2020, 1, 1),
        borrower_scope=BorrowerScope.JOINT,
        purpose_scope=PurposeScope.FAMILY_ASSET,
    )

    result = run_liability_calculation(
        total_amount=total_amount,
        asset_type=AssetType.LIABILITY,
        metadata=metadata,
    )

    assert result.total_amount == total_amount
    assert result.is_candidate_for_sharing is True
    assert result.shared_amount == total_amount

