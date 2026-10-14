# Frozen Kempe classes on pseudo-surfaces vs manifolds [exploratory]

Long Table, 13 Oct 2026, one-day experiment (about 90 minutes, started 22:00 by the clock). Labels:
**[data]** computed here; **[hand]** argument written here, not reviewed. Other tracks' code is used
read-only; the engine `sf_eng.c` is a copy of TrackJ `tj_eng.c` with one added output (`DLrun`).
Compute: at most 3 processes, `nice -n 10`, each run at most 15 minutes, on AC power (checked with `pmset`).

## 0. Pre-registration (written 22:05, before any search was run)

**Question.** Does a *frozen class* exist (A) on pseudo-surfaces but not (B) on genuine closed
2-manifolds?

**Definitions.**
- *Frozen class.* h is a degree-5 vertex of G whose link (in the complex) is a 5-cycle. A Kempe class of
  proper 4-colourings of G − h (up to renaming; moves = swaps of any component of any of the six pair
  graphs) is frozen if **every** state lies on an all-DL π-cycle. Engine test: `size == onCyc` (this
  forces 0 filled states). By TrackF §8.1 this is exactly "LPC fails at that class". No condition on N,
  the law or H3 is imposed.
- *Arm A object.* G is the 1-skeleton of a closed pure 2-complex K in which every edge lies in exactly
  two triangles of K (pseudo-surface). Vertex links are then disjoint unions of cycles, so pinch points
  are allowed. The hole's link must be one 5-cycle.
- *Arm B object.* Arm A plus: every vertex link is a single cycle (a closed surface, any genus, either
  orientability).
- *Graph-level certificate.* If every edge of G lies in exactly two triangles **of G**, then K = all
  triangles of G is an arm-A complex. This "flag" condition is sufficient, not necessary.

**Searches.**
- S0: reproduce one or more TrackJ rung-d frozen classes with `sf_eng`, and measure their defects.
- S1 (from rung d, graph level): TrackJ-style annealing (edge toggles + vertex stacking), objective
  = gap + λ·defect, where gap = min over classes with a cycle state of (size − onCyc), defect_A =
  Σ_edges |t(e) − 2| (t = number of triangles of G on e), defect_B = defect_A + Σ_v (components of
  link(v) − 1). Hits must have gap = 0 and defect = 0.
- S2 (complex level): walks on explicit face lists that preserve "every edge in exactly two faces".
  Moves: edge flip, vertex insertion in a face, removal of a degree-3 vertex, handle/crosscap tube
  between two disjoint faces, and (arm A only) pinch = identification of two vertices with disjoint
  closed stars / unpinch. Every degree-5 vertex is a hole. Objective (lexicographic): min gap over cycle
  classes, else max DLrun (longest π-path of DL states).

**Power controls.**
- C1: S1 with λ = 0 must keep finding frozen classes (engine and scoring are sound).
- C2: the arm-B search must find all-DL π-cycle classes on manifolds (classes that have filled states):
  **at least 20 distinct cycle classes**, otherwise a B-null is reported as *unpowered*. The minimum gap
  reached is reported next to TrackF's floors.
- C3: an arm-A hit shows the complex-level search can find frozen classes when they exist.

**Verdict rules (fixed now).**
1. A yes, B no, C2 passed → reading 1: the missing local ingredient is "vertex links are single
   cycles" (a theorem candidate, data level).
2. A no, B no, C2 passed → reading 2: the pseudo-surface condition (edge in exactly two triangles)
   already kills frozen classes in the searched range; manifoldness/pseudomanifoldness is the axiom.
   If A's search has no positive control this is also reported as "not distinguishable from weak search".
3. B yes (any genus) → reading 3: LPC is sphere-only; the input must be the law at class level.
4. C2 failed → inconclusive for B.

## 1. Bottom line

- **Arm A (pseudo-surfaces): no frozen class found.** About 4.5M evaluations over five search designs.
  The searches came from two sides: from the TrackJ frozen classes towards pseudo-surfaces, and from
  genuine surfaces (with pinches allowed) towards frozen classes.
- **Arm B (closed surfaces, any genus): no frozen class found.** Control C2 passed: about 13,500
  distinct all-DL π-cycle classes on RP² and the Klein bottle in the arm-B runs (28,600 counting the
  manifold states visited by the arm-A runs), all with filled states.
- **Verdict (rule 2, with its caveat): A no, B no.** Arm A has no positive control (C3 was not met).
  So reading 2 ("pseudo-surface structure already kills frozen classes") **cannot be separated from
  "the search is too weak"**. Reading 1 ("links single cycles is the missing axiom") is **not supported**.
  Pinching never helped:
  - from the frozen side, the arm-A scores (pinches allowed) got no closer than arm B (flag 10 vs 9;
    complex level 3 vs 3);
  - from the surface side, pinches lowered the gap floor only from 52 to 48 (out of ≥ 68 states).

  Reading 3 is not triggered.
- **Where the two worlds stop [data].** From the frozen side, the frozen 20-state class survives every
  reduction of surface defect except the last one:
  - flag defects went from 71–93 down to 9;
  - at complex level, *every edge in at least two triangles* is reached with the class still frozen;
  - but a face set with *every edge in exactly two faces* never exists (SAT UNSAT every time).

  From the surface side, the smallest gap (non-cycle states in a cycle class) is **52** on manifolds
  (RP² / Klein, class [72, 28 filled]; TrackF's 7/18 class) and **48** on pinched pseudo-surfaces
  ([68, 22 filled]). So the obstruction sits at "**each edge in exactly two triangles**" (the
  pseudomanifold condition), not at link connectivity. This is a data tilt towards reading 2, not a proof.

## 2. S0: reproduction [data] (`s0_reproduce.py`, `out/s0_rung_d.txt`)

All 43 TrackJ rung-d graphs were run through `sf_eng` (hole 0).

**Frozen class.**
- Each graph has exactly one frozen class: 20 states, all on one all-DL 20-cycle, N = 8/9 (10 each),
  law failures 0, 0 filled states.
- G − h has 24–26 colourings in total, so G is 4-colourable through the other classes.

**Surface defects** (graph level; t(e) = number of triangles of G containing e).

| defect | range over the 43 graphs |
|---|---|
| edges with t ≠ 2 | 57–72 (matches SCOPE-A5v §4) |
| Σ\|t − 2\| | 71–93 |
| vertices whose link is not 2-regular | ≥ 27 |
| edges in fewer than 2 triangles | 21–32 |

Because of the last row, **no complex at all** (any face subset) has G as a pseudo-surface 1-skeleton.

## 3. Arm A and arm B from the frozen side: S1 [data] (`s1_search.py`)

**Method.**
- TrackJ-style annealing from the 43 rung-d graphs, 4,000 steps per walk.
- Moves: toggle 1–2 edges (never at h, never link–link), stack a vertex (10%), delete a vertex of
  degree ≤ 4 (5%).
- Score: gap + λ·defect.
- Logged: the Pareto front (defect → least gap).

**Defect variants.**
- *Flag level.* Arm A uses Σ\|t − 2\|; arm B adds Σ(link components − 1).
- *Complex level* (`sf_cplx.py`). CA uses the number of edges in fewer than 2 triangles (+3). Once
  that is 0, a MiniSat call (pysat) asks for a face set K with every edge in exactly 2 faces of K and
  the star of h forced; if none exists the defect is 3. CB adds "some solution has all links single
  cycles": up to 300 solutions are enumerated, and the defect is 2 if none qualifies.

| run | evaluations | least defect with gap 0 (frozen class kept) | hits |
|---|---|---|---|
| flag A, λ = 1 | 1.07M | 13 | 0 |
| flag A, λ = 3 | 1.22M | 10 (best trade-off: defect 7 at gap 10) | 0 |
| flag B, λ = 1 | 1.15M | 9 | 0 |
| complex CA, λ = 1, from rung d | 0.41M | **3** = every edge in ≥ 2 triangles, but no exact 2-cover (UNSAT) | 0 |
| complex CA, λ = 1, from CA near-misses | 0.30M | 3 (same) | 0 |
| complex CB, λ = 1, from CA near-misses | 0.29M | 3 (fails already at the arm-A SAT stage) | 0 |

- **Control C1 passed.** The frozen class (gap 0) persisted along the whole front in every run.
- **Near-miss shape.** The defect-3 graphs are very dense: n ≈ 60 (stacked), E ≈ 290–380, 316–500
  triangles, 180–290 edges in > 2 triangles, 8–28 colourings in total.
  - E mod 3 is 0 in some and non-zero in others, so the UNSAT is not only the counting parity 2E = 3F.
  - The search densifies until every edge has ≥ 2 triangles, then cannot choose an exact 2-cover.
- **Limit.** The complex-level score has no gradient between "≥ 2" and "exactly 2". A MaxSAT version
  (`maxsat_defect` in `sf_cplx.py`) was too slow to use (> 2 min per graph) and was not run. **This is
  the main weakness of the arm-A null.**

## 4. Arm A and arm B from the surface side: S2 [data] (`s2_search.py`)

**Method.**
- Annealing on explicit face lists. Every move keeps "every edge in exactly two faces" (checked).
- Moves: flips, 1–3 insertions, removal of degree-3 vertices; for arm A also pinch / unpinch, with at
  most 4 extra link cycles.
- Every degree-5 vertex with a single-cycle link is a hole.
- Score: log2(1 + gap), else a DLrun fallback.

**Starts.**
- *Random.* Octahedron + insertions + 1–5 tubes (handles or crosscaps).
- *Seeded.* The 250 TrackJ RP² / torus / Klein graphs. Their face sets were recovered by SAT with all
  links single cycles (`mk_surface_seeds.py`, `out/seeds_surfaces.jsonl`): 202 RP², 36 Klein, 12 torus.
- Seeded runs alternate seeded and random-sphere walks. The sphere walks act as a reference.

| run | arm | starts | evaluations | distinct cycle classes | least gap: sphere / manifold χ < 2 / pinched | least F/N in a cycle class: manifold / pinched | hits |
|---|---|---|---|---|---|---|---|
| s2_A | A | random, χ = 0 … −8 | 0.52M | 0 | – | – | 0 |
| s2_B | B | random (in practice spheres; tubes failed) | 0.23M | 323 | 904 / – / – | – | 0 |
| s2_Bg | B | seeds + 1–4 tubes (χ ≤ −2) | 0.23M | **0** | – | – | 0 |
| s2_Ag | A | seeds + 1–4 tubes | 0.18M | 618 | – / 52 / – | 0.389 / – | 0 |
| s2_Bs | B | seeds | 47k | 9,958 | – / 80 / – | 0.282 / – | 0 |
| s2_Bs2 | B | seeds (random choice) | 24k | 3,936 | 1,680 / **52** / – | 0.321 / – | 0 |
| s2_As | A | seeds | 73k | 13,019 | 80 / 52 / **48** | 0.316 / **0.187** | 0 |
| s2_As2 | A | seeds (random choice) | 33k | 6,876 | 1,180 / 52 / 52 | 0.333 / 0.338 | 0 |

**Reading [data].**
- **C2 passed.** About 13,500 distinct manifold cycle classes were found in the arm-B runs (28,600
  including the arm-A runs' unpinched states; RP² / Klein, χ = 0, 1).
  Every one has filled states.
- **The least manifold gap is 52**, in both arms and in four independent runs. It is the 72-state
  class [72, 28, 26, 20], TrackF's 7/18 class.
- **Pinching gives 48** once ([68, 22, 32, 20], χ = −2, 2 pinch points), F/N down to 0.187. A frozen
  class needs gap 0, so pinching helps marginally.
- **High genus is unpowered.** Starts with χ ≤ −2 built by tubes produced **no** all-DL π-cycle at all
  (s2_A random, s2_Bg), consistent with TrackF's census finding (random graphs off the sphere carry no
  π-cycles). The rung-d density corresponds to χ ≈ −8 for a surface on 35 vertices, which this search
  never populated with cycle classes. So **arm B at high genus is untested in practice**, and C2 was
  met only at χ = 0, 1.
- Side observation, not checked further: manifold cycle classes reached F/N = 0.282 < 3/8. These classes
  were not filtered for lock-parity violators, so this does not contradict TrackF's violator-free 3/8
  floor.

## 5. Verdict per the pre-registered rules

- A: **no** (0 hits; the closest objects are §3's "≥ 2 but not exactly 2" graphs and §4's gap-48 class).
- B: **no** (0 hits; C2 passed at χ = 0, 1; high genus unpowered).
- → **Rule 2**, with its caveat: *not distinguishable from weak search*, because no positive control
  for arm A exists.
- **Reading 1 ("links single cycles") has no support.** The pinch freedom of arm A bought nothing
  measurable on either side. Every frozen near-miss already fails the exact-two-faces condition.
- **The data place the barrier at the pseudomanifold condition** (each edge in exactly two triangles).
  As a theorem candidate this would be: *a closed pseudo-surface triangulation carries no frozen class
  at a degree-5 hole* [conjecture, weak data].
- To make this a powered test, two things are needed:
  1. a MaxSAT- or LNS-based arm-A score with a gradient through "exact 2-cover";
  2. high-genus (χ ≤ −4) manifold starts that actually carry all-DL π-cycles, e.g. TrackF's glued
     lifts with many handles.

## 6. Compute and process note

- Runs: 22:02–23:06, three at a time, each ≤ 14 minutes, under `nice -n 10`, on AC power (100%).
- Each "process" is one Python driver plus its `sf_eng` pipe child. The two are synchronous, so only
  one is busy at a time.
- One S2 pair (s2_A / s2_B, first version) was stopped after 1 minute and restarted, because tubes made
  the genus drift (χ to −110) and the score scale was wrong. Only the restarted runs are reported.

## 7. Files

| file | content |
|---|---|
| `sf_eng.c` / `sf_eng` | copy of TrackJ `tj_eng.c` with `DLrun` added (build: `cc -O2 -o sf_eng sf_eng.c`) |
| `sf_lib.py` | engine pipe, graph defects, face-list utilities (links, χ, orientability) |
| `sf_cplx.py` | SAT test for a pseudo-surface face set with 1-skeleton G (arm A) and single-cycle links (arm B); unused MaxSAT variant |
| `s0_reproduce.py` | S0 |
| `s1_search.py`, `s1_report.py` | S1 (flag-level A / B / 0, complex-level CA / CB) |
| `s2_search.py`, `s2_report.py`, `mk_surface_seeds.py` | S2 and its seeds |
| `out/s0_rung_d.txt` | S0 rows |
| `out/s1_*.{jsonl,log}` | S1 fronts (graph lines) and walk logs |
| `out/s2_*.{jsonl(.gz),log}` | S2 cycle-class records (graph line, class tuple, χ, orientability, pinch count) |
| `out/seeds_surfaces.jsonl`, `out/seeds_ca_focus.jsonl` | seeds |
