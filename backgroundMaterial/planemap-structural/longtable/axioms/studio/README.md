# Studio runs for the Long Table axioms programme (13 Oct 2026) [exploratory]

Mac Studio, `nice -n 10`, at most 14 worker processes. Jobs 3–5 of the Long Table briefs. Everything here is data
(label: exploratory). Long Table's code in `..` and `../proof` was used read-only.

## Job 3: exact T1-v search at n = 24, 26 (`sat_cubes.py`, `run_job3*.sh`)

**Method.** This is Long Table's encoding (`../sat_t1v.py`, `Enc`, eager = 1) with the same lazy CEGAR cuts, split into
cubes by the chord positions of v's labels. Depth 2 pins f_1 and f_3 on chords (0, j), giving (n−3)(n−4) cubes. Each
label sits on exactly one v-edge, so the cubes partition the search space.
- Each worker keeps one CaDiCaL 1.5.3 solver (python-sat) for all its cubes and solves each cube under assumptions.
  Every cut is valid globally, so cuts learnt in one cube carry over.
- **Proof material.** python-sat's CaDiCaL gives no DRAT trace. Instead every cut is appended to
  `out/<run>.cuts-<pid>` (DIMACS clauses; gzipped in git as `out/cuts/<run>.cuts.gz`). The eager CNF is reproducible
  from `Enc`, so eager CNF + cuts + cube units is a plain CNF that a proof-producing solver can refute offline.
- Every SAT result is re-checked with `ax_lib.G5`, which is independent of the SAT decode: DL at every state, A5v at
  every state, and the orbit for closed runs.
- **Time limits.** CaDiCaL in python-sat cannot be interrupted, so per-cube time limits are only checked between CEGAR
  rounds.

**Results** (`out/*.jsonl`; one line per cube):

| n | run | axiom | result | wall | CPU (sum of cubes) | max cube |
|---|---|---|---|---|---|---|
| 20 | closed L = 10 (check) | A5v | UNSAT, 17 cubes (depth 1) | 2 s | | |
| 22 | window 8 (check) | A5v | SAT (4 cubes), ax_lib-verified | 54 s | | |
| 22 | window 9 (check) | A5v | **UNSAT**, 19/19 cubes (Long Table: 392 s uncubed) | 65 s | | 40 s |
| **24** | **window 10** | **A5v** | **UNSAT, 420/420 cubes** ⇒ no T1-v orbit of any length at n = 24 | 1,241 s | 9,790 s | 124 s |
| 24 | window 10, power | none | SAT: 3 runs found (stop after 3), word 0121212121; 8 cubes timed out at 1,200 s | 2,035 s | | 835 s |
| 24 | window 10, power | anti-A5v | no SAT in 44 cubes / 57 min (29 UNSAT, 15 timeouts); capped | | | |
| 26 | window 10 | A5v | **SAT** in cube (f_1@4, f_3@20) after 367 s; 71 other cubes UNSAT; stopped | | | 1,706 s |
| 26 | window 11 | A5v | 77/506 cubes, all UNSAT; capped at 2 h (Long Table) | 2 h | 50,321 s | 2,981 s |

The n = 26 window-10 run (`out/n26_W10_A5v_window.json`) has these properties, re-derived with `ax_lib.G5` from the
graph line:
- 10 states, all DL, with A5v true at every state;
- frames 2, 0, 3, 1, 4, …; word 1212…;
- the graph is **non-planar**;
- state 10 is not DL, so the run dies.

It is **not** a closed orbit, so T1-v is not refuted. The closed L = 10 search at n = 24 was not run: the window-10
UNSAT already covers every length.

## Job 4: R0 at larger n (`r0_cubes.py`, `run_job4.sh`) — dropped

This was Conjecture R0 (`../proof/PROOF-ATTEMPT-1.md` §5) by cubes; the R0 encoding is pure SAT, so the full CNF is
written once. The driver was validated at n = 16 (planar UNSAT in every cube, as `relax2.py` gives; non-planar SAT,
verified). The job was dropped before it ran, because Job 5 refuted R0 directly on census graphs, and Long Table
agreed to give the cores to Job 5.

## Job 5: directed cycles of the PM digraph D at sphere holes (`dcyc.cpp`, `dcyc_worker.sh`)

**D** (`../proof/R0-ATTEMPT-1.md` §1): vertices are the perfect matchings of G = Tait dual of a triangulation at a
degree-5 hole. There is an arc M → M′ iff M ∩ M′ = ∅ and k(M′) = k(M) − 2.

**Implementation.**
- Arcs are enumerated as the perfect matchings of E − M containing f_{k−2}; then Tarjan SCCs.
- Per cyclic SCC: size, arcs, girth, frame counts, Hamiltonian arcs inside it, a histogram of the component counts
  of E − M_t, the DL states, and the Q-cycles. A **DL state** is E − M a connected figure-eight with loops paired
  {k±1} (even) and {k±2} (odd), exactly as `ax_lib.G5.dl`. A **Q-cycle** is a directed cycle through DL states only;
  for each, the length, the k(M_{t−1} ∪ M_t) word and its Hamiltonian arcs are reported.
- Per hole, the existence of Hamiltonian cycles for each of the 10 v-edge pairs is also reported. A Hamiltonian cycle
  through a non-adjacent pair is the same thing as a Hamiltonian arc of D.
- Flags:
  - R0\* violation: D cyclic and some Hamiltonian arc exists;
  - R0 violation: a Hamiltonian arc inside an SCC;
  - R0c violation: a Q-cycle with a Hamiltonian arc.

**Validation.**
- C30#0 (TrackU seeds) reproduces Long Table's numbers: 125 PMs, 60 arcs, 0 Hamiltonian arcs, one SCC of size 20 with
  girth 20, which is a Q-cycle with word 3232…, and Hamiltonian cycles only through adjacent pairs.
- 50 census holes (orders 28, 30, 33): #PM, #arcs, #Hamiltonian arcs and cyclic-or-not agree with
  `r0lib.analyse`.
- p27#4710 h14: the per-state DL and component counts agree with `ax_lib` state by state.

**R0 is false in the plane (13 Oct, three independent codes).** p27#4710 (Census29 frame-class, order 27), hole 14,
n = 46: D has a closed 10-cycle through a Hamiltonian arc (`out/R0_counterexample_p27_4710_h14.json`). It is
confirmed by `dcyc`, by `r0lib.analyse` and by `ax_lib` (PM, disjointness, frames −2, Hamiltonian M_0 ∪ M_1,
planar_rot), and independently on the MacBook. At 7 of its 10 states E − M_t is disconnected, so it is not a Q-cycle.

**Census, frame class, orders 22–33, every degree-5 hole** (`out/dcyc/census-22-33.jsonl.gz`):

| order | holes with cyclic D | cyclic SCCs | R0 violations | smallest n | Q-cycles |
|---|---|---|---|---|---|
| 22–26, 28 | 0 | 0 | 0 | – | 0 |
| 27 | 2 | 2 | 2 | 46 | 0 |
| 29 | 28 | 30 | 22 | 50 | 0 |
| 30 | 94 | 94 | 74 | 52 | 0 |
| 31 | 591 | 606 | 500 | 54 | 0 |
| 32 | 2,465 | 2,494 | 2,085 | 56 | 0 |
| 33 | 11,327 | 11,484 | 9,566 | 58 | 0 |

Totals and structure:
- 1,337,323 holes; 14,507 have a cyclic D, and all of them violate R0\*. Only 24 holes in the whole census have no
  Hamiltonian arc. R0 is violated at 12,249 holes.
- **Q-cycles: 0, and R0c violations: 0.** This agrees with TrackS (README §2.4: the frame class to order 33 has no
  Q-cycle).
- SCC girths are 10 (13,685) and 20 (1,025); sizes run from 10 to 318.
- The census all-DL π-cycles are D-cycles but **not** Q-cycles. For example, at p30.r10#1252 h19 only 8 of the SCC's
  34 states have E − M connected.
- 14.5 CPU-h.

**Fullerene duals** (TrackF graphs; `out/dcyc/fullerene/`). G must have at most 128 edges, which means dual V ≤ 46;
larger graphs are skipped and counted.

| set | holes | cyclic D | R0 violations | Q-cycles | R0c violations |
|---|---|---|---|---|---|
| all fullerenes C20–C46 (`fall_20_46`, 342 graphs) | 4,104 | 11 | 7 | 2 (C30#0 h0, h16) | 0 |
| IPR (`ipr32_52`, dual V ≤ 46: 105 graphs; 13,944 holes skipped) | 1,260 | 184 | 153 | 0 | 0 |
| Goldberg (`goldberg`; 48 holes skipped) | 36 | 0 | 0 | 0 | 0 |

- The C30#0 Q-cycles have length 20, word 3232…/2323… and no Hamiltonian arc, as TrackS found. C40#0's 20-cycles
  have no DL state.
- R0 violations among C20–C46 are at C40#14 (h0, h2), C44#12 (h0, h2), C44#57 (h9) and C46#21 (h0, h24).
  **C40#14, with n = 36, is the smallest planar R0 counterexample found** (the census minimum is 46).
- Max #PM per hole was 494,101 (IPR, n = 84).
