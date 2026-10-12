# Long-arc lemma

**Verdict: PROVED**, for the narrowed identity below. The reading in which boundary pattern $2,1,1,1$ and the locked placement alone force every long-arc chain to contain exactly one degree-5 neighbour is false. The obstruction is a proper recolouring of the same link, recorded after the proof. Orders 32 and 42 were not coloured.

## Statement

Let $T$ be a simple spherical triangulation and let $r$ be a degree-5 vertex. Let $c$ be a proper $4$-colouring of $T-r$ whose link, in cyclic order, is

$$
u^{5}_{\alpha},\; p_{\beta},\; q_{\gamma},\; v^{5}_{\alpha},\; w_{\delta},
$$

with $\{\alpha,\beta,\gamma,\delta\}$ all four colours. This is pattern $2,1,1,1$. On a $5$-cycle the two vertices of the repeated colour are non-adjacent, so they sit at cyclic distance $2$. The long arc is the pair $p,q$. The short arc is the single vertex $w$.

**Locked placement.** The degree-5 neighbours of $r$ are exactly $u$ and $v$, so both carry the repeated colour $\alpha$.

For a long-arc vertex $x\in\{p,q\}$ write $\beta_x=c(x)$, and write $s$ for the neighbour of $x$ in $\{u,v\}$. Thus $s=u$ when $x=p$, and $s=v$ when $x=q$. The edge $xs$ is an $\alpha\beta_x$-edge, so the $\alpha\beta_x$-component $C_x$ of $x$ in $T-r$ contains $s$.

**Hypothesis H1.** The other vertex of $\{u,v\}$ lies outside $C_x$. Equivalently, $C_x$ contains exactly one degree-5 neighbour of $r$, namely $s$.

**Hypothesis H2.** The vacancy slide $r\to x$ has a unique forward degree-5 continuation $y$, and $c(y)\neq\alpha$.

**Identity.** Let $S$ be the colouring of $T-y$ produced by the slides $r\to x\to y$. Let $K$ be the colouring of $T-s$ produced by swapping $C_x$ and then sliding $r\to s$. On $V\setminus\{y,s\}$ the colourings $S$ and $K$ differ exactly on $C_x\setminus\{s\}$.

Both routes give the old root the colour $\beta_x$.

## Proof

### The short arc is outside the pairing

The short-arc vertex $w$ is adjacent to both $u$ and $v$, and both of those vertices have colour $\alpha$. Each of the edges $wu$ and $wv$ is an $\alpha\delta$-edge, so the $\alpha\delta$-component of $w$ contains both degree-5 neighbours. Hypothesis H1 fails at $w$ for every proper colouring of this link. The degree of $w$ is not used.

Swapping that component sends both boundary copies of $\alpha$ to $\delta$. The colour $\delta$ then occurs twice on the link, on the two degree-5 vertices, so the swap creates no degree-5 singleton and there is no prepared slide onto one of them.

The degree split seen on the four orbits is a separate check, not the exclusion. On `17:0` roots 4 and 6 the short-arc vertex is vertex 5, of degree 6. Each intermediate link has two forward degree-5 landings, and their colours in $c$ are the two long-arc colours. On `20:7` root 7 the short-arc vertex is 16, of degree 7; on root 11 it is 5, of degree 7. In both intermediate links the only singleton is the return to the original root.

### The adjacent degree-5 vertex lies in the chain

The link order makes $p$ adjacent to $u$ and $q$ adjacent to $v$. For $x=p$ the colours on that edge are $\beta$ and $\alpha$. For $x=q$ they are $\gamma$ and $\alpha$. In either case $s\in C_x$. The far degree-5 vertex is the one H1 excludes. A chord from $x$ to the far vertex would be an $\alpha\beta_x$-edge and would put that vertex in $C_x$, which is an instance of H1 failing.

### After the swap, $s$ is the unique degree-5 singleton

The boundary vertices of colour $\alpha$ are $u$ and $v$. The boundary vertex of colour $\beta_x$ is $x$ alone. The swap of $C_x$ changes the boundary only at $s$ and at $x$: $s$ goes from $\alpha$ to $\beta_x$, and $x$ goes from $\beta_x$ to $\alpha$. Hypothesis H1 leaves the far degree-5 vertex coloured $\alpha$.

After the swap, $\beta_x$ occurs on the boundary only at $s$, and $\alpha$ occurs at $x$ and at the far degree-5 vertex. The locked placement says that $u$ and $v$ are the only degree-5 neighbours of $r$. So $s$ is the unique degree-5 singleton, and the slide $r\to s$ is the unique degree-5 singleton slide. It colours $r$ with $\beta_x$.

The other chain of the pair $\{\alpha,\beta_x\}$ contains the far degree-5 vertex and excludes $x$ and $s$. Swapping that chain leaves $s$ coloured $\alpha$, so the slide onto $s$ colours $r$ with $\alpha$. The identity uses the swap of $C_x$, which is the swap that writes $\beta_x$ on the old root.

### The two recolourings

Write $\sigma$ for the swap of colours $\alpha$ and $\beta_x$ on $C_x$. The Kempe colouring $K$ of $T-s$ satisfies $K(r)=\beta_x$, and $K(z)=\sigma(c(z))$ for every other coloured vertex. Thus $K$ differs from $c$ on $C_x\setminus\{s\}$, and agrees with $c$ off $C_x$.

The first slide $r\to x$ colours $r$ with $\beta_x$ and vacates $x$. The second slide $x\to y$ colours $x$ with $c(y)$ and vacates $y$. The two-step colouring $S$ of $T-y$ therefore satisfies $S(r)=\beta_x$, $S(x)=c(y)$, and $S(z)=c(z)$ for every other vertex coloured by both $c$ and $S$. In particular, on the common coloured vertices of $c$ and $S$, the only change is at $x$.

The vertex $y$ is adjacent to $x$, and $c(x)=\beta_x$, so $c(y)\neq\beta_x$. Hypothesis H2 adds $c(y)\neq\alpha$. An $\alpha$-neighbour of $x$ would lie in $C_x$, so $y\notin C_x$. The swapped colour of $x$ is $\alpha$, hence

$$
S(x)=c(y)\neq\alpha=K(x).
$$

### Where $S$ and $K$ differ

Both colourings are defined on $V\setminus\{y,s\}$. This set contains $r$, and it contains $C_x\setminus\{s\}$ because $y\notin C_x$.

- At $r$, both colours equal $\beta_x$. The old root is outside $C_x$.
- At $x\in C_x\setminus\{s\}$, the colours are $c(y)$ and $\alpha$, which differ.
- At any other $z\in C_x\setminus\{s\}$, one has $S(z)=c(z)$ and $K(z)=\sigma(c(z))\neq c(z)$.
- At any $z\notin C_x$ with $z\neq r$, both colours equal $c(z)$.

The set of disagreements is exactly $C_x\setminus\{s\}$.

A Kempe swap on one bichromatic component preserves properness: edges inside the component stay bichromatic, and an edge leaving the component meets a colour outside $\{\alpha,\beta_x\}$. A slide onto a colour singleton preserves properness: the newly coloured vertex meets that colour only at the vertex just vacated. So $S$ and $K$ are proper on their domains.

## Obstruction to dropping H1 or H2

Pattern $2,1,1,1$ and the locked placement fix the link colours and the two degree-5 vertices. They do not fix the interior. On `17:0`, root 4, the link $(0,3,10,11,5)$ has degrees $(5,6,6,5,6)$ and colours $(0,3,1,0,2)$. Exactly eight proper colourings of the interior extend that boundary. Four of them put both degree-5 vertices in one long-arc chain. Three keep the chains separated and still break H2. One satisfies both hypotheses; it is the locked orbit, state 25.

**H1 fails.** Vertex order skipping 4, colouring

$$
(0,1,2,3,2,0,3,0,2,1,0,1,2,1,0,3).
$$

The $\{0,1\}$-component of the long-arc vertex 10 is $\{0,1,6,8,10,11,12,14,15\}$. It contains both degree-5 neighbours, 0 and 11. The colouring is proper, and the boundary and the degrees are the locked ones.

**H2 fails while H1 holds.** Same boundary, colouring

$$
(0,1,2,3,2,0,3,1,2,1,0,3,1,0,3,2).
$$

The $\{0,3\}$-component of vertex 3 is $\{0,3\}$, and the $\{0,1\}$-component of vertex 10 is $\{10,11\}$. Each chain contains exactly one degree-5 neighbour. The unique forward degree-5 landing through 3 is vertex 0, and through 10 is vertex 11. Both landings have colour $\alpha$. For $x=3$, one has $s=y=0$ and $C_x\setminus\{s\}=\{3\}$. The two operations end with the vacancy at 0, and the resulting colourings agree at every common vertex.

The same division occurs on the other three locked boundaries. Extensions are proper colourings of $T-r$ with the orbit's boundary colours held fixed.

| Boundary | Proper extensions | H1 fails for some long arc | H1 holds, H2 fails | Both hypotheses hold for both long arcs |
| --- | ---: | ---: | ---: | ---: |
| `17:0` root 4 | 8 | 4 | 3 | 1 |
| `17:0` root 6 | 8 | 4 | 3 | 1 |
| `20:7` root 7 | 12 | 4 | 4 | 4 |
| `20:7` root 11 | 12 | 4 | 4 | 4 |

On every extension that meets both hypotheses, the forward colour is the short-arc colour $\delta$. The identity uses only the weaker demand $c(y)\neq\alpha$. Full singleton lock does not replace H2: separated extensions with the forward landing on $\alpha$ still link every singleton.

## Check on the four orbits

The four locked mass-stuck orbits satisfy H1 and H2 at every long-arc vertex. The raw symmetric difference stored in `kempe-vs-twostep-data.json` equals $C_x\setminus\{s\}$. The column $y$ is the forward root, and $c(y)=\delta$ in every row. The short-arc vertex is omitted.

| Orbit | $x$ | $\beta_x$ | $C_x$ | $s$ | $y$ | raw difference |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| `17:0` r4 s25 | 3 | 3 | $\{0,3,9,15\}$ | 0 | 2 | $\{3,9,15\}$ |
| `17:0` r4 s25 | 10 | 1 | $\{8,9,10,11\}$ | 11 | 16 | $\{8,9,10\}$ |
| `17:0` r6 s27 | 13 | 0 | $\{8,12,13,14\}$ | 12 | 16 | $\{8,13,14\}$ |
| `17:0` r6 s27 | 7 | 3 | $\{1,7,14,15\}$ | 1 | 2 | $\{7,14,15\}$ |
| `20:7` r7 s180 | 1 | 1 | $\{1,3,4,5,8,9\}$ | 8 | 0 | $\{1,3,4,5,9\}$ |
| `20:7` r7 s180 | 6 | 2 | $\{5,6,12,15,18,19\}$ | 15 | 13 | $\{5,6,12,18,19\}$ |
| `20:7` r11 s18 | 10 | 0 | $\{0,2,4,8,10,16\}$ | 4 | 9 | $\{0,2,8,10,16\}$ |
| `20:7` r11 s18 | 17 | 1 | $\{12,13,14,15,16,17\}$ | 12 | 19 | $\{13,14,15,16,17\}$ |

Each difference is $C_x$ with $s$ removed, and $y$ lies outside $C_x$. No hypothesis of the narrowed statement fails on these eight vertices.

## Feasibility

The recolouring identity under H1 and H2: **High**. It compares two explicit recolourings, and both hypotheses hold on all eight long-arc vertices of the four orbits.

The exclusion of the short arc by the two boundary edges at $w$: **High**.

A theorem that deletes H1 and still concludes the chain split from the boundary pattern and the locked placement: **Low**. The same locked links already have proper extensions in which one long-arc chain contains both degree-5 neighbours.

## Next steps

1. State the long-arc correspondence with H1 and H2 explicit. The eight rows above are a check of those hypotheses, not a substitute for them.
2. Keep $w$ outside the pairing by the boundary argument. Record the degree-6 double landing and the degree-7 return as orbit checks.
3. Leave mass-stuckness out of the hypotheses. Singleton lock survives on extensions where the forward landing has colour $\alpha$ and the identity fails.
