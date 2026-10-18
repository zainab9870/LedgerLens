"""Custom exceptions. A shared base class lets you catch ANY LedgerLens
problem with one `except LedgerLensError`, or a specific one when you care."""


class LedgerLensError(Exception):
    """Base class for all project-specific errors."""


class MissingFieldError(LedgerLensError):
    """A required field (e.g. customer_id) is blank."""


class InvalidAmountError(LedgerLensError):
    """Amount is blank, non-numeric, or not positive."""


class InvalidDateError(LedgerLensError):
    """Date is not a real ISO date (YYYY-MM-DD)."""
