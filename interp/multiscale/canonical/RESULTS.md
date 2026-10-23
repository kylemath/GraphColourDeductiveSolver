# Pair induction along canonical orderings: it fails at the first vortex pair

22 Oct 2026, ~100 min. Code: `pi.py` (canonical ordering by peeling, the pair invariant, the minimal-R search), `run.py` (batch → `runs.jsonl`, `runs.log`), `diag.py`, `cert.py`, `cc.py`, `claims.py` (→ `claims.json`). Failure instances: `fail_*.pkl` (boundary B, gauge signs s, parity, full colouring, the step's vertex and path). Labels: [P] proved, [M] measured (exact for the instance), [C] conjecture.

## 0. Numbers

| item | result |
|---|---|
| runs finished (ico4 n=162 left/right/rand×2, ico10 n=1002 rand×2; others still running at hand-off) | **7/7 FAIL.** No run got past the first time the disc enclosed 2 or 3 odd vertices. |
| failure step (n of prefix, L, interior odd) | ico4-left 110, 104, 2 · ico4-right 95, 93, 2 · ico4-rand 104, 63, **3** · ico4-rand 88, 70, 2 · ico10-rand 442, 375, 2 · ico10-rand 510, 347, 2 |
| R at the failure | **no recolouring within R ≤ 3** (exact search, every run); **R ≤ 4** checked on ico4-left (L = 105 instance) |
| R before the failure | R = 0 (plain greedy) at 1324 of 1325 steps; one step needed R = 2 |
| boundary length | canonical prefixes are thin: L ≈ 0.6n–0.95n at failure |
| best value reachable at R ≤ 1 (`diag.py`) | ico4-right: \|t\| = 2, τ_H ≥ 1.564; ico4-rand (odd case): fixed-point radius ≥ 2.0 |
| whole disc free (ico4-left, n = 109, L = 105; SAT with a centre grid of step 0.05 plus an exact check) | **unresolved**: best colouring found has \|t\| = 2, τ_H = 1.13. The run (`scratchpad t5b`) was still going at hand-off. |

**Verdict [M].** On these maps the pair is not locally inductive: R is not bounded by 3 (4 on one instance). Every failure happens at the moment the vortex count turns even with t ≠ 0 forced, or turns odd. The obstruction does not take the form of a short forbidden word (§2).

## 1. Method

- Canonical ordering [P, standard]: reverse peeling of the outer cycle, removing a chord-free vertex other than v1, v2. The choice is leftmost, rightmost or random, with a random outer face. Asserts: each removed vertex's present neighbours form one arc of the current cycle, and parity matches the interior odd count.
- At each step, the free set is ball_{G_{k+1}}(v, R). So R = 0 is greedy, and R = r frees everything within r−1 of the attachment path.
- Exact search:
  - a DFS over the colours of the free boundary vertices, branching on t ∈ {0, ±2e} (even case) or on the reflection centre (odd case), pruned by the incremental circumradius;
  - then a SAT extension (CaDiCaL, assumptions) for the free interior vertices.
- Policy `keep` (fewest changes) was used in all finished runs. The adversarial runs (`advtau`, `advt`) and the hub, flip and defect maps were queued but had not finished. Since `keep` already fails at the first vortex pair, the adversary is moot here.

## 2. Why it fails, and why there is no finite forbidden walk [P sketch + M]

- τ_H detrends by (i/L)·t, a ramp spread uniformly over the arclength of the **whole** boundary.
- Before the failing step the boundary is flat: t = 0 (or one cone) and τ ≤ 1, with a fixed arc of length L − O(R).
- Once a vortex pair with c(u) ≠ c(w) is enclosed, t ≡ 2(c(u)+c(w)) (mod 4Λ) gives |t| = 2. The fixed arc's detrended points then sweep about 2(1 − O(R/L)) along t, on top of the arc's own width ≥ √3/2. So the radius is > 1 no matter what happens inside the ball.
- `cert.py` turns this into a certificate (longest fixed arc alone, t = 0 excluded by the vortex colours). It proves R = 0 impossible in 4/4 even failures, with radius 1.20–1.63.
- At R ≥ 1 the newly enclosed vortex is itself free, so t = 0 is not excluded by colour. The exact search still finds nothing at R ≤ 3 (4 on ico4-left); the likely cause is the Z3 class (review2 §2) [C].
- The obstruction depends on the **ratio** of fixed arc to L, not on any bounded window. Hence **there is no minimal forbidden boundary walk of bounded length** [C, strong]: the same flat arc is harmless when L is much larger than the arc and fatal when the arc is most of L.
- The minimal-instance shrink was therefore not done. The saved instances are in `fail_*.pkl`.
- The odd case fails in the same way (ico4-rand: radius ≥ 2 at R ≤ 1). Threshold 1 is tight before the failure (radius = 1.0 at every odd step).

## 3. Side claims

- **(a) [M, exhaustive over edge stars].** Two adjacent odd vertices always give |t| = 2.
  - The exact-part radius is **neither** constant. Min τ_H is 0.601 for degrees (5,5), 0.760 for (5,7), 0.700 for (7,7) and 0.705 for (5,9).
  - 2/3 occurs, as one non-minimal value, only for (5,5). 2/√3 never occurs.
  - τ_H ≤ 1 holds in 100%, 53%, 30% and 24% of the colourings respectively; the max is 1.32.
- **(b) [M].** On a degree-6 cylinder, every c* rim row has |t| = L, which is linear, and **τ_H = 0** (the walk is straight), not 0.8. So the |t| ≤ 2 half of the pair is what excludes it, not τ_H. On a c*-coloured lattice parallelogram disc (no vortices) t = 0 and τ_H ≈ m/2 + 0.5, which grows linearly. The 0.8 figure was not reproduced.
- **(c) [P + M].** Shifting the base point by one maps the detrended set to itself translated by t/L. So τ_H is exactly base-point invariant; the odd radius is too. Measured spread over all L base points: ≤ 3×10⁻¹⁰ (5 discs, L = 63–375).

## 4. Calibration and open points

- [M] The failures are robust across 3 orderings and 2 maps.
- The larger maps, the hubs, the defect maps and the adversarial policies were still running (`runs.jsonl` is appended live). On the mechanism of §2 they are expected to fail at the first vortex pair too [C, 85%].
- Not established: whether the whole prefix disc admits the pair at all. If it does not, the invariant itself is unsatisfiable on thin discs, independently of R.
- [C] A fix would detrend by a geometric (harmonic-measure) parameter instead of uniform arclength, or would keep pockets and t local. As stated, the pair cannot support a bounded-R induction along canonical orderings, whose prefix boundaries are Θ(n).
