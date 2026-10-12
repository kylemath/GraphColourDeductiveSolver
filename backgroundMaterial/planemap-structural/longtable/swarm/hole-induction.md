# Induction from the vacancy hypothesis

**INDUCTION WORKS.**

The theorem below is 4-colourability of every spherical triangulation. The vacancy hypothesis is an assumption, used once on the triangulation being coloured. It is not the statement being proved by induction. The honest base is the tetrahedron. The icosahedron is the first order at which the hypothesis is used.

Throughout, a spherical triangulation is a simple maximal planar graph on $n \ge 4$ vertices: every face is a triangle, including the outer face, so $|E| = 3n - 6$. Colours are $\{0,1,2,3\}$.

## Hypothesis

Assume only the following.

Let $T$ be a spherical triangulation of minimum degree at least 5, and let $h$ be any vertex. Let the remaining vertices carry a proper 4-colouring. Then there is a finite sequence of the two moves below, applied to the current hole, after which the neighbours of the current hole use at most three colours. Assigning a missing colour to that hole is a proper 4-colouring of $T$.

A **singleton vacancy slide** at the current hole $h$ is allowed when a neighbour $u$ carries a colour $\alpha$ that occurs once on the link of $h$. Colour $h$ with $\alpha$ and erase the colour of $u$. The new hole is $u$, and the new colouring is a proper 4-colouring of $T - u$.

A **Kempe swap** stays at the same hole. On the coloured subgraph, take one connected component of the subgraph formed by two colours and exchange those colours on the component. Properness is preserved: edges inside the component are recoloured by a swap of the two colours, and every edge leaving the component meets a vertex of some other colour.

The sequence is allowed to move the hole. The vertex that is filled is whatever hole the sequence has reached, not necessarily the hole it started from. The coloured object is $T$, the same vertex set, now with every vertex coloured. Relative to the deletion, one more vertex is coloured. No new vertex is added.

## Theorem

Every spherical triangulation has a proper 4-colouring.

The proof is induction on $n = |V(T)|$.

## Base

The case $n = 4$ is the tetrahedron $K_4$. Every pair is adjacent, so the four vertices receive four distinct colours.

This is the honest base. Every spherical triangulation on $n \le 11$ vertices has a vertex of degree at most 4, by the counting lemma below, and the degree-3 and degree-4 steps never call the hypothesis. Those orders are theorems, not assumptions. They are also the graphs that appear when a larger face is completed by chords. An induction that began at the icosahedron would have no colouring of those graphs.

The icosahedron, order 12, all degrees 5, is the smallest triangulation to which the hypothesis can apply, and the first place the inductive step quotes it. It is a case of the step, not a base.

## Counting

For a spherical triangulation,
$$
\sum_v \bigl(6 - \deg(v)\bigr) = 12.
$$
Every such graph therefore has a vertex of degree at most 5. If every degree is at least 5, then
$$
n_5 - \sum_{k \ge 7} (k-6)\, n_k = 12,
$$
so $n_5 \ge 12$ and $n \ge 12$. Thus every spherical triangulation on at most 11 vertices has a vertex of degree at most 4. The unique equality case $n = 12$ is 5-regular. The inductive step treats every 12-vertex triangulation the same way, so uniqueness is not required.

A simple spherical triangulation also has minimum degree at least 3.

## Completing a vacated face

Let $v$ be a vertex of degree $d \in \{3,4,5\}$, with link cycle $C$ in cyclic order. In $T$ the star of $v$ fills one side of $C$. Every chord of $C$ that already exists lies on the other side, so the existing chords of $C$ are non-crossing. Deleting $v$ leaves a near-triangulation whose outer face is $C$.

- If $d = 3$, then $T - v$ is already a spherical triangulation on $n-1$ vertices. No chord is added. The edge count is $3n-6-3 = 3(n-1)-6$.
- If $d = 4$, label the link $a,b,c,d$ in order. The two diagonals $ac$ and $bd$ cross, so they cannot both lie on the far side of $C$. At least one is absent. Adding one absent diagonal across the face left by $v$ produces a spherical triangulation $T^\star$ on $n-1$ vertices. The edge count is $3n-6-4+1 = 3(n-1)-6$.
- If $d = 5$, label the link $0,1,2,3,4$ in order. A chord is an edge $i\,(i+2)$ with indices modulo 5. The five ways to triangulate the pentagon by two non-crossing chords are the fans
  $$
  \tau_i = \bigl\{\, i\,(i+2),\; i\,(i+3) \,\bigr\}.
  $$
  Neighbouring fans are disjoint: $\tau_i \cap \tau_{i+1} = \emptyset$. Any non-crossing set $F$ of chords has size at most 2, and if it has size 2 it equals some $\tau_j$. The chords already present are such a set, so they are contained in some $\tau_j$. The fan $\tau_{j+1}$ uses neither of them. Adding that fan across the face left by $v$ produces a simple spherical triangulation $T^\star$ on $n-1$ vertices. The edge count is $3n-6-5+2 = 3(n-1)-6$.

In every case, $T - v$ is a spanning subgraph of the graph that the induction colours. A proper colouring of that graph restricts to a proper colouring of $T - v$.

Two chords cover at most four vertices of a 5-cycle. At least one link vertex receives no new chord, and its degree in $T^\star$ is one less than its degree in $T$. If that vertex had degree 5, then $T^\star$ has a vertex of degree 4. The icosahedron realises this: every link vertex has degree 5, so $T^\star$ leaves the minimum-degree-5 class. The same drop happens for any degree-5 vertex whose link is entirely degree 5, since five vertices cannot all be endpoints of two chords.

## Degree 3

Let $\deg(v) = 3$. By the completion step, $T - v$ is a spherical triangulation on $n-1$ vertices. The inductive hypothesis supplies a proper 4-colouring. The link is a triangle and uses at most three colours. Give $v$ a missing colour. The new colouring lives on $T$. The only smaller graph in the call is $T - v$. The vacancy hypothesis is not used.

## Degree 4

Let $\deg(v) = 4$, with link $a,b,c,d$ in order. Build $T^\star$ on $n-1$ vertices by adding one missing diagonal, say $ac$. The inductive hypothesis supplies a proper 4-colouring of $T^\star$, which restricts to $T - v$.

If $a,b,c,d$ use at most three colours, give $v$ a missing colour. The new colouring lives on $T$.

Suppose they use four colours. Permute the names of the colours so that
$$
c(a)=0,\; c(b)=1,\; c(c)=2,\; c(d)=3.
$$
The edge $ac$ belongs to $T^\star$ and not to $T$. The Kempe argument is run in $T - v$.

Let $H_{13}$ be the subgraph of $T - v$ on colours 1 and 3, and let $H_{02}$ be the subgraph on colours 0 and 2.

**The neighbours $b$ and $d$ lie in different components of $H_{13}$.** Exchange colours 1 and 3 on the component of $b$. Then $b$ receives colour 3 and $d$ keeps colour 3, while $a$ and $c$ keep 0 and 2. The link uses $\{0,2,3\}$. Give $v$ colour 1.

**The neighbours $b$ and $d$ lie in the same component of $H_{13}$.** Let $P$ be a simple $1$–$3$ path in $T - v$ from $b$ to $d$, and let $\Gamma$ be the cycle $v\,b\,P\,d\,v$. The rotation at $v$ is $va,vb,vc,vd$. The two edges $vb$ and $vd$ divide a neighbourhood of $v$ into two wedges, one containing the initial segment of $va$ and the other the initial segment of $vc$. The cycle $\Gamma$ is a simple closed curve, so these two local sides lie in different components of the complement of $\Gamma$. Thus $a$ and $c$ lie in different regions. Any $0$–$2$ path from $a$ to $c$ in $T - v$ avoids $v$ and would have to meet $\Gamma$ in a vertex of $P$. Every vertex of $P$ has colour 1 or 3. So no such path exists: $a$ and $c$ lie in different components of $H_{02}$.

The edge $ac$ is a $0$–$2$ edge of $T^\star$, so the same swap inside $T^\star$ would recolour $a$ and $c$ together and the link would still use four colours. The swap is performed in $T - v$, where $ac$ is absent. Exchange colours 0 and 2 on the component of $a$. Then $a$ receives colour 2 and $c$ keeps colour 2, while $b$ and $d$ keep 1 and 3. The link uses $\{1,2,3\}$. Give $v$ colour 0. Vertices $a$ and $c$ are non-adjacent in $T$, so sharing colour 2 is proper.

In both branches the new colouring lives on $T$. The smaller graph named by the induction is $T^\star$. The vacancy hypothesis is not used. This is the ordinary degree-4 reduction: one Kempe swap on a single pair, with the Jordan split supplying the other pair. It is not the degree-5 Kempe argument, and it does not chain two swaps.

## Degree 5

Now every vertex has degree at least 5, and $v$ is a vertex of degree 5. This is the only case that quotes the hypothesis.

Build $T^\star$ on $n-1$ vertices by the pentagon fan above. The inductive hypothesis supplies a proper 4-colouring of $T^\star$. Its restriction $\gamma$ is a proper 4-colouring of $T - v$.

The graph $T$ has minimum degree at least 5, and $\gamma$ is a proper 4-colouring of $T$ minus one vertex. The hypothesis applies to the pair $(T, \gamma)$. Its sequence of slides and Kempe swaps ends at a hole whose link uses at most three colours, and the missing colour on that hole is a proper 4-colouring of $T$.

That is the colouring asserted by the theorem. The inductive call inside this step is the colouring of $T^\star$, which has fewer vertices. The hypothesis is not derived from that call. It is the standing assumption, applied to $T$.

## The graph the new colouring lives on

In every case the colouring produced for the inductive claim is a colouring of $T$.

- Degree 3: it is the colouring of $T - v$, plus a colour at $v$.
- Degree 4: it is a colouring of $T - v$, possibly after one Kempe swap in $T - v$, plus a colour at $v$. The auxiliary diagonal need not stay properly coloured, because it is not an edge of $T$.
- Degree 5: it is the colouring of $T$ produced by filling whichever hole the assumed sequence reaches. The chords of $T^\star$ are not edges of $T$. Slides and swaps are performed in deletions of $T$, and they are not required to preserve those chords.

$T^\star$ is coloured completely, on $n-1$ vertices, and then discarded. It is not the graph that receives the filled colouring. The sentence in the hypothesis, that the fill colours a triangulation with one more coloured vertex, compares $T$ with the deletion: both have the vertex set of $T$, and the fill colours the hole that was blank.

## Why the smaller instance is $T^\star$

A slide replaces a colouring of $T - h$ by a colouring of $T - u$ for a neighbour $u$ of $h$. The underlying triangulation is still $T$, the order is still $n$, and $n-1$ vertices are still coloured. That pair is a later state of the single sequence granted by one application of the hypothesis to $(T,\gamma)$. It is not a new instance, and the inductive claim is not applied to it.

The smaller graph is $T^\star$, order $n-1$, built from the original degree-5 link before any slide. What the induction applies to $T^\star$ is 4-colourability. The vacancy hypothesis does not apply to $T^\star$ merely because $T^\star$ is smaller: $T^\star$ may have a vertex of degree 4, and the hypothesis is stated only for minimum degree at least 5.

The hypothesis is applied to a smaller triangulation exactly when the recursive colouring of some auxiliary graph meets one. The recursion is on the number of vertices. Every such meeting has order strictly less than the graph whose auxiliary completion produced it. On orders at most 11 the recursion never meets one. The first application is the outermost fill of a 12-vertex triangulation, from an 11-vertex $T^\star$ that the degree-3 and degree-4 steps colour with no hypothesis at all. A later triangulation may, deeper in its own $T^\star$, reduce to that 12-vertex case or to another minimum-degree-5 triangulation of intermediate order. Each of those calls is on a graph with fewer vertices than the graph that called it.

## If the hole degree rises above 5

A slide moves the hole to a neighbour. The degree of the new hole is the degree of that neighbour in $T$, which the slide does not change. Minimum degree 5 allows neighbours of degree 6, 7, 8, and higher.

This rise occurs. On Florek's $G_8$, order 18, the belt vertices have degree 5 and the poles have degree 8. In the population-$(2,5,5,5)$ component, the link of belt vertex 0 is $(1,2,3,4,5)$ with colours $(0,1,2,1,3)$, so colour 2 occurs once, at the pole 3, and the slide $0 \to 3$ is legal. The pole of degree 8 becomes the hole. The record is `hole-support.md`. The same note records that this slide does not by itself free a colour. That is a fact about one component. The hypothesis, if it holds, may continue with further slides and Kempe swaps.

After the hole has degree greater than 5, the inductive step does not have a degree-5 deletion at the current hole, and it does not take one. The degree-5 vertex $v$ was used to build $T^\star$, and that appeal is finished before the sequence starts. The fill is the last sentence of the hypothesis: a link that uses at most three of the four colours has a missing colour, at any degree. Restarting the induction at the new hole would triangulate a face of length greater than 5, colour another graph of order $n-1$, and obtain a colouring of a deletion of $T$. It would not colour the remaining vertex. The degree-5 deletion that justified $T^\star$ is still the one the induction used; the moved hole does not replace it and does not need a successor.

## The circular variant

The following argument is circular. Fix $T$ and induct on the number of blank vertices, or induct on the vacancy statement itself. From a colouring of $T - h$, a slide produces a colouring of $T - u$. Quoting the statement for $T - u$ quotes the same order. Filling then colours $T$, which has the same vertices as the graph just named. Nothing in that call is a smaller triangulation. The existence of the sequence has been assumed in the form of an inductive hypothesis applied to the graph it was supposed to prove.

The smallest non-circular variant is the proof given above. Induct only on 4-colourability, and only on the number of vertices, over every spherical triangulation. Base the tetrahedron. Prove orders 5 through 11 by the degree-3 and degree-4 steps. At minimum degree 5, colour the $(n-1)$-vertex completion $T^\star$ by induction, restrict to the degree-5 deletion, and apply the vacancy hypothesis once, as an assumption, to that same $T$. Do not apply it again when the hole moves.

An induction whose class is only the minimum-degree-5 triangulations, based at the icosahedron, does not close either. The completion $T^\star$ of its degree-5 face has a vertex of degree at most 4 whenever the missed link vertex had degree 5, which is forced on the icosahedron. That $T^\star$ is not in the class, so the inductive hypothesis of the subclass does not colour it. Enlarging the class to every spherical triangulation, with the tetrahedron as base, is the repair. The filled graph of the top call is still $T$, and that is legitimate because the shrinking call is the colouring of $T^\star$, while the vacancy statement is not being proved.

## Scope

The degree-3 and degree-4 steps prove that every spherical triangulation on at most 11 vertices is 4-colourable, with no vacancy hypothesis. From order 12 upward, the theorem stands exactly where the hypothesis stands.

The argument does not use Florek's invariants, a fixed pole hole, Meyniel's theorem on 5-colourings, or a bound on the number of moves. PaperReading records that those theorems allow intermediate fifth colours, delete a pole rather than a belt vertex, or stop at even degrees. None of them is this induction.

The hypothesis allows an arbitrary finite mixture of slides and Kempe swaps. A single Kempe swap, and in some components a pair of them, is already known to be too little (`LibraryPlan.md`, `two-kempe-kill.md`). This note does not remove that gap. It says what follows if a sequence of unrestricted length is granted.

## Feasibility

Feasibility of the deduction, given the hypothesis: **High**. The descent is the order of an explicitly built triangulation, the degree-4 swap is one Jordan split, and the vacancy statement is quoted only as an assumption about the graph being coloured.

Feasibility of the same write-up with the icosahedron as base and the class restricted to minimum degree 5: **Low**. The completion of the deleted face leaves the class.

Feasibility that the vacancy hypothesis itself holds for every minimum-degree-5 triangulation: untouched. This note does not search and does not score it.

## Next steps

1. Formalise the degree-3 deletion and the degree-4 Jordan split on their own. They are the whole proof through order 11, and the colouring of every auxiliary $T^\star$ that has a vertex of degree less than 5.
2. State the hypothesis with the hole unrestricted in degree. A legal slide already reaches degree 8 on $G_8$, and the fill clause does not require the final hole to have degree 5.
3. Keep one application of the hypothesis per triangulation. A later hole of the same $T$ is a state of that application, not a place to build a second completion.
