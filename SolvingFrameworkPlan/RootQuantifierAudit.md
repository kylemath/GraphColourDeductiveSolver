# Root quantifiers, charge selection, and piecewise ranks

4 October 2026. Math team analytical audit. No repository files changed and no new corpus or feature search ran. This note inspects the existing WP11 declaration, discovery result and indexed tables. The producer report is not independent evidence; its replay status is the parent team's responsibility.

## A concrete obstruction to the simplest charging proof

Let D(T) be the degree-five vertices. Fix one rank w. Call r bad if there is a proper deletion colouring at r with no lower endpoint within two component swaps. Each bad root may have its own witness c_r; those witnesses are not one colouring of T.

Define the negative-curvature budget

    E(T) = sum over vertices v of max(deg(v) - 6, 0).

For a minimum-degree-five spherical triangulation, the proved spherical sparsity inequality 2e + 12 <= 6v gives

    |D(T)| >= 12 + E(T).

This needs only the inequality, not an unproved Euler equality for the abstract spherical carrier.

**Conditional charging lemma.** If there is an injection from Bad_w(T) into

    {(v,j) : deg(v) >= 7 and 1 <= j <= deg(v)-6},

then at least twelve degree-five roots are good. Proof: the codomain has E(T) elements, so |Bad_w(T)| <= E(T); subtract from |D(T)| >= 12+E(T).

The combinatorial conclusion is sound, but its proposed structural hypothesis is **already killed for q, lin, and q+lin** by an existing graph. Order 17, graph 0 has degree list

    [5,5,5,6,5,6,5,6,5,5,6,5,5,6,5,5,5].

Thus it has twelve degree-five vertices, five degree-six vertices and E(T)=0. The published discovery result records:

- q: bad roots 4, 6, 9, 14;
- lin: bad roots 4, 6;
- q+lin: bad roots 4, 6.

In particular, a bad mass root does not require a degree-seven-or-higher vertex anywhere in the graph. A stronger local assertion assigning every bad root to an adjacent high-degree vertex is killed too.

Exact fixture: `wp11-discovery/tables/17-0-r4.json.gz`, graph ASCII SHA256 `1203efa037ee84da877d10d6f94b4d81f4224dab98ffb995de0abb125fb2b3c5`. Root 4's q failure is state 25:

- vertex order `[0,1,2,3,5,6,7,8,9,10,11,12,13,14,15,16]`;
- colouring `[0,1,2,3,2,0,3,1,0,1,0,3,1,2,3,2]`;
- p=1, q=143, lin=31.

Its complete macro-endpoint list is in that existing table. No new enumeration was needed for this audit.

This is not a kill of root selection. Eight roots on this graph are good for q, and ten are good for lin. It kills a particularly clean curvature-capacity explanation of the bad roots.

## The exact missing condition in charge-based selection

Here is a general sufficient condition with the root quantifier in the right place.

For each graph T, construct an isomorphism-equivariant integer charge a_T(v), from T alone. Suppose:

1. the total charge is positive;
2. only degree-five vertices can receive positive charge;
3. every positively charged root is Good_w(T,r).

Then the positive-charge set is a nonempty, equivariant set of uniformly good roots. Choosing any member before examining the deletion colouring gives the existential contact hypothesis. If charge construction and tie-breaking are polynomial, it also gives a polynomial selector.

Proof: positive total charge forces some positive entry; conditions 2 and 3 give a degree-five root good for every deletion colouring. All properties are graph-level; no colouring witnesses at different roots are combined.

The third condition is the missing mathematics. Conservation, isomorphism invariance, nonempty receivers and degree-five membership do not imply it. Calling a receiver 'reducible' without proving that condition merely renames the Gate-D hypothesis. The order-17 fixture above shows why unredistributed curvature +1 on each degree-five vertex is inadequate: it gives positive charge to bad roots too.

This lemma does not require that the entire candidate set be a single orbit or that one vertex be fixed by all automorphisms. Tie-breaking may depend on labels after the set itself has been proved sound. Symmetric graphs prevent a deterministic equivariant singleton selector, not a sound equivariant set.

A useful next mathematical target is consequently a **graph-only, charge-receiving condition with a hand proof of universal descent at every receiver**. A radius-two condition may be sufficient without being a complete classification, but it must be stated independently of the colouring witnesses and survive the known bad-root fixtures.

## Piecewise rank closure: one valid lemma and one invalid inference

Fix ONE root, a finite family of nonnegative integer potentials f_i, a target predicate p=0, and the legal macro relation. Set F(c)=min_i f_i(c), and use lex(p,F).

**Lower-envelope descent lemma.** Suppose every non-target colouring c has an index i attaining the current minimum F(c), and a legal macro to c' such that either c' is a target or f_i(c')<f_i(c). Then lex(p,F) strictly decreases: in the non-target case,

    F(c') <= f_i(c') < f_i(c) = F(c).

Bounded polynomial potentials therefore yield a polynomial number of macros, conditional on this active-minimum coverage lemma and an efficient legal-macro search. Switching which index is active at the next state is harmless because F is one fixed state function.

But the following weaker statement does NOT imply that lemma:

    for every c, some potential admits a decreasing macro.

Counterexample to the inference: two non-target states a,b joined by an involutive move, with an unreachable target z. Let f(a)=0, f(b)=1 and g(a)=1, g(b)=0. At a, g decreases on the move to b; at b, f decreases on the move to a. Choosing a currently convenient potential cycles. The lower envelope is zero at both states, so it never decreases. Targets can be assigned zero under both potentials without changing the example.

Likewise, separately available decreasing moves for f and g need not be the same move, so their sum, maximum, or a lexicographic pair is not automatically a rank. For a maximum envelope, a sufficient endpoint condition is that one macro lowers **every** f_i below the old maximum; merely lowering one active feature is insufficient.

These are logical lemmas, not a new feature search or a proof that a particular envelope works on Kempe states. A piecewise rank remains viable only if its branch rule and coverage are proved. It must not be presented as closing the original q hypothesis.

## What WP11's root/rank facts do and do not imply

For a fixed graph T, the report's 'no root is bad under every vector' says

    for every r, some registry vector w satisfies Good_w(T,r).

Good_w contains the universal colouring quantifier. Thus w can be fixed before colouring c, on this finite discovery domain. That is stronger than the statewise statement 'for every c there exists a convenient w', and the two must not be confused.

It still does NOT produce:

- one fixed registry vector good at every root of every graph;
- a polynomial method for choosing w or r from T;
- lower-envelope coverage;
- descent for the original mass q;
- a theorem outside this finite discovery domain.

A graph-dependent finite portfolio target could be written

    for every T, there exist r and w in fixed finite W,
      for every proper deletion colouring c, macro descent holds for rank_w.

Its contact assembly and bounded-rank argument are straightforward conditional extensions of the existing single-rank contact theorem. Its root/rank existence premise and polynomial selector remain new open obligations. WP11 may provide candidate witnesses, not either proof.

The discovery tables give a sharp reason to keep graph-level choices separate. At order17 graph0, roots 4 and 6 are good under 2L+hubToggles, unlike q and lin. But that same 2L+hubToggles vector has **every** root bad on order17 graph1. Repairing a root by switching rank is not a uniform selector or a uniform rank.

## A coherent change-root lemma, and its smallest named obstruction

A root-changing certificate can avoid treating unrelated witnesses c_r as one global colouring, but only by carrying an actual transition.

**Vacancy slide lemma.** Let c be a proper colouring of G-r. Suppose x is a neighbour of r whose colour occurs exactly once on N(r). Uncolour x, colour r with the old colour of x, and retain all other colours. The result is a proper colouring of G-x.

Proof: old edges not incident to r retain their colours and remain proper. Every surviving edge incident to r has a neighbour other than x, whose old colour differs from c(x) by unique boundary occurrence. All edges incident to x disappear in the new deletion graph. This uses no spherical hypothesis.

For a degree-five non-target boundary, the multiplicities are (2,1,1,1), so there are three possible singleton slides. This is a coherent transition between root carriers; it does not identify Kempe components of different deletion graphs and does not combine separate witnesses.

However, slides are reversible: in the new colouring, r is the only neighbour of x with the colour formerly at x, because the old properness at x excludes that colour at every other neighbour. Hence vacancy sliding alone supplies no progress measure.

More importantly, the exact q trap above kills the premise that a degree-five vacancy can always slide immediately to a degree-five vacancy. At graph17/0, root4, state25:

- cyclic boundary vertices: [0,3,10,11,5];
- their colours: [0,3,1,0,2];
- their degrees: [5,6,6,5,6].

The only degree-five neighbours, 0 and 11, have the repeated colour. All three unique-colour neighbours have degree six. Thus every direct legal singleton vacancy slide exits the degree-five root class. This is an obstruction to that simple restricted move rule, not to a combined root-moving/Kempe proof. A prospective certificate must allow higher-degree vacancies, or prove a Kempe preparation that changes this situation, and must carry a globally decreasing measure on the actual (vacant root, partial colouring) state.

A certificate described only as 'there exists a future extendible root colouring' is the theorem in disguise. Useful data would name a checkable state predicate, the permitted root/Kempe transitions, a rank and a preservation proof before claiming that induction produces it.

## A report wording correction

The discovery prose says the minimum of two bad roots includes 'q + lin'. The exact vector [1,1,0,0,0,0,0,0] in results.json instead has FOUR bad roots: 17/0 roots4,6 and 17/3 roots3,13. Lin alone has two. This does not invalidate the indexed certificates or the independent replay of JSON; it is a prose discrepancy to correct. This audit used the exact registered vector and published JSON, not the informal shorthand.

## Recommendation

Do not formalize a charge selector yet and do not add a new rank experiment from this note. Finish the independent replay and the declared validation. Then choose one survivor for a structural proof effort with its own quantified contact statement. A useful contribution from the creative team would be a receiver condition that proves universal macro descent, rather than another proof of Euler charge availability.

If a piecewise potential is proposed, require its branch formula and active-minimum (or explicit common-endpoint) coverage lemma up front. If a charging proof is proposed, start it against order17 graph0 before attempting global discharging. These conditions expose the precise open mathematics and avoid combining incompatible colouring witnesses at different roots.
