# R0 attempt 1 (Long Table, 13 Oct 2026, 13:25–14:40)

Exploratory. Labels:
- **[proved, hand]**: argument written here, not independently reviewed.
- **[data]**: computation here. SAT answers are Glucose 4 / CaDiCaL verdicts from pysat; no DRAT proofs were kept.
- **[conjecture]**.

Scope:
- Scripts and logs are in `proof/r0a1/`; this note is `proof/R0-ATTEMPT-1.md`.
- Nothing outside these two paths was changed. `axioms/invariants/` and `axioms/r0surfaces/` were not touched.
- All code here is new and independent of `sat_t1v.py`; only the C30#0 seed file (TrackU) is read.
- Compute: `nice -n 10`, at most 3 processes, every run at most 10 min, on AC power (`pmset`: charged).

## 0. Verdict

1. **No proof of R0 in general.** But **R0 is proved for every odd L (L = 5, 15, 25, …)** by Lemma E (§3), a new parity law [proved, hand]. In a plane graph the total Tait sign S changes by 4 mod 8 at every step of D, so every closed R0 walk, Hamiltonian or not, has L ≡ 0 (mod 10).
   - In Fisk-degree form: S = 4·deg − 1 [data], and **the Fisk degree changes parity at every step**. This is the coordinator's colouring-invariant lead (§6, item 5).
   - Caveat: NRC orbits have even L anyway (the 1212 word), so Lemma E settles only the odd-L part of R0, not new NRC cases. It is probably the chain-parity law / "dκ odd" of the invariants agent in another form; this has not been checked.
   - Further results: an exact reformulation for all L at once (§1), exhaustive census data (§2), and the lemmas of §3.

2. **Reformulation [proved, hand].** Let D be the digraph on the perfect matchings of G with an arc M → M′ iff
   - M ∩ M′ = ∅, and
   - k(M′) ≡ k(M) − 2 (mod 5).

   Closed R0 sequences of any length are exactly the closed walks of D. So **R0 ⟺ no Hamiltonian arc (M ∪ M′ a Hamiltonian cycle) lies in a strongly connected component of D.**

3. **Exhaustive census, all L [data].**
   - The generator lists every planar Hamiltonian normal form (§2). At **n = 8, 10, …, 20 (all 426,320 chord diagrams at n = 18 and all 3,800,955 at n = 20)**, D is **acyclic** for *every* simple plane G that has a Hamiltonian arc.
   - So in this range there is no closed R0 walk of any length, and not even a closed walk avoiding the Hamiltonian arc.
   - Without planarity the same normal forms give violations at once: 1 of 28 classes at n = 8 and 12 of 327 at n = 10. Exactly the classes whose D has a cycle put a Hamiltonian arc inside it.

4. **Strong form, Conjecture R0\* [conjecture].** If a simple plane G (v of degree 5, all other vertices cubic) has a Hamiltonian cycle through two **non-adjacent** v-edges, then D is acyclic.
   - R0\* ⇒ R0 ⇒ NRC (simple Tait graph).
   - Evidence beyond the census: SAT on "planar G with the Hamiltonian arc, plus a closed walk *anywhere* in D" is UNSAT for:
     - L = 10, n ≤ 22;
     - L = 20, n ≤ 20;
     - L = 5, n = 20 and 24 (n ≤ 20 is covered by the census, and every n by Lemma E).
   - Open runs: L = 10 at n = 24 and n = 26 hit TIMEOUT (550 s each).
   - Other collections (`star_files.py`, `out/star_files*.txt`):
     - all distinct graphs in the TrackU seed / annealing / random / collection files were scanned: 222 graphs;
     - only 8 are planar with their rotation, and all 8 are C30#0 relabellings (n = 26, 125 perfect matchings);
     - all 8 have a cyclic D and **no** Hamiltonian arc.
     - So no R0\* counterexample was found, but this is thin independent evidence: C30#0 is the only known planar graph whose D has a cycle.
   - **Non-adjacency is necessary.** The planar C30#0 graph (n = 26) is Hamiltonian *only* through **adjacent** v-edge pairs (4 cycles for each of the pairs (0,1), (1,2), (2,3), (3,4), (0,4); 0 for the non-adjacent pairs). Its D has a 20-cycle (the known orbit) and no Hamiltonian arc at all.
   - SAT for "Hamiltonian through adjacent v-edges + closed walk" is UNSAT for L = 10, 20 at n ≤ 22 and for L = 5 at n ≤ 18. The positive control finds C30#0's 20-cycle (§2.3). So cyclic D needs size, and needs the absence of a 2|3 Hamiltonian split.

5. **Answers to the three leads.**
   - **(A) small cases.** The failure anatomy at n = 8, 10 is uniform:
     - every D is acyclic, and every maximal walk through a Hamiltonian arc has at most 3 arcs (n = 8) or 5 arcs (n = 10);
     - every walk dies at a *type-B* matching (§3, Lemma T), which is the planar "wrong pairing" at v. No walk ever dies at a crossed pairing.
     - The UNSAT cores are one-sided depth bounds (§5).
   - **(B) identity.** Found:
     - S = Σ_w σ_t(w), with S ≡ 3 (mod 4) conserved (Lemma K) and, more sharply, **S_{t+1} ≡ S_t + 4 (mod 8)** at every step [proved, Lemma E]. This is a genuine per-step law: it forces L ≡ 0 (mod 10).
     - S = 4·deg_Fisk − 1 [data].
     - Σ_w ρ(w) = L on C30#0 [data].

     Nothing found obstructs L ≡ 0 (mod 10). C30#0 closes at L = 20, so any state function is consistent there, and the Hamiltonian pair must enter. No monotone quantity was found. Linear edge-weight potentials do exist graph by graph, but shared-feature potentials are infeasible already at n = 10.
   - **(C) lollipop.** D is not of max degree 2: out-degrees 2 and 4 occur, with branching on extra even cycles of Q_t. Hamiltonian arcs are not forced to be path endpoints: at n = 16 a walk can have up to 6 arcs before a Hamiltonian arc and up to 6 after it (7 arcs in total at most). So no Thomason-style argument applies directly. What the data shows is stronger and global: D is acyclic.

6. **L = 5 is proved (Lemma E), and also has an explicit model (Lemma L5).**
   - A closed 5-walk of D is encoded exactly by a Lipschitz map τ: V(G) − v → C₅ with rigid edge rules and a +2 vortex at v. In normal form this becomes the chord-diagram **Level Model**: UNSAT for n ≤ 30 [data], non-planar SAT at n = 8.
   - Lemma E proves it for all n, because L = 5 is odd.
   - The level model shows exactly which planar ingredients the parity law uses: non-crossing on *both* sides and the o/e parity rule of the levels. Dropping any one of them gives SAT.

7. **Coordinator item (invariants agent, chord order) [data].**
   - "e1 before e0 along H at every Hamiltonian state", with *no other* planarity, does **not** imply R0. It is UNSAT for n ≤ 12 at L = 10 and at n = 10, 12 for L = 5.
   - It is SAT at n = 14, 16 for L = 10 and L = 5. The solutions are non-planar and satisfy the order at every Hamiltonian state they contain.
   - Positive control: planar windows satisfy the order at all their Hamiltonian states.
   - Details in §6.

## 1. Reformulation [proved, hand]

Notation: G is simple, v = 0 has degree 5 with f_0..f_4 in ccw rotation, all other vertices are cubic. PM(G) is the set of perfect matchings; k(M) is the index of M's v-edge.

### 1.1 The digraph D

- An R0 sequence (closed) is M_0, …, M_{L−1} with M_t ∩ M_{t+1} = ∅ and k(M_{t+1}) = k(M_t) − 2. That is exactly a closed walk in D, and L ≡ 0 (mod 5) automatically.
- A closed walk through the arc (M_0, M_1) exists iff M_0 is reachable from M_1, iff the arc lies in an SCC.
- Hence **R0 for G and a given Hamiltonian arc, for all L simultaneously** is the statement that this arc is not inside an SCC of D.
- Mirror and time reversal: the mirror of G reverses the rotation, so advance −2 becomes +2, which is D reversed. D and its reverse have the same SCCs.

### 1.2 Arcs as 2-factors

- An arc M → M′ is a 2-factor F = M ∪ M′ through v via f_k, f_{k−2} (non-adjacent v-edges).
- All of F's cycles are even and M-alternating, and M′ = F − M.
- Fixing F, every alternation choice on the cycles of F not through v gives an arc. This is where branching comes from.

## 2. Generator, counts, census

### 2.1 Generator (`r0lib.py`)

- **Hamiltonian normal form:** H = 0, 1, …, n−1, 0, with v = 0, f_0 = (0, n−1) and f_2 = (0, 1). The chords are f_1, f_3, f_4 from v to distinct vertices in 2..n−2, plus a perfect matching of the remaining vertices with no chord parallel to H.
- **Planarity** uses the circle rule of PROOF-ATTEMPT-1 §1.3:
  - the chord crossing graph is 2-colourable;
  - side(f_1) ≠ side(f_3) = side(f_4);
  - v-ends are placed at n + .25 (f_4), n + .5 (f_1), n + .75 (f_3).
- **Every** pair (simple plane G, Hamiltonian cycle through two non-adjacent v-edges) appears, relabelled. Graphs without such a cycle make R0 vacuous and are not generated.
- **Checks.**
  - Every generated graph passes an independent networkx planarity test with the rotation (5-wheel gadget, `G5.planar_rot`).
  - The fast incremental generator (`planar_normal_forms`) and the filter version (`normal_form_graphs`) give identical diagram counts at n = 8, 10, 12.
- **Classes** are isomorphism classes of (G, rotation at v up to dihedral symmetry): Weisfeiler–Lehman hash plus nx isomorphism on the gadget graph.

### 2.2 Census results [data]

`census2.py` (classes) and `census3.py` (all diagrams, no isomorphism reduction, chunked):

| n | planar diagrams | classes | classes with cyclic D | Hamiltonian arc in an SCC (R0 violation) | max #PM |
|---|---|---|---|---|---|
| 8 | 7 | 3 | 0 | 0 | 7 |
| 10 | 72 | 20 | 0 | 0 | 12 |
| 12 | 643 | 159 | 0 | 0 | |
| 14 | 5,578 | 1,227 | 0 | 0 | 30 |
| 16 | 48,488 | 9,794 | 0 | 0 | 48 |
| 18 | 426,320 (253,478 + 172,842) | (not reduced) | 0 | 0 | 78 |
| 20 | 3,800,955 (12 chunks, each ≤ 565 s; `out/census20{b..g}.txt`) | (not reduced) | 0 | 0 | 126 |

Non-planar control:
- The same normal forms that are *not* planar with the rotation give 28 classes at n = 8 (1 with a cycle in D, and that one has a Hamiltonian arc in it) and 327 classes at n = 10 (12 with a cycle, all 12 with a Hamiltonian arc inside an SCC).
- The non-planar SAT version is SAT at every n tested (n = 8–14 at L = 5, 10).

### 2.3 SAT (`r0sat.py`, an independent encoder; `run_star.sh`, `run_adj.sh`)

| mode | meaning | L = 5 | L = 10 | L = 20 |
|---|---|---|---|---|
| r0 | Conjecture R0 (sequence through the Hamiltonian arc) | UNSAT n = 8–14 (non-planar: SAT) | UNSAT n = 8–12 (non-planar: SAT) | |
| star | planar G having the Hamiltonian arc, closed walk anywhere (R0\*) | UNSAT n = 20 (9 s), 24 (546 s); n ≤ 20 by census; all n by Lemma E | UNSAT n ≤ 22 (n = 22: 120 s); n = 24 TIMEOUT 550 s | UNSAT n = 16, 18, 20 |
| adj | planar G Hamiltonian through adjacent f_0, f_1, closed walk anywhere | UNSAT n = 10, 14, 18 | UNSAT n = 8–22 | UNSAT n = 16–22; n = 24 TIMEOUT 400 s |

**Positive control (`poscontrol.py`).** C30#0 put into the adj normal form, chords fixed:
- L = 20 is **SAT**, decoded and verified: perfect matchings, disjointness, frames 2 0 3 1 4…, planar_rot True.
- L = 10 is UNSAT.

So the encoder with planarity clauses does find genuine planar closed walks.

### 2.4 C30#0 (`c30.py`, `hamcheck.py`, `c30_anat.py`) [data]

- #PM = 125, 60 arcs, 0 Hamiltonian arcs, one cyclic SCC of size 20 (the orbit).
- Hamiltonian cycles through v-edge pairs: 4 for each adjacent pair, 0 for each non-adjacent pair.
- Along the orbit every out-degree is 1, so all its states are DL with Q_t connected.
- Each edge is used 4 or 8 times out of 20:
  - the 8-edges form a 2-factor of G − v;
  - the 4-edges are the v-star plus a perfect matching.

## 3. Lemmas

### Lemma E (parity law: closed walks have L ≡ 0 mod 10) [proved, hand]

Setup:
- G is a plane graph with v of degree 5 and all other vertices cubic.
- For an arc (M_t, M_{t+1}) of D, put R_t = E − M_t − M_{t+1}.
- σ_t(w) = +1 iff the colours (M_t, M_{t+1}, R_t) at the cubic vertex w are in ccw order, and S_t = Σ_{w≠v} σ_t(w).

**Claim.** For every step (M_t, M_{t+1}) → (M_{t+1}, M_{t+2}) of D:

  **S_{t+1} ≡ S_t + 4 (mod 8).**

Hence every closed walk in D has even length. Since frames force L ≡ 0 (mod 5), we get **L ≡ 0 (mod 10)**, and **R0 (indeed: no closed walk at all) holds for every odd L.**

*Proof.*
1. **Setup of the step.** Let k = k(M_t). Then E − M_{t+1} is a figure-eight X ∪ Y at v plus cycles that avoid v (Lemma T):
   - Y is the even (M_t, R_t)-loop through f_k and f_{k+1};
   - X is the odd loop through f_{k−1} and f_{k+2}; it is v –R– w_1 –M_t– w_2 –R– … –M_t– w_{2r} –R– v;
   - every other component is an (M_t, R_t)-cycle Z;
   - M_{t+2} = M_t Δ Y Δ (some of the Z's).

   As in Lemma K, σ_{t+1} = σ_t on Y and on the swapped Z's, and σ_{t+1} = −σ_t on X − v and on the unswapped Z's. So S_{t+1} − S_t = −2 Σ_{off} σ_t, where "off" is X − v together with the unswapped Z's. It suffices to show that Σ_Z σ_t ≡ 0 and Σ_{X−v} σ_t ≡ 2 (mod 4).

2. **Signs in terms of turns.** Traverse a bicoloured cycle. At each vertex the third edge (the M_{t+1}-edge) is on the left or on the right. The sign is σ = ±(left ? 1 : −1), with the ± alternating along the cycle, because the arriving colour alternates. Hence Σσ ≡ 2·#(third edges on one fixed side) (mod 4).

3. **A cycle Z avoiding v.** Let I be the vertices strictly inside Z on the side not containing v.
   - M_t is perfect on I, because Z's vertices have their M_t-edges on Z; so |I| is even.
   - M_{t+1} matches I to itself and to the inward third edges of Z, where chords of Z count twice.
   - So the number of inward third edges is even, hence Σ_Z σ ≡ 0 (mod 4).

4. **The odd loop X.** Let Ω₁ be the side of X containing f_{k−2}, the M_{t+1}-edge of v. Its other v-edges f_k, f_{k+1} lie on the other side. Let I₁ be its interior vertices.
   - M_t is perfect on I₁: the X-vertices have their M_t-edges on X, and f_k is not in Ω₁. So |I₁| is even.
   - M_{t+1} matches I₁ to itself, to the third edges of X − v pointing into Ω₁, and to v by f_{k−2} if its far end u lies in I₁.
   - So #(third edges into Ω₁) ≡ [u ∈ I₁] + [u ∈ X − v] = 1 (mod 2). Here u is the far end of f_{k−2}; if u ∈ X − v, its third edge is f_{k−2}, which points into Ω₁.
   - Hence Σ_{X−v} σ ≡ 2 (mod 4). ∎

**Data.**
- ΔS ≡ 4 (mod 8) on all 4,928 steps of the planar census at n = 8–14 (`step_mod8.py`).
- Both intermediate claims hold on every arc with a successor at n = 10, 12, 14 (`lemmaE_parts.py`):
  - Σσ ≡ 0 (mod 4) on all 1,112 v-free cycles;
  - Σσ ≡ 2 (mod 4) on all 3,776 odd loops X − v.
- On C30#0, ΔS = −12, 12, −20, 20.
- The law must fail off the plane, and it does: non-planar closed 5-walks exist (n = 8).

**Fisk form [data].**
- On every arc of the planar census at n = 8–14 (8,346 arcs) and on C30#0, the Fisk degree vector of the face 4-colouring (edges M_t → 1, M_{t+1} → 2, R_t → 3, lifted to faces with the link normalised as (α, 0, γ, 0, β)) is (deg_0, deg_1, deg_2, deg_3) = (D, D, D, D − 1).
- Also S = 4D − 1. [hand: the face sign equals σ for every missing colour m, so Σ_m deg_m = S.]
- So **Lemma E says the Fisk degree changes by an odd amount at every step.** This also explains why S ≡ 3 (mod 4) in Lemma K.

### Lemma T (type lemma; exits) [proved, hand]

Let M have v-edge f_k. E − M has degree 4 at v, so its v-component is a figure-eight; denote the pairing of its four v-edges f_{k+1..k+4} into two loops. There are three cases:
- **type A:** {f_{k+2}, f_{k+3}}{f_{k+1}, f_{k+4}} (the DL pairing);
- **type B:** {f_{k+1}, f_{k+2}}{f_{k+3}, f_{k+4}};
- **crossed:** {f_{k+1}, f_{k+3}}{f_{k+2}, f_{k+4}}, which is impossible on the sphere because two closed curves meeting once at v cannot cross there.

**Claim.** If M has an in-arc, then M has an out-arc iff M is type A, and the same with in and out exchanged. Hence:
- every interior state of a walk in D is type A;
- every walk dies exactly at a type-B (or crossed) matching.

*Proof.*
- An in-arc P → M has k(P) = k + 2, and P is a perfect matching of E − M. So the loop through f_{k+2} is even (in edges), the other loop is odd, and all other cycles of E − M are even.
- A successor needs a perfect matching of E − M containing f_{k+3} = f_{k−2}. That needs f_{k+3} on the even loop, i.e. paired with f_{k+2}, and then all parities are already right.
- The reverse direction is symmetric. ∎

Further facts:
- **Successors.** The successors of P → M are exactly M′ = P Δ Y Δ S, where Y is the loop {f_{k+2}, f_{k+3}} and S is any union of the other (P, R)-cycles of E − M.
- So the "DL pairing" is not an extra assumption in R0: it is *forced* at every interior state. R0 differs from NRC-M only by allowing extra even cycles in Q_t (branching).
- This matches the invariants agent's exit mechanism (item 3): A5v runs exit at the crossed pairing; sphere runs exit at type B or by disconnection.
- [data] Checked on every matching with an in-arc in the census: n = 8–16, 66,300 matchings, 0 disagreements (`depth.py`).

### Lemma K (Kempe parity: S mod 4 is conserved) [proved, hand]

Setup:
- σ_t(w) = +1 iff the colouring (M_t, M_{t+1}, R_t) is ccw at the cubic vertex w.
- S_t = Σ_{w≠v} σ_t(w).

Claim: along any arc of D, S_{t+1} ≡ S_t (mod 4).

*Proof.*
- From step t to t+1 the roles are permuted cyclically on the swapped (M_t, R_t)-cycles Y ∪ S, which keeps σ. Elsewhere they are permuted by a transposition, which negates σ. This is R5 of PROOF-ATTEMPT-1.
- The negated vertices are the vertices of the odd loop X (minus v) and of the unswapped even cycles. Each of these sets has an even number of vertices, so Σσ over them is even and S changes by a multiple of 4. ∎

Data:
- S ≡ 3 (mod 4) on every arc of every planar census class, n = 8, 10, 12 (`sigsum.py`).
- On C30#0, S runs 11, −1, 11, −9 (period 4).
- The plain cubic analogue Σσ ≡ 0 (mod 4) holds for every Tait colouring of K4, the prism, the cube, the pentagonal prism and the dodecahedron (`cubic_sig.py`).

Because S is conserved, it **cannot** obstruct closure. It is recorded to close this avenue.

### Lemma L5 (the L = 5 vortex) [proved, hand]

Let M_0, …, M_4 be a closed 5-walk of D. For each edge e let T(e) = {t : e ∈ M_t} ⊆ ℤ/5. T(e) is independent in the 5-cycle, and at each cubic vertex the three sets partition ℤ/5.
- (a) At a cubic w the partition is necessarily {s}, {s+1, s+3}, {s+2, s+4} for a unique s =: τ(w). The edges carrying these are called S, D, U.
- (b) An edge with T = {s} joins two vertices of type s. An edge with T = {a, a+2} joins types in {a−2, a−1}. So **τ is 1-Lipschitz into C₅**, and the edge rules are rigid:
  - an edge between types s and s+1 is U at the s-end and D at the (s+1)-end;
  - an edge between equal types is S–S, D–D or U–U.
- (c) The far end of f_i has type T(f_i). With k_t = 2 − 2t, the far ends of f_0, …, f_4 have types 1, 3, 0, 2, 4: **+2 per rotation step at v**.
- (d) At a Hamiltonian arc (M_0, M_1), along H from the far end of f_2 to the far end of f_0 the types run (lifted) from 0 to −4. Equivalently, the levels ℓ = −τ run ivb = 0, ii = 1, i = 2, iii = 3, iva = 4. Moreover:
  - the v-chords f_4, f_1, f_3 land at levels 1, 2, 3;
  - in the true rotation the outside chords f_3, f_4 need pos(f_3) < pos(f_4), so the level path along H is forced into the shape 0 ↗ 3 ↘ 1 ↗ 4;
  - the number of 0–4 chords is odd.

*Proof.*
- (a): the only partitions of ℤ/5 into an independent singleton and two independent pairs.
- (b): direct from (a).
- (c): T(f_i) is the time of f_i's visit.
- (d): parity of the cut δ(level ≥ 3.5): |δ| ≡ 3|U| is odd, while f_0 plus the odd number of H-crossings is even. ∎

Data:
- [data] The non-planar L = 5 solutions read back as such level paths with one 0–4 chord (`l5_types.py`).
- [data] Planar L = 5 is UNSAT at n = 8–16 even with the v-rotation constraint dropped or replaced by any lone-chord placement (`l5_probe.py`); "star" L = 5 is UNSAT to n = 24.
- The τ-degree count (§4.4) and the mod-3 Heawood face congruences are consistent with the vortex. The contradiction comes instead from the mod-8 sign law of **Lemma E**, which uses the Jordan curve theorem on the bicoloured loops. L = 5 is odd, so **R0 at L = 5 is proved**.

**The level model (equivalent to R0 at L = 5, normal form) [proved, hand: (a)–(d) and the word check of §3; data: SAT below].** Let n be even, put v = 0, 1, …, n−1 on a circle (H), and ask for levels ℓ: {1..n−1} → {0,…,4} and chords such that:
1. ℓ(1) = 0 and ℓ(n−1) = 4.
2. For odd i (o-edge (i, i+1) ∈ M_1): {ℓ(i), ℓ(i+1)} ⊆ {0,1}, ⊆ {2,3}, or = {4}. For even i (e-edge ∈ M_0): = {0}, ⊆ {1,2}, or ⊆ {3,4}.
3. Every vertex 1..n−1 is the end of exactly one chord, and chords join non-adjacent vertices.
   - The chords f_1, f_3, f_4 from v end at levels 2, 3, 1 respectively, never at 1 or n−1.
   - Every other chord joins two vertices of equal level in {1, 2, 3}, or two vertices with levels in {0, 4}.
4. The chords are drawn without crossings on the two sides of H: f_1 alone on one side, f_3 and f_4 on the other, with v's chord ends in the order (n−1), f_4, f_1, f_3, (1).

The levels are the vertex words: ivb = eococ, ii = eoeoc, i = eoeco, iii = eoceo, iva = eocec (letters: M_0 H-edge e, M_1 H-edge o, chord c). Conditions 2–3 are exactly the edge consistency of these words. So the level model has a solution iff R0 at L = 5 does.

`l5_levels.py` [data]:
- With condition 4: **UNSAT for n = 8, 10, …, 30** (n = 28: 25 s; n = 30: `out/l5_levels30.txt`). This is R0 at L = 5 for n ≤ 30, which goes past the r0sat range.
- Without condition 4: SAT at every n.
- With either page allowed to cross (`crossI` / `crossO`): SAT from n = 14 / n = 10.
- With the levels of all three v-chord ends freed: still UNSAT at n ≤ 20 (parity forces one end at each of the levels 1, 2, 3).
- With condition 2 weakened to |Δℓ| ≤ 1: SAT from n = 14 (planar). **So the o/e parity rule of condition 2 is essential**: through-runs have odd length, bounce-runs even length, and the 0- and 4-runs pair along e- and o-edges.

The Level Lemma (no solution with conditions 1–4) is a self-contained statement about non-crossing chord diagrams. **It follows from Lemma E.** A direct chord-diagram proof is still missing; the item below records how far the mod-2 bookkeeping goes.

**Lemma P (interval parities in the level model) [proved, hand].**
- Condition 2 says exactly: |Δℓ| ≤ 1 along H, and a change between levels j and j+1 happens on an o-edge if j is even and on an e-edge if j is odd.
- Put π(x) = ℓ(x) + x mod 2. An up-step joins two vertices with π = 1, a down-step joins two vertices with π = 0, and π alternates inside a run.
- It follows that for an interval [a, b] with end levels λ_a, λ_b, the number of level-j vertices in [a, b] is, mod 2:
  - 1 if j lies strictly between λ_a and λ_b;
  - 0 if j lies outside [min λ, max λ];
  - 1 + a + b if j = λ_a = λ_b;
  - λ_a + a + [λ_b < λ_a] if j = λ_a ≠ λ_b, and symmetrically λ_b + b + [λ_a > λ_b] if j = λ_b ≠ λ_a.
- *Proof:* split the interval into level-j segments separated by excursions above or below j. A segment has odd length iff the excursions on its two sides lie on opposite sides; sum these. ∎
- Consequence: for an equal-level chord (a, b) at level λ, its interior holds an even number of vertices of every other level, so the chords leaving the interior to the other side carry even class counts except at level λ.
- **Checked: the coarse mod-2 bookkeeping with the regions cut by f_1 (inside) and f_3, f_4 (outside) is consistent.** For every class c, #c(A) ≡ #c(B) holds automatically. So a direct proof needs the nesting of further chords; Lemma E's proof does that through the bicoloured loops.

### Lemma D (depth anatomy) [data, `depth.py`]

| n | longest path in any D (arcs) | longest path through a Hamiltonian arc | back-depth histogram (into M_0) | fwd-depth histogram (from M_1) |
|---|---|---|---|---|
| 8 | 3 | 3 | {0: 4, 1: 2, 2: 1} | {0: 4, 1: 2, 2: 1} |
| 10 | 5 | 5 | {0: 27, 1: 12, 2: 9, 3: 1, 4: 1} | {0: 30, 1: 12, 2: 6, 3: 1, 4: 1} |
| 12 | 5 | 5 | max 4 | max 4 |
| 14 | 6 | 6 | max 5 | max 5 |
| 16 | 7 | 7 | max 6 | max 6 |

- The "longest path through a Hamiltonian arc" column agrees with PROOF-ATTEMPT-1's open R0 windows (6, 6, 7, 8 matchings at n = 10, 12, 14, 16), from independent code.
- Out-degree of matchings with an in-arc at n = 16: {0: 31,818, 1: 21,228, 2: 5,970, 4: 303}.

## 4. Per-graph failure anatomy (n = 8, 10) [data, `anatomy.py`, `show_small.py`]

### 4.1 Format

- Each row gives: the cubic chords; the far ends of f_1, f_3, f_4; #PM; #arcs of D; #Hamiltonian arcs; the longest walk through a Hamiltonian arc in arcs; and that walk's v-frame word, with `|` marking the Hamiltonian arc.
- **In all 23 classes D is acyclic, and both ends of the longest walk are type-B matchings** (Lemma T): the planar wrong pairing, never the crossed one.

### 4.2 n = 8 (3 classes)

| # | chords; f1,f3,f4 → | #PM | arcs | Ham arcs | longest | word |
|---|---|---|---|---|---|---|
| 0 | (1,3),(5,7); 2,4,6 | 4 | 3 | 3 | 3 | 1\|420 |
| 1 | (1,3),(4,7); 2,5,6 | 6 | 2 | 2 | 1 | 2\|0 |
| 2 | (1,4),(3,7); 2,5,6 | 7 | 4 | 2 | 2 | 03\|1 |

Class 0, in full (`show_small.py 8`):
- D is the path M3 (k = 1) → M1 (4) → M2 (2) → M0 (0), and all three arcs are Hamiltonian.
- M0 = {1-2, 3-4, 5-6, f_0} is a sink: in E − M0 the loop through f_2 returns by f_1 (type B), so no matching with v-edge f_3 exists.
- M3 is a source for the mirror reason.
- A closed walk would need 5 frames; D has 4 matchings in total.

### 4.3 n = 10 (20 classes)

All 20 classes (`python3 anatomy.py 10`). In every row, both the source and the sink of the walk are type B.

| # | chords; f1,f3,f4 → | #PM | arcs | Ham arcs | longest | word |
|---|---|---|---|---|---|---|
| 0 | (1,3),(6,8),(7,9); 2,4,5 | 7 | 6 | 2 | 3 | 142\|0 |
| 1 | (1,3),(6,8),(7,9); 4,2,5 | 7 | 6 | 4 | 3 | 42\|03 |
| 2 | (1,3),(5,8),(7,9); 2,4,6 | 5 | 3 | 3 | 3 | 14\|20 |
| 3 | (1,3),(5,9),(6,8); 2,4,7 | 5 | 3 | 3 | 3 | 14\|20 |
| 4 | (1,3),(5,7),(6,9); 2,4,8 | 6 | 3 | 3 | 3 | 14\|20 |
| 5 | (1,3),(4,8),(7,9); 2,5,6 | 6 | 2 | 2 | 1 | 2\|0 |
| 6 | (1,4),(3,8),(7,9); 2,5,6 | 8 | 4 | 2 | 2 | 03\|1 |
| 7 | (1,3),(4,9),(6,8); 2,5,7 | 7 | 2 | 2 | 1 | 3\|1 |
| 8 | (1,4),(3,9),(6,8); 2,5,7 | 9 | 4 | 2 | 2 | 2\|03 |
| 9 | (1,3),(4,6),(7,9); 2,5,8 | 5 | 3 | 3 | 3 | 14\|20 |
| 10 | (1,4),(3,6),(7,9); 2,5,8 | 9 | 5 | 3 | 3 | 42\|03 |
| 11 | (1,4),(3,9),(5,8); 2,6,7 | 10 | 3 | 3 | 1 | 1\|4 |
| 12 | (1,5),(3,9),(4,8); 2,6,7 | 8 | 6 | 4 | 5 | 03142\|0 |
| 13 | (1,3),(4,6),(5,9); 2,7,8 | 7 | 2 | 2 | 1 | 3\|1 |
| 14 | (1,4),(3,5),(6,9); 2,7,8 | 8 | 2 | 2 | 1 | 3\|1 |
| 15 | (1,5),(3,9),(4,6); 2,7,8 | 8 | 4 | 2 | 2 | 03\|1 |
| 16 | (1,5),(2,4),(6,9); 3,7,8 | 8 | 2 | 2 | 1 | 3\|1 |
| 17 | (1,6),(2,4),(5,9); 3,7,8 | 8 | 4 | 2 | 2 | 03\|1 |
| 18 | (1,6),(2,5),(4,9); 3,7,8 | 12 | 8 | 2 | 3 | 203\|1 |
| 19 | (1,4),(6,8),(7,9); 5,2,3 | 10 | 4 | 2 | 1 | 2\|0 |

The longest walk through a Hamiltonian arc has length 1, 2, 3 or 5. In the single length-5 class (#12) the walk visits all five frames and is back at frame 0 after 5 arcs, but at a different matching: it ends at the head of the Hamiltonian arc (a type-B sink) and began at a source. Frames close; matchings do not.

### 4.4 What "why it fails" amounts to [proved + data]

- By Lemma T, a closed walk lives entirely on type-A matchings. At small n, type-A chains through a Hamiltonian arc are at most 5–7 arcs long, so they cannot complete the 5-frame cycle and come back.
- The UNSAT cores (§5) show exactly this: one direction of the walk, with depth bounded by n.
- Lemma E disposes of every odd L. For L ≡ 0 (mod 10) the τ-degree identity of Lemma L5 is consistent. For a Hamiltonian arc with all non-v faces of τ-degree 0, the five corner face-paths at v have forced lifted τ-changes (2, 2, −3, 2, −3), which sum to 0. So the degree count gives no contradiction.

## 5. UNSAT cores [data, `core.py`]

Method:
- Clause groups: graph, vrot, planar, ham (M_0, M_1 fixed), and pm_t / frame_t / disj_t for each t.
- Deletion-based group minimisation, with the frame / disjointness / pm groups tried first, in time order.

| n (L = 10) | minimal group core |
|---|---|
| 8 | graph, ham, planar, vrot + steps 7..9 and disj 8, 9 (wrap) |
| 10, 12 | graph, ham, planar + pm/frame 5..9 and disj 5..9 |
| 14 | graph, ham, planar + pm/frame 4..9 and disj 4..9 |

Reading:
- **No core uses the forward half.** The obstruction certificate is "there is no backward walk of length 3 (n = 8), 5 (n = 10, 12) or 6 (n = 14) ending in the Hamiltonian state M_0". This is the back-depth of Lemma D: at L = 10 (even, so Lemma E does not apply) the core is a depth bound, not a parity.
- `vrot` is needed only at n = 8. At n ≥ 10 the chord non-crossing clauses alone suffice, whatever the sides of the v-chords. The same holds for L = 5 at n ≤ 16 (`l5_probe.py`).

## 6. Coordinator / invariants-agent items

1. **Chirality (item 1).** Consistent.
   - Every potential tried here is non-chiral in the invariants agent's sense:
     - per-graph linear edge weights exist (`linpot.py`: feasible for all classes at n = 8–12 and 400/400 at n = 14), but they are just certificates of acyclicity;
     - shared-feature potentials (`featpot.py`, `featpot2.py`: counts of even/odd H-edges, inside/outside chords, chord spans, positions, one-hot k) are **infeasible** already at n = 10;
     - the chord count q(M) = |M ∖ H| is not monotone along walks (non-monotone in 4–22 % of maximal walks, `hdist.py`), though it never returns to 0 at n ≤ 14.
   - The one quantity that does work, S in Lemma E, is **chiral** (σ changes sign under mirroring), as the chirality lemma demands. But it is a mod-8 law, not a monotone.
   - A chiral candidate suggested by Lemma L5: the vortex sense +2 at v against the lifted τ-path along H, which is 0 → −4. It is untested as a potential.
2. **Chord order at Hamiltonian states (item 2) [data, `order_test.py`, `order_cegar.py`].**
   - In normal-form coordinates "e1 before e0" is pos(f_3 end) < pos(f_4 end): at the Hamiltonian state t = 1, e_2 = f_0, e_0 = f_3, e_1 = f_4. This is exactly the outside non-crossing of f_3, f_4.
   - **Only at the normal-form Hamiltonian state**, with no crossing clauses: UNSAT at n = 8, 10 (L = 10) and n = 10 (L = 5); **SAT from n = 12** (L = 10) and at n = 14 (L = 5). The T1 order (pos f_3 > pos f_4) is SAT at every n.
   - **At every Hamiltonian state of the sequence** (CEGAR: each violating state cut by its two matchings plus the e_0, e_1 chords): UNSAT at n = 8, 10, 12 (L = 10; 0, 0, 37 cuts) and n = 12 (L = 5, 18 cuts). **SAT at n = 14 and 16, for both L = 10 and L = 5**. The solutions are non-planar (planar_rot False) and satisfy the order at all their Hamiltonian states (e.g. n = 14, L = 10: Hamiltonian at t = 0, 5).
   - Positive control: planar open windows (n = 12, 16, 20, L = 6) satisfy the order at every Hamiltonian state, with 0 violations.
   - **Conclusion: the order constraint at Hamiltonian states is genuine planar input, but not sufficient for R0.** The R0 obstruction also uses non-crossing at non-Hamiltonian states.
3. **Exit mechanism (item 3).** Proved here as Lemma T.
   - In R0 the crossed pairing is also a dead end (no successor), so it cannot be "the" planar input either. In the planar census every dead end is type B.
4. **Items 4, 5 (curvature parity, Conjecture C)** were not addressed directly; they concern law-respecting orbits, not R0. However, Lemma E ("Fisk degree odd per step") looks like item 4's "dκ_α odd at every step" in another form. Worth checking whether the two coincide, which would give that law a short Jordan-curve proof.
5. **r0surfaces lead: Fisk degree / R0-lift (priority item) [data + hand, `fisk.py`, `step_mod8.py`].**
   - (a) **Computed.** Setup: face 4-colouring of T − x from (M_t, M_{t+1}, R_t) ↦ (1, 2, 3); Klein lift; link normalised to (α, 0, γ, 0, β) at the frame k; Fisk sign of each triangle (cubic vertex) against ∂[0,1,2,3].
     - On every arc of the planar census at n = 8–14 and along C30#0, the degree vector is (D, D, D, D − 1): the γ = R_t colour is the special one, through the boundary walk.
     - So **S = 4D − 1**.
     - The Fisk sign of a triangle equals the Tait sign σ for every missing colour [hand]. Hence Σ_m deg_m = S, and on closed cubic plane graphs S = 4·deg ≡ 0 (mod 4), as checked in `cubic_sig.py`.
   - (b) **Per-step identity.** The degree changes by an **odd** amount at every step (Lemma E, proved through S). In genuine-colouring normalisation (κ_t = (1 2)^t c_t) the degree is (−1)^t D_t; on C30#0 it runs 3, 0, 3, 2, 3, 0, 3, 2, …
     - This forces only **L even**. A fixed nonzero per-period drift is impossible without the Hamiltonian pair: C30#0 is a closed sequence of genuine, lifting sphere colourings, L = 20, with total drift 0.
     - Nor is the Hamiltonian state extremal: at Hamiltonian arcs D takes every value from −3 to 3 (n = 14: 16, 215, 745, 1,229, 996, 387, 57).
     - So the Fisk degree gives exactly the parity law. R0-lift has to keep condition (iii) on the sphere, and any further invariant must see the Hamiltonian pair.
   - (c) **Theorem W relation:** not tested.

## 7. Best partial proof

1. R0 (all L) ⟺ no Hamiltonian arc in an SCC of D [proved].
2. **Lemma E [proved]: in the plane, S_{t+1} ≡ S_t + 4 (mod 8) at every step.** So closed walks have L ≡ 0 (mod 10), and **R0 holds for all odd L, at every n**. In Fisk form, the degree changes parity at every step (S = 4·deg − 1 [data]).
3. Interior states of any R0 walk are type A (the DL pairing); walks end at type B or crossed [proved]. R0 is "DL-pairing chains with extra even cycles allowed".
4. L = 5 is encoded by a C₅-Lipschitz map with a vortex, equivalently a chord-diagram level model [proved]. Both are consistent with, and settled by, Lemma E.
5. Exhaustive [data]: D is acyclic for every planar Hamiltonian-arc graph with n ≤ 20 (all L). SAT runs reach n = 20–24 for L = 10, 20.

## 8. Exact remaining gap

1. **R0 for L ≡ 0 (mod 10)** is now the whole gap. This is also NRC's own range, since the 1212 word already forces L even. The required statement: a planar closed walk of D of length 10m cannot pass through a Hamiltonian arc.
   - Lemma E, Lemma K and every state function (Fisk degree, S, frame) are consistent with such closure: C30#0 closes at L = 20.
   - So the missing invariant must use the Hamiltonian arc, i.e. the 2|3 split of the link by a Jordan curve through all vertices. It must be non-conserved (a monotone or a one-sided bound), and chiral (invariants agent).
2. **R0\*** (a non-adjacent Hamiltonian cycle ⇒ D acyclic) fits all data so far (census n ≤ 20; SAT n ≤ 22 at L = 10).
   - Its failure for adjacent-only Hamiltonian graphs (C30#0) shows what a closed walk needs.
   - Finding more planar graphs with a cyclic D (only C30#0 is known) is the most useful next computation. For example, run SAT in adj mode at n = 26–30, L = 20, seeded from C30#0.
3. **L = 10 analogue of Lemma L5.** Vertex words are cyclic words of length 10 with no repeated letter, giving a finite type set. The Lipschitz structure on these types, combined with the Hamiltonian normal form, is the natural next model. Lemma E is its mod-8 shadow.
4. The chord-order constraint at Hamiltonian states is insufficient (§6, item 2). Any proof must also use non-crossing at non-Hamiltonian states, as Lemma E does through the bicoloured loops.

## 9. Files (`proof/r0a1/`)

| file | content |
|---|---|
| `r0lib.py` | graph class G5, perfect matchings, digraph D, SCC analysis, circle rule, normal-form generators (filter and fast incremental), isomorphism buckets |
| `census.py`, `census2.py`, `census3.py` | census by classes (n ≤ 16) and over all diagrams (chunked, n = 18, 20); outputs `out/census_n*_p.jsonl`, `out/census*.txt` |
| `r0sat.py` | independent SAT encoder: modes r0 / star / adj, planar or non-planar, closed or open, time limit, built-in verification |
| `run_star.sh`, `run_adj.sh`, `run_quick.sh` | the §2.3 runs → `out/star.txt`, `out/adj.txt`; every quick experiment re-run → `out/quick.txt` |
| `poscontrol.py` | C30#0 in adj normal form: L = 20 SAT (verified), L = 10 UNSAT |
| `c30.py`, `hamcheck.py`, `c30_anat.py`, `winding.py`, `sigsum.py` | C30#0: D, Hamiltonian pairs, orbit anatomy, windings (ρ ∈ {0, 2}, Σρ = 20 = L), S per step |
| `depth.py`, `anatomy.py`, `show_small.py`, `hdist.py` | Lemma D, §4 tables, D listings, chord-count profiles |
| `core.py` | §5 group cores |
| `linpot.py`, `featpot.py`, `featpot2.py` | potential searches (§6.1) |
| `cubic_sig.py`, `cubic_sig2.py` | Σσ mod 4 on plane cubic graphs |
| `step_mod8.py`, `lemmaE_parts.py`, `fisk.py`, `run_lemmaE.sh` | Lemma E checks (ΔS mod 8 on every step; the two intermediate claims); Fisk degree vectors along C30#0 and on census arcs; driver for these and the level-model variants → `out/lemmaE.txt` |
| `star_files.py` | R0\* scan of the TrackU graph collections (`out/star_files*.txt`) |
| `l5_probe.py`, `l5_types.py`, `l5_levels.py` | L = 5 probes, type reading, and the level model as its own SAT problem (`out/l5_levels30.txt`) |
| `order_test.py`, `order_cegar.py` | §6.2 |

Run logs are kept as `out/*.txt`, because the repository ignores `*.log`.

Not committed (regenerable): `out/census_n16_p.jsonl` (3.2 MB). Regenerate with `python3 census2.py 16` (110 s).

Reproduce:
- `python3 census2.py N` for N ≤ 16; `python3 census3.py 18 c 2` for c = 0, 1 (≈ 3 min each); `python3 census3.py 20 c 12` for c = 0..11 (2–10 min each). Chunk 1 of `20 c 6` equals chunks 1 and 7 of 12.
- `./run_quick.sh`, `./run_lemmaE.sh` re-run everything else quoted here.
- `python3 r0sat.py {r0|star|adj} N L [nonplanar] [open] [t=sec]`.
- `python3 poscontrol.py`; `python3 anatomy.py 10`; `python3 core.py 10 10`.
