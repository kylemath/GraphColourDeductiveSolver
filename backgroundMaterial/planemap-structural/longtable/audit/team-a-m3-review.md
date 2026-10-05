# Team A adversarial review: exact mixed distance two at a degree-five hole

5 October 2026. Mathematical review of the candidate WP19 M3 statement. This does not amend the running experiment, its declaration, or its result interpretation. No graph census or new computational search was run.

## Verdict

The candidate is sound, with one small connectivity premise made explicit below. In fact the argument proves this graph-theoretic statement, without needing planarity or triangulation:

Let G be a finite simple graph with a proper four-colouring of G-h and degree(h)=5. A slide transfers a neighbour's colour onto the hole when that colour appears exactly once among the hole's neighbours. A Kempe move swaps one whole component of the two-colour induced graph in the current deletion. Let ell be the minimum mixed-move distance to a hole whose neighbour colours omit one of the four colours, allowing the hole to move. Let kappa be the minimum Kempe-only distance to such a target at the original hole h. If ell is 0, 1, or 2, then kappa=ell.

The degree-five restriction is used only when bounding the number of components in the exceptional SK case. Intermediate holes can have arbitrary degrees. Colour labels may be globally canonicalized in implementations: lift any canonical path to actual colour labels before applying the proof. The reasoning is invariant under consistent global permutations.

## Terminal-slide elimination

Suppose a hole z has a nonfillable link and a legal slide z->w, transferring colour alpha. After this slide the hole w is fillable, with missing colour x. Since z is now coloured alpha and adjacent to w, x is not alpha. Before the slide, properness excludes alpha from every coloured neighbour of w. Also x was absent from those neighbours: the slide changes no such colour except it adds alpha at z. Hence w is a singleton whole component of the {alpha,x} induced graph in G-z.

Swap that component, recolouring w from alpha to x. Because alpha occurred only at w on the original link of z, the new link of z omits alpha. This reaches a target at z with one Kempe swap. If the starting link of z was already fillable, the distance was zero and no elimination is needed.

This argument uses neither degree(z)=5 nor degree(w)=5.

## The four exact-two move types

KK already gives kappa<=2. In KS, the first Kempe move cannot have reached a target, by ell=2. Replace its terminal slide by the terminal-slide lemma. The resulting two Kempe moves fill at the original hole h.

In SS, the intermediate hole cannot already be fillable, by ell=2. Replace the second slide with the terminal-slide lemma, giving an SK path of length two. Its first slide and its original starting state are unchanged. It therefore suffices to check SK.

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

Let C_1,...,C_q be the connected components of K-{h}. In the original deletion G-h these are whole {sigma,rho} components. Indeed, the original/intermediate states agree on all vertices except u,h. Edges from K to vertices outside K were absent in the intermediate induced graph. Removing h introduces no new edges. The only possible newly restored connection is through u of colour sigma, and that would require a rho-neighbour of u in K, which was just excluded.

Every C_j attaches to h in the intermediate induced graph, because K is connected. Such an attachment is through a vertex originally coloured rho. Conversely every original rho-neighbour of h belongs to K, because it is adjacent to the intermediate sigma at h. Therefore q is at most the number of rho-neighbours of h.

The original link of h uses all four colours on five neighbours, with sigma unique at u. Its multiplicities are 2,1,1,1. Thus rho occurs at most twice, and q<=2. Swap C_1,...,C_q in G-h. These components are disjoint; swapping an entire two-colour component leaves the induced two-colour vertex set and its components unchanged, so the swaps remain legal in either order. Every rho on the original link of h becomes sigma; u remains its original sigma, because no C_j connects through u; no original sigma-link vertex other than u exists. Hence rho disappears from the link of h. This gives kappa<=2.

## Exactness and practical limits

Mixed moves include every Kempe-only move, so ell<=kappa. The cases above give kappa<=2 when ell=2, hence kappa=2. When ell=1, a one-Kempe move is already such a witness, or a one-slide witness can be eliminated by the terminal-slide lemma; ell=0 is immediate.

No hypothesis about canonical orbit representatives, ignored global colour renamings, or triangulation edges is hiding in the component argument. In a quotient implementation, the component must still mean an actual whole component before canonicalization. Global relabellings alone cannot change fillability, so omitting their redundant moves does not change the conclusion.

This does not establish equality at mixed distance three or more. At higher original degree, the SK argument only bounds q by the multiplicity of rho on the original link, which can exceed two. Nor does it imply a global two-move bound for all starts. The completed degree-five exact-two statement is a mathematical theorem separate from a running experimental declaration; any change in experimental interpretation should be versioned and reviewed explicitly.
