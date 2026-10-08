# What a smallest counterexample to VH∃ must look like

Searcher note for the Proof Navigator, 5 October 2026. This page is a lead. It uses the accepted hand pages and the saved records named below. It generates no graph and runs no census.

Labels: **[hand]** a complete argument written here or on a page cited in the same sentence; **[computed]** a finite check already recorded, with its input named; **[lead]** a suggested consequence, not established; **[open]** not established.

Sources: `longtable/swarm/vh-exists.md`, `longtable/swarm/hole-induction.md`, `longtable/swarm/fan-link.md`, `docs/reports/TriangleSumM3Family.md`, `docs/reports/TriangleSumSymmetryCounterexample.md`, `docs/reports/MathWP19Results.md`, `longtable/WP18-results.md`, `longtable/wp18/analysis-17-1.md` with `analysis-17-1.txt`, `longtable/wp19/counterexample-analysis.md`.

## The object

**[hand]** VH∃ says: for every spherical triangulation \(T\) of minimum degree 5, some degree-5 vertex \(v\) and some legal fan \(\tau\) of two noncrossing chords are such that every proper 4-colouring of \(T-v\) that is proper on those chords reaches a state whose link uses at most 3 colours, by singleton slides and whole-component Kempe swaps. Call such a pair a **good pair**. A **failure** is a triangulation in that class with no good pair.

**[hand]** A **smallest failure** is a failure of least order. The page describes what one must satisfy. It does not assert that one exists.

**[hand]** (`vh-exists.md`, Theorem A, and `hole-induction.md`.) If VH∃ holds, every spherical triangulation is 4-colourable. The degree-3 and degree-4 steps never quote VH∃. From the handshaking identity \(\sum_v(6-\deg v)=12\), every minimum-degree-5 member has order at least 12 and
\[
n_5=12+\sum_{k\ge 7}(k-6)\,n_k,
\]
so \(n_5\ge 12\).

**[hand]** A finite fan-selection length \(m(T)\) means some pair fills every admitted start in finitely many moves, so that pair is good. The triangle-sum graphs below have \(m=3\). They satisfy VH∃.

**[computed]** Kempe-fill at every hole holds on the 118 manifest graphs of orders 12 and 14–20 (`vh-exists.md`). Finite \(m\) holds on orders 12–22, equal to 3 only for 17:1 (`WP18-results.md`). On orders 23–24 every tested graph has \(m\le 2\) except 24:6406, which has \(m=3\), and U∃ holds on orders 21–24 (`MathWP19Results.md`). **[hand]** Finite \(m\) supplies a good pair, and U∃ supplies one by R1 of `vh-exists.md`. This page does not re-run those passes. \(H_2\), of order 31, is a success by the hand argument below.

## Gluing: the fragment that survives

Let \(T\) be a minimum-degree-5 spherical triangulation and let \(F\) be a separating triangle. **[hand]** Write \(T=A\cup B\) with \(A\cap B=F\) and with no edge from \(A\setminus F\) to \(B\setminus F\). Completing either side along \(F\) gives a smaller spherical triangulation. Every vertex of \(A\setminus F\) has the same degree in \(T\) as in \(A\), hence degree at least 5, and likewise for \(B\). For \(f\in F\),
\[
\deg_T(f)=\deg_A(f)+\deg_B(f)-2\ge 5.
\]
An interface vertex has degree 5 in \(T\) exactly when the two side-degrees are 3 and 4. In that case its link meets both sides. **[hand]** At most three degree-5 vertices lie on \(F\), so at least nine degree-5 vertices lie in the open interiors. At least one of them lies in \(A\setminus F\) or in \(B\setminus F\), and the link of that vertex is entirely on its own side.

**[hand]** Call \((v,\tau)\) an **interior witness** for \(A\) relative to \(F\) when \(v\in A\setminus F\), \(\tau\) is legal at \(v\), and every colouring of \(A-v\) proper on \(\tau\) reaches a fill of \(A\) by slides and Kempe swaps whose holes all lie in \(A\setminus F\).

**[hand]** An interior witness for either side is a good pair of \(T\). The argument is the component-restriction lemma of `TriangleSumM3Family.md`, applied at every hole of the path, together with one slide step that lemma does not spell out.

Fix an interior witness \((v,\tau)\) for \(A\), and let \(c\) be a colouring of \(T-v\) proper on \(\tau\). Its restriction \(c_A\) is a colouring of \(A-v\) proper on \(\tau\), because every edge of \(A\) is an edge of \(T\) and the chords of \(\tau\) meet only the link of \(v\), which lies in \(A\). By the witness, \((v,c_A)\) has a filling path in \(A\) with every hole in \(A\setminus F\). Lift that path step by step. The invariant is: the current hole \(h\) lies in \(A\setminus F\), and the colouring of \(T-h\) restricts to the colouring of \(A-h\) at the same step. It holds at the start.

- Kempe swap of a component \(K\) of \((A-h)[a,b]\). The lemma says \(K\) is the restriction of a unique component \(K^+\) of \((T-h)[a,b]\). Swapping \(K^+\) performs the selected swap on \(A\) and may recolour vertices of \(B\). The hole stays at \(h\). The invariant holds for the successor.
- Singleton slide \(h\to u\) with \(u\in A\setminus F\). Since \(h\in A\setminus F\), one has \(N_T(h)=N_A(h)\). A colour unique on the link of \(h\) in \(A\) is unique on the link in \(T\). The slide is legal in \(T\), writes a colour only at \(h\), and leaves \(B\) unchanged. The new hole \(u\) is still interior. The invariant holds.
- At a terminal hole \(h\in A\setminus F\) the link in \(A\) uses at most 3 colours. The same vertices are the link in \(T\).

The lemma, as written, assumes the hole lies in \(A\setminus F\). Each Kempe step above is one application of that statement to the current colouring. The slide step uses only \(N_T(h)=N_A(h)\). Neither step uses minimum degree 5 on \(A\): low degree on a side, if any, sits on \(F\).

**[hand]** (`TriangleSumM3Family.md`.) The same lemma is why a pure Kempe path at a hole off \(F\) lifts, and why the family's upper bound is of this form. The family's lower bound, that \(m\ge 3\) survives the glue, uses the short-fill theorem to return to pure swaps at the original root. That lower bound keeps every pair hard for two moves. It is compatible with a good pair of length 3.

## \(H_2\) satisfies VH∃

**[hand]** (`TriangleSumM3Family.md`, `TriangleSumSymmetryCounterexample.md`.) Let \(Q\) be 17:1, with disjoint facial triangles \(F_-=\{1,2,7\}\) and \(F_+=\{3,4,11\}\), both avoiding vertex 0. The chain \(H_k\) of \(k\) copies has order \(14k+3\) and \(m(H_k)=3\). Thus \(H_2\) has order 31. Its interface is its unique separating triangle, and its automorphism group is trivial. A 4-connected form of the axis-symmetry conjecture is **[open]**.

**[computed]** (`analysis-17-1.txt`.) \(Q\) has degree list \(5^{12}6^{5}\). The degree-6 vertices are 2, 3, 6, 11, 14. So \(F_+\) meets \(Q\) in degrees 6, 5, 6 and \(F_-\) meets \(Q\) in degrees 5, 6, 5.

**[hand]** Any identification of those vertices gives three interface degrees, each at least \(5+5-2=8\), summing to \((6+5+6)+(5+6+5)-6=27\). Every degree-5 vertex of \(H_2\) lies off the interface, in one copy, with its link and its legal fans unchanged. This is the degree hypothesis the family uses.

**[hand]** The family's good pair is vertex 0, fan 1, in the last copy. Both faces avoid vertex 0, and the saved certificate fills all 34 admitted starts by at most three pure Kempe swaps at that same hole. The holes of those paths stay at 0, hence off the interface. The pair is an interior witness. The lift above is the family's upper bound, read as a special case. Therefore VH∃ holds for every \(H_k\), including \(H_2\).

**[hand]** From the printed links in `analysis-17-1.txt`, the link of vertex 0 is \((1,2,3,4,5)\), which meets both faces. Inheritance uses the holes of the path, not a link disjoint from \(F\). A slide from vertex 0 can land on \(F\). The certificate never takes that slide.

**[computed]** (`analysis-17-1.txt`, the recorded shortest fill of the start \(X\) at vertex 7.) That fill is the three Kempe swaps \((K,0,3,0)\), \((K,1,2,1)\), \((K,1,3,1)\). The hole stays at 7.

**[hand]** The link of vertex 7 is \((1,6,14,8,2)\), which misses \(F_+\). One length-3 fill on 17:1 is interior-staying relative to \(F_+\). The certificate covers that one start, proper on \(\tau_1,\tau_3,\tau_4\). A good pair at vertex 7 would require every admitted start at one fan.

**[hand]** If either side has an interior witness, the glue has a good pair. A glued failure therefore has no interior witness at any interior degree-5 vertex. \(H_2\) has such a witness, so the glue of these two copies is a success. An interior-staying filling path remains legal after the lift. Slides from a hole whose link meets \(F\) can land on \(F\), and those moves have no counterpart in the side.

## Where the glue can still break

**[open]** Whether VH∃ on both completed sides implies VH∃ on \(T\).

The interior-witness implication above leaves two gaps.

**[hand]** The component-restriction proof replaces an excursion through the other side by a path of length 0 or 1 along \(F\). That replacement uses all three vertices of the clique. If the hole is the interface vertex \(f\), the remaining interface is an edge, and the third vertex of \(F\) is blank. An excursion whose ends are the two surviving interface vertices need not collapse to that edge when the edge is the wrong colour pair. The written lemma does not apply to a hole on \(F\). A local fill at \(f\) need not be a global fill: \(N_T(f)\) properly contains \(N_A(f)\), and the extra neighbours can carry the missing colour.

**[lead]** This is the whole obstruction to pushing an arbitrary good pair across the glue. A good pair on \(A\) whose every filling path eventually occupies \(F\) gives no interior witness. The lifted object would be a state whose hole has neighbours on both sides. Slides and Kempe swaps from there are moves of \(T\), and the side-\(A\) projection no longer matches them.

**[open]** Whether VH∃ implies an interior witness relative to every facial triangle. The strong form is: on a minimum-degree-5 triangulation, for every facial triangle \(F\), some degree-5 vertex off \(F\) has a legal fan such that every admitted start fills along a path whose holes stay off \(F\).

**[hand]** If that form holds, each minimum-degree-5 side of a glue supplies an interior witness relative to the interface, or itself fails VH∃. A failing side would be a smaller failure. A smallest failure would then have no separating triangle whose two completed sides both have minimum degree 5. One path that avoids \(F\), for one start, is weaker than an interior witness, and does not close this step.

**[lead]** The remaining candidate for a separating triangle inside a smallest failure is a side whose completed triangulation has a vertex of degree 3 or 4. That vertex lies on \(F\). The side is outside the class of VH∃, so it is not a smaller failure. Its interior degree-5 vertices still have unchanged links. By the lift, none of them has an interior witness, or else \(T\) would have a good pair. The degree-3 and degree-4 steps of `hole-induction.md` colour a smaller triangulation. They do not manufacture a filling path for an interior degree-5 deletion of \(T\).

## Four reductions

### 1. Must it be free of separating triangles?

**[hand]** If either side has an interior witness, \(T\) has a good pair. A smallest failure that contains a separating triangle has no interior witness at any interior degree-5 vertex.

**[hand]** \(H_2\) contains a unique separating triangle and has an interior witness, so it is a success. The existence of one separating triangle does not describe a failure.

**[open]** Whether both gaps in the previous section are empty. If they are, a smallest failure has no separating triangle.

**[lead]** That is the reduction worth writing next. It is a statement about paths relative to one triangle. It asks for no enumeration.

### 2. Must it be 4-connected, or stronger?

**[hand]** A separating triangle is a cut of size 3, so a triangulation that has one is not 4-connected. \(H_2\) is not 4-connected, and it satisfies VH∃.

**[open]** The converse: every cut of size 3 in a spherical triangulation is a separating triangle. This page does not contain that argument. "No separating triangle" and "4-connected" become the same question once it is written.

**[open]** Whether a smallest failure is 5-connected, and whether it is internally 6-connected. Both ask about separating cycles longer than 3. Nothing on the cited pages reduces VH∃ across a separating 4-cycle.

**[computed]** 17:1 has no separating triangle (`analysis-17-1.md`). 24:6406 has no separating triangle and degree list \(5^{14}6^{8}7^{2}\) (`counterexample-analysis.md`). Both have finite \(m\), equal to 3, so both satisfy VH∃. Both have a half-turn. They are the saved \(m=3\) graphs in the triangle-free class where the 4-connected symmetry conjecture is still open. Their half-turns are properties of two successes.

**[lead]** If the separating-triangle reduction is filled in, a smallest failure lies in that same triangle-free class. The symmetry conjecture, even if true there, constrains graphs with \(m\ge 3\). A failure is a graph with no good pair at any finite length. Symmetry would be an extra property inside the class, not a substitute for the missing pair.

### 3. What degree list must it have?

**[hand]** The list satisfies the displayed formula for \(n_5\). Interface degrees in a glue of two minimum-degree-5 sides are at least 8. A failure with such a glue would have a vertex of degree at least 8, and would still have to lack interior witnesses. \(H_k\) for \(k\ge 2\) has those degrees and has an interior witness.

**[computed]** The killed statement C3 said that \(m\ge 3\) occurs only for degree lists \(5^{12}6^{n-12}\). 24:6406 kills it: \(m=3\) with two degree-7 vertices. That graph satisfies VH∃. A degree-7 vertex is compatible with a good pair.

**[hand]** In the same note the hand colouring X2 at vertex 4 has chains \(P=3{-}11{-}10{-}18{-}8{-}1{-}6{-}14\) and \(Q=3{-}12{-}22{-}15{-}6{-}5\). The degree-7 vertices are 1 and 21. Then \(P\) meets vertex 1, while \(Q\) uses degrees 6, 5, 5, 5, 6, 5 only. A locked chain in this saved success avoids both degree-7 vertices.

**[open]** Whether a smallest failure can have a vertex of degree \(\ge 7\), and whether it can be the equality case \(n_5=12\) with every other degree equal to 6. The saved successes realise both a \(5\)-\(6\) list (17:1) and a list with 7s (24:6406). Copying either list onto a failure is a lead with no forcing argument.

**[hand]** The 5-regular case of the formula is order 12. **[computed]** The manifest graph 12:0 satisfies the every-hole Kempe-fill recorded in `vh-exists.md`, so that graph has a good pair.

### 4. Must a link type repeat?

**[hand]** (`fan-link.md`.) Up to dihedral symmetry and renaming, a proper 4-colouring of a 5-cycle link is one of two orbits. The orbit of type \((2,2,1)\) uses three colours, so it is already a fill. The orbit of type \((2,1,1,1)\) has its repeated colour on two vertices at cyclic distance 2. One Kempe swap at that hole reaches a 3-colour link exactly when at least one of the two useful pairs separates. In the locked placement both paths are present, and no single swap at that hole fills.

**[hand]** Take a start that never reaches a fill. Its link uses four colours, hence the second orbit, and both paths are present. Otherwise one swap would finish. Lemma 3.2 of `vh-exists.md` makes the slide to the fan apex legal at every start, so that slide's result lies in the same non-filling component.

**[hand]** A failure realises this locked orbit once for every legal fan at every degree-5 vertex: each such pair has at least one start of that type whose whole slide-and-Kempe component misses the fill set. The repeated type forced by the definition is this one orbit, at every legal pair.

**[computed]** 17:1 realises a strong finite version and still has a good pair: every one of its twelve degree-5 vertices is bad for length 2, by two crossing far diagonals, and \(m(17:1)=3\) (`analysis-17-1.md`). Repeating the locked type at every degree-5 vertex is what \(m\ge 3\) looks like on that graph. The fills exist at length 3.

**[open]** Whether a smallest failure must contain two degree-5 vertices with the same link-degree list, in a form that one of them could be deleted. \(H_2\) repeats an entire copy of 17:1 and remains a success, because the repeated copy brings its interior witness with it.

**[lead]** The dipyramid colouring in `fan-link.md` shows that the locked orbit occurs inside the class. It is one start on one graph of order 14. A single locked start is the opening of a bad component. A failure is the demand that every pair has a whole component of that kind.

## What is forced, and what is only asked

Forced, if a smallest failure exists:

- **[hand]** Minimum degree 5, the degree-sum formula, and at least twelve vertices of degree 5.
- **[hand]** Every legal pair carries a locked start of type \((2,1,1,1)\) whose component never fills. The apex slide is legal and stays in that component.
- **[hand]** Across any separating triangle, no interior degree-5 vertex has an interior witness.

Asked, and unanswered:

- **[open]** Can such a triangle occur at all, once sides of minimum degree 5 and sides with an interface degree below 5 are both considered?
- **[open]** Is the failure 4-connected, 5-connected, or internally 6-connected?
- **[open]** Which degree lists survive the formula and the interior-witness constraint?
- **[open]** Must two links share a neighbourhood, beyond the locked orbit already required at every pair?
- **[open]** The 4-connected form of the axis-symmetry conjecture. It lives in the triangle-free class. It is a question about \(m\ge 3\), and the saved graphs in that class satisfy VH∃.

## Feasibility

Feasibility of a finished list of reductions for a smallest failure: **Medium**. The interior-witness lift is a short argument from an accepted lemma, and \(H_2\) sits on the success side of it. The unsettleable part is one named gap in that lemma, the hole on the triangle, together with sides that leave the minimum-degree-5 class only on the interface.

## Next checks

None of these generates a graph or runs a census.

1. **Line-check the lift.** Against the component-restriction paragraph in `TriangleSumM3Family.md`, write one Kempe step and one interior slide with the invariant above, and mark the first sentence that uses the third vertex of \(F\). Input: that paragraph only. Outcome: the interior-witness statement stands as a checked lemma, or the slide step fails in a named line.

2. **Steps of the saved seed paths.** In `longtable/audit/triangle-sum-seed-results.json`, under `upper_bound.certificates`, each of the 34 starts at vertex 0, fan 1, has a `kempe_path`. Those paths were built by `shortest` with Kempe moves only, from a deletion colouring at vertex 0 (`triangle_sum_seed_check.py`). Read the stored steps and record whether each one begins with `K`. A Kempe swap keeps its hole, so a path of such steps from a deletion at vertex 0 stays at vertex 0. Alongside it, the three-swap fill of \(X\) at vertex 7 is already printed in `analysis-17-1.txt`. Outcome: which of these saved paths are interior-staying relative to \(F_+\) and to \(F_-\).

3. **Separating 4-cycles on the two saved triangle-free successes.** Using only the stored rotation of 17:1 (`analysis-17-1.txt`) and the stored rotation of 24:6406 (`counterexample-analysis.md`'s graph record), decide whether either graph has a separating 4-cycle. Outcome: whether those \(m=3\) successes are free of separating 4-cycles. That is the connectivity question one step past the triangle, on graphs already known to satisfy VH∃.
