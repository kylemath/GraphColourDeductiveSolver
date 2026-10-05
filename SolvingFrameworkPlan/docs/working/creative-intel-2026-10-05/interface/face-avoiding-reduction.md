# A face-avoiding hypothesis whose smallest failure is 4-connected

Long Table (Creative Intel), 5 October 2026, 17:00 MDT. A line-1 page for `VHExistsAttack.md`. Math has not reviewed it. No census was run for this page; an exploratory plausibility check is reported separately at the end and labelled.

Background, accepted by Math at 16:45 and 16:59:
- the interior-witness lift (`interior-witness.md` (A)), valid only when every hole stays off the separating triangle;
- the three-cut core: for order $\ge5$, "no separating triangle" is the same as "4-connected";
- the fixed-hole theorem (`fixed-hole-two-swaps.md`), and Math's corollary that every vertex of a separating triangle in a failure has degree $\ge 6$.

Math's 16:45 message leaves four-connectivity of a smallest VH∃ failure open. Two gaps stand in the way of the direct attempt. One is a side path that lands on the triangle at a vertex of degree $\ge 6$. The other is the carry: the completed side need not have minimum degree $5$. This page moves both gaps into the statement. The induction hypothesis is strengthened so that the side's own path is never allowed onto the triangle, and the side's low-degree vertices are allowed exactly where the triangle is.

## Definitions

Let $T$ be a spherical triangulation and $\varphi$ a face of $T$, with vertex set $V(\varphi)$.

- $\mathcal C$ is the class of pairs $(T,\varphi)$ such that every vertex of $T$ off $V(\varphi)$ has degree at least $5$. The vertices of $\varphi$ may have any degree.
- A pair $(v,\tau)$ is **$\varphi$-good** when:
  - $v\notin V(\varphi)$, $\deg v=5$, and $\tau$ is a legal fan at $v$;
  - for every start $c\in S(v,\tau)$, there is a path in $M(T)$ from $(v,c)$ to $F(T)$ every one of whose holes lies off $V(\varphi)$.
- $\mathrm{VH}_\varphi(T)$ says that a $\varphi$-good pair exists. $\mathrm{VH}_\mathcal C$ says that $\mathrm{VH}_\varphi(T)$ holds for every $(T,\varphi)\in\mathcal C$.

**[hand] Degree-5 vertices off the face exist.** $\sum_v(6-\deg v)=12$ (Euler, [cited]). Each vertex of $\varphi$ has degree $\ge3$, so the three of them contribute at most $9$. The vertices off $\varphi$ therefore contribute at least $3$. Each of them contributes at most $1$, so at least three have degree exactly $5$. If $T$ is 4-connected of order $\ge5$, the face vertices have degree $\ge4$ and contribute at most $6$, so at least six degree-5 vertices lie off $\varphi$.

**[hand] $\mathrm{VH}_\mathcal C$ implies VH∃.** A minimum-degree-5 triangulation $T$ is in $\mathcal C$ with any face $\varphi$. A $\varphi$-good pair is a good pair. Theorem A of `vh-exists.md` then gives 4-colourability.

The converse is not claimed. $\mathrm{VH}_\mathcal C$ is a strengthening in two ways: the class is larger, and the paths are constrained.

## The reduction

**[hand] Theorem (triangle reduction).** Let $(T,\varphi)\in\mathcal C$, and let $F$ be a separating triangle of $T$, with closed sides $A$ and $B$ named so that $\varphi$ is a face of $B$. Then:
1. $A$ is a spherical triangulation of order less than $|T|$ in which $F$ is a face, and $(A,F)\in\mathcal C$.
2. Every $F$-good pair of $A$ is a $\varphi$-good pair of $T$.

So $\mathrm{VH}_F(A)$ implies $\mathrm{VH}_\varphi(T)$.

*Proof.*

*Naming.* $\varphi\neq F$, because $F$ bounds no face (`interior-witness.md` (B)). Every face of $T$ lies on exactly one side, so the naming is possible.

*Part 1.* $A$ consists of the faces of $T$ on the $A$-side of $F$, together with the face $F$. This is the standard decomposition, also used in (A). Its order is $|T|-|B\setminus F|<|T|$. A vertex $x\in A\setminus F$ has $N_A(x)=N_T(x)$ (`interior-witness.md` (A), neighbourhoods off $F$). Also $x\notin V(\varphi)\subseteq V(B)$, so $\deg_A(x)=\deg_T(x)\ge5$. The vertices off $V(F)$ in $A$ are exactly $A\setminus F$. Hence $(A,F)\in\mathcal C$.

*Part 2.* Let $(r,\tau)$ be $F$-good in $A$. Then $r\in A\setminus F$, with $\deg_T(r)=\deg_A(r)=5$, and $\tau$ is legal in $T$ (the fan paragraph of (A)). Let $c\in S_T(r,\tau)$. Its restriction to $A-r$ is proper and is proper on $\tau$, so it lies in $S_A(r,\tau)$. By hypothesis, that restriction has a filling path in $A$ whose holes all lie in $A\setminus F$. Lemma (A) lifts this path step by step to a path of $T$ from $(r,c)$ to $F(T)$, with the same holes. Every hole lies in $A\setminus F$, which is disjoint from $V(B)\supseteq V(\varphi)$. So $(r,\tau)$ is $\varphi$-good in $T$. ∎

**[hand] Corollary.** If $\mathrm{VH}_\mathcal C$ fails, then a failure $(T,\varphi)$ of least order has no separating triangle. It has order $\ge 7$, and $T$ is 4-connected.

*Proof.* If $T$ had a separating triangle, part 1 would give a smaller member $(A,F)$ of $\mathcal C$. By minimality it satisfies $\mathrm{VH}_F(A)$, and part 2 would give $\mathrm{VH}_\varphi(T)$. On the order: in $\sum_v(6-\deg v)=12$, each face vertex contributes at most $3$ and each other vertex at most $1$, so $12\le 9+(n-3)$ and $n\ge6$. Equality forces the three face vertices to have degree $3$ and the other three to have degree $5$. At $n=6$, a degree-5 vertex is adjacent to all five others. So each face vertex would be adjacent to the three degree-5 vertices and to the two other face vertices, which is degree $5$, not $3$. Hence $n\ge7$, and 4-connectivity follows from the three-cut core. ∎

Note that the $n=6$ count is the only place on this page where a small case is used, and it is by hand.

## What this changes

- **The landing gap disappears.** A side's path never lands on $F$, by hypothesis on the side. Degree $\ge6$ on $F$ is irrelevant.
- **The carry gap disappears.** The side is in the class whatever the side degrees of $p,a,q$ are, because the designated face absorbs them. No inner completion is formed.
- **The induction closes on its own class.** The designated face of the side is the separating triangle. The recursive call never leaves $\mathcal C$.
- **The price is the stronger statement.** $\mathrm{VH}_\mathcal C$ needs a $\varphi$-good pair on 4-connected members of $\mathcal C$, including members with degree-4 vertices on $\varphi$. Such members are outside the minimum-degree-5 data. If $\mathrm{VH}_\mathcal C$ is false on some 4-connected member, the reduction is valid but useless.

**[hand] A remark on pure fills.** If every start at $(v,\tau)$ has a pure Kempe fill, the hole never moves. Then $(v,\tau)$ is $\varphi$-good for every face $\varphi$ that avoids $v$. So $\mathrm{VH}_\varphi(T)$ holds as soon as the vertices of $T$ that carry a pure-good pair are not all contained in $V(\varphi)$. On the saved WP19 data every start had a pure fill [computed, post hoc, orders 23–24], but that data has no member of $\mathcal C$ with a vertex of degree $4$.

## Relation to Math's corollary

Math's corollary, that a separator vertex of degree $5$ is itself good with the apex-$a$ fan, holds for plain VH∃ and does not need least order. Under $\mathrm{VH}_\mathcal C$ the separating triangle is removed before degrees matter. The two results are compatible. The corollary also gives $\varphi$-goodness when $f\notin V(\varphi)$, because its fill is pure.

## What remains on line 1, in this frame

1. **Plausibility of $\mathrm{VH}_\mathcal C$ on 4-connected members, especially with degree-4 vertices on $\varphi$.** This is a finite question at each order, and nothing on these pages tests it. It needs a declaration before any confirmatory test. An exploratory reading at small orders is below.
2. **The 4-cut.** A minimal failure of $\mathrm{VH}_\mathcal C$ is 4-connected; the next reduction is across a separating induced 4-cycle $Q$. Put $\varphi$ on side $B$. The side $A$ has a quadrilateral face, so it is not a triangulation. Adding a diagonal fixes that, but a start may colour the two ends of the diagonal alike. Worse, a Kempe component of $T$ can join two components of $A$ through $B$ at opposite vertices of $Q$. A swap in $T$ then performs two swaps in $A$, and the side path is not followed. This is the classical 4-ring difficulty. A designated quadrilateral with "virtual" boundary connections may be the right class. Not started.
3. **The 5-cut** that is not a neighbourhood. Not started.

## Feasibility

| Question | Rating |
|---|---|
| The triangle reduction and its corollary, as hand arguments | High |
| $\mathrm{VH}_\mathcal C$ holds on 4-connected members (plausibility) | Unknown; see the exploratory reading |
| A 4-cut reduction in the same style | Low to Medium |

## Exploratory reading (not evidence)

**[computed, exploratory, post hoc, undeclared code]** This was run at the user's instruction in this session to explore first and check slowly afterwards. It is not a WP, has no declaration, and uses no holdout order. The code is `backgroundMaterial/planemap-structural/longtable/explore-vhphi/vhphi_explore.py`. It is self-contained and imports no team code.

**Generation.** Members of $\mathcal C$ were generated by random edge flips with an annealed score, not by plantri. The generated triangulations are 4-connected, every vertex of degree $<5$ lies on one face, and the orders are $13$–$18$. There are $163$ graph records over three seeds, not deduplicated up to isomorphism across seeds, giving $1308$ pairs $(T,\varphi)$:
- $906$ pairs have no degree-4 vertex;
- $276$ have one degree-4 vertex on $\varphi$;
- $126$ have two;
- none has three, because the generator did not reach that case.

**Pure test.** Is there a degree-5 vertex off $\varphi$ and a legal fan such that every start lies in a Kempe class, at the fixed hole, that contains a filled state?

**Result.** $1308$ of $1308$ pairs pass the pure test. In every record, every degree-5 vertex carried such a fan, so the face constraint never bit.

**Reading.** The degree-4 members met so far behave like the minimum-degree-5 data. This says nothing about members with three degree-4 vertices on $\varphi$, about orders above $18$, or about rare graphs such as $17{:}1$, which a random flip search would not be expected to hit.
