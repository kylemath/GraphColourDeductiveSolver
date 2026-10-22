# Spin conservation on windows: the disc Stokes law and what it does (not) explain

Scripts are in this folder and use python-sat, scipy and networkx.
- `spinlib.py` holds the shared code: parsing, the rotation system, spins, fan turns, triangle signs and the ring flux.
- `q1_verify.py` and `q1_extra.py` check the formula numerically (Q1).
- `q2_budget.py` and `q2_aggregate.py` run the spin-budget test against direct extension (Q2). Per-window rows are in `q2_results_<group>.tsv`.
- `q3_vortex.py` computes the vortex statistics (Q3). Output is in `q3_summary.json`.

Labels used below:
- **[P]** proved, with the proof given here.
- **[M]** measured, with the sample stated.
- **[C]** conjecture.

## 0. Setup and the embedding

Colours are in Z2^2 = {0,1,2,3}. An edge uv gets the label c(u)^c(v). A step a -> b is *forward* iff b == a%3+1, as in `vortex_spin.py`.

**Embedding.** A window is a ring cycle 0..r-1 plus interior vertices with the given adjacencies. Add an apex joined to every ring vertex. This gives a triangulated sphere, which is 3-connected, so its embedding is unique. We read the rotations off `networkx.check_planarity`.
- An interior vertex's rotation is its cyclic link.
- A ring vertex's rotation, cut at the apex, is its **fan**. The fan runs from one ring neighbour, through its interior neighbours, to the other ring neighbour. It has k_v = (#interior neighbours)+1 steps.
- The ring is traversed in the direction "v -> first vertex of v's fan". This is the orientation the link orientation induces.

We tested 3,000 random dataset windows (out of 97,174), and all 3,000 embed as triangulated discs: every consecutive rotation pair is adjacent and #triangles = r+2m-2 [M].

Notation:
- **Spin.** w(v) = (f-b)/3 around the link of an interior vertex v.
- **Fan turn.** t(v) = f-b along the fan of a ring vertex v. This is an integer, not divided by 3.
- **Triangle sign.** ε(T) = +1 if the triangle's label cycle runs forward, -1 otherwise. The sign is the same whichever corner you read it from [P]: the labels x, y, x^y appear at the three corners as x->y, y->x^y and x^y->x, so all three steps are forward or all three are backward.
- **E** = Σ_T ε(T). Each triangle with colour set F = {a,b,c} is one signed covering of the face F of the tetrahedron, so E is the signed area of the colour map.
- **Ring flux.** δ(c->d) = #{ring steps v_i -> v_{i+1} with colours c -> d} − #{steps d -> c}.
- **Orientation factor.** σ(c->d; a) = +1 if (c^a) == (c^d)%3+1, and −1 otherwise.
- **Per-colour totals.** S_a = Σ{ w(v) : v interior, c(v)=a } and X_a = S_a + (1/3)·Σ{ t(v) : v on the ring, c(v)=a }.

## 1. The disc conservation law (Q1)

**Theorem [P].** Let D be a near-triangulated disc with a proper 4-colouring. Then:

1. Σ_a X_a = E.
2. For a ≠ b, with {c,d} the other two colours: **3(X_a − X_b) = σ(c->d; a) · δ(c->d)**. Swapping c and d changes neither side.
3. Combining 1 and 2:

  **S_a + (1/3)·Σ{ t(v) : ring v of colour a } = E/4 + Ψ_a(ring word),  where Ψ_a = (1/12)·Σ_{b≠a} σ(c_ab->d_ab; a)·δ(c_ab->d_ab).**

   Σ_a Ψ_a = 0.
4. A finer per-face form also holds. Let N(F) = Σ{ε(T) : T has colour set F}. Then N(F_acd) − N(F_bcd) = σ(c->d; a)·δ(c->d), and N(F) = S_a + Σ{n_v(F) : ring v of colour a} for each a in F. Here n_v(F) is the net number of times the fan of v crosses the label edge of F.

So **the ring word fixes every difference of per-colour spin totals, up to the fan turns of the ring vertices of that colour. Only one integer is left free: E, the "wrapping number" of the interior.** On the sphere there is no ring, so X_a = E/4 for every a. This is Fisk's statement with K = E/4.

**Proof.**

*(a) Lifting lemma.* The link of an interior vertex v of colour a is a closed walk on the 3-cycle of labels {1,2,3}. Its net displacement is 3w(v). Lift the walk to Z. Each label edge {i,j} lifts to one integer edge in every period of 3, so a closed walk with displacement 3w crosses each label edge net w times. Each step of the link is one triangle at v, with sign equal to the step direction. Hence n_v(F) = w(v) for each of the three faces F that contain a. For a ring vertex, the fan is an open walk with displacement t(v). Its three net edge-crossings add up to t(v).

*(b) Counting.* A triangle with colour set F has exactly one vertex of each colour in F. So for a in F, N(F) = Σ_{v of colour a} n_v(F) = S_a + Σ_{ring v of colour a} n_v(F). Sum this over the three faces F that contain a:

  Σ_{F∋a} N(F) = 3S_a + Σ_{ring, a} t(v) = 3X_a.

Summing over a counts each face three times, so Σ_a X_a = Σ_F N(F) = E. This proves 1.

*(c) Boundary.* Fix the colour pair {c,d}. Each triangle of colour set {c,d,a} or {c,d,b} has exactly one {c,d}-edge. So

  N(F_acd) − N(F_bcd) = Σ over {c,d}-edges e of Σ over triangles T at e of ε(T)·χ(T),

where χ(T) = +1 if T's third colour is a and −1 if it is b. Now consider an interior edge uv and its two triangles.
- If both third vertices have the same colour, the corner labels at u are ℓ->m and m->ℓ. The two signs are opposite and the two χ are equal, so the edge contributes 0.
- If the third colours differ, the labels are ℓ->m1 and m2->ℓ with {ℓ,m1,m2} = {1,2,3}. These steps are both forward or both backward. The two signs are equal and the two χ are opposite, so the edge again contributes 0.

So only ring edges contribute. Take a ring edge u->v with colours c->d. Its single triangle contributes ε·χ = σ(c->d; a), whichever of a or b is the third colour. The ring edges with colours d->c contribute −σ(c->d; a). This proves the per-face law. From (b), 3(X_a − X_b) = Σ_{F∋a} N(F) − Σ_{F∋b} N(F) = N(F_acd) − N(F_bcd), which proves 2. ∎

**The fan turns are almost determined by the ring word [P].** For a ring vertex v, the constraints are |t(v)| ≤ k_v, t(v) ≡ k_v (mod 2), and t(v) ≡ ℓ_last − ℓ_first (mod 3), where ℓ_first = c(v)^c(succ) and ℓ_last = c(v)^c(pred) are ring labels.
- For k_v ≤ 2 (at most one interior neighbour), t(v) is **unique**. For example, k_v = 2 gives t = 0, −2 or +2 according as the end label minus the start label is 0, 1 or 2 mod 3.
- For k_v = 3, t(v) is unique unless the two end labels are equal, in which case t(v) = ±3.

In windows, most ring vertices have k_v ≤ 3. So the boundary term is, in practice, a function of the ring colour word, up to a few ±1 ambiguities in τ_a and the free integer E.

**Numerical checks [M].** The identity was checked exactly, as 12S_a + 4Σt = 3E + 12Ψ_a for every a:
- 1,980 colourings of 198 random spherical-cap discs, with 200–1,500 vertices on the sphere and random caps. There were 0 failures. The opposite sign convention fails on every trial colouring.
- 6,000 colourings of 3,000 random dataset windows. There were 0 failures.
- The pairwise form 2 and the per-face form were checked on 2,160 pairs. There were 0 mismatches.

E really is free. With the ring colouring fixed and the interior resampled, E took more than one value in 195 of 198 discs.

## 2. Spin budget as an extension test (Q2)

**The test.** The interior colouring is unknown. The theorem gives these necessary conditions:
- The colour classes of the interior vertices are unknown.
- w(v) is taken from the values allowed for deg v: |3w| ≤ d and w ≡ d (mod 2). So deg 5 and deg 7 give ±1, deg 6 gives {0, ±2}, and deg 8 gives {0, ±2}.
- t(v) is taken from the allowed set above.
- E has |E| ≤ #triangles and E ≡ #triangles (mod 2).
- The four equations 12S_a + 4Σ_{ring a} t − 3E = 12Ψ_a must hold.

We solve this as an exact integer feasibility problem (scipy `milp`). Without some colour constraint the problem is vacuous, so we use two relaxations:
- **A**: each interior vertex avoids the colours of its ring neighbours.
- **A_odd**: A, plus a proper colouring on the edges between two odd-degree vertices (vortex–vortex edges).

For each relaxation there is a matching *spin-free baseline*, which is the same colour constraints without the equations:
- **blocked**: some interior vertex sees all four colours on the ring.
- **odd-colouring infeasible**: the A_odd colour constraints alone have no solution.

The fair comparison is against **AC**, the elementary local propagation. AC removes the ring colours from each interior domain, then repeatedly deletes a singleton's colour from its interior neighbours. It refutes the class if some domain becomes empty.

Soundness checks [M]: see the note under the table. In short, all of the spin test's bite is parity.

**Sample.** Groups by kc label:
- a7 = windows around a degree-7 receiver; these are the "face-7" binder windows.
- D = two-engine D-reducible.
- notD = kc D false, ring 10–15.

Each window has 120 uniformly random canonical ring colourings. "Bad" means the class does not extend directly (SAT).

| group | windows | classes sampled | extend | bad | bad refuted by AC | killed by spin A | killed by spin A_odd | A beyond "blocked" | A_odd beyond odd-colouring | bad classes surviving AC | of those, killed by A_odd | of those, killed by A_odd and not by odd-colouring |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a7_D | 12 | 1438 | 195 | 1243 | 1220 (98.1%) | 279 (22.4%) | 553 (44.5%) | 0 (0.0%) | 135 (10.9%) | 23 | 0 | 0 |
| a7_notD | 12 | 1437 | 113 | 1324 | 1321 (99.8%) | 985 (74.4%) | 1161 (87.7%) | 60 (4.5%) | 156 (11.8%) | 3 | 0 | 0 |
| a9_D | 12 | 1440 | 214 | 1226 | 1159 (94.5%) | 307 (25.0%) | 611 (49.8%) | 0 (0.0%) | 188 (15.3%) | 67 | 10 | 6 |
| a9_notD | 12 | 1439 | 93 | 1346 | 1341 (99.6%) | 786 (58.4%) | 1111 (82.5%) | 70 (5.2%) | 238 (17.7%) | 5 | 3 | 2 |

The last three columns come from `q2_survivors.py`, which reruns the same sample. Soundness [M]: every extending class we tested passes every variant (236/236). The per-face version kills nothing beyond A (0/238). The parity-only version kills exactly the classes the bounded version kills (85/85).

**Answers [M].**
- **Almost every non-extending class fails for a trivial local reason.** AC refutes 93–99.9% of the bad classes in every group.
- **The spin budget adds very little.** Compared with its spin-free baselines, the spin equations kill another 0–5% of bad classes under A and 11–18% under A_odd. **Almost all of those are already refuted by AC.** Mechanically, the parity of S_a forces where the vortices go. That is an indirect way of detecting two adjacent interior vertices that are each forced to the same colour.
- **Only 98 of 5,139 bad classes survive AC**, and these are the ones that matter for Kempe arguments. The spin budget kills 13 of them. Only **8 of the 98 (8%) are killed by spin and not by its spin-free baseline**. All 8 are in a9 windows, whose degree-9 centre allows spin ±1 or ±3; 6 are in D windows and 2 in notD windows. In a7 windows, spin kills 0 of 26. These 8 are the only genuine spin obstructions we found. Examples, as kc-canonical ring words: a9_u656.56665_.....5555 with 01010232103132, and a9_-7556...56_75......5 with 010212131010101.
- So **the spin view does not explain non-extension.** About 92% of the classes that survive local propagation are invisible to it, as are 100% of those in face-7 windows.
- **The spin view does not separate D from non-D.** The raw spin-kill rate is higher in notD windows, but only because those windows are smaller, so their interior vertices touch the ring more and are more often blocked. After the local baseline is factored out, there is no difference. The visible difference between the groups is that the larger D windows keep more AC-surviving bad classes (a9_D: 67 of 1,226; a7_D: 23 of 1,243; against 3 and 5 in the notD groups). Those are the classes Kempe swaps rescue.
- **The ring charge Ψ correlates only weakly with extension.** Classes with Ψ = 0 (no net flux) extend somewhat more often: 17% vs 13% in a7_D, 12% vs 6.6% in a7_notD; 2,994 and 2,996 classes. The mean flux |δ|_1 is 4.6 for bad classes and 4.0 for good ones.

**Why this is unsurprising [P/C].** For any extension, the identity has exactly one free integer, E. All other freedom sits in which vortices get which colour. With m ≥ 3 vortices and one free sign per vortex, any non-local balance condition is almost always satisfiable. [C] For face-7 windows with ring ≤ 15, the spin budget is implied by local consistency; we saw no exceptions in 2,567 bad classes. Higher-degree centres allow rare exceptions: 8 of 2,572 bad a9 classes.

## 3. What binder windows look like in spin terms (Q3)

**Vortices.** The odd-degree interior vertices are the forced vortices, each with spin ±1. In the face-7 windows these are the central 7 and every 5. Mean vortex counts per window over the whole dataset [M]:

| group | a7 D | a7 C | a7 notD | a9 D | a9 notD |
|---|---|---|---|---|---|
| windows | 155 | 199 | 35,723 | 1,632 | 14,619 |
| mean # vortices | 6.8 | 6.4 | 4.1 | 7.8 | 4.4 |

The difference mostly tracks window size: reducible windows are the larger ones. Degree-6 and degree-8 vertices can carry spin 0 or ±2. About half of all windows, in every group, have an odd number of vortices.

**Can the vortices be balanced inside the window?**

- **[P] Parity obstruction.** S_a ≡ (number of vortices of colour a) mod 2. Hence Σ_a S_a ≡ #vortices mod 2. If the count is odd, the four per-colour totals cannot all be equal, so some per-colour spin must leave through the ring. It shows up as ring flux δ and fan turns. This applies to about half of all windows.
- **[M] Balance is rare even when the count is even.** We sampled extensions of 20 a7_D and 20 a7_notD windows (1,209 and 639 extensions). All four S_a were equal in only 5.0% (a7_D) and 2.5% (a7_notD). The typical spread max S − min S is 1–2, with a maximum of 5. **Inside a binder window the vortex spins are essentially never balanced colour by colour. The imbalance is carried out through the ring**, as the theorem says it must be: X_a − X_b = σδ/3.
- **Kempe swaps [P].** Swapping colours a and b on a Kempe chain XORs the colours of the chain's vertices by x = a^b. For a vertex in the chain, its label to a chain neighbour stays x, and the other two labels y and x^y are exchanged. That is a transposition of {1,2,3}, so **every vertex in the chain changes its spin to −w and moves from class a to class b.** Neighbours of the chain that are outside it can change spin as well: this happened in 301 of 953 cases [M].
  - A swap on an interior-only chain leaves the ring word unchanged. So it leaves Ψ and every difference X_a − X_b unchanged; it only reshuffles which vortices carry which signs and classes.
  - A swap on a chain that reaches the ring changes the ring word, and with it the flux δ that the boundary must carry. In spin language, **a Kempe chain is the conduit that carries per-colour spin out through the ring**. This is the "carried out" option. The data in §2 say this is not what makes a ring colouring non-extend directly, though.

**Plain-language picture.** A face-7 binder window has about 4–7 forced vortices of charge ±1: the 7 and the 5s around it. Often there is an odd number, and then perfect per-colour neutrality is impossible. Even when it is possible, it almost never happens. So every colouring of the window pushes a net per-colour spin across the ring, and how much is read directly off the ring word. That bookkeeping is exact, but it is not what makes a ring colouring fail. Failures are overwhelmingly local: two interior vertices next to the ring are forced to the same colour. **[C]** Whether a binder window is reducible is decided by the Kempe-chain connectivity (kc's non-crossing partitions), not by a spin budget. A spin-based invariant would have to track how chains carry spin between ring runs, not just per-colour totals.
