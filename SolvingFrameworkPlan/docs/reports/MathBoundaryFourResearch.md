# Math: a protected degree-four vertex can supply a good pair

5 October 2026. Math / high_degree_landings. Hand arguments for independent review; no enumeration, graph generation, or new colouring search. This follows `MathFourConnectedResearch.md` and uses the accepted apex-singleton fan lemma and the compiled short-fill theorem M3.

## 1. Boundary-degree-four reduction

Let T be a four-connected spherical triangulation and phi a designated face. Every vertex off phi has degree at least five. Suppose a vertex a on phi has degree four and an off-face neighbour x has degree five.

**[hand] Theorem.** The pair consisting of x and its fan with apex a is phi-good. Every admitted deletion start fills at the original hole x within at most two pure Kempe swaps.

All five fans at a degree-five vertex are legal in a four-connected triangulation: an existing nonconsecutive link chord would give a nonfacial, hence separating, triangle through that vertex. In particular the fan with apex a is legal and is chosen before the colouring.

Take any start admitted by this fixed fan at x. The colour of a differs from the colours of all other neighbours of x. Its two adjacent link neighbours differ by original edges, and its two far neighbours differ by the added fan chords. Thus a carries a singleton colour on N(x), and the slide x→a is legal.

After that slide the hole a has degree four. Every proper four-colouring at a degree-four hole in a spherical triangulation fills in zero or one Kempe swap: if all four colours occur on its four-cycle link, the two disjoint-colour opposite locks cannot coexist by Jordan separation, so the unlocked component swap removes one link colour. If at most three occur, it is already filled.

Therefore the original state at x has an unrestricted mixed filling path of length at most two. This path temporarily visits a, but M3 converts it to a pure filling path of length at most two at the original hole x. The converted path never changes its hole, so it is phi-avoiding. Kempe swaps may recolour phi, which is allowed. This proves the required universal statement for every fan-admitted start, not just one colouring.

The conclusion does not depend on preserving boundary colours or allowing a slide onto phi. The forbidden slide is used only as a witness to which the compiled short-fill theorem is applied; the resulting permitted path consists entirely of swaps at x.

**[hand] Corollary.** In any four-connected VH_C failure, every off-face neighbour of a degree-four vertex of phi has degree at least six.

Each degree-four boundary vertex has exactly two neighbours off phi. They are distinct opposite-face vertices at its two incident boundary edges. Thus this restriction adds two specific high-degree vertices per such boundary vertex, rather than merely a total curvature inequality.

The same argument works for any degree-five root with a legal fan whose apex has global degree at most four: slide to that apex, fill there within at most one Kempe swap in the planar triangulation, then apply M3. The protected-face version needs no new theorem about long paths.

## 2. All order-eleven signatures are impossible even as members

**[hand] Proposition.** Every four-connected member (T,phi) of the face-avoiding class has order at least twelve, whether or not it satisfies VH_C.

The already reviewed order bound excludes n≤10. Let n=11. There are eight vertices off phi, of degree at least five. Euler's identity gives

    n5 − H = S − 6,

where S is the sum of the three boundary degrees, n5 counts off-face degree-five vertices and H is the off-face excess above degree six. Four-connectivity gives boundary degrees at least four; the all-four boundary pattern is impossible by the reviewed annulus argument. Since n5≤8, S≤14. Consequently the only cases, up to boundary permutation, are:

- Boundary (4,4,5), seven outside vertices of degree five and one of degree six.
- Boundary (4,4,6), all eight outside vertices of degree five.
- Boundary (4,5,5), all eight outside vertices of degree five.

For S=13, n5−H=7 on eight outside vertices. A vertex of degree at least seven would force n5≤7 and H≥1, contradicting the equality. Thus the one non-degree-five vertex has degree six. For S=14, n5−H=8 forces all eight outside vertices to have degree five.

Name phi=abc, and let x,y,z be the vertices opposite its edges ab,bc,ca. They are distinct. Every vertex adjacent to two boundary vertices must be the unique opposite-face vertex at that boundary edge; otherwise the resulting triangle would be nonfacial. No vertex outside phi is adjacent to all three boundary vertices.

### Case (4,4,5)

Name a,b as the degree-four boundary vertices. Their links force facial triangles axz and bxy. The fifth neighbour w of c is distinct from x,y,z, and its link forces cyw,cwz. The seven specified faces form the same annulus as in the reviewed n=10 exclusion, with inner boundary the four-cycle x,y,w,z. Three boundary vertices and four ring vertices account for seven vertices, leaving four strictly inside the ring.

The ring vertices x,y,z each have four already specified neighbours, and w has three. If all ring vertices had degree five, their total remaining capacity would be five. If the unique degree-six vertex is on the ring, capacity is at most six, while the four remaining degree-five vertices need at least 20−2·6=8 ring edges. If the degree-six vertex is among those four remaining vertices, ring capacity is five, while those four have total degree 21 and need at least 21−2·6=9 ring edges. Here six is the elementary maximum number of edges among four vertices. Neither arrangement is possible. Extra ring diagonals only consume capacity.

### Case (4,4,6)

Again a,b have degree four. The six neighbours of c have order a,b,y,u,v,z, where u,v are distinct new vertices outside phi. Neither equals x, since adjacency to a,b,c is forbidden. Their links force the faces cyu,cuv,cvz. The annulus has inner boundary the five-cycle x,y,u,v,z. This leaves exactly three other vertices.

On this ring x,y,z have four specified neighbours each; u,v have three each. All ring vertices have degree five. Therefore at most 1+1+1+2+2=7 edges can join the ring to the three remaining vertices. Those three all have degree five and at most three mutual edges, so they require at least 15−2·3=9 ring edges. Contradiction.

### Case (4,5,5)

Name a as the degree-four boundary vertex. Its link forces axz. The extra off-face neighbour u of b lies between x and y in b's link; the extra off-face neighbour v of c lies between y and z in c's link. They differ from x,y,z: for example u=z would make z adjacent to all boundary vertices. They also differ from one another, since a shared vertex would be a second common neighbour of b,c besides the unique opposite-face vertex y. The forced faces form an annulus with inner boundary the five-cycle x,u,y,v,z, again leaving three remaining vertices.

The ring vertices x,y,z have four specified neighbours each, while u,v have three. The same capacity-seven versus required-nine contradiction excludes this case.

In each case the annulus uses actual facial triangles, so no hidden vertex can lie in it. Boundary degrees are exhausted, so the remaining vertices have no edge directly to phi. Every other edge from them goes to the ring. This completes the hand exclusion of order eleven.

## 3. Stronger restrictions on failures with degree-four boundary vertices

The good-pair theorem gives more than the member bound when restricting to failures.

**[hand] Proposition.** Any four-connected VH_C failure with a degree-four boundary vertex has order at least thirteen.

If exactly one boundary vertex has degree four, the other two have degree at least five, so S≥14 and n5≥S−6≥8. The two off-face neighbours of the degree-four boundary vertex must both have degree at least six by Theorem 1. They are distinct from the n5 vertices, yielding at least ten off-face vertices and n≥13.

If exactly two boundary vertices have degree four, S≥13, so n5≥7. The union of their off-face neighbourhoods is the three distinct opposite-face vertices x,y,z; all three must have degree at least six. Again there are at least ten vertices off phi and n≥13. Three degree-four boundary vertices are impossible in this class.

Thus any order-twelve failure would have all three boundary degrees at least five. Euler then forces all twelve global degrees to be five. This last necessary signature is not a classification proof or a claim that the order-twelve case is resolved here.

## 4. What advances VH_C, and what remains

The principal advance is Theorem 1, not the small-order count: a degree-four boundary vertex adjacent to a degree-five interior root gives a fixed, legal fan that fills every start within two pure swaps. It removes that entire structural case without any census or long-path termination argument.

The remaining boundary-degree-four case has both off-face neighbours of every degree-four boundary vertex at degree at least six. A naïve deletion of that boundary vertex and addition of a diagonal is not yet a carry proof: the chosen diagonal may have equal-coloured ends in an arbitrary original start. That obstruction is not removed by the new theorem. In the degree-four-neighbour reduction proved here, M3 handles the move restriction directly and no diagonal carry is needed.
