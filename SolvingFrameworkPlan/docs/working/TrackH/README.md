# Track H: why do small cycle classes contain filled states? [exploratory]

Studio, 7 Oct 2026, night. Nothing here is committed, and nothing outside `TrackH/` was changed; the Track A/F/G engines and data were used read-only. Labels: **[hand, unreviewed]** = hand proof, not yet reviewed; **[data]** = computation; **[verified]** = checked by two or three independent engines in this directory. Compute: at most 2 worker processes, all under `nice -n 10`.

## 0. Bottom line

1. **No proof of LPC can be of local type.** By "local type" we mean a proof that uses only facts stated at the hole: the dualities D1/D2, the parity identities P1–P3 (lock parity), Lemma A, Lemma P, and π/π̃ being mutually inverse.
   - The evidence is explicit **general graphs** (not surfaces) with a degree-5 vertex h whose link is an induced 5-cycle. In each one, a Kempe class of G − h is **one all-DL π-cycle of length 10 and nothing else**: no filled state, and no D-violator (no π-path end).
   - The sharpest one (`lp_general_min.txt`, 28 vertices, 109 edges): **D1, D2, P1, P2, P3 and lock parity hold at all 10 states**. Every hole-local fact used in Tracks C/F/G holds, and the conclusion of LPC fails. Verified three ways (§4).
   - So whatever makes LPC true on surfaces lives in the triangulation away from the hole.
2. **The hypothesis "D1/D2 hold along the π-cycle" is empty.** Every state of an all-DL π-cycle satisfies D1 and D2 automatically, on any graph (Lemma H0).
   - A lemma "if D holds along a π-cycle then some σ-image is not DL" would therefore be σ-escape for every π-cycle in every graph.
   - That is false in general graphs: in both counterexamples σ is a pure renaming at every state.
3. **Pattern in the small test beds [data].**
   - Exits from the cycle are almost all σ itself, or a link-free {α,μ}-swap that equals σ up to renaming. They land on **lockless** states (in′ = 11), and a filled state is reached one Lemma-A move later (dF = dS + 1 ≤ 4).
   - Whether σ exits is governed by the component counts (#{α,μ}, #{A,B}) of the state:
     - σ never exits when {α,μ} is connected (σ is then a renaming);
     - on the sphere it exits at 128 of 132 cycle states with #{A,B} = 1 and #{α,μ} ≥ 2.
   - At C30#0, σ exits exactly at the 10 states where K_{αμ}(x_{j+2}) is the link triple itself.
4. **What separates the counterexamples from the sphere: rigid states.**
   - Call a DL state *rigid* if its six pair graphs have the minimum component counts (1,1,2,1,2,1). A class made only of rigid states is a single all-DL π-cycle with no exits (Lemma H5). Both general-graph counterexamples are such rigid cycles.
   - On a closed triangulated surface an exact **edge-balance / Euler identity** holds per partition (Lemma H3). On the sphere it makes rigid states exactly the Tait colourings whose bicoloured cycles all pass through the hole.
   - **Data conjecture "rigid isolation" (sphere):** if c is rigid, then π(c) is not rigid.
     - 0 counterexamples among 22,053 rigid states at 10,812 holes of 712 sphere triangulations (24-vertex min-degree-5, frame class 22–28, fullerene duals, the Census29 cycle graphs);
     - 0 among all 17,059 rigid states of the planar chord model up to 15 cubic vertices (exhaustive, validated against the vertex engine; §6);
     - 0 in a falsification flip search on spheres (≈6k graphs; the closest misses have excess 1).
   - Rigid isolation **fails on RP²** (36 rigid→rigid steps in 15 graphs, runs of length 2; D holds at both states in all 10 checked), and in general graphs. It implies "rigid LPC" on the sphere: no class consists of rigid states only.
   - It is the first concrete sphere-only fact, beyond D, that excludes the counterexample shape. I could not prove it by hand.
5. **Verdict.**
   - There is no candidate proof mechanism for LPC that uses only duality at the hole; §4 gives a precise reason, an explicit configuration.
   - The mechanism visible in the data (σ / {α,μ}-exits to lockless states) works on surfaces only because the triangulation forces {α,μ} to be disconnected somewhere along every cycle. In the counterexamples it is connected everywhere.
   - The smallest new target this suggests is the rigid-isolation lemma on the sphere (§6). It is a statement about Hamiltonian-cycle-plus-chords Tait colourings, checkable and possibly provable, but it covers only the extreme (Kempe-degree-2) shape of a counterexample.

### 0.1 The brief's questions, answered

| question | answer |
|---|---|
| Does σ exit DL at a fixed phase of the 10-step period? | **No.** The σ-exit set has period 10 in only 4 of the 6 test beds, and the phase varies from hole to hole (§1.1) |
| Does the exit land on a single-lock state, from which Lemma A gives a filled state? | Mostly it lands on a **lockless** state (both π and π⁻¹ lead to filled states), sometimes on a single-lock state. A filled state is always one Lemma-A move further on; never directly |
| Does the parity of K_{αμ} (P3, always odd) force anything? | **No.** P3 holds at all states of the closed general-graph class `lp_general_min.txt` |
| Can one prove "D1/D2 along a π-cycle ⇒ some σ-image is not DL"? | The hypothesis always holds (H0), so this is σ-escape outright. It is **false in general graphs** (σ is a renaming along the whole counterexample cycle), so any proof must use the surface. Open on surfaces |
| Is there a configuration where all local facts hold and the conclusion fails? | **Yes, in general graphs** (§4): D1, D2, P1–P3 and lock parity hold at every state of a 10-state all-DL class with no filled state. **None on surfaces**: Track F's 1.1M evaluations, plus §5 here and the frozen-2-ball runs (282k evaluations, always ≥ 1 violator) |

## 1. Test beds and engines

**Engines** (new, pure Python, independent of kclass*/kempe_py):
- `th_engine.py`: states up to renaming, every Kempe move, π, σ, locks, D, P quantities, all-DL cycles, BFS distances.
- `th_bruteverify.py`: absolute colourings, no shared code.
- `kclass4` (TrackF) is used read-only as the fast evaluator in the searches.

The engine reproduces every class tuple below from `TrackF/out/lpc2/report.txt` and the sphere list.

| test bed | surface | hole word (link degrees) | hole states | cycle class [N, F, DL, S, N₀, viol] | cycle | σ-exit string (π order) |
|---|---|---|---|---|---|---|
| `rp2_s203_w16_t114` h21 ("7/18") | RP² | 5,8,5,5,9 | 802 | [72, 28, 26, 12, 6, 0] | 20 | `.s.s.s.....s.s.s....` |
| `rp2_s205_w2_t-1` h13 ("3/8") | RP² | 5,5,7,6,7 | 348 | [320, 120, 84, 88, 28, 0] | 20 | `ss...s.s.sss...s.s.s` |
| `C30#0` h0 | sphere | 55555 | 100 | [100, 40, 30, 20, 10, 0] | 20 | `.s.s.s.s.s.s.s.s.s.s` |
| `p30.r10#1252` h19 | sphere | 7,5,7,5,5 | 3976 | [3976, 1884, 472, 928, 692, 0] | 20 | `ss.s.s.s.s.s.s.s.s.s` |
| `p31.r1#7302` h27 | sphere | 55757 | 3784 | [3784, 1886, 414, 828, 656, 0] | 20 | `..sssss...s...s...s.` |
| `p31.r13#292235` h3 | sphere | 55666 | 3122 | [3122, 1608, 321, 726, 467, 0] | 20 | `s.s.s.s.s.s.s.s.s.s.` |

Full per-state dumps are in `out/dump_*.txt` and `out/dumps.jsonl`; σ anatomy is in `out/sigma_*.txt`. Each dump line gives:
- the absolute (normalised) link colouring, j, Lock1/Lock2, inA/inB;
- |K_{αA}|, |K_{αB}|, |K_{αμ}| of x_{j+2}, with their odd-G-degree counts in brackets;
- the σ-image type and locks;
- every Kempe move leaving DL (role pair, link positions met, target type);
- dS / dF (distance to a non-DL / filled state) and a shortest path to a filled state.

### 1.1 What the dumps show [data]

- **Parity.** Every cycle state has inA = inB = 0, L1 = L2 = 1, and odd counts in K_{αA}, K_{αB} and K_{αμ} (P1–P3 with D). This holds at all 140 cycle states.
- **Exits.**
  - In the two RP² classes and at C30#0, the only DL-leaving moves from cycle states are {α,μ}-swaps (in the 320-class, also 2 {μ,A}-swaps).
  - With exactly two {α,μ}-components, the link-free one is σ up to renaming. That is why "am:-" and "am:012" exits come in pairs: each pair is one exit.
  - On the sphere graphs, {α,A}, {α,B}, {A,B}, {μ,A} and {μ,B} exits also occur.
- **Exit targets.**
  - σ-exits land on lockless states (N, with in′ = 11 by D) or single-lock states.
  - No exit lands on a filled state directly. The next Lemma-A move (`mA`/`mB`) gives a filled state.
  - Max dS / dF: 2/3 on the sphere and on the 320-class, 3/4 on the 72-class (two σ-silent stretches of 4 states).
- **No fixed phase.**
  - States t and t + 10 of a 20-cycle always have the same j, since j advances by 3 per step.
  - The σ-exit set has period 10 in four test beds (the 72- and 320-classes, C30#0, p31.r13). It does not in p30.r10#1252 (an extra exit at t = 0) or in p31.r1#7302 (exits at t = 2–6, 10, 14, 18).
  - Where it is periodic, the phase differs from hole to hole. So there is no "σ exits at a fixed phase of the 10-step period"; that holds only at holes with a rigid local structure, such as the (5,5,5,5,6) results of `QuarterPeriodJ`.
- **P3 forces nothing by itself.** The odd parity of K_{αμ}(x_{j+2}) holds at every cycle state. It also holds at every state of the general-graph counterexample `lp_general_min.txt` (§4), whose class is closed.
- **C30#0.** σ exits at exactly the 10 states with |K_{αμ}(x_{j+2})| = 3. There K_{αμ} is the link triple {x_j, x_{j+1}, x_{j+2}}, σ is the triple swap of `QuarterSigmaExit`, and both locks die.
  - At the other 10 states, |K_{αμ}| = 6 and the σ-image stays DL.
  - The counts (#{α,μ}, #{A,B}) alternate (2,2) / (2,1), and σ exits at the (2,1) states.
- **Cycle statistics** (`th_cycstats.py`, `out/cycstats.jsonl`; 486 all-DL cycles: 18 sphere, 322 off-sphere violator-free, 146 off-sphere with violators).
  - Every cycle has a σ-exit.
  - The longest σ-silent stretch is 4 states (sphere) and 5 (off-sphere).
  - σ is trivial (a pure renaming) at 21% of sphere cycle states and 5% of off-sphere ones. It never exits there.
  - Exit counts by (#{α,μ}, #{A,B}) on the sphere (exits / non-exits):

    | (#{α,μ}, #{A,B}) | exits / non-exits |
    |---|---|
    | (1, ·) | 0 / 77 |
    | (2,1) | 50 / 2 |
    | (3,1) | 60 / 2 |
    | (4,1) | 14 / 0 |
    | (2,2) | 15 / 46 |
    | (2,3) | 9 / 19 |

    Off the sphere the same monotone pattern holds: (2,1) 2526 / 362, (2,2) 1325 / 2635.

  - So σ-exits are driven by {α,μ} splitting while {A,B} stays connected.

## 2. Lemmas [hand, unreviewed; each checked against the data]

Notation as in `TrackF/LockParity.md`: link (α, μ, α, A, B) at x_j…x_{j+4}, and a = α-vertices, m = μ-vertices; L1, L2, inA, inB.

The three partitions of the colours into two pairs are:
- P1 = {αμ | AB};
- P2 = {αA | μB};
- P3 = {αB | μA}.

**Lemma H0 (D is automatic on π-cycles; any graph).** If s is unfilled, π(s) is defined and s = π(t) for an unfilled t, then s satisfies D2 and D1. In particular every state of an all-DL π-cycle satisfies D1 and D2.

*Proof.*
- π(s) is defined only if inA(s) fails. So ¬inA, and at a DL state L2 = 1 = ¬inA (D2).
- Write t with frame j₀ and roles (α, μ, A, B). Then s = π(t) has frame j = j₀ + 3 and roles (α, B, μ, A).
- In s, x_j = x_{j₀+3} and x_{j+2} = x_{j₀}. The {α_s, B_s}-graph of s is the {α, A}-graph (same vertex set as in t, since π swaps within that pair). The swapped component K_{αA}^t(x_{j₀+2}) is still a component, and it contains x_{j₀+3}.
- So K^s_{α_s B_s}(x_j) = K_{αA}^t(x_{j₀+2}), which does not contain x_{j₀} = x_{j+2}, because π(t) is defined.
- Hence ¬inB(s), and L1 = 1 = ¬inB (D1). ∎

*Data:* in=00 at all 140 test-bed cycle states and at all cycle states of both counterexamples. This is §5.2 of LockParity.md read backwards: violators are path ends, and a cycle has none.

**Lemma H1 (when σ keeps a lock; any graph).** Let c be DL, K = K_{αμ}(x_{j+2}) (which contains x_j, x_{j+1}, x_{j+2}) and σ = swap K. The roles of σ(c) are (μ, α, A, B) at the same j. Then:
- Lock1(σc) ⇔ x_{j+1} and x_{j+3} are joined in G[(m∩K) ∪ (a∖K) ∪ A];
- Lock2(σc) ⇔ x_{j+1} and x_{j+4} are joined in G[(m∩K) ∪ (a∖K) ∪ B].

In particular:
- if some {μ,A}-lock chain of c from x_{j+1} to x_{j+3} has all its μ-vertices in K, then σ(c) keeps Lock1 (likewise Lock2);
- if K contains every α/μ vertex (the {α,μ}-graph is connected), then σ(c) equals c up to renaming, and σ cannot exit.

So **a σ-exit needs a second {α,μ}-component through which every chain of the dying lock passes.**

*Proof.* In σc the vertices coloured α are (a∖K) ∪ (m∩K), A is unchanged, and x_{j+1} has colour α. The locks of σc are reachability in these graphs. ∎

*With D at σc:*
- σ(c) is lockless ⇔ inA(σc) and inB(σc);
- that is, x_j and x_{j+2} are joined both in G[(a∩K) ∪ (m∖K) ∪ A] and in G[(a∩K) ∪ (m∖K) ∪ B].

So these joins must use μ-vertices of other {α,μ}-components. In the test beds every lockless σ-image has in′ = 11 (`out/sigma_*.txt`).

**Lemma H3 (edge balance / Euler identity per partition; any closed triangulated surface).** Let T be a closed triangulated surface with Euler characteristic χ, h a degree-5 vertex, and c any proper colouring of T − h. For a partition P_k, let E_k be the number of edges of T − h whose ends get colours from the same pair of P_k; let c_k and β_k be the number of components and the cycle rank of the two pair graphs of P_k together.

Then, at an unfilled state (labelling as above):

  E₁ = E₂ + 1 = E₃ + 1, and c₁ − β₁ = χ, c₂ − β₂ = c₃ − β₃ = χ + 1.

*Proof.*
- A face of T − h has three distinct colours p, q, r. Its three edges lie in the three different partitions ({pq|rs}, {pr|qs}, {qr|ps}).
- Inner edges of T − h lie in 2 faces of T − h, and the 5 link edges in 1. The unfilled link has partition counts ℓ = (3, 1, 1).
- So f − 5 = 2E_k − ℓ_k with f = 2(n − χ), which gives E_k = n − χ − (3 − ℓ_k)/2 − 1.
- For a graph, c − β = |V| − |E|. Hence c_k − β_k = (n − 1) − E_k = χ + (3 − ℓ_k)/2. ∎

*Data:* 0 failures on all 2,776 unfilled states of the four test-bed holes (`th_rigid.py`). This is a global consequence of purely local face data, the same kind of fact as Theorem P.

**Lemma H4 (rigid states).** Every DL state satisfying D has component counts at least (#αμ, #AB, #αA, #μB, #αB, #μA) ≥ (1, 1, 2, 1, 2, 1). Call it *rigid* when equality holds. Rigid ⇒ DL: #μB = 1 forces Lock2, and #μA = 1 forces Lock1.
- On a closed triangulated surface, H3 shows that rigid ⇔ β₁ = β₂ = β₃ = 2 − χ.
- On the sphere, rigid ⇔ all six pair graphs are forests (trees, given the counts).
  - Equivalently, in the dual Tait colouring (cubic, plus the 5-valent hole vertex v) every bicoloured subgraph is connected, and the pairings at v are the DL ones.
  - Precisely: the {2,3} edges form one Hamiltonian cycle through v, and {1,2} and {1,3} are figure-eights through v.
  - This uses the region ↔ component correspondence.

**Lemma H5 (rigid classes are bare π-cycles; any graph).** At a rigid state with D, every Kempe move gives either a renaming of c, or π(c), or π⁻¹(c).
- The {α,μ}, {A,B}, {μ,A} and {μ,B} graphs are connected, so swapping them is a renaming.
- {α,A} has exactly the two components K_{αA}(x_{j+2}) and K_{αA}(x_j). Swapping either gives π(c) up to renaming.
- {α,B} likewise gives π̃(c), the mirror move of LockParity §5.2. It satisfies π̃ ∘ π = id, so π̃(c) = π⁻¹(c) whenever c is a π-image.

Hence the Kempe graph of a class all of whose states are rigid has degree ≤ 2 and consists of π-steps. Since π is injective and the class is finite, the class is a single all-DL π-cycle, with no filled state and no violator. *Data:* Kempe degree 2 at every state of both counterexamples (§4).

## 3. Why σ exits on surfaces and not in general [data + H1, H3]

- σ can exit only where {α,μ} is disconnected (H1).
- In both general-graph counterexamples, {α,μ} and {A,B} are connected at every state. σ is then a renaming at all 10 states, and so are all other partition-1 swaps.
- On surfaces, H3 ties partition-1 connectivity to cycle rank: c₁ = χ + β₁. On the sphere, a state with both {α,μ} and {A,B} connected has both of them trees.
- Along the test-bed cycles, states with {α,μ} connected occur:
  - at most 4 in a row on the sphere, at most 1 in a row off the sphere;
  - never all the way round a cycle (`out/cycstats.jsonl`).
- Where {α,μ} has ≥ 2 components and {A,B} is connected, σ exits in 128/132 sphere cycle states and 3,263/3,737 off-sphere ones.
- I could not turn this into a proof. The sphere fact needed is about how π carries partition-1 connectivity from state to state (π rotates the partitions: P1 of π(s) is P3 of s). That is a global planar statement, not a hole statement.

## 4. The counterexamples to "local LPC" [verified]

Search (`th_gsearch*.py`): annealing over **arbitrary graphs** with a hole h adjacent to an induced 5-cycle (no surface). Moves are edge toggles; scores come from kclass4 at h. Seeds are the test beds, with h relabelled to 0. 2 workers, nice'd.

| mode / target | evaluations | result |
|---|---|---|
| free, CF (min filled in a cycle class) | 30k | **CF fails**: 674 events of a cycle class with F = 0. Smallest: 12 states = one 10-cycle + 2 path ends (violators) |
| free, LPC (F = 0 and no π-path ends) | 93k | **LPC fails for D**: 1,784 events. Smallest: a class of exactly 10 states = one all-DL 10-cycle. D holds everywhere (Lemma H0); lock parity / P fail at some states |
| free, LPC + lock parity (F = 0, no path ends, no LP violation) | 80k | **LPC fails for D and LP**: 15 events. `lp_general_min.txt` |
| tri (every edge of G − h in ≥ 1 triangle), CF | 85k | no F = 0; min F = 8 (class [34, 8, 22, 4, …], one 20-cycle) |
| ball (the triangulated 2-ball of h frozen from the seed surface: all edges at link vertices and between neighbours of a link vertex; everything else free), LPC + LP | 216k + 66k | **CF fails** (F = 0, P1–P3 hold at all 11 states) but **always with exactly 1 violator**: an 11-state class = 10-cycle + one isolated DL state violating D1 and D2. No violator-free cycle class reached |

**`lp_general_min.txt` (g51_11_1772_min):** n = 28, 109 edges, link degrees 9,6,8,4,5. It is not planar; its edge density is that of a genus-5 triangulation.
- G − h has 11 colourings up to renaming (264 absolute). One Kempe class has 10 states (240 absolute).
- All 10 states are DL with D1, D2, P1, P2, P3 and lock parity. There is no filled state.
- The class is one π-cycle of length 10. Every state has Kempe degree 2 and component counts (1,1,2,1,2,1), i.e. rigid. σ is trivial throughout.

It was checked by:
1. kclass4;
2. `th_verify.py` (th_engine);
3. `th_bruteverify.py` (absolute colourings, separate code): `class(absolute)=240 = 10 x 24 filled=0 failures={'D1': 0, 'D2': 0, 'P1': 0, 'P2': 0, 'P3': 0, 'notDL': 0}`.

The edge balance of H3 fails (|E(G − h)| = 104 ≢ 1 mod 3; imbalance 78 over the class). Two attempts to restore it did not succeed:
- annealing with the balance added to the score (`th_gsearch_bal.py`, 60k evaluations, of which 183 reached the counterexample tier) brought the class imbalance down only to 36;
- class-preserving edits (`th_balance.py`) left it at 58. These edits add neutral edges and remove edges that are not bridges at any class state, and so provably keep the class, D and the locks; but they are too few.

Whether a counterexample can also satisfy the per-state edge balance is **open**. If one exists, it would show that the counting consequences of triangulation (P and H3) are not enough either.

**Non-rigid counterexamples also exist** in general graphs. The violator-free, filled-free classes found by the D-only search include:
- 20-state classes (one 20-cycle, Kempe degree 2–3);
- 40-state classes (two 20-cycles, Kempe degree 3–6);
- 80-state classes (four 20-cycles).

Example `lpc_general_40.txt` (g31_22_1392; brute-force verified: 40 × 24 absolute states, filled 0, D everywhere, P fails).
- At 8 of its 40 states σ is *not* a renaming: {α,μ} has 2 components and {A,B} is connected.
- Even so, σ maps each of them to a DL state on the other cycle.
- So the sphere tendency "#{α,μ} ≥ 2 with #{A,B} = 1 ⇒ σ exits" (128/132) is not a graph-theoretic fact either.

**`lpc_general_min.txt` (g31_22_1205_min):** n = 21, 61 edges (greedily minimal for the property). It has the same structure (10-state rigid π-cycle class, D everywhere), but P fails (P1 at 6 of 10 states).

**Reading.**
- Every fact that LockParity.md, `QuarterLockParity`, `QuarterLemmaP`, `NoFrozen`, `QuarterPi` and `QuarterNonDLImage` state at the hole is a statement about one state and the components through the link. Those facts hold at every state of these classes.
- So LPC is **not** a consequence of them, and a proof must use the rest of the triangulation.
- What fails in the counterexamples, and holds on every triangulated surface, is the global face structure: the edge balance of H3 and the region ↔ component correspondence. On the sphere, rigid isolation (§6) is what fails.
- The "ball" runs suggest that even the triangulated 2-ball of h makes a violator-free cycle class hard to reach: 282k evaluations, always one violator left. This is weak evidence (a local search), not a lemma.

## 5. Surfaces of higher genus (does the counterexample shape appear once β can be large?) [data]

`th_hgsearch.py` uses genuine simplicial surfaces:
- the test-bed surfaces are connected-summed with 1–5 copies of the 9-vertex torus `torus(3,3)`, far from h (χ from −1 to −9);
- flip walks follow (min degree 3, the star of h kept), with the same LPC + LP score.

Runs:
- test-bed seeds with 1–5 handles: 11 walks, about 18k evaluations, χ from −1 to −7. Slow, because many evaluations hit the 5–15 s state-count timeout.
- C30#0 with 1–4 handles: 200 walks, 296k evaluations, χ = 0, −2, −4, −6. All logged graphs were re-validated as simplicial surfaces.

No class with F = 0 was found on any surface. The C30#0 lifts never went below F = 40 (the original class). The minimum F/N over violator-free cycle classes at χ = −1 was 0.364 (64/176), slightly below Track F's 3/8 and still above 1/4. As in Track F's glue runs, the classes stay close to products of the seed class with the handles.

## 6. Rigid isolation: a sphere-only fact that excludes the counterexample shape [data conjecture]

**Conjecture RI.** On a triangulated sphere, if c is a rigid DL state at a degree-5 hole, π(c) is not rigid. By Lemma H5, RI implies that no Kempe class consists only of rigid states (rigid LPC).

| data | rigid DL states | π(c) rigid |
|---|---|---|
| 24-vertex min-degree-5 sphere triangulations (`plantri24.txt`, every 60th graph, all 1,866 degree-5 holes) | 2,751 (2.8% of DL states) | **0** (1,947 → single-lock, 804 → DL non-rigid) |
| fullerene duals C20–C46 (every 8th, 480 holes) | 1,523 (6.2%) | **0** |
| Census29 cycle graphs p30/p31 (every degree-5 hole of the 13 test-bed sphere graphs) | 1,382 | **0** (1,065 → single-lock, 317 → DL non-rigid) |
| planar chord model, all instances with N ≤ 15 cubic vertices (exhaustive; includes all sphere rigid states of triangulations with ≤ 12 vertices, plus multigraph duals) | 17,059 | **0** (π(c) is Tait-rigid but not DL in 13,719 of them: it loses Lock 2; DL but not rigid in 600) |
| off-sphere cycle graphs (`cycstat_items.txt`, every degree-5 hole: RP² 2,981, Klein 527, torus 171) | RP² 2,573, Klein 613, torus 194 | **RP²: 36** (15 graphs, runs of length 2; D holds at both ends in all 10 pairs checked), Klein 0, torus 0 |
| general graphs (§4) | all states | rigid π-cycles of length 10 |

The chord model (`th_chord.py`) works in the dual.
- It applies to states whose partition-1 graphs are trees, i.e. whose {2,3} edges form one cycle H through v. H is drawn as a circle v, u₁, …, u_N, with colours 2, 3, … alternating; colour 1 is a pair of non-crossing chord matchings, one inside and one outside. The rotation at v is e0, e1, e2, e3, e4, with e3 inside and e0, e1 outside.
- DL ⇔ the {1,2} pairing at v is (e0e3)(e1e2) and the {1,3} pairing is (e1e3)(e0e4). Rigid ⇔ {1,2} and {1,3} are connected.
- π swaps colours 1 and 3 along the {1,3} trail through e1 and e3.
- In these terms, RI says: after the swap, the {2,3}′ trails do not pair (e1e4)(e2e3) while all three bicoloured subgraphs stay connected.

Why it matters:
- The counterexamples of §4 are exactly rigid cycles.
- On RP², rigid → rigid steps exist even with D at both ends (checked for 10 of the 36). So RI is a genuinely spherical statement. It is not implied by D at the two states, nor by the surface counting of H3.

**Validation of the chord model.**
- `th_chordcheck.py` rebuilds the primal near-triangulation from each model instance and recomputes everything with th_engine. The quantities compared are:
  - the vertex colouring, obtained by Z₂² integration of the Tait colours;
  - DL, rigid, and DL / rigid of π(c).
- All 628 model DL instances with a simple primal (N ≤ 11) were checked, 481 of them rigid with their images: **0 mismatches**. The other model instances have multi-edges in the primal; they are kept, since the model is a superset of the sphere.
- Extended to N = 15: 14,270 further rigid DL instances, 0 rigid images. The model total is 17,059 rigid DL instances, all with non-rigid images.

**Falsification search on spheres** (`th_risearch.py`, `out/risearch.jsonl`).
- Flip walks over simplicial spheres starting from 24-vertex triangulations: 40 walks × 150 flips. The score is the minimum over rigid DL states c of the component-count excess of π(c) over the rigid vector (10 is added if π(c) is not DL).
- 1,582 graphs reached excess 1 (typically π(c) DL with counts (2,1,2,1,2,1)). **None reached 0.**

**Caution about small N.**
- The model also suggested a stronger statement, TP: "if c and π(c) are both DL, they cannot both have both partition-1 graphs connected". TP holds for every model instance with N ≤ 11.
- But TP is **false** on real spheres: 382 such DL→DL steps among 7,616 in 40 plantri24 graphs (`th_treeprop.py`).
- So exhaustive small-N evidence can mislead. The real-triangulation counts (22,053 rigid states) are the better evidence for RI, together with the falsification search below.

**A clean reformulation for an attack [hand, unreviewed].**
- In a rigid DL state, H contains every colour-2 and colour-3 edge. The {1,3} subgraph is the figure-eight X ∪ Y, with X through e1, e3 and Y through e0, e4.
- After π (the swap on X), the two new bicoloured subgraphs that contain colour 2 are symmetric differences with H:
  - {1,2}′ = H Δ Y: H with Y's colour-3 edges replaced by Y's chords;
  - {2,3}′ = H Δ X.
- So RI reads: for a plane Hamiltonian cycle H through v with chords such that {1,2} = H₂ ∪ chords and {1,3} = H₃ ∪ chords are figure-eights with the DL pairings, it is impossible that
  - H Δ Y is a single cycle, and
  - H Δ X is connected and pairs (e1e4)(e2e3) at v.
- Two facts may help:
  - the {1,2}-loop through e1, e2 and the {1,3}-loop Y through e4, e0 each bound a disc that contains no cubic vertex (each loop lies on one side of the other loop of its figure-eight);
  - in the chord model, when π(c) is DL, the obstruction is always one extra closed cycle in H Δ Y (data, N ≤ 11).

Status: I did not find a proof. The obvious tools do not suffice: a Jordan-curve separation fails because the {2,3}′ paths can run along the swapped chords of the trail. RI is offered as the cleanest next target. It is a finite, checkable statement about Hamiltonian-cycle-plus-chords diagrams; the exhaustive check now reaches N = 15.

## 7. Pseudo-surfaces (attempted, inconclusive)

- `th_psearch.py` and `th_pinch.py`: surfaces with pinch points, where (F1)–(F3) and Theorem P hold.
- Pinching destroyed every π-cycle in the seeds. Only 7 pinch candidates preserved the cycle colourings. The surviving cycle classes all had filled states:
  - [144,56,…] and [100,44,…] on RP² pinches;
  - [1064,438,…] and [754,344,…] on sphere pinches.
- Not pursued further.

## 8. Runs and files

| file | content |
|---|---|
| `th_engine.py` | independent state / Kempe-move / π / σ engine |
| `th_dump.py`, `th_sigma.py`, `th_cycstats.py` | dumps of cycle states, σ anatomy, per-cycle statistics |
| `th_gsearch.py`, `th_gsearch_lpc.py`, `th_gsearch_lp.py`, `th_gsearch_bal.py` | general-graph searches (CF; LPC with D; LPC with D + LP; plus H3 edge balance); modes free / tri / ball |
| `th_minimize.py`, `th_verify.py`, `th_bruteverify.py` | shrinking and three-way verification of counterexamples |
| `th_hgsearch.py` | higher-genus surface search |
| `th_rigid.py`, `th_rigidscan.py`, `th_rigidscan_lib.py`, `th_rigidrun.py`, `th_rigidnext.py`, `th_risearch.py` | Euler identity check, rigid-state census, π-successors of rigid states, falsification search for RI on spheres |
| `th_balance.py` | class-preserving edits towards the H3 edge balance (inconclusive, §4) |
| `th_chord.py`, `th_chordcheck.py`, `th_treeprop.py` | exhaustive planar chord model for rigid isolation; its validation against th_engine; the (false) stronger statement TP |
| `th_psearch.py`, `th_pinch.py` | pseudo-surface attempts |
| `extract_testbeds.py`, `testbeds.txt`, `testbeds.jsonl`, `seeds_all.txt`, `seeds_lpcex.txt`, `cycstat_items.txt` | inputs |
| `lp_general_min.txt`, `lp_general_cex.txt`, `lpc_general_min.txt`, `lpc_general_cex.txt`, `lpc_general_40.txt`, `cex_free.txt`, `cf_ball_cex.txt` | the counterexample graphs ('name n adj;…', hole 0, link = adj[0] in cyclic order) |
| `out/` | dumps, search logs (`g*.jsonl.gz` gzipped, `hg*.jsonl`, `risearch.jsonl`; `out/old/` = the first general-graph runs scored by F/N), statistics (`cycstats.jsonl`, `rigid*.jsonl`, `chord*.txt`) |
