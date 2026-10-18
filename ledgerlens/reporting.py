"""reporting.py
Turn results into a Markdown report you can commit to the repo.
Concepts: f-strings, loops, file I/O (with open(...)), functions.
"""


def write_report(
    path, clean, rejected, duplicates_removed, outliers, bursts, overlap, top
):
    """Write a Markdown audit report to `path`.

    Suggested sections: Summary counts, Rejected records (with reasons),
    Outliers, Velocity bursts, Channel overlap, Top customers.
    """
    with open(path, "w") as f:
        f.write("# LedgerLens Audit Report\n\n")
        f.write("## Summary Counts\n")
        f.write(f"- Clean records: {len(clean)}\n")
        f.write(f"- Rejected records: {len(rejected)}\n")
        f.write(f"- Duplicates removed: {duplicates_removed}\n")
        f.write(f"- Outliers flagged: {len(outliers)}\n")

        f.write("\n## Rejected record\n")
        for row, reason in rejected:
            f.write(f"- {row['txn_id']}: {reason}\n")

        f.write("\n## Outliers\n")
        for t in outliers:
            f.write(f"- {t.txn_id}: {t.customer_id} on {t.date}, {t.amount:.2f}\n")

        f.write("\n## Velocity bursts\n")
        for cust, dates in bursts.items():
            f.write(f"- {cust}: {', '.join(str(d) for d in dates)}\n")

        f.write("\n## Channel overlap\n")
        for key, customers in overlap.items():
            f.write(f"- {key}: {', '.join(customers)}\n")

        f.write("\n## Top customers\n")
        for cust, profile in top:
            f.write(
                f"- {cust}: {profile['total']:.2f} across {profile['count']} transactions\n"
            )
