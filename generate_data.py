"""
generate_data.py
Creates a deliberately DIRTY synthetic bank-transaction file, plus a
ground_truth.json that records exactly which problems were planted.
You will use ground_truth.json to check that LedgerLens finds them.

Run:  python generate_data.py
Out:  data/transactions_raw.csv, data/ground_truth.json
"""
import csv
import json
import random
from datetime import date, timedelta

# ---- Settings (change these to experiment) -------------------------------
SEED = 42              # same seed -> same data every run (reproducible)
N_CUSTOMERS = 60
N_CLEAN = 1000         # how many normal transactions to create
START = date(2026, 1, 1)
DAYS = 180             # transactions are spread over this many days
CHANNELS = ["card", "transfer", "atm", "wallet"]
CATEGORIES = ["groceries", "transport", "dining", "utilities", "shopping", "travel"]
FIELDS = ["txn_id", "customer_id", "date", "amount", "channel", "category"]

random.seed(SEED)  # fix the random number sequence


def make_normal_row(i):
    """Build one realistic-looking transaction as a dict. i is its index."""
    # lognormvariate gives many small amounts and a few bigger ones,
    # which is how real spending behaves. Median is roughly 33.
    amount = round(min(random.lognormvariate(3.5, 0.8), 500), 2)
    return {
        "txn_id": f"T{i:05d}",                                   # T00001 ...
        "customer_id": f"C{random.randint(1, N_CUSTOMERS):03d}", # C001 ...
        "date": (START + timedelta(days=random.randint(0, DAYS - 1))).isoformat(),
        "amount": f"{amount:.2f}",   # stored as TEXT, like a real CSV
        "channel": random.choice(CHANNELS),
        "category": random.choice(CATEGORIES),
    }


def main():
    truth = {"invalid_rows": {}, "duplicates": [], "outliers": [], "burst_customers": []}

    # 1. Normal rows ---------------------------------------------------------
    rows = [make_normal_row(i) for i in range(1, N_CLEAN + 1)]

    # 2. Pick DISTINCT rows to damage so one row never gets two problems ------
    #    random.sample(range(...), k) returns k unique indices.
    chosen = random.sample(range(len(rows)), 5 + 12)
    outlier_idx, invalid_idx = chosen[:5], chosen[5:]

    # 3. Plant outliers: absurdly large amounts ------------------------------
    for idx in outlier_idx:
        rows[idx]["amount"] = f"{random.uniform(8000, 20000):.2f}"
        truth["outliers"].append(rows[idx]["txn_id"])

    # 4. Plant invalid rows: cycle through 5 kinds of corruption -------------
    kinds = ["missing_amount", "negative_amount", "text_amount", "bad_date", "missing_customer"]
    for n, idx in enumerate(invalid_idx):
        kind = kinds[n % len(kinds)]  # % wraps around so kinds repeat
        row = rows[idx]
        if kind == "missing_amount":
            row["amount"] = ""
        elif kind == "negative_amount":
            row["amount"] = f"-{random.uniform(5, 200):.2f}"
        elif kind == "text_amount":
            row["amount"] = "12O.50"          # letter O instead of zero!
        elif kind == "bad_date":
            row["date"] = "2026-13-45"        # month 13 does not exist
        elif kind == "missing_customer":
            row["customer_id"] = ""
        truth["invalid_rows"][row["txn_id"]] = kind

    # 5. Plant exact duplicates (same txn_id appears twice) ------------------
    clean_ids = [r for k, r in enumerate(rows) if k not in chosen]
    for original in random.sample(clean_ids, 10):
        rows.append(dict(original))           # dict(...) makes a copy
        truth["duplicates"].append(original["txn_id"])

    # 6. Plant velocity bursts: 1 customer, 8 small txns on the SAME day -----
    next_id = N_CLEAN + 1
    for cust in random.sample(range(1, N_CUSTOMERS + 1), 2):
        cust_id = f"C{cust:03d}"
        burst_day = (START + timedelta(days=random.randint(0, DAYS - 1))).isoformat()
        for _ in range(8):
            rows.append({
                "txn_id": f"T{next_id:05d}",
                "customer_id": cust_id,
                "date": burst_day,
                "amount": f"{random.uniform(5, 40):.2f}",
                "channel": "card",
                "category": "shopping",
            })
            next_id += 1
        truth["burst_customers"].append(cust_id)

    # 7. Shuffle so problems are not conveniently grouped, then write --------
    random.shuffle(rows)
    with open("data/transactions_raw.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    with open("data/ground_truth.json", "w") as f:
        json.dump(truth, f, indent=2)

    print(f"Wrote {len(rows)} rows to data/transactions_raw.csv")
    print(f"Planted: {len(truth['invalid_rows'])} invalid, {len(truth['duplicates'])} duplicates, "
          f"{len(truth['outliers'])} outliers, {len(truth['burst_customers'])} burst customers")


if __name__ == "__main__":
    main()
