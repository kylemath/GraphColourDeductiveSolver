# Triangle carry: an exact four-connected relative target

Math, triangle-carry research team, 5 October 2026. All results here are hand arguments. No new graph, census, or colouring search was run. This page checks and sharpens Creative's `interface/face-avoiding-reduction.md`; it does not prove VH∃.

## The strengthened hypothesis and its reduction

Let C consist of finite simple spherical triangulations A with a designated facial triangle F, such that every vertex outside F has degree at least five. Say (r,τ) is F-good if r is outside F, has degree five, τ is a legal fan, and every proper colouring of A−r admitted by τ has a finite filling path all of whose holes remain outside F. The pair is chosen before the colouring; the path may depend on the colouring. Kempe components may meet F and change its colours. The condition restricts holes, not swapped vertices.

**[hand] Creative's triangle reduction is valid.** Given (T,φ) in C and a separating triangle F, choose the closed side A not containing the interior of φ. Then A completed by its facial triangle F belongs to C and has fewer vertices than T. An F-good pair lifts to a φ-good pair of T by the accepted interior-path lift. This uses neither prescribed boundary-colour extension nor a same-order induction. The boundary vertices of A may have degrees three or four: membership in C explicitly permits them.

Consequently VH_C is equivalent to its restriction to four-connected members of C. One direction is immediate. For the other, assume the restriction and induct on order. A member with a separating triangle reduces as above; a member without one is four-connected. The low-order K4 exception is absent, since it has an off-face vertex of degree three. This is an equivalence for the strengthened statement, not an equivalence of VH_C with plain VH∃.

## An innermost side already excludes degree-three boundary vertices

**[hand] Lemma.** Let T have minimum degree five and a separating triangle F. Choose a closed triangular disk D bounded by a separating triangle, with nonempty interior and with minimum interior vertex count among such disks. Let A be its spherical completion, and call its facial boundary F. Then:

1. Every vertex in A−F has its original T-neighbourhood and degree at least five.
2. A has no separating triangle.
3. Every vertex of F has degree at least four in A.
4. A is four-connected.

Proof of (2): a separating triangle of A has a side not containing the open face F. That side gives a triangular disk strictly contained in D, with nonempty interior. Its vertices and edges are also those of T, and its opposite side in T contains the nonempty exterior of D. Thus it is a separating triangular disk of T with fewer interior vertices, contradicting the choice. A proper contained disk cannot retain every interior vertex: if its boundary differs from F, some vertex of D−F belongs to its boundary or lies outside it. Two distinct triangles on the same three vertices do not occur in a simple triangulation.

For (3), suppose f∈F has degree three in A, with F={f,p,q}. Its remaining neighbour is a∈A−F, and its three incident faces are fpa, faq, fpq. If A has any vertex other than f,p,q,a, the triangle paq separates f from that vertex, contradicting (2). If there is no such vertex, A=K4 and a has degree three, contradicting (1). Hence degree three is impossible.

Now A has at least five vertices, and the accepted three-cut core gives (4) from (2). The original degree identity can still leave all global separator degrees at least six: the argument has not ruled out these separators. It has identified their innermost completed side more precisely.

## Exact curvature and size of that side

**[hand]** Write I=A−F, let n5 be the number of degree-five vertices in I, and let H be the vertices in I of degree at least seven. Euler's curvature identity gives

n5 = 6 + Σ_{f∈F}(deg_A(f)−4) + Σ_{x∈H}(deg_A(x)−6).

Indeed the boundary contribution is 6−Σ_F(deg_A(f)−4); interior degree-five vertices contribute +1, degree-six vertices zero, and H contributes the negative of the displayed last sum. The total is 12.

Thus an innermost side has at least six interior degree-five vertices, and order at least nine. At order nine the degree sequence is forced to be three boundary vertices of degree four and six interior vertices of degree five. This is a necessary condition, not a claim that this sequence is realised.

## A single sufficient target for plain VH∃

**[hand, conditional] Relative four-connected target R:**

For every four-connected finite simple spherical triangulation A with a designated face F, if every vertex outside F has degree at least five, there is an F-good pair.

**R implies VH∃ on every minimum-degree-five triangulation.** If T has no separating triangle, take any face F and apply R to T. If it has a separating triangle, choose an innermost side A as above, apply R to (A,F), and lift its F-good pair directly to T. There is no need to invoke plain VH∃ on A, and no need to recurse through its low-degree boundary vertices.

This is also the precise four-connected base case of Creative's VH_C statement. Therefore the relevant degree-three boundary cases do not need to be solved first. The base case permits degree four only on the designated face, and it offers at least six degree-five roots outside that face. It still demands that a single root and fan work for every admitted start.

## What is unresolved

R is stronger than the original hypothesis: a prescribed forbidden facial triangle must be avoided by every hole along the selected paths, and the triangulation may have boundary vertices of degree four. The existing minimum-degree-five corpus does not test this class. A proof of ordinary four-colourability or of one extendible colouring supplies neither the universal-start move statement nor its forbidden-face condition.

Curvature guarantees candidate roots, not good roots. Four-connectivity eliminates separating triangles, not long Kempe-chain obstructions. At present there is no termination controller or boundary-degree-four lemma proving R. The accepted fixed-hole theorem cannot be applied to a first landing at a global degree-six-or-higher interface vertex.

The next useful theorem is a face-avoidance mechanism on this four-connected relative class, or an explicit hand obstruction to it. Separating four-cycles require a different interface argument: their boundary is not a clique, so an exterior bichromatic excursion can merge side components. The triangle proof cannot simply be repeated there.

## Four-cycle interface: three external connection states

Here is a small additional structural fact, without a termination claim. Let Q=(q0,q1,q2,q3) be an induced separating four-cycle, let A and B be its two closed disk sides, and let the hole lie in A−Q. Fix a proper four-colouring c of T−h. For each colour pair, encode which boundary vertices are joined by bichromatic paths in B.

**[hand] Trace lemma, for boundary words using at least three colours.** Apart from connections already supplied by the edges of Q, the exterior B can supply a connection across at most one of the two opposite pairs of boundary vertices. Therefore its additional component-merging information has only three possibilities: no diagonal connection, the q0–q2 connection, or the q1–q3 connection.

Proof. If a colour pair meets zero or one vertex of Q, it cannot merge two boundary-touching side components. If it meets two adjacent vertices, their boundary edge already connects them. If it meets three vertices, they form a length-two boundary path and are already connected. If it meets all four vertices, the properly bichromatic boundary cycle connects them all. Only a pair meeting precisely two opposite vertices can add a connection.

If Q uses four distinct colours, each diagonal can be active only in the colour pair of its two ends. These two pairs are disjoint. If Q uses three colours, write its word as (α,β,α,γ). The repeated-colour diagonal can be active only in {α,δ}, where δ is the unused fourth colour: using β or γ includes a third boundary vertex, so the connection is already supplied by boundary edges. The other diagonal can be active only in {β,γ}. Again the pairs are disjoint.

For a boundary word with three or four colours, simultaneous additional connections of both diagonals would be two paths with disjoint colour pairs and hence disjoint vertex sets. They join alternating vertices in the same disk B, which Jordan separation forbids. This proves the scoped assertion.

For a two-colour boundary word (α,β,α,β), retain the full bichromatic boundary partition for each pair. There are four potentially additional bridges, one for each diagonal and each unused colour. A bridge at each diagonal using the same unused colour may intersect, so planar separation alone does not exclude them. The three-state bound above deliberately excludes this case.

There is nevertheless a nine-state upper bound in this two-colour case. Write the unused colours as δ and ε, and record a 2×2 Boolean matrix: rows are the two diagonals and columns are δ,ε. A bridge in row 0, column δ and a bridge in row 1, column ε have disjoint colour pairs and cannot coexist; the same holds with δ and ε reversed. Therefore an admissible matrix is empty (one option), has one entry (four options), has both entries in one row (two options), or has both entries in one column (two options). Any three entries contain a forbidden opposite-column pair. These nine possibilities are an upper bound, not a realisability assertion. Their entries completely specify the additional external component connections for this fixed colouring.

For every word, a global bichromatic component restricts to the union of A-components generated by adding the exterior connectivity relation on Q. This follows by replacing exterior excursions with their recorded endpoint relation; conversely each recorded exterior path is an actual excursion. This is an exact component quotient, not a permission to swap just one merged A-component.

The quotient is useful for a relative four-ring statement, but its trace is dynamic: after a lifted swap the colouring inside B can change, and the recorded connections must be recomputed or proved to transform. Treating the initial trace as fixed is unjustified. No finite-state controller or four-cut reduction is proved here.
