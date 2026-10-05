# The joined belt argument: the vacancy hypothesis on every hole of Florek's $G_n$

5 October 2026. Long Table. This is a hand proof with a mechanical replay. It is not compiled, and no Lean was used. No $n\ge 14$ enumeration was run. Every claim carries one of four labels:
**[hand]** means proved on this page; **[cited]** means taken from a named source and not re-proved here; **[computed]** means checked by `belt_joined_check.py` on $G_5,G_8,G_{11}$ only (output `belt-joined-check.txt`); **[open]** means not established.

The page is self-contained for the belt holes. It re-derives every tile it uses, and does not lean on `unequal-cap.md` or `unequal-general.md`. One local lemma is cited and not re-derived, as requested: the doubled-1 recurrence, from the independent audit chat's `doubled-one-opening-audit.md`. Long Table checked that lemma, and the replay asserts each of its forced colours. The termination and cap argument for that recurrence are given here.

## 0. Statement

**Theorem (belt vacancy).** Let $n\ge 5$. Let $h$ be any vertex of $G_n$, and let $c$ be any proper 4-colouring of $G_n-h$. Then some finite sequence of singleton slides and Kempe swaps reaches a hole whose link uses at most three colours.

The status of each part is as follows.

| Hole | Poles in $c$ | Moves used | Status |
|---|---|---|---|
| belt | unequal | slides only, at most $2n$ | **[hand]** for every $n\ge5$ (§4–§7) |
| belt | equal | at most one Kempe swap, no slides | **[hand]** for every $n\ge5$ (§3) |
| pole | link already uses $\le3$ colours | none | **[hand]** |
| pole | some colour occurs once on the link | one slide, then a belt row above | **[hand]** (§2) |
| pole | every colour occurs $\ge2$ times on the link | Kempe swaps only | **[cited]** Florek Thm 3.1 plus an explicit target **[hand]**; **[computed]** at $n=5,8,11$, at most 3 moves |

**Is $n=3k+2$ needed?** Not by any argument on this page.

- The equal-pole star (§3) holds for every $n\ge5$. Equal-pole belt deletions do not exist for $n\equiv1\pmod 3$. For $n\equiv0$ they are already filled. Only for $n\equiv2$ do they need the swap. That is the one place where $3k+2$ is special.
- The unequal-pole walk never uses $n \bmod 3$.
- Florek's Theorem 3.1 is stated for all $n\ge5$, with bounds that depend on $n\bmod 3$.

So the theorem as stated is proved for all $n\ge5$, modulo the citation in the last row. The computation covers $n=5,\dots,11$, which includes every residue mod 3 (see §9).

## 1. Conventions

$G_n$ has poles $a,b$ and belt vertices $u_i,v_i$ with indices mod $n$. Its edges are $a u_i$, $b v_i$, $u_iu_{i+1}$, $v_iv_{i+1}$, $u_iv_i$, and $u_iv_{i-1}$. There is no edge $ab$. It has $6n=3(2n+2)-6$ edges, belt degree 5 and pole degree $n$. The neighbour lists are
$$N(u_i)=\{a,u_{i+1},v_i,v_{i-1},u_{i-1}\},\qquad N(v_i)=\{b,v_{i-1},u_i,u_{i+1},v_{i+1}\}.$$
For $n\ge5$ the five neighbours are distinct. Links are always written in these orders.

**Automorphisms [hand, also computed].** Three maps are automorphisms:

- rotation $r$: $u_i\mapsto u_{i+1}$, $v_i\mapsto v_{i+1}$;
- ring swap $s$: $a\leftrightarrow b$, $u_i\mapsto v_{-i}$, $v_i\mapsto u_{-i}$;
- reflection $R$: $u_i\mapsto u_{-i}$, $v_i\mapsto v_{-1-i}$, with $a$ and $b$ fixed.

Each one maps the edge list onto itself; for example $s(u_iv_{i-1})=v_{-i}u_{-i+1}=u_jv_{j-1}$ with $j=1-i$. Moves commute with automorphisms and with colour permutations. So every belt hole may be taken to be $u_0$, and every pole hole to be $a$. $R$ fixes $u_0$, swaps $u_1\leftrightarrow u_{n-1}$ and swaps $v_0\leftrightarrow v_{n-1}$.

**Moves.** These are as in `hole-induction.md`. A slide $h\to x$ is allowed when $c(x)$ occurs once on $N(h)$: it writes $c(x)$ on $h$ and makes $x$ the hole. A Kempe swap exchanges two colours on one component of the two-coloured subgraph of the current deletion. A state is *filled* when $N(\text{hole})$ uses at most 3 colours.

**Slide lemma [hand].** A slide preserves properness. The only new coloured vertex is $h$, with colour $c(x)$. Every coloured neighbour of $h$ other than $x$ has another colour, by uniqueness. $x$ is now blank.

**Pole invariant [hand].** In §4–§7 the poles are never the hole and are never recoloured. With $c(a)=0$ and $c(b)=1$, every coloured $u$ lies in $\{1,2,3\}$ and every coloured $v$ lies in $\{0,2,3\}$ at every moment. Every "forced" colour below comes from this invariant together with properness of the current colouring at the named neighbours.

## 2. Pole holes

Take the hole to be $a$. The link is the $n$-cycle $u_0\dots u_{n-1}$.

1. **[hand]** If the ring uses at most 3 colours, fill $a$.
2. **[hand]** If some colour $\alpha$ occurs once on the ring, at $u_i$, slide $a\to u_i$. The state is a belt hole $u_i$ with $c(a)=\alpha$, so §3 or §4–§7 finishes. This is the reduction: belt holes are proved for every colouring, whichever colour $a$ received.
3. **[cited]** If every colour occurs at least twice on the ring, use Florek's Theorem 3.1, applied through $s$.

   **What the theorem says.** Florek (arXiv:2511.00485, §3, Theorem 3.1) works with $H_n=G_n-b$, where $G_n$ is his triangulation with two non-adjacent poles of degree $n$ and $2n$ vertices of degree 5, and $n\ge 5$.

   - *Definitions.* A Kempe chain is a component of the subgraph induced by two colours. A Kempe change swaps the two colours on one chain. Colourings are functions, and the chapter normalises $A(a)=1$.
   - *Conclusion.* Any two 4-colourings of $H_n$ are joined by a sequence of Kempe changes. The length is at most $6\lfloor n/2\rfloor$ for $n\equiv0$, $9\lfloor n/2\rfloor$ for $n\equiv2$, and $9\lfloor n/2\rfloor+6\lfloor n/3\rfloor-2$ for $n\equiv1 \pmod 3$.
   - *Source of the wording.* This is our paraphrase from the arXiv PDF. Its text was recovered by decompressing the PDF streams, because no PDF tool was installed.

   A Kempe change in $H_n$ is exactly our Kempe swap with the hole fixed at the deleted pole.

   **The target, without the Four Colour Theorem [hand].** We need one colouring of $G_n-a$ whose $u$-ring uses at most 3 colours. The restriction of any 4-colouring of $G_n$ will do. Here is an explicit one for every $n\ge5$.

   - Write $n=2p+3q$ with $p,q\ge0$, and go around the belt with blocks. Put $c(a)=0$, $c(b)=1$, $\rho=2$, $\tau=3$.
   - An **A block** at base $k$ is $v_k=0$, $v_{k+1}=\tau$, $u_{k+1}=1$, $u_{k+2}=\rho$.
   - A **B block** is $v_k=0$, $v_{k+1}=\rho$, $v_{k+2}=\tau$, $u_{k+1}=\tau$, $u_{k+2}=1$, $u_{k+3}=\rho$.
   - Every block ends with $u=\rho$ above $v$-colours $\{\tau,0\}$, and starts with $u\in\{1,\tau\}$ above $v$-colours $\{0,\tau\}$ or $\{0,\rho\}$. Checking the eight edge types at a junction and inside each block gives properness. This is **[computed]** for $n=5$ (AB), $n=8$ (AAAA) and $n=11$ (AAAAB).

   The restriction of this colouring to $G_n-a$ (after $s$, to $H_n$) has a 3-coloured ring. If Florek's equivalence is read only up to colour permutation, the endpoint is $\pi\circ t$, whose ring still uses 3 colours. Either way the Kempe sequence ends filled.

   **Caveats.**
   - That our $G_n$ is Florek's graph is taken from his definition and figures. Its degree data are checked, but uniqueness of a triangulation with those data is not re-proved **[cited]**.
   - Florek's proof was not re-verified by Long Table. The parts read construct colourings combinatorially and do not invoke the Four Colour Theorem.
   - No claim of historical novelty is made for anything on this page. No literature check was done beyond `PaperReading.md`.

**[computed]** The pole-hole counts are below. In the no-singleton case, every orbit reaches a fill in at most 3 moves by breadth-first search over slides and Kempe swaps. The Kempe graph of all colourings of $G_n-a$ is connected for $n=5,8,11$, which agrees with Theorem 3.1 at those $n$.

| $n$ | orbits (labelled) | filled | singleton | no singleton | one swap gives fill or singleton | BFS max |
|---|---|---|---|---|---|---|
| 5 | 20 (480) | 10 | 10 | 0 | – | – |
| 8 | 326 (7 824) | 46 | 248 | 32 | 32 | 3 |
| 11 | 5 192 (124 608) | 462 | 2 288 | 2 442 | 2 409 | 3 |

**[open]** A hand argument for the no-singleton pole case that avoids Florek. The data say that one Kempe swap at the pole creates a ring singleton or a fill in 2 409 of 2 442 orbits at $n=11$, and in every orbit at $n=8$. The remaining 33 need more than that one swap but still need at most 3 moves.

## 3. Belt holes, equal poles [hand]

This section re-derives `TwoPoleStarEscape.md`, which is correct as written. Take the hole $u_0$ and $c(a)=c(b)=A$.

**No belt vertex has colour $A$.** Every coloured belt vertex is adjacent to an $A$-coloured pole.

**The link has a singleton $B$ on the $v$-side.** Suppose the link is unfilled. Then its four belt vertices $u_1,v_0,v_{n-1},u_{n-1}$ use all three non-$A$ colours, with multiplicities $(2,1,1)$. Since $v_0\sim v_{n-1}$, these two have different colours and cannot both carry the doubled colour. So one of them, $z$, carries a colour $B$ that is unique on the link.

**The swap.** The $(A,B)$-component of $b$ is exactly $\{b\}\cup\{v_i:c(v_i)=B\}$. Indeed $b$ is adjacent to every $v$, the $B$-vertices are pairwise non-adjacent, and $a$ is not adjacent to any $v$. Swapping it changes only $z$ on the link, from $B$ to $A$. Then $B$ is absent, and we fill $u_0$ with $B$.

**Residues.** The belt is the square of the $2n$-cycle $\cdots v_{i-1}u_iv_iu_{i+1}\cdots$. Deleting $u_0$ leaves a path whose consecutive triples are triangles, so its colouring is 3-periodic. The single wrap edge then forces $n\not\equiv1\pmod3$. For $n\equiv0$ the four belt link vertices use two colours, so the link is already filled. For $n\equiv2$ the swap is needed, and the star has $k+2$ vertices when $n=3k+2$.

**[computed]** One equal orbit for each $n\in\{5,8,11\}$. The star has sizes 3, 4 and 5, its component is exactly as stated, and it fills.

## 4. Belt holes, unequal poles: openings

Normalise the hole to $u_0$ with $c(a)=0$ and $c(b)=1$, and put $\{\rho,\tau\}=\{2,3\}$. Write
$$(p,q,r,s)=(c(u_1),c(v_0),c(v_{n-1}),c(u_{n-1})),$$
so that the link is $(0,p,q,r,s)$. The reflection $R$ sends $(p,q,r,s)$ to $(s,r,q,p)$.

**Classification [hand; agrees with the audit's 14].** The link is unfilled exactly when $\{1,2,3\}\subseteq\{p,q,r,s\}$. Also $q\ne r$, since $v_0\sim v_{n-1}$.

- If $q,r\in\{2,3\}$, write $(q,r)=(\rho,\tau)$. Then $p\in\{1,\tau\}$ and $s\in\{1,\rho\}$. The pair $(\tau,\rho)$ is filled, which leaves $(1,\rho)$, $(\tau,1)$ and $(1,1)$.
- If $r=0$ and $q=\sigma$, then $\{p,s\}=\{1,\sigma'\}$.
- If $q=0$, apply $R$ to reach the case $r=0$.

Up to $R$, and with both namings of $\rho$ and $\sigma$, there are four classes:

| Class | Link $(0,p,q,r,s)$ | Doubled | Labelled words |
|---|---|---|---|
| O1 | $(0,1,\rho,\tau,\rho)$ | $\rho$ | 2, plus 2 reflected |
| O2 | $(0,1,\rho,\tau,1)$ | 1 | 2 |
| O3a | $(0,1,\sigma,0,\sigma')$ | 0 | 2, plus 2 reflected |
| O3b | $(0,\sigma',\sigma,0,1)$ | 0 | 2, plus 2 reflected |

That gives $4+2+8=14$ words, as in the audit. The eight doubled-0 words are O3a and O3b with their reflections. The two words the audit named on $G_5$ are $(0,1,2,0,3)$, which is O3a with $\sigma=2$, and $(0,1,2,3,1)$, which is O2. Both are replayed and fill, after 4 slides and 1 slide **[computed]**.

**Opening moves [hand].** "Forced" means forced by properness at the listed neighbours together with the pole invariant.

| Class | Slides | Forced colours used | Arrives at |
|---|---|---|---|
| O1 | $u_0\to v_{n-1}$ ($\tau$ is unique), then $v_{n-1}\to v_{n-2}$ (0 is unique on $(1,0,\rho,\tau,\rho)$) | $v_{n-2}=0$, since it meets $v_{n-1}=\tau$ and $u_{n-1}=\rho$ | $Z(n-2)$ with $c(u_{n-1})=\rho$ and $c(v_{n-1})=0$; S-family with trailing $\rho$ |
| O3a | $u_0\to u_{n-1}$ ($\sigma'$ is unique), giving link $(0,\sigma',0,\sigma,1)$; then $u_{n-1}\to v_{n-2}$ ($\sigma$ is unique) | $v_{n-2}=\sigma$, since it meets $v_{n-1}=0$ and $u_{n-1}=\sigma'$; $u_{n-2}=1$ | $Z(n-2)$ with link $(1,c(v_{n-3}),1,\sigma,0)$. If $c(v_{n-3})=0$, fill; otherwise this is $S_{\tau1}$ with $\rho=\sigma$ |
| O3b | $u_0\to u_{n-1}$ (1 is unique), giving link $(0,1,0,x,y)$ with $\{x,y\}=\{2,3\}$; then $u_{n-1}\to v_{n-2}$ ($x$ is unique) | $x=c(v_{n-2})$ and $y=c(u_{n-2})$; $c(v_{n-3})=0$, since it meets $x$ and $y$ | $Z(n-2)$ of type $S_0$ with link $(1,0,y,x,0)$ |
| O2 | the audit's doubled-1 recurrence D, from $u_0$ (§6) | | |

The states after the opening are:

- In O1, $u_0=\tau$ and $v_{n-1}=0$ are written. The input colours $u_1=1$, $v_0=\rho$ and $u_{n-1}=\rho$ are unchanged.
- In O3a, $u_0=\sigma'$ and $u_{n-1}=\sigma$ are written. The input colours $v_{n-1}=0$, $v_0=\sigma$ and $u_1=1$ are unchanged. With $\rho=\sigma$ and $\tau=\sigma'$, the vertices $u_1$, $v_0$ and $v_{n-1}$ carry the same colours as after O1, and so does $u_0$.
- In O3b, $u_0=1$ and $u_{n-1}=x$ are written. The input colours $v_{n-1}=0$, $v_0=\sigma$ and $u_1=\sigma'$ are unchanged.

## 5. The step table: Z-states [hand]

A **Z-state** $Z(i)$ has its hole at $v_i$ with current $c(v_{i+1})=0$ and current $c(u_{i+1})=w\neq 1$. Put $\rho:=w$ and $\tau:=5-\rho$. The link is $(1,x,y,\rho,0)$, where $x=c(v_{i-1})\in\{0,\rho,\tau\}$ and $y=c(u_i)\in\{1,\tau\}$, with $x\ne y$.

The state is filled unless $\tau\in\{x,y\}$. That leaves exactly three rows, $S_{\tau1}$, $S_{\rho\tau}$ and $S_0$. Every proper case is listed below. In every row each slide moves onto a colour that is unique on the current link, which is shown in brackets.

| Row | Link at $v_i$ | Slides, with the forced colours read on the way | Outcome |
|---|---|---|---|
| $S_{\rho1}$ | $(1,\rho,1,\rho,0)$ | none | **fill** $v_i$ with $\tau$ |
| $S_{0,1}$ | $(1,0,1,\rho,0)$ | none | **fill** with $\tau$ |
| $S_{\tau1}$ ($A_\tau$) | $(1,\tau,1,\rho,0)$ | $u_{i-1}=\rho$ and $v_{i-2}=0$ are forced. $v_i\to v_{i-1}$ [$\tau$], giving link $(1,0,\rho,1,\tau)$; then $v_{i-1}\to v_{i-2}$ [0] | $Z(i-2)$ with $w=\rho$ and $x=c(v_{i-3})\ne0$; 2 slides |
| $S_{\rho\tau}$ | $(1,\rho,\tau,\rho,0)$ | $u_{i-1}=1$ is forced. $v_i\to u_i$ [$\tau$], giving $(0,\rho,\tau,\rho,1)$; then $u_i\to u_{i-1}$ [1], giving $(0,1,\rho,c(v_{i-2}),c(u_{i-2}))$ with $c(v_{i-2})\in\{0,\tau\}$ | branches A and B below |
| $S_{\rho\tau}$-A ($A_\rho$, outer $\tau$; the audit's tile) | $c(v_{i-2})=0$, $c(u_{i-2})\in\{\rho,\tau\}$ | If $u_{i-2}=\rho$, the link $(0,1,\rho,0,\rho)$ is **filled** after 2 slides. If $u_{i-2}=\tau$: $u_{i-1}\to v_{i-1}$ [$\rho$], giving $(1,0,\rho,1,\tau)$; then $v_{i-1}\to v_{i-2}$ [0] | $Z(i-2)$, exactly $S_{\rho\tau}$ again, since $c(v_{i-3})=\rho$ is forced; 4 slides |
| $S_{\rho\tau}$-B ($B_\tau$) | $c(v_{i-2})=\tau$, which forces $u_{i-2}=\rho$ and $v_{i-3}=0$ | $u_{i-1}\to v_{i-2}$ [$\tau$], giving $(1,0,\rho,\tau,\rho)$; then $v_{i-2}\to v_{i-3}$ [0] | $Z(i-3)$ with $w=\rho$ and $x=c(v_{i-4})\neq0$; 4 slides |
| $S_0$ | $(1,0,\tau,\rho,0)$ | $v_i\to u_i$ [$\tau$], giving $(0,\rho,\tau,0,c(u_{i-1}))$ with $u_{i-1}\in\{1,\rho\}$. If $u_{i-1}=\rho$, **fill** after 1 slide. If $u_{i-1}=1$: $u_i\to u_{i-1}$ [1], giving $(0,1,0,p,q)$ with $\{p,q\}=\{2,3\}$; then $u_{i-1}\to v_{i-2}$ [$p$], and $v_{i-3}=0$ is forced | $Z(i-2)$, type $S_0$ with $(\rho,\tau):=(p,q)$; 3 slides |

These rows are not separate theorems. Each forced colour is the unique colour in $\{0,1,2,3\}$ allowed by the listed neighbours. For example, in $S_{\rho\tau}$, $u_{i-1}$ meets $a=0$, $u_i=\tau$ and $v_{i-1}=\rho$, so it is 1.

**Families are closed.** Rows $S_{\tau1}$ and $S_{\rho\tau}$ return a Z-state with the **same** $\rho$ and with $x\neq0$; the next $x$ meets a vertex whose colour was 0 before the step. They therefore never return $S_0$ (**S-family**). Row $S_0$ returns $S_0$ (**S0-family**). The Q-type, $w=1$, is never reached.

**Rewrite sets.** A step from $v_i$ that lands at $v_j$ rewrites only vertices of index in $(j,i]$:

- $S_{\tau1}$ rewrites $\{v_i,v_{i-1}\}$;
- A rewrites $\{v_i,u_i,u_{i-1},v_{i-1}\}$;
- B rewrites $\{v_i,u_i,u_{i-1},v_{i-2}\}$;
- $S_0$ rewrites $\{v_i,u_i,u_{i-1}\}$.

**Distinctness.** The step reads only $v_{i+1},\dots,v_{i-4}$ and $u_{i+1},\dots,u_{i-3}$. Every inference is "$X$ is adjacent to $Y$, so $c(X)\neq c(Y)$". These stay valid when two names coincide, because a coincidence only makes a case contradictory, and so vacuous. Two checks are needed beyond that:

- No vertex read after a rewrite aliases a rewritten vertex. This needs $n\ge5$.
- At $n=5$, $v_{i-3}$ is adjacent to $v_{i+1}$. So B and the landing of $S_0$, which both need $v_{i-3}=0$ next to $v_{i+1}=0$, cannot occur at $n=5$.

## 6. The doubled-1 recurrence D [cited: audit chat; re-checked]

The source is `doubled-one-opening-audit.md`. The hole is $u_i$, with link $(0,1,\rho,\tau,1)$ on $(a,u_{i+1},v_i,v_{i-1},u_{i-1})$.

1. Slide $u_i\to v_i$ [$\rho$], giving link $(1,\tau,\rho,1,c(v_{i+1}))$ with $c(v_{i+1})\in\{0,\tau\}$.
2. If $c(v_{i+1})=\tau$, **fill** $v_i$ with 0.
3. Otherwise slide $v_i\to v_{i+1}$ [0]. The colours $p=c(u_{i+2})$, $q=c(v_{i+2})$ with $\{p,q\}=\{2,3\}$, and $c(u_{i+3})=1$, are forced.
4. Slide $v_{i+1}\to u_{i+2}$ [$p$]. This gives $D(i+2)$ with link $(0,1,q,p,1)$.

The step rewrites $\{u_i,v_i,v_{i+1}\}$, all of index below the new hole. O2 is $D(0)$.

## 7. Termination: one potential, the linear interval, and the caps [hand]

Fix the input colouring $c^0$, after normalisation and, if used, $R$.

**Linear unprocessed interval.**

- For the downward Z-walk at $Z(j)$ with $1\le j\le n-2$, put $I_j=\{v_0,\dots,v_{j-1}\}\cup\{u_1,\dots,u_j\}$.
- For the upward D-walk at $D(i)$ with $0\le i\le n-2$, put $I_i=\{v_i,\dots,v_{n-1}\}\cup\{u_{i+1},\dots,u_{n-1}\}$.

These are index intervals of $\{0,\dots,n-1\}$ taken **without wrap**. The potential is $\Phi=|I|$: $\Phi=2j$ for Z and $\Phi=2(n-i)-1$ for D.

**Invariant.** Every vertex of $I$ carries its input colour $c^0$.

- It holds at the first state. The openings rewrite only $u_0$, $v_{n-1}$ and $u_{n-1}$ (for Z), or nothing in $I_0$ (for D).
- It is preserved. A step rewrites only vertices strictly between the old hole and the new hole (§5, §6), and those vertices leave $I$.
- Each return lowers $\Phi$ by exactly 4 (A-type returns, $S_0$ and D) or by 6 (B).

So the walk stops after at most $\Phi_0/4$ returns. It never laps, because $I$ is linear and only shrinks. It remains to show that the walk is filled before $j$ or $i$ would leave the linear range. That is the cap.

**Next-zero property.** An S-family step from $j$ lands at the largest $j'<j$ with $c^0(v_{j'})=0$, by the forced colours of §5. An $S_0$ step and a D step land at exactly $j-2$ and $i+2$.

**Cap S** (O1 and O3a). Here $c^0(u_1)=1$ and $c^0(v_0)=\rho$, with $\rho$ the family colour, and both lie in $I$. Every S-landing at $v_j$ has $c(u_{j+1})=\rho$, while $u_j$ keeps its input colour. Since $v_1$ meets $v_0=\rho$, either $c^0(v_1)=0$ or $c^0(v_1)=\tau$.

- **Short cap, $c^0(v_1)=0$.** By the next-zero property the walk cannot pass $v_1$ without landing on it. A landing there has link $(1,\rho,1,\rho,0)$, which is **filled**.
- **Long cap, $c^0(v_1)=\tau$.** Then $c^0(v_2)=0$. Otherwise $v_2=\rho$ forces $u_2=1$, adjacent to $u_1=1$. Also $c^0(u_2)=\rho$, forced by $a$, $u_1$, $v_1$ and $v_2$. A landing at $v_2$ would put $\rho$ on $u_3$ next to $u_2=\rho$, which is impossible. Since $v_2$ is a zero of $I$, the walk is **filled** before reaching it.

The walk starts at $j=n-2\ge3$. A step from $j=3$ reads only $I_3\cup\{v_3,u_4,v_4\}$. So no step ever reads across the cap except the landings just named, and every landing satisfies $j\ge1$. A B-step from $j=3$ would need $c^0(v_0)=0$, so it does not occur.

**Cap S0** (O3b). Here $c^0(v_0)=\sigma$ and $c^0(u_1)=\sigma'$, which force $c^0(v_1)=0$. An $S_0$ state at $j$ has $c^0(v_{j-1})=0$.

- $S_0(1)$ would need $v_0=0$, and $S_0(3)$ would need $v_2=0$ next to $v_1=0$. Both are impossible.
- $S_0(2)$ has $c(u_3)=\rho_2$ and $c(u_2)=\tau_2$. Since $u_1\sim u_2$, $\sigma'\neq\tau_2$, so $u_1=\rho_2$. The first branch of $S_0$ then **fills** after 1 slide.
- Landings move by exactly 2 from $n-2$, so they reach 2 or 3 unless filled earlier.

**Cap D** (O2). Here $c^0(u_{n-1})=1$ and $c^0(v_{n-1})=\tau_0\neq0$. A $D(i)$ landing has $c(u_{i+1})=1$ and forces $c^0(u_{i+3})=1$.

- $D(n-3)$ would put 1 on $u_{n-2}$ next to $u_{n-1}=1$, which is impossible.
- At $D(n-2)$, $v_{n-1}$ meets $b$, $v_{n-2}=\rho$ and $u_{n-1}=1$, so $c^0(v_{n-1})\in\{0,\tau\}$. It is not 0, so it is $\tau$, and step 2 of D **fills**.
- Landings move by exactly 2 from 0.

**Length [hand].** Each return uses at most as many slides as its drop in $\Phi$. The opening uses at most 2 slides and the final partial step at most 2. So every unequal belt start fills within $2n$ slides.

**[computed]** The longest replayed walks are 4, 10 and 14 slides for $n=5,8,11$. The shortest slide walks found by BFS are at most 2, 4 and 6.

**$n=5$ explicitly [hand].** The start index is $n-2=3$.

- O1: $c^0(v_3)=0$ makes the long cap impossible, because $v_2=0$ would sit next to $v_3=0$. That is the audit's point. The walk lands at $v_1$ and fills, or is filled at the start.
- O3a: if $c^0(v_2)=0$ the start fills; otherwise $S_{\tau1}$ lands at $v_1$, which is filled.
- O3b does not occur. It forces $c^0(v_2)=0$ from the opening and $c^0(v_1)=0$ from the cap, and $v_1\sim v_2$.
- O2: $D(2)=D(n-3)$ is impossible, so D fills at its first step.

**[computed]** The opening counts are as follows.

- $n=5$: F0 10, O1 4, O2 1, O3a 4, O3b 0.
- $n=8$: F0 48, O1 24, O2 17, O3a 8, O3b 24.
- $n=11$: F0 462, O1 92, O2 81, O3a 92, O3b 80.

Here F0 is "already filled", and each count includes the reflected starts. That is 19, 121 and 807 unequal orbits, matching the earlier census.

## 8. What the replay asserts

`belt_joined_check.py` imports none of the team's earlier code. For hole $u_0$ it enumerates every proper colouring of $G_n-u_0$ for $n\in\{5,8,11\}$: 20, 122 and 808 orbits, with labelled counts 480, 2 928 and 19 392. For each start it does the following.

- **Equal poles.** It applies the star swap and checks that the component is exactly as stated in §3.
- **Unequal poles.** It runs the walk of §4–§7. The opening class is chosen by the table. At every state the row is chosen by the table, and any state outside it raises an error. Every forced colour is asserted, and every slide is checked to be legal and proper. At every landing it asserts the linear-interval invariant, a drop in $\Phi$ of exactly 4 or 6, and the linear index range. The walk must end filled.
- **Independent BFS.** It also runs a separate breadth-first search: slides only for unequal starts, and slides with Kempe swaps for equal starts.

Pole holes are replayed as in §2, including the belt walk after the singleton slide. Rotation, ring swap and reflection are checked to be automorphisms. Every start was covered, with no uncovered state. The output is in `belt-joined-check.txt`.

## 9. What remains open

1. **The no-singleton pole case.** It rests on Florek's Theorem 3.1 **[cited]**. Long Table has neither re-proved it nor checked it beyond $n=5,8,11$, where the Kempe graph is connected **[computed]**. A self-contained hand argument is **[open]**.
2. **Identification with Florek's graph.** That our $G_n$ is Florek's graph for every $n$ rests on his definition **[cited]**.
3. **Review.** The page has not been reviewed by the math team or the audit chat.
4. **Other residues.** *[Updated 5 October by Long Table.]* The replay has also been run for $n=6,7,9,10$, using block words AAA, AAB, AAAB and AAAAA. The output is in `belt-joined-check-residues.txt`. Every unequal start is classified and fills; the invariant and the drop in $\Phi$ hold at every landing; the explicit colouring is proper; and $G_n-a$ has one Kempe class. Equal-pole belt deletions are 1, 0, 1 and 0 orbits, consistent with §0. Nothing was computed for $n\ge14$ (team rule); the hand proof covers those $n$.
5. **Novelty.** No historical novelty is claimed.
