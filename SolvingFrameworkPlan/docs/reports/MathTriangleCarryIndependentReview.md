# Independent review of the triangle-carry research

Math, four-connected research team, 5 October 2026. Independent hand review of `MathTriangleCarryResearch.md`. No new computation or enumeration. This is a review recommendation for root Math, not a Navigator status change.

## Accepted hand arguments

The designated-face triangle reduction and the equivalence of VH_C with its four-connected restriction are sound. The reverse direction is an ordinary induction on graph order, with the designated face changing to the separator on the smaller side. No same-order induction is used. Kempe swaps may recolour the protected face; only holes are protected.

The innermost-side lemma is sound under its expressly stated hypothesis that the entire original T has minimum degree five. A separating triangle G in the completion A has a side away from the open boundary face F. This gives a smaller separating triangular disk of T. Strict decrease follows because G differs from F and consequently at least one vertex of G lies in the original disk interior, or some interior vertices lie outside the smaller disk. In particular its interior cannot equal the original interior. The nonempty exterior of the original disk supplies vertices on the other side in T. The degree-three boundary exclusion and the four-connectivity conclusion then follow as written.

Scope warning: for a general member (T,phi) of C, a disk chosen without reference to phi might enclose low-degree vertices of phi and fail to belong to C. Use a disk on the side away from the original phi, and minimize among such disks, or use the triangle reduction's induction instead. The published innermost lemma states global minimum degree five and does not make this error.

The curvature identity is correct. Its lower bounds of six interior degree-five vertices and order nine are valid but weaker than Proposition 1 and Corollary 2 of `MathFourConnectedResearch.md`: three degree-four face vertices are impossible in this four-connected class, so the sharpened bounds are seven interior degree-five vertices and order ten. The forced order-nine signature is consequently unrealizable in the stated class.

R is a clearly stated **open conditional target**. The implication R ⇒ VH∃ and the equivalence R ⇔ VH_C are proved deductions. Neither constitutes a proof of R, VH_C, or VH∃.

## Four-ring trace: accepted with fixed-colouring scope

For a proper boundary word, an individual colour pair can add exterior merging information only when it meets exactly two opposite boundary vertices. With zero or one boundary vertex no merging is possible. With two adjacent vertices, three vertices, or four vertices, the boundary edges already join all the vertices involved.

For four distinct boundary colours, the only two candidate diagonal bridges use disjoint colour pairs. For the three-colour word (alpha,beta,alpha,gamma), the repeated-colour diagonal can add a bridge only in (alpha,delta), with delta the unused colour; the other diagonal uses (beta,gamma). These pairs are again disjoint. Two such bridges would be vertex-disjoint paths joining alternating endpoints in the exterior disk, impossible by Jordan separation. Thus the three-state upper bound is valid.

For the two-colour word (alpha,beta,alpha,beta), encode four bridge booleans in a matrix whose rows are diagonals and whose columns are the unused colours delta,epsilon. The opposite-corner combinations

- row0/delta with row1/epsilon;
- row0/epsilon with row1/delta

use disjoint colour pairs and are impossible. The allowed Boolean matrices are exactly the empty matrix, four singleton matrices, two same-row doubletons, and two same-column doubletons: nine matrices. Every triple or quadruple contains a forbidden opposite-corner pair. This proves a nine-state **upper bound**; no claim that all nine are realizable is necessary or established.

These booleans completely record additional exterior merging, pair by pair, at the fixed colouring. Shared-unused-colour bridges on different diagonals may intersect, which is why both entries in one column are not excluded. Same-diagonal bridges in two different colour pairs can also coexist.

The component quotient statement is sound: subdivide a global bichromatic path into excursions in A and B; exterior excursions induce the recorded endpoint relation on Q. Conversely every relation used has an actual path in B. A global component's restriction is therefore the union of the A-components joined by this relation. An empty restriction is allowed.

## What the trace does not establish

The trace is not static under Kempe swaps. The nine-state count is not a nine-state transition system, a termination proof, or a four-cut reduction. A global swap must swap every A-component in its merged quotient class; swapping an arbitrarily selected A-component alone generally fails to lift. Any controller must track actual updated exterior connectivity, or derive a valid invariant governing its transformation.

There is a further distinction between counting exterior traces for a fixed boundary colouring and counting the complete boundary/controller state. The latter also needs the boundary word (and any required side-colouring information); the assertion is not that all boundary colourings together have only nine states.

Review conclusion: accept the scoped trace lemmas and the innermost-side deductions as hand arguments; retain R and every proposed four-ring controller as open. Update the curvature target to seven candidates and order ten after root checks the separate boundary-annulus proof.
