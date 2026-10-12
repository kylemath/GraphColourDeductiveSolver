# Ordered rewriting of a colouring with a hole

4 October 2026. Variability seed 99. A term is a pair $(h, c)$: a hole together with a proper 4-colouring of the remaining vertices. A singleton slide is a reversible ground rule. A Kempe swap on one bichromatic component is a second reversible ground rule. When the boundary of $h$ uses at most three colours, filling $h$ is a third rule, from a partial colouring to a colouring of the whole graph.

The system is ground. A critical pair is a local peak at one state, which is the overlap test in an abstract rewrite system. There is no free-variable unifier underneath these rules.

Two witnesses are already on record. On order 17 graph 0 the stuck orbits at roots 9 and 14, colourings 18 and 21, are a 2-cycle of slides. Both have sorted counts $(4,4,4,4)$, with $p=1$ and $q=138$. On order 20 graph 7 root 7 orbit 180, after the vacancy $1\to 0$, the slowest-greedy walk has the length-2 macro $63\to 24\to 194$. Colouring 24 has $p=0$ and $R=188$. Colouring 194 has $p=1$ and $R=2597$.

**Survivor.** The strict orientation by the sorted-count distance $\delta$ defined in §5. It falls on the equal-pole star swap, from $\delta=3$ to $\delta=1$, and the oriented relation has no 2-cycle on roots 9 and 14.

Feasibility on equal-pole belt deletions of $G_n$ for $n=3k+2$: **High**. Feasibility on the 21 mass traps, and on a general spherical triangulation: **Low**.

The orientation is a progress measure on one proved repair. It is not a four-colour proof.

## Orders already killed

A reduction order keeps a rule $s\to t$ only when a well-founded measure strictly falls. A tie contributes no arrow. The non-strict reading, which steps on a tie, is a different relation. The measures below are killed in `rank-kill.md`.

| Order | Roots 9 and 14 | Kill |
|---|---|---|
| $q$ | tie at 138; the non-strict reading cycles $18\leftrightarrow 21$ | 17:3 root 3 colouring 44, $107\to 111$ |
| $(p,q)$ | $p$ stays 1, so the same tie | the same orbit, $(1,107)\to(1,111)$ |
| $(n_5,q)$ | tie $(1,138)$; the non-strict reading cycles | locked orbits: $n_5=0$, and every slide raises it |
| $(d_{\min},q)$ | the degree-6 slide falls, $138\to 126$ | colouring 44: $d_{\min}$ stays 5 and $q$ rises |
| $\mathrm{repMass}$ |  | 20:7 root 7 colouring 180, $50\to 58,108,174$ |
| $(L,q)$ |  | colouring 44: $L$ stays 9 and $q$ rises |
| $(\mathrm{shortLinks}, q)$ | both sides $(0,138)$, so the exchange contributes no arrow | the next minimum of the same rule, order 17 graph 3, degree-6 vertex 11, at $(0,96)$ |
| $(H,q)$ | the twin keeps $H=1$ | the first landing, order 17 graph 3 root 0 colouring 37, at $(0,111)$ |

$(\mathrm{shortLinks}, q)$ and $(H,q)$ fall on all 21 traps and leave the exchange unoriented. Each dies on the next colouring. They are killed with the others. So are $\mathrm{lin}$, $(\mathrm{chainMax}, q)$, the exterior-size tuple, $(\sigma, q)$ and $(\mathbf{1}_{n_5=0}, q)$, all on colouring 44.

$(d_{\min}, q)$ is the witness that a strict fall on the degree-6 exit is not enough. It leaves the exchange and still dies on colouring 44.

## 1. Newman's lemma

Newman's lemma: a terminating relation is confluent when every local peak joins.

Object on $(h, c)$: the one-step slide relation.

The slide relation on order 17 graph 0 contains the cycle of roots 9 and 14, so that relation does not terminate. The hypothesis of the lemma is false on that component. A diagram that joined the two slides would not, by this lemma, produce unique normal forms.

A second computation kills the unique-normal-form reading on its own. Take a full colouring, hole already filled, as an irreducible term. $G_n$ has at least $\lfloor n/6\rfloor$ Kempe classes. For every $n\ge 12$ the bound is at least 2. Distinct irreducible terms with no rule between them fail confluence. The statement that matches a colouring argument is weak normalisation: some normal form exists. Newman's lemma concludes uniqueness.

On $G_8$ the same bound is $\lfloor 8/6\rfloor=1$, so the class count does not by itself kill confluence there. The 2-cycle already kills the appeal to Newman for the slide relation.

Feasibility of a confluence proof by Newman's lemma on these rules: **Low**.

## 2. Completion adds the missing rule

Knuth–Bendix completion orients equations and, when a critical pair does not join, adds a rule. On a ground system the pairs are the local peaks.

Object: the slide component of a fixed charge, as a set of equations.

On order 18 graph 10, Florek's $G_8$, the slide component of the published start has 32 states. Every state has sorted counts $(2,5,5,5)$. Every full colouring has counts $(4,4,5,5)$. No peak inside the component joins by slides to a full colouring. Completion's answer is a new rule.

The rule that joins the class is the equal-pole star swap. On the published start, hole 0, the common pole colour is 2 and the swapped component is $\{1,6,13,16\}$, three belt vertices of colour 0 and the other pole. The counts go from $(2,5,5,5)$ to $(4,3,5,5)$. The boundary goes from four colours to three. Writing the free colour produces $(4,4,5,5)$.

The same procedure at roots 9 and 14 meets the inverse overlap of one slide with itself. The two colourings are

$$
(0,1,2,1,3,2,3,0,3,0,1,0,1,2,3,2)
$$

at root 9 and

$$
(0,1,2,1,3,2,3,0,3,2,0,1,0,1,3,2)
$$

at root 14. Both have sorted counts $(4,4,4,4)$. A slide writes the deleted vertex's colour onto the old hole, so every slide in the pair, including each degree-6 exit, preserves the counts. The preparing Kempe at root 9, colours 1 and 3 on $\{1,6,13,15\}$, meets two vertices of each colour, so it preserves the counts as well. An order that reads only the sorted counts has no orientation for this peak, and completion has no new rule it can add.

Feasibility of one added rule on the equal-pole component: **High**. The rule is the star swap. Feasibility of completing the 9–14 peak by a count order: **Low**.

## 3. Orienting the reversible rules by a killed measure

Object: each measure in the table above, used as $\succ$.

The computation is the one `rank-kill.md` already ran. Strict $q$, strict $(p,q)$ and strict $(n_5,q)$ leave the 9–14 exchange unoriented, because the two sides tie. The non-strict reading of each of those three is the 2-cycle. $(d_{\min}, q)$, $\mathrm{repMass}$ and $(L,q)$ die by a rise on a legal move. $(\mathrm{shortLinks}, q)$ and $(H,q)$ die one step after the traps. A further pair $(f,q)$ is the experiment `LibraryPlan.md` stops.

This mapping has no survivor.

Feasibility of another $(f,q)$ orientation: **Low**.

## 4. A length-2 strategy rewrites past a fillable term

Object: a strategy, as distinct from the one-step relation. A strategy is normalising when it stops on a normal form whenever a normal form exists.

The smallest-index mass rule reaches $p=0$ in at most three macros on each of the 21 landings, and it revisits no colouring.

The slowest-greedy rule scores the endpoint of a macro of length 1 or 2. On the landing at root 0 of order 20 graph 7, macro 3 runs from colouring 63 through colouring 24 to colouring 194. Colouring 63 has $p=1$, $q=204$, $R=2605$. Colouring 24 has $p=0$ and $q=R=188$, so the hole has a free colour. Colouring 194 has $p=1$, $q=196$, $R=2597$. The endpoint lies below the start of the macro, and the rule takes the macro. The intermediate term is fillable. The second swap leaves it.

In the one-step relation ordered by $R$, by $p$, or by $q$, the step from 24 to 194 raises the measure: $188\to 2597$, $0\to 1$, and $188\to 196$. Ordered rewriting refuses that step. The slowest-greedy rule never puts the question to the intermediate, because the length-2 macro is one scored step. Those three measures are already killed as descent ranks on other orbits, so the refusal explains this walk and does not supply a new order.

Feasibility of an unguided length-2 macro as a normalising strategy: **Low**.

## 5. Unfailing completion by the population distance

Ordered rewriting applies an equation only in a direction that decreases one fixed well-founded order. Bachmair, Dershowitz and Plaisted use that restriction so that a reversible equation never becomes a 2-cycle: a tie is not a step, and the uphill direction is not a step.

Object on $(h, c)$: the sorted colour-count 4-tuple $\pi$, and its distance to the full population of the equal-pole repair.

On $G_n$ with $n=3k+2$, let $\tau=(k+2,\,k+2,\,2k+1,\,2k+1)$, sorted nonincreasing, and let $\pi$ be the sorted colour counts on the coloured vertices. Set

$$
\delta(\pi)=\lVert\pi-\tau\rVert_1.
$$

Values are nonnegative integers, so every strict $\delta$-step terminates. For $k=2$, $\tau=(5,5,4,4)$.

On the belt charge $\pi=(5,5,5,2)$, one has $\delta=3$. The star swap produces $\pi=(5,5,4,3)$, with $\delta=1$. The fill produces $\tau$, with $\delta=0$. Both steps are forward rules. The inverse Kempe raises $\delta$ from 1 to 3, so the inverse is not a forward rule. The published component $\{1,6,13,16\}$ realises the same arithmetic: colour 2 occurs twice before the swap and the component holds one vertex of colour 2 and three of colour 0, and the image counts are $(4,3,5,5)$.

Slides preserve $\pi$. Every slide in the 32-state component is a tie, and the oriented relation has no slide arrow there, hence no slide cycle. A slide onto a pole keeps $(2,5,5,5)$ and is not the oriented rule. The oriented rule is the Kempe swap, available while the hole is a belt vertex.

On roots 9 and 14 both published colourings have $\pi=(4,4,4,4)$. The exchanging slide preserves $\pi$, so the two sides have equal $\delta$ for any target tuple. Neither direction is a rewrite. The oriented relation has no 2-cycle on those roots.

$\delta$ is not one of the killed orders. Those orders move under slides. The degree-6 slide from root 9 drops $q$ from 138 to 126 while $\pi$ stays $(4,4,4,4)$. A function of $\pi$ alone is constant on that slide.

### Scope

The known exit from the 9–14 pair is count-preserving, so $\delta$ gives that exit no arrow. The pair has no $\delta$-decreasing rule. Completion with this order does not connect it to a fillable term.

The value of $\delta$ on colourings 24 and 194 is not in the swarm record. Nothing here asserts a direction for $\delta$ on that second swap. The slow macro is a different strategy: it scored a composed step on which $p$, $q$ and $R$ all rise in the second half, and a $\delta$-step fires only when $\delta$ falls.

Unequal pole colours lie outside the star proof, so this note does not claim that $\delta$ falls on a belt deletion in that case. On a general spherical triangulation the tuple $\tau$ is the list of populations of the full colourings, and that list is the theorem.

Feasibility on equal-pole belt deletions of this family: **High**. The star proof names the swap, Florek's lemmas give the target counts on $G_8$, and $\delta$ falls on that swap.

Feasibility as a terminating confluent system for the 21 mass traps: **Low**.

Feasibility on a general spherical triangulation: **Low**.

## Next step

Keep $\delta$ as the orientation of the one star-swap rule on equal poles. The hand argument that comes next is the unequal-pole count, already the first item in `LibraryPlan.md`. An orientation of the 9–14 exit has to fall on a slide that preserves $(4,4,4,4)$, so it has to read a quantity other than the colour counts, and it has to fall on order 17 graph 3 root 3 colouring 44 and on the later minimum $(0,96)$ before any new pair is scored.
