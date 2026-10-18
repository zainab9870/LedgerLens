"""Command-line entry point.  Usage:  python main.py data/transactions_raw.csv"""

import argparse

from ledgerlens.cleaning import load_transactions
from ledgerlens.detection import (
    build_profiles,
    find_outliers,
    find_velocity_bursts,
    channel_overlap,
    top_customers,
)
from ledgerlens.reporting import write_report


def main():
    parser = argparse.ArgumentParser(description="LedgerLens transaction auditor")
    parser.add_argument("path", help="path to raw transactions CSV")
    parser.add_argument(
        "--z", type=float, default=3.0, help="outlier z-score threshold"
    )
    parser.add_argument("--max-per-day", type=int, default=5, help="velocity limit")
    args = parser.parse_args()

    clean, rejected, dups = load_transactions(args.path)
    profiles = build_profiles(clean)
    outliers = find_outliers(clean, z_threshold=args.z)
    bursts = find_velocity_bursts(clean, max_per_day=args.max_per_day)
    overlap = channel_overlap(clean)
    top = top_customers(profiles)
    write_report("report.md", clean, rejected, dups, outliers, bursts, overlap, top)
    print(
        f"Done: {len(clean)} clean, {len(rejected)} rejected, {len(outliers)} outliers"
    )
    print(f"Auditing {args.path} ...")


if __name__ == "__main__":
    main()
