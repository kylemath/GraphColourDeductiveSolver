# Intern C, cycle 6: the non-DL single-swap map in the 18:11 quarter-floor note (hand only, nothing run)

Notation: s unfilled, repeat colour alpha at x_j and x_{j+2}, m = x_{j+1} (mu), a = x_{j+3} (A), b = x_{j+4} (B). Image t = phi(s).

## Verdict
- **Per-j injectivity (all the inequality (U_j - D_j) <= F_{j+3} + F_{j+4} needs): PROVED, no gap.**
- **Global injectivity "the map is injective" (all j at once): NOT justified by the sketch, and there is a local configuration where two states with adjacent repeat indices collide.** I did not show that this configuration sits inside a min-degree-5 triangulation, so this is a gap in the claim as worded, not a counterexample to the inequality.

## 1. The map is well defined and lands in filled states
- Lock 1 fails: the only link vertices coloured mu or A are m and a, and m is not in a's {mu,A}-component. So the swap changes only a (to mu). The image link is (alpha, mu, alpha, mu, B): filled, singleton B at j+4.
- Lock 1 holds, so lock 2 fails (non-DL): the only link vertices coloured mu or B are m and b, and m is not in b's component. The swap changes only b (to mu). The image link is (alpha, mu, alpha, A, mu): filled, singleton A at j+3.
- The image is in the same class: it is a Kempe swap.

## 2. The inverse (answer to "does the swap undo itself when the component differs?")
- The vertex set coloured in {mu,A} is the same in s and in t, because the swap only exchanges mu and A inside the component. So the induced subgraph and its components are identical as vertex sets. Re-swapping the component of a recovers s. The sketch is right here. "The component differs" cannot happen.
- Read from t alone, given j and the branch: A (resp. B) is the colour missing from the link of t, mu is the colour of the swapped vertex in t, and the swapped vertex is x_{j+3} (resp. x_{j+4}). So s = psi_{j,branch}(t). This is a left inverse, so phi is injective on each (j, branch).
- Within fixed j the two branches land at different singleton positions (j+4 versus j+3), so they cannot collide. Hence the per-j injection into F_{j+3} + F_{j+4} is a proof, and so is the per-j inequality. Summing over j gives the stated sum, which counts each F twice; no global injectivity is needed for that.

## 3. Cross-j collisions (the gap in "the map is injective")
A filled t with singleton at position i can arise from branch 1 with j = i+1 or from branch 2 with j = i+2. So t alone does not determine the preimage. Collision pattern (all five link vertices and the ring of degree 5 around v, link y0..y4 = x_i..x_{i+4}):
- t: link (S, p, q, p, q); ring w_0..w_4 = (q, S, X, S, p), where X is the colour missing from the link. This is a proper colouring of the 2-ball: the link and ring conditions all check.
- s1 = t with y4 recoloured q -> X (y4 has neighbours p, S, S, p). Repeat p at y1, y3, so j = y1. Lock 1 needs a {q,X}-path from y2 to y4, but y4 has no q or X neighbour, so it fails and phi(s1) = t.
- s2 = t with y1 recoloured p -> X (y1 has neighbours S, q, q, S). Repeat q at y2, y4, so j = y2, m = y3, a = y0, b = y1. Lock 1 holds via the path y3 (p), w_3 (S), w_4 (p), y0 (S). Lock 2 fails since y1 is isolated in the {p,X}-graph. So the branch-2 swap recolours y1 back: phi(s2) = t.
So phi(s1) = phi(s2) with s1 != s2 (different repeat indices), in the same class. Whether a min-degree-5 triangulation realises the colouring is something I did not show; it only needs a proper 4-colouring of T - v with that ring, and no other restriction.

## 4. Consequence and request
- The inequality that is actually proved this way is per-j. If anywhere the argument is used as "(sum of non-DL unfilled) <= (sum of filled)" (one-to-one globally), it is unsupported, and the computed "0 collisions in 353,812 states" must have counted collisions within each j only, or the configuration above does not occur in orders 12-21. I cannot tell which.
- Ask: state "injective on each (j, branch)" and note the F-count is used twice.

## Self-check: what would make me wrong
- A planarity or colouring obstruction that forbids the ring (q, S, X, S, p) together with these links. I found none locally; I did not check any particular triangulation.
- If the note's "injective" already means per j, then there is no gap and only wording.
