# Joint page: the lift on 24:7228

5 October 2026. Potential team, Creative Intel. One saved path. No census, no new graph, no distance recomputed.

The kill rule is the rule in `SolvingFrameworkPlan/docs/working/VHExistsPotential.md`. A piece dies if it names the rails, the poles, or an unwrapped belt index; if it is undefined at the degree-6 hole; or if its integer fails to strictly drop on the slide or on either swap. Survival of this one path is a **[lead]**.

## A. The mixed path, checked

**[computed]** Order 24, graph 7228, vertex 17, fan 0. The link is $[7,16,23,18,8]$, coloured $(3,1,0,1,2)$. The added chords are $7$–$23$ and $7$–$18$. Exact mixed distance $\ell=3$. Exact Kempe distance $\kappa=5$. The same graph has $m=1$.

**[hand]** The three moves, in the actual palette, are the slide $17\to 8$, the swap of $\{1,2\}$ on $E'=\{1,2,4,5,10,11\}$, and the swap of $\{0,2\}$ on $\{0,1,4,6,15,17,23\}$. These are the sets in section D of `backgroundMaterial/planemap-structural/longtable/wp19/counterexample-analysis.md`. Vertex $17$ has five neighbours, so the hole starts at degree $5$. Vertex $8$ has neighbours $1,7,17,18,19,9$, so it has degree $6$. The hole stays at $8$ for both swaps. The hole degrees are $5,6,6,6$.

**[hand]** The Witness start, with the hole written $\cdot$, is

$$
(0,1,2,3,1,2,0,3,2,3,1,2,3,0,3,2,1,\cdot,1,0,2,1,3,0).
$$

Reading the link $(7,16,23,18,8)$ off that tuple gives $(3,1,0,1,2)$. The slide paints $17$ with $2$ and blanks $8$, and the tuple becomes

$$
(0,1,2,3,1,2,0,3,\cdot,3,1,2,3,0,3,2,1,2,1,0,2,1,3,0).
$$

The link $(1,7,17,18,19,9)$ reads $(1,3,2,1,0,3)$. Immediately before the first swap, vertices $1,2,4,5,10,11$ are coloured $1,2,1,2,1,2$. The exchange produces $2,1,2,1,2,1$. Only vertex $1$ of the degree-6 link lies in $E'$, and it changes from $1$ to $2$, so the link is $(2,3,2,1,0,3)$. Immediately before the second swap, vertices $0,1,4,6,15,17,23$ are coloured $0,2,2,0,2,2,0$. The exchange produces $2,0,0,2,0,0,2$. Vertices $1$ and $17$ of the link change from $2$ to $0$, and vertices $7,18,19,9$ stay $3,1,0,3$, so the link is $(0,3,0,1,0,3)$.

**[hand]** Those four lists are the published lists $(3,1,0,1,2)$, $(1,3,2,1,0,3)$, $(2,3,2,1,0,3)$, $(0,3,0,1,0,3)$. The tuples and the published colours agree. No correction is made.

**[hand]** The colours present on the last link are $\{0,1,3\}$, so colour $2$ is free and the state is filled.

## B. Candidates that die

**[hand]** Distinct link colours, counted from the four lists: $\{0,1,2,3\}$, $\{0,1,2,3\}$, $\{0,1,2,3\}$, $\{0,1,3\}$. The sequence is $4,4,4,3$. It is flat on the slide and flat on the first swap.

**[hand]** Missing colours, out of $\{0,1,2,3\}$: $0,0,0,1$. The sequence is flat on the first two steps. The last step rises.

**[hand]** Defect count $N_1$, the number of singleton colours on the link. The same four lists have multiplicities $2,1,1,1$, then $2,2,1,1$, then $2,2,1,1$, then $3,2,1$.

- $(3,1,0,1,2)$: colour $1$ twice, colours $3,0,2$ once each. Three singletons.
- $(1,3,2,1,0,3)$: colours $1$ and $3$ twice, colours $2$ and $0$ once. Two singletons.
- $(2,3,2,1,0,3)$: colours $2$ and $3$ twice, colours $1$ and $0$ once. Two singletons. The swap takes vertex $1$ from $1$ to $2$, so colour $2$ becomes a pair and colour $1$ becomes a singleton.
- $(0,3,0,1,0,3)$: colour $0$ three times, colour $3$ twice, colour $1$ once. One singleton.

The sequence is $3,2,2,1$. It is the Physicist's sequence. It drops on the slide, stays $2$ across the swap that cuts $P$, and drops at the fill. A constant middle step dies under the rule.

**[hand]** The published $\beta\gamma$-chain before the slide is $P=23$–$15$–$6$–$5$–$13$–$20$–$19$–$8$, eight vertices. After the slide it is $19$–$20$–$13$–$5$–$6$–$15$–$23$–$17$, eight vertices. The length is $8$ before the slide and $8$ after. It does not drop on the slide. The published $\beta\delta$-chain $Q$ has eight vertices at the start and is unpublished at hole $8$, so a sum of the two chains has no value on the second state.

**[hand]** A sandpile height, or any height equal to the degree of each vertex, depends only on the triangulation. The triangulation is the same graph on all four states, so the height is the same integer on each of them. It does not drop. The degrees of the hole itself are $5,6,6,6$, which rise on the slide.

**[hand]** The excess $e=\max\bigl(0,\ |c(N(h))|-3\bigr)$ is $1,1,1,0$. As an integer by itself it is flat on the first two steps.

**[hand]** The multiset of cardinalities of bichromatic components that meet the link is defined at a degree-6 hole and names no rail. Section D lists the components of $T-17$ at the start, and the analysis txt lists the components of $T-8$ after the slide. Neither page lists the components after the swap on $E'$ or after the swap on $\{0,1,4,6,15,17,23\}$. The four multisets are not published. An unevaluable candidate supplies no strict drop.

**[hand]** The belt index $\Phi=2j$ or $\Phi=2(n-i)-1$, the caps read off the poles, and the refusal to wrap an index interval still name the rails, the poles, or an index taken without wrap. They have not left the belt. The sentence that every return drops the potential by $4$ or by $6$ does not describe the three steps below: the only integer that drops on all three steps drops by $1$, then by $6$, then by $4$. The fitted ranks $q$ and $\mathrm{lin}$ are not revived on this page. The Ranker left them aside, and this page does not score a length.

## C. The agreement cardinality

**[hand]** Define $I$ exactly as the Witness does. Write $c^0$ for the start colouring on $V\setminus\{17\}$. The current hole is uncoloured, and a blank is not a colour. Vertex $17$ had no start colour, so it stays out of $I$ after it is painted. Set

$$
I=\{x:x\text{ is coloured in the current deletion},\ x\neq 17,\ \text{and }c(x)=c^0(x)\}.
$$

**[hand]** The four values are $23,22,16,12$.

At the start every vertex other than $17$ carries $c^0$, so $|I|=23$. The slide blanks vertex $8$, whose start colour is $2$, and paints vertex $17$. Vertex $17$ stays outside $I$, and vertex $8$ leaves, so $|I|=22$. The first swap changes exactly $E'$. Each of those six vertices still carried its start colour, and each leaves $I$, so $|I|=16$. The second swap meets that copy of $I$ in $\{0,6,15,23\}$: vertices $1$ and $4$ have already left, and vertex $17$ was never in. Those four change and none of the seven swapped vertices returns to $c^0$, so $|I|=12$.

Each step is a strict drop: by $1$, then by $6$, then by $4$. The sentence is defined at the degree-6 hole. Its data are the hole, the start colouring, and the current colouring. It names no rail, no pole, and no unwrapped index.

**[lead]** Survival of $|I|$ on this one mixed path is a lead. It authorises no further graph, and it is not a theorem.

**[hand]** The Ranker's pair $\bigl(e(h,c),\ |I|\bigr)$ takes the values $(1,23)$, $(1,22)$, $(1,16)$, $(0,12)$. On the slide and on the first swap, $e$ stays $1$ and the drop is the drop of $|I|$. The pair is that integer with a first coordinate that waits until the fill. It is the same lead.

**[hand]** The controller gap. On the belt, $\Phi$ drops because a rule names the next return and an invariant forces the drop: the next-zero property names the landing, and every vertex of the interval still carries $c^0$, so the landing deletes a positive piece. A number that falls on a path a search already found is a ghost variable scored after the fact. It does not choose the next move on an arbitrary state. Lemma 1.3(b) of `backgroundMaterial/planemap-structural/longtable/swarm/vh-exists.md` says every move is reversible by a move of the same kind, so the move graph $M(T)$ is undirected. The reverse of this walk visits the same four states in the opposite order: the second swap is undone by swapping the same vertex set, the first swap likewise, and the slide $17\to 8$ is undone by the slide $8\to 17$. Against the same $c^0$, the values rise: $12,16,22,23$. So $|I|$ is not a Lyapunov function for the whole move graph. It can only be one for a policy.

**[post hoc]** The mixed path was printed before this integer was scored on it. The definition of $I$ does not use the path. The four values do.

## D. The five-swap test

**[computed]** Next step 4 of `VHExistsPotential.md` asks for the five-swap Kempe path at the same hole, printed in `SolvingFrameworkPlan/docs/reports/MathWP19Counterexamples.md` in canonical labels after each move:

$$
K(1,2,\mathrm{seed}\,1),\ 
K(0,2,\mathrm{seed}\,0),\ 
K(0,3,\mathrm{seed}\,0),\ 
K(2,3,\mathrm{seed}\,2),\ 
K(0,3,\mathrm{seed}\,0).
$$

**[hand]** Section D of the counterexample analysis does not print the five vertex sets. It says the pure path starts by swapping $E$, which also recolours $8$ and $18$, and then needs $\{0,1\}$, $\{1,3\}$, $\{0,1\}$, and $\{3,0\}$ swaps on large components listed in the txt. The file `backgroundMaterial/planemap-structural/longtable/wp19/counterexample-analysis.txt` prints those components under the heading "kempe path lifted to actual colours". The hole stays at $17$ for all five swaps. The five lines are:

1. Swap $\{1,2\}$ on $\{1,2,4,5,8,10,11,18\}$. Link $(3,1,0,2,1)$.
2. Swap $\{0,1\}$ on $\{0,2,5,6,13,16,21,23\}$. Link $(3,0,1,2,1)$.
3. Swap $\{1,3\}$ on $\{0,3,6,7,8,9,11,12,13,14\}$. Link $(1,0,1,2,3)$.
4. Swap $\{0,1\}$ on $\{2,3,5,9,12,14,19,21\}$. Link $(1,0,1,2,3)$.
5. Swap $\{3,0\}$ on $\{0,3,6,11,12,13,14,16\}$. Link $(1,3,1,2,3)$, filled.

The test is evaluable from that saved page. The sets used below are those five sets. Nothing is added.

**[hand]** Start from the same $c^0$, hole $17$, $|I|=23$. A vertex in the swapped set leaves $I$ when its current colour equals $c^0$, because the swap exchanges the two colours. It enters $I$ when the colour it receives equals $c^0$. The original hole is never in the set.

1. The eight vertices $1,2,4,5,8,10,11,18$ are coloured $1,2,1,2,2,1,2,1$, each equal to $c^0$. All eight leave. None returns. $|I|=23-8=15$. The link vertices $18$ and $8$ change from $1,2$ to $2,1$, and $7,16,23$ stay $3,1,0$, so the link is $(3,1,0,2,1)$, as published.
2. The eight vertices $0,2,5,6,13,16,21,23$ are then coloured $0,1,1,0,0,1,1,0$. Vertices $0,6,13,16,21,23$ still carry $c^0$ and leave. Vertices $2$ and $5$ already differ from $c^0$ (they are $1$ against $2$) and the exchange sends them to $0$, which is still not $c^0$. Six leave, none returns. $|I|=15-6=9$. The link becomes $(3,0,1,2,1)$, as published.
3. The ten vertices $0,3,6,7,8,9,11,12,13,14$ are then coloured $1,3,1,3,1,3,1,3,1,3$. The five that still carry $c^0$ are $3,7,9,12,14$. They leave. The other five stay off $c^0$: $0$ goes to $3$, $6$ to $3$, $8$ to $3$, $11$ to $3$, $13$ to $3$. Five leave, none returns. $|I|=9-5=4$. The set $I$ is now $\{15,19,20,22\}$. The link becomes $(1,0,1,2,3)$, as published.
4. The eight vertices $2,3,5,9,12,14,19,21$ are then coloured $0,1,0,1,1,1,0,0$. The intersection with $I$ is $\{19\}$ only. Vertex $19$ carries $0=c^0(19)$ and goes to $1$, so it leaves. Vertex $21$ carries $0$ against $c^0(21)=1$ and goes to $1$, so it enters. Vertices $2,3,5,9,12,14$ match $c^0$ neither before nor after the exchange. One leaves and one enters. $|I|=4$. The link vertices are disjoint from this set, so the link stays $(1,0,1,2,3)$, as published.
5. The eight vertices $0,3,6,11,12,13,14,16$ are then coloured $3,0,3,3,0,3,0,0$. None of them lies in $\{15,20,21,22\}$, the copy of $I$ left by the previous step. Six receive their start colour: $0$ goes to $0$, $3$ to $3$, $6$ to $0$, $12$ to $3$, $13$ to $0$, $14$ to $3$. Vertex $11$ goes to $0$ against $c^0(11)=2$, and vertex $16$ goes to $3$ against $c^0(16)=1$. None leaves and six enter. $|I|=4+6=10$. The link becomes $(1,3,1,2,3)$. Colour $0$ is absent, and the state is filled, as published.

**[hand]** The six values of $|I|$ are $23,15,9,4,4,10$. The fourth step is flat. The fifth step rises, by the six restorations $0,3,6,12,13,14$. The integer does not strictly fall on the five-swap path.

**[hand]** Next step 4 says that a quantity which treats the longer route as descent has not selected the short path. This quantity does not treat the longer route as descent. That fact does not select the slide. From the start, the slide lowers $|I|$ by $1$, and the first swap of the pure path lowers $|I|$ by $8$. Both opening moves are strict drops. A policy that accepts every strict drop of $|I|$ may take the pure path's first three swaps, and then has no strict drop through the fourth and fifth swaps, which are the swaps that finish that fill.

**[lead]** $|I|$ remains a lead on the mixed path. On the pure path it is a score that stalls and then rises.

## E. Verdict

**[hand]** Every coordinate-free piece in the three positions, other than $|I|$, dies on the mixed path. Distinct colours, missing colours, the defect count, the excess, the $\beta\gamma$-length, and the degree height fail a strict drop. The link-meeting multiset has no published values after the swaps. The pieces that still name the rails, the poles, or an unwrapped index have not left the belt.

**[lead]** $|I|$ falls on the mixed path: $23,22,16,12$. It has no controller.

**[hand]** The navigator's rule on the kill page is that a piece dies if it does not fall, and that a survivor of the path is a lead rather than a theorem. The attack page says that a potential copied off the belt has feasibility Low, that deciding the question on this path has feasibility High, and that surviving that path would raise the research plan to Medium and would not be a theorem.

Bare survival of $|I|$ meets the screen the kill page defined: four defined values, three strict drops, a sentence with no rail, no pole, and no unwrapped index, defined at hole $8$. It does not meet the raise sentence. The subject of that sentence is a potential. On the belt, the potential drops because a rule names the next return and an invariant forces the drop. $|I|$ is the integer scored on a walk that was already found. The same integer rises on the reverse walk, and on the published five-swap fill it is flat and then rises. A policy is not supplied by either sequence. Calling the screen "surviving the path" in the raise sentence would raise the plan for a ghost variable.

The lift of $\Phi$ is not a proof. The research plan does not rise to Medium.

**[open]** Whether any policy, defined on an arbitrary hole and an arbitrary colouring and allowed to remember $c^0$, names a legal move that strictly lowers $|I|$ whenever the link is unfilled, and whether that policy reaches a fill.

Feasibility that a controller for $|I|$ exists off the belt: **Low**. The next-zero rule uses the rail. No substitute is written for vertex $17$. The fifth swap of the published pure fill restores six vertices to $c^0$. On the belt, the invariant is that a named return only deletes vertices from the untouched interval. That deletion property does not hold for this swap. A controller for $|I|$ would have to refuse a move that this filling walk uses, and it would have to do so from the current state. The saved pages do not name that rule. Reversibility leaves no function of the current state alone that falls on every edge. The Ranker's dissent, that the four drops are themselves the survival priced at Medium, is the reading this verdict refuses.
