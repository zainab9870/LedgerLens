# LedgerLens Audit Report

## Summary Counts
- Clean records: 1004
- Rejected records: 12
- Duplicates removed: 10
- Outliers flagged: 5

## Rejected record
- T00676: Amount is blank.
- T00992: Amount is blank.
- T00214: Amount must be positive: -60.59
- T00816: Amount must be positive: -89.76
- T00055: bad date: 2026-13-45
- T00865: customer_id is blank
- T00116: Amount is blank.
- T00284: Invalid amount: 12O.50
- T00702: bad date: 2026-13-45
- T00934: Amount must be positive: -70.19
- T00153: Invalid amount: 12O.50
- T00199: customer_id is blank

## Outliers
- T00225: C005 on 2026-03-21, 10115.89
- T00789: C039 on 2026-02-09, 8517.39
- T00520: C057 on 2026-06-07, 13692.95
- T00476: C032 on 2026-05-26, 16041.71
- T00642: C045 on 2026-03-17, 15738.33

## Velocity bursts
- C012: 2026-01-08
- C011: 2026-03-25

## Channel overlap
- card_and_transfer: C023, C060, C021, C017, C042, C041, C056, C025, C030, C020, C002, C014, C050, C059, C005, C032, C024, C029, C058, C011, C046, C040, C018, C026, C054, C051, C055, C015, C048, C019, C007, C038, C035, C036, C016, C045, C006, C049, C037, C008, C027, C044, C039, C001, C034, C010, C043, C013, C031, C004, C033, C003, C057, C012, C052, C053, C009, C047, C022
- card_only: C028
- transfer_only: 

## Top customers
- C045: 16843.68 across 28 transactions
- C032: 16414.19 across 8 transactions
- C057: 14229.29 across 14 transactions
- C005: 11057.66 across 17 transactions
- C039: 9956.22 across 24 transactions
