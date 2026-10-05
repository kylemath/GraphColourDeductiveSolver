# Pre-meeting: interface

Interface team, 5 October 2026. Three speakers. The positions are already written; this discussion fixes the outline of the joint page.

## The third vertex

**Gluer.** The sentence I will not let onto the joint page is the one that says the excursion replacement uses all three vertices of the clique. That sentence is not in the component-restriction paragraph. The paragraph says: replace each excursion through the far side by a path of length zero or one in the interface; the endpoints lie on the interface and carry the selected colours; if they are distinct, they are adjacent in the clique; properness makes those colours distinct, so the interface edge lies in the same bichromatic graph. The path has two endpoints. My line check names an earlier sentence as the first use of the third vertex: every pair of vertices of $F$ is adjacent in both sides, because the intersection is the triangle and both sides are induced on their closed vertex sets. Once that edge is in hand, the replacement of one excursion uses that edge alone. The third vertex receives the colour outside the chosen pair, and it lies on no path of those two colours. My closing line already says so. Calling the replacement a use of all three vertices pastes the clique sentence and the path sentence together.

**Adversary.** The attack I actually ran was an attempt to drop the third vertex out of the shortcut while the hole was still off $F$. It failed. All three vertices are coloured. Distinct ends of an excursion are adjacent. Properness puts the interface edge in the bichromatic graph, and the replacement lies in the near side. If your joint page says the third vertex is idle, you are describing the path. You are not describing the sentence that puts the edge into both sides. Drop the clique sentence and the shortcut has nothing to substitute for the excursion. I will sign "idle on the path." I will not sign "unused."

**Gluer.** Then the page names one sentence, the adjacency of every pair, and says in the next sentence that the path does not contain the third vertex. Those are different claims. The misquoted line treats them as one claim.

**Adversary.** Agreed, provided the page also says what happens when the hole is the third vertex. My section 2 is not your open item (99). With the hole at $f$, the surviving interface is the edge $pq$. For the pair $\{0,3\}$ that edge carries $\{0,2\}$, and there is no $\{0,3\}$-path through the far side from $p$ to $q$ to replace. For the pair $\{0,2\}$ the ends carry the selected colours and $pq$ is the replacement. The shortcut still returns a path in the side. The sentence that fails is the target sentence: a $3$-colour link on $N_A(f)$ is a target of the side, and the five-vertex link is the target of $T$. Your (99) leaves the match "untouched." The Kempe half is not untouched. The slide half is worse than untouched: it is illegal.

## The coloured link

**Adversary.** Take $F=\{f,p,q\}$, $\deg_T(f)=5$, $\deg_A(f)=3$, $\deg_B(f)=4$, cyclic order $(p,a,q,b_2,b_1)$, colours $(0,1,2,1,3)$. The $A$-link uses three colours. The $T$-link uses four. There is no edge from $a$ to $\{b_1,b_2\}$. Colour $1$ occurs at $a$ and at $b_2$. The slide $f\to a$ is legal on the side and illegal in $T$. A slide is a different move from a Kempe swap. The joint page says that in one sentence, and then it does the Kempe case split at the fixed hole. I asked whether every proper colouring of $T-f$ in which $\{p,a,q\}$ uses at most three colours reaches, by Kempe swaps at this fixed hole, a colouring in which the five-vertex link uses at most three colours. The page answers that. It does not reprint the question.

**Gluer.** An apex on $F$ is not the interior lemma. The neighbourhood identity is for a vertex off $F$, and the interior slide lands off $F$. If the page imports my (94), which makes the apex slide legal in $T$ by copying the fan, it has to stop when the apex lies on $F$. Your colouring is the stop: the colour that is unique on $(p,a,q)$ is repeated on the five-vertex link.

**Connectivity.** The bipyramid in my note already splits the two postconditions, and both poles have degree $3$. It sits outside the minimum-degree-$5$ class. It does not answer a degree-$5$ link. If the joint page treats that order-$5$ colouring as a substitute for the five-vertex link, I will not sign it. Use the bipyramid only to show that degree $4$ occurs for a cut vertex. The degree-$5$ case is the adversary's colouring.

**Adversary.** Then the case split is on that colouring, for an arbitrary interior consistent with the link, or on one finite schematic in which the blocking paths are written as vertex lists. I want the page to say what the outcome does to the question above. A schematic that stops at "one swap fails," without saying whether a sequence at the same hole still reaches, dodges the question I wrote.

**Gluer.** And a schematic that is not minimum degree $5$ is a certificate about this coloured link. It is not a failure. The page says so next to the vertex list.

## The cut

**Connectivity.** I am not signing the degree line on the minimal-counterexample page,
\[
\deg_T(f)=\deg_A(f)+\deg_B(f)-2\ge 5.
\]
The arc count gives $\deg_A(f)\ge 3$, $\deg_B(f)\ge 3$, and $\deg_T(f)=\deg_A(f)+\deg_B(f)-2\ge 4$. The arithmetic $3+3-2$ is $4$. The triangular bipyramid attains $4$. The bound $5$ is the minimum-degree hypothesis of the class, read off the vertex itself, and it is a different sentence. Inside that class a cut vertex has degree at least $5$, so the side degrees $3$ and $4$ are the least split that the class allows. The signed theorem keeps $\ge 4$.

I checked the three structural claims the same way, and I want them on the page as checked claims, not as a citation of my note. Each vertex of a $3$-vertex cut meets every component: if $a$ missed $C_1$, then $\{b,c\}$ would disconnect $T$. There are exactly two components: $b$ and $c$ both lie on the link of $a$, both arcs are nonempty, each arc lies in one component, and a third component would have no arc on which to meet $N(a)$. The triangle is non-facial: $b$ and $c$ are not consecutive at $a$, and a face bounded by $abc$ would be a face at $a$. If any one of those steps is wrong, the joint page replaces it and says so. If they stand, the page signs the equivalence for order at least $5$: the $3$-vertex cuts are exactly the separating triangles, so "no separating triangle" and "$4$-connected" are the same property. $K_4$ is a separate sentence. Order $4$, no $3$-vertex cut, no separating triangle, not $4$-connected, every degree $3$, outside the class.

**Gluer.** My hypotheses (8) and (9) wrote the vertex intersection and the graph union. They did not say that $A$ and $B$ are induced. The shortcut needs the interface edge to lie in the near side. Your induced subgraphs put all three edges in both sides. The joint page uses that reading, and it attributes it to the cut, not to a silent upgrade in my (32).

**Connectivity.** Yes. And the Jordan converse, that a non-facial $3$-cycle separates, stays off the equivalence. Parts (A) and (B) already match the cut in the definition. I will not have the page pretend the converse is load-bearing.

**Adversary.** The degree-drop configuration is still a gap, and I will not let the page close it by mood. If $\deg_A(f)=3$ with link $(p,a,q)$, the opposite disc of $(p,a,q)$ is where the rest of $A$ sits. Whenever that disc contains a vertex, $(p,a,q)$ separates it from $f$ and from $B$. Least order hands a minimum-degree-$5$ inner completion a good pair. Carrying the pair into $T$ is the interior lemma at the inner triangle, or a hole on that triangle. The degree-$3$ step stops at a colouring of $A$. If the page cannot finish the carry, the carry stays open. $H_2$ does not touch this configuration: both completed sides of $H_2$ have minimum degree $5$, and the witness stays off the interface.

**Gluer.** $H_2$ is one short paragraph. It is a success with a separating triangle. The paragraph exists so that nobody writes "a separating triangle is a failure" underneath a signed cut theorem. The degree histogram and the trivial automorphism group stay in your note.

**Connectivity.** One paragraph. My (A) already says $H_2$ is not $4$-connected. The joint page does not need a second proof of that.

## What the page is for

**Adversary.** A smallest failure has no interior witness. Your lift is why. The page says the remaining way a separating triangle can still sit there: a hole on the interface, where the side link is a proper subset of the link in $T$, or a side whose vertices of degree less than $5$ all lie on $F$, with the inner carry unfinished.

**Connectivity.** The size-$4$ count is my next sentence, and it is not this page. Leave it open in one line.

**Gluer.** Then the outline is the lift, the signed cut, the case split at $f$, the degree-drop with the carry open if it will not close, the $H_2$ paragraph, and the sentence about a smallest failure. Feasibility ratings at the end, in the allowed words. No census and no new order.

## Sentences the joint page will assert

1. For $v\in A\setminus F$, the neighbourhoods $N_T(v)$ and $N_A(v)$ agree as sets and in cyclic order.
2. A Kempe step whose hole lies in $A\setminus F$ lifts: each excursion through $B\setminus F$ is replaced by a walk of length $0$ or $1$ on the clique edge of its ends, and the global component restricts to one whole component of the side, or to the empty set.
3. The first sentence that uses the third vertex of $F$ is the sentence that every pair of vertices of $F$ is adjacent in $A$ and in $B$. The replacement path does not contain that vertex.
4. The sentence "the replacement uses all three vertices of the clique" does not match the component-restriction paragraph, and the joint page will not adopt it.
5. An interior slide, landing in $A\setminus F$, lifts because the links agree, so a colour that occurs once on the side link occurs once on the link in $T$.
6. An apex on $F$ is not this lemma.
7. Under the interior-witness hypothesis, $(r,\tau)$ is a good pair of $T$.
8. For a spherical triangulation of order at least $5$, each vertex of a $3$-vertex cut meets every component, the deletion has exactly two components, the induced triangle is non-facial, and $\deg_T(f)=\deg_A(f)+\deg_B(f)-2\ge 4$. None of these four steps is replaced unless the check finds it wrong.
9. The $3$-vertex cuts are exactly the separating triangles, so "no separating triangle" and "$4$-connected" are the same property. $K_4$ is recorded separately.
10. In the coloured link $(p,a,q,b_2,b_1)=(0,1,2,1,3)$, the slide $f\to a$ is illegal in $T$ because colour $1$ occurs twice.
11. The page decides the fixed-hole Kempe question by a case split, and, if one swap does not fill an arbitrary interior, by a finite schematic with every vertex, every edge, the colouring, and the blocking paths as vertex lists, together with a sentence that says what that schematic does to the question.
12. Whenever the opposite disc of $(p,a,q)$ contains a vertex, $(p,a,q)$ separates that vertex from $f$ and from $B$.
13. $H_2$ carries an interior witness. A separating triangle occurs on a success.
14. A smallest failure has no interior witness on any separating triangle. The remaining way such a triangle can still occur is a hole on the triangle, or a side whose deficient degrees lie on $F$ with the inner carry unfinished.

## Sentences the joint page will leave open

1. Any interior of the coloured link for which the case split does not reach a $3$-colour five-vertex link by Kempe swaps at the fixed hole $f$. The page may not reprint the question in place of an answer; if a case remains, it names the case.
2. The carry of a good pair from a minimum-degree-$5$ completion of the opposite disc of $(p,a,q)$ into $T$. Least order supplies the pair on the completion. It does not, by itself, supply the carry.
3. Whether a smallest failure contains a separating triangle.
4. The count for a vertex cut of size $4$.
