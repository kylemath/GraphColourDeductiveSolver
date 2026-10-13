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

---

# Run 2 (13 Oct 2026, ≈ 11:15–12:25): exact search for T1-v

Exploratory. Labels as above. Compute: ≤ 4 processes, `nice -n 10`, on AC power. Solver: `python-sat`
(CaDiCaL 1.5.3), installed `--user`. Nothing outside `axioms/` changed.

## R0. Verdict

**T1-v has no solution with n ≤ 22, for every orbit length L.** n = 24 is open: the closed L = 10 search timed
out (3,000 s), and a 9-state A5v-respecting 1212 run exists at n = 24.
The pipeline has power: with the axiom bit off or flipped to anti-A5v, the same search refinds the n = 22 T1
counterexample exactly (with 2–9 of its 12 chords pinned, everything else free) and, fully free with
anti-A5v, finds a T1 orbit at n = 22 on its own (a different, non-isomorphic n = 22 graph); and it accepts the planar C30#0 Q-cycle when the word condition is relaxed.

## R1. Encoding (`sat_t1v.py`)

**Normal form (exact, no loss).** Word 1212… means some M_{t−1} ∪ M_t is a Hamiltonian cycle. Rotate t so
that M_0 ∪ M_1 = H is Hamiltonian, rotate the f-labels so that M_0 ∋ f_2, and number the vertices along H:
v = 0, M_0 = {(i,i+1): i even}, M_1 = {(i,i+1): i odd}, f_2 = (0,1), f_0 = (0,n−1). Then
G = H + C where C is a matching of the cubic vertices plus three chords at v (labels f_1, f_3, f_4 free).
Every (G, orbit) with word 1212… has this form; the only labelling freedom left is which Hamiltonian state
is called t = 1. Simplicity: no chord joins H-neighbours. 3-connectivity is **not** assumed.

**Variables.** chord presence x_c (all non-H pairs), labels lab[s][e] for v-edges, matchings y[t][e]
(t = 0,1 fixed), loop membership z[t][u] (u on X_t).
**Eager clauses.** degrees (cubic / 5 at v); each M_t a perfect matching; M_t ∩ M_{t+1} = ∅ (cyclically);
v-edge of M_t is f_{k_t}, k_t = 2 − 2t mod 5 (so L ≡ 0 mod 5; with word 1212, L ≡ 0 mod 10);
z propagates along E − M_t, the frame forces the ends of f_{k±1} into X and f_{k±2} into Y (so the loop
pairing is eager), |X_t| even (XOR chain), and **A5v**: lab[k_t][(0,j)] ⇒ z[t][j] (anti: ⇒ ¬z).
The successor is automatically the unique PM of E − M_t through f_{k−2} once the state is DL-good, so the
orbit is genuinely the deterministic orbit of the TrackU dynamics.
**Lazy cuts (CEGAR), all valid:** a cycle of E − M_t avoiding v (disconnected); a v-loop with wrong
pairing/parity; v's partner on the wrong loop; too many components of M_{t−1} ∪ M_t (w + 1 smallest cycles
blocked) or a Hamiltonian union at an even t (blocked). An eager rank encoding of connectivity
(`eager=2/3/4`) was tried and is 2–10× slower; the runs below use `eager=1`.

**Open windows (`sat_window.py`).** Same encoding without the closing constraint: W consecutive states
M_0..M_{W−1}, M_0 ∪ M_1 Hamiltonian, every state DL-good with the successor rule, word alternating on
t = 1..W−1, axiom at every state. Any closed 1212 orbit (any L) contains, cyclically, windows of every
length starting at a pre-Hamiltonian state. So **window(n, W) UNSAT ⇒ no closed T1-v orbit at that n, of any
length L.**

## R2. Controls [data] (`sat_controls.py`, `sat_power.py`; `out/sat/controls.txt`, `out/sat/power_partial.txt`)

Every SAT orbit is re-found by the independent engine `ax_lib.G5.orbits` (same matchings, same word).

| control | setting | result |
|---|---|---|
| n22 T1 graph, fixed | word 1212, axiom off | 1 orbit, word 1212121212, ax_lib agrees, A5v false at all states |
| n22 T1 graph, fixed | A5v on | UNSAT (0 orbits) |
| n22 T1 graph, fixed | anti-A5v | the same orbit |
| C30#0, both TrackU seed lines (n = 26, planar), fixed | word relaxed, law imposed, L = 20, A5v on | SAT: the known orbit (words 3232…/2323…), ax_lib agrees, A5v at all states |
| C30#0, fixed | anti-A5v | UNSAT |
| **free search, n = 22, L = 10**, T1 in ham normal form, a random fraction of its 12 chords fixed present, everything else free (other chords, labels, M_2..M_9) | 9, 6, 4, 3, 2 chords fixed × 3 seeds | axiom off: **SAT in all 15**, always the T1 chord set exactly (≤ 113 s); anti-A5v: SAT in all 15; **A5v: UNSAT in all 15** (≤ 3.3 s) |
| **fully free, n = 22, L = 10, anti-A5v** (`out/sat/ham_n22_L10_axv2.txt`) | nothing fixed | **SAT after 1,405 s / 64,921 CEGAR rounds: a T1 orbit** (ax_lib: 48 PMs, 16 DL-good, L = 10, word 1212121212, law holds, A5v false at all 10 states, non-planar), on a graph *not* isomorphic to `t1_n22_first` — the free search rediscovers the T1 family on its own |
| fully free, n = 22, L = 10, axiom off | lazy-only first version | not finished (killed after 825 s / 44k rounds to free a core); the anti-A5v run above is the free control |

## R3. Exhaustive results [data] (`out/sat/`)

Closed orbits, word 1212…, free graph (normal form), CaDiCaL proof of UNSAT:

| n | L | axiom | result | time |
|---|---|---|---|---|
| 10, 12, 14, 16 | 10 | none | UNSAT (no 1212 orbit at all) | ≤ 5 s |
| 18 | 10 | none | UNSAT | 47 s |
| 16, 18, 20 | 10 | A5v | UNSAT | 0.1 s, 0.7 s, 12 s |
| 20 | 10 | anti-A5v | UNSAT (no anti-A5v 1212 orbit at n = 20; every known T1 orbit is of this type; mixed-bit orbits not excluded) | 719 s |
| **22** | **10** | **A5v** | **UNSAT** | 362 s |
| 22 | 10 | anti-A5v | SAT (T1 orbit, see R2) | 1,405 s |
| 24 | 10 | A5v | TIMEOUT (732 rounds) | 3,000 s |

Longest open 1212 window W*(n) (window W*+1 is UNSAT; ≥ means the next window timed out):

| n | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 |
|---|---|---|---|---|---|---|---|---|
| no axiom | 4 | 6 | 6 | 7 | 7 | ≥ 9 (W = 10 timed out, 600 s) | ∞ (T1 closes) | ∞ |
| anti-A5v | 3 | 6 | 6 | 6 | 6 | – | ∞ (T1 closes) | – |
| **A5v** | 4 | 4 | 4 | 5 | 6 | **8** | **8** | ≥ 9 (W = 10 timed out, 1,200 s) |

So: **no T1-v orbit of any length for n ≤ 22** (A5v window 9 UNSAT at n = 20 and n = 22, 20 s and 392 s).
At n ≤ 18 this is not specific to A5v: there is no 1212 closed orbit at all there (axiom-off windows are
bounded too). At n = 20 A5v is already discriminating at window level (axiom off: a 9-state 1212 run
exists; A5v: none). The decisive size is **n = 22**: the T1 orbit exists without the axiom (and the free
search finds it), and A5v leaves no 1212 run longer than 8 states.

## R4. The statement, and why it may be provable

**Conjecture T1-v (law + A5v ⇒ no R-cycle).** Let G be a simple graph, cubic except one vertex v of degree 5
with a cyclic order f_0..f_4 of its edges. There is no closed orbit M_0, …, M_{L−1} of DL-good perfect
matchings (M_{t+1} ⊆ E − M_t, f_{k_t − 2} ∈ M_{t+1}) whose word k(M_{t−1} ∪ M_t) alternates 1, 2 and at every
state of which the far end of v's M_t-edge lies on the even loop X_t (equivalently |M_t ∩ E(X_t, Y_t)| odd).
(For word 1212 the chain-parity law holds automatically, so the law adds nothing to this case.)

*Status:* exhaustively true for n ≤ 22, all L (SAT solver UNSAT answers, not independently certified; no DRAT
proofs kept). n ≥ 24 open. False without A5v (n = 22).

**What the data say a proof must use.**
1. *It is not local in time.* All four A5v / anti-A5v patterns occur on two consecutive states of 1212 runs
   (n = 16, 20), and A5v-respecting 1212 runs of length 8 exist at n = 20, 22. A proof cannot be a
   one-step contradiction; it must use a whole frame period (5 steps, 10 states for frame + word).
2. *It is quantitative in n.* W*(n) for A5v grows (4, 4, 4, 5, 6, 8, 8) but stays below the unconstrained
   runs, and the earlier annealing found a 10-state A5v run at n = 26. A natural shape is a potential that
   moves monotonically along A5v-respecting 1212 runs and is bounded by n, so a run cannot close. The two
   obvious candidates, |X_t| and |M_t ∩ E(X_t, Y_t)|, are **not** monotone (checked on all 8 maximal windows
   at n = 18; e.g. |X| = 8, 10, 12, 6, 6, 10).
3. *The uniform failure on T1.* On every known T1 orbit A5v fails at **every** state, while single steps flip
   A5v freely. The sharper (testable) form is: **on a closed 1212 orbit the A5v bit is constant, and it is 0.**
   The constancy half would be a parity invariant transported around the orbit (the bit is the parity
   |M_t ∩ E(X_t,Y_t)|), the value half the Jordan input. Not tested here (an exhaustive mixed-pattern
   search at n = 22 needs the axiom-off free search, which did not finish in this budget).
4. *Normal form for a proof.* At a Hamiltonian state the problem is a chord diagram: H = n-cycle, C a chord
   matching with three chords at v; both Q_0 = M_1 ∪ C and Q_1 = M_0 ∪ C must be figure-eights, and A5v at
   t = 0, 1 says on which loop the H-neighbours 1 and n − 1 of v lie. This is the same chord-diagram setting
   as TrackT's interlace (A1); A5v is its one-curve shadow, so a proof would likely go through the
   interlace/crossing structure of C relative to the two figure-eights and track it over two Hamiltonian
   states (t = 1 and t = 3).

## R5. Files (run 2)

| file | content |
|---|---|
| `sat_t1v.py` | encoding + CEGAR loop; CLI `n L axv [tlimit] [eager]` (closed, word 1212, ham normal form); also fixed-graph mode and per-state axiom patterns |
| `sat_window.py` | open windows; CLI `n W axv word [tlimit] [--dump]`; axv like `12` = per-state pattern |
| `sat_controls.py` | fixed-graph controls (n22 T1, C30#0), re-verified with `ax_lib` |
| `sat_power.py` | partial-fix power control at n = 22 |
| `out/sat/*.txt` | logs of every run quoted above |
| `.gitignore` | compiled `ax_eng` (removed from the index) and caches |
