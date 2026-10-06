# Math review: Fellow F, `FellowF-55656.md` (Lemmas O, Γ, LC; move catalogue; G0/D2 starvation)

Math independent review worker, 6 October 2026. **Hand only.** No code was run on this machine; files were only read. Scope: the statements the coordinator named. The §3 predicate table, the full G-table, Lemma C★ and the computation list were not reviewed beyond the spot checks named below. No other file was edited. Nothing was committed.

Context used: Theorem C (`MathCleanVertexAttack.md`, re-derived correct by a worker); the Tait lock criterion and its corollary (`pathways/pd2_lock_proof.md`, reviewed CORRECT in `MathReviewTaitLockCriterion.md`); the pattern and Γ tables (`MathTwoSixNeighbours.md` §3, §5; hand, single reader); Lemma SS with the Math-lead correction (`MathRstar55656.md`, review note); the parity lemma (`MathTaitGlobal.md` §2, unreviewed).

## Verdicts at a glance

| Statement | Verdict |
|---|---|
| O.1 F and B mutually inverse on exact DL colourings | **CORRECT** (the §0 wording "bijection between DL states" is loose: a partial injection) |
| O.2 every F/B component is a path or a cycle; a path fills | **CORRECT** |
| O.3 exact cycle length ≡ 0 (mod 15) | **CORRECT**, elementary, independent of the parity lemma |
| Corollary O | **CORRECT** |
| §2.3 exactly eight link-touching components, and the image table | **CORRECT** (all eight rows rechecked) |
| G0-starvation and D2-starvation | **CORRECT** (a direct endpoint check, so the SS correction does not apply to them) |
| Γ(1) Γ₂ walks have period 10 | **CORRECT given Math's arrow lists** (all Γ₂ arrows rechecked against the 10-slot scheme) |
| Γ(2) no Γ₁/Γ₂ arrows; cycle length ≡ 0 (mod 30) | **CORRECT given Math's tables**; does not use the parity lemma |
| Γ(3) confined G at N2 ↔ N4; Q meets both families; \|Q\| ≥ 60 | **CORRECT** |
| §2.4 "Use": the four-path coupling (i)–(iv) | **CORRECT** |
| LC lock 2 of s = lock 1 of F(s); the mirror | **CORRECT** (needs only lock 2 of s) |
| LC consequence (exit constraint at M(O4)) | **CORRECT** |
| W1 kill rule | **CORRECT** as stated; the "harmless" remarks and "exactly one of F, G0 kills" are loose |
| W2 Jordan side lemma | **CORRECT** |
| W3 "in a targetless class, no lock-2 path enters through w₃ (w₄)" | **CORRECT** |
| "membership m₄ ∈ K_F (K₀) is **equivalent** to the cut condition" (§0, §3 W34/W23, §7 item 3) | **GAP**: only membership ⇒ cut is proved |
| SS3/SS4 (§4.3) against the corrected Lemma SS hypothesis | **CORRECT**: K_u ∩ N(t) = {u} holds at all eight named states |
| SA-5 lock-swap derivation of SS3/SS4 | **CORRECT** (endpoint form) |
| SA-3 counter-picture | **GAP (minor, repairable)**: as written it realises (i) and (ii) only |

## 1. Lemma O

**O.1.**
- I rechecked the frame of F(s). K_F is the {a,g}-component of x₂. It contains x₃ and misses x₀: lock 2 with v separates x₀ from x₂ (pd2 Corollary (i)).
- After F the link is (a,b,g,a,d). The repeat is {x₃, x₀}, so the middle is x₄ and x′ᵢ = x_{i+3}. The roles are a′ = a, b′ = d, g′ = c(x₁) = b, and d′ = c_F(x₂) = g.
- B at F(s) swaps the {a′,d′} = {a,g}-component of x′₀ = x₃. A swap does not change the vertex set of a component, so this component is K_F, and B(F(s)) = s.
- The identity needs only that F(s) is unfilled with that frame. It does not need F(s) ∈ D, so the proof shows slightly more than it states. F(B(s)) = s holds symmetrically, using lock 1 for x₂ ∉ K_B.
- **Wording.** §0 says "F is a bijection between DL states". What is proved is that F is a partial injection on D with left inverse B (F(D) ⊄ D in general). §2.2 states this correctly.

**O.2 (paths fill).**
- Out-degree ≤ 1 is trivial. In-degree ≤ 1 holds because F(s) = F(s′) = t gives s = B(t) = s′.
- **Can a path end because F is undefined?** No. F is defined on every DL state. Lock 2 gives x₀ ∉ K_F, so F(s) is a proper colouring of T − v with link (a,b,g,a,d), which is unfilled. So a path ends only at a state s_end with F(s_end) ∉ D.
- F(s_end) is proper, unfilled and not in D, so it is non-DL. It fills in one swap by Unlock (MathReviewCleanToVHE L3, HP review step 0). That is the only external input.
- A state at F-distance k from s_end fills within k + 2 swaps. A single isolated state (F(s) ∉ D) fills within 2.
- The argument uses only the F-end. That is enough, because every state of a path reaches the F-end by forward steps inside the same Kempe class.

**O.3 (15 | length).**
- F moves the middle index by +3. The triple (c(x₁), c(x₃), c(x₄)) = (β, γ, δ) becomes (δ, β, γ): the new middle x₄ has colour δ, x′₃ = x₁ has colour β, and x′₄ = x₂ has colour γ after F.
- The repeated colour a is fixed (MathRstar55656 4.1).
- An exact link colouring determines its frame uniquely. Four colours on five vertices give a unique repeated pair. So F^k(s) = s forces 3k ≡ 0 (mod 5), and also k ≡ 0 (mod 3) because β, γ, δ are distinct. Hence 15 | k.
- **This is proved here directly. It does not rely on the unreviewed parity lemma.** That lemma claims more (30 raw for every orbit, in any class), and it is consistent with 15.
- **Exact versus up to renaming.** This is handled consistently. Lemma O works on raw colourings, and "Math's 5 | k" is correctly identified as the renaming version.

**Corollary O.** In a targetless class every state is DL and F maps the class into itself, so no path ends. Every component is a cycle, of length divisible by 15. **CORRECT.**

## 2. Move catalogue (§2.3) and the new starvation rules

**Eight components.** The link colours are a (x₀, x₂), b (x₁), g (x₃) and d (x₄).
- {a,b}: x₀x₁ and x₁x₂ are link edges, so this is one component.
- {a,g}: x₂x₃ is an edge, and x₀ is separated from them by lock 2 (Jordan). Two components.
- {a,d}: x₄x₀ is an edge, and x₂ is separated from them by lock 1. Two components.
- {b,g}, {b,d} and {g,d}: one each, by lock 1, lock 2 and the edge x₃x₄.
- Total 8. **CORRECT.**

**Image table.** I recomputed every row: the link, the shift, the roles a′b′g′d′, the kept lock and the new lock. All eight agree with the source.
- For example, G0 gives the link (g,b,a,g,d) with middle x₄ and roles (g,d,b,a). Its lock 1′ = {d,b} x₄ ~ x₁ is lock 2, unchanged because G0 recolours only a/g vertices. Its new lock is {d,a} x₄ ~ x₂.
- D2 gives (a,b,d,g,d) with middle x₃ and roles (d,g,a,b). It keeps lock 1 as lock 2″ and needs {g,a} x₃ ~ x₀.

**G0-starvation and D2-starvation.**
- The new middle x₄ needs a d′ = a neighbour after G0. This is a direct check of the colours after the swap: a ↔ g on K₀, and x₃ ∉ K₀ because x₃ ∈ K_F ≠ K₀.
- The rule is not a silent swap, so the Lemma SS gap (a c′-neighbour turned into c) cannot arise. Both directions of recolouring are already counted, as W1's proof shows.
- The x₂ half of G0 is F-starvation, as stated: G0 does not touch x₂'s d-neighbours.
- D2 is the mirror.
- **CORRECT.**

**G and E1.** For deg x₁ = 5, the adjacent ring pair w₀, w₁ is coloured {g,d}, so they enter or leave K_G together. **CORRECT.**

## 3. Lemma Γ

**(1) The Γ₂ slot scheme.** I checked every Γ₂ arrow in MathTwoSixNeighbours §5 against Fellow's ten slots:

N1(·) → L1(·) → M(O4|O5) → O10 → M(L4) → N4 → L4 → M(O10) → O4|O5 → M(L1(·)) → N1(·).

- N1 → L1 (three arrows), L1 → M(O4|O5), M(O4|O5) → O10, O10 → M(L4), M(L4) → N4, N4 → L4, L4 → M(O10), M(O10) → O4|O5, O4|O5 → M(L1(·)), and M(L1(·)) → N1(·).
- Every arrow advances the slot by exactly 1 (mod 10). The ten slots are disjoint, so every closed walk has length ≡ 0 (mod 10).
- The ten Γ₁ patterns are distinct. **CORRECT given the tables.**

**(2) No arrows between the families; 30 | length.**
- The arrow lists show Γ₁ and Γ₂ each closed under F. B = F⁻¹ on DL images, so the same holds for B.
- An exact F-cycle of length L projects to a closed pattern walk of length L, so 10 | L. With O.3, 15 | L, so 30 | L.
- **Exact versus renaming is consistent.** The patterns are role-level (renaming-invariant), and a closed raw cycle gives a closed pattern walk.
- **Dependence.** The 10 rests on Math's hand tables (single reader). The 15 rests on O.3. **The parity lemma is not used.** If correct, it would give 30 independently, which corroborates.
- One observation for §7 item 2: a raw cycle of length 15·(odd) would kill Lemma Γ(2) or Math's tables, **and also** MathTaitGlobal Theorem 2.4's raw-30 corollary.

**(3) N2 ↔ N4.**
- At N2 (S = 02, w = gdbab, m₀ = d, m₂ = g): x₃ has degree 5 with neighbours x₂ (a), x₄ (d), w₂ (b) and w₃ (a). x₄ has degree 5 with neighbours x₃, x₀ (a), w₃ (a) and w₄ (b). So K_G = {x₃, x₄}.
- Flipping every g/d ring letter gives w = dgbab, m₀ = g, m₂ = d, which is N4. N4 is symmetric.
- In a targetless class G(s) is in Q, so it is DL. Its F-cycle has pattern N4, so it lies in Γ₂. Conversely, from Γ₂ the same move reaches N2.
- So Q meets both families, and the two F-cycles are disjoint (disjoint pattern sets), giving |Q| ≥ 60. **CORRECT.**

**Use (four paths).** At N2:
- the only b-neighbour of x₃ is w₂, and the only b-neighbour of x₄ is w₄;
- x₁ has degree 5, with w₀ = g and w₁ = d;
- s and G(s) agree off {x₃, x₄}.

So (i)–(iv) follow from the locks of s and of G(s). (iii) is SS3 (w₂ ∈ K₂) and (iv) is SS4 (w₄ ∈ K₁). **CORRECT**, and the claim that G-closure re-derives them without Lemma SS is right.

## 4. Lemma LC

- F recolours only a/g vertices, so the {b,d}-subgraph is unchanged.
- In F(s), b′ = d and g′ = b, so lock 1′ is the {b,d}-component of x′₁ = x₄. That is K₂(s), which contains x₄ by lock 2.
- This is exactly the accepted pd2 Corollary (ii), stated as vertex sets. It needs only lock 2 of s, not DL of F(s).
- **Mirror.** B recolours a/d only. B(s) has b″ = g and d″ = b, so lock 2″ is the {g,b}-component of x″₁ = x₃, which is K₁(s). **CORRECT.**
- **Consequence.**
  - w′₀ = w₃, w′₁ = w₄, x′₁ = x₄ and x′₃ = x₁.
  - The only K₂-neighbours of x₄ are w₃ and w₄. After F, x₃ and m₄ are a or g, and x₀ is a.
  - So under W34-a, every lock-1′ path leaves x₄ through w₄.
  - At L1(g,a) → M(O4), I recomputed the mirror of O4: (w₀, m₁, w₁) = (g, d, g). **CORRECT.**
- The sentence "no Kempe component can be swapped to exploit a cut" is a remark, not a proved claim.

## 5. Lemma W

**W1.**
- After F, the neighbours of x₄ are x₃ (now a), x₀ (a), w₃ and w₄ (b), and m₄.
- With m₄ = a, a g-neighbour exists iff m₄ ∈ K_F. With m₄ = g, G0 needs m₄ ∈ K₀.
- **CORRECT as stated.**
- **Loose wording.**
  - "If m₄ = a, G0 is harmless" holds only when m₄ ∉ K₀. If m₄ (= a) ∈ K₀, both F and G0 kill.
  - Likewise "if m₄ = g, F is harmless" needs m₄ ∉ K_F.
  - The combined surviving predicates are still exactly m₄ ∈ K_F, resp. m₄ ∈ K₀, because K_F and K₀ are distinct. So no conclusion changes, but §0's "exactly one of F, G0 kills" should read "at least one kills unless …".

**W2.** I rechecked the rotation at x₄, (v, x₃, w₃, m₄, w₄, x₀), the two sector splits, and the rotation at v (sectors {x₂, x₃} | {x₀}). K_F (a/g) avoids C (v, b, d) and contains x₂. **CORRECT.**

**W3.**
- "No lock-2 path enters through w₃" in a targetless class with m₄ = a follows from W1 and W2. The restatement as a cut in K₂ − x₄ is a correct equivalence.
- **GAP: the claimed equivalence of *membership* with the cut.** §0 says the membership "is equivalent to a cut condition on lock 2". §3 defines W34-a as "m₄ ∈ K_F, *equivalently* w₃ is not joined to x₁ in K₂ − x₄", and similarly for W34-g, W23-a and W23-d. W2 proves only membership ⇒ cut.
  - The converse fails in general. If every lock-2 path enters through w₄, then m₄ lies on x₂'s side of C. Nothing forces an {a,g}-path from m₄ to K_F; m₄ may sit in a different {a,g}-component on that side.
  - **Fix.** The targetless requirement is membership (the stronger predicate). The cut is a consequence. Replace "equivalently" by "which implies".
  - §7 item 3's "assert they are equal; a mismatch kills Lemma W2" must become "assert membership ⇒ cut". Cut true with membership false is consistent with W2.

## 6. SS3/SS4 against the corrected Lemma SS hypothesis

The correction requires K_u ∩ N(t) = {u}.

**SS3** has t = x₃ (degree 5), u = w₂ (b), c′ = d, and Y the {b,d}-component of w₂.
- N(x₃) − v = {x₂ (a), x₄ (d), w₂ (b), w₃ (a)}. The hypothesis w₃ = a is essential, and it is stated.
- x₄ ∈ K₂ and Y ≠ K₂, so Y ∩ N(x₃) = {w₂}. The hypothesis holds.
- Y avoids the link, because the only b/d link vertices x₁ and x₄ are in K₂.
- States checked:
  - N2 and N4 (S = 02): w₂ = b and w₃ = a.
  - L2 (gdbab@24) and L4 (dgba·@24): w₂ = b and w₃ = a.
  - At L4, m₂ = d joins Y but is not adjacent to x₃.
- **SS4** is the mirror, at N2, N4, M(L2) and M(L4), with x₄ of degree 5 at S = 02 and S = 30.
- **CORRECT.**

**SA-5.**
- After the L2-swap the link is (a,d,a,g,b) with roles (a,d,g,b). Lock 1′ = {d,g} needs x₃ to have a d-neighbour.
- The candidates are x₄ (now b), w₃ (a) and w₂, which is d iff w₂ ∈ K₂.
- So the L2-swap is an endpoint kill exactly when SS3 fails. This is a one-swap kill that never uses the silent swap, so it is independent of the SS correction.
- "Kills exactly when" is meant in the endpoint sense, as Fellow says.
- **CORRECT.**

## 7. Spot checks outside the named scope

- **G-table entries rechecked:** N2, N4, L2 (the run {w₀, w₁, m₂}; out-case L4(b,g), B-starved), L1(b,g) (out-case L3(b,g), B-starved) and O6 (the three cases; O7 is B-starved). All **CORRECT**.
- **§4.4 automatic AB★ at L1(g,a):** w₄ → m₄ → w₃. **CORRECT.**
- **SA-3 counter-picture: GAP (minor).**
  - As written, z is joined to w₂ only through g-vertices and to w₄ only through d-vertices. That realises (i) and (ii), but not (iii) (a {b,d}-path from w₂) or (iv) (a {b,g}-path from w₄).
  - **Repair.** Give each of w₂ and w₄ both a g-spoke and a d-spoke to z, and make w₀ and w₁ adjacent to z. The picture stays plane.
  - The conclusion (no contradiction from one N2/N4 pair) is plausible, but the realisation in a full triangulation is not shown.

## 8. Not reviewed

- The §3 predicate column (about 60 component checks) and the "18 new predicates across 15 states" count.
- The rest of the G-table: N1(·), N3, L3, L4, O3/O4/O5/O10 and the mirrors.
- §5 C★ and §6 SA-0.
- Math's Γ arrow lists themselves. They were used as cited, and only their slot structure was checked.
