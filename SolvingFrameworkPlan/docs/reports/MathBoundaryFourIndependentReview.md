# Independent review: degree-four boundary reduction and mobility bridge

Math, four-connected research team, 5 October 2026. Independent hand review of the frozen `MathBoundaryFourResearch.md` and `MathMobilityShortFillBridge.md`. No enumeration or new computation. Recommendations are for root Math acceptance, not a Navigator status change.

## Fixed fan and protected conversion

The boundary-degree-four good-pair theorem is sound. In a four-connected triangulation all five fans at an off-face degree-five root x are legal. Choosing the fan whose apex is the degree-four neighbour a fixes the pair before seeing a colouring. Every admitted colouring makes a singleton by the original link edges plus the fan chords.

The auxiliary slide x→a and the at-most-one-swap degree-four fill form an unrestricted mixed path of length at most two. Applying the compiled M3 theorem gives a pure path of length at most two at the original hole x. That path is permitted in the protected-face problem even though its auxiliary witness visited a forbidden hole: the actual resulting path never changes its hole. Boundary colours may change, which the statement allows. There is no illicit use of a forbidden slide as part of the final permitted path.

The universal quantifier is preserved: the construction works for each start admitted by that same preselected fan. The conclusion is stronger than merely finding one extendible colouring.

## Every-start three-swap bridge

The bridge theorem is sound on any finite simple spherical triangulation. If a degree-five deletion state does not fill within one swap, the independently checked mobility theorem reaches any chosen neighbour a by an optional swap at x followed by a slide. When a has degree at most four it fills after zero or one further swap. The suffix starting immediately after the optional preparatory swap has mixed length at most two, so M3 applies with original hole x. Prepending the preparatory swap gives a pure fill of length at most three.

This is a legitimate suffix conversion, not a claim that every mixed three-move fill has a three-swap counterpart. The initial optional swap leaves a proper state at x, and M3 is applied to that current colouring. For an already-singleton a, no prefix swap is needed and the bound is two.

Consequently every legal fan at a degree-five root adjacent to degree at most four is good, and every such fan is protected-face good when its root is off the protected face. The fixed apex-a fan gives the sharper two-swap bound.

The degree-five-region transfer is also sound. A predetermined path in the off-face degree-five region is followed one edge at a time. At each current colouring mobility either produces a fill immediately or actually moves to the next root. All holes stay off the face. On reaching a root adjacent to a degree-four boundary vertex, use the established pure fill. This transports fillability for arbitrary current states, not fan admission or bad-component labels. Thus every legal fan at every root in that region is protected-face good.

## Order-eleven annulus exclusions

The three degree signatures listed exhaust order eleven. With eight off-face vertices, the identity n5−H=S−6 and S≥13 imply S≤14. For S=13 there are seven degree-five vertices and one degree-six vertex; for S=14 all eight are degree five. The boundary signatures are respectively (4,4,5), (4,4,6), and (4,5,5).

The ring vertices in all three cases are distinct. Opposite-edge vertices x,y,z are distinct because a repeated vertex would create K4; any other coincidence either creates K4 or a second off-face common neighbour of a boundary edge, whose triangle would be nonfacial. The degree-four, degree-five, and degree-six boundary links force the stated faces. Their unions form actual annuli with no hidden vertices, and boundary degrees are exhausted. Therefore remaining vertices can attach only to the ring or each other.

The capacity comparisons are correct:

- (4,4,5): ring capacity is at most six if the unique degree-six vertex is on the four-cycle; the four remaining degree-five vertices require at least eight attachments. If the degree-six vertex is among the four remaining vertices, ring capacity is five and at least nine attachments are required.
- (4,4,6): the five-cycle ring has capacity seven; the three remaining degree-five vertices need at least nine attachments.
- (4,5,5): the same five-cycle capacity seven versus required nine applies.

The upper bounds of six mutual edges on four remaining vertices and three on three remaining vertices use only simplicity, so they are safe even before exploiting four-connectivity. Extra ring diagonals lower capacity and cannot repair the contradictions. The argument proves that every four-connected member of the class has order at least twelve, not merely that a failure does.

## Failures with degree-four boundary

The order-thirteen lower bound for a failure with a degree-four boundary vertex follows from the good-pair theorem and curvature. With exactly one such boundary vertex, its two off-face neighbours must both have degree at least six, while boundary degree sum at least fourteen forces at least eight degree-five vertices. With two degree-four boundary vertices, the union of their off-face neighbours is exactly the three distinct opposite-edge vertices; all must have degree at least six, and boundary sum at least thirteen forces at least seven degree-five vertices. Either way there are at least ten off-face vertices, hence order at least thirteen.

For an order-twelve failure there can be no degree-four boundary vertex. All twelve global degrees are then at least five, and the total degree 60 forces all to equal five. This necessary signature is correctly not presented as a classification or a resolution of that case.

## Review conclusion

Recommend accepting all scoped theorems and exclusions above as hand arguments. The bridge eliminates every off-face degree-five region meeting a degree-four boundary neighbour. Remaining failures may still have a higher-degree frontier around every such region, or have no degree-four boundary vertices at all. These results do not establish VH_C or VH∃.
