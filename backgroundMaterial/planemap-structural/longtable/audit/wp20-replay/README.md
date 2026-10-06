# WP20 P1: audit replay package (ready before any P1 output was read)

Plan: `../WP20-P1-audit-replay-plan.md` (commit `003c289`). This package is a third implementation. It imports and reads neither `d1_confirm.py` nor `d1_check.py`.

- **`wp20_audit.py`** recomputes every per-vertex field, and the witness states, for a graph, from the declaration and the output format.
- **`compare_p1.py`** runs plan steps 1–7 on a merged phase output:
  - bindings;
  - merge integrity;
  - accounting identities;
  - a recount of the flagged graphs, the audit's 1% sample (`AUDIT-WP20-P1-`) and the declared 2% sample (`WP20-`);
  - an exact field and witness-set comparison.

## Validation before P1

- **Declaration regressions:**
  - order 16: 0 SEP-bad;
  - order 17: 8 SEP-bad, 4 on graph 0 and 4 on graph 1, all depth 1, 32 locked classes;
  - order 18: 0 SEP-bad.

  All reproduced (`tests/recount-order17.jsonl`).
- **Dry run against the producer's committed `wp20/regression-m5-17.json`:** REPLAY AGREES on every field and on the witness sets (`tests/dryrun-regression17-compare.json`).
- **Negative control:** one count and one witness were corrupted. Both are caught (`tests/negative-control-compare.json`).

## Cost (revised)

- About 8 s per order-25 graph, timed on input graphs 0, 1, 5000, 12345 and 25380, which are inputs only.
- The audit and declared samples together are about 760 graphs plus the flagged ones, so about 1.7 CPU-hours: roughly 50 minutes on 2 workers.
- This is more than the plan's estimate of "well under 1 CPU-hour". The estimate was wrong; the method is unchanged.
