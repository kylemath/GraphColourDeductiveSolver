# Intern C, cycle 3: Tait lock criterion and F corollary (hand only, nothing run)

Sources: longtable/explore-vhphi/pathways/pd2_lock_proof.md and Math's 13:55 review message. I re-derived every step independently.

## Verdict: NO GAP FOUND

Steps checked hardest:

1. **Colours of the pentagon edges.** With colours in Z2xZ2, the dual colour of uw is c(u)+c(w), nonzero by properness. Then e_j = e_{j+1} = e_{j+3} = beta (e_{j+3} because c(a)+c(b) = alpha+mu, as the four colours sum to 0), e_{j+2} = gamma, e_{j+4} = delta. beta, gamma, delta are distinct, and the five colours sum to 0, which is consistent. Both key sums mu+c(a) = delta and mu+c(b) = gamma hold.
2. **Does the hole face behave like the others?** It need not. Every node of H other than P is a triangle (G is a triangulation, v is the only deleted vertex), so each has one edge of each colour. P is never assumed to be Tait. P enters only as the endpoint of the (beta,gamma) paths, which have degree 4 there (e_j, e_{j+1}, e_{j+2}, e_{j+3}). The component through P is exactly two P-to-P paths. A P-edge cannot be a loop, since each link edge borders P on one side only.
3. **Orientation, Step 0.** Cyclic order of the four ends at P is e_j, e_{j+1}, e_{j+2}, e_{j+3}. The pairing (e_{j+2},e_j)(e_{j+1},e_{j+3}) alternates, and Jordan then forces a crossing at a non-P node, which is impossible because those nodes have degree 2 in the subgraph. So Z1 returns by e_{j+1} or e_{j+3}. For lock 2 the order is e_{j+3}, e_{j+4}, e_j, e_{j+1}, Z2 starts at e_{j+4}, and the same argument leaves e_j or e_{j+3}. This matches the claim.
4. **Step 1 (cut argument).** Cut edges of K = the {mu,c(a)}-component of a have outer ends coloured alpha or c(b), so dual colours lie in {beta,gamma}. At a triangle the cut has 0 or 2 edges, so both (beta,gamma) edges are cut or neither. At P, e_{j+2} is cut and e_{j+1} is not (m not in K, x_{j+2} is alpha). So all of Z1 is in the cut, and Z1 cannot end at e_{j+1}. For lock 2, e_{j+4} is cut and e_j is not; same conclusion.
5. **Step 2 (Jordan curve).** Z1 meets P only at its ends. Closing it inside P by an arc gives a simple closed curve that cuts off corner a and crosses only edges of dual colour beta or gamma. A {mu,c(a)}-edge has dual colour delta, so it is never crossed. a and m are separated because the boundary arc a, x_{j+2}, m meets the curve once. The lock-2 version cuts off corner b; the edge colour that is not crossed is gamma.
6. **Corollary.** (i) The {mu,c(b)}-path m to b closed through v separates x_j from x_{j+2}, so x_j is not in the {alpha,c(a)}-chain F swaps. (ii) After F the link is (alpha,mu,c(a),alpha,c(b)). The new repeat index is j+3, so the new middle is b and the new a' is m. Lock 1 of Fs asks for m in the {c(b),mu}-component of b. That subgraph is untouched by F, so this is lock 2 of s. I also checked the Tait statement directly. F adds gamma to the colours in K. The cut edges of K have dual colours in {beta,delta} (alpha+mu = beta, alpha+c(b) = delta, c(a)+mu = delta, c(a)+c(b) = beta), so they swap beta and delta, and the (beta,delta)-edge set is unchanged as a set. Interior edges of K have colour gamma and are untouched. So "the 2-factor is fixed" is correct, as an unlabelled edge set. The beta/delta labels on the cut edges do swap, and the roles are relabelled in the new frame.

## Severity
Wording only. The statement "the (beta,delta) 2-factor is fixed" is true as an edge set, but the beta/delta labels of F's cut edges swap (consistent with the new frame's roles). Worth one clause. Math's wording point (Z1 touches P only at its ends) is also right.

## Self-check: what would make this wrong
- If H had a loop or a triangle node with two P-edges (a link chord), Step 0's picture changes. A chord means a separating triangle, which is excluded, and the criterion would still go through.
- Embedded-dual conventions: I assumed the rotation at P in H matches the boundary order of x_t. This is standard for a plane dual.
- I did not run or read the pd2_x.py code check, so the 3,682-state check is not independently confirmed.
