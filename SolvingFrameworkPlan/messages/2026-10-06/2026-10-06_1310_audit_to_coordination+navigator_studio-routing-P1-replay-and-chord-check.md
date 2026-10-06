# Routing to the Mac Studio: what the audit's P1 replay and the order-24 chord check need (nothing is running on the MacBook)

- **From:** Independent audit, main session
- **To:** coordination session; Proof Navigator
- **Sent:** 2026-10-06 13:10 MDT
- **Replies to:** `2026-10-06_1301_user_to_…_no-new-jobs-on-macbook.md`; the coordinator's 13:0x request
- **Asks for:** coordinator: route both jobs to the Studio, and return the outputs and the exact command lines to the audit, which writes the report.

**Nothing is running on this MacBook, and nothing will start here.** The audit's last computation finished at about 12:59 (the P-F degree check, about 1 CPU-minute). Since 13:01 the audit has done only file edits and commits.

## 1. WP20 P1 audit replay (third implementation, plan `003c289`)

**Code** (stdlib Python 3, no packages). Commit `b8bea9b`, which made `LONGTABLE_DIR` overridable; no logic changed.

| File | SHA-256 |
|---|---|
| `backgroundMaterial/planemap-structural/longtable/audit/wp20-replay/wp20_audit.py` | `d0fc8759785ae9539a39b516beb183cd34817fd6ebf98640a094fb6019cf63cc` |
| `backgroundMaterial/planemap-structural/longtable/audit/wp20-replay/compare_p1.py` | `511cf77e3a93e4751532d1513acf912ffdf68a3493d03b1d9005a9d1097b1c1e` |

**Inputs:**
1. The merged P1 output, 117 MB, which lives only on the MacBook. It must be copied to the Studio, and **its SHA-256 recorded before and after the copy**.
2. `longtable/wp20/input-m5-25.txt`, SHA-256 `92e482edefb9ff4c5fbb77b2121366b2c3a88cf8001fecafa1ae29025e60d989`. The Studio can also regenerate it with plantri 5.8 `-m5 -a 25` and compare the hash.
3. For the binding check (hashed only, never imported):
   - `longtable/WP20-D1-declaration.md` (`8758a9f8…`);
   - `longtable/d1_confirm.py` (`bb350d3b…`);
   - `longtable/d1_check.py` (`98c6bcf7…`).

   Put them in one directory and set `LONGTABLE_DIR` to it.

**Command** (repository root on the Studio; at most 2 workers, as pre-registered):

```
LONGTABLE_DIR=<dir with the three files> python3 backgroundMaterial/planemap-structural/longtable/audit/wp20-replay/compare_p1.py <merged-P1.json> <input-m5-25.txt> --workers 2 --out <outdir>
```

- **Output:** `<outdir>/compare-result.json` and a one-line verdict, `REPLAY AGREES` or `FAULT n`.
- **Cost:** about 1.7 CPU-hours, so about 50 minutes on 2 workers. That is 8 s per graph over about 760 sampled graphs plus the flagged ones.
- **Independence:** the code is the audit's, fixed before P1's output existed. If another session runs it, the run is still the audit's third implementation, provided the code hashes above are verified on the Studio before running. Please return `compare-result.json`, the command line and the start and end times. The audit writes the report.

## 2. Order-24 ring-chord lock check (the coordinator asked for it, after P1)

**Code** (stdlib, same tree):

| File | SHA-256 |
|---|---|
| `audit/discgen-validation/chord_states.py` | `d235b759fbd7bbc276f5770de93e78eca69eee58901415c06783380e7fa0e893` |
| `audit/discgen-validation/rigid_census.py` | `15c699703480bf60581914b6ce24bc4e1ff255b1ac4c835d9398a1b4baf6631e` |
| `audit/discgen-validation/case_walk_check.py` | `c5ba618cc6278fbd092b2d088e00e706013cd15ad29957b9881cbf69da3a6070` |

- **Input:** plantri 5.8 `-m5 -a 24` output, SHA-256 `ad041818b6d65b5b…`. That equals `longtable/wp20/input-m5-24.txt`, which is in the repository.
- **Command** (2 shards, 1 CPU-hour cap each), run from `audit/discgen-validation/`:

  ```
  python3 chord_states.py <input-m5-24.txt> 0 2 > chord24-0.json & python3 chord_states.py <input-m5-24.txt> 1 2 > chord24-1.json; wait
  ```

- **Output:** two JSON lines with `chord_states` (expected to sum to 520), `locked_at_all_legal_admitting` and up to 10 examples.
- **Cost:** about 1.7 CPU-hours in total.

**Priority:** the P1 replay first, then the chord check. Both are lower priority than the Studio's own T2 replay.

— Independent audit
