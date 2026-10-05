# Witness: the saved path on 24:7228

5 October 2026. Potential team, Creative Intel. This page holds the four states of one saved path. The distances $\ell=3$ and $\kappa=5$ are the published distances. No census is run.

## The path

**[computed]** Order 24, graph 7228, vertex 17, fan 0. The link is $[7,16,23,18,8]$, and the added chords are $7$–$23$ and $7$–$18$. The start, with the hole written $\cdot$, is

$$
(0,1,2,3,1,2,0,3,2,3,1,2,3,0,3,2,1,\cdot,1,0,2,1,3,0).
$$

The link colours are $(3,1,0,1,2)$. Exact mixed distance $\ell=3$. Exact Kempe distance $\kappa=5$. The same graph has $m=1$, so this hard start is the path of the kill test while an easier pair exists on the graph.

**[hand]** In the start palette the three moves are the slide $17\to 8$, the swap of $\{1,2\}$ on $E'=\{1,2,4,5,10,11\}$, and the swap of $\{0,2\}$ on $\{0,1,4,6,15,17,23\}$. These are the sets in section D of `backgroundMaterial/planemap-structural/longtable/wp19/counterexample-analysis.md`. Vertex $8$ has neighbours $1,7,17,18,19,9$, so the hole has degree $5$, then degree $6$, then degree $6$, then degree $6$. The chords belong to the fan that admitted the start. They are data of that pair. They are entries of a colour tuple only if a later sentence gives them a job.

`SolvingFrameworkPlan/docs/reports/MathWP19Counterexamples.md` names the same walk after first-occurrence canonical labels: slide to $8$, then $K(1,2,\mathrm{seed}\,1)$, then $K(0,1,\mathrm{seed}\,0)$. The renaming that carries the actual pair $\{0,2\}$ to the canonical pair $\{0,1\}$ is written in the arithmetic below.

## Arithmetic

Write $c^0$ for the start colouring on $V\setminus\{17\}$. A slide onto a neighbour $u$ whose colour $\alpha$ occurs once on the link moves the hole to $u$ and paints the old hole with $\alpha$. A swap of a pair $\{a,b\}$ on a set $K$ exchanges $a$ and $b$ on $K$ and leaves every other coloured vertex as it stands. The hole of a swap stays fixed.

**[hand]** On the start link, $c^0(7)=3$, $c^0(16)=1$, $c^0(23)=0$, $c^0(18)=1$, $c^0(8)=2$. Colour $2$ occurs once, at vertex $8$. The slide paints vertex $17$ with $2$ and blanks vertex $8$. The degree-6 link then reads $c(1)=1$, $c(7)=3$, $c(17)=2$, $c(18)=1$, $c(19)=0$, $c(9)=3$, which is $(1,3,2,1,0,3)$.

**[hand]** Immediately before the first swap the vertices $1,2,4,5,10,11$ are coloured $1,2,1,2,1,2$. The exchange produces $2,1,2,1,2,1$. Of the degree-6 link, only vertex $1$ lies in $E'$, and it changes from $1$ to $2$. The other five link colours stay $3,2,1,0,3$. The link is $(2,3,2,1,0,3)$.

**[hand]** Immediately before the second swap the vertices $0,1,4,6,15,17,23$ are coloured $0,2,2,0,2,2,0$. The exchange produces $2,0,0,2,0,0,2$. Of the link, vertices $1$ and $17$ lie in the set and both change from $2$ to $0$. Vertices $7,18,19,9$ stay $3,1,0,3$. The link is $(0,3,0,1,0,3)$. The colours present are $\{0,1,3\}$, so colour $2$ is free and the state is filled.

**[hand]** First-occurrence canonical labels rename colours by order of appearance along the vertices, skipping the hole. After the slide, colours $0,1,2,3$ already appear in that order at vertices $0,1,2,3$, and the link remains $(1,3,2,1,0,3)$. After the first swap the first occurrences are colour $0$ at vertex $0$, colour $2$ at vertex $1$, colour $1$ at vertex $2$, and colour $3$ at vertex $3$. The map is $0\mapsto 0$, $2\mapsto 1$, $1\mapsto 2$, $3\mapsto 3$. It sends the link $(2,3,2,1,0,3)$ to $(1,3,1,2,0,3)$, and it sends the actual pair $\{0,2\}$ of the next swap to the canonical pair $\{0,1\}$, with least vertex $0$. After the second swap the first occurrences are colour $2$ at vertex $0$, colour $0$ at vertex $1$, colour $1$ at vertex $2$, and colour $3$ at vertex $3$. The map $2\mapsto 0$, $0\mapsto 1$, $1\mapsto 2$, $3\mapsto 3$ sends $(0,3,0,1,0,3)$ to $(1,3,1,2,1,3)$. Those three canonical lists are the successive hole-link colours in the Team B replay of this certificate. The three actual-colour lists are the lists in section D. Both publications are this path, and the tuples below are the actual-colour states.

## The four states

**[computed]** The blank is written $\cdot$. The set $D$ consists of the vertices that are coloured in the current deletion and do not carry a start colour. Vertex $17$ had no start colour, so it lies in $D$ once it is coloured. The current hole is uncoloured, and a blank is not a colour, so the hole is not a member of $D$. The untouched set is

$$
I=\{x:x\text{ is coloured in the current deletion},\ x\neq 17,\ \text{and }c(x)=c^0(x)\}.
$$

| State | Hole | Tuple in vertex order | Link | Distinct link colours | $D$ | $\|I\|$ |
|---|---|---|---|---|---|---|
| Start | $17$, degree $5$ | $(0,1,2,3,1,2,0,3,2,3,1,2,3,0,3,2,1,\cdot,1,0,2,1,3,0)$ | $(7,16,23,18,8)$ coloured $(3,1,0,1,2)$ | $4$ | $\emptyset$ | $23$ |
| After the slide $17\to 8$ | $8$, degree $6$ | $(0,1,2,3,1,2,0,3,\cdot,3,1,2,3,0,3,2,1,2,1,0,2,1,3,0)$ | $(1,7,17,18,19,9)$ coloured $(1,3,2,1,0,3)$ | $4$ | $\{17\}$ | $22$ |
| After $\{1,2\}$ on $E'$ | $8$, degree $6$ | $(0,2,1,3,2,1,0,3,\cdot,3,2,1,3,0,3,2,1,2,1,0,2,1,3,0)$ | $(1,7,17,18,19,9)$ coloured $(2,3,2,1,0,3)$ | $4$ | $\{1,2,4,5,10,11,17\}$ | $16$ |
| After $\{0,2\}$ on $\{0,1,4,6,15,17,23\}$ | $8$, degree $6$ | $(2,0,1,3,0,1,2,3,\cdot,3,2,1,3,0,3,0,1,0,1,0,2,1,3,2)$ | $(1,7,17,18,19,9)$ coloured $(0,3,0,1,0,3)$ | $3$ | $\{0,1,2,4,5,6,10,11,15,17,23\}$ | $12$ |

**[hand]** At the start every vertex other than $17$ is coloured by $c^0$, so $|I|=23$ and $D=\emptyset$. The slide blanks vertex $8$, whose start colour is $2$, and colours vertex $17$. Vertex $17$ stays outside $I$, and vertex $8$ leaves, so $|I|=22$ and $D=\{17\}$. The first swap changes exactly $E'$. Each of those six vertices still carried its start colour, and each leaves $I$, so $|I|=22-6=16$ and $D=\{1,2,4,5,10,11,17\}$. The second swap meets that copy of $I$ in $\{0,6,15,23\}$: vertices $1$ and $4$ have already left, and vertex $17$ was never in. Those four change, so $|I|=16-4=12$ and $D=\{0,1,2,4,5,6,10,11,15,17,23\}$.

Each link colour in the table is the published actual-colour list for that move: $(3,1,0,1,2)$, then $(1,3,2,1,0,3)$, then $(2,3,2,1,0,3)$, then $(0,3,0,1,0,3)$.

## The kill rule

**[lead]** A candidate sentence dies on this path if it names the rails, the poles, or an unwrapped belt index; if it is undefined at hole $8$; or if its integer fails to strictly drop on any of the three steps. A drop only on the slide, with the two swaps flat, is a kill. The four values are the start at $17$, the state after the slide, the state after the first swap, and the filled state after the second swap. Each value has to be defined, and each step has to be a strict drop. Surviving this one path is a **[lead]**, and authorises no further graph.

The integer $|I|$ takes the values $23,22,16,12$. It is defined at the degree-6 hole, its data are the hole, the start colouring, and the current colouring, and the three steps drop by $1$, then $6$, then $4$. That survival on this path is a **[lead]**. **[open]** Whether a sentence with this value is a piece of the belt potential at a general hole.

## Reversibility

**[hand]** Lemma 1.3(b) of `backgroundMaterial/planemap-structural/longtable/swarm/vh-exists.md` states that every move is reversible by a move of the same kind, so the move graph $M(T)$ is undirected. A function of the current state alone cannot strictly decrease on every edge. A fall from $s$ to $s'$ is a rise from $s'$ to $s$ along the reverse move, which the lemma supplies.

A quantity that remembers the start colouring can decrease on a chosen walk and increase on the reverse. The forward values of $|I|$ are $23,22,16,12$. The reverse walk visits the same four states in the opposite order, because each swap is undone by swapping the same vertex set and the slide $17\to 8$ is undone by the slide $8\to 17$. Against the same remembered $c^0$, those values rise: $12,16,22,23$.

This is the constraint on a Lyapunov proposal. The kill test scores one chosen walk, which is the standard already used for the belt potential: descent is required on the walk the argument selects. A function of the current state alone is unavailable as a strict descent on every edge of $M(T)$, and a drop of that function on these three steps still rises on the reverse walk. A quantity that remembers $c^0$, as the belt potential does, may fall on the way to the fill and rise on the way back. The kill test still scores only the forward walk. A survivor of that score remains a **[lead]** about this walk. It is a Lyapunov function of the state only if it fell on every edge, and Lemma 1.3(b) leaves no such function.

## Use of the table

The four integers $|I|$ are $23,22,16,12$.

Feasibility that the table is usable as the kill test: **High**. The start tuple, the slide rule, and the two explicit vertex lists determine every later colour. Each list lies in the named colour pair in the preceding tuple, and the resulting link colours are the published lists in the actual palette and in the canonical palette.

Next step, on this path: read one integer from each of the four rows and test the candidate sentence against the kill rule. A sentence that drops on all three steps stays a **[lead]** here. No other graph is authorised.
