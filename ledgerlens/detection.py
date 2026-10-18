"""
detection.py
Find suspicious behaviour in a list of clean Transactions.
Concepts: dicts, sets, slicing, lambda, statistics module, keyword args.
"""

import statistics


def build_profiles(transactions):
    """Return {customer_id: {"total": float, "count": int, "channels": set}}."""

    profiles = {}
    for t in transactions:
        p = profiles.setdefault(
            t.customer_id, {"total": 0.0, "count": 0, "channels": set()}
        )
        p["total"] += t.amount
        p["count"] += 1
        p["channels"].add(t.channel)
    return profiles


def find_outliers(transactions, z_threshold=3.0):
    """Return a list of Transactions whose amount is unusually large.

    z-score = (amount - mean) / stdev. Flag amounts with z > z_threshold.
    Use statistics.mean and statistics.stdev.
    """
    amount = [t.amount for t in transactions]
    mean = statistics.mean(amount)
    stdev = statistics.stdev(amount)
    return [t for t in transactions if (t.amount - mean) / stdev > z_threshold]


def find_velocity_bursts(transactions, max_per_day=5):
    """Return {customer_id: [dates]} for customers with more than
    max_per_day transactions on a single day."""

    counts = {}
    for t in transactions:
        key = (t.customer_id, t.date)
        counts[key] = counts.get(key, 0) + 1

    bursts = {}
    for (cust, day), n in counts.items():
        if n > max_per_day:
            bursts.setdefault(cust, []).append(day)
    return bursts


def channel_overlap(transactions):
    """Return a dict of SETS of customer_ids:
    {"card_and_transfer": ..., "card_only": ..., "transfer_only": ...}"""
    card = {t.customer_id for t in transactions if t.channel == "card"}
    transfer = {t.customer_id for t in transactions if t.channel == "transfer"}
    return {
        "card_and_transfer": card & transfer,
        "card_only": card - transfer,
        "transfer_only": transfer - card,
    }


def top_customers(profiles, n=5):
    """Return the n customers with the highest total spend."""
    ranked = sorted(profiles.items(), key=lambda item: item[1]["total"], reverse=True)
    return ranked[:n]
