# Lemma R\* at a (5,5,6,5,6) hole: the radius-5 certificate and the silent-starvation move

Math research worker, front 1, 6 October 2026. **Hand work only.** No code, script or build was run (battery restriction); files were only read. Labels: [hand] derived here by hand; [cert] read from the Studio certificate files; [open]; [memory] cited from memory, not rechecked. No other file was edited; nothing committed.

Sources: certificate `backgroundMaterial/planemap-structural/studiointel/run-C-2026-10-06/cert/91a307d1852a1764.{graph,hole22.state}.json`, `check.py` (read only, for the move definition), intern-B.md, intern-B-cycle2.md, intern-D-cycle2.md, MathTwoSixNeighbours.md (Γ₁, Γ₂), MathHighDegreeNeighbour.md (HP), pd2_lock_proof.md (Tait criterion), MathReviewCleanToVHE.md (L3), MathVacancyDRed/REFINEMENT.md.

## Verdict, first

1. **[hand] The 5-swap fill of the radius-5 state, written out (§1).** It is **B, B, B, then a silent {b,d}-swap that touches no link vertex, then a one-vertex fill**. The B-walk follows Math's deterministic cycle Γ₁ backwards: dgdbg@41 → gdbab@24 → dgdbg@02 → gdbab@30, i.e. M(O3) → L2 → N3 → M(L2). At M(L2) a silent swap starves the singleton x₄ (degree 5) of its only b-neighbour. So the certificate **leaves Γ₁ by a move that is outside the automaton** (F, B, AB and their starvation rules). It does **not** use AB, and AB* is false at all four states it visits.
2. **[hand] Lemma SS (silent starvation), degree-free (§2).** At a DL state, take a lock endpoint t and one of its two lock colours c. Suppose every c-neighbour of t lies in a Kempe component of a pair {c, c′} that contains no link vertex, where c′ is not the colour of t. Swapping those components (one swap each) gives a non-DL state. With one such neighbour the radius is ≤ 2.
3. **[hand] SS on Γ₁ (§3).** Each of the five gdbab states of Γ₁ has an SS move that is **not locally blocked** when the free vertices have degree exactly 6. The dgdbg states have only the AB\*-type move, which gives nothing new. So the adversary that keeps Γ₁ alive must pay **one extra ring-3 leak at every second step**. The certificate is a graph where this leak is missing at M(L2).
4. **[hand] Small structural lemmas (§4).** These are: the repeated colour is invariant along F/B; an F-cycle has length ≡ 0 (mod 5); Kempe classes are the same as dual Tait-switch classes; and a targetless class must contain only F-cycles.
5. **Killed (§5).** K1: AB\* as a provable lemma. K2: the 3-colourable (Mohar/Fisk) route. K3: "the F/B orbit alone realises the radius". K4: the local SS catalogue does not close the automaton in the independent-leak model.
6. **[open]** Finiteness for the class is **not proved**. The missing step is a planarity coupling between the SS leak at the gdbab states and the AB leak at the neighbouring dgdbg states (§6).
7. **Degree ≥ 6 (coordinator, mid-task).** Lemma SS and §4 use no degree beyond 5 at the starved vertex. §3's "not locally blocked" uses **degree exactly 6** at the free vertex: it needs a single forced m. For degree ≥ 7, SS remains a candidate, but it can be locally blocked by a b/g run along the m's (§3.3).

---

## 1. The certificate's 5-swap fill [hand, from the cert files]

### 1.1 The graph near hole 22

Neighbours in T − 22, read from the 52 faces:

| v | nbrs | v | nbrs |
|---|---|---|---|
| 0 | 1 2 3 4 5 6 | 14 | 3 4 11 13 21 |
| 1 | 0 5 6 7 8 18 | 15 | 5 8 13 17 19 20 21 27 |
| 2 | 0 3 6 9 10 | 16 | 7 17 18 24 27 |
| 3 | 0 2 4 9 11 12 14 | 17 | 15 16 19 24 27 |
| 4 | 0 3 5 13 14 | 18 | 1 6 7 10 16 24 |
| 5 | 0 1 4 8 13 15 | 19 | 10 15 17 20 23 24 26 |
| 6 | 0 1 2 10 18 | 20 | 15 19 21 23 25 |
| 7 | 1 8 16 18 27 | 21 | 13 14 15 20 |
| 8 | 1 5 7 15 27 | 23 | 12 19 20 25 26 |
| 9 | 2 3 10 12 26 | 24 | 10 16 17 18 19 |
| 10 | 2 6 9 18 19 24 26 | 25 | 11 12 20 23 |
| 11 | 3 12 14 25 | 26 | 9 10 12 19 23 |
| 12 | 3 9 11 23 25 26 | 27 | 7 8 15 16 17 |
| 13 | 4 5 14 15 21 | | |

Check: the degree sum is 146 = 2(78 − 5). The degree counts match the certificate: 17 vertices of degree 5, seven of degree 6, three of degree 7 and one of degree 8.

Link, in intern B's frame: x₀..x₄ = 21, 20, 25, 11, 14, with degrees 5, 6, 5, 5, 6. Certificate colours: a = 2, b = 0, g = 3, d = 1.

### 1.2 The state s and its moves

The colour classes of s (A = colour 2, B = 0, G = 3, D = 1):
- A = {4, 9, 18, 19, 21, 25, 27}
- B = {3, 5, 6, 7, 20, 24, 26}
- G = {0, 8, 10, 11, 13, 17, 23}
- D = {1, 2, 12, 14, 15, 16}

Properness was checked edge by edge.

Bichromatic components at s:
- {A,B}, {B,G}, {B,D} and {G,D} are each **connected**.
- {A,G} has two components: {0, 4, 13, 21} and the rest.
- {A,D} has two components: {2, 9, 12, 25} and the rest.

So, up to colour permutation, **s has exactly two neighbours**: F(s) and B(s). Both locks are carried by connected two-colour subgraphs, and AB is a global colour permutation. This is the leak, in its most extreme form.

### 1.3 The witness path

Each step is one whole-component swap of T − 22.

| step | swap (cert colours) | component | state | frame (x_j…), roles a,b,g,d | pattern@S | DL? |
|---|---|---|---|---|---|---|
| 0 | — | — | s | (21,20,25,11,14); 2,0,3,1 | dgdbg@41 = M(O3) | yes [cert] |
| 1 | 2↔1 | {2,9,12,25} | s₋₁ = B(s) | (25,11,14,21,20); 1,3,2,0 | gdbab@24 = L2 | yes [hand] |
| 2 | 0↔1 | {1,5,6,7,15,16,20,24,25} | s₋₂ = B(s₋₁) | (14,21,20,25,11); 1,2,0,3 | dgdbg@02 = N3 | yes [hand] |
| 3 | 3↔1 | {20,23} | s₋₃ ≅ B(s₋₂) | (20,25,11,14,21); 3,0,1,2 | gdbab@30 = M(L2) | yes [hand] |
| 4 | 0↔1 | {1,5,6,7,15,16,24} (**no link vertex**) | s₋₃′ | same link as s₋₃ | — | **no**: lock 2 fails |
| 5 | 2→0 | {21} | filled | link 0,3,0,3,1 | — | fill |

Notes on the steps:
- **Step 3.** At s₋₂ the {G,D}-subgraph has exactly two components: {20,23} and the one containing x₀ = 14 and x₄ = 11. So swapping {20,23} is B(s₋₂) up to permutation.
- **The final colouring.** s₋₃ = A{2,4,12,18,19,21,27}, B{1,3,15,16,25,26}, G{0,8,10,11,13,17,20}, D{5,6,7,9,14,23,24}. It is proper, checked edge by edge.

**Why step 4 kills.**
- In the frame of s₋₃ (roles: a = G, b = B, g = D, d = A), x₄ = 21 has degree 5. Its outer neighbours are w₃ = 13 (colour a) and w₄ = 15 (colour b). So **15 is the only b-neighbour of x₄**.
- The {B,D}-subgraph at s₋₃ has two components: {3, 9, 14, 23, 25, 26}, which is lock 1 and contains x₁ = 25 and x₃ = 14, and {1, 5, 6, 7, 15, 16, 24}, which contains **no link vertex**.
- Swapping the second component turns 15 into D. Then 21 has neighbours 13 (G), 14 (D), 15 (D) and 20 (G), so its {A,B}-component is {21}, and lock 2 (25 to 21) fails.
- Recolouring 21 with B is then proper, and it leaves the link coloured 0, 3, 0, 3, 1, which has three colours. That is the fill.

So r(s) ≤ 5. With the certificate's lower bound, r(s) = 5.

**Net change.** Steps 2 and 4 swap the same seven vertices back. From s to s₋₃′ only six vertices change: 2, 9, 12 (A↔D), 25 (A→B), 20 (B→G) and 23 (G→D).

**Relation to intern D's C5.** The final kill starves the same kind of vertex that C5 highlights: a degree-5 singleton whose only lock-colour neighbour is a ring vertex. But the kill comes at s₋₃, three B-steps away. C5 is a statement about s itself; the mechanism here is "walk the F/B orbit to a state with an un-leaked silent starvation".

**Count not reconciled.** By hand I find 2 states at distance 1 and 5 at distance 2: s₁′ (the {2,10} G↔D swap after F), s₂, s₋₁′ ({9,10}), s₋₁″ ({3,9,14,26}) and s₋₂. Distance 3 then has at least 10 states, which looks more than the 13 implied by "21 within 3 swaps". This may be my slip; the audit replay should print the per-layer counts (§7, item 1).

## 2. Lemma SS (silent starvation) [hand, degree-free]

**Setting.** A DL state with frame (a,b,a,g,d) on x₀..x₄. Lock 1 is x₁ ~ x₃ in {b,g}; lock 2 is x₁ ~ x₄ in {b,d}.

**Lemma SS.**
- Let (t, c) be one of the following four pairs: (x₃, b) or (x₁, g) for lock 1; (x₄, b) or (x₁, d) for lock 2.
- Let U be the set of c-neighbours of t in T − v.
- Suppose that for each u ∈ U there is a colour c′ ∉ {c, colour(t)} such that the {c, c′}-component K_u of u contains no link vertex.
- Then swapping the distinct K_u in turn (at most |U| swaps) gives a state with the same link colouring in which the corresponding lock fails. That state is not DL, so r ≤ |U| + 1.

**Proof.**
- Each K_u avoids the link, so each swap leaves the link colours unchanged. The swaps are of components that avoid t, since colour(t) ∉ {c, c′}.
- A swap of K_u recolours only vertices of K_u. A vertex of U lying in a different K_{u′} keeps its colour c until its own swap, because the components of one pair are disjoint. Components of different pairs may change after a swap, so do the swaps in an order and recompute.
- The simple sufficient form is |U| = 1, which is the case used here.
- After the swaps, t has no c-neighbour. Lock 1 needs a {b,g}-path that enters x₃ through a b-vertex and leaves x₁ through a g-vertex. Lock 2 needs the same with b and d. So that lock fails.
- An unfilled non-DL state fills in one swap (L1 Step 1 / MathReviewCleanToVHE L3). If the state is filled, r is even smaller. ∎

**Remarks.**
- (i) No degree hypothesis is used. The radius bound is ≤ 2 when |U| = 1, that is, when t has a unique c-neighbour, which is typical for a degree-5 t.
- (ii) Which c′ are possible:
  - For (x₃, b): c′ ∈ {a, d}. With c′ = a, K_u must miss the AB component of the triple; with c′ = d, it must miss the lock-2 component.
  - For (x₄, b): c′ ∈ {a, g}.
  - For (x₁, g): c′ ∈ {a, d}. With c′ = a, K_u must miss K_F and the {a,g}-component of x₀; with c′ = d, it must miss the {g,d}-component of x₃x₄.
  - For (x₁, d): c′ ∈ {a, g}.
- (iii) The (x₃, b) and (x₄, b) cases with c′ = a, applied to w₃ in the R3/dgdbg states, are **exactly intern B's AB\***. So SS contains AB\* as a special case and adds three more types.
- (iv) In Tait terms (§4.3), an SS swap is a switch of dual 2-coloured **cycles** that do not pass through P. For example, SS on (x₄, b) with c′ = g switches (ab, ag)-cycles. That switch reroutes the lock path Z₂, which is a (ab, ad)-path, along those cycles.

## 3. SS on Math's cycle Γ₁ for (5,5,6,5,6) [hand]

Notation is as in MathTwoSixNeighbours §1. The ring is cyclic, consecutive ring vertices are adjacent, and x_t sees w_{t−1}, then m_t (if t ∈ S), then w_t. The m's are forced by properness, exactly as in MathTwoSixNeighbours' tables.

Meaning of the verdicts:
- **"Blocked"**: the component is locally forced to contain a link vertex.
- **"Fails"**: the swap gives t a new c-neighbour. This happens at a degree-5 x₁, where w₀ and w₁ are adjacent and coloured g and d.
- **"Branch"**: locally isolated, so the move kills unless an outside path leaks.

### 3.1 The dgdbg states (N3, L3, M(O3), O3, M(L3))

The only unblocked SS move is (x₃ or x₄, b) at w₃ with c′ = a: "w₃'s {a,b}-component misses the triple", which is AB\*. The x₁ moves fail or are blocked in every case:
- @02 and @24: w₀w₁ = dg are adjacent.
- @41 and @13: w₁ is joined to w₂ = d, which is adjacent to x₃; and w₀ is joined to w₄ = g, which is adjacent to x₄.

So nothing new beyond AB\*.

### 3.2 The gdbab states (L2, M(L2), N2, O6, M(O6))

| state | forced m | SS branch(es), i.e. the leak needed to block | blocked/failing |
|---|---|---|---|
| L2 = gdbab@24 | m₂ = g, m₄ = g | (x₃, b) via w₂ with c′ = d: w₂'s ring neighbours are m₂ (g) and w₃ (a). **Leak: w₂ ∈ {b,d}-component of x₁.** | x₄ via w₄: w₄ adj w₀ (g) adj x₁; x₁ moves fail |
| M(L2) = gdbab@30 | m₀ = d, m₃ = d | (x₄, b) via w₄ with c′ = g: w₄'s ring neighbours are m₀ (d) and w₃ (a). **Leak: w₄ ∈ {b,g}-component of x₁.** *This leak is absent in the certificate (step 4).* | x₃ via w₂: w₂ adj w₁ (d) adj x₁ |
| N2 = gdbab@02 | m₀ = d, m₂ = g | **both** of the above | x₁ moves fail |
| O6 = gdbab@13 | m₁ = a, m₃ = d | (x₁, g) via w₀ with c′ = d, and (x₁, d) via w₁ with c′ = g: w₀ and w₁ are separated by m₁ = a. **Leak: w₀ and w₁ are both in the {g,d}-component of x₃x₄.** Its only local access is m₃. | x₃ and x₄ moves blocked |
| M(O6) = gdbab@41 | m₁ = a, m₄ = g | same as O6 (w₀ and w₁ separated by m₁ = a) | x₃ and x₄ moves blocked |

Sample derivations:
- **@30.** m₀ is adjacent to x₀ (a), w₄ (b) and w₀ (g), so m₀ = d. The ring neighbours of w₄ are m₀ (d) and w₃ (a), and its link neighbours are x₀ (a) and x₄ (d). So no b/g neighbour of w₄ lies in the ball, and its {b,g}-component meets x₁'s only through vertices beyond the ring.
- **@13.** m₁ is adjacent to x₁ (b), w₀ (g) and w₁ (d), so m₁ = a. That separates w₀ from w₁ on the ring.

**Consequence [hand].** Along Γ₁ the states alternate dgdbg, gdbab. To survive the adversary must leak AB at every dgdbg state, which MathTwoSixNeighbours already required. It must **also** leak the SS branch at every gdbab state. In particular, a DL state on Γ₁ whose F/B-orbit meets a gdbab state with the SS leak absent has radius ≤ (distance along the orbit) + 2. The certificate is the case at distance 3, which gives 5.

### 3.3 Degree ≥ 6 (where exactly 6 is used)

- **Lemma SS: degree-free.**
- **The ring table** uses "the free vertex has exactly one m", in order to force m's colour and isolate w_t.
  - If x₀ has degree ≥ 7 at a gdbab state with x₀ free and x₄ of degree 5, the ring between w₄ and w₀ is w₄, m⁽¹⁾, …, m⁽ᵉ⁾, w₀, with every m ≠ a.
  - SS on (x₄, b) is then **locally blocked** iff the m-run from w₄ to w₀ is entirely b/g.
  - With one m this is impossible, since m⁽¹⁾ = d is forced. With two or more it is possible, for example the run b, g, b, g. Otherwise it is a branch, as before.
- So for degree ≥ 7 the SS candidates of §3.2 can disappear for some m-colourings. Any extension needs the m-run colours added to the automaton state (as in intern B §4).
- **The certificate's kill** uses x₀ = 20 of degree 6 (m₀ = 19, coloured D, which is d in the frame of s₋₃).

## 4. Structural lemmas toward a potential argument [hand]

**4.1 (repeated colour is invariant).** If s is DL with repeated colour a, then F(s) and B(s) (when unfilled) have repeated colour a again.
- *Proof.* F swaps a ↔ g on K_F, which contains x₂ and x₃ but not x₀ (Jordan). The new repeated pair is {x₃, x₀}, and both are now a. B is the mirror case. ∎
- So one actual colour class is "the a-class" along a whole F/B orbit, and only its shape changes. Degree-free.

**4.2 (F-orbits).** On DL states, B ∘ F = id (MathTwoSixNeighbours §1). So the F/B graph on DL states is a disjoint union of paths and cycles.
- (a) If the orbit of s is a path, both of its ends are DL states whose F-image or B-image is not DL. So r(s) ≤ 2 + (distance to the nearer end).
- (b) If F^k(s) ≅ s up to colour permutation, then **5 | k**. F moves the repeated pair index j to j + 3, and a canonical state fixes the repeated positions, so 3k ≡ 0 (mod 5).
- Degree-free. ∎

**Corollary 4.3.** A targetless Kempe class at v (one with infinite radius) consists of DL states only. So every F/B orbit in it is a **cycle** of length divisible by 5, and every SS branch of §2 is leaked at every state of it. *This is the exact target of a potential argument.* A function on states that strictly changes along every F-cycle cannot exist, because the orbit returns to its start. The potential must therefore be **non-local in the orbit**: for example, an invariant that forbids a closed F-cycle in which every SS leak is present. I found no such invariant [open].

**4.4 (Tait form) [hand, standard].**
- *Correspondence.* Canonical states, meaning colourings of T − v up to permutation, correspond one-to-one with Tait colourings of the dual H of T − v. In H, P is the pentagon node with edges e_t dual to x_t x_{t+1}.
- *Kempe classes.* The Kempe classes coincide with the classes under single 2-coloured cycle or path switches.
  - A G-swap of K switches all the 2-coloured dual cycles and paths in ∂K at once.
  - Conversely, switching one cycle (or one path through P) C, in the two colours other than p + q, equals swapping p and q on every vertex on one side of C.
  - That is a union of whole {p,q}-components, because {p,q}-edges have dual colour p + q and do not cross C.
- *The fill set.* With X, Y, Z the three dual colours, the edges at P always carry one colour three times and the other two once each. **Filled ⇔ the two singleton P-edges are adjacent.** The total is zero, so the counts have equal parity, giving (3,1,1).
- *DL* is the Tait lock criterion (pd2).
- *The five link swaps at a DL state.* F, B, AB (or G), {a,d} of x₂, and {a,g} of x₀ switch exactly the five P-paths Z₂′, Z₁′, Z₃, Z₁ and Z₂ (up to cycles). All five keep the state unfilled. So **every route to a fill passes through a non-DL state created by cycle switches (silent swaps) or by a lock-path switch at a state that is already non-DL**. The certificate does exactly this at step 4.

## 5. Killed lines

- **K1. "AB\* can be proved" (intern B cycle 2): KILLED.**
  - At all four DL states of the certificate path (s, s₋₁, s₋₂, s₋₃) the triple's {a,b}-subgraph is **connected**: the whole two-colour class.
  - AB\* is a hypothesis to be leaked, not a lemma. It is replaced by the SS family (§2), of which it is one member.
- **K2. "Mohar/Fisk: all 4-colourings of a 3-colourable planar graph are Kempe equivalent [memory], so v is clean": KILLED for this class.**
  - A near-triangulation is 3-colourable only if every interior vertex has even degree [memory, standard].
  - T has n₅ ≥ 12 − 2n₄ ≥ 8 vertices of degree 5 (relative class, MathReviewCleanToVHE L5). At most 6 of them lie in {v} ∪ link, so T − v has an interior vertex of odd degree.
- **K3. "The F/B orbit alone realises the radius": KILLED on the certificate.**
  - B-direction: s₋₁, s₋₂, s₋₃ and B(s₋₃) = s₋₄ are all DL. At s₋₄ the swap is {11,12} A↔G, and its locks are {D,B} 14~25 and {D,G} 14~20, both checked by hand.
  - F-direction: F(s) and F²(s) are DL.
  - The radius is achieved by leaving the orbit with a silent swap.
- **K4. "Adding SS to the independent-leak automaton closes Γ₁ ∪ Γ₂": not true in that model.**
  - Every SS move needs a non-leak, so the adversary of MathTwoSixNeighbours §6 survives by leaking each one, as in the self-loop lemma.
  - SS only helps once leaks are coupled by planarity.
- **Partial negative.** At O6 / M(O6) I looked for a planarity contradiction between the locks P₁ (through w₀) and P₂ (through w₁) and the two {g,d}-leaks into m₃. Every crossing the chords force can be realised by a shared vertex of the common colour. No contradiction exists at one state; any contradiction must use two or more states.

## 6. What remains [open]

The finite target is now sharper than "Γ₁ ∪ Γ₂ closes". In a targetless class every Γ₁ state carries the AB leak (at dgdbg states) **and** the SS leak (at gdbab states), at every visit of a period-5k F-cycle.

**Candidate Lemma C [open].** Let s be dgdbg@02 (N3). Suppose AB leaks at s (w₃ ∈ the {a,b}-component of x₁). Then at B(s) = gdbab@30, the SS leak (w₄′ ∈ the {b′,g′}-component of x₁′) fails, or a leak needed two steps later fails.
- In the certificate, the AB leak at s₋₂ ({D,A} connected) and the absent SS leak at s₋₃ coexist. So "fails at the next step" is consistent with the data, but this is not a proof.
- How to attack it: translate both leaks to fixed colours.
  - At s₋₂ the AB leak is a {D,A}-path.
  - At s₋₃ the SS leak is a {B,D}-path from 15 to 25.
  - B changed only the D,G vertices of K_B.
- Then use 4.4: the SS leak is a pair of (XY)-cycle conditions, and AB is a Z₃-path condition.

## 7. For the Mac Studio (nothing was run here)

1. **Replay of the 5-swap witness (light, < 1 s).** A new 20-line script `replay_path.py`, stdlib only, importing nothing.
   - Load `91a307d1852a1764.graph.json` and hole 22, starting from `hole22.state.json`.
   - Apply the five swaps of §1.3, each given as (seed vertex, colour pair) = (2,{2,1}), (25,{0,1}), (20,{3,1}), (15,{0,1}), (21,{2,0}).
   - At each step assert that the seed's component equals the listed set, and print the link colours and DL status using `check.py`'s `kind` (copied, not imported).
   - Expected: DL, DL, DL, DL, nonDL, filled.
   - Also print the per-layer counts of the `lb` BFS, so the "21 within 3" figure can be reconciled with §1.3.
2. **Test "F/B-walk + one SS" (one core, minutes).** For every DL state in the Phase C tables at holes with two non-adjacent link vertices of degree ≥ 6 (including (5,6,5,5,8)), compute:
   - r(s);
   - r_SS(s) = min over k ≥ 0 of k + 1 + (1 if the state F^{±k}(s) has a one-swap kill, i.e. starvation, confined AB or SS with |U| = 1, else ∞) — the extra 1 counts the fill.
   - Tabulate r against r_SS.
   - Prediction: r = r_SS for every radius-5 state, and r ≤ r_SS everywhere (always true).
   - Kill: a radius-5 state with r_SS > 5. Then SS is not the mechanism, and §6 is aimed at the wrong move.
3. **Leak coupling test (one core).** In the same tables, record at each Γ₁ state the two leak bits: AB leaked at dgdbg, SS leaked at gdbab. Report every F/B-cycle (not path) found and its leak bits.
   - Prediction: no DL F-cycle has all SS bits leaked.
   - Any F-cycle found is the first evidence of the structure in Corollary 4.3.

## 8. Ledger

- [hand]: §1 component computations and the witness path (radius ≤ 5, matching the certificate's 5); Lemma SS; the §3 tables; 4.1, 4.2, 4.3; 4.4 (standard); kills K1–K4.
- [cert]: radius = 5 lower bound (Studio check, audit replay pending).
- [memory]: the Mohar/Fisk theorem and the even-degree criterion (used only to kill K2).
- [open]: finiteness of R\* for (5,5,6,5,6) and for degree ≥ 6; Candidate Lemma C.
- Single reader. Every [hand] item is unchecked by a second reader or machine. The likeliest slip is a component list in §1.3, so Studio item 1 checks every one of them.

## Math lead's review note (6 Oct): a gap in Lemma SS, and the fix

**Gap.** The proof says "after the swaps, t has no c-neighbour". But swapping K_u (the {c, c′}-component of u) also turns every **c′-coloured** vertex of K_u into colour c. If some c′-neighbour y of t lies in K_u (y adjacent to t, joined to u by a {c, c′}-path avoiding t), then after the swap y has colour c and is again a c-neighbour of t. The lock is then not shown to fail. Nothing in the hypotheses excludes this: K_u avoids the link, but y need not be a link vertex.

**Fix (stronger hypothesis).** Require in addition that **K_u ∩ N(t) = {u}** for each u ∈ U, i.e. no c′-neighbour of t lies in K_u. Then after the swaps t has no c-neighbour, and the rest of the proof stands. With |U| = 1 the bound r ≤ 2 holds under this hypothesis.

**Effect.** §3's claim that each gdbab state of Γ₁ has an SS move that is "not locally blocked" must be rechecked against the added condition. The worker's certificate reading in §1 is unaffected, because it replays actual swaps. Status of Lemma SS: **[hand], corrected, unreviewed beyond this note.**
