# Team B: general proof of M3

5 October 2026. Independent hand review of the audit chat's proposed component argument. No new census, no changes to the WP19 declaration or running computation. Verdict: the argument works, including the SK case formerly left open. The result is stronger in scope than the experimental candidate: it does not use planarity, triangulation, fan admissibility, degree 5, or even the restriction to four colours. The audit chat found a sharpening while this review was underway; the original two-component bound was valid but unnecessary.

## Statement and conventions

Let G be a finite simple graph, h any vertex, and c a proper colouring of G-h with colours in any finite palette C. A target is a deletion colouring whose current hole has a neighbour link omitting a colour in C. A slide h→u transfers c(u) onto h and deletes u, and is permitted when c(u) occurs exactly once on the full neighbour link of h. A Kempe move swaps one whole connected component induced by a pair of colours in the current deletion graph; singleton components are permitted.

Write ell for the minimum number of mixed moves (slides or Kempe moves) to a target, and kappa for the minimum number of Kempe moves to a target at the original hole h. Then

    ell <= 2 implies kappa = ell.

In particular, exact mixed distance 2 implies exact pure Kempe distance 2 (M3). We prove the stronger constructive assertion that any mixed path of at most two moves to a target can be replaced by at most two Kempe moves at h. No degree bound is used at any stage. The four-colour degree-5 statement is a special case.

## Terminal-slide lemma

Suppose a slide from hole z to neighbour w transfers colour gamma and ends at a target. Let x be a missing colour on the new hole w. The newly coloured vertex z is adjacent to w and has colour gamma, so x!=gamma. In the old deletion G-z, w has colour gamma, no gamma-coloured neighbour by properness, and no x-coloured neighbour: all these old neighbours still occur with unchanged colours in the target link at w. Thus {w} is a whole {gamma,x} Kempe component in G-z. Swap that singleton to recolour w from gamma to x. The colour gamma was unique on the old link of z, so this move removes gamma from that link and produces a target at z.

This lemma uses full neighbour links and requires neither a degree bound nor a triangulation.

## Reducing KK, KS and SS

If the original start or an intermediate state is already a target, use zero or one move and the terminal-slide lemma if needed. Otherwise the starting link uses every colour in C.

KK is already a two-Kempe path. For KS, eliminate its terminal slide to obtain KK, at the original hole. For SS, eliminate its terminal slide in the intermediate deletion graph to obtain SK, with the same first slide and original start. It therefore suffices to convert any SK target path from a non-target start.

## SK notation

Let the first slide be h→u, transferring sigma=c(u), which is the unique sigma on the original h-link. Let d be the resulting proper colouring of G-u:

    d(h)=sigma, and d(v)=c(v) for v outside {h,u}.

The second move swaps a component K for the colour pair P in G-u. Let e be the resulting target colouring, and choose any colour x omitted on the e-link of u.

### Pair P avoids sigma

Both u in the original deletion and h in the intermediate deletion have colour sigma and are therefore absent from the P-induced graph. Consequently the P-induced graphs before and after the slide are identical, and K is the same whole component in G-h. Swap K first. The original slide remains legal since sigma colours are unchanged. The same final target is reached. Eliminate the now-terminal slide to obtain a second Kempe move at h.

### Pair P={sigma,rho}; omitted x is outside P

The swap does not change occurrences of x. Hence x is absent from the original neighbours of u in G-h. Properness excludes sigma on those neighbours as well. Recolour the singleton {u} from sigma to x by a Kempe move. This removes the unique sigma from the original h-link and yields a target after one swap.

The remaining cases have x in P. The position of h determines which one is possible, because h is a neighbour of u.

### h is not in K

Here e(h)=sigma, so x!=sigma and therefore x=rho. Every original rho-neighbour of u belongs to K: otherwise it remains rho in e and contradicts the absence of rho on u's target link. There are no original sigma-neighbours of u by properness. If u has no original rho-neighbour, {u} is already a whole {sigma,rho} component in G-h: properness also excludes sigma-neighbours of u. Swap that singleton to change u from sigma to rho. Since sigma was unique on the original h-link, this alone gives a one-swap target.

Otherwise u has at least one original rho-neighbour. Since h is outside K, removing h preserves K as a connected component until u is added. Adding u connects precisely to its original rho-neighbours, all in K, and at least one such attachment exists. Thus K∪{u} is one whole connected {sigma,rho} component in G-h.

Every original rho-neighbour of h lies outside K: in G-u it is adjacent to the sigma-coloured h, so membership in K would imply h is also in K. The only original sigma-neighbour of h is u. Swapping K∪{u} changes u to rho, introduces no sigma at any other neighbour of h, and removes sigma from the original h-link. This gives a one-swap target.

### h is in K: the sharper one-component escape

Now e(h)=rho, so x!=rho and therefore x=sigma.

1. **No original rho-neighbour of u belongs to K.** Such a vertex would change from rho to sigma and occur on the final link of u, contradicting the omitted colour sigma. Original sigma-neighbours of u do not exist by properness.
2. **K minus h is a union of whole original {sigma,rho} components, disjoint from u.** Removing h may split K. No edge in the induced pair graph joins a remaining piece to a pair vertex outside K, since K was a whole component of G-u. Restoring u creates no attachment to a piece, by step 1. Hence every piece is a whole component in G-h.
3. **Every original rho-neighbour of h lies in K minus h.** These vertices are directly adjacent to sigma-coloured h in the intermediate pair graph, so they belong to K.
4. **Swap the original component J containing u.** By step 2, J is disjoint from K minus h. By step 3, J contains no original rho-neighbour of h. The only original sigma-neighbour of h is u. Swapping J changes u from sigma to rho, while no neighbour of h changes from rho to sigma. Thus sigma disappears from the original h-link, producing a target after one Kempe swap.

This is sharper than swapping all components in K minus h. That earlier construction would need a degree bound to limit their number; swapping J needs no such bound. Both constructions are legal, but J gives the stronger statement.

## Distance conclusion

Every mixed target path of length at most two now has a Kempe-only replacement of length at most two. Mixed moves include all Kempe moves, so ell<=kappa. For ell=0, kappa=0. For ell=1, its sole move is either already Kempe or is eliminated by the terminal-slide lemma, giving kappa<=1. For ell=2, the proof above gives kappa<=2. These bounds force kappa=ell in every case.

The three one-swap subcases in SK cannot occur for a start of exact mixed distance 2; their existence would already show ell<=1. Exactness is not needed to validate the component constructions.

## Sharp scope and limitations

* No assumption on planarity, a triangulation, a fan, or the degree of the hole is used. Any finite colour palette works with the same target definition.
* If the Kempe pair in SK contains the first transferred colour, a target at the end already implies a one-Kempe target at the original hole. Thus an exact mixed-distance-two SK witness must use a pair avoiding that colour and can be commuted and terminal-eliminated.
* SS reduces to SK by terminal-slide elimination, so the separate two-slide missing-colour case split is unnecessary here.
* No claim is made about mixed paths of length three or more. Several intermediate slides can change the component-cut structure substantially.
* The argument changes neither WP19's predeclared hypotheses nor the interpretation of finite computations. M3 can now be proposed as a theorem with this proof for Math's acceptance.
