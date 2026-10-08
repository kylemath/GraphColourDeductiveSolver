# Can any piece of the belt potential be stated at a general degree-5 hole?

5 October 2026. Searcher for the Proof Navigator. This page is a lead. It asks a question. It enumerates no new graph and claims no theorem.

The search premise is this. **[lead]** On an infinite family, the termination argument that actually runs is the belt potential $\Phi$ of `backgroundMaterial/planemap-structural/longtable/swarm/belt-joined.md`, section 7. The other rows of that family finish by a single star swap, or by a swap count on the pole hole. $\Phi$ is the piece that has to keep going for an arbitrarily long belt. The question is whether any piece of it still has a sentence when the hole is an arbitrary degree-5 vertex of an arbitrary triangulation.

## The question

**[open]** Which pieces of $\Phi$, if any, can be stated for a general degree-5 hole?

A piece counts only if the sentence no longer names the two rails, the two poles, or an index taken without wrap. Survival is then judged on one saved path, below. A sentence that still needs $G_n$ has not left the belt.

VH$\exists$ asks for one degree-5 vertex and one legal fan that work for every start, and the hole is allowed to move. **[lead]** The kill test on this page is stricter than that quantifier. Order 24 graph 7228 has fan-selection length $m=1$, so an easy pair exists on the same graph. A quantity that descends only at an easy vertex fails the test used here. The test is the hard start.

## What section 7 actually uses

Throughout, **[hand]** means the belt page writes the argument for unequal poles of $G_n$, $n\ge 5$. Nothing in this list is claimed for any other graph.

Fix the input colouring $c^0$ after the belt normalisation. The hole walks on the belt, where every vertex has degree 5. The poles keep their colours and are never the hole.

**[hand]** The unprocessed set is a linear index interval, taken without wrap.

- At a downward state $Z(j)$, $1\le j\le n-2$, $I_j=\{v_0,\dots,v_{j-1}\}\cup\{u_1,\dots,u_j\}$.
- At an upward state $D(i)$, $0\le i\le n-2$, $I_i=\{v_i,\dots,v_{n-1}\}\cup\{u_{i+1},\dots,u_{n-1}\}$.

**[hand]** The potential is the cardinality $\Phi=|I|$: $\Phi=2j$ on $Z(j)$, and $\Phi=2(n-i)-1$ on $D(i)$.

**[hand]** Every vertex of $I$ still carries its input colour. A return rewrites only vertices strictly between the old hole and the new hole, and those vertices leave $I$.

**[hand]** Each return lowers $\Phi$ by exactly 4 (an A-type return, an $S_0$ return, or a D return) or by exactly 6 (a B return). The walk therefore stops after at most $\Phi_0/4$ returns. The interval never wraps, because it is linear and only shrinks.

**[hand]** The caps say the walk is filled while the index is still inside the linear range. The next-zero property sends an S-family landing to the largest earlier belt index whose input colour on the $v$-rail is 0; an $S_0$ step and a D step move the index by exactly 2. Cap S fills on the short pattern or before the long pattern can be passed. Cap $S_0$ fills, or the dangerous indices are impossible. Cap D fills at the last legal index. The forcing uses the fixed pole colours and the rail adjacencies.

**[hand]** Each return spends at most as many slides as its drop in $\Phi$. The opening and the last partial step spend at most two slides each. Every unequal belt start fills within $2n$ slides, and those slides are the whole path.

**[computed]** On $G_5,G_8,G_{11}$ the joined replay checks the interval invariant and a drop of 4 or 6 at every landing. That check is inside the belt. It is not a test of a general hole.

## The pieces, asked off the belt

**[lead]** Six pieces are visible in the list above. The untouched set is the one that might have a coordinate-free sentence. The other five still speak in rail coordinates, or they are arithmetic that waits on that sentence.

1. **The index.** **[open]** $\Phi=2j$ and $\Phi=2(n-i)-1$ name a position on a rail. A general degree-5 hole has a 5-cycle link and no second rail. This piece has a sentence only after some other set has been named. Until then there is nothing to count.

2. **The untouched set.** **[open]** The belt sentence is: a set $I$, remembered against the input colouring $c^0$, keeps those colours, and each return deletes vertices from it. Remembering $c^0$ is already part of $\Phi$; a lift is allowed to remember the start. The open sentence is whether any set defined from a hole, a start colouring, and the current colouring shrinks under the moves of a general triangulation. A Kempe swap recolours a whole component. On the belt the chosen walk never does that. Off the belt the component need not lie between two successive holes.

3. **The drop of 4 or 6, and the bound $\Phi_0/4$.** **[lead]** These numbers are the amounts by which the belt interval shrinks on the named returns. The arithmetic “a positive integer that falls by at least 4 reaches 0” lifts as soon as a drop exists, and it says nothing until a drop exists. Copying the numbers 4 and 6, without a set whose cardinality falls by those numbers, is not a piece.

4. **The refusal to wrap.** **[lead]** This is the part that makes the belt an infinite family: the same local step cannot cycle, because the index interval has a cut and only shrinks. A finite triangulation has a finite state space, so strict decrease of any integer would also stop. The belt argument never counts the colourings. The open sentence is a uniform set that shrinks for every $n$, or for every order, with no case split that grows with the graph. That sentence is piece 2 again, together with a reason the set cannot grow.

5. **The caps.** **[lead]** A cap is a local colour obstruction at the end of the interval, read off the poles. The short cap lands on a link that already uses three colours, which is a fill. The forcing that reaches it uses a pole adjacent to a whole rail. **[open]** A sentence for an arbitrary degree-5 hole has to name its own substitute for that pole. The 7228 start is not supplied with one. The substitute claim would be: once the untouched set is smaller than a fixed size, the current link is already filled. Section 7 does not contain that sentence.

6. **The slide budget $2n$.** **[lead]** This counts slides along the unequal walk, and that walk is slides from start to fill. On a path whose last two moves are Kempe swaps, the same count stays constant on those two moves unless the budget is rewritten to charge swaps as well.

**[hand]** An unfilled link of a degree-5 vertex is a proper 4-colouring of a 5-cycle, so the multiplicities are $2,1,1,1$. The two vertices of the repeated colour are non-adjacent, hence at cycle distance 2. The belt’s unfilled links are of this same type. **[lead]** $\Phi$ reads the interval behind the link. The link type alone does not determine it. The saved start below has this ordinary link type.

## The kill path

Source: `SolvingFrameworkPlan/docs/reports/MathWP19Counterexamples.md`, with the same start in `SolvingFrameworkPlan/docs/reports/MathWP19Results.md`. Both record a finished WP19 phase. This page does not recompute the distances.

**[computed]** Order 24, graph 7228, vertex 17, fan 0. The link is $[7,16,23,18,8]$, and the added chords are $7$–$23$ and $7$–$18$. The start, with 4 for the hole, is

$$
[0,1,2,3,1,2,0,3,2,3,1,2,3,0,3,2,1,4,1,0,2,1,3,0].
$$

The link colours are $(3,1,0,1,2)$. Exact mixed distance $\ell=3$. Exact Kempe distance $\kappa=5$. So $\kappa-\ell=2$.

**[computed]** A mixed filling path is: slide to 8, then $K(1,2,\text{seed }1)$, then $K(0,1,\text{seed }0)$, in canonical colour labels after each move. A pure Kempe filling path at the original hole has five swaps. The published layers first show a mixed target at depth 3 (one target among 82 new states) and first show Kempe targets at depth 5 (six targets among 26 new states).

**[computed]** The published rotation of this graph gives vertex 17 the five neighbours $7,16,23,18,8$, and vertex 8 the six neighbours $1,7,17,18,19,9$. The first move leaves the degree-5 class. The fill is a state at a degree-6 hole. The belt walk of section 7 never does this: its hole stays on a belt vertex.

**[computed]** The same report records $m=1$ for the graph. The hard start is not the best pair. The phase table records largest $\ell/\kappa$ equal to $4/5$ on the released phases. This page uses the one path those two reports write out. It does not look up any other start.

**[lead]** “Falls on the path” means four values, one at each state: the start at 17, the state after the slide to 8, the state after the first swap, and the filled state after the second swap. Each value is defined, and each step strictly lowers the number. Decrease on some other walk is not required. $\Phi$ itself is only required to fall on the one walk the belt table selects. Matching that standard is enough for the first test. Matching it is not a theorem.

**[lead]** The two swaps are the filling work. A quantity that drops on the slide and is constant on both swaps does not fall on the path. A quantity whose domain is “degree-5 hole” is undefined at the second state, so it has no value to compare along the rest of the path.

The fan explains why WP19 admitted the start. **[lead]** $\Phi$ never reads a fan. A lift is a quantity on deletions and moves. The chords $7$–$23$ and $7$–$18$ are not part of the potential unless a later sentence gives them a job.

## What would kill the idea

A proposed piece dies on the saved start of order 24 graph 7228 at vertex 17, fan 0, the start with $\ell=3$ and $\kappa=5$ whose short path is a slide from 17 to 8 followed by two Kempe swaps. It dies if the sentence still names the rails, the poles, or an unwrapped belt index; if it is undefined at vertex 8, the degree-6 hole where that path continues and fills; or if the number fails to drop on the slide or on either swap. A drop on the slide alone leaves the two swaps, which finish the filling, with a constant value. This one path is enough to kill the piece. Surviving the path leaves the question open, authorises no theorem, and asks for no further graph.

## Feasibility

Feasibility that some piece of $\Phi$ can be stated for a general degree-5 hole and still fall on this path: **Low**. The cardinality, the drop sizes, the caps, and the slide budget are written in rail coordinates, and the one coordinate-free piece, an untouched set remembered against the start, has to shrink under two Kempe swaps at a degree-6 hole. That is a different mechanism from the belt walk.

Feasibility of deciding the question on this saved path: **High**. The path is already written. The test is four values.

## Next steps

1. For each of the six pieces, write one sentence whose only data are a hole, the input colouring, and the current colouring. Reject the sentence if a rail, a pole, or an unwrapped index is still in it.
2. On the four states of the 7228 path, record whether that sentence has a value and whether the value strictly drops at each of the three steps.
3. If every sentence fails, stop. The lift is dead.
4. If one sentence drops on all three steps, the next comparison is the five-swap Kempe path at the same hole, already printed in the counterexample report. A quantity that treats that longer route as descent has not selected the short path. Still no new graph.
5. Keep any survivor labelled **[lead]** until a later page writes an argument.
