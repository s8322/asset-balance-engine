from datetime import date

from domain.asset_source_dates import AssetSourceDates
from domain.enums import AssetType
from domain.relevant_start_date_resolver import resolve_relevant_start_date


def test_pension_uses_first_contribution_when_available() -> None:
    source_dates = AssetSourceDates(
        account_opened_date=date(2020, 1, 1),
        first_contribution_date=date(2020, 2, 1),
    )

    result = resolve_relevant_start_date(AssetType.PENSION, source_dates)

    assert result == date(2020, 2, 1)


def test_pension_falls_back_to_account_opened_when_no_first_contribution() -> None:
    source_dates = AssetSourceDates(
        account_opened_date=date(2020, 1, 1),
        first_contribution_date=None,
    )

    result = resolve_relevant_start_date(AssetType.PENSION, source_dates)

    assert result == date(2020, 1, 1)


def test_pension_returns_none_when_no_relevant_dates() -> None:
    source_dates = AssetSourceDates(
        account_opened_date=None,
        first_contribution_date=None,
    )

    result = resolve_relevant_start_date(AssetType.PENSION, source_dates)

    assert result is None


def test_study_fund_follows_same_rules_as_pension() -> None:
    source_dates = AssetSourceDates(
        account_opened_date=date(2020, 1, 1),
        first_contribution_date=date(2020, 3, 1),
    )

    result = resolve_relevant_start_date(AssetType.STUDY_FUND, source_dates)

    assert result == date(2020, 3, 1)


def test_budgetary_pension_uses_service_start_date() -> None:
    source_dates = AssetSourceDates(service_start_date=date(2010, 5, 1))

    result = resolve_relevant_start_date(AssetType.BUDGETARY_PENSION, source_dates)

    assert result == date(2010, 5, 1)


def test_budgetary_pension_returns_none_when_service_start_missing() -> None:
    source_dates = AssetSourceDates(service_start_date=None)

    result = resolve_relevant_start_date(AssetType.BUDGETARY_PENSION, source_dates)

    assert result is None


def test_rsu_uses_grant_date() -> None:
    source_dates = AssetSourceDates(grant_date=date(2021, 7, 1))

    result = resolve_relevant_start_date(AssetType.RSU, source_dates)

    assert result == date(2021, 7, 1)


def test_stock_options_uses_grant_date() -> None:
    source_dates = AssetSourceDates(grant_date=date(2022, 1, 15))

    result = resolve_relevant_start_date(AssetType.STOCK_OPTIONS, source_dates)

    assert result == date(2022, 1, 15)


def test_equity_compensation_returns_none_when_grant_date_missing() -> None:
    source_dates = AssetSourceDates(grant_date=None)

    assert resolve_relevant_start_date(AssetType.RSU, source_dates) is None
    assert resolve_relevant_start_date(AssetType.STOCK_OPTIONS, source_dates) is None


def test_other_asset_types_and_bank_account_behavior() -> None:
    source_dates = AssetSourceDates(
        account_opened_date=date(2020, 1, 1),
        first_contribution_date=date(2020, 2, 1),
        service_start_date=date(2010, 5, 1),
        grant_date=date(2021, 7, 1),
    )

    assert resolve_relevant_start_date(AssetType.BANK_ACCOUNT, source_dates) == date(
        2020, 1, 1
    )
    assert resolve_relevant_start_date(AssetType.LEGAL_DOCUMENT, source_dates) is None


