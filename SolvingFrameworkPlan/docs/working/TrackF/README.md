# Track F (G66 at fullerene duals): a global handle? [exploratory]

Track F agent, 7 Oct 2026, Mac Studio. Nothing here is committed. Every claim is labelled **formal** (Lean), **hand** (a proof written here, unreviewed), **data** (a computation here, exact counts), **data (Studio)** (someone else's run, re-aggregated), **conjecture**, or **lit-L/M/H** (literature, by confidence).

Inputs read: CoordinatorPlan (status log), TrackB/README, NightG66, NightG66IPR, NightF6Status §0, Jobs BR/BS, `QuarterBitDynamics.pureClean_of_no_allDL_orbit`, `QuarterLemmaP`.

## 0. Bottom line

1. **No multi-hole handle exists in the form asked for.**
   - *hand:* the icosahedral fullerenes GC(k,l) (C60, C80, C140, C180, C240, ...) and every fullerene whose symmetry group is transitive on its 12 pentagons have all 12 holes equivalent. On them "some hole is PureClean" ⇔ "every hole is PureClean". So G66^IPR is exactly as hard as G66 on an infinite family whose holes are flat (hexagonal) to radius about k.
   - *data:* holes do not compensate each other. Across all 1,267 IPR duals C60–C100, a long DL run at one hole goes with longer runs elsewhere: the correlation of maxrun between hole pairs is +0.10 to +0.20 at every distance, and the correlation of best-hole and worst-hole maxrun over graphs is +0.38. The best hole's maxrun stays at 6–11 while the worst grows to 24. Local pentagon density barely predicts maxrun: the correlation is −0.13 to +0.15 for C82–C100, the exception being C60's (5,5) holes.
2. **New exact lemma (hand + data): Lock parity.** At an unfilled state at a degree-5 hole of *any* sphere triangulation, with link (α, μ, α, A, B) at x_j..x_{j+4}:
   - **Lock2 ⇔ K_{αA}(x_{j+2}) contains an odd number of odd-degree vertices of T** (h excluded);
   - **Lock1 ⇔ K_{αB}(x_{j+2}) does;**
   - **K_{αμ}(x_{j+2}) always does.**

   So DL is a pure parity ("charge") condition. At an IPR dual it reads: the π-swap component, and the {α,B}-component of x_{j+2}, each contain an odd number (≥ 1) of the other 11 pentagons *as vertices*. This makes "lock chains must reach other pentagons" exact.
   - The mod-4 pocket versions also hold.
   - Formal Lemma P's "the π-image of a DL state has Lock1" follows as a corollary.
   - Checks: 0 mismatches on **496,777,103 unfilled sphere states** (all fullerenes C20–C46; IPR C60–C88; all 7,209 order-24 min-degree-5 triangulations; the 147-graph frame census; 86 frame-class adversarial witnesses), plus pocket parity on 1.31·10⁹ IPR DL states.
3. **The lock-parity lemma is where planarity enters (data, torus).** On the 17,700 torus degree-5 holes of `local-runs/18-torus-floor`:
   - lock parity fails at 17,537 holes;
   - **all 21,915 targetless Kempe classes contain parity-violating states** (99.0% of their unfilled states violate it);
   - **all 24,042 parity-clean classes contain a filled state.**

   This gives a candidate lemma **LPC** (§4): a Kempe class in which every unfilled state obeys lock parity has a filled state. With the parity lemma (a theorem on the sphere), LPC ⇒ PureClean at every hole ⇒ R\* ⇒ 4CT. So LPC is 4CT-strength, but it is purely combinatorial (no topology).
4. **G66⁰ / G66 data, two engines.**
   - IPR C60–C100: 1,267 graphs, 15,204 holes, exhaustive, **0 all-DL π-cycles in 1,310,135,893 DL states**. Longest DL run **24** (C98, ipr#543 h5); 23 at C88 and C100.
   - Identical (nDL, full run-length histogram, #all-DL cycles) to Studio Job BO's independent `picyc.bo --jobbo` on the 11,460 holes both covered.
   - Nanotubes (5,5) and (9,0), IPR and non-IPR, to C120 exhaustive: maxrun ≤ 12. Sampled to C274: maxrun ≤ 15, not growing with tube length.
   - Icosahedral C180/C240/C320 (flat holes, sampled): maxrun 13 / 12 / 10, 0 cycles. IPR C108–C120 samples (1,534+ holes): maxrun ≤ 17, 0 cycles.
   - **Where G66 comes closest to failing is not long runs but tiny Kempe classes:** Job BO has 155 holes with a **4-state class containing exactly 1 filled state** (F/N = 1/4, the floor's equality case). One was re-verified with an independent engine (ipr#32 C96 h8, h21: [4 states, 1 filled, 1 DL, 2 single-lock]).
   - A targetless class needs ≥ 10 states (formal `allDL_cycle_length_dvd_ten` + C1), so these tiny classes cannot be counterexamples. The next sizes seen are 6, 12 and 24, with F/N = 2/3.
5. **Closed fullerenes are far from Kempe-unique, but one pentagon hole merges almost everything (data, two engines).**
   - C60 has 52 edge-Kempe classes of Tait colourings (30 frozen singletons, 20 of size 4, and two big classes, 1,400 and 1,680). C80 Ih has 156 classes. All 27 IPR fullerenes C60–C82 have 6–156 classes.
   - Yet κ(T − h) = 1 at 98.3% of IPR holes (11,507 of 11,701, Job BO data). NightG66IPR's "κ(F) = 1 is expected" (T-IPR3) is false.
6. **Verdict.** G66 at fullerene duals does **not** look attackable by a global or multi-hole argument. The fullerene class buys nothing over the frame class at the hard holes (flat holes), and the 12-pentagon structure enters only through the parity lemma, which is satisfiable along DL runs. The one new lead is a reformulation: **LPC**, a class-level parity statement, together with the observation that the planarity input to G66 is exactly the lock-parity lemma (torus data). The data for G66 itself stay clean everywhere tested. Recommended: keep G66 on the critical path only as a test of LPC-type class arguments; do not spend more on orbit-level (G66⁰) or multi-hole routes.
7. **LPC falsification off the sphere (§8): alive, weakly tested.**
   - Exact reformulation (hand): the violators of a targetless class are the ends of its π-paths, so LPC ⇔ "no Kempe class is a union of all-DL π-cycles".
   - Random censuses on five surfaces (40k holes) contain no π-cycles, so they test nothing beyond that tautology.
   - A targeted search found all-DL π-cycles on the Klein bottle, RP² and torus. Every one sits in a class with ≥ 2 filled states per cycle state; the bound 2 is attained.
   - Parity-clean classes satisfy the quarter floor F/N ≥ 1/4 on every surface tested.
   - "minviol = 1" is a forced frozen singleton, not fragility.

## 1. Engines and data

- `src/f66.cpp` (new, independent of picyc/radius.py):
  - DL states at a hole with the link fixed to (0,1,0,2,3) at j (unique representative mod S₄);
  - π (R₊₃) on DL states, π⁻¹ for sampling;
  - maximal DL runs and all-DL π-cycles;
  - pocket geometry: P2 = comp(x_{j+2}, T − h − K2), P1 = comp(x_{j+2}, T − h − K1), with curvature Σ(6 − deg), boundary edges, and the pentagons inside;
  - Jordan sanity (x_j ∉ pockets);
  - `--lockparity` (the §3 check on every unfilled state);
  - `--sample S` (randomised DFS colourings, each DL hit extended to its full run both ways).

  Binaries `f66_w{1,2,4,5}` handle n ≤ 64/128/256/320. *Calibration:* on ipr#543 h5 (exhaustive maxrun 24), 100k samples find the 24-run.
- `src/kclass.cpp`: all Kempe classes of T − h (or of T, `none`) by union-find over every component swap, with per-class filled/DL/lock-parity counts. `src/kclass_py.py` is an independent Python check (agrees on C20, C60 closed and C76 h8).
- `src/spiral.py`: Fowler–Manolopoulos face-spiral windup (written here). Isomer counts C20–C40 match the known 1, 0, 1, 1, 2, 3, 6, 6, 15, 17, 40; all fullerenes C20–C46 are in `graphs/fall_*.txt`.
- `src/goldberg.py`: GC(k,0) geodesic icosahedra and leapfrog, giving C60, C80, C180, C240, C320, C540.
- `src/make_tubes.py`: spiral-shift tube families, with the belt (min hexagon cut between caps) checked:
  - (5,5) D5d C60+20k and D5h C70+20k (belt 10);
  - (9,0) IPR C78+18k (belt 9; found by `tube_ipr_search.py`);
  - (9,0) non-IPR C58+18k (belt 9, 6 adjacent-pentagon pairs).
- `src/torus2txt.py`: torus faces from `local-runs/18-torus-floor` to oriented rotation systems.
- Analyses: `anal_ipr.py`, `anal_geom.py`, `anal_sweep.py`. Outputs are in `out/` (summaries `*_summary.txt`, per-hole JSONL, run dumps `*.runs.jsonl` for runs ≥ 10 or ≥ 12).

All runs used `nice -n 10`, at most 4 single-threaded processes.

## 2. Data

### 2.1 IPR C60–C100, exhaustive (data; `out/ipr_summary.txt`)

| dual n | C_N | graphs | holes | maxrun | all-DL |
|---|---|---|---|---|---|
| 32 | C60 | 1 | 12 | 2 | 0 |
| 37–40 | C70–C76 | 5 | 60 | 5–8 | 0 |
| 41–43 | C78–C82 | 21 | 252 | 10, 11, 14 | 0 |
| 44–46 | C84–C88 | 78 | 936 | 15, 15, 23 | 0 |
| 47–49 | C90–C94 | 266 | 3,192 | 16, 17, 21 | 0 |
| 50–52 | C96–C100 | 896 | 10,752 | 20, 24, 23 | 0 |
| **total** | | **1,267** | **15,204** | **24** | **0** |

- DL states 1,310,135,893.
- piFail 0, Jordan failures 0, pocket-parity failures 0, mod-4 failures 0.
- The run-length tail is geometric (C100: 3.8·10⁸ runs of length 1, … 2 of length 23).
- Cross-check: 11,460 holes identical to Job BO, 0 differ.
- Run ends: every run of length ≥ 10 (16,060) ends with Lock2 dying and Lock1 surviving. Job BO: all 7.06·10⁸ runs do, at every length. This is formal Lemma P, re-derived in §3.

### 2.2 Multi-hole (data; `out/ipr_multihole.txt`, `out/ipr_geom.txt`)

- **Per graph, best-hole maxrun:** C84 6–7; C92 mostly 7–8; C100 6–11 (median 8).
- **Worst hole:** grows to 24.
- **Graphs with a run ≥ 15 at some hole (118):** best hole ≤ 7 in 29, ≥ 8 in 89. Graphs without one (1,149): 518 and 631. So long runs make other holes *worse*, not better.
- **Hole-pair maxrun correlation by dual distance 2–6:** +0.20, +0.11, +0.12, +0.12, +0.17.
- **Local geometry:**
  - n2 = #pentagons at dual distance 2 (the w-positions): mean maxrun 9.1–9.95 for n2 = 1–4.
  - Only (n2, n3) = (5,5), C60, gives 2.
  - corr(maxrun, n2 + n3/2) per order: −0.47 (C78, 60 holes), then |r| ≤ 0.15.

### 2.3 Pockets and lock chains (data)

- Over all 1.31·10⁹ DL states:
  - the Lock2 pocket holds np2 ∈ {1, 3, 5, 7, 9} other pentagons (never 0 or 11; §3 explains why), with frequencies 670M / 304M / 195M / 103M / 38M;
  - the mean length of the containing run falls with np2: 2.02 / 1.87 / 1.73 / 1.61 / 1.52;
  - the Lock1 inner pocket holds np1 ∈ {1, ..., 9} (812M / 264M / 148M / 68M / 18M).
- Along long runs (e.g. ipr#88 h23, L = 21) the Lock1 inner pocket is usually the single nearest pentagon "in front of" x_{j+2}. The pocket sets change at every step and have empty intersection along a run.
- So no pentagon is "held" by a run. NightG66IPR's T-IPR4 prediction ("long runs need pockets with pentagons") is true but vacuous: *every* DL state has pentagons in both pockets (§3).

### 2.4 Stress tests

| family | range | method | maxrun at 66666 | all-DL | notes |
|---|---|---|---|---|---|
| all fullerenes (non-IPR) | C20–C46, 342 graphs, 4,104 holes | exh | 9 | 4, all at 55555 holes of C30#0 = A₃ and C40#0 (L = 20, the known A₃ cycle) | other patterns up to 21 (56655) |
| (5,5) tubes D5d / D5h | C60–C120 | exh | 2, 7, 7, 11 / 5, 7, 10 | 0 | |
| (9,0) IPR tubes | C78, C96, C114 | exh | 5, 8, 9 | 0 | |
| (9,0) non-IPR tubes | C58–C112 | exh | 6–9 (55666 holes ≤ 9, 56665 ≤ 12) | 0 | |
| long tubes, sampled | (5,5) C130–C270; (9,0) IPR C132–C258; (9,0) non-IPR C130–C274 (n ≤ 139) | sample 2·10⁵/hole, 12 holes each | (5,5): 11 at every length; (9,0) IPR: 15 at C132, else 10; (9,0) non-IPR: 8–14 (other patterns ≤ 15) | 0 | flat in tube length: separated caps give no long runs |
| icosahedral GC(3,0) | C180, hole flat to radius 2 | sample 8·10⁶ | 13 | 0 | 1,173,309 distinct runs |
| icosahedral GC(2,2), GC(4,0) | C240, C320, radius 3 | sample 8·10⁶ / 4·10⁶ | 12 / 10 | 0 | 1,020,053 / 459,628 distinct runs; GC(3,3) C540 queued (see §7) |
| IPR samples (random 40 per order from studiointel part 0/400) | C108 (480 holes), C112 (480), C116 (492), C120 (≥ 82) | sample 10⁵/hole | 17, 16, 16, 15 | 0 | top ipr56_1140 h34 (17) |
| frame census | 147 graphs, orders 22–28 | exh | 7 | 0 | all patterns |
| frame adversarial witnesses (Track B) | 86 graphs, n ≤ 49 (no 66666 holes) | exh | — | 0 | maxrun 37 at 55676 |
| all min-degree-5 triangulations of order 24 | 7,209 graphs, 111,492 holes | exh | 9 | 5 cycles (75755, 55555 ×2, 56556, 55557; all L = 20) | sanity: the census all-DL cycles are found |

- Long tubes do not produce long runs; the separated caps are not a mechanism.
- No G66⁰ failure was found anywhere, so the two-engine rule for a failure was never triggered. The IPR data were nevertheless matched against picyc.

### 2.5 Kempe classes (data, two engines)

- **Closed fullerenes** (`out/kclass_closed_*.jsonl`):
  - C20: 10 classes, all frozen;
  - C60: 52 classes (sizes 1 ×30, 4 ×20, 1,400, 1,680);
  - C76 Td (ipr#211): 59;
  - C80 Ih: 156;
  - the 27 IPR C60–C82: 6–156 classes each.
- **Holes:**
  - κ(T − h) = 1 at C60, C80 Ih and C20 holes.
  - ipr#211 has κ = 2 at 8 of its 12 holes: a 12-state class with 8 filled and 4 unfilled. These 8 filled states are 8 of C76's Tait colourings. At the other 4 holes everything merges.
  - Job BO over 11,701 IPR holes: κ ≥ 2 at 194. The extra classes are (size, filled) = (4, 1) ×155, (6, 4) ×4, (12, 8) ×63, (24, 16) ×3.
- **Exact identity (hand):** the filled set at every hole is the set of Tait colourings of F, so F_h is hole-independent (30,293 at all 12 holes of C76). Each hole's Kempe partition coarsens the partition of Col(T) into Kempe classes of T. This is the only exact cross-hole relation found.

## 3. Lemmas (hand; data-verified)

Notation:
- T is a sphere triangulation, h a vertex of degree 5, c a proper 4-colouring of T − h, unfilled at j with link (α, μ, α, A, B).
- ε(X) = Σ_{v∈X} (6 − deg v) mod 2 = #odd-degree vertices in X mod 2. Note ε(V − h) = 1.
- Tait form (NightG66IPR §1): G = T* minus the face P of h is a 5-pole with spokes s_t (dual to x_t x_{t+1}). The edge colouring is e(uv) = c(u) + c(v).
- The leg word is (γ₁, γ₁, γ₂, γ₁, γ₃), where γ₁ = α+μ, γ₂ = α+A, γ₃ = α+B.

**(i) Parity lemma** (classical). For a vertex set I of G, each colour class meets δ(I) (legs included) in ≡ |I| (mod 2) edges.

**(ii) Patch formula** (Euler). A disc D bounded by a closed edge curve of G, not containing P, satisfies Σ_{faces f in D}(6 − |f|) = 6 − n₂ + n₃. Here n₂ and n₃ count the boundary vertices whose third edge points out of or into D.

**Lemma PP (pocket parity).**
- Let Q be a bicoloured leg-to-leg path from s_a to s_b, and D the disc bounded by Q, the two spokes and the P-arc on the side containing r spokes strictly inside.
- Let ℓ = |Q|. Then L = ℓ + r + 3, and n₃ = k + r, where k is the number of Q-vertices whose third edge points into D.
- (i) gives k ≡ r_a + r_c (mod 2), counting inner legs by colour.
- Hence **Σ_D(6 − |f|) ≡ 3 − ℓ + r + 2(r_a + r_c) (mod 4)**. In particular it is ≡ r + [e(s_a) ≠ e(s_b)] (mod 2), since ℓ is odd iff the end colours agree.
- A closed bicoloured cycle not meeting P encloses Σ ≡ 2 − L (mod 4), which is even.
- In dual form, for the DL pockets of `f66`: **Lock1 ⇒ Σ_{P1}(6 − deg) ≡ 1 − E(P1, K1)** and **Lock2 ⇒ Σ_{P2}(6 − deg) ≡ −E(P2, K2) (mod 4)**, both odd.
- *Data:* 0 failures over all DL states of §2 (1.31·10⁹ IPR plus about 10⁸ others).

**Lemma LP (lock parity).**
- (a) Lock2 ⇔ ε(K_{αA}(x_{j+2})) = 1.
- (b) Lock1 ⇔ ε(K_{αB}(x_{j+2})) = 1.
- (c) ε(K_{αμ}(x_{j+2})) = 1 always.

*Proof.*
- The {γ_a, γ_b}-leg-paths cut the disc into regions. The region of x_{j+2} is its Kempe component for the complementary pair, plus the discs inside the closed bicoloured cycles around it. Those discs are even by PP. A link face touches P, so it is never inside a closed bicoloured cycle; hence the component is the region minus the maximal cycle-discs it contains, and the region's parity is ε(component).
- PP's mod-2 rule gives the region parities:

| system | pairing | region parities |
|---|---|---|
| γ₁γ₃ | Lock2 (j, j+4)(j+1, j+3) | (x_{j+2}, x_{j+3}) odd; x_j odd; (x_{j+1}, x_{j+4}) odd |
| γ₁γ₃ | otherwise (j, j+1)(j+3, j+4) | x_{j+1} even; x_{j+4} odd; (x_j, x_{j+2}, x_{j+3}) even |
| γ₁γ₂ | Lock1 | x_{j+2} odd |
| γ₁γ₂ | otherwise | x_{j+2} even |
| γ₂γ₃ | the single path (j+2, j+4) | the x_{j+2} side is odd |

∎

- *Data:* **0 mismatches in 496,777,103 unfilled states** on the sphere (§0.2).
- *Corollaries:*
  - (1) Under Lock2, ε(K_{αA}(x_j)) = 1. Since K_{αA}(x_j) is the {α′, B′}-component of x_{j′+2} after π, **π of a Lock2 state always has Lock1**. This is formal Lemma P (`unfilled_pred_iff_lock1`), re-derived.
  - (2) A run continues iff, after the swap, the {α, μ}-component of x_j has odd charge.
  - (3) At a hole whose ball of radius R has no other odd vertex, every lock component reaches beyond R.
  - (4) Let p = (parities of #odd vertices coloured α, μ, A, B). On each DD step p ↦ (¬p_α, p_B, p_μ, ¬p_A). This map has period 6 (period 2 iff p_A = p_B ≠ p_μ). So a canonical all-DL cycle has 30 | L unless p_A = p_B ≠ p_μ. This is mild and not used.
- *Literature:* lit-L. The parity lemma and "odd vertices obstruct Kempe arguments" are classical (Tait/Heawood; Fisk 1977–78 on Eulerian triangulations). I did not find this exact lock criterion stated; not checked further.

## 4. Candidate statements and their support

| statement | level | status |
|---|---|---|
| **LPC:** at a degree-5 hole of a triangulation of any surface, a Kempe class of T − h all of whose unfilled states satisfy LP(a,b) contains a filled state | class | **conjecture.** Torus: 24,042 / 24,042 parity-clean classes filled; 21,915 / 21,915 targetless classes not parity-clean. On the sphere LP always holds, so LPC ⇒ PureClean everywhere ⇒ R\* ⇒ 4CT (4CT-strength). Orbit-level analogue is FALSE: sphere all-DL π-cycles (e.g. order-24 75755, 55555) are parity-clean. **§8:** ⇔ no Kempe class is a union of all-DL π-cycles; 0 counterexamples on torus / Klein / RP² / genus 2 / rp2x3, including the classes of all-DL π-cycles found off the sphere. |
| "frozen orbit at h ⇒ a clean hole elsewhere" | multi-hole | **no support.** Holes correlate positively; icosahedral fullerenes make it equivalent to single-hole G66. |
| "all Tait colourings of a fullerene are Kempe-equivalent" | — | **false** (C60: 52 classes). |
| κ(F − P) = 1 for IPR fullerenes | class | **false** at 194 / 11,701 holes (Job BO; re-verified at ipr#211, ipr#32). All extra classes are filled. |
| G66 / G66⁰ at IPR C60–C100 | — | **data:** holds at all 15,204 holes (0 all-DL in 1.31·10⁹ DL states) |

## 5. Verdict on attackability

- **Multi-hole:** dead. Pentagon-transitive fullerenes reduce it to single-hole G66 at flat holes, and the data show no compensation between holes.
- **Parity, Euler, curvature:** the exact content is LP/PP. They turn DL into an odd-charge condition on Kempe components, which explains why locks need distant pentagons. They do not forbid DL runs or cycles: sphere all-DL cycles exist at other patterns and satisfy LP.
- **What survives** is a class-level route with one well-defined topological input: prove LPC, or an LPC-type class statement at 66666, using only the Kempe structure plus LP. The torus data say LP is the *right* input: 100% separation. Whether a class argument can use it is open, and I see no proof.
- Probability that Track F as such yields a G66 proof: low (my estimate ≤ 5%).
- The LP lemma is cheap to formalise via the Tait/Kempe dualities already in Lean (`sphere_pair_duality`), and it is a reusable statement of where planarity enters.

## 6. Files

`src/`: f66.cpp, kclass.cpp, kclass_py.py, spiral.py, enum_small.py, enum_range.py, goldberg.py, tubes.py, tube_ipr_search.py, make_tubes.py, pc2txt.py, torus2txt.py, anal_ipr.py, anal_geom.py, anal_sweep.py, slot1–3.sh.

`graphs/`:
- ipr32_52.txt (copy of in-ipr.txt);
- fall_20…46.txt (all fullerenes);
- goldberg.txt, tubes.txt, frame22_28.txt, witness.txt, plantri24.txt, torus.txt;
- ipr56–62_part0.txt (from studiointel .pc).

`out/`:
- ipr/ (per-hole + runs ≥ 10), tubes/, gold/, big/, sweep/, wit/;
- torus_lp.jsonl, torus_kclass.jsonl;
- kclass_closed_*.jsonl;
- summaries: ipr_summary.txt, ipr_geom.txt, ipr_multihole.txt, sweep_summary.txt, wit_summary.txt, torus_parity_summary.txt, bo_smallclasses.txt, plus the final big-run summaries.

LPC work (§8): `src/surfaces.py`, `lpc_census.py`, `lpc_search.py`, `lpc_slotA.sh`, `kclass_pi.cpp` → `kclass3`, `lpc_detail.py`, `lpc_pi.py`, `lpc_cycsearch.py`. Outputs are in `out/lpc/`:
- `census_*`, `census.log`;
- `pi_*.jsonl`, `pi.log` (second engine);
- `picyc_*.jsonl` (π-cycles: census, torus18, sphere24);
- `search_*`, `search_best.*`;
- `cyc_*.{out,log}`, `cyc_graphs.*`.

## 7. Caveats

- LP and PP proofs are hand proofs in Tait form (unreviewed). The data check is exhaustive on the listed sets only.
- Sampling (C130+) explores a vanishing fraction of the state space. Its maxrun is a lower bound. Calibration found the known 24-run with 10⁵ samples at C98.
- The torus test uses the existing 18-torus-floor graphs (n ≤ 36). LPC there is data, not a theorem.
- κ statistics for IPR come from Job BO (picyc). I re-verified only ipr#211 and ipr#32 with `kclass`.
- The (9,0) IPR tube family was found by search, not from a reference spiral. Its belt is 9 (checked), and its first member is an IPR C78.
- **Still running at report time** (nice 10, three single-threaded processes, each bounded; started 14:30–14:45 MDT):
  - `src/slot2.sh`: the last GC(4,0) seed, then GC(3,3) C540 (10⁶ samples);
  - `src/slot3.sh`: the last two (9,0) non-IPR tubes;
  - the C108–C120 sample (C120 had 82 of ~492 holes done).
- Outputs append to `out/gold/`, `out/tubes/big.*`, `out/big/ipr56_62.*`. Re-summarise with `python3 src/anal_big.py {gold|tubes|big} FILE`. The numbers in §2.4 are those at report time.

## 8. Falsifying LPC off the sphere (7 Oct, afternoon; Track F handover)

Question: does LPC ("a Kempe class at a degree-5 hole in which every unfilled state obeys lock parity contains a filled state") fail on a triangulation of the torus, Klein bottle, projective plane (RP²), orientable genus 2, or non-orientable genus 3 (RP²#RP²#RP², "rp2x3")? LPC on the sphere is 4CT-strength, so a counterexample anywhere would kill it as a route; survival is weak evidence only.

### 8.1 Reformulation (hand; LockParity.md §5)

- **Theorem P** (the parity identity) holds on every surface, so lock parity at a state ⇔ the hole duality D1, D2 at that state.
- In a targetless class every unfilled state is DL. For a DL state, D2 ⇔ π = R₊₃ is defined, and D1 ⇔ π⁻¹ is defined. π is injective with inverse the mirror swap.
- So the **lock-parity violators of a targetless class are exactly the ends of its non-cyclic π-orbits**. A one-state orbit violates both D1 and D2. A longer path has one D1-violator (its start) and one D2-violator (its end).
- **LPC ⇔ no Kempe class of T − h consists only of states on all-DL π-cycles.** On the sphere this is PureClean.
- A violation is a lock chain and a π-chain that close up through h into two cycles crossing once (ℤ/2 intersection number 1), i.e. two non-separating cycles. That is the only way the topology enters.

### 8.2 Engines

| engine | what | role |
|---|---|---|
| `src/kclass2` (= `kclass.cpp`) | all Kempe classes of T − h; per class: size, filled, DL, single-lock, Kempe degree, LP violators; Theorem P check (`pid_bad`) and D check (`dual_bad`) | census and walks |
| `src/kclass3` (`kclass_pi.cpp`, new) | kclass2 plus π on every unfilled state, all-DL π-cycles, the longest DL π-run (`maxDLrun`), and for each class containing a cycle [states on cycles, DL path ends, filled] | cycle census and cycle search |
| `src/lpc_detail.py` (new, pure Python, shares no code with the C++) | the same class list and per-state detail (j, locks, inA/inB, which D fails, component sizes and odd vertices), π-orbit decomposition of every targetless class, "violators = path ends" check | second engine |

- `src/lpc_census.py` and `src/surfaces.py` generate random min-degree-5 triangulations, by subdivision plus flips, with the surface checked (Euler characteristic and orientability).
- `src/lpc_search.py` is annealing on the obeying fraction in targetless classes.
- `src/lpc_cycsearch.py` (new) is annealing on all-DL π-cycles. Phase 1 maximises the number of cycles, then the longest DL π-run. Phase 2 (`LPC_OBJ=ratio`) maximises onCycles / (onCycles + pathEnds + filled) over classes containing a cycle. This ratio is 1 exactly at an LPC counterexample.
- `src/lpc_pi.py` re-runs the census holes with the Python engine.

Cross-checks:
- Python vs kclass2: identical class lists on all 6,026 re-run census holes (every hole with a targetless class of size ≥ 3) and on all 87 holes of the 9 best search graphs. 0 mismatches.
- kclass3 vs kclass2: identical class lists on all 40,241 census holes.
- kclass3 against known sphere data:
  - C30#0: π-cycles of length 20 at the two 55555 holes, matching f66;
  - all 7,209 order-24 min-degree-5 triangulations: exactly 5 all-DL π-cycles, all L = 20, matching f66 (§2.4);
  - C60 maxrun 2, matching f66.

### 8.3 Census (data; `out/lpc/census_*.jsonl`, 600 random graphs per surface, n = 16–40, seed 11)

| surface | holes | classes | targetless | of which frozen singletons | parity-clean classes with unfilled states (min F/N) | max obeying fraction in targetless classes | Theorem P failures | D failures / unfilled states | all-DL π-cycles | LPC counterexamples |
|---|---|---|---|---|---|---|---|---|---|---|
| torus | 8,277 | 43,374 | 10,809 | 5,405 | 1,285 (1/4) | 3/5 | 0 | 1,664,226 / 3,862,132 | 0 | 0 |
| Klein | 8,658 | 39,919 | 10,261 | 5,180 | 1,219 (1/4) | 3/5 | 0 | 1,510,240 / 3,173,373 | 0 | 0 |
| RP² | 9,245 | 22,701 | 4,118 | 1,826 | 1,228 (1/4) | 1/2 | 0 | 2,996,439 / 13,676,975 | 0 | 0 |
| genus 2 | 6,851 | 24,688 | 7,652 | 3,207 | 709 (1/4) | 1/2 | 0 | 225,753 / 264,195 | 0 | 0 |
| rp2x3 | 7,210 | 28,840 | 7,649 | 3,329 | 1,150 (1/4) | 3/5 | 0 | 633,096 / 991,495 | 0 | 0 |
| torus (18-torus-floor, §0.3) | 17,700 | — | 21,915 | — | 2,517 (1/4) | — | 0 | — | 0 | 0 |

D failures count D1 and D2 separately.

- Every targetless class is all-DL (0 single-lock states), as §8.1 predicts.
- In the 21,571 targetless classes re-run with the Python engine (`out/lpc/pi_*.jsonl`, `pi.log`):
  - the violators are exactly the π-path ends in every case;
  - no targetless class contains a π-cycle;
  - the longest π-path is 5 (RP²: 4).
- **The census itself is a weak test.** It contains no all-DL π-cycle at all (0 in 57,941 holes, torus18 included), and by §8.1 only classes built from π-cycles can be counterexamples. For comparison, the sphere rate is 5 in 111,492 holes at order 24, which predicts about 2.6 here. Off the sphere, then, "0 counterexamples" in the census only re-confirms the tautology "a cycle-free targetless class has violators".

### 8.4 The "minviol = 1" classes are trivial (data + hand)

- Every targetless class with exactly one violator is a **Kempe-frozen singleton**:
  - torus 5,405, Klein 5,180, RP² 1,826, genus 2 3,207, rp2x3 3,329, all of them (size 1, DL, Kempe degree 0);
  - every class with ≥ 2 states has ≥ 2 violators.
- Why it is forced (hand): at a frozen state every 2-colour subgraph of T − h is connected. So x_j ∈ K_{αA}(x_{j+2}) and x_j ∈ K_{αB}(x_{j+2}), and the state violates D1 and D2 simultaneously: a π-path of length 1.
- In the 5-state torus class (torus_11_568 h27, both engines), the violation looks like this:
  - The class is one π-path with j = 2 → 0 → 3 → 1 → 4.
  - The start (j = 2) has x_j ∈ K_{αB}(x_{j+2}) while Lock1 holds. This is a D1 failure: the {α,B}-component of x_{j+2} has 20 vertices and 14 odd vertices, even, as P predicts.
  - The end (j = 4) has x_j ∈ K_{αA}(x_{j+2}) while Lock2 holds (D2 failure; 19 vertices, 12 odd).
  - The three interior states obey LP with both components odd.
- On the sphere `NoFrozen` rules frozen DL states out formally. So the "minviol = 1" phenomenon is not evidence that LPC is fragile.
- What can be fragile is the **obeying fraction**: a class that is a single π-path of length L has fraction (L − 2)/L, which tends to 1.

### 8.5 Fraction search (data; `out/lpc/search_{torus,klein,rp2}.{out,log}`, 150 walks × 3,000 flips each, n = 16–30)

| surface | evaluations | best obeying fraction in a targetless class, by order n | LPC counterexamples |
|---|---|---|---|
| torus | 159,411 | 16: 2/3, 17: 3/5, 18: 5/7, 19: 3/5, 20: 5/7, 21: 9/13, 22: 3/5, 23: 2/3, 24: 5/7, 25–30: 2/3 (26: 3/5) | 0 |
| Klein | 155,196 | 20: 2/3, 21: 7/9, 22: 1/2, 23: 3/5, 24: 5/7, 25: 7/10, 26: 7/9, 27: 3/4, 28–29: 3/5, 30: 3/4 | 0 |
| RP² | 118,693 | 16–22: 3/5 (17: 2/3), 23: 2/3, 24–26: 3/5, 27: 1/2, 28: 3/5, 29: 5/8, 30: 3/5 | 0 |

- The best classes were verified with both engines (`out/lpc/search_best.*`). **Each is a whole Kempe class consisting of one or two π-paths.** Examples:
  - Klein n = 21 (`klein_best_w5` h16): one π-path of 9 DL states, with 2 violators (one D1 at the start, one D2 at the end) and 7 obeying;
  - torus: paths of 7;
  - RP²: two paths of 6.
- So the fraction grows with path length and says nothing about LPC. The relevant object is the π-cycle.

### 8.6 Cycle search: the real test (data; `out/lpc/cyc_*.{out,log}`, `cyc_graphs.*`)

`src/lpc_cycsearch.py` ran annealing flip walks at n = 16–34, 2,000 flips per walk (1,000 for the first torus run). Runs:
- **(a) all degree-5 holes:**
  - torus: 30 + 73 walks;
  - Klein: 80 walks;
  - RP²: 50 walks.
- **(b) only holes with no three consecutive degree-5 link vertices ("no-555"):** torus 75, Klein 67, RP² 71 walks.

  This excludes the hole types where PureClean is already proved on the sphere (F5 / weak F6 / `pureClean_of_hole4`). Track B's frame class has no such holes.
- The runs were stopped by hand after about 25–40 minutes each; walk counts are as completed.
- Every graph with a cycle was re-run with kclass3 and with the Python engine (`src/lpc_cycverify.py`): **0 mismatches on 604 + 82 cycle holes** (cycle lengths, the class list, and [onCycles, filled] per class).

| run | surface | distinct graphs with an all-DL π-cycle | cycle holes | cycle lengths | classes containing a cycle | … with no DL violator (parity-clean) | min filled / (states on cycles) | LPC counterexamples |
|---|---|---|---|---|---|---|---|---|
| (a) | Klein | 87 | 100 | 20 ×118, 40 ×1 | 102 | 13 | 2 | 0 |
| (a) | RP² | 260 | 413 | 20 ×834, 40 ×105, 60 ×97, 80 ×8, 100 ×13, 120 ×2, 180 ×1 | 504 | 319 | 2 | 0 |
| (a) | torus | 74 | 91 | 20 ×107, 40, 60 | 94 | 4 | 1.55 (a class *with* violators); 2 among parity-clean | 0 |
| (b) | torus | 16 | 16 | 20 ×24 | 16 | 0 | 7.35 | 0 |
| (b) | Klein | 26 | 26 (all 55757) | 20 ×39, 40 | 26 | 0 | 9 | 0 |
| (b) | RP² | 23 | 23 (55758, 55787, 5,5,8,5,10, 55677, 55768, 55656, …) | 20 ×28 | 23 | 3 | 2 | 0 |

- **All-DL π-cycles exist off the sphere**, contrary to what the census suggested.
  - Every length found is a multiple of 20, the same as on the sphere.
  - In run (a), 564 of the 604 cycle holes have a 555 run in the link. The 40 that do not are 36 on RP² and 4 on the Klein bottle, among them a 77775 hole.
  - Run (b) found cycles at frame-like hole types: Klein 55757, torus 55769, RP² 55656 / 55677 / 55758.
- **Every class containing a cycle has filled states.** In parity-clean cycle classes, filled ≥ 2 × (states on cycles) in all 339 cases, with equality in 291 of them.
  - The equality cases reproduce the sphere exactly. The Klein `klein_c32_w33_t648` h10 class and the RP² `rp2_c33_w2_t1397` h3 class are both [100 states: 40 filled, 30 DL, 30 single-lock; 0 violators], identical to the unique class at the 55555 hole of C30#0 (sphere).
  - RP² h21 at a 5,10,5,5,8 hole has [200, 80, 60, 60]: two cycles, a doubled copy.
  - Only a class *with* violators went below 2: 1.55 on the torus.
- **Quarter floor in parity-clean classes (data).** F/N ≥ 1/4, with equality attained, in every parity-clean class with unfilled states:
  - census 5,591; torus18 2,517; cycle graphs (a) 2,087; (b) 71;
  - order-24 sphere 115,068.

  Classes that contain violators go down to F/N = 0.003 (genus 2, census).
- Theorem P: 0 failures on every state of every graph above.

### 8.7 Verdict on LPC

- **Alive, not fragile in the sense feared, but weakly tested.**
  - No counterexample on five surfaces.
  - The "minviol = 1" classes are forced frozen singletons.
  - High obeying fractions are long π-paths, which are irrelevant by §8.1.
- **The honest content of the off-sphere data** is the following:
  1. all-DL π-cycles do exist off the sphere (Klein bottle, RP², torus; lengths 20–180, all ≡ 0 mod 20), and the Kempe class of every one found contains filled states. Every parity-clean one has at least 2 filled states per cycle state;
  2. in every parity-clean class (10,266 off the sphere plus 115,068 at order-24 sphere graphs) the **quarter floor F/N ≥ 1/4 holds, with equality attained**. Classes with violators go down to F/N = 0.003.
  3. The caveat: most off-sphere cycles sit at 555-type holes (the sphere-easy ones), and their tight classes are verbatim copies of a sphere class (C30#0). At frame-like no-555 holes only 3 parity-clean cycle classes were found, all on RP². So the test at the holes that matter is thin: 65 graphs, 3 parity-clean cycle classes.

  So parity-clean classes off the sphere behave like sphere classes, quantitatively.
- **What a proof would have to use.**
  - LPC ⇔ "the Kempe class of an all-DL π-cycle is never closed under Kempe swaps". The only topological input allowed is D1/D2 at every state of the class, i.e. no crossing pair (lock chain, π-chain) through h.
  - A proof must show that some state of the class reachable from the cycle has a single lock. The data suggest a quantitative form: **LPC-¼**, "a parity-clean class has F/N ≥ 1/4" (Track A's quarter floor, with the sphere hypothesis weakened to D on the class).
  - Proving the quarter floor from class-wide local duality alone would prove LPC, and with it R\* and 4CT. I see no such proof. The quarter-floor bijections of Track A (π-blocks, Conjecture E) are the natural place to check whether they use only D.
- **Recommendation.**
  - Keep LPC (better: LPC-¼) as the stated class-level target, labelled conjecture.
  - Use off-sphere π-cycle classes, especially the tight ones with filled = 2 × onCycles, as a test bed for any proposed quarter-floor argument: an argument that uses more than D would be refuted there.
  - Do not spend more CPU on random censuses: they contain no π-cycles.
  - If more CPU is spent, spend it on run (b): no-555 holes, phase-2 ratio objective, larger n, and genus 2 / rp2x3, which were not searched for cycles.
- **Data claim to hand to Track A.** At degree-5 holes on 6 surfaces (sphere, torus, Klein bottle, RP², genus 2, rp2x3), the quarter floor F/N ≥ 1/4 held in all 125,334 parity-clean classes. Where it fails, the class has a lock-parity violator. Conjecture **LPC-¼**: F/N ≥ 1/4 for every Kempe class whose unfilled states all satisfy D1, D2.
  - LPC-¼ ⇒ LPC.
  - On the sphere it is exactly the quarter floor.

## 9. LPC at frame-like holes off the sphere (7 Oct, evening; Track F second run) [exploratory, data]

Question: run (b) of §8.6 found only 65 graphs with all-DL π-cycles at no-555 holes, and only 3 parity-clean cycle classes. Does LPC, or LPC-¼ (a violator-free class has F/N ≥ 1/4), fail at **frame-like** holes when the search is pushed harder? A frame-like hole here is a degree-5 hole whose cyclic link-degree word has no three consecutive 5s and no consecutive 5,6,5 (stricter than run (b), which only excluded 555).

### 9.1 Method

- **Engine.** `src/kclass_pi2.cpp` → `src/kclass4` is `kclass_pi.cpp` with the per-class tuple extended to `cls2[size, filled, DL, single, minK, maxK, viol, onCycles, piPathEnds]`, so a cycle class can be read together with its size, filled count and violator count. Checked against kclass3 on every hole of 20 §8 cycle graphs (270 holes, 0 mismatches) and again on every verified item (below).
- **Search** (`src/lpc2_search.py`). Annealing flip walks (min degree 5, surface checked by Euler characteristic and orientability), evaluated **only at frame-like holes**. The score is lexicographic:
  1. any class containing an all-DL π-cycle (tier 1000), otherwise the longest DL π-run;
  2. then few lock-parity violators in cycle classes (300/(1 + min viol));
  3. then a low filled fraction in violator-free cycle classes (300/(4·F/N)); a small term 2/(4·F/N) over all violator-free classes is always added.

  Every graph with a cycle class, every violator-free class with F/N ≤ 1/4 and size ≥ 8, and every LPC / LPC-¼ counterexample is logged (`out/lpc2/s_*.jsonl`). Size-4 equality classes [4,1] are only counted.
- **Starts.** Four kinds:
  - *random*: `surfaces.make`, n = 22–48 per surface, plus one worker at n = 45–60. At n = 60 a hole has about 10⁶ states (about 5 s in kclass4), so n ≥ 50 got few walks.
  - *prevseed*: the §8 graphs with a frame-like cycle hole (`src/lpc2_prev.py` → `out/lpc2/prev_seeds.txt`, 103 holes).
  - *focus*: the 40 graphs with the lowest violator-free cycle-class F/N found by 19:50.
  - *glue*: the 13 Census29 sphere graphs with all-DL π-cycles, each connected-summed (glued along a face as far as possible from the cycle hole) with a small 4-colourable min-degree-5 triangulation of the torus, Klein bottle, RP², genus 2 or rp2x3 (n = 37–58). Note that K6 = `RP2_6` is not 4-colourable, so pieces come from a checked pool.
- **Compute.** 6 workers, all under `nice -n 10`, 18:35–21:17. Load stayed at 16–28, so there was no need to drop to 3 workers. In total 1,113,506 kclass4 evaluations and 2,833 walks (rp2 1,726, klein 482, torus 341, genus 2 148, rp2x3 136). 3 evaluations timed out at 90 s.
- **Verification** (`src/lpc2_verify.py`, `out/lpc2/verify/`). Each item (graph, hole) is run through:
  - kclass3 (the §8 engine, unchanged) and kclass4: class list, cycle lengths, and [onCycles, pathEnds, filled];
  - `lpc_detail.analyse` (pure Python, no shared code; it now also emits `cls2`): class list, `cls2`, cycle lengths, Theorem P;
  - `kclass_py.py` (pure Python, enumerates all colourings): the class-size histogram.

  The items are: every violator-free cycle class (up to 3 instances per class signature), 60 dirty cycle classes (the 30 with fewest violators plus 30 random), the 40 largest non-trivial equality classes, and every counterexample event (there were none).
- **Sphere comparison** (`src/lpc2_sphere.py`): the 13 Census29 graphs with all-DL π-cycles (17 cycles at 16 holes), run through the same analysis.

### 9.2 Results

**Sphere (Census29, n = 30–32; `out/lpc2/sphere_holes.jsonl`, `sphere_verify.jsonl`).**
- All 16 cycle holes are frame-like (55757 ×12, 55666 ×2, 55667 ×2).
- Each cycle sits in the **giant class** of its hole, which is the only class that contains a cycle: N = 3,122–8,458, F/N = 0.441–0.545, viol = 0 (LP holds on the sphere).
- Filled per cycle state is 98–196: the classes are nowhere near all-cycle.
- All 16 holes agree across all four engines.

**Off the sphere, frame-like holes** (`out/lpc2/report.txt`). Instances are distinct (WL graph hash, hole word, class tuple). Rows are grouped by start type, because seeded walks revisit one family many times.

| start | surface | n | graphs with a cycle class | cycle-class instances | violator-free | min viol (all) | min F/N, violator-free cycle classes | min filled / onCycles (violator-free) |
|---|---|---|---|---|---|---|---|---|
| random | RP² | 22–33 | 57 | 57 | 13 | 0 | **7/18 = 0.389** | 1.4 |
| random | Klein | 29–43 | 165 | 210 | 7 | 0 | 0.389 | 1.4 |
| random | torus, genus 2, rp2x3 (n 24–60) | | 0 | 0 | 0 | — | — | — |
| prevseed | RP² | 24–33 | 746 | 653 | 117 | 0 | 0.389 | 1.4 |
| prevseed | Klein | 28–32 | 5,264 | 5,346 | 65 | 0 | 0.406 | 2.6 |
| prevseed | torus | 28–31 | 1,161 | 1,172 | **0** | 6 | — | — |
| focus | RP² | 28 | 144 | 145 | 65 | 0 | **3/8 = 0.375** | 1.4 |
| glue | torus | 45–52 | 179 | 516 | 495 | 0 | 0.458 | 90.9 |
| glue | Klein | 57–58 | 157 | 881 | 845 | 0 | 0.472 | 92.6 |
| glue | RP² | 37–44 | 105 | 155 | 149 | 0 | 0.468 | 79.0 |
| glue | genus 2 | 48–50 | 535 | 863 | 788 | 0 | 0.442 | 59.0 |
| glue | rp2x3 | 40–43 | 156 | 242 | 228 | 0 | 0.442 | 94.3 |

- Frame-like hole words with cycles include 55757, 55758, 55759, 55767, 55768, 55769, 55787, 55858, 55859, 55868, 55869, 55959, 55666, 55667, 55676, 55677, 55687, 55697, 55698, 56667, 56676, 56677, 56687, 56767, 5,5,8,5,10–12, 5,5,7,7,11, 5,7,7,8,10, 5,6,7,8,10 and 57777.
- Cycle lengths are again all multiples of 20, up to 580 in the glued Klein graphs.
- The §8 graphs re-filtered to frame-like holes (`out/lpc2/prev_frame.jsonl`) give 104 cycle classes (RP² 58, Klein 30, torus 16), of which 16 are violator-free (all on RP², minimum F/N 0.389). So §8's "3" was an undercount: run (a) graphs also carry frame-like cycle holes.

**Counterexamples.**
- **LPC: 0.** No class at a frame-like hole has filled = 0 and viol = 0, in any evaluation (1.1M evaluations, every class at every frame-like hole, not only cycle classes).
- **LPC-¼: 0.** No violator-free class has F/N < 1/4.

**Minimum filled fraction.**
- Over all violator-free classes at frame-like holes, the minimum is **exactly 1/4**. It is attained by 39,476 distinct non-trivial equality classes (size 8 up to 48,992, all of the form N = 4F, on all five surfaces), plus the [4,1] classes, which are counted only.
- Over violator-free **cycle** classes, the minimum is **3/8**: one RP² family at n = 28, hole 13, class [320, 120, 84, 116, 2, 9, 0, 20, 0] (one 20-cycle).
- The next floors are 0.3793 ([464,176,…,40 on cycles] and [696,264,…,60]), 0.383 ([188,72,…]) and 7/18 = 0.389 ([72,28,26,18,2,9,0,20,0], the smallest cycle class found, plus its multiples 144, 288, 576).
- The annealing went 0.406 → 0.389 → 0.375 in its first 75 minutes, then stalled at 3/8 for the last 85 minutes, focus walks included.
- **No equality class (F/N = 1/4) contains an all-DL π-cycle.** Every cycle class has F/N ≥ 3/8.

**Filled per cycle state.**
- In violator-free cycle classes it goes down to **1.4** (the [72,28,…,20 on cycle] class), below §8's "≥ 2 in all 339".
- So "filled ≥ 2 × onCycles" is **false** as a general rule. The F/N floor (≥ 1/4, here ≥ 3/8 for cycle classes) is the robust quantity.

**Violators in cycle classes.**
- The histogram of viol over the 10,240 cycle-class instances is continuous from 0: 2,772 at 0, then 1 at 2, 16 at 3, 21 at 4, … up to > 180.
- So "nearly clean" cycle classes exist (2 violators), but the step to 0 violators with 0 filled never happens.
- The torus prevseed family (1,172 instances, n = 31) never reached 0 violators (minimum 6).

**Glued lifts.**
- A sphere cycle class glued to a far handle or crosscap is, at the start, a product: the sphere class times the piece's Kempe classes. Sizes are multiplied, F/N is unchanged, and viol stays 0.
- Annealing from there kept the classes violator-free (2,505 of 2,657 instances) but never lowered F/N below 0.44. That is roughly the sphere value: the handle does not make a sphere cycle class thinner.

**Verification** (`out/lpc2/verify/res_all.jsonl` plus `rres_*.jsonl`, the late glue items).
- 751 + 226 items: kclass3 ≡ kclass4 on all of them. The 226 are glued (mostly genus-2) items checked by the C++ engines, with Python only at ≤ 20k states; the remaining late glue items were not re-verified, for lack of time.
- `lpc_detail` (Python) agrees on all 408 items with ≤ 150k states; `kclass_py` histograms agree on all 365 with ≤ 30k states.
- Theorem P has 0 failures in both engines.
- Every claimed class tuple is present in the verified class list.
- **Every class signature of a violator-free cycle class from the random, prevseed and focus starts passed all engines** (205 items, up to 3 per signature, including the 3/8, 0.3793, 0.383 and 7/18 classes). The 315 earlier glue classes without a Python check are large lifts (110k–550k states, F/N ≥ 0.472), checked by the two C++ engines only.

### 9.3 Verdict

- **LPC and LPC-¼ survive** at frame-like holes on torus, Klein bottle, RP², genus 2 and rp2x3.
- This is a much stronger test than §8:
  - 10,240 distinct cycle-class instances at frame-like holes (versus 65 graphs);
  - 2,772 violator-free ones (versus 3): 267 from random / seeded / focus walks, and 2,505 glued lifts;
  - 20 violator-free cycle classes from random starts (RP² 13, Klein bottle 7);
  - all five surfaces covered.
- **The quarter floor is tight but never broken** (39k distinct equality classes up to size 48,992). The searches drove violator-free cycle classes down only to **F/N = 3/8**, and no equality class contains a cycle.
- **Caveats.**
  - Random starts found violator-free frame-like cycle classes only on RP² and the Klein bottle (n ≤ 43). On the torus, genus 2 and rp2x3, all violator-free cycle classes come from the glued sphere lifts, which are products and therefore weak tests.
  - n ≥ 50 got few walks.
  - The search is local (flip walks), and the floor at 3/8 is one RP² family, so a deeper minimum is not excluded.
  - Survival here is evidence, not proof; LPC on the sphere is 4CT-strength.
- **For Track A.**
  - The off-sphere data support LPC-¼ in a sharper, cycle-aware form: **a violator-free class containing an all-DL π-cycle has F/N ≥ 3/8** (data, frame-like holes, five surfaces; the sphere minimum is 0.441).
  - A quarter-floor argument that uses only D should be tested on the small RP² classes [72,28] and [320,120] (`out/lpc2/report.txt`, "lowest-F/N" list, graphs in `s_focus.jsonl` / `s_prevseed.jsonl`).
  - The claim "filled ≥ 2 per cycle state" is refuted (1.4).

### 9.4 Files

| path | content |
|---|---|
| `src/kclass_pi2.cpp`, `src/kclass4` | kclass_pi + per-class [onCycles, piPathEnds] |
| `src/lpc2_search.py` | frame-like-hole annealing search (random / seeded / glued starts) |
| `src/lpc2_prev.py`, `src/lpc2_sphere.py` | §8 graphs and Census29 sphere graphs at frame-like holes |
| `src/lpc2_report.py`, `src/lpc2_verify.py` | aggregation and dedup; three/four-engine verification |
| `src/lpc_detail.py` | now also returns `cls2` (additive change) |
| `out/lpc2/s_*.{jsonl,out,progress}` | search logs (cyc / low / cex events), per-walk output, progress |
| `out/lpc2/report.txt`, `verify_items.jsonl`, `verify/` | tables; verification items and results |
| `out/lpc2/sphere_*`, `prev_*`, `focus_seeds.txt` | sphere comparison, re-filtered §8 graphs, seeds |
