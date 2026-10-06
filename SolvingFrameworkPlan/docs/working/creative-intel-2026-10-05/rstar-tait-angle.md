# Lemma R*, case "two or more neighbours of degree ≥ 6": the Tait angle (Long Table, 6 Oct 2026, afternoon)

All [hand]: written by Long Table on the MacBook, nothing computed, because the user's 13:01 rule stops new jobs on this machine. Not yet reviewed by Math or Audit. This page uses the lock criterion of `explore-vhphi/pathways/pd2_lock_proof.md` (hand, pending review), and its notation.

**Notation.** G is a triangulation and v a degree-5 vertex with link x_0..x_4. H is the dual of G−v, with pentagon node P and P-edges e_t dual to x_t x_{t+1}. In an unfilled state the P-edges are coloured β β γ β δ, with β triple. The odd edges are γ at e_{j+2} and δ at e_{j+4}. The *middle* β-edge is e_{j+3}, the one between the two odd edges on the short side.

A Kempe class is **targetless** if no state in it is filled. Then every state in it is doubly locked (DL), because by L3 an unfilled state that is not DL fills in one swap.

## 1. Normal form of a DL state [hand]

At P the (β,γ)-subgraph has degree 4 and splits into two P-paths. The (β,δ)-subgraph also splits into two. The (γ,δ)-subgraph has degree 2 and is one P-path. In a DL state:

- (β,γ): **Z1** joins e_{j+2} to e_{j+1}, and **Y1** joins e_{j+3} to e_j;
- (β,δ): **Z2** joins e_{j+4} to e_j, and **Y2** joins e_{j+3} to e_{j+1};
- (γ,δ): **W** joins e_{j+2} to e_{j+4}.

*Proof.* There are only two non-crossing pairings of four edges at P (Jordan; pd2 Step 0). The lock criterion fixes which pairing holds: Z1 returns by e_{j+1} and Z2 by e_j, so the leftover edges pair up as stated. ∎

So in a DL state **the middle edge e_{j+3} is (β,γ)-joined to e_j and (β,δ)-joined to e_{j+1}**, and neither odd edge reaches it. That is the whole content of "doubly locked" in Tait terms.

## 2. The Kempe class is closed under P-path swaps [hand]

**Lemma.** Swapping the two colours along any bichromatic cycle of H, or along any bichromatic P-path, gives a state in the same Kempe class.

*Proof.* Let C be the cycle, or the P-path closed up through the pentagon face, with colours x and y. Let z = x + y. Recolour every vertex on one side of C by c ↦ c + z.
- Edges crossing C had difference x or y. Now they have difference y or x, so the colouring stays proper, and the new Tait colouring is the old one with x and y swapped on C.
- C crosses no edge of difference z. So every {p, p+z}-component of G−v lies entirely on one side of C.
- So the move swaps a set of whole Kempe components, one at a time, and every intermediate step is a proper colouring of G−v. ∎

This is the converse of the P-D dictionary item "a chain swap = swapping all Tait cycles of its cut" (28,000 checks), and it is proved here by hand.

**Consequence.** In a targetless class, all four of Z1(s), Z2(s), Y1(s), Y2(s) must again be DL, as must every swap on a cycle away from P. Tracking only the positions of the two odd edges, which always form a diagonal {i, i+2} of the pentagon:

| move on s (odd at {j+2, j+4}) | new odd pair | new triple colour |
|---|---|---|
| Z1 (this is F) | {j+1, j+4} | β |
| Z2 (F′) | {j, j+2} | β |
| Y1 | {j+1, j+4} | γ |
| Y2 | {j, j+2} | δ |
| W | {j+2, j+4} (colours swapped) | β |

Z1 and Y1 move the odd pair to the same diagonal, and so do Z2 and Y2. But they leave *different* Tait colourings, and each must again be DL.

## 3. What "Y1(s) is DL" says about s [hand]

Swapping Y1 exchanges β and γ only on Y1. So the union of β- and γ-edges is unchanged, and in Y1(s) the loop from the new odd edge e_{j+1} is Z1 again, back to e_{j+2}. That is a lock automatically.

The other lock of Y1(s) is a real condition. In Y1(s) the triple colour is γ, and the odd edges are β at e_{j+1} and δ at e_{j+4}, with middle edge e_j. **The (γ,δ)-path of Y1(s) leaving e_{j+4} must return by e_{j+3}, not by the middle edge e_j.** In terms of s, its edge set is: every δ-edge of s, every γ-edge of s not on Y1, and every β-edge of Y1. In terms of s alone:

> **(Y1-lock)** Start at e_{j+4}, a δ-edge. At each node, alternate between the node's δ-edge and its "γ′-edge". The γ′-edge is the node's γ-edge if that edge is not on Y1, and otherwise the node's β-edge, which is then on Y1. The route must return to P by e_{j+3}.

While the route avoids Y1 it is exactly W. It differs from W only where W touches Y1.

The same holds for Y2 with δ and γ exchanged. So a targetless class imposes, at every state, four coupled conditions on how the three bichromatic structures Z, Y and W meet. The two lock conditions on Z1 and Z2 are only the first two.

## 4. Where the degrees enter [hand]

In H, the link vertex x_t is a face through P, lying between e_{t−1} and e_t, with **deg(x_t) − 1 edges**. Lock 1 holds *trivially* when Z1 is the boundary of x_{j+2}'s face. That happens exactly when the neighbours of x_{j+2} other than v use only the two colours μ and c(a). Then F = Z1 recolours x_{j+2} alone, α ↦ c(b).

- If deg(x_{j+2}) = 5, that face has 4 edges, and its colours are tightly forced. This is the room Theorem H's ring argument uses.
- If deg(x_t) ≥ 6, the face has ≥ 5 edges, and x_t's neighbours can carry three colours. A non-trivial lock path then has to leave the ring of faces around P and come back. This is the "outside two-colour path" in Math's 74 patterns.

**Proposed handle for the "two or more degree-≥6 neighbours" case.** Think of the outer ends of the five P-paths Z1, Z2, Y1, Y2, W as a **meander**: five arcs through P that do not cross, plus the crossings between arcs of *different* colour pairs, which are allowed and happen at shared edges. The Y1-lock and Y2-lock say that W and Y1, and W and Y2, cross in a specified order. A contradiction would come from showing that the moves of §2 must eventually produce a state where the crossing order is reversed. My guess is that the cause is a crossing between W and Y1 forced at a degree-≥6 face, where W passes through x_t's face and Y1 must cross it to reach e_j. **This is a direction, not an argument.** The first test is to compute, on T4's 26 radius-4 states and on the Six-Ring Trap's 121 DL states, which of the conditions in §3 fails first along each shortest fill. That is a kill test for the Studio, not this machine.

## 5. What is new here, and what is not

- New [hand, unreviewed]: the normal form (§1), closure under P-path swaps (§2), and the Y-lock conditions (§3).
- Classical: the dictionary itself, and Heawood's 1890 observation that the two Kempe chains from m interfere, which §1 restates.
- Not a proof of anything about R*. It reformulates "targetless" as a closed system of meander conditions, which a global (Jordan) argument would have to contradict.
