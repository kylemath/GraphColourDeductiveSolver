# Intern C, cycle 7: the cross-j collision is realisable (hand only, nothing run)

## Verdict: REALISABLE. The bound "at most 2 preimages" is tight, and the collision occurs in the order-17 minimum-degree-5 triangulation.

## 1. What cannot work
If every ring vertex also had degree 5, the neighbourhood would close up to the icosahedron, whose ring is adjacent to a single extra vertex u. The ring (q,S,X,S,p) uses all four colours, so u would have no colour. So the configuration needs some ring vertex of degree >= 6. My earlier derivation only used the degrees of the link vertices (they fix the neighbour lists of y0..y4); ring degrees were never used.

## 2. The realisation (order 17)
Graph T: vertices v, y_0..y_4 (link), w_0..w_4, z_0..z_4, u. Edges: v to every y_t; y_t y_{t+1}; y_t to w_{t-1}, w_t; w_t w_{t+1}; w_t to z_{t-1}, z_t; z_t z_{t+1}; u to every z_t (indices mod 5).
- Face count: 5 + 10 + 10 + 5 = 30 = 2*17 - 4, so it is a plane triangulation.
- Degrees: v, y_t, z_t, u have degree 5; w_t has degree 6. This is the order-17 triangulation with degree sequence 5^12 6^5.
- No separating triangle: the only triangles are the 30 faces. I checked the adjacent ring triples: w_t is not adjacent to w_{t+2}, y_t and y_{t+1} share only w_t, and z_t, z_{t+1} share only w_{t+1} among ring vertices.

Colouring of T (colours S, p, q, X): v = X; y = (S, p, q, p, q); w = (q, S, X, S, p); z = (p, q, p, q, S); u = X.
Every edge is proper (I checked all of them: v-y, y-y, y-w, w-w, w-z, z-z, u-z).

Let t = this colouring restricted to T - v. It is filled (link colours S,p,q).

- s1 = t with y_4 recoloured from q to X. The neighbours of y_4 are y_3 (p), y_0 (S), w_3 (S), w_4 (p), so this is proper. The link is (S,p,q,p,X), repeat p at y_1, y_3, so j = 1. Lock 1 needs a {q,X}-path from m = y_2 to a = y_4, but y_4 has no q or X neighbour, so lock 1 fails. The map swaps the {q,X}-component of a, which is {y_4}, giving t.
- s2 = t with y_1 recoloured from p to X. The neighbours of y_1 are y_0 (S), y_2 (q), w_0 (q), w_1 (S), so this is proper. The link is (S,X,q,p,q), repeat q at y_2, y_4, so j = 2, m = y_3, a = y_0, b = y_1. Lock 1 holds via the {p,S}-path y_3 - w_3 - w_4 - y_0 with colours p, S, p, S; its edges y_3 w_3, w_3 w_4, w_4 y_0 are present, and none of these vertices were changed. Lock 2 fails because y_1 has no p or X neighbour. So the branch-2 swap is the {p,X}-component of b = {y_1}, giving t.

So s1 and s2 (different repeat indices) are two preimages of the same filled t, in one Kempe class. t has exactly these two candidate preimages, one per branch, so the bound 2 is attained.

## 3. Consequence
- The hole v (all five link vertices of degree 5) is in the order-17 census range, so a computed claim "0 collisions in 353,812 states, orders 12-21" cannot refer to a global (all-j) check. Either the check was per j, or it missed this t. The localcompute run should recount globally.
- The DL half of the floor inequality therefore only has the slack of F_{j+3}+F_{j+4} left after the per-j injection, with no extra global slack from the non-DL part. The collision can only reduce the global room, it never creates room.

## 4. Self-check: what would make me wrong
- A mistaken edge in my T description. Face count, degrees, and the triangle check agree with the known order-17 graph (12 vertices of degree 5, 5 of degree 6).
- The collision uses only two single-vertex recolourings, so even if the colouring were slightly off, I would expect a nearby variant to work. No computation was run.
