# WP9 declaration: is the mass-macro good-root property locally determined?

Long Table, 4 October 2026. Committed **before** any run. This is Track 2 of the contact pathway, recorded by the Proof Navigator in revision 50. These are facts and a test protocol only; status words are the Proof Navigator's.

## The property being tested

`Good(T, r)` is the published mass-macro outcome at root r of T: `outcome = passes` in `mass-macro-results.json`. Equivalently, the dead-end region D_r is empty.

## Rooted ball and its isomorphism type (declared now)

For k ∈ {1, 2, 3}, the **rooted ball** B_k(T, r) is defined as follows:
- **Vertices:** those at graph distance ≤ k from r in T.
- **Root:** r is marked as the root.
- **Rotation:** each ball vertex v keeps the cyclic rotation of T at v, restricted to neighbours that lie in the ball.
- **Degrees:** each ball vertex also carries its **full degree in T**. Vertices on the ball's edge thereby record how many neighbours lie outside.

Two rooted balls are **isomorphic** if a bijection of their vertex sets maps root to root, preserves T-degree, and carries every restricted rotation to the corresponding restricted rotation. The bijection may preserve all rotations or reverse all of them.

**Computation.** A canonical code is computed as follows:
1. For every dart (r, w) at the root and each orientation ±, run a breadth-first traversal from r.
2. At each vertex, visit its in-ball neighbours in rotation order (or reversed), starting just after the dart back toward its breadth-first parent; at the root, start at w.
3. Label vertices in order of discovery. Record, for each vertex in label order, its T-degree and the labels of its in-ball neighbours in that visiting order.
4. The code is the lexicographically least record over all starts and orientations.

Equal codes mean isomorphic rooted balls.

## Hypothesis LD_k (local determinacy at radius k)

On a given set of roots, any two roots with equal B_k codes have the same `Good` outcome.

## Protocol (frozen)

1. **Discovery: orders 12–18 only** (22 graphs, 279 roots), for k = 1, 2, 3.
   - **Report:** the number of distinct codes; the number of *mixed* codes, which contain both passing and failing roots; for each failing root, the size of its code class and whether any passing root shares it.
   - **Kill LD_k:** a single mixed code, recorded with both roots.
   - **Survival,** reported honestly. If every failing root's code is unique to failing roots, LD_k survives only vacuously for those roots. With 6 failing roots in 3 automorphism classes in this range, that is likely, and **it would not be evidence for locality.** We therefore also report how many failing roots share a code with *any* other root.
2. **Orders 19–20** are run only after the discovery report is posted, and only for the radii that survive. This follows the Proof Navigator's instruction.
3. **Descent-reducibility** (route B) waits until some radius survives non-vacuously.

The Proof Navigator expects k = 1 to fail. A failure at radius k kills only LD at that radius.
