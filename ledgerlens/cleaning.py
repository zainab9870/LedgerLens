"""
cleaning.py
Turn raw CSV rows (all strings, some broken) into clean Transaction records,
and collect the broken ones with a reason instead of crashing.
Concepts: functions, try/except/else/finally, raise, custom exceptions,
          while loop, lists, break/continue.
"""

import csv
from datetime import datetime

from .exceptions import (
    InvalidAmountError,
    InvalidDateError,
    MissingFieldError,
    LedgerLensError,
)
from .models import Transaction


def parse_amount(raw):
    """Convert a raw string like '12.50' to a positive float.
    Raise InvalidAmountError if raw is blank, not a number, or <= 0.
    """
    if not raw.strip():
        raise InvalidAmountError("Amount is blank.")
    try:
        value = float(raw)
    except ValueError:
        raise InvalidAmountError(f"Invalid amount: {raw}") from None
    if value <= 0:
        raise InvalidAmountError(f"Amount must be positive: {raw}")
    return value


def parse_date(raw):
    """Convert 'YYYY-MM-DD' to a datetime.date.
    Raise InvalidDateError if it isn't a real date.
    """
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        raise InvalidDateError(f"bad date: {raw}") from None


def clean_record(row):
    """Turn ONE raw dict (from csv.DictReader) into a Transaction.

    - customer_id blank -> raise MissingFieldError
    - use parse_amount and parse_date for the other fields
    Let the exceptions propagate; the caller decides what to do with them.
    """
    if not row["customer_id"].strip():
        raise MissingFieldError("customer_id is blank")
    return Transaction(
        txn_id=row["txn_id"],
        customer_id=row["customer_id"],
        amount=parse_amount(row["amount"]),
        date=parse_date(row["date"]),
        channel=row["channel"],
        category=row["category"],
    )


def load_transactions(path, max_retries=3):
    """Read the CSV at `path`. Return (clean, rejected, duplicates_removed).

    clean:    list of Transaction
    rejected: list of (raw_row, reason_string)
    - Skip (don't reject) rows whose txn_id was already seen: use a SET of
      seen ids and `continue`.
    - Wrap file opening in a while loop that retries up to max_retries on
      FileNotFoundError (then raises). Use try/except/else/finally.
    """

    clean = []
    rejected = []
    duplicates_removed = 0
    seen = set()

    attempt = 0
    while attempt < max_retries:
        try:
            f = open(path, newline="")
        except FileNotFoundError:
            attempt += 1
            if attempt >= max_retries:
                raise
        else:
            break

    try:
        reader = csv.DictReader(f)
        for row in reader:
            if row["txn_id"] in seen:
                duplicates_removed += 1
                continue
            seen.add(row["txn_id"])
            try:
                txn = clean_record(row)
            except LedgerLensError as err:
                rejected.append((row, str(err)))
            else:
                clean.append(txn)

    finally:
        f.close()

    return clean, rejected, duplicates_removed
