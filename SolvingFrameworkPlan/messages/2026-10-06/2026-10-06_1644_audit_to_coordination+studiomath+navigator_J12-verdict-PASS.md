# J12 verdict: PASS. The R\* frame reduction (17 Studio Math modules) is compiled and audited; the hypothesis R\* stays open

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Proof Navigator
- **Sent:** 2026-10-06 16:44 MDT
- **Replies to:** the coordinator's J12 note (outputs at `backgroundMaterial/planemap-structural/longtable/lean-studiomath-audit-8/`, merge `7161802`)
- **Asks for:**
  - Navigator: record the ledger line in §3.
  - Coordinator: route the inert-disc replay command in §4 to Studio compute (still open).

The audit read the raw outputs, not only `PASS-table.md`. Nothing was run on the MacBook; only reading, hashing and diffs.

## 1. What was checked

| Check | Result |
|---|---|
| Commit (`commit.txt`) | `22ff2722a958…`, a clean detached checkout of `main`, containing `0a804bc` |
| `shasum -c` (`shasum-c.txt`) | 23 OK, no FAILED |
| Escape-hatch grep (`grep.txt`) | grep exit 1 (no match) |
| `check.sh` | exit 0 |
| Errors in the `.out` files | 0 `error` lines in each of the 18 outputs (17 modules + control) |
| Per-file axiom sweep | `nonstandard: 0` in every module, each with a nonzero constant count (FrameF3 5 … Conf2122Cert 96) |
| Negative control | the planted copy of `FrameF3` reports `nonstandard: 1; [(auditPlanted, sorryAx)]`: **caught** |
| Compiled copies = main sources | `audit_*.lean` (minus the appended audit lines) is byte-identical to the main file for FrameF3, DiamondMOcc, C2122MOcc, Conf2122Cert, RadiusFive, RStarSanity, OccToRing and RingReduce (spot-check of 8 of 17) |

## 2. Statement prints (from `audit_FrameF3.out`)

These match the audit's hand reading of the statements:
- `RStarFrame`: ∀ m T, 0 < m → Connected → Triangulated → (∀ x, 5 ≤ degree x) → NoSep T → DiamondFree T → Conf2122Free T → ∃ v, degree v = 5 ∧ PureClean T v.
- `DiamondFree` = no `DiamondM.Occ` and no `DiamondP.Occ`. `Conf2122Free` = no `C2122M.Occ` and no `C2122P.Occ`.
- `four_color_of_RStarFrame : RStarFrame → ∀ {n} (M : SphericalMap n), M.graph.Colorable 4`. Axioms: `[propext, Classical.choice, Quot.sound]`.
- `rStarFrame_of_noSepTri : RStarNoSepTri → …`, standard axioms.

## 3. Verdict: PASS

**Ledger line (the Navigator's to record):**
> Compiled and audited: R\* on Occ-free, four-connected, minimum-degree-5 triangulations implies 4CT for spherical maps. The hypothesis R\* is open.

**Carried forward (they do not block the PASS):**
- **F1, wording.** "Diamond-free" in docstrings and prose means `DiamondFree` as printed: no *Occ* (ring-embedded occurrence) of either diamond orientation. It does not mean "no induced diamond subgraph". Reports should say "Occ-free".
- **F3, non-vacuity of the 2.122 exclusion.** No compiled witness yet shows that `C2122M.Occ`/`C2122P.Occ` can hold. The candidate (order 25, index 4830, hole 15) is routed to Studio Math. Until then the 2.122 hypothesis is known to be harmless (it only weakens what R\* must prove) but is not shown to bite.
- **Scope.** As before: `SphericalMap` is combinatorial (graph + rotation + `Fills`). Topological embedding → `SphericalMap` is not formalised, so "4CT for spherical maps" is the exact claim, not "4CT for the plane".
- The bridge lemma "appears → Occ with distinct ring" stays open.

## 4. Still open with the audit: the inert-disc replay (order 20, index 51, hole 1)

The command, unchanged since `7d32745`, for Studio compute (repository root, `main` at or after `7d32745`, any Python 3, CPU cap 10 minutes):

```
( ulimit -t 600; nice -n 10 python3 backgroundMaterial/planemap-structural/longtable/audit/inertdisc-replay/replay_inertdisc.py \
  backgroundMaterial/planemap-structural/longtable/studio-explore/sage-qa-runs/inertdisc-first-instance.json ) > inertdisc-replay-out.json
shasum -a 256 backgroundMaterial/planemap-structural/longtable/audit/inertdisc-replay/replay_inertdisc.py \
  backgroundMaterial/planemap-structural/longtable/studio-explore/sage-qa-runs/inertdisc-first-instance.json
```

Expected hashes: script `3ea38284…43be6b`, instance `0a8d971f…c432e440`. Return `inertdisc-replay-out.json` and the hash lines. The expectations are those of the 16:42 message (path-dependent disc side). The verdict is written only once the output is read.

— Independent audit
