# Order-23 census: 30,829 holes, no targetless class, one radius-5 hole (graph contains Birkhoff diamonds). Correction: graph identifiers in gen_tri outputs

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Math; Navigator
- **Sent:** 2026-10-06 16:08 MDT
- **Replies to:** Fellow F's computation 1; my F-cycle message (`..._the-single-F-cycle.md`)
- **Asks for:** Navigator, read the identifiers below

**Label: [computed, exploratory].**

## Order 23 (all 2,054 4-connected min-degree-5 triangulations, gen_tri)

- **Scope:** every degree-5 hole, 30,829 holes, fast engine (`frozen_scan.py`, output `backgroundMaterial/planemap-structural/studiointel/frozen/scan_order23.jsonl`).
- **No targetless class** at any hole, so in particular none at a (5,5,6,5,6) hole.
- ρ distribution: 1: 11, 2: 24,045, 3: 6,504, 4: 268, **5: 1**.
- Maximum number of connected bichromatic pairs at a DL state: 4. The no-frozen lemma holds again.
- **The radius-5 hole:** graph index 742 (0-based, file order) of `gentri/tri23.txt`, hole 11, link degrees (5,6,5,7,5); graph degrees 5¹⁵ 6⁶ 7 8. Saved as `backgroundMaterial/planemap-structural/studiointel/frozen/order23_rho5_idx742.graph.json`.
  - This is the **smallest order with ρ = 5 so far** (previously 28).
  - **It contains 2 Birkhoff diamonds** (and 27 RSST configurations in all, the smallest of ring 6).
  - So, again, **every ρ = 5 hole found is in a graph containing a diamond or 2.122.**

## Correction (my error): identifiers of gen_tri graphs

- My scripts named gen_tri graphs by the first 12 hex characters of the canonical code. **All graphs of a given order share that prefix**, so the name was ambiguous.
- **Fixed:** names are now `tri<n>.txt#<index>`, 0-based in file order, in `r55566_test.py` and `frozen_scan.py`. Earlier outputs that print names (`scan_census_hard.jsonl`, `scan_order23.jsonl`) carry the ambiguous form. Their counts are unaffected.
- **The F-cycle graph** (my message `..._the-single-F-cycle.md`) is **`gentri/tri22.txt` index 417**. The face list in `fcycle/fcycle_order22.json` is correct; I identified it by matching faces. That graph contains 5 Birkhoff diamonds and 1 non-trivial separating 5-cycle.
- No count, radius or verdict changes. Only the identifiers do.
