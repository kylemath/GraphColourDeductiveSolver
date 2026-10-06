# P-D: hand proof of the Tait lock criterion (Long Table, 6 Oct 2026, written about 12:40 MDT)

[hand]. Code re-check (not part of the proof): `pd2_x.py` part A, 0 mismatches on 3,682 unfilled states (T4, A_3, A_4, every degree-5 hole).

## Definition matched

The definition is in `astruct_core.py`, the one used for every lock count in P-D and A-Structure:

    locks(adj,col,L) = (a in comp(adj,col,m,{col[m],col[a]}), b in comp(adj,col,m,{col[m],col[b]}))

Here `comp` is the connected component in G-v. In words: G is a triangulation, v has degree 5 with link x_0..x_4 in rotation order, and c is a proper 4-colouring of G-v with four colours on the link. The repeat is c(x_j) = c(x_{j+2}) = α, with m = x_{j+1}, a = x_{j+3}, b = x_{j+4}, and μ = c(m).
- **Lock 1 (m~a):** a lies in the {μ, c(a)}-component of m.
- **Lock 2 (m~b):** b lies in the {μ, c(b)}-component of m.
- **Doubly locked:** both hold.

## Notation (Tait)

Colours are in Z2xZ2. H is the dual of G-v; its node P is the pentagonal face. The dual edge of a G-edge uw has colour c(u)+c(w). Every node of H other than P is a triangle, so its three edges carry 1, 2, 3 once each [cited: Tait 1880; Saaty–Kainen]. The P-edge e_t is dual to x_t x_{t+1}.

Since α+μ+c(a)+c(b) = 0, we can put β = α+μ, γ = α+c(a), δ = α+c(b). Then e_j = e_{j+1} = e_{j+3} = β, e_{j+2} = γ and e_{j+4} = δ. Two sums are used below:
- μ+c(a) = α+c(b) = δ;
- μ+c(b) = α+c(a) = γ.

**Claim.** Let Z1 be the (β,γ)-path that leaves P by e_{j+2}, and Z2 the (β,δ)-path that leaves P by e_{j+4}. Then:
- Lock 1 holds iff Z1 returns to P by e_{j+1}; otherwise Z1 returns by e_{j+3}.
- Lock 2 holds iff Z2 returns to P by e_j; otherwise Z2 returns by e_{j+3}.

## Proof

**Step 0: where Z1 can return.** Every node other than P has exactly one edge of each colour. So the (β,γ)-subgraph has degree 2 at every node except P, where its edges are e_j, e_{j+1}, e_{j+2}, e_{j+3}. Its component through P is therefore two P-to-P paths, and they meet only at P.

Suppose they pair e_{j+2} with e_j, and so e_{j+1} with e_{j+3}. Their ends then alternate around P. The first path together with P is a simple closed curve. The second path leaves P on one side of it and returns on the other, so by the Jordan curve theorem it crosses the first path away from P. That is impossible: the two paths share no node, and dual edges do not cross. A path cannot return by the edge it left by. So Z1 returns by e_{j+1} or by e_{j+3}.

**Step 1: if Z1 returns by e_{j+1}, lock 1 holds.** Suppose a is not in the {μ, c(a)}-component of m, and let K be the {μ, c(a)}-component of a. Every G-edge with exactly one end in K has its other end coloured α or c(b), because a neighbour coloured μ or c(a) would lie in K. So its dual colour lies in {μ, c(a)} + {α, c(b)} = {β, γ}.

At a triangle the number of cut edges is 0 or 2. So at every node other than P, the cut ∂K contains either both (β,γ)-edges or none, and ∂K is a union of whole (β,γ)-paths and cycles. On the link, a is in K, while x_j and x_{j+2} (coloured α), b (coloured c(b)) and m (by assumption) are not. So ∂K contains e_{j+2} but not e_{j+1}. Then ∂K contains all of Z1, which ends at e_{j+1}. Contradiction.

**Step 2: if Z1 returns by e_{j+3}, lock 1 fails.** Draw Z1 through the faces of G-v. Inside the pentagon, close it by an arc from side x_{j+2}x_{j+3} to side x_{j+3}x_{j+4}. This gives a simple closed curve C.
- C crosses only G-edges of dual colour β or γ. So it never crosses an edge whose two ends are coloured μ and c(a), since such an edge has dual colour δ.
- C meets the pentagon boundary at exactly two points, because Z1 uses only two P-edges. So the boundary arc a = x_{j+3}, x_{j+2}, x_{j+1} = m crosses C exactly once, and a and m lie on opposite sides of C.
- A {μ, c(a)}-path from m to a would have to cross C.

So there is no such path, and lock 1 fails.

**Lock 2.** The argument is the same with (β,δ) in place of (β,γ). In Step 1, K is the {μ, c(b)}-component of b. Its cut edges have dual colour in {μ, c(b)} + {α, c(a)} = {β, δ}. ∂K contains e_{j+3} and e_{j+4} but not e_j. In Step 2 the curve cuts off the corner b, and it does not cross the {μ, c(b)}-edges, whose dual colour is γ. ∎

Relation to Lemma D (`MathNAttack.md` §2.1): Step 1 is the (⇒) half of Lemma D read in the dual, and Step 2 is the (⇐) half. Lemma D's ring condition for lock 1 is that x_{j+2} is joined to x_j or to x_{j+4} by an {α, c(b)}-path. In the dual, this is "Z1 is not the short path around x_{j+2}".

## Corollary (F keeps one lock for free) [hand]

If s has lock 2, then:
- (i) x_j is not in the chain K that F swaps;
- (ii) F s has lock 1.

So F s is doubly locked iff F s has lock 2.

*Proof of (i).* The {μ, c(b)}-path from m to b, closed through v, separates x_j from x_{j+2} [Jordan]. So the {α, c(a)}-chain of x_{j+2} misses x_j.

*Proof of (ii).* By (i), the link of F s is (α, μ, c(a), α, c(b)), with repeat index j+3, m' = b and a' = m. Lock 1 of F s says that m and b lie in one {μ, c(b)}-component. F recolours only α- and c(a)-vertices, so the {μ, c(b)}-subgraph is unchanged and this is lock 2 of s.

In Tait terms, the (β,δ) 2-factor is invariant under F. Code re-check: `pd2_x.py` [A] gives 0 exceptions.
