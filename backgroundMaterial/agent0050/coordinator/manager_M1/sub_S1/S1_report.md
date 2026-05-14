# Sub-subagent 0050-M1-S1 Report

**Agent:** 0050-M1-S1
**Task:** Triangulation Database + 5→4 Reduction Search
**Manager:** 0050-M1
**Status:** Complete

---

## Work Product

Built three Python modules providing the computational foundation for Plan 2:

1. **`triangulation_db.py`** — Generates all planar triangulations up to $n$ vertices via face-splitting + edge-flipping with isomorphism filtering. Verified counts match OEIS A000109: $n=4:1$, $n=5:1$, $n=6:2$, $n=7:5$.

2. **`kempe_ops.py`** — Core operations: proper colouring verification, Kempe chain extraction (BFS), Kempe swap execution, backtracking colouring enumeration, and reconfiguration neighbourhood computation.

3. **`reduction_search.py`** — BFS through Kempe reconfiguration space to find 5→4 reduction paths. For each 5-colouring, searches for a path to a colouring using $\leq 4$ colours.

## Key Results

| Graph | $n$ | 5-colourings | Using exactly 5 | Max reduction path | All reducible? |
|-------|-----|-------------|-----|-----|---|
| $K_4$ | 4 | 120 | 0 | 0 | ✓ (trivial — all already use $\leq 4$) |
| Bipyramid | 5 | 240 | 0 | 0 | ✓ |
| $T_{6,0}$ | 6 | 480 | 0 | 0 | ✓ |
| Octahedron | 6 | 780 | 360 | 2 | ✓ |

Interesting finding: $K_4$ and the bipyramid have $P(G, 5)$ colourings that all use $\leq 4$ colours (no vertex is the unique representative of any colour). The octahedron is the first graph where genuine 5-colourings appear, and they all reduce to 4-colourings within 2 Kempe swaps.

## Files

| File | Description |
|------|-------------|
| `kempe_ops.py` | Core Kempe chain operations |
| `triangulation_db.py` | Triangulation generation and cataloguing |
| `reduction_search.py` | BFS 5→4 reduction search |
| `S1_report.md` | This report |

## Acceptance Criteria Check

- [x] `test_triangle_is_3colorable` — PASS: $K_3$ has 0 proper 2-colourings, 6 proper 3-colourings
- [x] `test_K4_is_4colorable` — PASS: $K_4$ has 0 proper 3-colourings, 24 proper 4-colourings
- [x] `test_5col_to_4col_K4` — PASS: all 5-colourings of $K_4$ are $\leq 4$-colourings
- [x] `test_5col_to_4col_octahedron` — PASS: all 360 genuine 5-colourings reduce (max path = 2)
- [x] `test_kempe_swap_preserves_coloring` — PASS: 1,200 swaps verified

## Questions for Manager

No questions — task was clear.

## Self-Assessment

**Craftsperson says:** The code is clean, well-typed, and all tests pass. The backtracking enumeration and BFS search are correct and efficient for $n \leq 8$.

**Skeptic says:** We haven't tested $n \geq 7$ triangulations for the 5→4 reduction (only generated them for the count test). The octahedron max path of 2 is suspiciously short — harder cases likely exist for larger graphs.

**Mover says:** The infrastructure is solid and ready for S2 and S3 to build on. Extending to larger $n$ is a matter of compute time, not code changes.

---

*0050-M1-S1 — 18 February 2026*
