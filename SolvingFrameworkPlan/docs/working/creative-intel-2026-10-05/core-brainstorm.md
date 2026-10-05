# Brainstorm: a good pair on the core

Long Table (Creative Intel), 5 October 2026, 17:44 MDT. Working notes only; nothing here is a claim. Literature references are from memory and must be checked before citation.

**The target.** A least failure of the strengthened hypothesis lives in the core:
- 4-connected (accepted);
- no separating 4-cycle (pending review: `interface/trace-game-reduction.md`);
- no non-neighbourhood separating 5-cycle (pending review);
- at most two degree-4 vertices on $\varphi$, each with only degree-$\ge6$ off-face neighbours (Math).

Nothing proves that a core member has a good pair. Every fixed swap budget and every fitted potential has died.

## A. Local lemma at a Wernicke pair (most concrete)

**The input.** Wernicke (1904): every minimum-degree-5 triangulation has a degree-5 vertex adjacent to a vertex of degree 5 or 6. The proof is a tiny discharging argument, not a census.

**Math's precedent.** A degree-5 vertex $x$ adjacent to a degree-$\le4$ vertex $a$ is good with the apex-$a$ fan. Slide $x\to a$, fill there by the degree-4 Jordan argument, and convert the path with M3.

**The target lemma.** A degree-5 vertex adjacent to a degree-5 or degree-6 vertex has a good fan, with its apex at that neighbour. Together with Wernicke this would finish the core. A 5–5 edge is not classically reducible, so the lemma must use global information: Jordan arguments on chains, the structure of starts that come from $T^\ast$, and cyclic 5-connectivity.

**Cheap test.** Do apex-at-neighbour fans at 5–5 and 5–6 edges stay good on all saved and plantri graphs? The bad vertices of $17{:}1$ and $24{:}6406$ are the critical cases.

## B. Topological invariant (Fisk–Mohar degree) — weakened, see `literature-check.md` §3

A colouring maps the sphere onto the boundary of the tetrahedron, and the map has a degree; I recall that Mohar proved Kempe invariance mod 12, following Fisk. With a hole, each tetrahedron face gets a local degree.
- The differences between local degrees are fixed by the link word.
- One global number remains.
- A fill missing colour $k$ forces the three local degrees around $k$ to be equal.

This gives a non-fitted distance-to-fill, and possibly a component invariant if slides respect it. The risk is that the differences are local; the global number is the new part.

**Test.** Compute it on the saved $24{:}7228$ paths and on the order-16 losing kernel.

## C. Wilson-type connectivity of the move graph

Slides behave like moves in a 15-puzzle (Wilson's theorem), and Kempe swaps add mixing.

**Conjecture.** On core members, the components of $M(T)$ are classified by a computable invariant, and every class contains a fill. Plain connectivity is circular, because fills exist only if $T$ is colourable. The useful form ties each component to a class whose fill comes from the inductive colouring of $T^\ast$.

**Test.** Count the components of the full move graph on small core members.

## D. One giant bad component

An unfilled degree-5 state has link pattern $(2,1,1,1)$, so it is a start for the three fans whose apex is a singleton. Math's mobility spreads a targetless component across whole degree-5 regions. A failure may therefore be one targetless component, and then VH∃ is close to the strong form on the core. Such a component is a union of whole Kempe classes at each visited hole. Combine with B or C.

## E. Edge-defect (Tilley's Kempe-locking)

Contract $xy$ instead of deleting a vertex. The defect is a monochromatic edge.

Corollary 3.3 restated in $T^\ast$: VH$(v,\tau)$ holds unless some Kempe class of $T^\ast_\tau$ is **double-diamond-locked** at the two chord edges. In that class, neither chord's diamond tips can be made equal. As I recall, Tilley conjectured that every Kempe-locked triangulation contains a Birkhoff diamond, and verified it to large orders. This needs a literature check.

## F. Hunt for a counterexample (risk control)

Candidate fixtures:
- Tilley's locked triangulations;
- Birkhoff diamonds inside cyclically 5-connected graphs;
- 4-connected variants of the $14k+3$ family.

Each needs a declared WP. This is the cheapest way to avoid investing in a false route.

## G. Smaller

- **Double hole at a 5–5 edge.** The joint link is a 6-cycle, and two adjacent vertices must be coloured.
- **Math's degree-6 3+5 split.**
- **The branching trap.** Holes of degree $\le7$ always have a singleton colour: four colours without one need at least $8$ link vertices. So slides never freeze below degree $8$.

## Order

1. A's test.
2. C's count.
3. A literature check on Tilley, Mohar and Fisk, before B or E.

## First readings (17:46, exploratory, post hoc)

- **A's test is uninformative.** At every degree-5 vertex of every `plantri -m5` triangulation of order $\le18$, every apex-at-5/6-neighbour fan is pure-good: $1307$ of $1307$ (`longtable/explore-vhphi/wernicke_apex.py`). But every pair is good in all saved data, so the test could not discriminate.
- **U is also out for A.** U (each $T^\ast$-class has an unlocked member) fails at $22$ pairs of $17{:}1$, whose vertices all have degree $5$ or $6$. So every fan apex there is a Wernicke neighbour, and U cannot carry the Wernicke lemma.
- **C is answered by saved data, and is circular as a route.** `swarm/vh-exists-check.txt` reports `Mcomp=1` on all $118$ graphs: the full move graph is connected. But a fill exists only if $T$ is colourable, so "connected implies reaches fill" presupposes the conclusion. **Meta-point:** a proof of VH∃ has to construct a path from the $T^\ast$-start. Mixing or counting arguments help only when tied to a locally certifiable target, such as "every component contains an unlocked state", which can be checked without knowing a fill exists.
- **Consequence for A.** A Wernicke lemma would need a structural argument at the 5–5 or 5–6 edge: Jordan arguments plus the slide to the apex. Data cannot rank candidate lemmas while every pair is good. Discriminating statistics are needed: shortest fill length, U, pure versus mixed.


**17:52.** In `literature-check.md`:
- the Mohar–Salas mod-12 invariance needs a three-colourable (Eulerian) triangulation, so it does not apply to minimum-degree-5 graphs, and idea B is weakened;
- Tilley's Kempe-locking is confirmed as the right vocabulary for idea E;
- the Inoue et al. 2026 paper uses obstructing cycles of length $\le5$, the same cut sizes as our trace-game reductions.
