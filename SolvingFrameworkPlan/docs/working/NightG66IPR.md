# NightG66IPR: the weak form on IPR fullerene duals, in Tait language

Night worker, 7 October 2026 (started 05:54 MDT). **Exploratory. Hand translation, checked by computation; a literature check (two web searches); one new exhaustive run on IPR duals of 32–46 vertices (scratchpad script, not committed). Unreviewed.**

Sources:
- NightG66 (whole note; ladder §4.1; F-dynamics §1.3; 2-ball silence §1.4); NightWeakForm (§0, §3: (6,6,6,6,6) must be in any unavoidable set);
- NightLog-2026-10-06 from "05:03 — Studio Job AW" to the end;
- Lean docstrings of `QuarterBitDynamics` (`dd_step_bits`, `allDL_cycle_length_dvd_ten`, `pureClean_of_no_allDL_orbit`), `QuarterHole66`, `QuarterNonDLImage`;
- Studio intel data: `studiointel/ipr/ipr_32_52.jsonl` (exact Kempe radius at all 15,204 holes of all 1,267 IPR duals of 32–52 vertices) and `studiointel/flat/kclass_{56,58,60,62}.jsonl` (Kempe class counts at 153 flat holes); message `2026-10-06_1640_studiointel_..._hybrid-checks-a-b-c-IPR-final.md`;
- engine: `studiointel/radius.py` (state enumeration, `classify`, `comp`), π as in `fcycle_census.F`.

Labels as in NightG66: [formal], [proved], [computed], [data] (someone else's run, re-aggregated here), [sketch], [lit-H/M/L].

## 0. Bottom line

1. **Translation [proved, and checked on every unfilled state of 1,000+ holes].** Let F be the fullerene, T = F* its dual, h a degree-5 vertex of T, P the pentagon of F dual to h, and F − P the cubic "5-pole" with five legs s₀..s₄ (s_t is the spoke between the hexagons H_t = x_t and H_{t+1} = x_{t+1}).
   - States of T − h modulo S₄ ↔ 3-edge-colourings of F − P modulo S₃ (colour of edge uv* = c(u) + c(v) in ℤ₂²).
   - **Filled ⇔ the triple leg colour sits on three consecutive legs.** By the parity lemma every leg word is 3+1+1.
   - **Unfilled at j ⇔ the leg word is (γ₁, γ₁, γ₂, γ₁, γ₃) at s_j..s_{j+4}**, with γ₁ = α+μ = A+B, γ₂ = α+A = μ+B, γ₃ = α+B = μ+A.
   - **Lock1 ⇔ the {γ₁,γ₂}-Kempe paths of F − P pair the legs (s_j s_{j+3})(s_{j+1} s_{j+2}).**
   - **Lock2 ⇔ the {γ₁,γ₃}-paths pair (s_j s_{j+4})(s_{j+1} s_{j+3}).**
   - So DL means that both Kempe path systems take the "wrong" non-crossing pairing. The {γ₂,γ₃}-path always joins s_{j+2} to s_{j+4}. This is exactly Kempe's 1879 pentagon case in edge form, i.e. the Heawood situation.
   - **π = swap γ₁ ↔ γ₃ on the Lock2 inner path Π (s_{j+1} → s_{j+3})**, together with the closed {γ₁,γ₃}-cycles bounding holes of the region that contains H_{j+2}. The new triple is γ₃ on s_{j+3}, s_{j+4}, s_{j+1}, so the repeat index is j+3, as in `rot3_move`.
2. **Kempe classes coincide [proved].** Vertex-Kempe classes of T − h (mod S₄) are exactly the edge-Kempe classes of F − P (mod S₃), where a switch is allowed on a bicoloured cycle or on a leg-to-leg bicoloured path. So:
   - **G66^IPR in Tait form:** for an IPR fullerene F, some pentagon P has the property that every edge-Kempe class of 3-edge-colourings of the 5-pole F − P contains a colouring whose triple leg colour is on three consecutive legs (one that extends over P).
   - **G66 in Tait form:** every pentagon has that property.
3. **What fullerene/Kempe theory gives [proved + lit].**
   - If all Tait colourings of F are Kempe-equivalent, then all *filled* states of F − P lie in one class (restriction maps F-switches to sequences of F − P switches).
   - That says nothing about classes with no filled state, which are exactly the danger (C1). So whole-fullerene Kempe uniqueness is **neither known nor sufficient**.
   - The known uniqueness theorem (Belcastro–Haas: 2-connected planar **bipartite** cubic graphs have one edge-Kempe class) does not apply: fullerenes have 12 pentagons, and a 5-pole is not a closed cubic graph.
   - Mohar's k = 3 conjecture ("all 3-edge-colourings of a cubic graph ≠ K₄ form one Kempe class") is false in general (Goedgebeur–Östergård: families with 2ⁿ classes).
4. **No proof.** The obstruction is exact and is the same one as in NightG66:
   - the DL conditions are pairing conditions on three Kempe path systems, which the hexagon/pentagon face structure does not constrain locally (the 2-ball is silent at all-6 holes; NightG66 §1.4);
   - the torus has targetless 66666 classes, so planarity must enter globally;
   - the fullerene's distinctive invariants (face sizes 5/6, IPR, cyclic 5-edge-connectivity) are local or cut-level, and none of them bounds a Kempe path's route.
   - §3 lists what a proof would need.
5. **Data: G66^IPR, and G66 itself, hold on every IPR fullerene C60–C100 [data], and G66⁰ holds on C60–C88 [computed, new].**
   - Studio's exact radius run: on all 1,267 IPR duals of 32–52 vertices (C60…C100), 15,204 holes, there is **no targetless class**. So every Kempe class at every hole has a filled state, i.e. PureClean at *every* degree-5 vertex. This is G66 restricted to these graphs, which is stronger than G66^IPR.
   - Flat holes at C108–C120 (153 holes): **κ(T − h) = 1** (a single Kempe class) every time.
   - New here: on all IPR duals of 32–46 vertices (C60–C88), there are **0 all-DL π-cycles**, so G66⁰ holds there. T1 (`dd_step_bits`) holds on every DD step, and the Tait lock translation has 0 mismatches. See §4 for the table.
   - **But the longest DL run grows with order:** 2 at C60, 5 at C70, 10 at C78, 14 at C82, 23 at C88. Runs of length ≥ 10 are long enough to close a cycle (10 ∣ L). G66⁰ (orbit level) is therefore the fragile rung. The class-level G66 / G66^IPR is what the data support robustly.

## 1. The translation in detail

### 1.1 Objects

- T = F* is a triangulation with degrees 5 (12 vertices, pairwise non-adjacent by IPR) and 6. A degree-5 vertex h has all-6 link x₀..x₄, so every hole of an IPR dual is a `Hole66` hole.
- Faces of T − h ↔ vertices of F − V(P). Inner edges of T − h ↔ edges of F not incident to P.
- The five link edges x_t x_{t+1} are dual to the five spokes s_t, which in F − P are legs (pendant half-edges) attached to the vertex v_t = face (x_t, x_{t+1}, w_t). **The w_t of `Hole66` are the five second-ring faces of F that meet two first-ring hexagons**, and m_t is the remaining outer neighbour face of H_t (the one meeting only H_t among the first ring). These can be pentagons: in C60 every w_t is a pentagon and every m_t a hexagon, since the faces around a C60 hexagon alternate 5, 6.
- Colour group ℤ₂² = {0, a, b, c}. Edge colour of uv* is c(u)+c(v) ∈ {a, b, c}, and properness ⇔ every vertex of F − P sees three distinct colours. The map from 4-colourings to Tait colourings is 4:1, with fibres given by ℤ₂² translation. Hence S₄ = ℤ₂² ⋊ S₃ classes ↔ S₃ classes.

### 1.2 Leg words

- Leg colour e_t = c(x_t) + c(x_{t+1}), so Σe_t = 0.
- Parity lemma (the 5-edge cut around P): each colour occurs an odd number of times among the legs, so the word is 3+1+1.
- Link (α, μ, α, A, B) at j gives e = (γ₁, γ₁, γ₂, γ₁, γ₃) at j..j+4. The triple sits at {j, j+1, j+3}: two adjacent legs, around **H_{j+1} = the μ vertex**, plus one isolated leg.
- A 3-coloured link gives a triple on three consecutive legs (check the two shapes ababc and abacb). So **filled ⇔ the triple is consecutive ⇔ the colouring extends over P**.
- The repeat index is read off the legs: H_{j+1} is the unique first-ring hexagon both of whose spokes carry the triple colour and whose two neighbouring spokes do not both carry it.

### 1.3 Locks as leg pairings [proved; computed 0 mismatches]

- A {p,q}-Kempe component of T − h is a connected region of the disc (sphere minus P) cut along the {δ,ε}-bicoloured cycles and leg-to-leg paths of F − P, where {δ,ε} is the complement of p+q.
  - Proof: faces on either side of a δε-edge have colour sums in {δ,ε}, i.e. one face is in {p,q} and the other in {r,s}. Faces joined across a (p+q)-edge are in the same pair class.
- Lock1 asks whether x_{j+3} is in the {μ,A}-component of x_{j+1} (pair sum γ₃). The cutting curves are the {γ₁,γ₂}-paths. Their leg ends are s_j, s_{j+1}, s_{j+2}, s_{j+3}, which pair in one of two non-crossing ways:
  - (s_j s_{j+1})(s_{j+2} s_{j+3}) puts H_{j+1} in the pocket of the first path, so **no Lock1**;
  - (s_j s_{j+3})(s_{j+1} s_{j+2}) puts H_{j+1} and H_{j+3} in the band between the paths, so **Lock1** (the band is connected and closed cycles do not separate it from the boundary hexagons).
- Lock2 is the same argument with {γ₁,γ₃}-paths on legs s_j, s_{j+1}, s_{j+3}, s_{j+4}: Lock2 ⇔ (s_j s_{j+4})(s_{j+1} s_{j+3}).
- Check: `tait_pairing` in the scratchpad script computes the pairings by walking the bicoloured paths of the dual. It agrees with `radius.classify` on **every unfilled state** at every hole of the 37 IPR duals with 32–43 vertices (C60–C82), and at A₃, the icosahedron and GC(2,0).

### 1.4 The moves

- An edge-Kempe switch on a closed δε-cycle C of F − P is a ℤ₂²-translation by p+q on the side of C away from P. That is a composition of vertex swaps (no {p,q}- or {r,s}-component crosses C).
- A switch on a leg-to-leg path is the same with one side of the path.
- Conversely, a vertex swap of K is the switch of every boundary curve of K's region; these curves are disjoint, so the switches can be done one at a time.
- So the classes coincide (§0 item 2).
- **π (R₊₃) in Tait form:** the {α,A}-component K of x_{j+2} has pair sum γ₂, so its boundary curves are {γ₁,γ₃}-curves. Under Lock2, H_{j+2} lies in the pocket of Π = the (s_{j+1} s_{j+3}) path. π switches γ₁ ↔ γ₃ on Π and on every closed {γ₁,γ₃}-cycle bounding a hole of that pocket region. The legs s_{j+1} and s_{j+3} become γ₃, so the word is (γ₁, γ₃, γ₂, γ₃, γ₃): unfilled at j+3.
- **σ** (`sigSwap`, the {α,μ}-component of x_{j+1}, sum γ₁) switches γ₂ ↔ γ₃ on the (s_{j+2}, s_{j+4}) path and on the boundary cycles of x_{j+1}'s region. It changes no leg of colour γ₁, which is why the repeat index stays j.

### 1.5 An all-DL orbit in Tait form

An all-DL orbit is a cyclic sequence of 5-pole colourings. At each one:
- the {γ₁,γ₂}-paths pair (j, j+3)(j+1, j+2);
- the {γ₁,γ₃}-paths pair (j, j+4)(j+1, j+3);
- switching the γ₁γ₃ pocket path Π (plus its hole cycles) produces the same picture rotated by 3 with (γ₁, γ₂, γ₃) ↦ (γ₃, γ₁, γ₂).

The last claim follows from the renaming α′ = α, μ′ = B, A′ = μ, B′ = A of NightG66 §1.1: γ₁′ = α+B = γ₃, γ₂′ = α+μ = γ₁, γ₃′ = α+A = γ₂. So the leg colours cycle with period 3 and the index with period 5, which gives the absolute period 30 ∣ L of NightG66 §1.3.

In this language the formal bit dynamics (`dd_step_bits`) is the statement that the colours of the 10 edges joining the w-hexagons to the first ring move by the signed rotation F. It is pattern-free because those edges lie in the 2-ball.

## 2. What fullerene theory gives

| fact | source | confidence | consequence here |
|---|---|---|---|
| fullerenes are 3-edge-colourable | 4CT; for fullerenes also direct constructions | lit-H | states exist at every hole; says nothing about classes |
| every 2-connected planar bipartite cubic graph has exactly one edge-Kempe class | Belcastro–Haas, "Counting edge-Kempe-equivalence classes for 3-edge-colored cubic graphs" (Discrete Math. 2014; arXiv 1209.1730) | lit-H (confirmed by search) | not applicable: fullerenes are not bipartite. Dually, Eulerian triangulations have Kempe-unique 4-colourings (Fisk 1977, lit-M), and IPR duals have twelve odd vertices |
| Mohar's conjecture (k = 3: one Kempe class for cubic ≠ K₄) is false; cubic graphs with 2ⁿ classes exist; tables to order 30 | Goedgebeur–Östergård, "Switching 3-edge-colorings of cubic graphs" (Discrete Math. 2022; arXiv 2105.01363) | lit-H (confirmed) | uniqueness is not automatic; whether *planar* cubic graphs, or fullerenes, can have ≥ 2 classes should be read off their tables (not done) |
| fullerenes are cyclically 5-edge-connected; nontrivial cyclic 5-edge-cuts occur only in nanotube-type fullerenes | Došlić 2003; Qi–Zhang 2008; Kardoš–Škrekovski 2008 | lit-M | P's spoke cut is the unique 5-cut through P (generic case). A Kempe leg path plus part of P is a cycle, but bicoloured paths are long and wind, so no cut bound applies |
| exponentially many perfect matchings | Kardoš–Král'–Miškuf–Sereni 2009 | lit-M | the γ-classes are perfect matchings; abundance, but no Kempe connectivity |
| all Tait colourings of F Kempe-equivalent ⇒ all filled states at every pentagon are in one F − P class | [proved here]: an F-switch through P restricts to ≤ 2 disjoint leg-path switches (the cycle enters and leaves P through legs; P has 5 vertices, each with one γ-edge, so a bicoloured cycle meets P in at most two arcs) plus switches off P | proved | the filled states form **one** class; G66 ⇔ no *other* class |

**The key negative point.** G66^IPR is about classes of the 5-pole that contain *no* extendable colouring. No theorem about colourings of the closed fullerene sees them. The tool that does see them is Kempe uniqueness for the 5-pole, which is the Studio's κ(T − h) = 1. A theorem "κ(F − P) = 1 for every pentagon of every IPR fullerene" would be a Belcastro–Haas-type result for a non-bipartite planar 5-pole. It would imply G66 on IPR duals. It cannot be pattern-local, because the torus 66666 holes have targetless classes (NightWeakForm §4: 101/196).

## 3. Proof attempt and the exact obstruction

What one would like:
- (a) an all-DL orbit forces Π (the γ₁γ₃ pocket path from s_{j+1} to s_{j+3}) to keep the same "shape" through all 30 absolute steps;
- (b) a winding or length invariant of the path systems that changes monotonically along the orbit;
- (c) a contradiction from F's finiteness.

Where it fails:
1. **No monotone invariant exists at the vertex level** (NightG66 M1, NightClosedSets: 14 descents fail). The Tait picture adds the *lengths* of the three leg-path systems and the *number of closed bicoloured cycles*.
   - A switch on Π leaves every path of the other two colour pairs as a set of edges but rewires them at Π's vertices. Path lengths can go up or down.
   - The only conserved quantity is the parity data (`delta_rank_odd'`: Σ rank changes by an odd amount), which gives 2 ∣ L and nothing more.
2. **The face structure is invisible to the locks.** The pairing conditions of §1.3 are topological (which legs a path joins), not metric. Hexagons versus pentagons change which paths are *possible*, but the 2-ball model already allows all 32 w-words and 74 ring colourings per index (NightG66 §1.4). IPR says only that the link is all-6. The second ring may contain pentagons (in C60 all five w_t are pentagons, at dual distance 2 from h), and the 2-ball model of NightG66 §1.4 does not use second-ring degrees. So even the extra degree-5 vertices of small IPR fullerenes are not seen at radius 2. The "hexagonal cone" of T6 does not occur in small IPR fullerenes.
3. **Pentagram crossing (NightG66 M4) in Tait form.** The Lock2 paths Q_n (n = step) pair the legs (s_{j_n}, s_{j_n+4}) and (s_{j_n+1}, s_{j_n+3}). Consecutive steps use leg pairs rotated by 3, so Q_n and Q_{n+2} must cross. Each crossing is a vertex of F where the colours γ₁^{(n)}γ₃^{(n)} and γ₁^{(n+2)}γ₃^{(n+2)} = γ₂^{(n)}γ₁^{(n)}-paths meet, i.e. a shared γ₁^{(n)}-edge. This is the only sphere-specific input found, and it is satisfiable: all-DL cycles exist at 55666 and 55757.
4. **Curvature does not help directly.** A fullerene has total curvature concentrated at 12 pentagons. A lock path enclosing a pocket with k pentagons has its turning number fixed by k (Gauss–Bonnet on the hexagonal lattice). A candidate statement would be "an all-DL orbit needs a pocket containing ≥ 1 further pentagon". The data give no support to a small-radius rule: max DL runs of 5–23 already occur at C70–C88, while the C60 runs stop after 2 steps although pentagons sit at distance 2. I found no way to make it quantitative.

**Exact obstruction.** In Tait form G66 is a Kempe-connectivity statement for the 5-pole F − P (planar, cubic, one pentagonal boundary of 5 legs, all other faces 5 or 6). Every known Kempe-uniqueness proof (Fisk; Belcastro–Haas; Mohar) uses a global parity/orientation structure: Eulerian triangulations, i.e. bipartite cubic graphs, where every Kempe cycle is even and the colouring is determined by a height function. Fullerenes break exactly this at the 12 pentagons. The question is therefore *whether 12 isolated defects can create a second Kempe class of the 5-pole with no extendable colouring*. That is a genuinely new statement. It is not known to be easier than the general case (cf. NightWeakForm §3.4).

A possible route [sketch, untested]: a height-function argument on the hexagonal parts.
- Away from pentagons a Tait colouring of the hexagonal lattice has a ℤ²-valued height (the 3-colouring/dimer ↔ height correspondence for the honeycomb).
- A Kempe switch on a closed cycle C changes the height by a constant inside C.
- The 12 pentagons are the height's monodromy points (each carries a ℤ₃-twist of the colour cyclic order).
- An all-DL orbit realises the 30-step colour rotation (γ₁, γ₂, γ₃) ↦ (γ₃, γ₁, γ₂) around P. One would try to show that the accumulated monodromy around P after one period is nontrivial unless some pocket swallows a second pentagon, and then use IPR distances to bound that.
- **Gap:** heights are only locally defined (12 defects), and I have not checked whether the long DL runs at C78–C88 (up to 23) have pockets containing pentagons (T-IPR4). I do not believe this closes. It is recorded as the one fullerene-specific idea.

## 4. Tests

### 4.1 Already done [data, Studio intel]

| set | holes | result |
|---|---|---|
| all IPR duals, 32–52 vertices (C60–C100), 1,267 graphs | 15,204 | ρ ∈ {2, 3, 4}; **no targetless class**, so PureClean at every hole (G66 on this set) |
| C60 dual | 12 | ρ = 2 |
| flat holes (link and second ring all degree 6) in IPR duals of 56–62 vertices (C108–C120, part 0/400 samples) | 153 | **κ(T − h) = 1 at every hole**; 0 classes without a filled state |

### 4.2 New here [computed]: G66⁰ on IPR duals

Script: scratchpad `g66ipr/g66ipr.py` and `drive.py`. For each hole it enumerates the canonical states (`radius.enumerate_states`) and restricts to DL states. It then iterates π (the {α,A}-component of x_{j+2}) on canonical states and records:
- all-DL π-cycles;
- the longest forward DL run (number of consecutive DL states before an exit);
- the T1 check (bits of NightG66 §1.3 move by bitF on every DD step);
- the Tait lock check of §1.3 (every unfilled state, orders ≤ 43).

Sanity checks:
- A₃ (17 vertices): one all-DL cycle, L = 20 canonical, as expected.
- icosahedron: 0 DL states.
- the leapfrog of the icosahedron (32 vertices, the C60 dual) reproduces the 4,840 states and 130 DL states of the C60 entry in Studio's file.

| dual order (fullerene) | graphs | holes | DL states per hole | all-DL π-cycles | longest DL run | T1 fails | Tait mismatches |
|---|---|---|---|---|---|---|---|
| 32 (C60) | 1 | 12 | 130 | **0** | 2 | 0 | 0 |
| 37 (C70) | 1 | 12 | 900–1,192 | **0** | 5 | 0 | 0 |
| 38 (C72) | 1 | 12 | 1,073 | **0** | 6 | 0 | 0 |
| 39 (C74) | 1 | 12 | 2,400–2,763 | **0** | 8 | 0 | 0 |
| 40 (C76) | 2 | 24 | 3,160–3,817 | **0** | 7 | 0 | 0 |
| 41 (C78) | 5 | 60 | 3,145–5,176 | **0** | 10 | 0 | 0 |
| 42 (C80) | 7 | 84 | 2,660–6,662 | **0** | 11 | 0 | 0 |
| 43 (C82) | 9 | 108 | 5,973–11,682 | **0** | 14 | 0 | 0 |
| 44 (C84) | 24 | 288 | 7,414–17,091 | **0** | 15 | 0 | not run |
| 45 (C86) | 19 | 228 | 9,207–23,385 | **0** | 15 | 0 | not run |
| 46 (C88) | 35 | 420 | 11,112–36,784 | **0** | 23 | 0 | not run |
| **total** | **105** | **1,260** | | **0** | | **0** | **0** (orders ≤ 43) |

Distribution of the per-hole longest DL run over the 1,128 holes at orders 42–46: 5 (26), 6 (108), 7 (342), 8 (325), 9 (174), 10 (73), 11 (41), 12 (12), 13 (8), 14 (10), 15 (6), 16 (2), 23 (1).

Reading:
- G66⁰ holds on every hole of every IPR fullerene C60–C88, so by `pureClean_of_no_allDL_orbit` G66 holds there with a *formal* bridge from the computed fact.
- The longest DL run grows roughly with order. Runs ≥ 10 (a full F-period) exist from C78 on. The pattern-free dynamics would allow a cycle as soon as a run closes up.
- **Prediction: G66⁰ fails on some IPR fullerene of moderate order** (the census found all-DL cycles at other patterns at orders 22–24). G66 / G66^IPR, which are class-level, should survive: Studio's κ = 1 data support them.

### 4.3 For Jobs BO/BR (all-6 DL runs) and next

- **T-IPR1 (orbit level).** Extend §4.2 to all IPR duals of 47–52 vertices and to the n = 56–62 samples, with the fast C++ engine. Report the run-length distribution, the first all-DL π-cycle (graph, hole, L; expect 10 ∣ L, absolute 30 ∣ L), and for it the Tait picture: Π's length and the number of pentagons in each pocket along the cycle.
  - A cycle kills G66⁰ on IPR only. Then check its class for a filled state (G66).
- **T-IPR2 (class level, the real target).** κ(T − h) at every hole of every IPR dual of ≤ 52 vertices, and at all flat and non-flat holes of the 56–62 samples.
  - Any κ ≥ 2 is the first evidence of a second 5-pole class.
  - A class with no filled state kills G66 on IPR. G66^IPR then needs some other pentagon of the same F, so check all 12.
- **T-IPR3 (literature/data, cheap).** From the Goedgebeur–Östergård tables (Zenodo dataset), extract the planar cubic graphs with ≥ 2 edge-Kempe classes and check whether any fullerene (C20–C30) appears. Also compute κ for the closed fullerenes C60–C100 directly; one class is expected. This decides whether "Tait-Kempe uniqueness for fullerenes" is even true, which §2 needs for its filled-class statement.
- **T-IPR4 (pocket pentagons).** On every DL run of length ≥ 5 at C70–C100, record the number of pentagons enclosed by the Lock2 pocket path Π at each step. The §3 sketch predicts that long runs need pockets containing pentagons. If some long run has all-hexagonal pockets, drop the sketch.
- **Lean (cheap, optional).** `tait_lock`: Lock1 ⇔ the pairing statement, on `SphericalMap` via the existing Kempe-duality lemmas (`reach_alpha_B_of_not_lock1`, `sphere_pair_duality`). This is only worth formalising if the height route revives.

## 5. Caveats

- The Tait translation of the locks is proved by a Jordan-curve argument on the disc (§1.3). It is checked computationally on every unfilled state at orders ≤ 43, but it is not formal.
- "No targetless class" (Studio) and "no all-DL π-cycle" (§4.2) are different: the first is G66, the second G66⁰. By `pureClean_of_no_allDL_orbit` the second implies the first.
- §4.2 uses the Python engine (`radius.py`) and canonical states. π commutes with colour renaming, so canonical cycles ↔ labelled cycles (lengths can differ by the renaming period).
- Literature rows marked lit-M were not re-checked: cyclic edge-connectivity, perfect matchings, Fisk. The two lit-H rows were confirmed by search (arXiv 1209.1730; arXiv 2105.01363).
- The script is in the session scratchpad and is not committed (about 150 lines).
