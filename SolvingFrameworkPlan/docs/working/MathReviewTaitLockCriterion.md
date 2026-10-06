# Math review: Long Table's Tait lock criterion (`pathways/pd2_lock_proof.md`)

Math lead, 6 October 2026. Reviewed by hand, line by line. Nothing was run. The code re-check cited in the source (`pd2_x.py`, 0 mismatches on 3,682 states) was not rerun and is not part of this review.

**Verdict: CORRECT [hand].** The criterion is correct, and so is the corollary that F keeps one lock for free. One wording improvement is noted under Step 2.

## Checks

- **Tait colours.** In Z₂×Z₂, the edges of a properly coloured triangle carry the three nonzero values, one each. The four link colours α, μ, c(a), c(b) are distinct and sum to 0. With β = α+μ, γ = α+c(a), δ = α+c(b), I re-derived:
  - e_j = e_{j+1} = β, e_{j+2} = γ, e_{j+3} = c(a)+c(b) = β, e_{j+4} = δ;
  - μ+c(a) = δ and μ+c(b) = γ.
- **Step 0.**
  - The (β,γ)-subgraph of the dual has degree 2 at every triangle node. At P it has the four edges e_j, e_{j+1}, e_{j+2}, e_{j+3}. So the component through P is two P-to-P paths that meet only at P.
  - Pairing e_{j+2} with e_j would make the two pairs alternate around P (j, j+1, j+2, j+3), forcing a crossing in a plane graph. So Z1 returns by e_{j+1} or e_{j+3}.
  - The same holds for (β,δ): the edges at P are e_j, e_{j+1}, e_{j+3}, e_{j+4}; pairing e_{j+4} with e_{j+1} alternates; so Z2 returns by e_j or e_{j+3}.
- **Step 1 (returns by e_{j+1} ⇒ lock 1).**
  - Assume lock 1 fails, and let K be the {μ, c(a)}-component of a.
  - Every cut edge of K has its outer end coloured α or c(b), so its dual colour lies in {β, γ}.
  - Every triangle meets ∂K in 0 or 2 edges. So at each triangle node, ∂K contains both (β,γ)-edges or neither, and ∂K is a union of whole (β,γ)-components.
  - On the link only a lies in K (m is excluded by the assumption). So ∂K ∩ P = {e_{j+2}, e_{j+3}}, and Z1, which follows ∂K, must return by e_{j+3}.
  - The lock 2 case uses K = the {μ, c(b)}-component of b. Its cut colours are {β, δ}, ∂K ∩ P = {e_{j+3}, e_{j+4}}, and Z2 must return by e_{j+3}.
- **Step 2 (returns by e_{j+3} ⇒ lock fails).**
  - The closed curve C is Z1 drawn through faces, closed by an arc inside the empty pentagon around the corner a. It crosses only edges of dual colour β or γ, never a vertex.
  - A {μ, c(a)}-edge has dual colour δ, so a {μ, c(a)}-path cannot cross C.
  - Z1 is a path that touches P only at its two ends. So the boundary arc a, x_{j+2}, m crosses C exactly once (at side x_{j+2}x_{j+3}), and a and m lie on opposite sides.
  - The lock 2 case is the same with corner b; its arc b, x_j, m crosses C once, at e_{j+4}.
  - **Wording improvement:** say explicitly that Z1 touches P only at its endpoints. That is what makes "exactly two boundary points" true.
- **Corollary.**
  - (i) The {μ, c(b)} path from m to b, closed through v, separates x_j from x_{j+2}: at v the edges to x_{j+1} and x_{j+4} split the rotation into the sector {x_{j+2}, x_{j+3}} and the sector {x_j}. Both α vertices are off the curve, so the {α, c(a)}-chain of x_{j+2} misses x_j.
  - (ii) F swaps α ↔ c(a) on that chain, which contains x_{j+3} (adjacent to x_{j+2}, coloured c(a)). The new link is (α, μ, c(a), α, c(b)) with repeat index j+3, m′ = b and a′ = m. F recolours no μ- or c(b)-vertex, so the {μ, c(b)}-subgraph is unchanged, and lock 1 of F s is lock 2 of s.

## Relation to earlier results

This is the dual form of Lemma D (`MathNAttack.md` §2.1), as the source says. Corollary (ii) is the "inherited lock persists one step" lemma (Lemma 1 of `MathConjectureL.md`), now with a two-line Tait proof.
