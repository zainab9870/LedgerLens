"""Run with:  pytest -v
These FAIL until you implement cleaning.py. That's the point:
make them pass one at a time."""
import datetime

import pytest

from ledgerlens.cleaning import clean_record, parse_amount, parse_date
from ledgerlens.exceptions import InvalidAmountError, InvalidDateError, MissingFieldError


def test_parse_amount_valid():
    assert parse_amount("12.50") == 12.5


@pytest.mark.parametrize("bad", ["", "12O.50", "-5.00", "0"])
def test_parse_amount_invalid(bad):
    with pytest.raises(InvalidAmountError):
        parse_amount(bad)


def test_parse_date_valid():
    assert parse_date("2026-03-01") == datetime.date(2026, 3, 1)


def test_parse_date_invalid():
    with pytest.raises(InvalidDateError):
        parse_date("2026-13-45")


def test_clean_record_missing_customer():
    row = {"txn_id": "T1", "customer_id": "", "date": "2026-03-01",
           "amount": "10.00", "channel": "card", "category": "dining"}
    with pytest.raises(MissingFieldError):
        clean_record(row)
