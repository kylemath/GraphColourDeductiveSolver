# Job 17: C-reducibility census of wheels (Studio, 14 Oct 2026) [exploratory; every C verdict is a CANDIDATE]

The pre-registration is `HYPOTHESIS.md` (H17). The checker is `../studio15/cfast.cpp`: dfast D-closure plus a
contraction search, |X| ≤ 4, with Gonthier `valid_contract` admissibility as translated there.

**Scope.** 216 wheels with ring ≤ 16, up to rotation and reflection:
- 5-wheels with link words in {5,6,7,8}^5 (126);
- 6-wheels with link words in {5,6,7}^6 (90).

Verdict per wheel: `wheels17_verdicts.txt` (the working-X count and one X, or the best leftover). The full search
output, with every working X, its size, ring-edge count and triad vertex, is `census17_full.txt.gz`.

| family | D | C (candidate) | neither |
|---|---|---|---|
| 5-wheels | 12 | 12 | 102 |
| 6-wheels | 25 | 12 | 53 |

- **H17 survives.** Every 5-wheel whose link has no vertex of degree ≥ 7 is D or C. The only one that is not D is
  66666, and it is C.
- **C-candidate 5-wheels:** 55558, 55568, 55577, 55578, 55588, 55658, 56568, 56577, 56578, 56588, 56658, 66666.
- **C-candidate 6-wheels:** 555577, 555677, 555767, 555777, 556577, 565667, 565676, 565677, 565757, 565767,
  565777, 566577.
- **Controls** (`controls.out`): 2.126 and 122.126 are C (RSST's X found); 66667 is neither; 666666 is not C under
  contraction ≤ 6 (Franklin's reducer identifies ring vertices and is out of scope).
