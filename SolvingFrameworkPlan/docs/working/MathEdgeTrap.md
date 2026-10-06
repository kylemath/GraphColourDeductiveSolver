# Edge traps versus vertex traps: when deletion creates a new Kempe class

Math lead, 6 October 2026. Hand only; nothing was run. Labels: [hand] means a complete argument is given here, [sketch] means a reasoned outline. **Unreviewed.**

**Setting.**
- T is a triangulation of the sphere, and colourings are proper 4-colourings.
- For a subgraph H obtained from T by deleting an edge or a vertex, a Kempe class of H is **new** when it contains no restriction of a colouring of T.
- Given the Four Colour Theorem, R\* at v holds exactly when T − v has no new class.

## 1. Edge deletion: an exact characterisation [hand]

Let e = xy be an edge of T, with the two faces xyp and xyq. Put G = T − e. A colouring of G restricts from a colouring of T exactly when c(x) ≠ c(y). So a class S of G is new exactly when **every** state of S has c(x) = c(y).

**Theorem 1.** A Kempe class S of G is new if and only if, in every state c of S, with κ = c(x) = c(y), the vertices x and y lie in a common {κ, r}-component of G for each of the three colours r ≠ κ.

*Proof.*
- (⇒) Suppose some state c of S and some r ≠ κ have x and y in different {κ, r}-components. Swap the component of x. Then c(x) = r ≠ κ = c(y), and the new state lies in S. So S is not new.
- (⇐) Suppose every state of S has all three chains. Take a swap K of colours {s, t}.
  - If κ ∉ {s, t}, then x and y are not recoloured.
  - If κ ∈ {s, t}, say s = κ, then the chain condition puts x and y in the same {κ, t}-component, so both are recoloured or neither is. Both end up with the same colour.
  - In every case c(x) = c(y) after the swap. By induction along any Kempe path, every state of S has c(x) = c(y). ∎

**Free chains.** p is adjacent to both x and y, and c(p) ≠ κ, so the path x–p–y is a {κ, c(p)}-chain for free. Likewise q gives a free {κ, c(q)}-chain.
- If c(p) ≠ c(q), **two of the three chains are free**. The class is new exactly when the **single** remaining chain {κ, r₃} (r₃ the fourth colour) joins x to y in every state of S.
- If c(p) = c(q), one chain is free and two are non-trivial.

**On intern D's "step 4" (closure under swaps).** Theorem 1 shows no separate closure step is needed. The condition "the chains hold in every state of S" is itself the characterisation, and S is a Kempe class by definition. What is genuinely open is an **intrinsic, checkable criterion**, e.g. on the structure of T near e: when does a class exist in which the third chain is never broken? The natural mechanism is:
- the third chain together with e closes a cycle;
- every swap that could cut the chain is either trivial on it, or recolours it into another chain with the same endpoints.

That last property must be proved for each concrete mechanism. It does not follow from a general argument.

## 2. Vertex deletion: the analogous characterisation [hand]

Let v have degree 5 with link x₀..x₄. A colouring of T − v restricts from a colouring of T exactly when it is **filled** (the link uses at most 3 colours). So a class S of T − v is new exactly when every state of S is unfilled.

**Theorem 2.** A Kempe class S of T − v is new if and only if every state of S is doubly locked.

*Proof.* An unfilled state that is not doubly locked fills in one swap (L3, reviewed). If every state is doubly locked, every state is unfilled, so no state is filled. ∎

**Free versus non-trivial chains at a degree-5 hole [hand].** Take an unfilled state: repeat colour α at x_j and x_{j+2}, singletons m = x_{j+1} (colour μ), a = x_{j+3} (colour A) and b = x_{j+4} (colour B). One swap fills the hole only by removing a singleton colour from the link, i.e. by recolouring one singleton without bringing its colour back elsewhere on the link. For each singleton and each other colour:
- m with α: m is adjacent to x_j and x_{j+2}, both α, so the swap also recolours them, and the link keeps four colours. **Free (blocked).**
- a with B, and b with A: a and b are adjacent, so the swap exchanges them. **Free.**
- a with α: a is adjacent to x_{j+2} (α). **Free.**
- b with α: b is adjacent to x_j (α). **Free.**
- m with A, equivalently a with μ: **lock 1**, the non-trivial chain from x_{j+1} to x_{j+3}.
- m with B, equivalently b with μ: **lock 2**, the non-trivial chain from x_{j+1} to x_{j+4}.

So among the singleton-pair swaps, **all but two pairs are blocked for free**, and the state is trapped for one move exactly when **two** non-trivial chains hold. This is the vertex analogue of the edge case's single non-trivial chain.

## 3. Why the edge mechanism does not transfer to a degree-5 vertex [hand + sketch]

1. **Two non-trivial chains, not one [hand].** An edge trap needs one non-trivial chain per state (when c(p) ≠ c(q)). A vertex trap needs two.
2. **The two chains must cross [hand, path 9 Lemma X, unreviewed].** Every lock-1 path crosses every lock-2 path at a μ-vertex other than x_{j+1}. The edge trap has no such constraint: its single chain plus e is just a cycle.
3. **The repeat position rotates [hand, Theorem A].** A new class at v contains states of **all five** repeat types. So the trap must sustain the two crossing chains in five rotated frames, each with a different pair of link vertices joined by a different pair of colours. The edge trap has one fixed frame: the colour κ moves, but x and y and their faces stay the same.
4. **No frozen states [hand, no-frozen-DL lemma].** In every doubly locked state, two of the six bichromatic subgraphs are disconnected (the {α, A}- and {α, B}-subgraphs separate x_j from x_{j+2}). So the class always has non-trivial swaps, which must all preserve the two-chain trap. An edge trap can live in a class of nearly frozen colourings.
5. **[sketch] The relation through a fan.** T − v equals T\*_τ minus its two chords, for any legal fan τ. Every unfilled state is admitted by three fans, i.e. it is a colouring of three different triangulations T\*_τ. A new class at v is therefore **not** a new class of T\*_τ minus the chords relative to T\*_τ (its states are colourings of T\*_τ). It is a class whose states all fail to extend to T. That is why edge-trap results about T\*_τ − chord do not transfer.

**What this explains, and what it does not.** Items 1–4 explain why vertex traps are much harder to sustain than edge traps: two crossing chains in five rotated frames, closed under non-trivial swaps, against one chain in one frame. This fits the empirical finding that edge deletion creates new classes while vertex deletion has not been seen to. **It is not a proof that vertex deletion never creates a class.** The data say traps sustain 4–5 consecutive F-steps (A_r: infinitely many F-steps) before a non-F swap breaks them, and no hand argument shows that some swap always breaks them.

**Under what condition could a vertex trap exist?** All of the following must hold in every state of the class:
- both locks (the two crossing chains);
- for each of Lemma E's eight link-touching swaps, the image is again doubly locked;
- for every silent swap (one not touching the link), lock preservation as in Lemma R.

A construction would need a family of colourings in which the two lock chains are **stable** under all these swaps. One candidate is the infinite F-orbits of A_r, which already sustain locks under F and B but fail under other swaps (they fill within radius 2–3). This is the target for path 3's SL design.

## 4. A clean statement for the paper

> **Proposition (edge and vertex traps).**
> (i) Deleting an edge e = xy of a triangulation creates a new Kempe class if and only if some Kempe class of T − e keeps x and y joined by all three {c(x), r}-chains in every state; when the two faces at e have differently coloured apices, exactly one chain is non-trivial.
> (ii) Deleting a degree-5 vertex v creates a new Kempe class if and only if some Kempe class of T − v consists of doubly locked states. In each of these, two non-trivial chains are required and must cross (Lemma X), and all five repeat types occur in the class (Theorem A).

Parts (i), (ii) and the free-chain counts are [hand] above. Lemma X and Theorem A are cited from the path-9 and confinement write-ups: Lemma X is unreviewed, and Theorem A was re-derived by a worker.
