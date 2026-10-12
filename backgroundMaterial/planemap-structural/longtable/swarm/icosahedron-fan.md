# Icosahedron fans

**FILL.** The worst length is 1.

Every proper 4-colouring of every fan completion \(T^\star\), restricted to the icosahedron minus the deleted vertex, reaches a link of at most three colours by one Kempe swap, or is already on such a link. Every such colouring filled inside the cap of 20 swaps and slides.

## The graph

\(T\) is the regular icosahedron returned by `icosahedron` in `inquiry_slide.py`. It has 12 vertices, 30 edges and 20 triangular faces, every degree is 5, and `validate_triangulation` accepts the rotation. The same abstract graph is `icosahedron-fixture.json`: an explicit isomorphism was found. The rotation admits an automorphism sending vertex 0 to every vertex, so one vertex determines the census. The five fans at that vertex were still enumerated separately, and vertices \(1\) through \(11\) were repeated as a check. Every one of those 60 fans has the same orbit count, the same four link patterns, and worst length 1.

The link of vertex 0, in rotation order, is
\[
(8,4,2,5,10).
\]
It is an induced 5-cycle. A fan is a pair of non-crossing chords \(\tau_i=\{i(i+2),\,i(i+3)\}\) on that cycle. All five chord pairs are absent, so all five fans are legal. The fan at apex 8 is the chord pair \(\{8\,2,\,8\,5\}\).

## The completion

\(T^\star\) is \(T-0\) with those two chords added across the pentagon. It is a simple spherical triangulation on 11 vertices: 27 edges, 18 triangular faces, Euler characteristic 2. The degree sequence is \(6,5^8,4^2\). The degree-6 vertex is the fan apex 8. The chord ends 2 and 5 have degree 5. The two link vertices the fan misses, 4 and 10, have degree 4. The degree-3 and degree-4 steps therefore colour \(T^\star\). The census below runs through every proper 4-colouring of \(T^\star\).

Colourings are orbits under renaming \(\{0,1,2,3\}\), in first-occurrence form along increasing vertex labels. There are 8 orbits. The labelled count is \(192=24\times 8\), so each orbit uses all four colours on the eleven vertices and has trivial colour stabiliser. Forgetting the two chords leaves a proper colouring of \(T-0\). Each of the five fans arises from 8 of the 20 deletion orbits at vertex 0, and the union over the five fans is all 20 orbits.

## Link patterns

Read the link from the fan apex and rename colours by first occurrence along the link. Adjacent link vertices have different colours, and both fan chords meet the apex, so the apex differs from the vertices two and three steps along the cycle. The only possible patterns are
\[
(0,1,2,1,2),\quad (0,1,2,1,3),\quad (0,1,2,3,1),\quad (0,1,2,3,2).
\]
The first uses three colours. The other three use four. Each occurs, in two orbits. That is the whole list the fan can impose on an induced 5-cycle, and the enumeration meets every entry.

| Pattern from the apex | Orbits | Colours on the link | Shortest length | Orbits filled by one slide | Slides alone |
| --- | ---: | ---: | ---: | ---: | ---: |
| \((0,1,2,1,2)\) | 2 | 3 | 0 | already filled | 0 |
| \((0,1,2,1,3)\) | 2 | 4 | 1 | 1 | at most 2 |
| \((0,1,2,3,1)\) | 2 | 4 | 1 | 1 | at most 2 |
| \((0,1,2,3,2)\) | 2 | 4 | 1 | 1 | at most 2 |

## Length

A move is one Kempe swap or one singleton slide, on the icosahedron, with the fan chords forgotten. A Kempe swap exchanges the two colours on one bichromatic component of the current deletion and stays at the same hole. A singleton slide, allowed when a neighbour carries a colour that appears once on the current link, writes that colour on the hole and moves the hole to the neighbour. The length of a colouring is the number of moves in a shortest sequence after which the current link uses at most three colours. Sequences were searched to length 20. The move graph has \(12\times 20=240\) colouring orbits and the search closed inside it.

On the two orbits of pattern \((0,1,2,1,2)\) the link of vertex 0 already uses three colours, so the length is 0. The missing colour extends the colouring to \(T\).

On each of the six four-colour orbits, one Kempe swap in \(T-0\) reaches a three-colour link, so the length is 1. Three of those six also have a singleton slide onto a three-colour link. The other three do not: every legal slide from vertex 0 still has four colours on the new link. For those three, slides with no swap finish in length 2, and one swap followed by slides has length 1 because the swap itself fills. The shortest sequence is the single swap.

Recomputed on this rotation, the 20 deletion orbits at vertex 0 split into 10 links of three colours and 10 links of four, and the Kempe distance from every orbit to a three-colour link is at most 1. This agrees with the fixture regression. The fans meet the four-colour side: six of the eight orbits of \(T^\star\) have four colours on the link, so the worst length on the induction's starting colourings is 1.

## A colouring of length 1

Fan \(\{8\,2,\,8\,5\}\), pattern \((0,1,2,1,3)\), the orbit whose three singleton slides all stay on four colours. Vertices \(1\) through \(11\) are coloured
\[
(0,0,1,1,1,2,3,3,3,2,2).
\]
The link \((8,4,2,5,10)\) receives \((3,1,0,1,2)\). All four colours appear. The chords are properly coloured: vertex 8 has colour 3, vertex 2 has colour 0, and vertex 5 has colour 1.

Exchange colours 0 and 2 on the component \(\{2,11\}\). The link becomes \((3,1,2,1,2)\), which uses \(\{1,2,3\}\). Colour 0 is missing. Writing 0 on vertex 0 is a proper colouring of \(T\). The image is a proper colouring of \(T-0\). This is one move.

The three slides from this colouring go to vertices 8, 2 and 10, and each new link still uses four colours. Slides alone can continue. One shortest slide walk is
\[
0\to 2\to 11.
\]
After \(0\to 2\) the link of 2 is \((11,5,0,4,9)\) with colours \((2,1,0,1,3)\). The slide \(2\to 11\) lands on the link \((7,5,2,9,3)\) with colours \((3,1,2,3,1)\). That link uses \(\{1,2,3\}\), so colour 0 fills vertex 11. The walk is proper at both holes and has length 2. The swap fills vertex 0. The slide walk fills vertex 11, as the vacancy hypothesis permits when the hole has moved. The shortest sequence is still the single swap.

## A colouring of length 0

The same fan, pattern \((0,1,2,1,2)\), colours of vertices \(1\) through \(11\)
\[
(0,1,1,0,0,2,3,3,3,1,2).
\]
The link \((8,4,2,5,10)\) receives \((3,0,1,0,1)\). The colours are \(\{0,1,3\}\), so colour 2 is missing on the link. It is used at vertices 6 and 11, neither of which meets vertex 0. The chords again have distinct colours, 3 against 1 and 3 against 0. Writing 2 on vertex 0 colours \(T\).

## Feasibility

Feasibility of this finite reading: **High**. The graph is the icosahedron, the five fans are the complete legal list, and the eight orbits are all of the 4-colourings of \(T^\star\).

The check is the icosahedron. On a larger minimum-degree-5 triangulation, a deletion colouring can fail one Kempe swap. Such a colouring meets this induction when it extends across a legal fan.

## Next steps

1. Repeat the fan restriction on the next minimum-degree-5 triangulations. On the icosahedron every deletion colouring has Kempe distance at most 1, so this order has no long sequence to exhibit.
2. Keep the test on colourings of \(T^\star\), then forget the chords. A starting colouring is one in which every fan chord receives two distinct colours.
3. The length 1 above is the length on this graph. The vacancy hypothesis, for a general minimum-degree-5 triangulation, is untouched.

Recomputed by `backgroundMaterial/planemap-structural/longtable/swarm/icosahedron_fan.py`. The census is in `icosahedron-fan-data.json`.
