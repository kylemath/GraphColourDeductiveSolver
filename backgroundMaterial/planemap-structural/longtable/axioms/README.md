# Axiom discovery, run 1: which local planar property kills the abstract T1 counterexamples?

Long Table, 13 Oct 2026, about 09:00–10:00. Exploratory. Labels: **[data]** computation here;
**[hand]** short argument written here, not reviewed. Nothing outside `axioms/` was changed. Other tracks'
files were read only (TrackU graphs/logs, TrackT `tt_lib` for sphere duals, TrackF plantri24).
Compute: at most 4 processes under `nice -n 10`, each run ≤ 5 min; machine was charging.

## 0. Verdict

1. **The n = 22 T1 counterexample is reproduced** by an independent Python engine (`ax_lib.py`): 48 perfect
   matchings, 14 DL-good, one closed orbit, L = 10, word 1212121212, 0 law violations. It is non-planar,
   also with the rotation at v fixed (5-wheel gadget + networkx). [data]
2. **A new, very local planar axiom kills every abstract T1 counterexample on disk:**

   **A5v (Jordan at v).** At a DL state M (frame k, Q = E − M = X ∪ Y, X the even loop through f_{k−1}, f_{k+1}),
   the M-partner of v (the far end of f_k) lies on X. Equivalently [hand, parity]: |M ∩ E(X, Y)| is odd.

   *Why it holds on the sphere [hand]:* X is a Jordan curve through v; at v it separates f_k from
   {f_{k+2}, f_{k−2}}. Y touches X only at v, so Y lies on the {f_{k+2}, f_{k−2}} side; every vertex lies on
   X ∪ Y, so the far end of f_k (on the other side) must lie on X.
   *Data:* holds at **48,948 / 48,948** DL-good states of 1,100 plantri24 sphere holes (every 100th graph, all
   degree-5 holes, all DL-good matchings, not only orbit states), at all 40 C30#0 orbit states, and — notably —
   at all 1,672 DL states of the 6 RP²/Klein seed holes too (so it is a *local* Jordan fact, not a sphere-only one).
   *On the counterexamples:* it fails at **every** state of **every** T1 orbit on disk (n22 first; 52 `coll_t1`
   graphs; 576 distinct n = 22 walk graphs; 300 n = 28 walk graphs; `t1_first`): A5v fraction = 0.0 in all
   939 orbits. In fact **no DL-good matching at all** of the n = 22 graph satisfies A5v (0 of 14), and only
   50 of 1,097 across `coll_t1`; with A5v imposed, none of the T1 graphs keeps a law orbit (`ax_eng`, AXV=1).
3. **Not sufficient on its own, as far as is known — and the sufficiency test is inconclusive.**
   The non-T1 law cycles from RP²/Klein seeds (`coll_seeded`, 87 orbits, n = 26–54, levels {2,3}/{2,3,4,5}) satisfy
   A5v at every state, and 79 of them are non-planar. So *law + A5v* does not force planarity. Whether
   *law + A5v* excludes R-cycles (1212…) is open: A5v-constrained annealing (≈ 41M unseeded evaluations, n = 20–26)
   found **no closed orbit of any kind**, but the anti-axiom control (partner on Y, which *has* the T1 family)
   also found none (7.3M unseeded evaluations at n = 22), so this null is **not evidence** (§3).
4. **The interlace axiom A1 is not local: at any one Hamiltonian state it *is* planarity** (with the rotation at v),
   because H ∪ C is all of G. Its local shadow at v (e₀, e₁ chords must not cross) already fails at every
   Hamiltonian state of every T1 orbit (shortest unbalanced cycle = 2; IG has a triangle in all 280 Hamiltonian
   states of `coll_t1`). It holds at 10,493 / 10,493 sphere Hamiltonian states [data] and fails at all 126 RP²/Klein ones.
5. **A3 (Lemma E constants (2,3,3)) is not defined on an abstract matching-form graph.** In the Tait dual, the
   primal pair-graph component counts c_k are face counts of the 2-factors E − M_k, so (2,3,3) is Euler's
   formula for a given face set; with no faces, the only intrinsic version is "genus 0", i.e. A4. TrackN's
   result (no R-cycle meets (2,3,3)) lives in the primal abstraction (general graphs with colourings), a
   different object from TrackU's cubic abstraction. Not tabulated separately here.

**Bottom line.** Planarity enters NRC-M at least through A5v, a one-curve Jordan fact at v. It is the first
candidate that (a) is local, (b) is true on sphere and on RP²/Klein data, and (c) kills all known abstract
R-cycles at every state. The next sharp question is **T1-v**: *no abstract orbit satisfies law + A5v at every
state with word 1212…*. The loop looks viable but needs a stronger search (exact/SAT) to test sufficiency.

## 1. Axiom × counterexample table [data]

"all" = holds at every state of the orbit (Hamiltonian states only for A1). Counts are orbits.

| family (source, TrackU `out/`) | orbits | T1 word | A2 law | A4 planar (rot) | A1 bip IG (rot) at ham. states | A1-local: e₀,e₁ uncrossed | A5v partner on X | A5x X–Y chords uncrossed | ball-planar radius |
|---|---|---|---|---|---|---|---|---|---|
| n22 first (`t1_n22_first.txt`) | 1 | yes | holds | **no** | **no** (0/5) | **no** | **no** (0/10 states) | no (min 2 crossings) | 2 |
| coll_t1 (n = 28, 52 graphs) | 53 | yes | holds | **no** | **no** | **no** | **no** (0 %) | no (some states 0) | 2 |
| t1_first (n = 28) | 1 | yes | holds | **no** | **no** | **no** | **no** | no | 2 |
| walk n = 22 (576 distinct) | 576 | yes | holds | **no** | **no** | **no** | **no** | no | 2 |
| walk n = 28 (300 distinct) | 308 | yes | holds | **no** | **no** | **no** | **no** | no | 2–3 |
| coll_seeded (RP²/Klein seeds, n = 26–54) | 87 | no | holds | no for 79, yes 8 | – (no ham. state) | – | **yes (all)** | yes 11 / no 76 | 2, 3, 6 |
| seed_surf RP² w501 h2 (n = 50) | 1 | no | holds | no | – | – | yes | no | 2 |
| C30#0 h0/h16 (planar control) | 2 | no | holds | yes | – | – | yes | yes | 6 = diam |

All on-disk T1 violators are killed by each of A4, A1, A1-local, A5v and A5x(all states). A2 (the law) kills none.
Among the local ones, **A5v** (one bit per state) and **A1-local** (Hamiltonian states only) are the cheapest;
A5v is the one that is defined at every state and also holds off the sphere.

Ball planarity: every induced ball of radius 2 is planar in every graph above, radius 3 fails for the T1
graphs — so "locally planar to radius 3" also kills them, but that is far less local (diameter 5).

## 2. Truth on planar data [data]

`sphere_check.py`: plantri24 (TrackF), every 100th graph, every degree-5 hole, Tait dual via TrackT `tait_dual`,
all DL-good perfect matchings (`out/sphere_check.txt`):

| data | holes | DL states | A5v | A5x | figure-eight 3-region planarity | ham. states | A1 (bip IG with v-constraints) |
|---|---|---|---|---|---|---|---|
| sphere plantri24 | 1,100 | 48,948 | 48,948 ok | 48,948 ok | 48,948 ok | 10,493 | 10,493 ok |
| RP²/Klein seeds | 6 | 1,672 | 1,672 ok | 1,298 ok | 0 ok | 126 | 0 ok |

(A1 needed the blow-up order fixed: circle … −(e₄)− e₀ e₃ e₁ −(e₂)− …; with the opposite order the test
fails everywhere, and with the side constraints swapped it fails everywhere — so the constraints carry content.)

## 3. Sufficiency search for law + A5v (T1-v) [data, inconclusive]

`ax_eng.c` is a copy of TrackU `tu_eng.c` with one change: env `AXV=1` makes a matching DL-good only if A5v
holds (`AXV=2`: the anti-axiom, partner on Y, as a control; `AXX=1`: also A5x). So any orbit it finds
satisfies the axiom at every state. Runs (`out/axv_*`, `out/ctrl_*`):

| run | evaluations | closed orbits seen | law | T1 |
|---|---|---|---|---|
| AXV=1, mode B, n = 22 / 22 seeded from n22 / 26 (300 s each) | 9.0M / 9.0M / 3.0M | 0 | 0 | 0 |
| AXV=1, mode A, n = 20 (300 s) | 14.8M | 0 | 0 | 0 |
| AXV=1, mode B, n = 24 (240 s) | 4.3M | 0 | 0 | 0 |
| AXV=1, modes B / A seeded from C30#0 (240 s each) | 6.6M / 6.7M | 416k / 418k visits, all L = 20, no Hamiltonian state | all | 0 |
| control AXV=0, mode A, n = 20 (90 s) | 4.2M | 600k visits (5- and 10-cycles) | 0 | 0 |
| control AXV=1 / AXV=2, mode A, n = 20 (90 s) | – | 0 / 0 | 0 | 0 |
| **power control** AXV=2 (anti-axiom, contains the T1 family), mode B, n = 22 unseeded (240 s) | 7.3M | **0** | 0 | 0 |

Longest open A5v-respecting R-run found: 1212121212 (10 states, n = 26, `out/axv_B_n26.jsonl`) — as long as
the unconstrained abstract records, but not closing.

Reading: imposing the axiom (either direction) removes all closed orbits that random annealing can reach,
because it cuts the DL set roughly in half and a closed orbit needs every state to pass. The anti-axiom
control *has* known T1 orbits (the whole TrackU family is anti-A5v) yet is not rediscovered unseeded either.
So these nulls bound nothing. A real test of T1-v needs an exact search (SAT/ILP over graphs + orbit at
n ≤ 22–24); `python-sat`/OR-tools are not installed and that was beyond this budget.

## 4. Is the axiom-discovery loop viable?

Yes, as a cheap filter: in one hour it separated a candidate (A5v) that is local, provably true by a one-curve
Jordan argument, true on all sphere and surface data, and violated at every state of every abstract R-cycle.
It also showed two candidates are *not* local (A1 = planarity at any Hamiltonian state; A3 needs faces) and
one is insufficient (A2). The weak point is step 3: random annealing has no power once an axiom is imposed,
so each candidate needs an exact search, or a proof attempt (does law + A5v + matching dynamics exclude
1212… closure?). A suggestive structural fact for that proof: in every T1 orbit, A5v fails at *all* states
(never mixed), whereas in random abstract graphs single steps flip A5v freely (`out/law_vs_axv_n16.txt`:
A5v does not determine the law step by itself).

## 5. Files

| file | content |
|---|---|
| `ax_lib.py` | independent matching-form engine (PMs, DL, orbits, k(H) words, law) and the axioms: planarity (plain / with rotation), Hamiltonian chord diagram + signed interlace bipartiteness and shortest unbalanced cycle, figure-eight diagram (A5v, A5x, 3-region 2-SAT), ball-planarity radius |
| `run_one.py` | per-graph dump of orbits and axioms |
| `tabulate.py` | axiom × family table; `out/tab_*.jsonl`, `out/tabulate.txt` |
| `sphere_check.py` | axioms at all DL states of sphere / surface holes; `out/sphere_check.txt` |
| `law_vs_axv.py` | step-level relation between A5v and the law in random abstract graphs |
| `ax_eng.c`, `ax_eng` | copy of TrackU `tu_eng.c` with the AXV / AXX filters |
| `out/axv_*.jsonl`, `out/ctrl_*.jsonl` | constrained searches and controls |
