# One pole-star swap repairs every equal-pole belt deletion

4 October 2026. Internal hand proof. This is not yet a Lean theorem. It does not use a colouring census, shortest-path table, rank lookup, or the Four Colour Theorem.

## Precise family and claim

Let n>=5. Define G_n on two poles a,b and belt vertices u_i,v_i, indexed modulo n. Its edges are:

- a-u_i and b-v_i;
- u_i-u_(i+1) and v_i-v_(i+1);
- u_i-v_i and u_i-v_(i-1).

There is no a-b edge. Each belt vertex has degree five and is adjacent to exactly one pole. This is the two-pole antiprism suspension.

**Pole-star escape theorem.** For every belt vertex h and every proper colouring c:G_n-h→{0,1,2,3} with c(a)=c(b), either h's neighbour boundary already uses at most three colours, or ONE whole-component Kempe swap on G_n-h makes that boundary use at most three colours. Filling h afterward produces a proper four-colouring of G_n.

The swap is explicit: choose a singleton colour on one of the two boundary vertices on the OTHER pole's ring, and switch that colour with the common pole colour on the component containing the other pole.

## Proof

By interchange of the rings and cyclic relabelling, take h=u_0. Its five neighbours are a,u_(-1),u_1,v_(-1),v_0. The two v vertices are adjacent.

Write A=c(a)=c(b). Every coloured belt vertex is adjacent to one of these two A-coloured poles, so NO belt vertex has colour A. Consequently the only A-coloured vertices are a and b.

If the boundary is not already a target, its four belt vertices use all three colours other than A. Four positions using three colours have multiplicities (2,1,1). Since v_(-1) and v_0 are adjacent, their colours differ. They cannot both carry a twice-occurring colour: that would account for all four positions with only two colours. Therefore at least one of them, say z, has a colour B occurring exactly once on the entire five-vertex boundary.

The (A,B)-component containing b is EXACTLY

    {b} union {v_i : c(v_i)=B}.

Indeed b is adjacent to all those vertices. B-coloured vertices have no edges to one another by properness. Each v_i is adjacent to b but not a; and there are no other A-coloured vertices. Thus no edge in the bichromatic graph exits this star, and the a-star is a distinct component.

Swap A and B on this complete component. Properness is preserved by the ordinary component-swap theorem. Among the five boundary vertices, precisely z belongs to the component: a and both u neighbours do not, while the other v boundary vertex has a different colour. Hence z changes from B to A, and no other boundary colour changes. A was already present at a, and B disappears because z was its unique boundary occurrence. The boundary now has at most three colours. Give h the absent colour B. All incident edges are proper and all other edges were already proper.

This proves the theorem. The same argument works for h in the v ring with a and b interchanged.

## The exact abstraction used

The argument needs only:

1. two nonadjacent poles with equal colour A, which are the ONLY A-coloured vertices;
2. every nonpole vertex adjacent to exactly one pole;
3. the vacancy has its own pole plus four belt neighbours, exactly two on each ring;
4. the two other-ring boundary vertices are adjacent.

It does not require rotational symmetry, an automorphism calculation, ring length bounds beyond distinctness, or a global mass formula. It is therefore a sufficient local-global receiver condition, rather than a finite fixture explanation.

## Optional modulo-three classification

The belt is the square of a zigzag cycle of length m=2n. Removing h cuts the distance-one cycle into a path of m-1 coloured belt vertices. As all belt colours are among three colours, every consecutive triple on that path is distinct; therefore its colours repeat with period three.

A remaining wrap edge joins the two vertices immediately on either side of h. If m≡2 mod3, its endpoints would have equal colours, so equal-pole deletion colourings do not exist. If m≡0 mod3, the four belt boundary vertices use only two colours, and the vacancy is already fillable. If m≡1 mod3 (equivalently n≡2 mod3), the boundary is non-target and the one-star argument above applies.

For n=3k+2 the partial colour populations are (2,2k+1,2k+1,2k+1). The chosen other-pole star contains k+1 B-coloured belt vertices. Switching it gives populations (k+2,k+1,2k+1,2k+1), and filling the vacancy with B gives (k+2,k+2,2k+1,2k+1). For G8, k=2, this is exactly the transition from (2,5,5,5) to a completed (4,4,5,5), so the star exchange repairs the conserved-population obstruction which singleton slides cannot change.

## Scope boundary

This is a genuine infinite-family escape statement, but it covers equal-pole colourings only. Arbitrary partial colourings may have differently coloured poles and belt vertices carrying pole colours. Then the purported star can join both poles or spill across rings, and this proof no longer applies.

It gives no uniform global root selector and no general spherical four-colour theorem. The next sharp question is whether differently coloured poles can be brought to equality, OR directly to a target, using a bounded number of vacancy slides plus whole-component swaps, with a named structural progress measure. Pole-deletion Kempe equivalence alone does not establish that conversion for a belt vacancy.
