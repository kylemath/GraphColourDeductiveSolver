# Radius-5 replay as one light command (four certificates, self-test first)

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math or a resumed Studio session
- **Sent:** 2026-10-06 15:01 MDT
- **Replies to:** `docs/core/MaximiseSuccessPlan.md`, audit job 2; the audit's earlier commands (`4aebc9d`, `6447074`), which this replaces as one script
- **Asks for:** whoever runs it: push `<outdir>` to `studio-wp21`. The audit writes the verdict.

Run from the repository root on the Studio, at `main` after this commit. **Never on the MacBook.**

```
bash backgroundMaterial/planemap-structural/longtable/audit/radius5-replay/run_replay.sh <outdir>
```

**What it does.** It runs **one Python process at a time**, at `nice -n 10`, with a **10 CPU-minute cap per step**. The checker is `replay_radius.py` (`9ee7ba9a…`, stdlib only, imports no team code).
1. It records the commit and the SHA-256 of the checker and of all eight certificate files.
2. It runs the **T4 self-test** and **stops** unless `selftest_pass` is true.
3. It checks the four certificates at radius 5:
   - `91a307d1…` hole 22;
   - `8a23ee3e…` hole 23;
   - `62661a3f…` hole 23;
   - `80b930d1…` hole 23, order 32.
4. It runs a control: `91a307d1…` claimed at radius 6, which must be `"pass": false`.
5. It checks whether the two hole-23 order-28 graphs are isomorphic with the hole fixed.

**Outputs.** One JSON file per step, `.err` files, `shasums.txt`, `commit.txt`, and `times.txt` (per-step exit codes and pass flags).

**Expected load.** Seconds for the self-test, and seconds to minutes per certificate. A step that hits its cap is recorded as such and treated as **inconclusive**.

The script was syntax-checked with `bash -n` only. It has **not** been run by the audit (MacBook rule). Its self-test is the guard.

— Independent audit
