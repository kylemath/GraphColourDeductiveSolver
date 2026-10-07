# The quarter floor at a degree-5 hole: final statement for the paper

Math lead, 6 October 2026. This is the version Long Table should use for the paper section. Each item carries its label. Sources: Math's `MathQuarterFloorLemmaA.md` and `MathQuarterFloorBijections.md`; local compute and local intel messages 1753, 1805, 1811, 1827, 1848, 1855, 1901, 1920, 1925 (commits c24d895, 0c0e098, 8ab6f1d, 2163e02, 9c1e03c, 707840b, 534dfb2, 3a346c8, ba90dfd). Long Table should copy numbers from those messages, not from this summary, and cite them.

## Definitions

- **Setting.** T is a triangulation of the sphere, v a vertex of degree 5 with link x₀..x₄ in rotation order, and indices are taken mod 5. A state is a proper 4-colouring of T − v. A Kempe class is a class of states under whole-component Kempe swaps of T − v.
  - Every state uses all four colours, so stabilisers under renaming are trivial and each class is a union of free S₄-orbits. **Every ratio below is the same in labelled colourings and in colourings up to renaming.**
- **Filled states.** The link uses 3 colours, with the singleton colour at position i. F_i is the set of filled states with singleton at i, and F = Σ_i |F_i|.
- **Unfilled states.** The link uses 4 colours, with the repeat pair {j, j+2}. U_j is the set of such states, and U = Σ_j |U_j|.
  - Write m = x_{j+1} (colour μ), a = x_{j+3} (colour A) and b = x_{j+4} (colour B).
  - **Lock 1** holds when m and a lie in one {μ, A}-component. **Lock 2** holds when m and b lie in one {μ, B}-component.
  - D_j ⊆ U_j is the set of **doubly locked (DL)** states. An unfilled state that is not DL fills in one swap [hand, L3].

## Proved results

**Lemma A [hand; audited: correct per j].** In every Kempe class and for every j,

  |U_j ∖ D_j| ≤ |F_{j+3}| + |F_{j+4}|.

The map is Kempe's single swap, made injective for each j:
- if lock 1 fails, swap the {μ, A}-component of x_{j+3};
- otherwise swap the {μ, B}-component of x_{j+4}.

The map is at most 2-to-1 over all j, which gives Σ_j |U_j ∖ D_j| ≤ 2F. The 2-to-1 case occurs: local compute found 81,571 filled states with exactly two preimages, always from different j, and never more than two. Intern C's order-17 example is gentri 17 #3.

**Class identity [hand, MathQuarterFloorBijections.md §2–§3; reviewed by interns B (7ba6411) and C (4fac326), no error, wording fixed; not yet by the audit; verified with 0 mismatches on all 46,488 degree-5 classes, orders 12–23 plus the order-24 floor holes, and on all 232,440 (class, j) cases].**
- Join each unfilled state to its image under the rotation R₊₃: the swap of the {α, A}-component of x_{j+2}, which is defined exactly when lock 2 holds.
- The resulting graph Γ is a disjoint union of paths and cycles, and

  3F − U = 2N₀ + 1.5·L_F + Σ_paths (1 − d(P)) − D_cyc.

  Here N₀ is the number of unfilled states with neither lock, L_F the filled states' long bits, d(P) the number of DL states inside a path P, and D_cyc the number of DL states on cycles.
- **Per-j form:** |DD_j| ≤ room_j, with room_j := L_j + |U_j^ff| + |U_{j+3}^ff| + |E_j| (see the worker's file for the exact terms). This is equivalent to Math's per-j target for the DL states. DD_j is the set of DL states whose rotation is again DL.

**ρ rule [hand; verified].** ρ = φ ∘ R₊₃ maps D_j ∖ DD_j injectively into F_{j+1} in two swaps, avoiding Lemma A's images. In the **floor classes** every term of the identity is zero and ρ is **onto**. This explains their structure: four equal blocks F_i, U_{i+1}, D_{i+4}, U_{i+2}.

## The conjecture

> **Quarter-floor conjecture (strong per-j form).** At every degree-5 vertex v of every triangulation T, and for every Kempe class of T − v and every j,
>   |DD_j| ≤ L_j + |U_j^ff| + |U_{j+3}^ff| + |E_j|.
> Equivalently, given Lemma A and the identity, U_j ≤ F_{j+1} + F_{j+3} + F_{j+4}. Summed over j, every Kempe class of T − v has **at least a quarter of its states filled**.

**Strength.** The conjecture is **at least as strong as R\* at every degree-5 vertex**, hence as the Four Colour Theorem, via the minimal-counterexample frame. It is presented as a well-tested conjecture with an exact identity behind it, **not as a proof target**.

## Data (computed, exploratory; post hoc in the sense that the statement was found from data)

| Test | Scope | Result |
|---|---|---|
| Floor | degree-5 holes, orders 12–24: 156,033 holes, 160,979 classes | no class below 1/4; 419 at exactly 1/4 (sizes 4 to 384); nothing strictly between 1/4 and 16/59 |
| Degree control | degree 6 and 7 holes | floor fails: 1/8 at degree 6, 2/17 at degree 7 (a degree-5 phenomenon) |
| Block structure | 419 floor classes | 405 split into 4 equal link-pattern blocks; all 419 have U_j = F_{j+1} + F_{j+3} + F_{j+4} with equality for every j |
| Per-j inequality | all classes, orders 12–23 | holds in every (class, j), with equality occurring |
| Adversarial search | 95,884 core graphs seeded from A_5–A_7, K3, HoG 1152 | no class below 1/4; maximum per-j excess 0 (attained at HoG 1152, hole 16); all-DL rotation cycles up to length 880 exist (flipped A_7), in classes 37–42 % filled |
| DL distance to filled | orders 12–23 | 2 / 3 / 4 / 5 swaps for 1,634,586 / 19,925 / 700 / 2 states |
| Local injection, per j (minimal Kempe radius k_min) | orders 16–24, maximum by order | 2, 5, 4, 3, 5, 6, 6, 6, **7** (the 7 is at gentri 24 #1460, hole 19, j = 4, independently recomputed); 98.6 % matched by k = 3 at order 23; tight cases need k ≤ 3 at order 24 |
| Local injection, pooled over j | orders 16–24, maximum by order | 2, 4, 3, 3, 4, 5, 5, 5, **6** |

**Reading.** The matching radius grows slowly with order, per j and pooled alike, so **no local charging scheme of fixed radius is supported**. The line is **closed** (Math messages 2b46322 and ab4fc92). The inequality is genuinely global, which is consistent with its 4CT strength.

## Killed along the way (for the record)

- "One word with four non-crossing matching combinations" as the source of the factor 4 (Math's own candidate, withdrawn).
- "Block-mates agree outside the 1-ball."
- The floor by local counting alone.
- Per-path charging (Γ-paths have two ends, but DL chains reach length 31 and DL cycles have no ends).
- Per-j fixed-radius charging.
- Pooled fixed-radius charging.
