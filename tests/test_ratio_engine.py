from datetime import date

from domain.ratio_engine import calculate_shared_ratio
from domain.shared_period import SharedPeriod


def test_ratio_full_overlap_is_one() -> None:
    period = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 1, 10))

    ratio = calculate_shared_ratio(asset_period=period, marriage_period=period)

    assert ratio == 1.0


def test_ratio_partial_overlap() -> None:
    asset_period = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 1, 10))
    marriage_period = SharedPeriod(start=date(2020, 1, 6), end=date(2020, 1, 15))

    # Overlap is from 6th to 10th (5 days) over 10 days total → 0.5
    ratio = calculate_shared_ratio(
        asset_period=asset_period,
        marriage_period=marriage_period,
    )

    assert ratio == 0.5


def test_ratio_no_overlap_is_zero() -> None:
    asset_period = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 1, 5))
    marriage_period = SharedPeriod(start=date(2020, 1, 6), end=date(2020, 1, 10))

    ratio = calculate_shared_ratio(
        asset_period=asset_period,
        marriage_period=marriage_period,
    )

    assert ratio == 0.0


def test_ratio_capped_when_marriage_period_longer() -> None:
    asset_period = SharedPeriod(start=date(2020, 1, 5), end=date(2020, 1, 10))
    marriage_period = SharedPeriod(start=date(2019, 1, 1), end=date(2021, 1, 1))

    ratio = calculate_shared_ratio(
        asset_period=asset_period,
        marriage_period=marriage_period,
    )

    assert ratio == 1.0


