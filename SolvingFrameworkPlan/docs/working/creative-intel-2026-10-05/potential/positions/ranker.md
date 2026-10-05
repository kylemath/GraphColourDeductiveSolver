# Ranking functions off the belt

5 October 2026. Ranker, Potential team, Creative Intel. The techniques are ranking functions, lexicographic orders, the size-change principle, and the Dershowitz–Manna multiset order. A technique counts only once it is a sentence whose data are a hole, an input colouring $c^0$, and a current colouring. A sentence that still names the two rails, the two poles, or an index taken without wrap has not left the belt.

The path is the published one. **[computed]** Order 24, graph 7228, hole $17$ of degree $5$, slide to vertex $8$ of degree $6$, then two Kempe swaps that fill. The link colours are $(3,1,0,1,2)$, then $(1,3,2,1,0,3)$ on the $6$-cycle, then $(2,3,2,1,0,3)$, then $(0,3,0,1,0,3)$. The degrees of the hole are $5,6,6,6$.

**[lead]** The shortness note records that a length cap is dead, including the fitted ranks $q$ and $\mathrm{lin}$. This page does not score a length, and it does not revive those ranks. Each candidate below is an element of a well-founded set, read from the hole, from $c^0$, and from the current colouring.

**[hand]** The number of missing colours on the link is $0,0,0,1$, and that integer does not strictly drop on the first two steps.

## What a belt return ranks

**[hand]** In section 7 of the joined belt argument, $\Phi$ is the cardinality of one linear unprocessed interval, an index range taken without wrap. The invariant is that every vertex of the interval still carries the input colouring $c^0$. A return rewrites only vertices strictly between the old hole and the new hole, those vertices leave the interval, and $\Phi$ falls by $4$ or by $6$.

**[lead]** The fall is the fall of a ranking function on the returns a controller names. The next-zero property names the landing, and the invariant says that landing deletes a positive piece of the interval. The three sentences below name no next move. Each is scored on the four states of the walk already found.

## 1. Agreement cardinality

**[hand]** Let $h_0$ be the hole of $c^0$, and let $h$ be the current hole, with $c$ a colouring of $T-h$. The original hole is handled by keeping it out of the set for the whole path, since $c^0$ does not colour it. The current hole stays out because $c$ does not colour it. Set

$$
I(h,c^0,c)=\{x\in V\setminus\{h_0,h\}:c(x)=c^0(x)\}.
$$

The sentence is the nonnegative integer $|I|$, ordered by the usual order on $\mathbb{N}$, which is well-founded. This is the coordinate-free piece already named for $\Phi$: a set remembered against the input colouring. The definition uses the degree of neither hole, so the domain includes the degree-$6$ hole on this path. Here $h_0=17$.

**[hand]** At the start, $h=h_0$ and every other vertex carries $c^0$, so $|I|=23$. The slide blanks vertex $8$ and paints vertex $17$ with colour $2$. Vertex $17$ stays outside $I$, vertex $8$ leaves the domain, and no comparable vertex changes colour, so $|I|=22$. The first swap exchanges $\{1,2\}$ on $E'=\{1,2,4,5,10,11\}$. Immediately before that swap those six vertices are coloured $1,2,1,2,1,2$, each equal to $c^0$, and the exchange sends each of them off $c^0$, so $|I|=16$. The second swap exchanges $\{0,2\}$ on $\{0,1,4,6,15,17,23\}$. Immediately before it, that set is coloured $0,2,2,0,2,2,0$, and it meets $I$ in $\{0,6,15,23\}$: vertices $1$ and $4$ have already left, and vertex $17$ was never in. The exchange restores none of the seven vertices to $c^0$, so $|I|=12$.

The four values are $23,22,16,12$. Each of the three steps is a strict drop. The sentence names no rail, no pole, and no unwrapped index.

**[hand]** On a Kempe swap that recolours $k$ vertices, let $d$ be the number of those vertices that lie in $I$, and let $r$ be the number that the swap restores to $c^0$. The original hole, if it lies in the swapped set, contributes to neither count. The integer changes by $r-d$, and it rises whenever $r>d$. Moves are reversible. With $c^0$ held fixed, the reverse of this walk reads the same four states in the opposite order and raises $|I|$ through $12,16,22,23$. Remembering $c^0$ is what permits a drop on the forward walk. It is the memory the belt already uses for $\Phi$.

**[lead]** The four values meet the path test. Survival of this one path is a **[lead]**.

## 2. A lexicographic pair

**[hand]** Let $e(h,c)=\max\bigl(0,\ |c(N(h))|-3\bigr)$, the number of link colours above three. The published link uses $4,4,4,3$ colours, so $e$ takes the values $1,1,1,0$. The second coordinate is $|I|$, which moves on a swap. The rank is the pair

$$
\bigl(e(h,c),\ |I(h,c^0,c)|\bigr)
$$

in the lexicographic product $\mathbb{N}\times\mathbb{N}$. That product is well-founded. Both coordinates are defined for a link of any length, so the domain includes the degree-$6$ hole.

**[hand]** The four pairs are $(1,23)$, $(1,22)$, $(1,16)$, $(0,12)$. On the slide and on the first swap the excess stays $1$ and $|I|$ strictly falls. On the second swap the excess falls from $1$ to $0$. Each step is a strict lexicographic drop.

**[lead]** This is the size-change reading of the same walk. The excess decreases at the fill. The agreement cardinality decreases on the two earlier steps, and it decreases again at the fill. A size-change step of that shape is legal for these three transitions. The size-change principle certifies termination when every transition the argument quantifies over has such a step. The transitions quantified over here are the three moves of the walk already found.

**[hand]** A swap of $k$ vertices can raise $e$, by bringing a new colour onto the link, and can raise $|I|$, by the same difference $r-d$. Either rise lifts the pair in lexicographic order. On this path neither coordinate rises.

**[hand]** The link-local substitute for the second coordinate, the number of singleton colours on the link, takes the values $3,2,2,1$. The pairs $(1,3)$, $(1,2)$, $(1,2)$, $(0,1)$ are flat across the first swap, so that substitute fails the path test. The pair that falls takes its second coordinate from $|I|$. The excess is constant on the slide and on the first swap, so the drop on those two steps is the drop of $|I|$. The pair is that integer with a first coordinate that waits until the fill.

**[lead]** The pair meets the path test as the same **[lead]** as the agreement cardinality.

## 3. Multiset of components that meet the link

**[hand]** For a hole $h$ and a colouring $c$ of $T-h$, let $\mathcal{K}(h,c)$ be the multiset of cardinalities of the bichromatic components of $T-h$ that meet the link $N(h)$. The sentence reads the hole and the current colouring.

Order nonnegative integers by the usual relation $>$. In the Dershowitz–Manna extension, a multiset $A$ stands strictly above a multiset $B$ when $B$ comes from $A$ by deleting a nonempty submultiset $X\subseteq A$ and adding a finite multiset $Y$ in which every element is strictly smaller than some element of $X$. The extension of a well-founded order is well-founded. Descent is the downward direction of that extension. A component of size $s$ that splits, replaced by finitely many integers each strictly smaller than $s$, is a descent. A merge into a larger part is an ascent in the same extension.

The multiset is defined at a degree-$6$ hole. The definition does not use the degree.

**[hand]** A Kempe swap that recolours $k$ vertices of one component of the swapped pair leaves that component's vertex set fixed, so the part $k$ stays in $\mathcal{K}$ for that pair. The multiset can still change, because every pair that shares a colour with the swap is repartitioned. A split of one of those parts into smaller parts is a descent. A merge is an ascent. The multiset may rise. The input colouring is not an input of $\mathcal{K}$, so remembering $c^0$ does not choose the direction.

**[open]** Section D of the counterexample analysis lists the components of $T-17$ at the start, and after the slide it records the split of one $\{1,2\}$-component into $E'=\{1,2,4,5,10,11\}$ and the set $\{15,16,17,18,20,21\}$. The two swaps are named as the sets $E'$ and $\{0,1,4,6,15,17,23\}$, with no list of the other link-meeting sizes after either swap. The four multisets are not in that section. Without the component sizes after each swap the descent cannot be evaluated. An unevaluable candidate supplies no strict drop, so it does not survive.

## What surviving the path amounts to

**[lead]** The agreement cardinality is defined at hole $8$ and strictly decreases on the slide and on both swaps. That is the path test. Passing it is a **[lead]** on this walk. A ranking of one known path supplies no policy that chooses the next move on an arbitrary state.

**[lead]** The belt potential works because a controller names the next return and an invariant says that return drops $\Phi$. A lifted potential without a controller is a score of a path already found. A lexicographic ranking and a size-change step certify the transitions they quantify over. Quantifying over the slide and the two swaps scores that walk.

The multiset candidate does not survive. The lexicographic pair meets the arithmetic as the agreement cardinality written in a pair.

Of the three, the agreement cardinality is the one that survives, as a **[lead]** on this path.

Feasibility that the lift is real: **Low**.

The sentence the manager must not water down: the drop $23,22,16,12$ is a score of the published walk, and the lift is a controller that names the next move together with an invariant that forces that move to lower the integer.
