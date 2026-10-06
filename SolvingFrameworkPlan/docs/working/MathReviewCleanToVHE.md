# Review: from a radius lemma to VH∃ in the core (links L1–L6)

Math independent review worker, 6 October 2026. I did not write any of the reviewed claims. Hand review, line by line. One small exhaustive Python check on the icosahedron (§8); it turned out vacuous and is reported only as a consistency check. No census, no declared experiment, no status change, no other file edited, nothing committed.

Sources: `MathConfinementAttack.md` (Theorem A, Corollary B), `MathCleanVertexAttack.md` (Theorems C, D; not needed by the chain), `MathTraceFourConnAttack.md` (Prop 2.2, §5), `MathConjectureR.md` §1 (radius), `MathRadiusGeometry.md`, `MathPathwaysPAPC.md`, `docs/reports/MathTriangleCarryResearch.md`, `MathFourConnectedResearch.md`, `MathVHCoreAdvance.md`, `MathFixedHoleReview.md`, START-HERE §1 and §6, `longtable/swarm/vh-exists.md`, `hole-induction.md`, and Math's 12:33 message (items 4(b)–(d)).

## Verdict, first

| Link | Verdict |
|---|---|
| L1 Theorem A | **CORRECT** under the VH_C definitions (swaps may recolour φ). It also holds word for word for pure Kempe classes. It is a **DEFINITION MISMATCH** only under a "frozen φ" convention, which VH_C does not use. |
| L2 Corollary B | **CORRECT**. The hypothesis "four-connected / all five fans legal" is **not needed**: the equivalence holds at every degree-5 vertex off φ of every member of 𝒞, reading "every fan" as "every legal fan". |
| L3 finite radius ⇒ clean | **CORRECT**. Pure-swap cleanliness is stronger than mixed cleanliness. Finite radius is enough; a uniform bound is not needed. |
| L4 clean off φ ⇒ φ-good fan | **CORRECT**, and trivial. It uses only the easy direction of Corollary B, not Theorem A. Math's 12:33 item 4(c) ("the radius must be achieved by swaps compatible with φ") is a **DEFINITION MISMATCH**: VH_C restricts holes, not swaps. |
| L5 clean v in every least failure ⇒ VH_C | **CORRECT, conditional on a class hypothesis**. The radius lemma and the counting lemma must hold on four-connected members of 𝒞, which may have one or two degree-4 vertices on φ. The audit/Math Euler lemma is stated for minimum degree 5. I give the repair (§6): at least 7 suitable vertices remain off φ. |
| L6 VH_C ⇒ plain VH∃ | **CORRECT** and elementary. It does not need four-connectivity of a plain failure (12:33 item 4(d), second clause, is irrelevant to this direction). |

End-to-end: **if every four-connected (T,φ) in 𝒞 has a degree-5 vertex v ∉ φ at which every doubly locked state has finite pure Kempe radius, then VH_C holds, hence VH∃, hence 4-colourability.** No link mixes pure and mixed moves in the wrong direction. The only real input missing is the radius/clean-vertex lemma on the relative class (and that is the whole difficulty).

---

## 0. Definitions as actually written in the sources

**Plain (vh-exists.md §1.2–1.3; hole-induction.md).** State (h,c): any vertex h, c a proper 4-colouring of T−h. Moves of M(T): whole-component Kempe swaps of T−h (hole fixed) and singleton slides to **any** neighbour. Fill set F: |c(N(h))| ≤ 3. Starts S(v,τ) = colourings of T−v proper on the two chords of τ, i.e. colourings of T*_τ. VH(v,τ): every start is joined to F in M(T). VH∃(T): some degree-5 v and legal τ satisfy VH(v,τ). **No protected face appears in the plain definitions.**

**VH_C (TriangleCarry lines 7–9; FourConnected §1; VHCoreAdvance "The target").** (T,φ) with φ a facial triangle and every vertex off φ of degree ≥ 5 (φ vertices may have degree 3 or 4; in the four-connected core at most two have degree 4, FourConnected Prop 1). Permitted states have their hole off φ. Permitted moves are whole-component swaps **with no restriction on recolouring φ**, and slides **whose destination is off φ**. A pair (v,τ) is φ-good if v ∉ φ, deg v = 5, τ is legal, and every admitted start is joined to F in the permitted move graph. All three sources say explicitly that swaps may meet φ and change its colours.

**Targetless (TraceFourConn Prop 2.2; FourConnected §4; ConfinementAttack).** A component of the **permitted (mixed, φ-restricted)** move graph that contains no filled state. 𝒯(v) is the set of repeat pairs of targetless states with their hole at v.

**Clean (Corollary B (iii)).** No permitted state at v lies in a targetless component, in the same mixed φ-restricted sense.

**Kempe radius (ConjectureR §1).** For a state s at a fixed degree-5 hole v, r(s) is the least number of whole-component swaps of T−v that reach F. These are **pure swaps, unrestricted, with the hole fixed**. A state is doubly locked (DL) if, with link (α,β,α,γ,δ) and repeat pair {x0,x2}, there are a βγ-path x1~x3 and a βδ-path x1~x4 in T−v. A "targetless Kempe class" is a pure-swap class with no fill. Call v **pure-clean** if every Kempe class of T−v contains a fill; this is KD(v) of vh-exists §4.3.

**Frozen φ (ConjectureR §3, "protected-face check").** Swaps whose component meets φ are forbidden. This is **not** the VH_C definition. It is a stronger, optional restriction.

Answers to the brief's two definition questions:
- "Targetless" and "good" are defined with **slides and swaps (mixed)** in Prop 2.2, Theorem A and Corollary B, and **with φ**: holes stay off φ, slides into φ are forbidden, and swaps are free. "Radius" is defined with **pure swaps**, with the hole fixed and no φ.
- The chain uses only the direction pure ⇒ mixed, which is sound because every pure swap is a permitted move of VH_C and of M(T).

---

## L1. Theorem A (MathConfinementAttack §1)

**Statement.** Let v be a degree-5 vertex. If 𝒯(v) ≠ ∅, then 𝒯(v) contains all five pentagram pairs {xj, xj+2}.

**Definitions used.** Targetless in the permitted mixed graph. Only swaps are used inside the proof, and component closure is used.

**Line-by-line check.**
- *Step 1 (locks).* Unfilled with link (α,β,α,γ,δ). If there is no βγ-path x1~x3, the βγ-component of x1 contains no other link vertex: x0 and x2 are α, x4 is δ, and x3 is excluded by assumption. Swapping it gives (α,γ,α,γ,δ), which is filled, and filled states are not in a targetless component. The same holds for βδ. ✓ This is the standard double lock, and it applies to every state of the component, since all of them are unfilled. ✓
- *Step 2 (two swaps).* P1 (colours β,γ) avoids x0, x2 (α) and x4 (δ). P2 (colours β,δ) avoids x0, x2 and x3 (γ). C2 = v x1 P2 x4 v is a simple closed curve. At v the rotation x0..x4 puts x0 on one side and x2, x3 on the other. An αγ-path from x2 to x0 lies in T−v and could meet C2 only at a vertex coloured β or δ, so no such path exists. Hence the αγ-component K of x2 contains x3 (adjacent, coloured γ) and misses x0, x1 and x4. Swapping K gives (α,β,γ,α,δ), with index 3. Symmetrically, C1 separates x2 from {x0, x4}; the αδ-component of x0 contains x4 and misses x2, x1 and x3; the result is (δ,β,α,γ,α), with index 2. ✓ (The Jordan step needs the planar embedding of T with v present, as in vh-exists §2, d = 4.)
- *Step 3 (orbit).* The results are permitted moves, so they lie in the same component, which is still targetless. Steps of +3 and +2 mod 5 generate Z5. ✓

**Verdict: CORRECT** under VH_C. Remarks:
1. The proof uses only swaps. So the same statement holds for **targetless pure Kempe classes** at v, and also for the plain M(T), where there is no φ.
2. v ∉ φ is not used. Four-connectivity is not used. The degree of the link vertices is not used.
3. **Definition dependence.** If swaps meeting φ were forbidden (frozen φ), K or the αδ-component could contain a φ vertex and Step 2 would be blocked. Under that convention Theorem A is unproved (a GAP at Step 2). VH_C does not use that convention, so the stated theorem stands.

## L2. Corollary B (MathConfinementAttack §2; Prop 2.2 of TraceFourConn)

**Statement.** For v ∉ φ of degree 5 in the four-connected core, the following are equivalent: (i) some fan at v is φ-good; (ii) every fan is φ-good; (iii) v is clean.

**Check.**
- Prop 2.2: τ_i admits an unfilled state iff x_i is a singleton, i.e. x_i is not in the repeat pair (Lemma 3.2 of vh-exists, plus the count of 3 singletons). Targetlessness is a property of the state, independent of the fan. So τ_i is bad iff some targetless state at v has x_i outside its pair, and τ_i is good iff x_i lies in every pair of 𝒯(v). ✓ Filled starts are trivially fine. Unfilled states always have a 4-colour link with one nonadjacent repeated pair. ✓
- (iii) ⇒ (ii): if 𝒯(v) = ∅, every legal fan is good. Trivial. (ii) ⇒ (i): a legal fan exists at every degree-5 vertex (vh-exists Lemma 1.2(c)). (i) ⇒ (iii): if 𝒯(v) ≠ ∅, Theorem A gives the pair {x_{i+1}, x_{i+3}}, which misses x_i, so τ_i is bad for every i. ✓

**Verdict: CORRECT.** The hypothesis "all five fans legal (core)" is **unnecessary**. If only some fans are legal, (i) ⇔ (iii) still holds by the same argument, with "every fan" read as "every legal fan". By L1 remark 1, the pure-swap version also holds: some fan is swap-only good ⇔ every legal fan is swap-only good ⇔ KD(v). This removes the "C_v induced" hypothesis from vh-exists Prop 4.2(b).

**Important for the route.** L3 → L4 → L5 uses only the trivial direction (iii) ⇒ (ii). **The radius route does not depend on Theorem A.** Theorem A is needed only for the converse: that no good fan exists at an unclean vertex, which explains why clean-vertex existence is *necessary*. Math's 12:33 item 4(b) therefore overstates the dependence: the route "bounded radius ⇒ clean ⇒ good fan" is sound even if Theorem A were withdrawn.

## L3. "Every DL state at v has finite Kempe radius" ⇒ v clean

**Statement as I read it.** Let deg v = 5. If every DL state (colouring of T−v) has r(s) < ∞, then v is pure-clean, and hence clean in the VH_C sense for every face φ ∌ v.

**Check.**
- Filled states have r = 0. An unfilled state that is not DL has r = 1, by Step 1 of L1, which needs no targetless hypothesis (ConjectureR §1 gives the same reduction). DL states have r < ∞ by assumption. So every state at v reaches F by pure swaps, and v is pure-clean. ✓
- Pure-clean ⇒ clean (mixed, φ): every swap of T−v is a permitted VH_C move whatever it does to φ. The hole stays at v ∉ φ throughout. So no permitted state at v lies in a component without a fill. ✓
- Only finiteness is needed. A uniform bound (sup r < ∞) plays no role in the logic.

**Verdict: CORRECT.** Hypotheses needed:
- (a) v ∉ φ, so that the states at v are permitted states.
- (b) The lemma must cover **all** colourings of T−v. For one good fan, all colourings admitted by that fan suffice. Covering one Kempe class is not enough.
- (c) If the radius lemma is ever proved with **mixed** moves (slides allowed) rather than pure swaps, this link changes: every slide destination must then be off φ, and the lemma must be stated in the φ-restricted mixed graph. As written (pure swaps), no φ condition arises.

## L4. Clean v ∉ φ ⇒ v has a φ-good fan (protected-face compatibility)

**Check.** Take any legal τ at v; one exists (Lemma 1.2(c)). Let c ∈ S(v,τ).
- If v is pure-clean, a pure swap path from (v,c) reaches F with every hole equal to v ∉ φ. Pure swaps are permitted moves of VH_C, and VH_C allows swaps to recolour φ (TriangleCarry line 7: "Kempe components may meet F and change its colours. The condition restricts holes, not swapped vertices"; FourConnected §1; VHCoreAdvance).
- If v is clean in the mixed φ sense, a path exists in the permitted graph by definition, so all its holes are off φ.

Either way τ is φ-good. ✓

**Verdict: CORRECT, trivially.** No Theorem A and no four-connectivity are needed.

**Correction to Math 12:33 item 4(c).** "The radius must be achieved by swaps compatible with φ" is a **DEFINITION MISMATCH**. VH_C, the triangle reduction and the compiled `VacancyProtectedLift` all allow swaps to recolour φ (VHCoreAdvance: "allowing earlier lifted swaps to recolour the far side"). The ConjectureR frozen-face check tests a stronger, unnecessary property. No φ condition on the swaps is required anywhere in L3–L6.

## L5. A clean v ∉ φ in every least failure of VH_C ⇒ VH_C

**Statement.** Suppose every four-connected (T,φ) ∈ 𝒞 (or just every least-order failure) has a degree-5 vertex v ∉ φ that is clean. Then VH_C holds for all of 𝒞.

**Check.** Let (T,φ) be a least-order failure.
- If T has a separating triangle F, take the closed side A that does not contain the interior of φ, completed by F. Then (A,F) ∈ 𝒞: the vertices of A−F keep their T-neighbourhoods, and they are off φ, so they have degree ≥ 5. A is smaller, so it has an F-good pair. That pair lifts to a φ-good pair of T:
  - Holes stay in A−F, which is off φ.
  - Swaps lift because F is a clique, so each global bichromatic component meets A in a single A-component (`VacancyCliqueLift`, compiled).
  - Interior slides and fills are unchanged.
  - The fan is legal in T.
  This contradicts the choice of (T,φ). (TriangleCarry, accepted.) ✓
- Hence T is four-connected, with order ≥ 12 (VHCoreAdvance 5). By hypothesis there is a clean v ∉ φ of degree 5, and L4 gives a φ-good pair. Contradiction. ✓

**Verdict: CORRECT, conditional on the following hypotheses, which must be checked against whatever lemma is fed in.**
1. **Class.** The four-connected members of 𝒞 are not minimum-degree-5 triangulations. Up to two vertices of φ may have degree 4 (three is excluded by FourConnected Prop 1). The vertices of φ may also lie in the link of v. So the radius lemma (P-A\*) must be proved for holes in this relative class, and its proof must not use global minimum degree 5.
   - A link vertex of degree ≤ 4 is harmless for the conclusion: that hole fills in ≤ 3 pure swaps (VHCoreAdvance 2).
   - A Theorem-H-type proof also needs the outer ring vertices distinct, which four-connectivity gives (RadiusGeometry erratum).
2. **Counting lemma.** The audit/Math Euler lemma (12:33 §2: at least 12 degree-5 vertices with at most one neighbour of degree ≥ 12) is stated for minimum degree 5. Repair [hand, mine]:
   - In the core, Σ(6−d) = 12 with n4 ≤ 2 degree-4 vertices, all on φ. So n5 = 12 − 2n4 + Σ_{d≥7}(d−6).
   - The B-count goes through unchanged: |B| ≤ Σ_{d≥12}(d−6) ≤ n5 − 12 + 2n4.
   - So at least 12 − 2n4 degree-5 vertices have at most one neighbour of degree ≥ 12. At most 3 − n4 of them lie on φ.
   - **At least 9 − n4 ≥ 7 lie off φ.** The conclusion survives, with 7 in place of 9.
3. If the lemma is proved only for least failures, it may use only properties already established for least failures: four-connected, order ≥ 12, the curvature identities, and the boundary-degree-4 facts in VHCoreAdvance 5.

## L6. VH_C ⇒ plain VH∃

**Statement.** VH_C (for all of 𝒞) implies VH∃(T) for every minimum-degree-5 triangulation T.

**Check.** Pick any face φ of T. Then (T,φ) ∈ 𝒞, since all degrees are ≥ 5. VH_C gives a φ-good (v,τ). Compare the two settings:
- The permitted move graph is a subgraph of M(T): it has the same swaps and a subset of the slides.
- F is the same set.
- S(v,τ) is the same set.

So every start of (v,τ) is joined to F in M(T), and VH(v,τ) holds. ✓ VH∃ ⇒ 4-colourability is vh-exists Theorem A, which is accepted.

**Verdict: CORRECT.** Notes:
- If T is four-connected, only the core statement is used. If T has a separating triangle, the induction of L5 passes through the side A, which has degree-4 boundary vertices. So the core statement is needed for the relative class in any case (L5 hypothesis 1).
- The converse (VH∃ ⇒ VH_C) is not proved and is not needed. Four-connectivity of a least *plain* failure (12:33 item 4(d); TraceFourConn §4) is also not needed for this direction.
- TraceFourConn §5 ("★ for triangle φ gives R and hence VH∃") and TriangleCarry ("R implies VH∃") are correct for the same reasons.
- Alternative without VH_C: a pure-clean v in an innermost side A is pure-clean in T, by the clique lift of each swap. This gives the same class requirement.

---

## 7. Summary of what is actually needed

**Sufficient, and all links verified:** for every four-connected (T,φ) ∈ 𝒞 (degree-4 vertices allowed on φ), there is a degree-5 v ∉ φ such that every doubly locked colouring of T−v (or every one admitted by one legal fan) reaches a fill by finitely many whole-component swaps of T−v. These swaps are unrestricted on φ.

**Not needed:**
- Theorem A, and the four-connected half of Corollary B.
- φ-compatible ("frozen") swaps.
- A uniform radius bound.
- Four-connectivity of a plain failure.

**Needed but not yet stated in the right class:**
- The radius lemma P-A\* for the relative class.
- The Euler counting lemma for the relative class (repaired above: ≥ 7 vertices off φ).

## 8. Check [computed, vacuous]

Scratchpad script `frozen.py` (not committed). Icosahedron, hole v = 0, all 480 proper colourings of T−v:
- Pure unrestricted swaps: 1 Kempe class, no targetless class, 240 unfilled states, 0 doubly locked states.
- "Every unfilled state is DL or fills in one swap": 0 mismatches.
- Frozen φ for each of the 15 faces not containing v: 24 classes each, 0 targetless.

Theorem A's hypothesis never occurs here, so this is only a consistency check and says nothing universal.

## 9. Ledger

- [hand] Verdicts L1–L6. L2 does not need four-connectivity. The radius route is independent of Theorem A. The 12:33 item 4(c) definition mismatch. The relative-class repair of the Euler lemma (≥ 9 − n4 ≥ 7 off φ).
- [computed, vacuous] Icosahedron check in §8.
- [open] The radius / clean-vertex lemma itself, on the relative class.
- No other file edited; no status word changed; nothing committed.
