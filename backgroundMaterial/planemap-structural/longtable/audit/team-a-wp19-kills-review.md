# Team A independent review of the two WP19 P3 counterexample graphs

5 October 2026. Both new interpretations pass independent checking. This is an audit of two named graphs already present in the saved output, not a new census, an additional phase, or a change to the preregistered statements.

Input `wp19/wp19-P3.json` SHA256: `30efe4e37251e62c6666a6756df754380be57af3cfe2412d9ff988e3dc2f0c2a`. This matches the phase digest in the completed Math replay. The graph labels below use the saved zero-based `graph_index` convention.

I used the audit chat's independent graph validator, deletion-colouring enumerator and mixed-move generator from `wp18_independent.py`, not the WP19 producer or certificate checker. The new Team A checker has its own breadth-first search and writes all verification results to `team-a-wp19-kills-check-results.json`.

## Graph 24:6406 kills C1 and C3, with exact m=3

ASCII digest: `47cb6dc88b4225dfafce0bfec21f30265c8865ad54ecc0df8d387212938d136b`.

Independent rotation validation confirms a simple connected sphere triangulation with 24 vertices, 66 edges and 44 triangular faces. The degree distribution is fourteen degree-5 vertices, eight degree-6 vertices and two degree-7 vertices. Its legal fan set contains exactly 70 pairs. I recomputed that set from the rotation, matched every pair and its two absent chords, and verified the C1 certificate covers the complete set exactly once.

For each of the 70 pairs, its supplied start is a proper deletion colouring, has its hole at the declared degree-5 root, and gives different colours to both endpoints of each added fan chord. Thus it is genuinely admitted by that fan. Independent mixed breadth-first search finds no target at depths 0, 1 or 2. The 70 pair certificates use 35 distinct starts; memoization is only across identical complete states on this one graph. These checks prove every legal pair has L>=3, hence m>=3.

The lower-bound certificate alone does not prove exact m=3. For the upper bound I independently enumerated every deletion-colouring orbit at vertex 0, filtered the starts admitted by fan 0, and ran the independent mixed search on every resulting start. The pair has exactly 134 starts with distance histogram:

| Mixed distance | Starts |
|---:|---:|
| 0 | 22 |
| 1 | 81 |
| 2 | 28 |
| 3 | 3 |

Thus L(0,0)=3, proving m<=3. Together with the all-pair lower certificate, m=3 exactly. This agrees with Math's complete replay, which additionally reports 58 legal pairs with L=3 and 12 with L=4.

The original C1 says m(T)<=2 on every graph of order at least 18. This order-24 graph has m=3, so it kills C1. C3 says m(T)>=3 implies all vertices have degree 5 or 6. This same graph satisfies the antecedent and has two degree-7 vertices, so it kills C3. Neither implication relies on a histogram maximum at just one arbitrarily selected pair.

The independently checked pair (0,0) has finite filling distance for every admitted start. Consequently this graph does not refute the existential vacancy hypothesis: that hypothesis is satisfied here by this one pair. The separately reported U_exists=true is a different assertion about Kempe classes of the graph WITH fan chords; the mixed-distance certificate alone should not be advertised as an independent proof of U.

## Graph 24:7228 kills M2, with exact ell=3 and kappa=5

ASCII digest: `a031bc58029463df7662cfeafb89aba76915f4706c13cebd29e89fefadfb6cde`.

The certificate uses hole 17, fan 0, with added chords (7,23) and (7,18). I independently checked graph validity, legality of the fan and properness of the complete published start:

    [0,1,2,3,1,2,0,3,2,3,1,2,3,0,3,2,1,4,1,0,2,1,3,0]

Here 4 marks the unique hole. The fan apex 7 has colour 3, while endpoints 23 and 18 have colours 0 and 1, so both fan chords are bichromatic. The reported mixed path is legal and reaches a target:

    S(8), K(1,2,seed=1), K(0,1,seed=0).

Component seeds and colour pairs are interpreted in the canonical state after each preceding move. The independent search excludes mixed targets through depth 2 and finds this target at depth 3. Its complete non-target breadth-first layer sizes at depths 0,1,2 are 1,7,27. Therefore ell=3 exactly.

The compact producer kill object deliberately records only `kappa_lower=5`. That alone excludes depths 0 through 4; it is not by itself a five-step upper certificate. Team A independently ran the Kempe-only search through depth 5 at the original hole. The complete non-target layer sizes at depths 0,1,2,3,4 are 1,4,8,10,13. It finds and replays this five-swap target path:

    K(1,2,seed=1), K(0,2,seed=0), K(0,3,seed=0),
    K(2,3,seed=2), K(0,3,seed=0).

Thus kappa=5 exactly. This independently upgrades the compact kill's lower bound to the exact distance stated in Math's full replay.

M2 says kappa<=ell+1. Here 5>3+1, so it is false. Even the original lower-only certificate is sufficient to kill M2, because a recorded three-move mixed path gives ell<=3 and exclusion of all four-or-fewer Kempe fills gives kappa>=5. Exactness is stronger information, not a necessary extra premise for the kill.

This case does not touch M3, whose antecedent is ell=2. It does not refute a mixed bound of four moves, because ell=3. It also does not refute VH: this start has a finite three-move mixed fill and a finite five-swap fixed-hole fill. The graph has a separately reported best-pair value m=1; the difficult individual start at (17,0) should not be confused with the minimum over all pairs. Math's independent full replay reports U_exists=true, and this certificate supplies no locked whole fan-Kempe class that would contradict U.

## Scope

These are three killed preregistered conjectures on two graphs: C1/C3 on 24:6406, M2 on 24:7228. They are not a refutation of the unbounded existential vacancy hypothesis, the unlocking existence condition U, or a proof of a revised universal move bound. The exact-distance statements above are independently reconstructed from the named existing graphs; broader phase totals remain the remit of Math's completed full replay.
