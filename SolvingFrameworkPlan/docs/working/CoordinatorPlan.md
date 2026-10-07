# Coordinator plan (from 7 October 2026)

The Studio session is the lone coordinator (Kyle, 7 Oct). This file is the plan of record. Each Navigator revision should say which tracks moved.

## Target

R\* in the frame class: every connected spherical triangulation with minimum degree 5, no separating triangle, and no `Occ` of the Birkhoff diamond or of RSST 2.122 (either orientation) has a pure-clean vertex of degree 5. `four_color_of_RStarFrame` (FrameF3.lean) already compiles R\* ⇒ 4CT.

Scope gap: the compiled statement is 4CT for combinatorial `SphericalMap`s (rotation systems). 4CT for topologically drawn planar graphs (e.g. OpenAI's `OAI.PlanarL1.IsPlanar`: injective points, simple arcs with disjoint interiors) would need a separate drawing ⇒ combinatorial-map bridge. Cost revised down (OpenAIMathScan.md, 7 Oct): OpenAI's Barnette formalisation (`lean/OAI/Combinatorics/Hamiltonian/`, Mathlib-only, agent-written, unaudited) has `PlaneEmbedding.exists_exact_dual` (drawing ⇒ algebraic dual + Euler, no Jordan curve theorem needed), and `alonamaloh/schoenflies-lean` gives Jordan–Schoenflies. Remaining: algebraic dual ⇒ rotation system (`SphericalMap`), plus porting (they use Lean v4.34.1; StudioMathLean uses v4.35.0-rc3). Off the critical path until R\* moves; a Comparator-style frozen challenge file for R\*/4CT is queued for Track C.

Honest baseline: forecast p = 0.02. Every result proved so far (F5, weak F6, `pureClean_of_hole4`) is about holes with three consecutive degree-5 link vertices. Those holes contain a diamond, so they never occur in the frame class.

## Tracks and kill rules

| Track | Goal | Success | Kill rule |
|---|---|---|---|
| A: break it | Adversarial search inside the frame class for failures of R\*, then the quarter floor, B′ and G66⁰ | A verified counterexample (publishable) or a documented null over a stated search budget | — (always worth running) |
| B: unavoidable hole types | Discharging census: which link-degree words must occur at degree-5 vertices of frame-class triangulations; then PureClean per type, adding reducible exclusions where needed | ≤ ~20 hole types, each with PureClean proved | > ~100 types, or a type with no local handle and no candidate exclusion |
| C: formal discipline | Every claim labelled formal / hand / data / killed; nightly full regression; independent review of hand proofs before the Navigator | — | — |
| D: bank a result | Short paper: Theorem W, F5, weak F6, D-resolvability framework, Lean reduction (partial result, honest scope) | Draft ready for Kyle | — |

Go/no-go review every two weeks (next: 21 Oct 2026) against these kill rules.

## Budget (coordinator's decision, 7 Oct)

- Agents: at most 6 running at once (workflow guideline < 10).
- Studio CPU (16 cores, 128 GB): coordinator-started compute runs under `nice -n 10` and uses at most 8 worker processes in total. Jobs BO/BP keep their current workers. The Studio is shared with Kyle's EEGLearn project (Python multiprocessing jobs); EEGLearn has priority, so 4CT compute stays nice'd and within the cap even when the machine looks idle.
- Lean regression: one full `check.sh` run per day (about 10 minutes).

## Status log

**7 Oct, Track B verdict: amber, leaning kill** (TrackB/README.md). Proved unavoidable set: 59 hole types (78 without F2), using certified one-step discharging; the optimum for one-step rules is exactly 59. Rigorous lower bound 9; the empirical minimum is at least 13 and still rising. **66666 is forced into every S** (all IPR fullerene duals are frame-class, and their only hole type is 66666), and no hole type in the frame class has PureClean proved.
Consequence: **G66 is on the critical path.** R\* in the frame class implies PureClean at some 66666 hole of every IPR dual, which by `pureClean_of_no_allDL_orbit` is G66⁰ there. Fullerenes are a test bed where 3-edge-colourability is known independently (Kardoš: fullerenes are Hamiltonian). Next: a dedicated G66 track. Two-step discharging and the order 29–31 census are deferred.

