# Math review: VH∃, diagonals and fill mechanisms

5 October 2026. This chat is Math, as clarified by the user. This review distinguishes conditional deductions, finite checks and unproved universal hypotheses. Source pages remain Long Table's; corrections are reported here rather than silently editing their argument.

## Accepted hand deductions

Theorem A of `longtable/swarm/vh-exists.md`, **VH∃ implies four-colourability**, passes review. The induction is on all simple spherical triangulations, not only minimum-degree-five ones. Degree-three and degree-four reductions produce smaller simple triangulations; the degree-four Jordan curve uses the embedding with the old vertex present. In the degree-five case the existential vertex and legal fan are selected before a colouring, induction supplies a colouring of that smaller fan triangulation, and VH is applied only to the original graph. No inductive call is made on later same-order hole states. This accepts the implication, not its hypothesis.

Legal fan existence, the smaller-graph construction, containment, apex singleton, component and class reformulations, U∃⇒VH∃, fifth-colour interpretation, terminal-slide elimination, one-swap out-and-back simulation and degree-three lifting/extension pass hand review. In particular, containment decomposes one T* bichromatic component into components of the original deletion; swapping them successively is legal because the pair-colour vertex set never changes. Class representatives can therefore be used without assuming that every original start is itself unlocked.

The family-of-inductive-colourings reformulation is equivalent to the chosen-pair hypothesis by finite quantifier negation. It is not a new weaker theorem. Global colour canonicalisation is also harmless: colour transpositions can be implemented by swapping every component on that colour pair.

The candidate U∃ remains open. Its sufficient implication is a swap-only route: move inside the smaller triangulation's class, transfer that sequence to the original deletion, then take the unlocking swap. This class excursion may be long; immediate unlocking at one member does not bound the total length from every start.

## Independently reproduced old class observations

`audit/math_vh_review.py` reconstructs the smaller-graph Kempe classes using only the audit's own enumeration and move code. It checks containment inside original-deletion classes, apex singletons, U at each pair, and the stronger “every class contains an immediate fill” property on the already analysed 118 graphs through order 20. Results are in `math-vh-review-results.json`; orders 19–20 are a spent holdout and remain a secondary reading. The replay passed: 7,930 pairs, 41 U-failing pairs, U∃ on all 118 graphs, 16 graph-level failures of the stronger immediate-fill property, zero containment failures and zero apex-singleton failures. These finite observations are accepted on these inputs; they do not prove U∃.

## Diagonal reduction accepted

At a four-colour degree-five link the repeated colour occupies one diagonal. An admitted fan has its apex away from that diagonal; fill distance depends on the original deletion, not the chosen fan. Hence a fan has worst length at most two exactly when all far diagonals meet its apex. When all five fans are legal, the intersecting-diagonal graph is a pentagon: a pairwise-intersecting collection has a common endpoint unless it contains two disjoint, geometrically crossing diagonals. This proves the stated crossing criterion with its legality condition.

The symmetry lemma applies only to the specified reflected pair of crossing diagonals. It does not explain badness at vertices with trivial stabilisers. The edge-flip observations are not a causal proof.

`audit/math_diagonal_review.py` independently checked all 12 degree-five roots and all 60 fans of named graph 17:1. It also checked the vertex-7 witness: six nontrivial distinct neighbouring states, none with a one-move fill, no fill within two moves, and the explicit three-swap path. The witness has distance exactly three. The script and `math-diagonal-review-results.json` are the independent finite evidence.

## Mechanism lemmas and necessary corrections

Lemma A passes hand review: the two gap chains bring all four colours to the link of any possible singleton-slide destination; outside the gap the usual single Kempe swap fills. Lemmas B and C, and the one-way assertions of E and F, also pass review. Lemma E proves that absence of the interlock permits Kempe's pair; it does not prove that presence of the interlock makes that pair fail.

**A false converse appears in the prose after Lemma F.** The statement that the cascade fails “exactly in configuration X” is false. The independent named counterexample below has both halves of X but Kempe's pair fills:

- Graph: order 17, index 0; hole 0.
- Start in vertex order: `(4,0,1,2,0,3,1,2,3,1,3,1,2,3,0,2,0)`, where 4 is the hole marker.
- Roles `(a0,b,a2,g,d)=(4,5,1,2,3)`, colours `(alpha,beta,gamma,delta)=(0,3,1,2)`.
- C0 is `{4,11,16}`; D2 is `{1,7,12,14,15,16}`. Deleting C0 blocks every beta–gamma path between b and g; deleting D2 blocks every beta–delta path between b and d. Thus full X holds.
- The canonical-state certificate is `K(0,1,seed=4)`, then `K(0,2,seed=1)`. Both are complete components in their respective current deletions, and the resulting link has at most three colours.

`audit/math_mechanism_review.py` checks this counterexample and replays its path independently. On the named old graphs 12:0,14:0,17:0,17:1, Lemma A passes on 1,378 four-colour states and Lemma E's necessity passes on 494 gap states. Among them, 80 have full X and a successful KP_g. These are regression fixtures, not a new graph census. Replace the “exactly” assertion with the proved necessary direction. No WP19 statement or implementation depends on this false converse.

**The two-slide corollary needs one missing argument.** Turning SS into SK by terminal-slide elimination does not by itself show that the swap avoids the first slid colour. The correction is short. Write the slides h→u→t, first transferred colour sigma and second gamma. Let x be missing at the final hole t. If x differs from sigma, the resulting singleton swap at t avoids sigma, so commutation and terminal-slide elimination give KK. If x=sigma, t is not adjacent to h, the original `{sigma,gamma}`-component is exactly `{u,t}`, and swapping it at hole h removes sigma from h's link: there was already a one-swap fill. Thus for starts of exact mixed length two the latter case is impossible. The two-slide case is repairable; the general SK cases remain open as stated, and M3 remains a conjecture.

**Another quantifier overstatement remains near the end of the mechanism note.** A uniform bound for every gap start at every degree-five hole is stronger than a bounded existential-pair version of VH∃, and is not “exactly” that version. It implies a bounded existential hypothesis, while VH∃ itself permits arbitrarily long paths and asks for only one pair per graph. Preserve this distinction.

The previously withdrawn bounded-radius claim stays withdrawn. Identical link colours and degrees do not determine exact length; that does not exclude a common upper bound.

## Status

The conditional proof route and diagonal/one-way mechanism lemmas are accepted within the scopes above. Universal VH∃, U∃ and Conjecture M are unproved. The mechanism page needs the specific prose corrections and the short SS proof completion. None changes the preregistered WP19 tests. WP19 P1/P2 execution and complete replay are recorded separately; no finite pass upgrades these conjectures to theorems.
