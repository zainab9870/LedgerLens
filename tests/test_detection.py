"""Uses the ground truth file from generate_data.py to check your detectors.
Run `python generate_data.py` first."""
import json

from ledgerlens.cleaning import load_transactions
from ledgerlens.detection import find_outliers, find_velocity_bursts

PATH = "data/transactions_raw.csv"


def test_outliers_found():
    truth = json.load(open("data/ground_truth.json"))
    clean, _, _ = load_transactions(PATH)
    found = {t.txn_id for t in find_outliers(clean)}
    assert set(truth["outliers"]) <= found   # every planted outlier was caught


def test_bursts_found():
    truth = json.load(open("data/ground_truth.json"))
    clean, _, _ = load_transactions(PATH)
    assert set(truth["burst_customers"]) <= set(find_velocity_bursts(clean))
