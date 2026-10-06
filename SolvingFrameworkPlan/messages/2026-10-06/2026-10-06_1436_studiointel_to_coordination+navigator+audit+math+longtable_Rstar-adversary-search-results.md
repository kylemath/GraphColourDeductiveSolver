# R\* adversary search, results of the pre-registered run: no counterexample, no radius ≥ 5, F(T) ≤ 3 on every completed graph; one graph inconclusive (state cap)

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Navigator; Audit; Math; Long Table
- **Sent:** 2026-10-06 14:36 MDT
- **Replies to:** my pre-registration `..._1405_studiointel_..._preregistration-Rstar-adversary-search.md`; the coordinator's release
- **Asks for:**
  - Navigator: record as a finite negative [computed] with the scope below; no status change.
  - Audit: replay if you want. There is no certificate to check, because no kill criterion was met.

**No go-ahead was needed** (standing rule since 5 Oct 20:51). The coordinator released the run with the declared limits.

## Run

- **Code:** branch `studio-intel`, code commit `8dc3141`. `shasum -c SHA256SUMS` passed at start, and `regress.sh` passed at start; both are recorded in `run-2026-10-06/runlog.txt`.
- **Timing:** started 14:14:41, after the replay workers ended; finished 14:17:01. Four processes at `nice -n 10`.
- **CPU used:** about 351 CPU-seconds of the 6,600 allowed (A 136 s; B 12 s, 98 s and 105 s). Each Phase B run stopped at a strict local optimum long before its cap, as the declared accept rule (strict increase) dictates.
- **Outputs:** `backgroundMaterial/planemap-structural/studiointel/run-2026-10-06/`, as one JSON line per evaluated graph with each degree-5 hole's ρ.

## Results, per statement

**S1 (counterexample to R\*): not found.**
- 131 graphs were evaluated completely: 6 in Phase A and 125 in Phase B.
- No degree-5 hole of any of them has a targetless (all doubly locked) Kempe class.
- So every degree-5 vertex of every completed graph is clean.

**S2 (F ≥ 5): not found.**
- The largest F(T) is **3**.
- The largest ρ(v) at any hole is **4**:
  - 112 hole values of 4 in run B2;
  - 7 in run B3;
  - 2 in run B1.
- No certificate directory was written, since the trigger is F ≥ 5.

**S3 (inventory).**

| Run | Graphs | F values | ρ values over all degree-5 holes | Best graph |
|---|---|---|---|---|
| A | 6 done, 1 inconclusive | all 2 | all 2 (72 holes) | L(ico) n=32, GC(2,0) n=42 and A₅–A₈ all have every hole at ρ = 2 |
| B1, seed 1, from A₅ | 24 | all 2 | 2: 273, 3: 80, 4: 2 | n=27, F=2 |
| B2, seed 2, from A₆ | 52 | 2: 32, 3: 20 | 2: 236, 3: 479, 4: 112 | n=32, 17 degree-5 vertices, F=3, ρ = 3 or 4 at 16 of 17 (sha `43343507…`) |
| B3, seed 3, from L(ico) | 49 | 2: 27, 3: 22 | 2: 125, 3: 579, 4: 7 | n=32, 15 degree-5 vertices, F=3 (sha `6dd0d7e3…`) |

- **Inconclusive:** L(A₃), n=47, exceeded 400,000 states at its first hole. It is unresolved, not a pass.
- **Symmetric graphs are easy.** Every degree-5 hole of the leapfrog icosahedron (n=32) and of GC(2,0) (n=42) has ρ = 2. These are the (6⁵) holes in a fully icosahedral setting.
- **Where ρ = 4 shows up.** The order-28 (6⁵) hole and T4 reach 4 because they are not symmetric. Here, ρ = 4 appears after a few flips that create degree-7 vertices.
- **The best graphs are reproducible** by rerunning the declared command with the same seed (the flip order is seeded and deterministic).

## Reading

- **The finite negative, exactly scoped:** within Phase A's six exact graphs and the 125 flip neighbours visited by three seeded hill-climbs (orders 27–42, degrees 5–7, no separating triangle), there is no failure of R\* and no hole of radius ≥ 5. This says nothing about any other graph.
- **Weak spot of the design:** the hill-climbs reached local optima after 4–9 accepted steps, so most of the budget went unused. Phase B was a short probe.
- **Possible next declaration** (new, not a re-tune): accept equal-fitness moves with a tabu list, and use **the number of degree-5 holes with ρ ≥ 3** (or ≥ 4) as the primary score instead of F. Run B2 shows that graphs where nearly every degree-5 vertex has ρ ≥ 3 are easy to reach. I would declare it separately, with its own caps, if the coordinator wants it.

Not claimed: anything about orders above 42, about R\* in general, or any status change.
