# Path 9: structure of a hypothetical stuck class at a degree-5 hole

Math research worker (path 9 lead), 6 October 2026. **Hand work only; nothing was run on this machine.** Studio specs are in §8. No other file was edited; nothing committed.

Labels: **[hand]** complete proof here, no second reader yet; **[cited]** from a named note; **[spec]** a Studio test, not run; **[open]**; **[KILLED]**.

Inputs read: TwoWeekPlan-2026-10-06 (path 9), the no-frozen-DL lemma and Math's review (15:31, 15:50), MathConfinementAttack (Thm A), MathCleanVertexAttack (Thms C, D), MathTaitGlobal, pd2_lock_proof, MathOneStarF1 (SK, leaks), MathRstar55656 (SS), MathClassicalReductions, and, after the coordinator's mid-task message, FellowF-55656.md (Lemma C★).

## 0. Verdict first

1. **Lemma E (exact one-step closure) [hand].** At a DL state, exactly eight bichromatic components meet the link. For each of the eight swaps, "the image is DL" is equivalent to **one or two explicit non-connectivity statements** between two link vertices, inside a mixed vertex set built from three colour classes (§2). This replaces every starvation, E1, SS, AB★ and W rule with one exact predicate per move.
2. **Lemma T (tangle) [hand].** In a stuck class, every lock-2 path passes through a B-vertex of K (the {α,B}-component of x₂), and every lock-1 path passes through an A-vertex of L (the {α,A}-component of x₀) (§3). This is degree-free and nonlocal. It is new at the "inverted" states of Fellow F's table (§7).
3. **Lemma X (forced crossing, no nesting) [hand].** In a stuck class, every lock-1 path crosses every lock-2 path at a μ-vertex other than x₁. **Nested lock curves never occur.** If the two lock paths leave x₁ in "inverted" order, they cross at least twice, and both have length ≥ 5 (§4).
4. **Lemma R (silent swaps act inside lock regions) [hand].** Split the six colour pairs into Π₁ = {αB, μA}, Π₂ = {αA, μB} and Π₃ = {αμ, AB}. A swap of a component that misses the link and has its pair in Π₁ lies on one side of every lock-1 curve. It keeps lock 1, K, K_B and M₁, and it can break lock 2 only through an exact rerouting predicate. The same holds for Π₂ with lock 2. Π₃ swaps can act on both (§5).
5. **Ring-adjacent components (§6) [hand].** The degree-5 two-ball consequences of Lemma E, with witnesses of length ≤ 4, are **exactly** the known rules: the five starvation rules, plus four forced memberships. These four are, letter for letter, **SS3, SS4 and AB★ (twice)** from MathRstar55656, intern B and Fellow F. Lemma E derives them degree-free, so that list is complete for such witnesses.
6. **Lemma C★ (Fellow F, (5,5,6,5,6)): NOT proved [open].** What Lemma T and X add (§7):
   - New nonlocal predicates **T1, T2** at the six inverted states (N3, N4, L3, L4, M(L3), M(L4)). Fellow F lists only AB★, SS3 or SS4 there.
   - At those states the lock paths must cross twice.
   - T1 and T2 at s are carried along the cycle by Lemma LC as constraints on F(s).
   - No contradiction follows from one state or from the LC-carried pair.
7. **Stop rule (plan, path 9): triggered for the colour-pattern space.** Lemmas E, T, X and R do **not** shrink the space of two-ball *colour* patterns beyond the starvation rules already known. They shrink only the membership- and incidence-annotated space: forced memberships, T1/T2 incidences, and the crossing type. Every one of them is a consequence of one-step closure, so Studio should compute closure exactly (§8, P9-F) rather than collect more hand lemmas. My recommendation: stop hand work on path 9 after P9-F. Resume only if P9-F finds a feature that is forced at depth 2 but not at depth 1, since that would be a genuinely multi-state structure.

## 1. Setting and conventions

- **Graph.** T is a plane triangulation and v has degree 5 with link x₀..x₄ in rotation order.
  - **Assumed: no separating triangle (F1b).** So the link is an induced 5-cycle. The ring vertex w_t (the common neighbour of x_t and x_{t+1} other than v) is not a link vertex. w_t ≠ w_{t+1}, since otherwise x_{t+1} would have degree 4.
  - R_t is the set of neighbours of x_t outside the link and v, read in rotation: w_{t−1}, middles, w_t. Consecutive members of R_t are adjacent. If deg x_t = 5, then R_t = {w_{t−1}, w_t} and these two are adjacent.
  - §4–§5 use nothing else. §6 uses F1b only to name w_t. **Nothing uses F2, the diamond or 2.122**, so everything holds in a minimal counterexample, as MathTaitGlobal Prop 5.1 says it must.
- **Stuck class S.** A Kempe class of 4-colourings of G = T − v with no filled state. Every state of S is DL [cited: Thm A Step 1] and non-frozen [cited: no-frozen lemma]. S is closed under every swap and contains all five repeat types [cited: Thm A].
- **Frame (index 0).** Link colours (α, μ, α, A, B) on x₀..x₄.
  - Lock 1: a {μ,A}-path x₁ ~ x₃.
  - Lock 2: a {μ,B}-path x₁ ~ x₄.
  - **Dictionary to Fellow F / intern B letters:** α = a, μ = b, A = g, B = d.
- **The eight link components of a DL state.** Their link traces are forced by the two lock Jordan curves [hand, same argument as the no-frozen lemma]:

| name here | pair | link trace | Fellow F name | swap name (here / F) |
|---|---|---|---|---|
| J | αμ | x₀ x₁ x₂ | K_AB | J / AB |
| N | AB | x₃ x₄ | K_G | N / G |
| M₁ | μA | x₁ x₃ | K₁ | M₁ / L1 |
| M₂ | μB | x₁ x₄ | K₂ | M₂ / L2 |
| L | αA | x₀ | K₀ | Z2 / G0 |
| K_F | αA | x₂ x₃ | K_F | F / F |
| K_B | αB | x₀ x₄ | K_B | B / B |
| K | αB | x₂ | K_D2 | Z1 / D2 |

- **Notation.** For a colour c and a set Y, c_Y means the c-vertices in Y, and c_{¬Y} the c-vertices not in Y. "u ≁ t in X" means u and t lie in different components of G[X].

## 2. Lemma E: exact one-step closure [hand]

**Lemma D (pentagon duality).** Let X be a {p,q}-component of G with X ∩ link = {x_i}, and let r, s be the other two colours. Then x_{i−1} and x_{i+1} are joined by an {r,s}-path in G. Conversely, an {r,s}-path from x_{i−1} to x_{i+1} separates x_i from the other two link vertices, by the Jordan curve through v.

*Proof.*
- **Cut edges per face.** Each triangular face of G has 0 or 2 edges with exactly one end in X. It has three distinct colours, so at most two vertices of X. The pentagon P has exactly two such edges, x_{i−1}x_i and x_ix_{i+1}.
- **The dual walk.** In the dual, the cut edges therefore form paths and cycles. The one through P leaves by x_ix_{i+1} and returns by x_{i−1}x_i.
- **The far ends.** List the ends of its cut edges that lie outside X: y₀ = x_{i+1}, …, y_t = x_{i−1}.
  - Two consecutive cut edges lie on one triangle. Either that triangle has one X-vertex, and then y and y′ are adjacent, or it has two, and then y = y′.
  - Each y_k is adjacent to an X-vertex and lies outside X, so its colour is r or s.
  - So (y_k) is an {r,s}-walk, and it contains an {r,s}-path.
- The converse is the Jordan curve theorem through v. ∎

**Lemma E.** Let s be DL (frame above). Then each image is DL if and only if the condition in the last column holds:

| move (swapped comp.) | image link, new frame | lock kept automatically | **image DL ⇔** |
|---|---|---|---|
| Z1 (K) | (α,μ,B,A,B), index 2 | old lock 1 | x₁ ≁ x₄ in μ ∪ B_{¬K} ∪ α_K |
| Z2 (L) | (A,μ,α,A,B), index 3 | old lock 2 | x₁ ≁ x₃ in μ ∪ A_{¬L} ∪ α_L |
| F (K_F) | (α,μ,A,α,B), index 3 | old lock 2 | x₁ ≁ x₃ in μ ∪ α_{¬K_F} ∪ A_{K_F} |
| B (K_B) | (B,μ,α,A,α), index 2 | old lock 1 | x₁ ≁ x₄ in μ ∪ α_{¬K_B} ∪ B_{K_B} |
| M₁-swap | (α,A,α,μ,B), index 0 | lock 1 | x₀ ≁ x₂ in α ∪ μ_{¬M₁} ∪ A_{M₁} |
| M₂-swap | (α,B,α,A,μ), index 0 | lock 2 | x₀ ≁ x₂ in α ∪ μ_{¬M₂} ∪ B_{M₂} |
| N-swap | (α,μ,α,B,A), index 0 | none | x₀ ≁ x₂ in α ∪ A_{¬N} ∪ B_N **and** in α ∪ B_{¬N} ∪ A_N |
| J-swap | (μ,α,μ,A,B), index 0 | none | x₀ ≁ x₂ in B ∪ α_J ∪ μ_{¬J} **and** in A ∪ α_J ∪ μ_{¬J} |
| (DL itself) | | | x₀ ≁ x₂ in α ∪ B **and** in α ∪ A |

*Proof (Z1 written out; the others are the same three steps).*
- **Image and frame.** Swapping K (with K ∩ link = {x₂}) gives the link (α,μ,B,A,B). The repeat is {x₂, x₄}, so the index is 2, with m′ = x₃, a′ = x₀ and b′ = x₁.
- **The kept lock.** Lock 2′ is an {A,μ}-path x₃ ~ x₁. K holds only α and B, so the {μ,A}-subgraph is untouched, and this is old lock 1.
- **The lock to check.** Lock 1′ is an {α,A}-path x₃ ~ x₀ in the image s₁.
  - It fails iff the s₁-{α,A}-component of x₃ meets the link only in x₃, because x₂ and x₄ are B and x₁ is μ in s₁.
  - By Lemma D, that happens iff x₂ and x₄ are joined by an s₁-{μ,B}-path.
- **Back to s-colours.** In the colours of s, s₁-μ = μ and s₁-B = B_{¬K} ∪ α_K. Also x₂ ∈ α_K is adjacent to x₁ ∈ μ, so "x₂ ~ x₄" is the same as "x₁ ~ x₄" in that set.

For each other row: name the image link and frame, note which pair the swap leaves untouched (the kept lock), apply Lemma D to the component of the remaining lock's endpoint, and translate the colours. A one-vertex link trace was checked in each case:
- Z2: the trace is {x₂}, or {x₄} for the x₀ form.
- F: {x₂}. B: {x₀}.
- M₁: {x₄}. M₂: {x₃}.
- N: {x₁} for both locks. J: {x₁} for both locks.

Two notes on the DL row:
- "Lock 1 ⇔ x₀ ≁ x₂ in α ∪ B" is the no-frozen lemma together with its Lemma-D converse.
- Lock 2 is the same with α ∪ A. ∎

**Shape of 1-closure.**
- The DL row and the M₁, M₂, N and J rows all say "**the repeat pair x₀, x₂ is separated**" in seven different three-class graphs.
- The Z1/B rows say that lock 2 is **destroyed** when B is replaced by B_{¬K} ∪ α_K, or by B_{K_B} ∪ α_{¬K_B}.
- The Z2/F rows say the same for lock 1, with A replaced by A_{¬L} ∪ α_L, or by A_{K_F} ∪ α_{¬K_F}.
- In a stuck class all eight hold at every state ("1-closed"), and at every image, and so on.

**Pattern-space consequence.** This gives the exact one-step predicate, but no new two-ball colour kills (§6). Studio test: P9-E.

## 3. Lemma T (tangle) [hand]

**Lemma T.** Let s be DL with Z1(s) and Z2(s) DL (true in S).
- **(T1)** Every lock-2 path P₂ contains a B-vertex of K. Equivalently, x₁ ≁ x₄ in M₂ − B_K.
- **(T2)** Every lock-1 path P₁ contains an A-vertex of L. Equivalently, x₁ ≁ x₃ in M₁ − A_L.

*Proof.* For T1: if P₂ avoided B_K, then P₂ ⊂ μ ∪ B_{¬K}, and P₂ would join x₁ to x₄ in the Z1 set of Lemma E. T2 is the same with the Z2 row. ∎

(F and B give the weaker statements "P₁ has an A-vertex outside K_F" and "P₂ has a B-vertex outside K_B". T implies them, since L ≠ K_F and K ≠ K_B.)

**Incidence reading (item 2 of the brief).** Pairs of link components that share one colour but have no common link vertex: there are six, namely (L,K), (K_F,K_B), (N,L), (N,K), (M₁,L) and (M₂,K).
- A stuck class forces **M₂ ∩ K ≠ ∅** and **M₁ ∩ L ≠ ∅**, in the separating form above.
- Heawood forces K and L to touch: they share an α-vertex or have a B–A edge [cited: MathTaitGlobal §1.4].
- The other three are free.
- In Fellow F's words, T1 and T2 are the degree-free "leaks" of the two lock components into the two far {α,·}-components.

**Pattern-space consequence.** None on colours. On incidences, 3 of the 7 bits are forced. Studio: P9-T.

## 4. Lemma X (forced crossing; nesting excluded) [hand]

Let C₁ = v x₁ P₁ x₃ v and C₂ = v x₁ P₂ x₄ v.
- At v, C₁ separates x₂ from {x₀, x₄}, and C₂ separates {x₂, x₃} from x₀.
- Call the pair (P₁, P₂) **inverted** if the first vertex b of P₂ comes before the first vertex a of P₁ in the rotation at x₁, read from x₀ to x₂.

**Lemma X.** Let s be DL with Z1(s) and Z2(s) DL. For every lock-1 path P₁ and every lock-2 path P₂:
- (i) P₁ and P₂ share a μ-vertex other than x₁ at which P₁ passes from x₀'s side of C₂ to x₃'s side.
- (ii) If the pair is inverted, they share at least two such μ-vertices, and |P₁|, |P₂| ≥ 5.

*Proof.*
- **Where a\* lies.** By T2, P₁ contains a\* ∈ A_L. Join x₀ to a\* by an {α,A}-path S_L inside L. S_L carries only α and A, and C₂ carries only v, μ and B, so S_L does not meet C₂. Hence a\* lies strictly on x₀'s side of C₂.
- **One crossing.** P₁ runs from a\* to x₃, which lies strictly on the other side. It meets C₂ only at common vertices: edges do not cross, and they share no edge, since μ–μ is impossible. So P₁ passes through a vertex y of P₂ after a\*. That y is coloured μ, and y ≠ x₁. This proves (i).
- **The inverted case.** At x₁, C₂ uses the edges x₁v and x₁b. The sector containing x₁x₂ holds the neighbours after b, so a lies strictly on x₂'s side.
  - P₁ = x₁, a, …, a\*, …, x₃ goes from x₂'s side to x₀'s side and back. That gives two distinct common μ-vertices y₁ and y₂, both other than x₁.
  - Each path alternates μ with A or B from x₁ to an end of colour A or B. So it has (|P|+1)/2 μ-vertices. Three of them (x₁, y₁, y₂) force |P| ≥ 5. ∎

**Corollaries.**
- **No nesting.** The configuration in which P₁ stays on x₂'s side of C₂ (lock-1 curve nested inside the lock-2 curve) never occurs in S.
- **Degree 5 at the middle.** If deg x₁ = 5, then R₁ = {w₀, w₁} = {A, B}.
  - (w₀, w₁) = (A, B) is non-inverted. T1 and T2 are then witnessed locally: w₀ ∈ L ∩ M₁ and w₁ ∈ K ∩ M₂. One crossing is needed.
  - (w₀, w₁) = (B, A) is inverted. Then w₀ ∈ K_B and w₁ ∈ K_F, T1 and T2 are both nonlocal, there are two crossings, and every lock path has length ≥ 5.
- **Along an F-orbit.** By pd2's corollary, lock 2 of s is lock 1 of F(s) (Fellow F's Lemma LC). The lock paths Λ_k := P₁(Fᵏs) therefore form a pentagram chain, and Λ_k crosses Λ_{k+1} inside the state Fᵏs.
- **Is the inverted case a local kill?**
  - Without further hypotheses: an inverted pair with a lock path of length 3 kills.
  - Under F1b + F2 a length-3 lock path x₁, a, y, x₃ through the corner w₁ forces d₂ = 5 and y = w₂. Starvation already kills that (R₂ would lack B).
  - Under Birkhoff's internal 6-connectivity [cited, F4; not assumed], every length-3 lock path would be such a corner path. So in the minimal frame this corollary kills nothing new locally.

**Pattern-space consequence.** On colours: none in the minimal frame. On geometry: it excludes nesting and forces double crossing at inverted states. Studio: P9-X.

## 5. Lemma R (silent swaps act inside lock regions) [hand]

Let Y be a {p,q}-component with Y ∩ link = ∅ ("silent").
- **(R1)** If {p,q} ∈ Π₁ = {αB, μA}, then Y ∩ M₁ = ∅. The colours differ, or Y is a different μA-component from M₁, which contains x₁. So Y lies strictly on one side of every lock-1 curve C₁. Likewise, Π₂ = {αA, μB} components lie on one side of every C₂.
- **(R2)** A swap of a {p,q}-component preserves the vertex sets of all {p,q}-components and all {r,s}-components. The colours of these sets are untouched or merely exchanged.
  - So a silent Π₁-swap preserves K, K_B, M₁, lock 1 and the (β,γ) Tait system (Z1, Y1).
  - A silent Π₂-swap preserves L, K_F, M₂, lock 2 and Z2, Y2.
  - A silent Π₃-swap preserves J, N and Z0.
- **(R3) Exact survival.** For a silent αB-swap of Y:
  - lock 2 survives ⇔ x₁ ~ x₄ in μ ∪ B_{¬Y} ∪ α_Y;
  - in particular it survives whenever some lock-2 path misses Y.
  - For a silent μA-swap: x₁ ~ x₄ in B ∪ μ_{¬Y} ∪ A_Y (x₁ ∉ Y since Y is silent).
  - Π₂ swaps are the same with lock 1; Π₃ swaps need both.
  - *Proof:* the recoloured {μ,B}-subgraph is exactly this set. ∎
- **Invariants of S under silent swaps.**
  - The link word is invariant under all of them.
  - The Π_i-structure is invariant under Π_i-silent swaps.
  - Lemma T is preserved in the following sense. A Π₁-silent swap leaves M₁ fixed and can change L only at α-vertices of Y. So T2 can only be destroyed if Y contains every α-vertex of L that links x₀ to M₁. Studio: P9-R.

**Pattern-space consequence.** None. Lemma R reduces the silent-swap work: Π₁ swaps need only the lock-2 test, Π₂ swaps only the lock-1 test.

## 6. Ring-adjacent components: what Lemma E forces in the two-ball [hand]

Allowed ring colours:
- w₀, w₁ ∈ {A, B};
- w₂ ∈ {μ, B};
- w₃ ∈ {α, μ};
- w₄ ∈ {μ, A}.

Memberships forced by adjacency to the link:
- an A-vertex of R₀ lies in L; an A-vertex of R₁ lies in M₁; an A-vertex of R₂ lies in K_F; and so on;
- w₃ = α lies in K_F ∩ K_B; w₃ = μ lies in M₁ ∩ M₂;
- w₄ = A lies in L ∩ N.

Two exclusions, used below, follow from DL:
- (w₂, w₃) = (B, α) adjacent would give K = K_B;
- (w₃, w₄) = (α, A) adjacent would give L = K_F.

I checked every predicate of Lemma E for witness paths through link vertices and ring vertices w_t, using ring edges w_{t−1}w_t at degree-5 link vertices (length ≤ 4). The complete list:
- **Starvation:**
  - R₁ ∋ A, B; R₃ ∋ μ; R₄ ∋ μ (DL);
  - **R₀ ∋ A** (Z1 and B rows, witness x₁ w₀ w₄ x₄ when d₀ = 5);
  - **R₂ ∋ B** (Z2 and F rows, witness x₁ w₁ w₂ x₃ when d₂ = 5).
- **FM1:** d₄ = 5 and w₃ = α force w₄ = μ ∈ M₁ (M₁ row, witness x₀ w₄ w₃ x₃). This is **SS4** in Fellow F's letters.
- **FM2:** d₃ = 5 and w₃ = α force w₂ = μ ∈ M₂ (M₂ row, witness x₄ w₃ w₂ x₂). This is **SS3**.
- **FM3:** d₃ = 5 and w₂ = B force w₃ = μ ∈ J (J row, first form, witness x₂ w₂ w₃ x₄ x₀). This is **AB★**.
- **FM4:** d₄ = 5 and w₄ = A force w₃ = μ ∈ J (J row, second form, witness x₀ w₄ w₃ x₃ x₂). This is **AB★**.
- The N row has no such witness. Both candidate paths need one of the excluded adjacent pairs, or an A–B edge split between N and not-N.

So the leak catalogue of MathRstar55656, intern B and Fellow F at degree-5 x₃ and x₄ is **exactly** the short-witness shadow of Lemma E, now derived degree-free. Fellow F's Lemma W (deg x₄ = 6) is the length-5 shadow of the F and Z2 (G0) rows through m₄.

**Pattern-space consequence.** No new colour kill. The membership-annotated space is cut by FM1–FM4, which were already known in specific classes.

## 7. Fellow F's Lemma C★ at (5,5,6,5,6) [open; what this note adds]

**Translation.** Fellow F's G0 is my Z2 and his D2 is my Z1. He checked those two moves, and L1, L2, AB, G, only for endpoint starvation (his §2.3 and SA-5). Lemma E gives their exact conditions. Their nonlocal content is T1 and T2.

**New predicates for his §3 table [hand].** The degree-5-middle states split by the first two ring letters.
- **Non-inverted** (w₀w₁ = gd in his letters): N1, N2, L1, L2, M(L1), M(L2).
  - T1 and T2 are automatic, since w₀ ∈ K₀ ∩ K₁ and w₁ ∈ K_D2 ∩ K₂. Nothing new.
- **Inverted** (w₀w₁ = dg): **N3, N4, L3, L4, M(L3), M(L4).**
  - (T1) Every lock-2 ({b,d}) path, which leaves x₁ through w₀ ∈ K_B, contains a d-vertex of K_D2.
  - (T2) Every lock-1 ({b,g}) path, which leaves through w₁ ∈ K_F, contains a g-vertex of K₀.
  - By Lemma X(ii) they cross twice, and both have length ≥ 5.
  - Each of these 6 states gets 2 new nonlocal predicates. So **each 10-period carries 3 inverted states on Γ₁ (N3, L3, M(L3)) and 3 on Γ₂ (N4, L4, M(L4))**, if Fellow F's slot lists are right.
- **Degree-6 middle** (S = 13 and 41: O·, M(O·)): T1 and T2 depend on which of (w₀, m₁, w₁) start the paths. I did not tabulate them. Studio item P9-C covers this.

**Carried along the cycle.** Lemma LC (lock 2 of s = lock 1 of F s) carries T1 at s into F(s), where it reads: every lock-1 path of F(s) contains a d-vertex of K_D2(s). T2 at F(s) needs a g′ = b vertex of F(s)'s K₀, which is the F(s)-{a,b}-component of x₃. So the single vertex set K₂(s) carries two tangle demands, one from each frame. That is the first concrete coupling of the kind C★-a asks for.

**Attempt at a contradiction, and why it stops.**
- At an inverted state, the two crossings of Lemma X(ii) are compatible with the plane. Take Fellow F's SA-3 cone, with a b-vertex z outside the ring and paths through it, and add a second b-vertex z′.
- Route P₁ through z′ into K₀'s side and back through z. Route P₂ symmetrically into K_D2's side.
- The four demands T1(s), T2(s), T1(F s) and T2(F s) are all positive connections ("contains a vertex of"). A plane contradiction needs at least one **cut** condition in the same region.
- The only cut conditions in the table are W34 and W23 (Γ₂, at L1·, M(O4|5), O4|5 and M(L1·)). None of these is an inverted state, and the nearest inverted states on Γ₂ (L4, N4, M(L4)) are 2–3 F-steps away.
- I found no way to transport a cut across 2–3 F-steps: LC carries one lock component one step, and its other side is recoloured.

**Status:** C★ is not proved. The concrete sub-target is **(C★-x)**: on Γ₂, the W34 cut at L1(·) (every lock-2 path enters x₄ through one named neighbour), carried by LC to M(O4|5), cannot coexist with T1 and T2 at the next inverted state. [open]

**Transfer to (5,5,6,6,6), (5,6,6,6,6) and (6⁵).** T1, T2, X and R are degree-free, so they transfer verbatim. The inverted/non-inverted split needs deg x₁ = 5, or a rule for which outer neighbour each lock uses. In (6⁵) every middle has three outer neighbours. Inversion is then a property of the chosen pair of paths, and X(ii) applies to every inverted pair. No class-specific table was built.

## 8. Studio intel specs [spec, not run]

Input: the 1,066,690 DL states (frozen_scan set), each with its graph, hole, rotation system and frame (index j, x₀..x₄). Use `astruct_core.py` (`comp`, `doubly`, `F`) and BFS on vertex subsets. Write fresh stdlib scripts.

- **P9-E (Lemma E check, 1-closure census).**
  - For each s, build K, L, K_F, K_B, M₁, M₂, N and J.
  - For each of the 8 moves: (a) evaluate the Lemma E predicate by BFS in the stated mixed set; (b) swap and test `doubly` on the image. Assert (a) == (b).
  - Output: mismatches (expected 0; one mismatch kills that row), the count of 1-closed states, the per-hole count, and a histogram of failing rows.
- **P9-T (Lemma T and incidences).**
  - For each s with Z1(s) and Z2(s) DL: assert T1 (x₁ ≁ x₄ in M₂ minus B-vertices of K) and T2 (x₁ ≁ x₃ in M₁ minus A-vertices of L). Expected 0 failures.
  - Over all DL states: tabulate the 7 incidence bits (6 nontrivial intersections plus K–L touching) against 1-closedness.
- **P9-X (Lemma X).**
  - For each 1-closed s and each pair (a, b), where a is an A-neighbour of x₁ that reaches x₃ in M₁ − x₁, and b is a B-neighbour that reaches x₄ in M₂ − x₁:
    - mark the pair inverted when b precedes a in the rotation at x₁ from x₀ to x₂;
    - for inverted pairs, compute 1 + dist(a, x₃) in M₁ − x₁ and 1 + dist(b, x₄) in M₂ − x₁, and assert both ≥ 5.
  - Expected 0 failures. Also report the fraction of 1-closed states with an inverted pair.
- **P9-M (FM1–FM4).** At 1-closed states meeting each hypothesis, assert the membership. Expected 0 failures. Report the hypothesis frequency and the length of the shortest connecting path (in the two-ball, or outside it).
- **P9-R (silent swaps).**
  - For each 1-closed s and each silent component Y: assert (R2), that the Π-invariant lock is kept.
  - Assert (R3), that the predicate equals the direct DL test of the other lock.
  - Report the fraction of silent swaps that break DL, by Π-type.
- **P9-F (main: forced local patterns).**
  - Pattern key: frame-normalised degrees d₀..d₄ (capped at 8) plus the colour words of R₀..R₄ in rotation, in letters α, μ, A, B.
  - Depth sets: D0 = DL; D1 = 1-closed under the 8 link moves; D1⁺ = D1 with all silent images DL; D2 = D1 with all 8 link images in D1.
  - If the per-hole state lists are complete, also compute the fixpoint D∞ (the largest set closed under link moves inside DL). The calibration predicts D∞ = ∅ at every hole.
  - Output: keys killed between depths; per-key survival rates; and every Boolean key feature that holds in 100% of D2 but in less than 100% of D1.
  - **Decision rule:** if the only features at 100% are the starvation set (R₀ ∋ A, R₁ ∋ A,B, R₂ ∋ B, R₃ ∋ μ, R₄ ∋ μ) and FM1–FM4, then path 9 is closed by the stop rule. Any other feature is a target for a hand proof.
- **P9-C ((5,5,6,5,6), for C★).**
  - On the (5,5,6,5,6) holes and the cert graphs, along every F-cycle found by Fellow F's item 2, log at each state: the §3 predicates, T1, T2, the inverted flag, and the W34/W23 cut sides.
  - Report the longest F-run on which all predicates hold. In particular, report whether any Γ₂ run L1 → M(O4|5) → … → L4 keeps W34, T1 and T2 together. If such a run never occurs across all data, C★-x is the right hand target.

## 9. Ledger

- **[hand]:** Lemma D; Lemma E (all 8 rows; Z1 written out, the rest by the same three steps); Lemma T; Lemma X and its corollaries; Lemma R; the §6 short-witness list with FM1–FM4; the §7 inverted/non-inverted split and the new T1/T2 entries. Nothing here has a second reader yet.
- **[cited]:** Thm A Step 1; the no-frozen lemma; the pd2 corollary (= Lemma LC); MathTaitGlobal §1.4 (Heawood touch) and Prop 5.1; Fellow F's §3 table, the Γ₁/Γ₂ slot lists and SA-3; Birkhoff's internal 6-connectivity (named only, not used).
- **[open]:** Lemma C★ and the sub-target C★-x; a degree-6-middle T table; any planarity contradiction.
- **Stop rule:** four lemmas without a colour-pattern shrink. I recommend stopping path 9 hand work after P9-F unless P9-F finds a depth-2 feature.
