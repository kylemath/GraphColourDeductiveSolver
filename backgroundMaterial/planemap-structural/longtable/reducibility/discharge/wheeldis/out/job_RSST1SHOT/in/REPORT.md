# W6r RSST-FP: exhaustive realisation-level check of the RSST fixed point on d7/d8

(Saved by the lead from W6r's hand-back, 10 Nov 2026 ~11:15Z. MD5SUMS 9aa388b9; this REPORT.md is not in it. Spec RSSTFP_SPEC.md 33338de6. [P], one engine.)

**Result.** With all 633 RSST configurations as kills, every d7/d8 row in the four sets ends at charge ≤ 0 in every filling.

**Method.**
- All 71 parts as written, with the K3gB5n per-filling domains.
- Exhaustive enumeration by relevant-private grouping with exact multiplicities: 1,243 rows, 541.6M fillings, no row left undone.
- Links containing a 9 are handled exactly: the code asserts that no middle letter is read.

| set | rows (d7/d8) | rows positive, domains only | max (RSST units) | rows positive, 582 proved | rows positive, all 633 |
|---|---|---|---|---|---|
| A binder | 162 (56/106) | 38 | 5 | 0 | 0 |
| B GS16 | 495 (369/126) | 98 | 6 | 4 | 0 |
| C pos6-alive | 281 (281/0) | 25 | 1 | 0 | 0 |
| T ST-102 tneg 4a181f67 | 305 (48/257) | 35 | 5 | 1 | 0 |

**Rows that need the "none" configurations.** Five rows are killed only by one of three "none" configurations: 2.126, 124.1324817 and 128.1324802. All 51 "none" configurations satisfy Gonthier's valid_contract verbatim (W6b, round16/round9_rsstnone/).
- B 8 76576756/65555556 (2.126)
- T 8 56765767/56655555 (2.126)
- B 7 8557766/7565755 (124.1324817 and 2.126)
- B 7 8565766/5557657 and 5557656 (128.1324802)

**Coverage.** 98 configurations cover the positive fillings: 90 proved and 8 "none".

**Findings at other degrees (in the spec):**
- **d ≥ 9:**
  - The exact per-hub maximum into a 9+ is 6 from hubs of degree 5, 6 or 7, and 4 from degree 8.
  - The Karp mean is −4, giving UB(d) = 60 − 4d, which is attained by the all-5 filling.
  - So with no kills, every d ≥ 15 passes. d = 9..14 need a joint DP with kills.
- **d = 5, 6:** random 2-balls reach a high of 10 and 16, so kills are needed at both degrees.

**Caveats for the Studio** (spec §7):
- The kill model treats the window graph as induced. W6r extended rsst_rows' internal-6-connectivity argument from {u, w, s} to the privates without re-proving it.
- These four sets are our row sets, not the full world of d7/d8 2-balls. The one-shot has to cover every label.

**Files.**
- `RSSTFP_SPEC.md`.
- `results/`: summary_fp.tsv/txt, positive_rows.tsv, covering_configs.tsv, fp_{A,B,C,T}.json/tsv, tail9.json, all5_d9plus.json, test_vectors.json (8 d7/d8 rows), test_vectors_ext.json (d = 5, 6, 9, 10, 11; seed 20261110).
- `code/` and `inputs/` (including parts71.txt).
