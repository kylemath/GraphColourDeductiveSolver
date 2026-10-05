# Team A adversarial review: exact mixed distance at most two, arbitrary degree

5 October 2026. Mathematical review of the candidate WP19 M3 statement. This does not amend the running experiment, its declaration, or its result interpretation. No graph census or new computational search was run.

## Verdict

The candidate is sound, with one small connectivity premise made explicit below. In fact the argument proves this graph-theoretic statement, without needing planarity or triangulation:

Let G be a finite simple graph with a proper colouring of G-h using a fixed finite palette. A slide transfers a neighbour's colour onto the hole when that colour appears exactly once among the hole's neighbours. A Kempe move swaps one whole component of the two-colour induced graph in the current deletion. Let ell be the minimum mixed-move distance to a hole whose neighbour colours omit a palette colour, allowing the hole to move. Let kappa be the minimum Kempe-only distance to such a target at the original hole h. If ell is 0, 1, or 2, then kappa=ell.

The sharpened proof does not bound the number of components: it swaps the original component containing u. No restriction on original or intermediate degree, palette size, planarity, or triangulation is needed. The original four-colour degree-five M3 claim is a corollary. Colour labels may be globally canonicalized in implementations: lift any canonical path to actual colour labels before applying the proof. The reasoning is invariant under consistent global permutations.

## Terminal-slide elimination

Suppose a hole z has a nonfillable link and a legal slide z->w, transferring colour alpha. After this slide the hole w is fillable, with missing colour x. Since z is now coloured alpha and adjacent to w, x is not alpha. Before the slide, properness excludes alpha from every coloured neighbour of w. Also x was absent from those neighbours: the slide changes no such colour except it adds alpha at z. Hence w is a singleton whole component of the {alpha,x} induced graph in G-z.

Swap that component, recolouring w from alpha to x. Because alpha occurred only at w on the original link of z, the new link of z omits alpha. This reaches a target at z with one Kempe swap. If the starting link of z was already fillable, the distance was zero and no elimination is needed.

This argument uses neither degree(z)=5 nor degree(w)=5.

## The four exact-two move types

KK already gives kappa<=2. In KS, the first Kempe move cannot have reached a target, by ell=2. Replace its terminal slide by the terminal-slide lemma. The resulting two Kempe moves fill at the original hole h.

In SS, the intermediate hole cannot already be fillable, by ell=2. Replace the second slide with the terminal-slide lemma, giving an SK path of length two. Its first slide and its original starting state are unchanged. It therefore suffices to check SK. After the sharpening below, an exact-two SK path must have its slide colour outside the swapped pair.

## SK in actual colour labels

Let h->u transfer the unique link colour sigma. The intermediate deletion is G-u, with h coloured sigma. Let the following Kempe swap use pair P on whole component K, and let x be any colour missing from the final link of u.

### sigma is outside P

Both the original u and the intermediate h carry sigma, so neither belongs to the induced P graph. The induced P graph, and component K, are identical before and after the slide. Commute the Kempe move before the slide. The slide remains legal because all sigma colours are unchanged. Apply terminal-slide elimination to replace this final slide by a second Kempe move at h. Thus kappa<=2.

### P={sigma,rho}, x outside P

No x colour changes during the Kempe swap. Since x is missing at the final hole u, it was absent from the originally coloured neighbours of u. Properness already excludes sigma from those neighbours. Thus u was a singleton {sigma,x} component in G-h, and recolouring u to x removes the unique sigma from the original link of h. That would give a one-Kempe target, contradicting ell=2. This branch is impossible for an exact-two start.

### P={sigma,rho}, h not in K

The final colour of h is sigma, so x cannot be sigma; the preceding case excludes x outside P. Therefore x=rho. Every original rho-neighbour of u belongs to K, because otherwise it would retain rho and prevent rho from being missing at u after the swap.

There is a small connectivity detail to state explicitly. If u has no original rho-neighbour, then u itself is a singleton {sigma,rho} component in G-h and swapping it already removes sigma from the link of h. Exact ell=2 excludes that case. Hence u has at least one original rho-neighbour, and it lies in K.

Since h is outside K, no vertex of K of colour rho is adjacent to h (otherwise the intermediate sigma at h would connect to K). Removing h does not split K, and adjoining u connects to K through the nonempty set of rho-neighbours just established. All rho-neighbours of u are in K; no sigma-neighbour of u existed by properness. Therefore K union {u} is one whole component in G-h. Swapping it removes sigma from the original link of h: u changes sigma->rho; no other original neighbour of h carried sigma; and K contains no rho-neighbour of h that could become sigma. This is again a one-Kempe target, contradicting ell=2.

### P={sigma,rho}, h in K

The final colour of h is rho, so x cannot be rho. The outside-pair case was excluded, hence x=sigma. Consequently no original rho-neighbour of u lies in K: any such neighbour would become sigma after the swap, violating the missing-colour condition at u.

Let L=K-{h}. In the original deletion G-h, L is a union of whole {sigma,rho} components. Indeed, the original/intermediate states agree on all vertices except u,h. Edges from K to vertices outside K were absent in the intermediate induced graph. Removing h introduces no new edges. The only possible newly restored connection is through u of colour sigma, and that would require an original rho-neighbour of u in K, which was just excluded.

Every original rho-neighbour of h belongs to L: before the swap it is adjacent to the intermediate sigma at h and therefore belongs to K. Let J be the ORIGINAL whole {sigma,rho} component containing u in G-h. Since u is outside L and L is a union of whole original components, J is disjoint from L. Thus J contains no original rho-neighbour of h.

Swap J in G-h. The unique sigma on the original link of h, at u, changes to rho. No original rho-neighbour of h lies in J, so no such vertex becomes sigma. No other original neighbour of h had sigma, by legality of the first slide. Consequently sigma disappears from the link of h: one Kempe swap already fills at h, contradicting exact ell=2.

This is stronger than the earlier component-count argument. It excludes the entire noncommuting same-pair SK branch, without needing degree(h)=5 or counting how many neighbours have rho. The original u-component, not the possibly numerous components in K-{h}, is the right witness.

## Exactness and practical limits

Mixed moves include every Kempe-only move, so ell<=kappa. The cases above give kappa<=2 when ell=2, hence kappa=2. When ell=1, a one-Kempe move is already such a witness, or a one-slide witness can be eliminated by the terminal-slide lemma; ell=0 is immediate.

No hypothesis about canonical orbit representatives, ignored global colour renamings, or triangulation edges is hiding in the component argument. In a quotient implementation, the component must still mean an actual whole component before canonicalization. Global relabellings alone cannot change fillability, so omitting their redundant moves does not change the conclusion.

This does not establish equality at mixed distance three or more. Nor does it imply a global two-move bound for all starts. The completed arbitrary-degree exact-two statement is a mathematical theorem separate from a running experimental declaration; any change in experimental interpretation should be versioned and reviewed explicitly. No empirical fixture or enumeration is used to establish this stronger scope.

## Independent sharpening verdict

I attacked the new J witness through all possible graph differences: reintroducing u, deleting h, and a possible indirect path from u through another component into K-{h}. The induced pair graph changes only at u,h. Removing h can split K but cannot create a boundary edge; reintroducing u creates edges only to original rho-neighbours, and the final missing sigma excludes every such neighbour in K. Hence no direct or indirect path from u to K-{h} is possible. The sharpening is sound. The h-not-in-K connectivity clarification earlier remains necessary for that other branch.
