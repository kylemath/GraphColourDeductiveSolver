# WP22 (S2) interfaces: certificate format, census format, definitions

Part of the S2 pre-registration (`WP22-S2-preregistration.md`). Fixed here so that the search code and the independent verifier can be written by separate teams.

## Definitions (shared)

- A **state** is a plane triangulation $T$ (oriented triangles), a vertex $v$ of degree 5, and a proper 4-colouring $c$ of $T-v$ whose link has four colours. **Filled:** the link of $v$ uses at most three colours. **Doubly locked** and the swap $F$: as in `MathConfinementAttack.md` Step 1 and `MathCleanVertexAttack.md` Theorem C (the verifier `explore-vhphi/lead_verify_L.py` shows them in code).
- A **Kempe swap** at the hole $v$: choose two colours and one whole connected component of the bichromatic subgraph of $T-v$ (a single vertex counts as a component, and moving it to a colour absent from its neighbours is a swap) and exchange the two colours on it. States are taken **up to renaming of colours** (canonical form: colours numbered in order of first occurrence over the vertices in increasing label order, $v$ skipped).
- **Kempe class** of $s$: all states reachable by Kempe swaps. **Radius** $r(s)$: the least number of swaps to a filled state; **infinite** if the class contains none. A class is **closed** if breadth-first search exhausts it. A search stopped by the state cap is **capped** (inconclusive).

## Certificate (JSON), for a claimed radius or a claimed targetless class

```
{"faces": [[a,b,c], ...],      // oriented triangles of T, ccw, vertex labels are integers
 "v": 16,                      // the degree-5 hole
 "colouring": {"1": 2, ...},   // colour 0..3 of every vertex except v (string keys)
 "claim": {"radius": 2}        // or {"radius": null, "class_closed_no_filled": true, "class_size": N}
}
```

## Census record (JSON lines), phase S2b

`{"graph": "A_3", "v": 0, "faces_sha256": "...", "state": [c_0,...] (canonical colouring, entry v is -1), "doubly_locked": true, "radius": 2}` for every doubly locked state at every degree-5 hole of `A_3`, `A_4`, `A_5`, with holes taken up to the 5-fold symmetry only if the symmetry is stated and used identically by the verifier.

## The family A_r

Defined in `SolvingFrameworkPlan/docs/working/creative-intel-2026-10-05/a-structure.md` §1 (rings of a 5-fold symmetric stacked antiprism around $v$, with a cap). The audit's independent rebuild of $A_r$ is in `audit/conjecture-L/`. Orders 17, 22, 27 for $r=3,4,5$.

## Regression cases (all must reproduce)

| Case | Source | Expected |
|---|---|---|
| W6 | `l-attack.md` §0 (faces and colours) | start state is doubly locked; radius 2 |
| A_3 centre | `lattack_witness.py` data | infinite-chain colourings: radius 2 or 3 (3 for 2 of 4 tested) |
| T4 | `SolvingFrameworkPlan/docs/working/MathConjectureR.md` (faces; hole $v=4$) | 68 canonical states, 22 filled; radius histogram over all states {0:22, 1:25, 2:15, 3:4, 4:2}; over the 21 doubly locked states {2:15, 3:4, 4:2}; nothing unreached |
| planted | any graph with the target predicate changed to "link uses at most 1 colour" (unreachable) | class closed, no target: the kill logic reports a closed targetless class |

## Revision 2 (6 October, after both teams reported; before any S2 run)

Both teams hit the following gaps; resolved here, identically for every code:
- **Orientation.** Math's T4 face list in `MathConjectureR.md` is not consistently oriented. Codes orient it by traversal before use; a global reversal does not change any radius.
- **`faces_sha256` is informational only.** The search code and the verifier define it differently; no check depends on it.
- **Labelling of $A_r$ in the census.** $v=0$; ring vertex $(i,t)$ is $1+5i+t$ ($i$ the ring index, $t=0..4$); the cap vertex is $5r+1$. Both teams used this; holes are all 12 degree-5 vertices, with no use of symmetry.
- **`class_size`** is the number of canonical states of the Kempe class, including the start state.
- **Cross-check done.** The verifier (written blind to the search code) rechecked all 3,720 census records of the search team's own census code: 0 mismatches.
