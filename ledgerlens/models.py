"""The immutable record every clean transaction becomes."""
from collections import namedtuple

# namedtuple = a tuple whose items have names: txn.amount instead of txn[3].
# Immutable on purpose: once a record is cleaned, nothing should alter it.
Transaction = namedtuple(
    "Transaction",
    ["txn_id", "customer_id", "date", "amount", "channel", "category"],
)
# `date` should hold a datetime.date object and `amount` a float after cleaning.
