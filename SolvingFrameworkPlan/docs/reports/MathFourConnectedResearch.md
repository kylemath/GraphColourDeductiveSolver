# Four-connected core: boundary curvature and targetless components

Math research team, 5 October 2026. **[hand arguments for root review]**. No census, new graph generation, external theorem search, or Lean compilation was performed. This report addresses Creative's `face-avoiding-reduction.md` and its stronger hypothesis VH_C, rather than substituting a bounded move budget for VH∃.

## 1. Precise setting

T is a finite simple spherical triangulation, phi=abc is a designated facial triangle, and every vertex off phi has degree at least five. A permitted state has a hole outside phi and a proper four-colouring of the remaining vertices. Permitted moves are whole-component Kempe swaps, without restrictions on recolouring phi, and singleton slides whose destination is outside phi. A filled state has at most three colours on its hole's neighbourhood.

For the core results T is four-connected. In particular it has no separating triangle, minimum degree at least four, and every triangle is facial. This last conclusion uses the accepted spherical three-cut theorem and the Jordan separation of a nonfacial triangle.

## 2. Three degree-four boundary vertices are impossible

**Proposition 1.** In the above four-connected class, at least one vertex of phi has degree at least five.

**Proof.** Suppose a,b,c all have degree four. Let x be the third vertex of the face opposite phi at edge ab, y the corresponding vertex at bc, and z the corresponding vertex at ca. Each lies outside phi.

The vertices x,y,z are distinct. For example x=y would be adjacent to all a,b,c. Those four vertices form K4; in a four-connected triangulation of order greater than four this is impossible: all four triangles would have to be facial, already forming a closed tetrahedral sphere, leaving no room for any other vertex. Here the class has order at least nine by the elementary curvature bound, so the tetrahedral exception cannot occur.

The neighbour sets are therefore exactly

- N(a)={b,c,x,z};
- N(b)={a,c,x,y};
- N(c)={a,b,y,z}.

The degree-four links force the facial triangles axz, bxy, cyz, besides the three faces abx, bcy, caz opposite phi. In particular xy,yz,zx are edges.

These six triangular faces form an annulus between abc and xyz. Together with the face abc, they form a closed disc with boundary xyz. There are no other vertices in this disc, since the specified triangles are faces. Thus every remaining vertex is on the other side of xyz. If any remaining vertex exists, xyz is a separating triangle, contrary to four-connectivity. If none exists, T has exactly the six vertices a,b,c,x,y,z and is the octahedron; x,y,z then have degree four. This violates the required minimum degree five off phi. Both possibilities contradict the assumptions. ∎

**Corollary 2.** At least seven degree-five vertices lie outside phi, and |T|≥10.

**Proof.** Let n5 be the number of degree-five vertices outside phi, and put

H=sum_{v outside phi, deg(v)≥7}(deg(v)−6).

Euler's identity gives

n5−H = 12−sum_{v in phi}(6−deg(v))
        = sum_{v in phi}deg(v)−6.

Proposition 1 and minimum degree four imply that the boundary degree sum is at least thirteen. Therefore n5=H+sum_{v in phi}deg(v)−6≥7, and the three boundary vertices imply |T|≥10. Equality |T|=10 forces boundary degrees (4,4,5), all seven other vertices of degree five, and no vertex of degree at least seven. This is a necessary signature, not an existence claim. ∎

Consequently, if Creative's triangle reduction is accepted, a smallest VH_C failure has order at least ten. This is stronger than the page's order-seven conclusion and the immediate order-nine bound from four-connectivity. It does not rule out such a failure.

## 3. Only three boundary-adjacent exceptions

**Proposition 3.** Every vertex h outside phi has at most two neighbours in phi. At most three vertices outside phi have two neighbours in phi, one per boundary edge.

**Proof.** Three boundary neighbours would give K4 on {a,b,c,h}, impossible as above. If h is adjacent to two boundary vertices, say a,b, then abh is a triangle. It must be facial. Edge ab already bounds phi on one side and exactly one other triangular face on the other. Thus h must be the unique vertex x opposite ab. The same argument applies to bc and ca. ∎

Call these at most three vertices the boundary exceptions. Every other vertex outside phi has at most one boundary neighbour.

**Corollary 4.** Every unfilled state whose hole has degree five admits at least one permitted singleton slide. If its hole is not a boundary exception, it admits at least two; if its hole has no neighbour in phi, it admits three.

**Proof.** Four colours on five neighbours have multiplicities (2,1,1,1), so exactly three neighbours carry singleton colours. At most two, one, or zero of them respectively can lie on phi. ∎

Thus a bad start cannot be explained by an immediate lack of permitted moves. The open problem is recurrence and escape to a fill, not merely existence of a first slide. Boundary colours are not held fixed in this statement.

## 4. Exact targetless-component closure

Let C be any connected component of the permitted move graph that contains no filled state. Let S be its hole projection: the set of vertices that occur as holes in states of C. Then S is nonempty, lies outside phi, and the induced graph T[S] is connected. The connectedness follows by projecting a move path: Kempe swaps keep the hole fixed and slides traverse edges of T.

**Proposition 5.** In every state (h,c) of C, every neighbour of h outside phi with a singleton colour lies in S. If d=deg(h), then

|N(h)∩S| ≥ max(0,8−d)−|N(h)∩phi|,

with a negative right-hand side interpreted as no restriction.

**Proof.** Every singleton outside phi permits a slide, and its destination must lie in the same move component C, hence in S. Since C is targetless, all four colours occur on N(h). If s of these colours occur once, the remaining 4−s occur at least twice, so d≥s+2(4−s)=8−s. Thus s≥8−d. Removing possible singleton neighbours on phi proves the bound. ∎

Wording correction after independent review: singleton neighbours on phi need not lie in S; the closure claim excludes them, as its proof and displayed inequality already did.

This is stronger than a statement about one selected starting colouring: it holds after every permitted Kempe swap and slide in the entire targetless component.

**Corollary 6 (degree-five tree traps are boundary strips).** Suppose every vertex of S has global degree five. If T[S] is a tree, it has at most three leaves, and every leaf is a boundary exception. Consequently it is either a path or a subdivision of a three-arm tree. Moreover every vertex of S that has no neighbour on phi has internal degree at least three, so there is at most one such vertex in a tree trap.

**Proof.** Proposition 5 gives internal degree at least one at every boundary exception, at least two at every other vertex touching phi, and at least three at every vertex not touching phi. In particular there are no isolated vertices and every leaf is among the at most three boundary exceptions. A finite tree with at most three leaves is a path or a subdivision of a three-arm tree, by the identity L=2+sum_{deg_S(v)≥3}(deg_S(v)−2). At most one vertex can have internal degree at least three. ∎

Without a protected face, a targetless component whose holes all have degree five instead forces minimum internal degree three; if all its holes have degree at most six, it forces minimum internal degree two and hence a cycle. Protecting phi weakens these statements exactly at the three exceptional opposite-face vertices and at vertices touching one boundary vertex. This identifies a concrete obstruction to transplanting an unrestricted movable-hole argument into VH_C.

## 5. Fan incidence: an exact finite hitting formulation

In the four-connected core, all five fans at every degree-five vertex are legal. Indeed any existing link chord would form a nonfacial triangle with the hole: the two link arcs each contain vertices, so the triangle separates.

For a targetless component C and a degree-five vertex v outside phi, define B_C(v) as the set of fan indices i for which C contains a state at v admitted by fan i. Every such state has a four-colour link. Its repeated colour occurs at two nonadjacent link vertices. Precisely the other three vertices are singletons, and precisely the three fans based at those singletons admit that colouring (the accepted apex-singleton classification). Therefore each individual targetless state marks exactly three of the five fans; a component may mark more when several link words occur.

A vertex-and-fan pair (v,i) is phi-good **if and only if** i is absent from every B_C(v) as C ranges over targetless permitted components. Thus VH_C fails exactly when, at every degree-five vertex outside phi, these targetless-component marks cover all five fans.

This reformulation preserves the crucial quantifier: one pair must work for every start. Showing merely that one state fills, or that every component has an available move, does not establish goodness.

## 6. Precise next targets

The new rigorous restrictions suggest two concrete claims worth attacking, without asserting either:

1. Show that a targetless component cannot have a degree-five-only hole projection that is a boundary strip as classified in Corollary 6. A proof would need to exploit Kempe swaps to escape that strip; singleton counting alone stops here.
2. More generally, show that the targetless-component marks cannot cover all five fans at every one of the at least seven degree-five vertices outside phi. This is the exact missing statement for VH_C in the four-connected core. The curvature count supplies seven candidate roots, but no current argument couples their bad components enough to force an uncovered fan.

Neither target assumes a uniform fill length, freezes phi's colours, or applies induction to a same-order deletion state. Higher-degree hole projections remain an additional obstruction; Corollary 6 explicitly does not handle them.

## 7. Boundary-strip tree traps are impossible

**Proposition 7.** Every vertex h of global degree five in the hole projection S of a targetless permitted component satisfies |N(h)∩S|≥2, including the three boundary exceptions.

**Proof.** The only case not already covered by Proposition 5 is a boundary exception h with exactly one neighbour in S. Let its two neighbours on phi be a,b. The triangle abh is facial by four-connectivity, so a,b are consecutive in its link. Every state at h has exactly three singleton neighbours. Their permitted destinations belong to S. Consequently two singletons must be a,b and the third must be the sole neighbour of h in S. The remaining two neighbours outside phi repeat the fourth colour. They cannot be adjacent in the link. Up to reflection and colour naming the link is

    (a,b,u,v,w) = (beta,gamma,alpha,delta,alpha),

with v the sole neighbour in S.

There must be a {delta,gamma}-path Q from v to b in T−h. Otherwise swap that colour component of v: it misses b, and neither colour occurs elsewhere on the link, so this fills the fixed hole, contrary to targetlessness. Take Q simple and close it through h using hv and hb. At h the order (a,b,u,v,w) shows that the resulting Jordan curve separates u from both w and a. A path in colours {alpha,beta} is disjoint from Q and h, since the two colour pairs are disjoint. Therefore the {alpha,beta}-component K of u contains neither w nor a. It contains neither b nor v, whose colours are outside the pair.

Swap K. The link becomes (beta,gamma,beta,delta,alpha). The neighbour w is now the unique alpha on the link, so the singleton slide h→w is permitted: w lies outside phi. This puts w in S, contradicting that v was h's sole neighbour in S. ∎

**Corollary 8.** A targetless permitted component whose holes all have global degree five has a hole projection containing a cycle. In particular all degree-five-only tree traps, including the boundary strips of Corollary 6, are impossible.

This does not prove that a component reaches a fill: a cyclic projection is still allowed, and components may reach higher-degree holes. It does prove that the apparent boundary-only singleton escape obstruction cannot seal a degree-five leaf, because a Kempe swap unlocks a second off-face destination. The argument recolours an unrestricted Kempe component and does not preserve boundary colours as an extra rule.

## 8. The forced order-ten signature is also impossible

**Proposition 9.** Every four-connected member (T,phi) of this class has order at least eleven.

**Proof.** Corollary 2 leaves only order ten to exclude. Its equality conditions give boundary degrees (4,4,5) and all seven vertices outside phi of degree five. Name the degree-four boundary vertices a,b and the degree-five boundary vertex c. Let x,y,z be opposite phi on edges ab,bc,ca. They are distinct as in Proposition 1. The degree-four links at a,b force the facial triangles axz and bxy. The neighbours of c include a,b,y,z and exactly one further vertex w. This vertex is distinct from x, since x adjacent to a,b,c would create a forbidden K4. Its link forces the facial triangles cyw and cwz.

The seven faces abx,bcy,caz,axz,bxy,cyw,cwz form an annulus between abc and the four-cycle x-y-w-z. Together with phi they form a closed disc whose boundary is that four-cycle. The three remaining vertices all lie in the complementary disc.

The ring vertices x,y,z each already have four specified neighbours, and w already has three. Their global degrees are all five, so the total number of edges from the ring to the three remaining vertices is at most 1+1+1+2=5. On the other hand those three vertices each have degree five. They have no edges to a,b,c, whose degrees are already exhausted. At most three edges can join the three vertices to each other, so their total degree fifteen requires at least 15−2·3=9 edges to the ring. This contradicts the upper bound five. ∎

This supersedes the order-ten lower bound, not the seven degree-five candidate bound. It is an elementary hand exclusion of a forced degree signature, not a census or assertion that order eleven is realizable.
