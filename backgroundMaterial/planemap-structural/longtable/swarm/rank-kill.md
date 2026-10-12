# Rank kill on the 21 two-swap-stuck orbits

4 October 2026. Scored on the 12 failing roots in `mass-macro-results.json`. A colouring of $T - r$ is stuck when `RootState.descent(i, 2)` is not `None`. The recomputation finds 21 such orbits, matching each root's published stuck count, and each published failure witness is one of them. Ranks are computed from the current hole, the colouring, the degrees, the boundary colour multiplicities, $q$, the bichromatic components, and the sorted colour counts. They do not read a pass/fail label, a distance to a passing root, or a mass-macro outcome. The script is `swarm/rank_kill.py`.

Legal moves from the stuck colouring, and only these:

- one Kempe swap of one bichromatic component in the current deletion;
- one singleton slide, along a boundary vertex whose colour appears once;
- one slide of length 2 whose intermediate vertex is not degree 5 and whose landing is a degree-5 singleton of that intermediate.

After a slide, $q$ and the boundary colours are recomputed at the new hole, of whatever degree that hole has. Lower tuples are better. A descent is strict.

On a degree-5 root the recomputed $q$ matches `RootState.info`. Every Kempe successor of each of the 21 has strictly larger $q$ than the stuck colouring, and still has four colours on the boundary. No scored slide fills: the boundary of the landing still uses four colours.

## The 9↔14 exchange

Order 17, graph 0, root 9, colouring 18, and root 14, colouring 21, are the published failure witnesses. The singleton slide $9 \to 14$ lands on colouring 21, and $14 \to 9$ lands on colouring 18. Both have $p = 1$, $q = 138$, sorted population $(4,4,4,4)$, four boundary colours, minimum singleton degree 5, and $\mathrm{shortLinks} = 0$. The exchange therefore preserves every rank below. It is a flat 2-cycle.

It is a kill witness only for a rank that also has no other strict descent from these two colourings. For $q$, for $(\#\text{boundary colours}, q)$, for $(d_{\min}, q)$, and for $(\mathrm{shortLinks}, q)$, the slide from root 9 to vertex 3 (degree 6) is a strict descent, and the symmetric slide from root 14 to vertex 7 is a strict descent. Those ranks are killed on a different orbit. The non-increasing population order is killed on the exchange itself; that reading is recorded under the population candidate.

## Verdicts

| Candidate | Verdict | Witness |
|---|---|---|
| $q$ | KILL | 17:3 root 3 colouring 44, $q = 107$, landings $111, 111, 123$ |
| sorted population | KILL | same colouring, population stays $(4,4,4,4)$; pure slides never change it |
| $(\#\text{boundary colours}, q)$ | KILL | same colouring, $(4, 107)$ and every move keeps 4 colours |
| $(d_{\min}, q)$ | KILL | same colouring, $(5, 107)$ and every move keeps $d_{\min} = 5$ |
| $(\mathrm{shortLinks}, q)$ | OPEN | strict drop on all 21; the exchange stays $(0, 138)$ and is refused |

No candidate is walled. Every decreasing move below is a named slide or a named component.

## 1. $q$ — KILL

Six orbits have a singleton slide that lowers $q$. They are order 17 graph 0, roots 4, 6, 9 and 14, and order 20 graph 7, roots 7 and 11. Each drop is a slide through a vertex of degree 6 or 7. From colouring 18 the slides to vertices 3 and 10 both give $q = 126$; the exchange stays at $138$. From colouring 180 the slide to degree-7 vertex 16 gives $q = 108$.

The other fifteen orbits have no legal move with smaller $q$. Witness: order 17, graph 3, root 3, colouring 44, the published failure witness,

$$
c = (0, 1, 2, 1, 3, 2, 0, 3, 1, 3, 2, 0, 3, 2, 0, 1)
$$

on vertices $(0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16)$. Here $N(3) = (0, 2, 9, 10, 4)$ is coloured $(0, 2, 1, 3, 1)$, so $p = 1$ and $q = 107$, and $R = 1842$ with scale $6 \cdot 17^2 + 1 = 1735$. The three singleton neighbours are vertices 0, 2 and 10, all of degree 5, so there is no length-2 slide. Their landings have $q = 111$, $111$ and $123$. The eight Kempe successors have $q \ge 115$; the minimum is colouring 43, by swapping colours $\{1, 3\}$ on $\{1, 4, 5, 8, 9, 10\}$.

The same fifteen are the ten stuck orbits at order 17 graph 3, both at order 20 graph 60, colouring 83 at order 20 graph 62 root 15, and both at order 20 graph 63. At colouring 83, $q = 164$ and the two degree-5 slides land at $q = 164$ again. The degree-6 slide raises $q$ to $195$.

## 2. Sorted colour population — KILL

Let $\pi$ be the non-decreasing 4-tuple of colour counts on the coloured vertices, zeros included. A fill, at most three colours on the boundary of the current hole, is a strict win: the key is $(0, \pi)$ when the hole fills and $(1, \pi)$ otherwise.

A pure slide does not drop this rank. Every singleton slide and every length-2 slide preserves the colour multiset, which the run checks move by move. None of those slides fills, so the key stays $(1, \pi)$ with the same $\pi$.

A Kempe swap can change $\pi$. From colouring 18, swapping colours $\{2, 3\}$ on $\{2, 8, 14, 15, 16\}$ lands on colouring 0 with $\pi = (3, 4, 4, 5)$, and $(3, 4, 4, 5) < (4, 4, 4, 4)$. The symmetric swap from colouring 21, colours $\{2, 3\}$ on $\{2, 8, 9, 15, 16\}$, does the same. Those are the only two stuck orbits on which any legal move changes $\pi$.

Witness: colouring 44, where $\pi = (4, 4, 4, 4)$. All eight Kempe successors keep that tuple, and every slide keeps it. Nineteen orbits are in this position: the fifteen of §1, together with colourings 25 and 27 at order 17 graph 0 and colourings 180 and 18 at order 20 graph 7.

The non-increasing convention, $\pi$ written in non-increasing order, is a kill on all 21, and there the exchange is the witness. Both stuck colourings have $\pi = (4, 4, 4, 4)$, which is already the minimum non-increasing tuple of four parts summing to 16. The Kempe above moves it to $(5, 4, 4, 3)$, which is larger. No other stuck orbit changes its multiset. Slides still preserve $\pi$, and none fills.

## 3. $(\#\text{boundary colours}, q)$ — KILL

The key is the number of distinct colours on the boundary of the current hole, then $q$. A fill is three or fewer colours, which would put the first coordinate at most 3.

Every stuck colouring has 4 boundary colours. Every scored Kempe successor and every scored slide also has 4. The pair therefore decreases exactly when $q$ decreases, and it dies on the same fifteen orbits. On colouring 44 the three slides and every Kempe give $(4, q)$ with $q \in \{111, 123\}$ or $q \ge 115$, against $(4, 107)$ now.

The exchange stays at $(4, 138)$. The slide $9 \to 3$ goes to $(4, 126)$, so this rank does leave the flat cycle. The kill is colouring 44.

## 4. $(d_{\min}, q)$ — KILL

$d_{\min}$ is the least degree among boundary vertices of unique colour. The key is $(d_{\min}, q)$. On a stuck degree-5 colouring there are three such vertices. Every graph here has minimum degree 5, so $d_{\min} \ge 5$.

Colouring 18 has $d_{\min} = 5$ and $q = 138$. The slide to vertex 3 has $d_{\min} = 5$ and $q = 126$, so $(5, 138) \to (5, 126)$. The exchange stays at $(5, 138)$. Colouring 180 has $d_{\min} = 6$, and the slide to vertex 16 gives $(5, 108)$.

The fifteen orbits of §1 already have $d_{\min} = 5$. Their slides and Kempe successors keep $d_{\min} = 5$ while $q$ does not fall. On colouring 44 every landing in the previous sections has $d_{\min} = 5$ and $q \ge 111$.

## 5. $(\mathrm{shortLinks}, q)$ — OPEN

$\mathrm{shortLinks}$ is the number of bichromatic components $K$ with $K$ contained in the boundary and $|K| \ge 2$. The key is $(\mathrm{shortLinks}, q)$. It uses the hole, the colouring, and the components. It does not use a pass/fail label.

The exchange is the flat pair $(0, 138)$ and is refused. Some other legal move is a strict drop from each of the 21. Where several moves share the minimum key, the row is the singleton slide to the smallest vertex. Where the minimum is achieved only by Kempe swaps, the row is the swap of least successor index.

| Orbit | Before | Move | After |
|---|---|---|---|
| 17:0 root 4 colouring 25 | $(0, 143)$ | slide to 3 (degree 6) | $(0, 130)$ |
| 17:0 root 6 colouring 27 | $(0, 143)$ | slide to 7 (degree 6) | $(0, 130)$ |
| 17:0 root 9 colouring 18 | $(0, 138)$ | slide to 3 (degree 6) | $(0, 126)$ |
| 17:0 root 14 colouring 21 | $(0, 138)$ | slide to 7 (degree 6) | $(0, 126)$ |
| 17:3 root 3 colouring 44 | $(1, 107)$ | slide to 10 | $(0, 123)$ |
| 17:3 root 3 colouring 47 | $(1, 107)$ | slide to 4 | $(0, 123)$ |
| 17:3 root 3 colouring 77 | $(1, 107)$ | slide to 0 | $(0, 123)$ |
| 17:3 root 3 colouring 91 | $(1, 107)$ | slide to 2 | $(0, 123)$ |
| 17:3 root 3 colouring 93 | $(1, 107)$ | slide to 9 | $(0, 123)$ |
| 17:3 root 13 colouring 19 | $(1, 107)$ | slide to 14 | $(0, 123)$ |
| 17:3 root 13 colouring 29 | $(1, 107)$ | slide to 12 | $(0, 123)$ |
| 17:3 root 13 colouring 52 | $(1, 107)$ | slide to 6 | $(0, 123)$ |
| 17:3 root 13 colouring 76 | $(1, 107)$ | slide to 7 | $(0, 123)$ |
| 17:3 root 13 colouring 96 | $(1, 107)$ | slide to 16 | $(0, 123)$ |
| 20:7 root 7 colouring 180 | $(1, 164)$ | Kempe $\{0, 2\}$ on $\{0, 2\}$, colouring 145 | $(0, 192)$ |
| 20:7 root 11 colouring 18 | $(1, 164)$ | Kempe $\{0, 3\}$ on $\{0, 5, 6, 7, 8, 9, 10\}$, colouring 19 | $(0, 192)$ |
| 20:60 root 3 colouring 93 | $(1, 169)$ | slide to 4 | $(0, 192)$ |
| 20:60 root 3 colouring 169 | $(1, 169)$ | slide to 0 | $(0, 192)$ |
| 20:62 root 15 colouring 83 | $(1, 164)$ | slide to 14 (degree 6) | $(0, 195)$ |
| 20:63 root 3 colouring 189 | $(1, 164)$ | slide to 11 | $(0, 208)$ |
| 20:63 root 15 colouring 197 | $(1, 164)$ | slide to 16 | $(0, 208)$ |

From colourings 25, 27, 18 and 21 a second slide ties the minimum ($q = 130$ or $q = 126$). From colouring 180 several Kempe swaps tie at $(0, 192)$; colouring 145 is the least successor index. The strict moves from colourings 18 and 21 are the degree-6 slides, so the descent does not travel along the exchange.

On colouring 44 the short component is the boundary edge $\{0, 2\}$, colours $(0, 2)$. The slides to 0 and to 2 keep $\mathrm{shortLinks} = 1$ and raise $q$ to 111. The slide to 10 is the only legal descent, to $(0, 123)$.

This scores the 21 stuck orbits only. It does not say that the same key descends from the landing colourings.

## Feasibility and next step

Feasibility that $q$, the sorted population, the boundary-colour pair, or $(d_{\min}, q)$ descends from every one of these 21 orbits: refuted by colouring 44. The population fact is stable under both sort directions.

Feasibility that $(\mathrm{shortLinks}, q)$ descends from every later colouring on these six graphs: **Low**, speculative. The drops above often raise $q$ while clearing one short chain, and that shape has not been walked past the first move.

Next step: from each of the 21 moves, follow the same strict rule and name the first colouring that has no legal descent. Stay inside the six graphs.
