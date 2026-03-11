from datetime import date

from application.liability_calculation_service import LiabilityCalculationService
from domain.enums import AssetType, BorrowerScope, PurposeScope
from domain.liability_metadata import LiabilityMetadata


def test_liability_calculation_service_delegates_to_domain() -> None:
    metadata = LiabilityMetadata(
        liability_inception_date=date(2020, 1, 1),
        borrower_scope=BorrowerScope.JOINT,
        purpose_scope=PurposeScope.FAMILY_ASSET,
    )
    service = LiabilityCalculationService()

    result = service.calculate_liability(
        total_amount=5000.0,
        asset_type=AssetType.LIABILITY,
        metadata=metadata,
    )

    assert result.total_amount == 5000.0
    assert result.is_candidate_for_sharing is True
    assert result.shared_amount == 5000.0

