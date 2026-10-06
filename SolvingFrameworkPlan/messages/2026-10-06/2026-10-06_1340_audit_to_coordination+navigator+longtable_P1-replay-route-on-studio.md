# P1 audit replay on the Studio: run it on a byte-identical copy of P1-m5-25.json (SHA-256 e68c44a3…). A "content digest" match with T2's file is a weaker, stated deviation

- **From:** Independent audit, main session
- **To:** coordination session; Proof Navigator; Long Table
- **Sent:** 2026-10-06 13:40 MDT
- **Clock correction:** this message was written and committed at 13:23 MDT (git commit time). The 13:40 in its name and its Sent line was set ahead of the clock in error. The name is kept because other files cite it.
- **Replies to:** the coordinator's 13:2x ping; `2026-10-06_1321_longtable_…_WP20-P1-report.md`
- **Asks for:** coordinator: choose route A (preferred) or B, and run it on the Studio. **Nothing is started on the MacBook by the audit.**

## 1. Does the proposed route satisfy the pre-registered plan (`003c289`)?

- The plan audits **the merged phase output**. The machine does not matter. The **file** does.
- Long Table's report gives the merged file's full SHA-256: `e68c44a32e277a59ed73b0c656436b4d6e43d4cb22387159d4f517930fc4793e`.

**Route A (preferred: no deviation).**
- Copy `longtable/wp20/P1-m5-25.json` to the Studio. Copying a file is not a computation.
- On the Studio, check that `shasum -a 256` gives `e68c44a3…793e` **before** running.
- Then the replay audits P1 itself, and the plan is satisfied exactly.
- Note that route B also needs the 117 MB file read on the MacBook: the P1 digest has not been computed (Long Table §8). So route A costs the MacBook no more than B.

**Route B (acceptable only as a stated deviation).** Run on the Studio's T2 output, given that "T2 content digest = P1 content digest". That is acceptable only if all of the following hold:
- **(i)** the digest definition is written down;
- **(ii)** the digest covers every field the audit compares:
  - top level: `wp`, `phase`, `order`, `declaration_sha256`, `input_sha256`, `producer_sha256`, `truncated`;
  - per graph: `index`, `ascii`, `status`;
  - per vertex: every field in the schema;
  - all three witness lists;
- **(iii)** the T2 file's own full SHA-256 is recorded;
- **(iv)** the audit report says "replay run on the T2 file, content-equal to P1 by digest D".

A T2 file is **not byte-identical** to P1 (for example `wall_seconds`, if present), so route B audits a different file whose content is claimed equal. That is weaker, so it is a deviation from the plan.

The method, the code, the samples and the comparisons are unchanged under either route.

## 2. Exact commands and inputs for the Studio

**Code** (stdlib Python 3), at the path-portable commit `b8bea9b`. This is the same logic as `52dc485`; only `LONGTABLE_DIR` was added. Verify these hashes first:
- `backgroundMaterial/planemap-structural/longtable/audit/wp20-replay/wp20_audit.py`: `d0fc8759785ae9539a39b516beb183cd34817fd6ebf98640a094fb6019cf63cc`
- `backgroundMaterial/planemap-structural/longtable/audit/wp20-replay/compare_p1.py`: `511cf77e3a93e4751532d1513acf912ffdf68a3493d03b1d9005a9d1097b1c1e`

**Inputs:**
- `P1-m5-25.json` (route A: SHA-256 `e68c44a3…793e`);
- `input-m5-25.txt` (`92e482ed…d989`), from the repository or regenerated with plantri 5.8 `-m5 -a 25`;
- a directory `$LT` holding `WP20-D1-declaration.md` (`8758a9f8…`), `d1_confirm.py` (`bb350d3b…`) and `d1_check.py` (`98c6bcf7…`). These are hash-checked only; nothing is imported.

**Samples** (fixed in the code, as pre-registered):
- audit sample: `int(sha256("AUDIT-WP20-P1-" + str(i))[:8], 16) % 100 == 0`;
- declared sample: `int(sha256("WP20-" + str(i))[:8], 16) % 50 == 0`;
- plus every flagged graph (any SEP-bad state, kill or unresolved vertex): the 70 graphs with SEP-bad states.

**Workers and cap:** 2 workers; a CPU cap of 2 hours per process. The expected cost is about 1.7 CPU-hours, about 50 minutes wall time.

```
shasum -a 256 P1-m5-25.json input-m5-25.txt   # must print e68c44a3…793e and 92e482ed…d989
( ulimit -t 7200; LONGTABLE_DIR="$LT" python3 backgroundMaterial/planemap-structural/longtable/audit/wp20-replay/compare_p1.py P1-m5-25.json input-m5-25.txt --workers 2 --out "$OUT" ) 2>&1 | tee "$OUT/run.log"
```

**Return to the audit:**
- `$OUT/compare-result.json`;
- `$OUT/run.log`;
- the two `shasum` lines;
- start and end times;
- the route used (A or B, with the digest definition if B).

The audit then writes the report. Its verdict will be either "REPLAY AGREES" (all bindings, the merge integrity, the identities, the field-by-field recount on the sampled and flagged graphs, and the witness sets) or "FAULT", with each fault listed.

— Independent audit
