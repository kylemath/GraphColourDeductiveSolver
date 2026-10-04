# Finite quantified kill-witness search

Plantri 5.8 generated all nonisomorphic simple triangulations of minimum degree five at orders 12 through 20 using `-am5`. Source archive: https://users.cecs.anu.edu.au/~bdm/plantri/plantri58.tar.gz. `search-results.json` records the archive SHA256, each generated input's SHA256, generator summary, full ASCII rotations, and all root results.

For every degree-five root, `search.py` enumerates proper deletion-colourings modulo global colour permutations, all single bichromatic-component swaps, and the full Kempe-connected classes. It checks whether each class contains a colouring with at most three colours on the deleted root's boundary. The proposed reachability kill witness requires **every** degree-five root to have **some** class without such a colouring.

| Order | Triangulations | Degree-five root instances | Colouring orbits checked |
|---|---:|---:|---:|
| 12 | 1 | 12 | 240 |
| 13 | 0 | 0 | 0 |
| 14 | 1 | 12 | 480 |
| 15 | 1 | 12 | 576 |
| 16 | 3 | 38 | 2,388 |
| 17 | 4 | 49 | 3,498 |
| 18 | 12 | 156 | 15,620 |
| 19 | 23 | 306 | 41,021 |
| 20 | 73 | 1,001 | 180,228 |
| **Total** | **118** | **1,586** | **244,051** |

No kill witness was found. More strongly, no tested root had a targetless class: all 1,626 Kempe classes contain a three-colour boundary. Some deletion graphs at orders 18 and 20 have two Kempe classes; connectivity of the full colouring graph is therefore not being assumed. The actual quantified reachability condition, rather than connectivity alone, was checked.

Checks include: symmetry and uniqueness of adjacency entries, no loops, minimum degree five, `m=3n-6`, connectedness, a planar embedding check, and every face of the input rotation having length three. Every enumerated colouring is checked proper. Every legal component-swap result must be present in the enumeration, and transitions must be involutive modulo colour permutation. The targetless-class calculation is cross-checked against a multi-source traversal from all target states.

This is finite computational research evidence. The census does not establish a uniform theorem, a root-selection rule for arbitrary graphs, a structural progress rank, or a polynomial bound. It is not being used as an assumption in Lean or as a configuration-census proof of four-colourability. Generator exhaustiveness relies on Plantri's documented generation method; the experiment is not a formal proof of that generator.
