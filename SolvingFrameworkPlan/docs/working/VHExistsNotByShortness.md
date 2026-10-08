# Lead: VH∃ does not go by shortness

Proof Navigator searcher, 5 October 2026. No computation was run. The label **[compiled]** is used only for the two theorems already in the module audit. Every other stamped sentence is **[lead]**.

## Verdict

**[lead]** The sentence under test stands. Proving VH∃ by showing that fills are always short is the wrong approach.

VH∃, as written in `backgroundMaterial/planemap-structural/longtable/swarm/vh-exists.md`, asks for one degree-5 vertex and one legal fan on each spherical triangulation of minimum degree 5, chosen before the colourings. Every colouring of the smaller triangulation $T^\ast_\tau$ must then reach a link of at most three colours by some finite sequence of singleton slides and Kempe swaps. The length may depend on the triangulation and on the start. A universal length bound asks for a cap on every start. That is a harder sentence. `longtable/wp18/mechanism.md` records the quantifier gap: a uniform bound on every gap start implies a bounded form of VH∃, and VH∃ itself allows arbitrarily long paths at the one chosen pair.

The concrete caps have died, or they have stopped at the compiled line of length 2. The next lemma has to name a chain or a Kempe class for that one fan, and it has to leave the length uncapped.

## Caps the restart page already records as dead

`SolvingFrameworkPlan/START-HERE.md` records four bounded-length ideas as killed. This lead does not reopen them.

- **Fixed Kempe budgets at a frozen hole.** In `swarm/two-kempe-kill.md` the hole is vertex 1, of degree 9, on a 21-vertex triangulation, and the link has multiplicities $(3,2,2,2)$. One Kempe swap stays frozen. Two population-changing swaps make one colour unique, and a slide then fills. The fill on this colouring is two swaps and one slide. The note rates “slides, at most one Kempe swap, slides, fill”, as a method for every partial colouring, as Low, and it leaves open whether some other colouring has every two-swap exit still frozen.
- **Fitted ranks.** `swarm/rank-kill.md` kills $q$, sorted population, and the pairs of $q$ with the boundary-colour count and with minimum degree. The witnesses include the flat exchange between order-17 graph 0, roots 9 and 14, where a singleton slide preserves the scored tuple. The restart page also records the height, sandpile, flow, and monodromy readings as killed.
- **$m \le 2$.** Order 17, graph 1 has fan-selection length 3 at every legal pair. Order 24, graph 6406 has exact $m = 3$. The restart page also records an infinite triangle-sum family of orders $14k+3$ with $m = 3$.
- **M2, the sentence $\kappa \le \ell + 1$.** Order 24, graph 7228, vertex 17, fan 0, has a start of mixed distance 3 and pure distance 5. The same graph still has a pair of fan-selection length 1, so a hard start at one pair can sit beside an easy pair.

**[lead]** These are deaths of uniform controls. The existential sentence VH∃ is still open. The controls one would have used to prove it by shortness are gone.

## The two compiled theorems

**[compiled]** M3, short fills. In `SimpleGraph.VacancyShortFill`, for an arbitrary simple graph and an initially proper deletion colouring, `short_fill` converts an actual mixed filling path of length $n \le 2$ into a pure Kempe filling path at the original hole of length at most $n$. `optimal_short` equates the two minima when the mixed minimum is at most 2. Planarity, degree, fans, and a four-colour palette are not hypotheses. The statement and the audit are in `SolvingFrameworkPlan/docs/reports/ShortFillLeanReport.md`.

**[compiled]** L3, the three-move shape. In `SimpleGraph.VacancyThreeMoveObstruction`, if a proper deletion start has no pure fill within three swaps, then any target-reaching mixed path of length three starts with a legal singleton slide (`first_is_slide`), and any two-swap finish after that slide has first pair containing the slid colour (`first_pair_contains_slide_colour`). The direct premise is `¬ PureFill G h c 3` together with an actual three-move path. The report `SolvingFrameworkPlan/docs/reports/ThreeMoveLeanReport.md` records that these two theorems give the shape of a strict three-move advantage $\ell = 3 < \kappa$. The conclusion is the first move and the first pair. A bridge face is a separate open sentence, and a bound on any longer path is not a conclusion of L3. The Lean statements do not assume an oracle for distances.

**[lead]** M3 removes the slides from a fill that is already of length at most 2. L3 says what a path must look like the first time a slide is indispensable. Both theorems are about a path that has been supplied. VH∃ is about existence of a path at one chosen pair.

## The note past length 2

`longtable/wp19/beyond-short-fill.md` is a research note. Its constructions are read here as leads.

**[lead]** Example E1 is a planar graph on 7 vertices, with 3 colours, and one start of mixed length 3 whose Kempe class at the original hole never fills. The note extends the same split to any palette size by apex joins, to a non-planar degree-5 hole with 4 colours, and to planar ladders of every order. If those arguments stand, no function of $\ell$ bounds $\kappa$ on arbitrary graphs, and length 2 is the last length at which a slide can always be deleted. M3 stops at 2 for that reason. A later universal cap is not a corollary of M3 and L3.

**[lead]** The vacancy setting is left open in that note: a spherical triangulation, four colours, a degree-5 hole. The note’s reading of the saved WP19 marginals, orders 21–24, has maximum $\kappa = 5$, gap $\kappa - \ell$ at most 2, and no start stored as having no pure fill. The counts are pair-weighted, and they are finite. They match a loose cap, and they are the same record on which $\kappa \le \ell + 1$ failed. The note also says that a proposed cap $\kappa \le 5$ at mixed distance 3 cannot follow from L3 and the local refinement alone, because E1 meets both and has no pure fill.

**[lead]** The note uses the name Lemma L4 for a local refinement of one shortest path of length 3: where the first Kempe component sits relative to the hole, and where a neighbour of the partner colour $\rho$ sits. E1 is recorded as satisfying that refinement. The refinement locates neighbours on a path of length 3. A pure fill is a different conclusion, and the prism start has the neighbours without one.

## Frozen holes, from the swarm notes

These notes are leads.

**[lead]** `swarm/fan-versus-frozen.md`. A frozen link uses all four colours at least twice, so it has at least eight vertices. A degree-5 link has five, so a degree-5 start is never frozen. The published frozen colouring blanks vertex 1, of degree 9. A hole of degree greater than 5 is a later state of a slide sequence if the sequence reaches it. The note supplies the count $8 > 5$ and does not build a path from a fan restriction to this colouring.

**[lead]** `swarm/frozen-patterns.md`. No sorted multiplicity forces an unlocking swap. A word of type $(2,2,2,2)$ can unlock by a separation that uses only the cycle, and another colouring of the same multiplicities can stay frozen. The chordal 9-gon of type $(3,2,2,2)$ stays frozen, and the witness interior is a second frozen extension of a different colouring of that type. The note rates classification by multiplicity as Low. The test it names is the footprint of the boundary chains after every non-crossing join.

**[lead]** `swarm/frozen-link-reasons.md`, on the same 21-vertex link. Six of the sixteen non-global swaps stay frozen on every triangulation that carries this coloured link. They are the pairs that meet the colour of multiplicity 3. The other ten are frozen by this interior. Another colouring of the same interior vertices, with the link held fixed, produces a singleton on pairs drawn from $\{1,2,3\}$. The note rates “this coloured link is frozen under every Kempe swap, for every interior” as Low.

**[lead]** `swarm/third-swap-slides.md`, on that one colouring. After a third swap that creates a singleton, a walk of further singleton slides from the new hole reaches a three-colour link, and the recorded lengths of that walk run from 1 to 7. One triangulation with a slide tail of length 7 decides nothing about all triangulations. It is a reason to keep a tail-length cap out of the next lemma.

## What the next lemma has to say

The lemma after the compiled L3 is the sentence this lead means by L4. Long Table’s note already uses that name for the $\rho$-neighbour refinement above. The two sentences are different. The refinement is a picture of one path of length 3. The lemma that would help VH∃ has to produce a fill at one fan.

**[lead]** L4 has the quantifiers of VH∃, and a reason that produces the fill.

For every spherical triangulation $T$ of minimum degree 5, there exist a degree-5 vertex $v$ and a legal fan $\tau$ such that every colouring of $T^\ast_\tau$ reaches a fill, for this reason. A start that already has a mixed fill of length at most 2 has a pure Kempe fill of that same length, by the compiled short-fill theorem. Every remaining start reaches a fill because the two chords of $\tau$ separate a bichromatic chain that meets the link, in the Jordan sense already used when the degree is 4, or because one legal slide lands in a Kempe class of the new deletion that contains a target. The number of swaps inside that class is whatever the class requires. It is not an argument of the lemma, and it may grow with $T$.

A sentence with the pair inside the colouring quantifier, or with a constant on the path, is a different theorem. The degree-5 step of the induction uses one pair and finiteness.

## Uniform caps stay out of that lemma

**[lead]** L4 contains no uniform length cap. The dead instances are a fixed Kempe budget, a fitted rank, $m \le 2$, and $\kappa \le \ell + 1$. The same exclusion covers $\kappa \le 5$, $\kappa \le 2\ell - 1$, and any function $\kappa \le f(\ell)$ whose $f$ ignores the triangulation. A cap that called on planarity and four colours would still bound every start. VH∃ asks for a finite path at one pair. The route that treats a cap as the proof has no surviving candidate short of the compiled line $n \le 2$, and that line is M3, which deletes slides from paths it is given.

## One structural question

**[lead]** The question to put in place of a length bound is this.

When a link is frozen, which of its bichromatic blocks does the circular word freeze on every interior, and which blocks can a change of interior unlock?

On the 21-vertex link the split is six and ten: the six are the pairs that meet the colour of multiplicity 3, and the ten are an interior fact. Degree-5 starts are never frozen, so the question applies to a later hole, the kind a slide can reach after the fan start. Asked of a frozen link that some degree-5 fan colouring of the same triangulation does reach, it is a question about chains and about the interior. The length of the path is not part of the question. The degree-9 colouring in the swarm notes is a pattern for the split. The fan note does not show that this colouring lies on a path from a fan start, so it is not yet an input to L4.

## Feasibility of a universal length bound

**[lead]** Three ratings, kept separate.

- On arbitrary graphs, feasibility of a single function $f$ with $\kappa \le f(\ell)$ for every start is **Low**. The prism and the ladders are written with mixed length 3 and with no pure fill. They are not compiled. They are enough to make the general function a bad bet. The note leaves open whether $\kappa$ can be finite and arbitrarily large at mixed length 3. An infinite value at $\ell = 3$, if the prism argument stands, already excludes a function bound.
- On 4-coloured spherical triangulations, at degree-5 holes, feasibility of some universal cap is **open**. E1–E4 do not sit in that setting. The saved distances through order 24 are consistent with $\kappa \le 5$ and with $\kappa - \ell \le 2$. They are also the record on which $\kappa \le \ell + 1$ failed. No note searched here gives a mechanism that would force a cap, and none exhibits a triangulation start with no pure fill. Finite agreement through order 24 is not a bound.
- Feasibility of proving VH∃ by any such cap is **Low**. The cap is stronger than the hypothesis the induction uses. The caps that were stated exactly have died, or they have stopped at compiled length 2. The compiled obstruction past that line, L3, is a shape.

## Next step

Write the existential sentence in “What the next lemma has to say”, with the pair outside the colouring quantifier and with no function $f$ in the conclusion. Check the wording against the two compiled theorems: M3 is the case of mixed length at most 2, and L3 is only the shape of a supplied three-move path. Then answer the chain question for one frozen link that a written argument already joins to a degree-5 fan start. Until that join exists, the degree-9 example stays a pattern, and no new length cap is the substitute.
