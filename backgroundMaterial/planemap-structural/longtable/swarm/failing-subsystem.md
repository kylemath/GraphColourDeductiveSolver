# Failing-root vacancy slides

**KILL.** Vacancy slides on the published failing roots do not give an all-roots descent.

The witness is the two-swap-stuck orbit at order 17, graph 0, root 9. Its component is the exchange with the two-swap-stuck orbit at root 14. Every slide that leaves that pair lands on a passing root. Roots 4 and 6 are unreachable by a slide. No stuck orbit in the published table reaches $p=0$ by a slide that stays on failing roots.

Replayed from `mass_core.RootState` and the vacancy slide in `inquiry_slide.py`, on the six graphs whose `failing_roots` list in `mass-macro-results.json` is nonempty. Passing roots were not coloured. The script is `swarm/failing_subsystem.py`.

## Witness orbit

Order 17, graph 0, ascii sha256 `1203efa037ee84da877d10d6f94b4d81f4224dab98ffb995de0abb125fb2b3c5`. Root 9 is the deleted vertex. The canonical colouring, in vertex order $(0,1,2,3,4,5,6,7,8,10,11,12,13,14,15,16)$, is

$$(0,1,2,1,3,2,3,0,3,0,1,0,1,2,3,2).$$

This is the published failure witness at that root. Here $p=1$, $q=138$ and $R=1873$, with $R=(6\cdot 17^2+1)p+q$. `descent(i, 2)` returns a witness, so the orbit is two-swap stuck. In the `RootState` enumeration it is orbit 18.

The link of root 9 is $(3,8,14,15,10)$ with colours $(1,3,2,3,0)$. The colours that appear once are at vertex 3 (degree 6), vertex 14 (degree 5) and vertex 10 (degree 6).

## Component

The component is this orbit together with the unique two-swap-stuck orbit at root 14. That colouring, in vertex order $(0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,16)$, is

$$(0,1,2,1,3,2,3,0,3,2,0,1,0,1,3,2),$$

again the published failure witness, with the same rank $p=1$, $q=138$, $R=1873$. In the enumeration it is orbit 21.

The slide that moves the deleted vertex from 9 to 14 recolours 9 with colour 2 and deletes 14. The resulting canonical colouring is the stuck orbit at root 14. The link of root 14 is $(7,13,15,9,8)$ with colours $(0,1,3,2,3)$, so the return slide along vertex 9 reproduces the stuck orbit at root 9. Those are the only two edges of the stuck-orbit digraph on this graph, and the only stuck-to-stuck vacancy slides in the whole published table.

Length-2 slides whose intermediate vertex is not degree 5 were included. From root 9 they run through vertex 3 to passing root 2, and through vertex 10 to passing root 16. From root 14 they run through vertex 7 to passing root 2, and through vertex 13 to passing root 16. Each intermediate also admits the return slide to the starting root, and that return reproduces the same stuck colouring. The degree-5 one-step landings inside the pair are the two edges above, so a further slide is the partner's own edge.

Every slide that leaves the pair lands on a passing root. The pair therefore has no slide, of length 1 or of length 2 through a non-degree-5 vertex, onto a descending orbit or a $p=0$ orbit at a failing root. Roots 4 and 6 do not occur as destinations. Once passing roots are forbidden, the pair is a closed component.

## The other stuck orbits

The published table has 12 failing roots on 6 graphs and 21 two-swap-stuck orbits. The recomputation matches those stuck counts, and each published failure-witness colouring is one of the 21.

Under slides alone, all 21 lie in dead-end components. Nineteen of them are singletons. The slide digraph contains the 2-cycle of the twin, so it is not an acyclic escape to descending orbits, and no orbit reaches a target on failing roots.

| Order | Graph | Root | Stuck orbits | $q$ | Slide component |
| ---: | ---: | ---: | ---: | ---: | --- |
| 17 | 0 | 9 | 1 | 138 | 2-cycle with root 14 |
| 17 | 0 | 14 | 1 | 138 | 2-cycle with root 9 |
| 17 | 0 | 4 | 1 | 143 | singleton |
| 17 | 0 | 6 | 1 | 143 | singleton |
| 17 | 3 | 3 | 5 | 107 | five singletons |
| 17 | 3 | 13 | 5 | 107 | five singletons |
| 20 | 7 | 7 | 1 | 164 | singleton |
| 20 | 7 | 11 | 1 | 164 | singleton |
| 20 | 60 | 3 | 2 | 169 | two singletons |
| 20 | 62 | 15 | 1 | 164 | singleton |
| 20 | 63 | 3 | 1 | 164 | singleton |
| 20 | 63 | 15 | 1 | 164 | singleton |

Roots 4 and 6 of order 17 graph 0 are dead ends of their own, separate from the twin. Their stuck colourings are

- root 4, vertex order $(0,1,2,3,5,6,7,8,9,10,11,12,13,14,15,16)$, colouring $(0,1,2,3,2,0,3,1,0,1,0,3,1,2,3,2)$, $q=143$, $R=1878$;
- root 6, vertex order $(0,1,2,3,4,5,7,8,9,10,11,12,13,14,15,16)$, colouring $(0,1,2,3,1,2,3,0,2,0,3,1,0,1,3,2)$, $q=143$, $R=1878$.

Every one-step slide from either colouring meets a degree-6 vertex. The length-2 continuations land on passing roots: from root 4, on $1,2,12,16$; from root 6, on $0,2,11,16$.

On the other five graphs every one-step degree-5 destination of a stuck orbit is a passing root, and every length-2 destination through a non-degree-5 vertex is a passing root or the cancelling return to the same colouring.

## One Kempe swap, then a slide

The Kempe swap stays at the same root. The slide after it is counted only when the new root is still failing. Length 2 through a non-degree-5 vertex is counted on the same terms.

From the witness, swap colours $1$ and $3$ on the component $\{1,6,13,15\}$. The canonical neighbour at root 9 is enumeration orbit 30, with $q=163$ and $R=1898$. Its link colours leave vertex 14 as a unique colour of degree 5. The slide $9\to 14$ lands on root 14, enumeration orbit 35, colouring

$$(0,1,2,3,1,2,3,0,1,2,0,3,0,1,3,2)$$

in the root-14 vertex order, with $p=1$, $q=163$, $R=1898$. That orbit is descending. The greedy two-swap iteration from it is

$$q=163 \to 147 \to 127 \to 123 \to 106 \to (p=0,\, q=163).$$

The terminal colouring at root 14 is $(0,1,2,3,1,2,3,0,1,0,2,3,1,2,1,0)$. So one Kempe preparation takes the witness out of the closed pair and onto a failing-root orbit whose mass iteration reaches a target. The symmetric preparation at root 14 lands on a descending orbit at root 9 with the same property.

Roots 4 and 6 are reachable on descending orbits only after that preparation, and only by a two-step slide through a degree-6 vertex:

- from root 9, through vertex 3, onto root 4 orbits with $q=163$;
- from root 14, through vertex 7 or 13, onto root 6 orbits with $q=163$.

The first decreasing macro of each of those landings is the stuck orbit at the destination ($q=143$ at root 4 or root 6). Arriving at root 4 or 6 on a descending orbit feeds that stuck orbit.

The same preparation removes every dead end on order 17 graph 0. It leaves the other seventeen stuck orbits untouched. On order 17 graph 3 and on order 20 graphs 7, 60, 62 and 63, every root reached by a Kempe-then-slide from a stuck orbit is a passing root. There is no landing on a stuck, descending, or target orbit at a failing root.

One such survivor is order 17, graph 3, root 3, enumeration orbit 47: colouring

$$(0,1,2,1,3,2,3,0,3,0,2,0,1,2,1,3)$$

on vertex order $(0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16)$, with $p=1$, $q=107$, $R=1842$. Its three unique-colour neighbours are the passing roots 2, 9 and 4. The component is the singleton. The same holds for the other four stuck orbits at that root, the five at root 13, and all seven stuck orbits on the four order-20 graphs.

A Kempe swap that does not leave the root can land on an orbit which is itself two-swap-descending. Those neighbours have larger $R$ than the stuck colouring, so they are not rank descents of it. They are not slide landings. The Kempe distance from the witness to a $p=0$ orbit at root 9 is 3, which is the two-swap failure at that root; that path keeps the deleted vertex fixed.

## Reading of the three labels

Slides alone exhibit a stuck orbit with no path to $p=0$ or to a descending orbit that stays on failing roots. That is the kill.

The slide digraph is not an acyclic system in which every stuck orbit escapes to a descending orbit on a failing root. The twin is a 2-cycle, and the other components have no escape edge of that kind.

No stuck orbit reaches a target by slides that stay on failing roots.

## Next step

An all-roots descent that uses vacancy slides has to send these orbits onto passing roots, or use a different move. One Kempe swap before the slide disposes of order 17 graph 0, including a mass path to $p=0$ at root 14, and still leaves seventeen stuck orbits whose every exiting slide meets a passing root.
