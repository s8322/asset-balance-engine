from datetime import date

import pytest

from domain.shared_period import SharedPeriod


def test_shared_period_days_single_day() -> None:
    period = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 1, 1))
    assert period.days() == 1


def test_shared_period_days_multiple_days() -> None:
    period = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 1, 10))
    assert period.days() == 10


def test_shared_period_invalid_range_raises() -> None:
    with pytest.raises(ValueError):
        SharedPeriod(start=date(2020, 1, 10), end=date(2020, 1, 1))


def test_shared_period_overlap_returns_expected_period() -> None:
    a = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 1, 10))
    b = SharedPeriod(start=date(2020, 1, 5), end=date(2020, 1, 15))

    overlap = a.overlap(b)
    assert overlap is not None
    assert overlap.start == date(2020, 1, 5)
    assert overlap.end == date(2020, 1, 10)


def test_shared_period_overlap_none_when_disjoint() -> None:
    a = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 1, 5))
    b = SharedPeriod(start=date(2020, 1, 6), end=date(2020, 1, 10))

    assert a.overlap(b) is None
    assert b.overlap(a) is None


def test_shared_period_overlap_days_matches_overlap() -> None:
    a = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 1, 10))
    b = SharedPeriod(start=date(2020, 1, 3), end=date(2020, 1, 5))

    assert a.overlap_days(b) == 3
    assert b.overlap_days(a) == 3


def test_shared_period_overlap_days_zero_when_no_overlap() -> None:
    a = SharedPeriod(start=date(2020, 1, 1), end=date(2020, 1, 5))
    b = SharedPeriod(start=date(2020, 1, 6), end=date(2020, 1, 10))

    assert a.overlap_days(b) == 0
    assert b.overlap_days(a) == 0


