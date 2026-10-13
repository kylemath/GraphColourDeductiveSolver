# INVARIANTS-1: exhaustive A5v run data, the constancy test, and an invariant hunt

Long Table data/invariant lead, 13 Oct 2026, 12:39–13:55. Exploratory. Labels: **[data]** computed here;
**[hand]** short argument written here, not reviewed; **[conjecture]**.
Compute: at most 3 of my processes at a time, all `nice -n 10`, each run ≤ 15 min, on AC power (100 %).
One enumeration was briefly paused with SIGSTOP to keep the process cap. Its wall-clock limit kept running, so it
timed out early (marked partial below).
Nothing outside `axioms/invariants/` was changed. Read-only inputs: `../sat_t1v.py`, `../ax_lib.py` (copied here as
`inv_sat.py`, `ax_lib.py`), TrackU `out/` graphs, TrackM `tm_lib`, TrackT `tt_lib`, Census33 `out/`,
`~/4square/maps/r178.json`.
The coordinator sent two messages during the run: add the real sphere 8-runs, and A5v = "π is defined". Both are
handled in §4–§5.

## 0. Answers

1. **Sub-conjecture (A5v bit constant on closed 1212 orbits):** proved by exhaustive SAT search for every **n ≤ 20 at
   L = 10**. **n = 22 is still open.** Three different splits (4 × 880 s, plus 19 cubes × 120 s) and the proof
   lead's own run (590 s) all timed out (§2.1).
   - At n = 20 there is no closed 1212 orbit of length 10 at all: with an A5v-true state it is UNSAT (here), and
     anti-A5v everywhere is UNSAT (Run 2).
   - **On other words, constancy needs the law.**
     - Every one of the 5,595 law-respecting closed orbits on disk has a constant bit: 5,454 + 53 T1 orbits are
       all 0; the 87 RP²/Klein-seeded orbits and C30#0 are all 1.
     - 26 of the 60 law-violating closed orbits in TrackU's random/annealed graphs are **mixed**.
     - Without the law, the SAT search finds a mixed closed orbit at n = 16 in 0.3 s. [data]
2. **No monotone quantity in the tested family. There is a reason, and it narrows the search.** [hand, proved §3.1]
   - The involution ι = (time reversal) ∘ (mirror of the rotation at v) maps A5v 1212 runs to A5v 1212 runs.
   - So any potential that is strictly monotone along *all* A5v runs must be **ι-odd (chiral)**.
   - Every size, count, crossing number or area is ι-even, so none of them can work. The data agree: none of 34
     features is monotone. [data]
   - The ι-odd offsets tested drift with a strong bias but are not monotone (§3.2).
3. **How A5v runs die** [data]. A maximal A5v run almost never stops because A5v fails: in 0 of 125 runs of length
   ≥ 7, and in 152 of 4,715 runs overall. It stops because the next complement E − M is not a DL figure-eight.
   - For long runs the most common cause is the **crossed pairing** (k+1, k+3)(k+2, k+4) at v.
   - That pairing cannot occur on the sphere [hand: Jordan]. The sphere runs die by disconnection, by the
     non-crossed wrong pairing, or by k(H) ≥ 3.
4. **Real sphere 8-runs** (p33.r147#128636 h2, p34.r178#11764701 h10, and all 184 order-33 holes with NR ≥ 6):
   transported to matching form, checked state by state against the successor rule, and mined (§4).
   - Both records extend to **9-state** A5v 1212 runs in matching form. The abstract maximum is 8 for n ≤ 22.
   - **"Monotone area" is not supported:**
     - the sides of H_t are pinned at half ± 2;
     - area changes have both signs;
     - persistent chords never change side.
   - **Primal (Kempe) structure:**
     - along every π-run the colour α is one fixed absolute colour, and the other three roles cycle μ → A → B → μ
       with period 3 [hand + 189/189];
     - colour classes stay balanced to within 3 [data];
     - an exact identity 4n_a = V′ + κ_a − c_a + β_a links class size, curvature and chain counts
       [hand + 1,146/1,146];
     - the swap's curvature transfer dκ_α is odd at every step (1,146/1,146).

## 1. Data set [data] (`data/`)

**Enumeration.** `enum_win.py` uses the Run 2 window encoding (Hamiltonian normal form), axiom on or off, and adds a
blocking clause on (chord set, v-labels) after each solution. In this normal form the window is determined by the
graph, so each solution is one (graph, window).
- `feat.maximal_run` extends each window both ways with the matching-form dynamics:
  - succ = the perfect matching (PM) of Q_t through f_{k−2};
  - pred = the PM of Q_t through f_{k+2}.
- The result is then deduplicated by the normal form at the first Hamiltonian pair of the maximal run.

| n | windows with A5v, word 1212 (number of (graph, window); "exh." = solver exhausted) | without axiom |
|---|---|---|
| 16 | W4: 1,390 exh.; W5: 3 exh.; W6: 0 (Run 2) | W7: 5 exh. |
| 18 | W5: 122 exh.; W6: 8 exh.; W7: 0 | W7: 127 exh. |
| 20 | W6: 215 exh.; W7: 3 exh.; **W8: 1 exh.**; W9: 0 | W9: ≥ 1 (partial, timed out) |
| 22 | W6: ≥ 3,000 (cap); W7: ≥ 7 (timeout, partial); **W8: 21 exh.**; W9: 0 (Run 2) | (T1 orbits below) |

**Final data (`data/pass2_runs.json.gz`, `data/pass2_feat.jsonl.gz`).**
- Per run, the runs file stores:
  - the graph line (`n m a0 b0 … f0..f4`, TrackU format);
  - every matching M_t (edge ids), the frames k_t, the A5v bits and the words;
  - the start/end reasons, and the hole and Nch for sphere runs.
- The feature file has one row per state.

| kind | runs | lengths |
|---|---|---|
| `a5`: maximal A5v 1212 runs | 4,715 | n16: 1,384×4, 6×5; n18: 112×5, 10×6; n20: 209×6, 4×7, 1×8; n22: 2,869×6, 99×7, **21×8** |
| `free`: maximal 1212 runs, no axiom | 133 | n16: 5×7; n18: 126×7, 1×8; n20: 1×9 |
| `planar`: sphere near-rigid (NR) runs, matching form (DL-good part) | 190 (189 distinct) | 5–8 |
| `t1`: closed T1 orbits, n = 22 (TrackU `t1_n22_walk.txt`, deduplicated by labelled edge set only) | 5,454 | 10 |

**Graph planarity of the abstract runs.**
- Every A5v run of length ≥ 7 lives on a non-planar graph.
- Of the 3,098 runs of length 6, exactly one is on a graph that is planar with its rotation (n = 22).
- Runs of length ≤ 5 on rotation-planar graphs: n = 16: 468×4, 2×5; n = 18: 16×5.

## 2. Sub-conjecture: on closed 1212 orbits the A5v bit is constant (= 0)

`mixed.py` uses the Run 2 closed encoding with the axiom off, plus an indicator a5[t] built from the eager loop
variables. In every accepted model those variables are the loop membership, because the lazy cuts force a connected
DL figure-eight. The test asks for an orbit with some a5 true; by an even time shift, a5[0] ∨ a5[1].

**Power control.**
- The Run 2 T1 orbit at n = 22 with its chords fixed: "all a5 false" is SAT, and `ax_lib` re-checks the pattern
  0000000000.
- "Some a5 true" on the same chords is UNSAT.

| n | L | test | result | time |
|---|---|---|---|---|
| ≤ 18 | any | – | vacuous: no closed 1212 orbit exists (Run 2 window bounds, axiom off) | – |
| 20 | 10 | some state A5v-true | **UNSAT** | 473 s |
| 20 | 10 | (Run 2) all states anti-A5v | UNSAT | 719 s |
| 20 | 20 | some state A5v-true | TIMEOUT | 880 s |
| 22 | 10 | a5[0] true / a5[1] true (split of "some") | TIMEOUT / TIMEOUT | 880 s each |
| 22 | 10 | a 0→1 transition at t = 0 / t = 1 (WLOG split of "mixed") | TIMEOUT / TIMEOUT | 880 s each |
| 22 | 10 | some state A5v-true, cube-split on the far end j of f_1 (j = 2..20, exhaustive) | see §2.1 | ≤ 120 s per cube |
| 22 | 10 | the proof lead's own mixed run (`../proof/out/mixed_n22_L10.txt`, read only) | TIMEOUT | 590 s |

So the constancy statement holds exhaustively for n ≤ 20, L = 10 [data]. In fact n = 20 has no L = 10 1212 orbit
at all. **n = 22 is open.**

**Other words (`orbit_bits.py`, `data/orbit_bits.txt`; `mixed_pm.py`).**
- Every closed orbit in TrackU's graph files was found with `ax_lib.G5.orbits`.

| orbits | law | A5v pattern |
|---|---|---|
| 53 `coll_t1` (L = 10) + 5,454 T1 walk orbits | holds | all **const 0** |
| 87 `coll_seeded` (RP²/Klein seeds, L = 20) + C30#0 | holds | all **const 1** |
| 60 law-violating orbits (random/annealed n = 16–40, L = 5, 10, 20, plus 12 seeded and 5 surface) | fails | 34 constant, **26 MIXED** |

- Mixed examples (word / bits):
  - 1113111131 / 0100101001;
  - 2211222112 / 1000010000.
- 200 of the 201 orbits in these files have a 5-periodic A5v pattern; the word is 5-periodic in 36 of 60 non-law
  orbits and in 0 of 141 law orbits.
- **SAT, any word (normal form at a PM):**
  - without the law, a mixed closed orbit exists at n = 16, L = 10 (0.3 s; word 3111131111, bits 0010000100);
  - with the law (lazy cuts only): n = 10 UNSAT; n = 12, 14, 16 TIMEOUT at 240 s. The law has no eager encoding
    here, so this test is weak.

**Reading [conjecture C].** *On every closed orbit that satisfies the chain-parity law, the A5v bit is constant.*
- The law (or the 1212 word, which implies it) is essential: without it, mixed orbits are common.
- By the scope agent, A5v = "π is defined". So C says a closed law orbit is either faithful at every state or at
  none.

### 2.1 The n = 22 attempts (all inconclusive)

| split of "some state A5v-true" (L = 10) | result |
|---|---|
| t0 / t1 | TIMEOUT / TIMEOUT, 880 s each (about 19k–21k CEGAR rounds) |
| P / Q (0→1 transition at t = 0 / 1) | TIMEOUT / TIMEOUT, 880 s each |
| 19 cubes on the far end j of the f_1 chord (`cubes.sh`; j = 2..20 is exhaustive in the normal form) | j = 2 and j = 20: UNSAT by unit propagation; the other 17 cubes: TIMEOUT at 120 s each (`data/cubes_n22_w*.txt`) |

A decision at n = 22 needs either much longer runs (Run 2's fully free n = 22 searches took 362 s to 1,405 s, and
this problem is harder) or a stronger eager encoding of connectivity and of the word.

## 3. Mining for a monotone quantity [data unless marked]

**Features.** `feat.state_features` computes these per state; `planar_features` adds the sphere-only ones.
- Frame and A5v bit; |X_t|, |Y_t|; the X–X, Y–Y and X–Y edge counts of M_t.
- Position of v's partner along X (pX) and along Y (pY).
- Crossings of v's M-chord in the figure-eight diagram; X–Y crossings; 3-region planarity of the figure-eight.
- Overlaps Y_t ∩ Y_{t+1}, X_t ∩ X_{t+1}, X_t ∩ Y_{t+1}, Y_t ∩ X_{t+1}, and |Y_t Δ Y_{t+1}|.
- At Hamiltonian states:
  - crossings of the chord diagram, interlace components, bipartiteness with and without the rotation, shortest
    unbalanced cycle;
  - minimum number of chords to delete to make the interlace graph bipartite (brute force, ≤ 16 chords);
  - circle positions of the far ends of e0, e1, e3, and the crossings of each.
- Sphere only: the face areas of the regions R_X, R_Y, R_O and of both sides of H_t.

`analyze.py` (`data/pass2_monotone.txt`) checks 1-step and 2-step differences, split by state class. Apart from
trivial identities (the frame step of −2, constant bits inside their own run kind), **no feature is monotone on all
runs of any kind**.

### 3.1 Why sizes and areas cannot work: the chirality lemma [hand]

Let ι reverse time and mirror the rotation at v (f_s ↦ f_{−s}).
- The DL pairing (k±1)(k±2) maps to the DL pairing of −k; X and Y are kept as sets; parities and A5v are kept.
- The predecessor rule "PM of Q_t through f_{k+2}" becomes the successor rule "through f_{k′−2}" with k′ = −k.
- Words are kept, read backwards.

So ι maps A5v 1212 runs, closed orbits, law orbits and sphere runs to runs of the same kind. Suppose Φ is ι-even and
strictly increasing along every A5v run of length ≥ 2. Then along the ι-image of a run, Φ would decrease, which is a
contradiction. Hence **a potential for T1-v must be chiral (ι-odd)**: it must see the orientation of the rotation at
v or the direction of time. The following are ι-even and therefore excluded in advance:
- loop lengths and loop sizes;
- chord counts and crossing numbers;
- interlace statistics;
- face areas, including both sides of H_t.

Several long A5v runs are literally ι-symmetric:
- the n = 20 eight-run has |X| = 14, 10, 10, 14, 14, 10, 10, 14;
- in the same run, h_e0(t) + h_e1(R − t) = n − 2.

### 3.2 Chiral offsets (`oddfeat.py`, `data/pass2_oddfeat.txt`)

Definitions:
- sX = 2·pX − (|X| − 1);
- sE = h_e0 + h_e1 − (n − 2);
- dE = h_e0 − h_e1;
- s3 = 2·h_e3 − (n − 2), at Hamiltonian states.

Counts of positive : negative changes:

| run kind | sE, 2-step | s3, 2-step | sX, 2-step |
|---|---|---|---|
| A5v runs | 2,211 : 5,635 | 5,258 : 2,501 | 5,997 : 8,630 |
| sphere runs | 117 : 173 | 202 : 87 | – |
| T1 orbits | balanced by closure | balanced by closure | – |

- The bias has the same sign on abstract A5v runs and on sphere runs for sE and s3.
- None of these is monotone: 1,889 of 4,715 A5v runs are mixed in sE.

### 3.3 What predicts the end of an A5v run (`ml.py`, `data/pass2_ml.txt`)

Label = "this state is the last of its maximal run", over 20,836 states.
- Best single-feature split: w(t) = 1, i.e. runs end right after a Hamiltonian state. Balanced accuracy 0.73.
- Class-weighted logistic regression on all local features: 0.75.
- Run length alone: 0.84. This is a trivial cue.

So the stopping point is **not a local function** of the state.

**End mechanism** (`endmech.py`, `data/pass2_endmech.txt`). The first state beyond the end (successor of the last
state, or predecessor of the first) is classified as follows.

| | crossed pairing (k+1,k+3)(k+2,k+4) | wrong planar pairing (k+1,k+2)(k+3,k+4) | E − M disconnected | wrong word | A5v false |
|---|---|---|---|---|---|
| A5v runs, all (end) | 993 | 2,569 | 672 | 329 | 152 |
| A5v runs, length ≥ 7 (end / start) | **54 / 69** | 42 / 36 | 6 / 10 | 23 / 10 | **0 / 0** |
| sphere runs (end) | **0** | 27 | 161 | 2 (k(H) = 3, 4) | 0 |

The crossed pairing means the two loops of E − M cross at v. On the sphere that is impossible: two closed curves
meeting once, transversally, would have odd intersection number [hand, Jordan]. Abstract long A5v runs end there most
often; sphere runs never do.

### 3.4 Order of v's chord ends along H (`patt.py`, `data/pass2_patt.txt`)

The pattern is the order of the far ends of e0, e1, e3 along H_t, read from the f_k side.
- **T1 orbits:** always `031` (27,270 / 27,270 Hamiltonian states). e0 comes first, e3 in the middle, e1 last:
  the e0 and e1 chords cross, with e3 nested between them. This is a fixed point of the pattern dynamics, and the
  closing mechanism of every T1 orbit uses it.
- **Sphere:** only `310`, `103` and `130` occur: e1 is always before e0, which is A1-local [hand: forced by
  planarity with the rotation].
- **A5v runs:** all six patterns occur. The crossing patterns `301`, `031` and `013` make up 2,878 / 12,663.

So A5v alone does not force A1-local. It does prevent the fixed `031` regime that T1 needs.

## 4. Real sphere runs (coordinator priority 1) [data]

`planar_runs.py`, `primal_feats.py`, `curv_track.py`, `planar_stats.py`, `primal_stats.py`, `curv_stats.py`.

**Pipeline.**
- TrackM `tm_lib.Hole` gives the π-runs of DL states with Nch ≤ 9 (the Census33 NR definition).
- TrackT `tait_dual` gives the dual G5 with the primal edge of every dual edge.
- Transport: M_t = {dual edges with c(u) xor c(w) = α xor A}, whose v-edge is f_{j+2}.
- All 190 run records pass two checks: M_t is a PM containing f_{j+2}, and succ(M_t) = M_{t+1} in matching form.
- p33.r147 h2 gives Nch 8,9,8,…, word 2,1,2,…; p34.r178 h10 gives Nch 9,8,…, word 1,2,…; both are 8 states long.
- **Extended in matching form** (DL-good, word alternating; A5v is automatic), **both records reach 9 states.**
- 7 other holes reach 8; most NR = 6 holes reach 7.

**(a) Sides of H_t at Hamiltonian states (482 states, 292 two-step pairs).**
- Side A, which holds x_{k+1} and x_{k+2}, is the αμ tree: hA = n_α + n_μ. Side B is the AB tree. Checked at
  482/482 states.
- hA − hB ∈ {0: 316, ±2: 156, ±1: 4, ±4: 6}, so the sides are pinned at half.
- hA(t+2) − hA(t) ∈ {0: 160, +1: 67, −1: 42, ±2: 21, ±3: 2}. Both signs occur, so the area is **not monotone**.

**(b) Loops at v.**
- Q_t always has exactly 3 face regions, and they are consistent with the frame (1,105/1,105):
  - R_X = K_{αA}(x_{j+2}): the region holding f_k, the π swap chain;
  - R_Y = K_{αA}(x_j);
  - R_O = K_{μB}.
- Which side of each loop v's five edges lie on is fixed by the frame at every state [hand]:
  - X separates f_k from f_{k±2};
  - Y has f_{k±2} adjacent, with f_{k−1}, f_k, f_{k+1} on the other side.
- So the local turning data carry no information beyond k_t. The only winding data are:
  - the frame step −2 (period 5);
  - the role cycle μ → A → B (period 3, below).
- |R_O| = ⌊(faces − 1)/2⌋ + {−1..3} at every state; aX alone is non-monotone in 190/190 runs.

**(c) Chords between Hamiltonian states t and t+2 (292 steps).**
- Persistent chords **never change side** (0 of 2,097).
- Chords leaving and entering a side balance: (out_A, out_B, in_A, in_B) = (15,13,15,13), (15,14,15,14), …
- So the side areas move by at most 3 per step.

**Primal Kempe features (coordinator priority 3; 189 runs, 1,146 states).**
- **α is invariant and the roles rotate** [hand + 189/189 runs].
  - π swaps α ↔ A on K = K_{αA}(x_{j+2}). This chain contains x_{j+3} and, because π is defined, not x_j.
  - The new link is (α, μ, A, α, B) with new frame j+3. So α′ = α, μ′ = B, A′ = μ, B′ = A.
  - In absolute colours, π always swaps the same colour α with a partner that cycles through the other three with
    period 3.
  - The frame has period 5 and the roles have period 3. On a closed orbit of length 10 the colouring therefore comes
    back relabelled by a 3-cycle fixing α. That 3-cycle is an affine map of Z₂², so this gives **no** obstruction.
- **Class sizes are balanced.** max − min ∈ {0: 406, 1: 8, 2: 711, 3: 21}; for example 8,8,8,8 at V′ = 32.
  - The swap chain is balanced too: |K∩A| − |K∩α| ∈ [−2, 3], with 0 at 616 of 1,146 states.
- **Exact identity** [hand + 1,146/1,146]. Notation, in T − h:
  - V′ = number of vertices, deg′ = degree;
  - κ_a = Σ_{v of colour a} (6 − deg′ v);
  - c_a = number of Kempe chains touching a, summed over the three pairs ab;
  - β_a = the summed cycle ranks of those pair graphs.

  Then

  **4 n_a = V′ + κ_a − c_a + β_a.**

  *Proof:* Σ_{v∈a} deg′ v = Σ_b e_ab and e_ab = n_a + n_b − c_ab + β_ab. Pure counting; no planarity is used.
- **The swap moves an odd amount of curvature.** dκ_α ∈ {±1: 633, ±3: 339, ±5: 132, ±7: 34, ±9: 7, 11: 1}, odd
  at all 1,146 steps.
  - [hand] dκ_α ≡ κ(K) ≡ (number of T − h edges leaving K) (mod 2).
  - With the identity, 4·Δn_α = dκ_α − Δc_α + Δβ_α, so Δc_α − Δβ_α is odd at every step.
  - [conjecture] This is the chain-parity law in curvature form.
- κ_α (absolute) is non-monotone in 189/189 runs: for example 9,6,5,6,5,6,5,2 on the p33 record.
- Lock lengths are non-monotone in 184/189 runs.
- All chain counts lie in (am,aA,aB,mA,mB,AB) ∈ {(1,2,2,1,1,1), (2,2,2,1,1,1), (1,2,2,1,2,1), (1,2,2,2,1,1)}.

## 5. Suggested lemmas for the proof lead

1. **Chirality lemma (proved, §3.1).** The set of A5v 1212 runs (and of law orbits, and of sphere runs) is invariant
   under ι = time reversal ∘ mirror. Any potential that moves one way along all such runs must be ι-odd.
   - Do not spend time on areas, loop lengths, crossing numbers or chord counts: they are ι-even.
   - Candidates must use the orientation of the rotation at v. Examples:
     - the signed positions s3 and sE of the v-chord ends along H_t (biased 2:1 in the same direction on abstract
       and sphere runs);
     - the interplay of the frame step (−2 mod 5) with the role cycle (+1 mod 3).
2. **Constancy (conjecture C, §2).** On a closed law orbit, the A5v bit (= "π defined") is constant.
   - Proved by exhaustive search for 1212 at n ≤ 20, L = 10.
   - Holds on all 5,595 law orbits on file.
   - **Fails without the law** (26/60 mixed). A proof must use the parity law. The mixed non-law orbits have period-5
     words, which the law forbids; that is the place to look.
   - What C is for [hand]: genuine colouring orbits are A5v at every state ("π defined"), so T1-v alone already
     excludes genuine R-cycles; C is not needed for that. C matters as a mechanism. If the A5v bit is conserved
     around law orbits, the proof of C is a parity transport using the law, and that transport may be exactly what
     T1-v needs. C together with T1-v says every abstract R-cycle is unfaithful at every state; it never touches a
     faithful state.
3. **Exit through the crossed pairing (data lemma, §3.3).** A long A5v run never ends by losing A5v (0/125 runs of
   length ≥ 7). It ends because E − M_{t+1} stops being a DL figure-eight, most often through the pairing
   (k+1,k+3)(k+2,k+4), which is Jordan-forbidden.
   - Suggested target lemma: **A5v at t−1, t and the 1212 word force the successor complement into one of three
     types:** DL, the non-crossed wrong pairing, or the crossed pairing.
   - On the sphere the third type is impossible. So a planar proof only has to exclude a long chain of DL states that
     avoids the second type.
   - Together with the pins of §4 (sides of H at half ± 2, balanced Kempe classes), this is where the exhaustion
     comes from: runs end, they do not drift.

## 6. Files

| file | content |
|---|---|
| `inv_sat.py`, `ax_lib.py` | copies of `../sat_t1v.py`, `../ax_lib.py` (unchanged) |
| `enum_win.py`, `batchA.sh`, `batchB.sh` | window enumeration with graph blocking clauses |
| `mixed.py` | closed 1212 orbits with an A5v indicator: modes `any`, `mixed`, `t0`, `t1`, `P`, `Q`, `allfalse`; optional fixed chords (power control) |
| `cubes.sh` | runs `mixed.py` cube by cube (env `CUBE` = far end of the f_1 chord) |
| `mixed_pm.py` | closed orbits of any word (normal form at a PM), optional lazy law, mixed A5v |
| `feat.py`, `build_data.py` | dynamics (succ, pred, maximal runs), normal-form dedup, per-state features → `data/pass2_*` |
| `analyze.py`, `oddfeat.py`, `ml.py`, `endmech.py`, `patt.py`, `show.py` | the analyses of §3 (outputs `data/pass2_*.txt`) |
| `orbit_bits.py` | A5v patterns of every closed orbit in TrackU files (`data/orbit_bits.txt`) |
| `planar_runs.py`, `planar_stats.py` | sphere NR runs → matching form; (a)–(c) (`data/planar_*.jsonl`, `data/pass2_planar.txt`) |
| `primal_feats.py`, `primal_stats.py`, `curv_track.py`, `curv_stats.py` | Kempe-chain features, absolute-colour tracking, the curvature identity (`data/primal_*`, `data/curv_*`) |
| `data/win_*.jsonl` | raw SAT windows (graph line + M_t); `data/mixed_*.txt`, `data/cubes_*.txt`, `data/mixed_pm_law_L10.txt` logs; `data/controls.txt` (power controls); `data/batch*.log` |
