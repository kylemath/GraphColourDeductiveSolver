# RSST-1SHOT: own §7 verdict (written before reading W6b's DECISIONS.md)

Spec: RSSTFP_SPEC.md 33338de6, §7 "Assumption H": in an internally 6-connected triangulation the window
(u, link, apexes s_i, privates) has no edges or identifications beyond those drawn, so induced-ness and
face-ness may be checked on the window.

**Verdict: HOLDS**, under the hypotheses below, including for the privates and for the undrawn middles of a
9+ link vertex. Hypotheses: T is a simple triangulation of the sphere, every vertex has degree >= 5 (d >= 5),
T has no separating cycle of length <= 4, and every separating 5-cycle has a single vertex on one side
(internal 6-connectivity in RSST's sense). If the project's frame class allows anything weaker than this,
the argument below has to be re-checked against it. The second-ring part uses the 5-cycle clause, not only
"no separating <= 4-cycles".

## Argument

F0. Every 3-cycle of T is a face. A non-facial triangle separates and has a vertex on each side.

(a) The link has no chord, and u, w_0..w_{d-1} are distinct. Suppose w_i ~ w_k with k != i+-1. Then u w_i w_k
is a triangle. The faces at u are only (u, w_j, w_{j+1}), so this triangle is not a face, which contradicts F0.

seg_i is rot(w_i) without u, w_{i-1} and w_{i+1}, in order. It runs ccw from s_{i-1} to s_i and has
deg(w_i) - 3 >= 2 vertices. For a 9+ link vertex this includes all of its real middles.

(c) No extra u/w edges, and ring 2 is disjoint from {u} and the link. rot(u) is exactly the link, so every
neighbour of u is a w. Every neighbour of w_i lies in rot(w_i) = u, w_{i-1}, seg_i, w_{i+1}. Could a vertex of
seg_i be u or some w_k? Then w_i ~ w_k, so k = i+-1 by (a). But u and w_{i+-1} already have their own
positions in rot(w_i), and in a simple graph a rotation lists each neighbour only once. So no.

(b) Ring-2 vertices are distinct, apart from the intended sharing of s_i between seg_i and seg_{i+1}. This
covers 9+ middles. Suppose a vertex x takes position P in seg_i and position Q in seg_k, and this is not the
s_i sharing. There are three cases.
- k = i. This contradicts simplicity.
- k = i+1. Then w_i, w_{i+1}, x is a triangle, so it is a face (F0). The faces on the edge w_i w_{i+1} are
  (u, w_i, w_{i+1}) and (w_i, s_i, w_{i+1}), so x = s_i. Simplicity then forces P and Q to be the two drawn
  slots of s_i, which is the excluded sharing.
- k not in {i, i+-1}. Then u w_i x w_k is a 4-cycle. Its two sides contain w_{i+1}..w_{k-1} and
  w_{k+1}..w_{i-1}. Both lists are non-empty, and none of these vertices is on the cycle, by (a) and (c). So
  the 4-cycle separates: contradiction. If x is the shared apex s_i and also lies in seg_k, then because
  d >= 5 one of i, i+1 is non-adjacent to k, and that one is used.

So R2 = seg_0[:-1] + seg_1[:-1] + ... is a simple cycle of length sum_i (deg w_i - 4).

(d) R2 has no chord. Its edges are the consecutive pairs inside each seg_i. For a degree-5 w_i this
includes the drawn s_{i-1} s_i. Suppose x ~ y with x, y on R2 but not consecutive on R2. There are three
cases.
- x and y lie in a common seg_i. Then w_i x y is a triangle, so it is a face, so x and y are consecutive in
  rot(w_i). Both lie in seg_i, so they are consecutive in seg_i and hence on R2: contradiction.
- x lies in seg_i and y in seg_{i+1}, and neither is s_i (otherwise the first case applies). The 4-cycle
  w_i x y w_{i+1} contains the edge w_i w_{i+1}. The two faces on that edge have third vertices u and s_i.
  Neither of these is on the cycle, so they lie on opposite sides: a separating 4-cycle. Contradiction.
- Otherwise x lies in seg_i and y in seg_k, k not in {i, i+-1}, and x, y share no seg and no adjacent pair of
  segs. Take the 5-cycle u w_i x y w_k. Its sides hold w_{i+1}..w_{k-1} and w_{k+1}..w_{i-1}. Suppose one
  side holds a single link vertex, say w_{i+1} with k = i+2. Every neighbour of w_{i+1} is on the cycle or
  on that side. seg_{i+1} has >= 2 vertices, and none of them is x or y by the case choice. So that side has
  >= 3 vertices. The other side holds d - 3 >= 2 link vertices. A separating 5-cycle with >= 2 vertices on
  each side is excluded: contradiction.

**Consequence.** The drawn window, together with the real 9+ middles, is an induced subgraph of T with no
identifications, and every triangle in it is a face of T (F0). The host graph of §7 is the subgraph induced
on the hosts, so rsst_rows' `contains` decides RSST appearance exactly on the window. A host's neighbours
outside the window are ring-3 vertices, which can only be images of K's ring vertices, and RSST appearance
does not constrain those. A 9+ middle is never a host (§6). So the relaxed host rule extended to the privates
is sound. Nothing in §8 needs to change.

**Gap or caveat.** The verdict is conditional on the frame class being internally 6-connected, as stated
above. The argument does not use the private letters, the domains, or the parts.

## Brute-force sanity check

`code/s7_check.py` builds real windows, with a 9/10 link vertex drawn with all of its real privates. For
every pair of R2 vertices it searches for an obstruction:
- stage I (identification): the witnesses are u and the w's only;
- stage C (chord): the witnesses are all window vertices.

An obstruction is a cycle through the new adjacency that is either a separating cycle of length <= 4 or a
5-cycle with >= 2 window vertices on each side. Results are in `logs/s7_check.log`. Any unobstructed pair
would be a candidate counterexample.
