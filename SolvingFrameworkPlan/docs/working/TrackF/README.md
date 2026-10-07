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
| **LPC:** at a degree-5 hole of a triangulation of any surface, a Kempe class of T − h all of whose unfilled states satisfy LP(a,b) contains a filled state | class | **conjecture.** Torus: 24,042 / 24,042 parity-clean classes filled; 21,915 / 21,915 targetless classes not parity-clean. On the sphere LP always holds, so LPC ⇒ PureClean everywhere ⇒ R\* ⇒ 4CT (4CT-strength). Orbit-level analogue is FALSE: sphere all-DL π-cycles (e.g. order-24 75755, 55555) are parity-clean. |
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
