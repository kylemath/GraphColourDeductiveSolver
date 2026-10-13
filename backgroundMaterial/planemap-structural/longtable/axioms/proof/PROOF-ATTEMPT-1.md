# Proof attempt 1 on T1-v / NRC (Long Table, 13 Oct 2026, 12:39–13:30)

Exploratory. Labels: **[proved, hand]** argument written here, not independently reviewed;
**[data]** computation here (SAT answers are CaDiCaL 1.5.3 verdicts, no DRAT proofs kept);
**[conjecture]**. Nothing outside `axioms/proof/` was changed. Read-only reuse: `../sat_t1v.py`,
`../sat_window.py`, `../ax_lib.py` (copied or imported), TrackT `tt_lib` (Tait duals), census maxima files.
Compute: ≤ 3 processes, `nice -n 10`, every run ≤ 10 min, on AC power (`pmset`: charged).

## 0. Verdict

1. **No proof of T1-v or NRC.** Every candidate potential and every one-state lemma tested is dead (§3).
2. **New exact planar search [data].** I added an exact planarity encoding to the SAT normal form
   (`sat_planar.py`; §1.3, checked both ways). With it, NRC-M itself, not the A5v proxy, can be searched
   exhaustively:
   - **No near-rigid π-cycle (R-cycle) of any length exists in any simple plane graph with n ≤ 24.**
     Planar window 7 is UNSAT at n = 22 and 24, and window 6 is UNSAT at n ≤ 20.
   - Closed L = 10 is UNSAT at n ≤ 26.
   - Planar runs are much shorter than A5v runs. The longest planar 1212 window is 4, 4, 4, 5, 5, 5, 6, 6 at
     n = 10, …, 24. The A5v windows are 4, 4, 4, 5, 6, 8, 8 at n = 10, …, 22.
   - So A5v (which is just ¬inA, as the scope agent showed) captures only a small part of the planar input.
3. **New phenomenon, the main finding: the R0 relaxation [data → Conjecture R0].**
   - Drop *everything* except these conditions:
     - perfect matchings M_0, …, M_{L−1};
     - consecutive ones disjoint, cyclically;
     - the v-edge of M_t is f_{k_0 − 2t};
     - M_0 ∪ M_1 is a Hamiltonian cycle.
   - There is no DL condition, no figure-eight connectivity, no A5v, no k(H) word after t = 1, and the successor is not unique.
   - **With planarity this is UNSAT for every n tested (8–26 at L = 10, up to 22 at L = 20; L = 5, 15 at n = 14)
     and for all 18 rotation variants at v.** Without planarity it is SAT immediately at every n.
   - The obstruction is about **closure**: open R0 sequences of length 10 exist at n = 22 (11 at n = 24), but closed ones do not.
   - The Hamiltonian pair is essential: the planar C30#0 Q-cycle is a closed R0 sequence with L = 20 and no
     Hamiltonian pair.
   - R0 ⇒ NRC trivially. If R0 holds, NRC needs only "perfect matchings + one Jordan curve + closure".
4. **Two small structural lemmas [proved, hand], confirmed on data.**
   - **A5v ⟺ the vertex matched to v bounces back:** M_{t+1}(w) = M_{t−1}(w).
   - **Lemma FE (far ends):** on a closed orbit, the matched-edge word of each neighbour w_s of v is forced, and
     **the number of A5v states among the visits of w_s is even**. For L = 10 this means b_t = b_{t+5}.
     - Under A5v the five neighbours of v have winding 0.
     - On the T1 family they wind ±L/5 (checked: both n = 22 T1 orbits, all five far ends |ρ| = 2; C30#0, all ρ = 0).
   - This is the precise sense in which "the twist at v propagates to its neighbours" in the T1 family but not
     under A5v. That answers the "what breaks for T1" question at the first ring.
5. **Coordinator leads.**
   - **Lead B (area monotone) is killed** on genuine sphere data: area_in changes by −2…+2 with both signs.
   - **Lead A (turning numbers)** reduces to Tait sign sums.
     - The rotation of w's matched edge at step t equals −s_{t+1}(w) [proved].
     - The mod-3 Heawood count at v closes automatically for every frame: Σ_t c_t(f) = L [proved].
     - So no turning-number contradiction exists at the mod-3 level. A frame-pattern table (§5.3) also shows that
       R0 closure is not decided by v's net turning.

## 1. Setting and normal form

### 1.1 Objects

- G is simple, cubic except one vertex v of degree 5 with edges f_0..f_4 in cyclic order. In the planar case the rotation is ccw.
- The orbit is M_t, t ∈ ℤ/L, a sequence of DL-good perfect matchings.
  - Q_t := E − M_t = X_t ∪ Y_t is a figure-eight. X_t runs through f_{k±1} and is even; Y_t runs through f_{k±2} and is odd. Here f_{k_t} ∈ M_t.
  - The frame moves by k_{t+1} = k_t − 2.
- The word is w_t = k(M_{t−1} ∪ M_t) = 1, 2, 1, 2, ….
- Frame-relative names at state t: e_i := f_{k_t − 2 + i}. So e_2 ∈ M_t, e_4 ∈ M_{t−1}, X_t ∋ e_1, e_3 and Y_t ∋ e_0, e_4.
- A5v(t): the partner of v in M_t (the far end of e_2) lies on X_t.

### 1.2 Hamiltonian normal form

- Two numberings are used.
  - **SAT numbering** (`sat_t1v.py`). At t = 1, H = M_0 ∪ M_1 = cycle 0, 1, …, n−1 with v = 0. M_0 consists of the even edges and contains f_2 = (0,1); M_1 consists of the odd edges and contains f_0 = (0, n−1). G = H + C, where C is a matching of the cubic vertices plus the chords f_1, f_3, f_4 at v.
  - **Frame numbering** (used in proofs). At a Hamiltonian state t, number H from the e_2-neighbour: position 1 is the far end of e_2 ∈ M_t, and position n−1 is the far end of e_4 ∈ M_{t−1}. The positions of the far ends of e_0, e_1, e_3 are p_0, p_1, p_3.
- In frame numbering:
  - Y_t is the loop of M_{t−1} ∪ C that starts v → n−1.
  - Y_{t−1} is the loop of M_t ∪ C that starts v → 1.
  - **A5v(t) ⟺ 1 ∉ Y_t, and A5v(t−1) ⟺ n−1 ∉ Y_{t−1}** [proved, hand: direct from the definitions].

### 1.3 Planarity as a chord-diagram condition (`sat_planar.py`)

**Planar circle rule [proved, hand].**
- G is planar with rotation f_0..f_4 at v (up to mirror) iff two conditions hold:
  - the chord diagram on the circle 1, 2, …, n−1, [f_4], [f_1], [f_3] has a side 2-colouring with no two same-side chords crossing; v is blown up between n−1 and 1, with H entering v by f_0 from n−1 and leaving by f_2 to 1;
  - side(f_1) ≠ side(f_3) = side(f_4).
- Proof: draw H horizontally through v. In the ccw rotation f_0 (left), f_1, f_2 (right), f_3, f_4, the edge f_1 lies alone below H. Above H, f_4 lies nearer the f_0 end and f_3 nearer the f_2 end. Blow v up along H, and use the standard fact that planarity of a Hamiltonian graph is a non-crossing two-sided chord drawing. This is TrackT's [via e₂] e₁ e₃ e₀ [via e₄] in SAT labels.

Checks [data]:
- **Positive control.** The rule holds at **1,244 / 1,244** genuine sphere Hamiltonian states (all near-rigid windows at all degree-5 holes of the 12 Census34 maxima graphs; `control_planar_rule.py`).
- **Soundness.** Every SAT window found with the rule is planar with the rotation, by an independent networkx 5-wheel-gadget test (`check_planar.py`). All 9 A5v windows of maximal length at n = 18, 20 are non-planar.
- **Closure is not over-constrained.** With frame patterns that permit closure, planar closed sequences are found (period 2 at n = 12, 16, 20; period 4 and (2,0,lone) at n = 16). They are verified independently: perfect matchings, disjointness, frames, Hamiltonian M_0 ∪ M_1, `planar_rot` True (`relax2.py --verify`).

## 2. Step rules [proved, hand]

All of these hold in any graph unless marked planar.

**R1 (S3, TrackS).** M_{t+1} = M_{t−1} Δ Y_t. Hence:
- H_{t+1} = H_t Δ Y_t;
- Q_{t+1} = H_t Δ X_t = M_t ∪ C_{t+1};
- M_{t+1} = (M_{t−1} ∩ X_t) ∪ (C_t ∩ Y_t), so **M_{t+1} has no X_t–Y_t edge**.

**R2 (two steps, TrackT Φ4).**
- H_{t+2} = H_t Δ (Y_t Δ Y_{t+1}).
- The frame index of the Hamiltonian states advances by +1 per Φ-step.
- At a Hamiltonian state with frame k, the far ends w_s of f_s play these roles:
  - w_k sits at position 1;
  - w_{k+2} sits at position n−1;
  - w_{k+1} is the lone chord e_3;
  - w_{k+3} and w_{k+4} are e_0 and e_1.
- Each v-edge cycles through these roles e_1 → e_0 → e_4 (∈ H) → e_3 (lone) → e_2 (∈ H) → e_1, one per Φ-step.

**R3 (local vertex rule).** For a cubic vertex w:
- if w ∈ X_t, then M_{t+1}(w) = M_{t−1}(w) ("back");
- if w ∈ Y_t, then M_{t+1}(w) is the third edge ("rotate").

So the matched-edge word of w has no two equal consecutive letters, and each "back" reverses the direction of rotation. On a closed orbit:
- w lies on an even number of the loops X_t;
- the winding ρ(w) satisfies 3ρ ≡ L (mod 2), so ρ(w) ∈ {−2, 0, 2} for L = 10.

**R4 (A5v as bounce-back).** Let w be the partner of v in M_t. Then A5v(t) ⟺ w ∈ X_t ⟺ M_{t+1}(w) = M_{t−1}(w). Proof: R3.

**Lemma FE (far-end words).** Fix s and let w = w_s. Let t_s be a visit, i.e. f_s ∈ M_{t_s}, and put τ = t − t_s.
- (a) The DL frame forces the membership of w: **X at τ ≡ 2, 3 and Y at τ ≡ 1, 4 (mod 5)**. At τ ≡ 0, w ∈ X iff A5v(t). This is because s − k_t ≡ 2τ, and w_{k±1} ∈ X_t, w_{k±2} ∈ Y_t.
- (b) So by R3 the word of w is a concatenation of blocks f x y x y, where {x, y} are the other two edges at w. The next block keeps (x, y) if the visit at its start is anti-A5v, and swaps it if that visit is A5v.
- (c) **Closure ⇒ the number of A5v visits of each w_s is even. For L = 10: b_t = b_{t+5} for all t.**
- (d) The winding of w_s is (#blocks with one orientation − #blocks with the other). It is 0 when A5v holds at all visits and ±L/5 when anti-A5v holds at all visits.

*Proof.*
- (a) Frame arithmetic: k_t = s − 2τ.
- (b) Apply R3 at τ = 1, 2, 3, 4: rotate, back, back, rotate. This gives f, x, y, x, y, f. At τ ≡ 0, the step back gives the next letter = y (swap), and the step rotate gives the next letter = x (keep).
- (c) After L/5 blocks the orientation must return.
- (d) Each block is +1 or −1 turn. ∎

The proof uses neither the 1212 word nor Hamiltonicity. Data:

| orbit | far-end windings |
|---|---|
| `t1_n22_first` | (−2, −2, 2, 2, 2) |
| the SAT-found n = 22 anti orbit | (2, 2, 2, −2, −2) |
| C30#0 (L = 20, planar, all A5v) | (0, 0, 0, 0, 0) |

The block patterns are as predicted (`farend_check.py`). Over all vertices, the T1 orbits have |ρ| = 2 at 11 of 21 cubic vertices (`winding_all.py`).

Consequence: **in a closed orbit with L = 10, the A5v bit pattern is 5-periodic.** "Mixed" orbits therefore reduce to 6 necklace classes, `run_patterns.py`. Two consequences of FE for A5v orbits:
- Two far ends w_s ≠ w_{s'} are never adjacent. A shared edge would need occupation t_s + {1,3,7,9} = t_{s'} + {1,3,7,9} or t_{s'} + {2,4,6,8} (mod 10), which forces t_s ≡ t_{s'} (mod 5).
- In the primal, adjacent consecutive far ends would mean a degree-4 link vertex. This is consistent with known facts and adds nothing at minimum degree 5.

**R5 (planar sign identity).** Let s_t(w) = ±1 be the Tait sign of (C_t, M_t, M_{t−1}) at w. Then:
- the rotation of the matched edge from M_t(w) to M_{t+1}(w) is −s_{t+1}(w) notches;
- hence ρ(w) = −(1/3) Σ_t s_t(w);
- s_{t+1} = −s_t on X_t, and s_{t+1} = s_t on Y_t.

**R6 (Heawood at v closes automatically).** Heawood at the face in corner (f_{i−1}, f_i) reads Σ_{w∈F−v} s_t(w) ≡ c_t(f_{i−1}) − c_t(f_i) (mod 3), where c_t(f) is 2, 0 or 1 as f is the M_t-edge, the M_{t−1}-edge, or a chord.
- For any frame sequence, Σ_t c_t(f) = 2a_f + (L − 2a_f) = L for every f, where a_f is the number of visits of f.
- So summing over a period gives no constraint, and Lead A gives nothing at the mod-3 level.
- This matches TrackS's negative Heawood result.

## 3. Tested lemmas

"n-range" is where the lemma was tested exhaustively (SAT enumeration of all windows) or on genuine sphere data.

| # | candidate | status | evidence |
|---|---|---|---|
| L1 | A5v at the two states sharing a Hamiltonian state ⇒ e_0, e_1 uncrossed (A1-local) | **killed** | crossed Hamiltonian states under A5v: n = 14: 12 / 222; n = 16: 240 / 2,780; the unique n = 20 W = 8 A5v window is crossed at t = 3, 5 (`lemma_test.py`, `show_win.py`) |
| L2 | some order type of (p_0, p_1, p_3) is forbidden under bits (1,1) | **killed** | all 6 types occur at n = 16 and 18 (n = 18: 1,825 / 1,404 / 16,827 / 1,744 / 1,825 / 16,827); the bits (0,1) and (1,0) are mirror images (`ham_patterns.py`) |
| L3 | **Lead B**: area inside H_t (faces on the e_3 side) is monotone along Φ | **killed** | 168 genuine sphere windows (Census33/34 maxima graphs, all holes, plus TrackS notable6 holes), 308 Φ-steps: Δarea = −2: 3, −1: 65, 0: 175, +1: 64, +2: 1. Both signs occur on the record windows, e.g. p34.r84#650604 h2 gives 18, 17, 16, 16 and p34.r51#808692 h26 gives 16, 17, 16, 16. Reason [proved, hand, Euler]: area_in = (n − 2 + Σ_{inside faces}(6 − deg_G f))/4, so the area is the inside curvature, and near-regular degree pins it at about V/2 |
| L4 | the lone-chord slot (p_3 left of p_1, between, or right of p_0) moves deterministically | **killed** | all 9 transitions occur (308 sphere Φ-steps) |
| L5 | any integer combination a·F_i + b·F_j (\|a\|, \|b\| ≤ 2) of 12 Hamiltonian-state features (area, \|X\|, \|Y\|, \|D_X\|, \|D_Y\|, \|O\|, p_0, p_1, p_3, gaps) is monotone along Φ | **killed** | only the trivial invariants \|X\| + \|Y\| = n − 1 and p_0 + (n − p_0) hold (`potential_search.py`) |
| L6 | \|O_t\| (the μB region) is invariant | **killed** | almost constant at about V/2 but moves by −3…+3 |
| L7 | A5v ⇒ planar-length runs | **killed** | A5v and A1-local at every Hamiltonian state still allow 6-state windows at n = 20 (90 of 215 A5v windows); planar windows stop at 5 there; 0 of the 215 are planar |
| L8 | on a closed 1212 orbit the A5v bit is constant | **half proved** | 5-periodicity is FE(c) [proved]. Full constancy is open: the mixed search at n = 22 timed out (590 s, 25k CEGAR rounds); pattern 00001 at n = 22 timed out (300 s); the other 5 classes were not run |
| L9 | Lemma FE / R4 | **proved** | §2; data as listed |
| L10 | **R0 closure obstruction** | **survives** | §5 |

## 4. Exact planar search [data] (`sat_planar.py`, `out/planar_*.txt`)

Planar 1212 windows (W states, M_0 ∪ M_1 Hamiltonian, every state DL with the successor rule, word alternating):

| n | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 |
|---|---|---|---|---|---|---|---|---|---|---|
| planar W* | 4 | 4 | 4 | 5 | 5 | 5 | 6 | 6 | ≥ 6 (W = 7 TIMEOUT, 435 s) | ≥ 6 (W = 7 TIMEOUT, 401 s) |
| A5v W* (README run 2) | 4 | 4 | 4 | 5 | 6 | 8 | 8 | 9 (Studio) | | |

Closed planar L = 10: UNSAT at n = 20, 22, 24, 26 (2 s, 11 s, 68 s, 403 s). Each was refuted by the eager clauses alone, with 0 CEGAR rounds.

**Result [data].** No simple plane graph G (v of degree 5, all others cubic) with n ≤ 24 carries a near-rigid π-cycle of any length. A closed 1212 orbit contains windows of every length starting at a pre-Hamiltonian state, and planar W = 7 (n = 22, 24) and W = 6 (n ≤ 20) are UNSAT.
- In triangulation terms n = 2V(T) − 8, so this is V(T) ≤ 16, with all triangulations included: not only the frame class, and not necessarily 3-connected.
- This is weaker than the census, which goes to V = 34 in the frame class. Its value is that it is a **free-graph exact search with planarity built in**, so planar lemmas can be tested exhaustively at small n.
- The genuine sphere records (NR = 8–9 at n = 58–60) and planar W* = 6 at n = 24 are consistent with slow growth. The Studio's A5v W* = 9 at n = 24 vs planar 6 shows how much A5v misses.

## 5. The R0 phenomenon (`relax_test.py`, `relax2.py`, `r0_dump.py`)

### 5.1 Statement tested

R0(n, L): G = H + C in the normal form, planar by §1.3. M_0, M_1 are fixed (H Hamiltonian), and M_2, …, M_{L−1} are perfect matchings with M_t ∩ M_{t+1} = ∅ (cyclically) and v-edge f_{2−2t}. Nothing else: no z-loops, no DL pairing, no parity, no A5v, no connectivity, no word. Pure SAT, no cuts.

| test | result |
|---|---|
| closed, L = 10, planar | **UNSAT at n = 8, 10, …, 26** (n = 22: 22 s; n = 24: 111 s; n = 26: 619 s, slightly over the 10-min cap) |
| closed, L = 10, non-planar | SAT at every n = 8…20 (instant; one decoded example verified: PMs, disjointness, frames, Hamiltonian M_0 ∪ M_1, `planar_rot` False) |
| closed, L = 5, 15 (n = 14); L = 20 (n = 12, 14, 16, 18, 20, 22; n = 22 in 30 s), planar | UNSAT |
| closed, L = 10, all 18 placements of f_1, f_3, f_4 around v with H through f_0, f_2 (n = 14); lone f_3 or f_4 (n = 18, 20) | UNSAT |
| levels R1–R3 (add z-propagation, which forces the DL pairing on the v-component; then parity; then A5v), planar, n = 16 | UNSAT (already R0) |
| **open** R0 windows from the Hamiltonian pair, planar: longest | 6 (n = 10, 12), 7 (n = 14), 8 (n = 16, 18), 9 (n = 20), **10 (n = 22), ≥ 11 (n = 24)** |

So at n = 22 an R0 sequence of length 10 exists, and at n = 24 one of length 11, but none closes. The obstruction is at closure, not in run length.

Maximal open R0 windows are not near-rigid runs: they pass through non-DL states and disconnected Q_t (`r0_dump.py`).

### 5.2 Why the Hamiltonian pair matters

C30#0 at holes 0 and 16 (planar, n = 26, TrackS) is a closed DL orbit with L = 20 and frame advance −2, so it is a closed R0 sequence. It has **no** Hamiltonian pair (k(H) ∈ {2, 3}). Hence R0 must use the Hamiltonian pair: the statement is about Jordan curves, not only about frames.

### 5.3 Frame-pattern table (n = 14, closed, planar; pattern = v-edge indices of M_0, M_1, … repeated; "lone" = the chord alone on its side of H)

| pattern | lone f_1 | lone f_3 | lone f_4 |
|---|---|---|---|
| 2 0 (period 2) | SAT (run at n = 12, 16, 20) | | |
| 2 0 3 1 | SAT | UNSAT | SAT |
| 2 0 3 4 | SAT | SAT | SAT |
| 2 0 1 3 | UNSAT | SAT | UNSAT |
| 2 0 1 4 | SAT | SAT | UNSAT |
| 2 0 4 1 | UNSAT | UNSAT | SAT |
| 2 0 4 3 | UNSAT | UNSAT | UNSAT |
| 2 0 1 0 | SAT | SAT | UNSAT |
| 2 0 3 0 | SAT | SAT | SAT |
| 2 0 4 0 | UNSAT | UNSAT | SAT |
| 2 0 x (period 3, L = 6) | SAT iff x = lone | SAT iff x = lone | SAT iff x = lone |
| **period 5 (2 0 3 1 4 = advance −2, and 2 0 3 4 1)** | **UNSAT** | **UNSAT** | **UNSAT** |

Clean sub-rule [data, period 3]: (2, 0, x)^∞ closes through the Hamiltonian pair iff f_x is the lone chord. The net turning of v's matched edge (shortest-rotation convention) matches the period-3 rows but **not** the period-4 rows: 2031 with lone f_1 has turning −1 turn and is SAT, while 2031 with lone f_3 has turning 0 and is UNSAT. So the mechanism is not v's turning number. Small-n effects (n = 14) cannot be excluded for the period-4 UNSAT entries.

### 5.4 Conjecture R0

**[conjecture]** Let G be a simple plane graph, v of degree 5 (rotation f_0..f_4), all other vertices cubic. Let M_0, M_1 be perfect matchings with M_0 ∪ M_1 a Hamiltonian cycle through f_{k}, f_{k+2}. There is no cyclic sequence M_0, M_1, …, M_{L−1} of perfect matchings with M_t ∩ M_{t+1} = ∅ (indices mod L) and v-edge of M_t equal to f_{k−2t}.

- R0 ⇒ NRC. An R-cycle on the sphere is, in Tait form, such a sequence through a rigid (Hamiltonian) state. G is simple when no link vertex has degree 3.
- Evidence: §5.1 (n ≤ 26 at L = 10; n ≤ 22 at L = 20; n = 14 at L = 5, 15).
- False without planarity at every n, so it is a genuinely planar statement.
- Untested off the sphere. The chord-diagram encoding is sphere-only; a crosscap encoding is needed for RP².

## 6. Best partial proof

What is proved here:
- the step rules R1–R6;
- Lemma FE, whose consequence b_t = b_{t+5} reduces the A5v-constancy question to 6 patterns;
- the bounce-back form of A5v;
- the far-end winding dichotomy, which separates the T1 family from A5v orbits at radius 1;
- R6, showing a mod-3 Heawood/turning count cannot close the gap.

None of these excludes a closed A5v or planar orbit. **The proof chain toward NRC is therefore not started beyond the restatements.** The strongest evidence-backed reduction is:

  NRC ⇐ Conjecture R0 (§5.4), whose hypotheses are only perfect matchings, one Hamiltonian cycle, planarity and closure.

Exhaustive status: NRC holds for all simple plane G with n ≤ 24 [data, exact]; Conjecture R0 holds for n ≤ 26 at L = 10 [data, exact].

**What breaks for the T1 family:**
- (i) Every T1 orbit is anti-A5v at every state. By FE all five neighbours of v then wind ±L/5: the frame twist propagates outward. Under A5v it does not.
- (ii) The T1 graphs are non-planar, and the R0 obstruction is planarity-specific. Non-planar R0 is SAT at every n.
- Any argument through R0 automatically "uses planarity essentially".

## 7. The precise remaining gap

1. A mechanism for Conjecture R0, i.e. a planar invariant of the Hamiltonian pair (H, M_0, M_1) that an R0 sequence with a period-5 frame cannot restore. It must:
   - be Jordan-level (it fails without planarity);
   - need the Hamiltonian pair (C30#0);
   - not be v's turning number (§5.3);
   - not be the mod-3 Heawood count (R6).
2. Independently: whether "no closed A5v orbit" (T1-v) holds at n ≥ 26. The Studio has n = 24 window 10 UNSAT. That question now matters less, because A5v is ¬inA (scope agent) and the planar search shows how much planarity A5v leaves out.

## 8. Recommended next lemma

**Lemma R0-core (target).** Find the counting argument behind the UNSAT verdicts of R0 at n = 8–12, where the instances are tiny.
- Extract a DRAT proof or an MUS of `relax_test.py 10 10 0 1` and read off which planarity clauses (crossing pairs) and which disjointness constraints are used.
- Then test the extracted statement in the form "no R0 sequence from (M_0, M_1) can end disjoint from M_0 with v-edge f_{k+2}". At n = 22 the open length-10 sequences exist and only the wrap-around disjointness M_9 ∩ M_0 = ∅ fails.
- Parallel tests:
  - extend closed R0 to n = 28–30, and to L = 20 at n ≥ 24;
  - encode R0 on RP² (circle with one crosscap: chords on the crosscap side may cross pairwise as in a Möbius band) to see whether R0, like NRC, is sphere-specific or survives on RP², where NRC also has no counterexample;
  - redo the §5.3 table at n = 18–20 to separate size effects from the real rule.

## 9. Coordinator notes addressed

- *Full planarity allowed.* Used directly via `sat_planar.py`; §4 and §5 are planar results.
- *Lead A (turning).* Reduced to sign sums (R5). The mod-3 closure is automatic (R6). The FE winding dichotomy at radius 1 is the only turning-number statement that separates T1 from planar. v's turning does not decide R0 (§5.3).
- *Lead B (area).* Killed (L3).
- *Records p33.r147#128636 h2 and p34.r178#11764701 h10.* Both are in `out/sphere_windows.jsonl`, together with all holes of the other maxima graphs: 168 windows of length ≥ 4, 476 Hamiltonian states, A5v at 923 / 923 states.
- *A5v = ¬inA (scope agent).* Consistent with R4/FE: these use only the DL frame plus the bit, and say nothing about the surface. The planar input in R0 is the chord-diagram planarity, which is sphere-specific as encoded.
- *Studio: A5v window 10 UNSAT at n = 24.* Consistent with §4; recorded in the A5v row.

## 10. Files

| file | content |
|---|---|
| `pf_lib.py` | sphere side: Tait dual (TrackT), near-rigid 1212 windows, per-state planar quantities (regions D_X, D_Y, O, area, chord positions, A5v) |
| `sphere_runs.py`, `sphere_collect.py`, `analyse_sphere.py` | sphere windows → `out/sphere_windows.jsonl`, `out/sphere_p33.jsonl`; Lead B and slot statistics |
| `control_planar_rule.py` | positive control of the circle rule (1,244 / 1,244) |
| `sat_t1v.py`, `sat_window.py` | copies of the run-2 encoder. Additions: axiom mode 3, a bit variable with a "mixed" clause (some A5v state and some anti-A5v state); `free_L` hook |
| `sat_planar.py` | planarity clauses (§1.3); `window` / `closed` / `--enum` |
| `check_planar.py` | independent networkx planarity check of SAT graphs |
| `enum_windows.py`, `win_lib.py`, `show_win.py`, `lemma_test.py`, `ham_patterns.py`, `a1local_filter.py` | exhaustive A5v window enumeration and lemma tests L1, L2, L7 (`out/win_*.jsonl`) |
| `potential_search.py` | L5 |
| `farend_check.py`, `winding_all.py` | Lemma FE and windings on closed orbits |
| `run_mixed.py`, `run_patterns.py` | L8 (both timed out at n = 22) |
| `relax_test.py`, `relax2.py`, `r0_dump.py`, `r0_hamreturn.py` | the R0 experiments (§5); `relax2.py --verify` re-checks a decoded solution |
| `run_planar.sh`, `run_planar_closed.sh` | §4 drivers |
| `out/` | all logs quoted. `win_n18_W4_axv1.jsonl` (10 MB) and `win_n16_W4_axv0.jsonl` (2.6 MB) are not committed; regenerate with `enum_windows.py 18 4 1` (16 s) and `enum_windows.py 16 4 0` (18 s) |

Reproduce §5.1: `python3 relax_test.py N 10 0 1` (planar) and `python3 relax_test.py N 10 0 0` (non-planar). Reproduce §5.3: `python3 relax2.py 14 L p<pattern> perm:413:<lone> [--verify]`.
