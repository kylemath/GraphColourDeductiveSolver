# Pole holes without Florek: the no-singleton case of the belt theorem by hand

5 October 2026. Long Table. This page replaces the one citation in `belt-joined.md` §2, case 3 (Florek, arXiv:2511.00485, Thm 3.1), with a hand argument. It is not compiled and no Lean was used. Labels: **[hand]** proved on this page; **[computed]** checked by `pole_hole_check.py` on $G_5,\dots,G_{11}$ only (output `pole-hole-check.txt`); **[open]** not established. Nothing was computed for $n\ge14$. The checker imports no team code.

## 0. Statement

**Theorem P [hand].** Let $n\ge5$ and let $c$ be a proper 4-colouring of $G_n-a$ in which every colour occurs at least twice on the ring $u_0\dots u_{n-1}$. Then a sequence of at most
$$3(n_0-2)+n-3\ \le\ 3\lfloor n/2\rfloor+n-9$$
Kempe swaps, with the hole fixed at $a$, reaches a colouring whose ring either uses at most 3 colours (a fill) or has a colour that occurs exactly once (a singleton). Here $n_0$ is the number of ring vertices coloured $c(b)$ at the start.

After a singleton, one slide $a\to u_i$ gives a belt hole, and `belt-joined.md` §3–§7 finish for every colouring of a belt deletion. So, with `belt-joined.md`, every pole hole of $G_n$ is resolved without Florek and without the Four Colour Theorem. The theorem is about $c$ alone, so the earlier caveat (that our $G_n$ is Florek's graph) is no longer needed for this case.

The bound is linear in $n$, not constant (see §8).

## 1. Setup [hand]

- Write $\beta=c(b)$. All moves below are Kempe swaps of $G_n-a$. Every swap either uses a pair $\{x,y\}\not\ni\beta$, or is a one-vertex $(\beta,\cdot)$ swap at a ring vertex. So $b$ is never recoloured, and $\beta$ is fixed throughout.
- **The cycle $C$.** List the belt as $C=u_0v_0u_1v_1\cdots u_{n-1}v_{n-1}$, so position $2i$ is $u_i$ and position $2i+1$ is $v_i$, mod $2n$. The belt edges are exactly the pairs at $C$-distance 1 or 2:
  - distance 1: $u_iv_i$ and $v_iu_{i+1}$ (the edge $u_{i+1}v_{i}$);
  - distance 2: $u_iu_{i+1}$ and $v_iv_{i+1}$.

  So the belt is $C_{2n}^2$. This is **[computed]** in the checker for $n=5..11$, and immediate from the edge list.
- Every $v$ is adjacent to $b$, so no $v$ has colour $\beta$. Consecutive triples of $C$ are triangles.
- **Size.** A no-singleton start uses 4 colours, each at least twice, so $n\ge8$. That is why there are 0 such starts at $n=5,6,7$ **[computed]**. Hence in every lemma below, $u_{i-1},u_{i+1},v_{i-1},v_i$ are four distinct vertices.
- **Junctions.** A *junction* is a ring vertex coloured $\beta$. Junctions are pairwise non-adjacent on the ring. $n_0$ denotes the current number of junctions. If $n_0\le1$ the state is good.

## 2. Segment lemma [hand]

Let $u_s,\dots,u_t$ be a maximal ring run with no junction, lying between junctions $u_{s-1}$ and $u_{t+1}$. (If $n_0=1$, these are the same vertex.) The **segment** is the $C$-word
$$v_{s-1}\,u_s\,v_s\,u_{s+1}\cdots u_t\,v_t,$$
which has odd length $2(t-s+1)+1\ge3$.

**Claim.** The segment avoids $\beta$ and has period 3. It uses each of the three non-$\beta$ colours.

**Proof.** The $u$'s are non-junctions and the $v$'s are never $\beta$. Consecutive triples are triangles, so they use 3 distinct colours from a 3-set. Then $w_{k+3}\notin\{w_{k+1},w_{k+2}\}$ and $w_{k+3}\neq\beta$, so $w_{k+3}=w_k$. ∎

**[computed]** The checker asserts this at every state it visits.

## 3. Junction lemma and types [hand]

Let $u_i$ be a junction. Put $p=c(v_{i-1})$ and $q=c(v_i)$. Then $p\ne q$, since $v_{i-1}\sim v_i$, and both differ from $\beta$. Let $m$ be the fourth colour, the *missing colour* of $u_i$.

**Forced colours.**
- $c(u_{i-1})\in\{q,m\}$, since $u_{i-1}$ meets $u_i=\beta$ and $v_{i-1}=p$.
- $c(u_{i+1})\in\{p,m\}$, since $u_{i+1}$ meets $u_i=\beta$ and $v_i=q$.

This gives four types:

| type | $(c(u_{i-1}),c(u_{i+1}))$ | meaning |
|---|---|---|
| F (free) | $(q,p)$ | the four neighbours of $u_i$ in $G_n-a$ use only $p,q$ |
| R1 | $(m,p)$ | |
| R2 | $(q,m)$ | R1 mirrored by the reflection $R$ of `belt-joined.md` §1 |
| X | $(m,m)$ | |

**Exposure.** A non-junction ring vertex is *exposed* if a ring neighbour is a junction, and *interior* otherwise. $E_x$ is the number of exposed ring vertices of colour $x$. Each junction has two ring neighbours, so
$$\textstyle\sum_{x\ne\beta}E_x\le 2n_0.\qquad(\ast)$$
The exposed neighbours of a junction have colours $\{q,p\}$ (F), $\{m,p\}$ (R1), $\{q,m\}$ (R2), or $\{m\}$ (X).

## 4. The lemmas

**L1. Zeroing [hand].** Let $u_i$ be an interior ring vertex of colour $x\neq\beta$. Its neighbours in $G_n-a$ are $u_{i\pm1}$, which are not $\beta$ (interior) and not $x$, and $v_{i-1},v_i$, which are not $\beta$ (adjacent to $b$) and not $x$. So $\{u_i\}$ is a whole $(\beta,x)$-component, and swapping it recolours $u_i$ to $\beta$.

This does not change $E_x$. The only vertices whose exposure changes are $u_{i\pm1}$, and they are not coloured $x$.

**L2. Rule T1 [hand].** Suppose $E_x\le1$ for some $x\ne\beta$. Zero the interior $x$-vertices one at a time (L1), and stop as soon as $x$ occurs at most once. When every interior $x$ is zeroed, $x$ occurs exactly $E_x\le1$ times. So the state is good: a singleton $x$, or a fill if $x$ is absent. This uses at most $n_x-1$ swaps, where $n_x$ is the number of ring vertices coloured $x$.

**L3 [hand].** If $n_0\le2$ then T1 applies. By $(\ast)$, $\sum E_x\le4<6$, so some $E_x\le1$.

**L4. Rule F, the toggle [hand].** If $u_i$ is a free junction, its neighbours in $G_n-a$ are coloured $q,p,p,q$. So $\{u_i\}$ is a whole $(\beta,m)$-component. Swap it: $u_i$ becomes $m$, and $n_0$ drops by 1.

**L5. Chain lemma [hand].** Let $x,y\neq\beta$, let $z$ be the third non-$\beta$ colour, and let $W$ be the set of belt vertices coloured $x$ or $y$. Then:

1. Inside one segment, $W$ is connected. Every window of 3 consecutive positions holds two $W$-vertices (§2), so consecutive $W$-vertices are at $C$-distance $\le2$, and hence adjacent.
2. Two different segments are separated on $C$ by a junction position $2j$. An edge of $C^2$ between them must therefore be the edge $v_{j-1}v_j$, at positions $2j\pm1$.

So the $\{x,y\}$-components are unions of the $W$-parts of consecutive segments. They are glued exactly at the junctions with $\{c(v_{j-1}),c(v_j)\}=\{x,y\}$, that is, with missing colour $m_j=z$. They never contain $a$ or $b$.

**L6. Rule K, the R-kill [hand].**

*R1 at $u_i$.* The forced colours are $c(u_{i-1})=m$, $c(u_{i+1})=p$, $c(v_{i-1})=p$ and $c(v_i)=q$. Let $K$ be the $\{q,m\}$-component of $v_i$. Call $u_i$ *non-degenerate* if $u_{i-1}\notin K$. Then swap $K$:

- $v_i$ becomes $m$;
- $u_{i+1}=p$ and $v_{i-1}=p$ are untouched, because $p$ is not in the pair;
- $u_{i-1}=m$ is untouched, because $u_{i-1}\notin K$.

Now $u_i$ has $v$-pair $(p,m)$, missing colour $q$, and ring neighbours $(m,p)$. So it is free, and L4 recolours it $q$. That is 2 swaps, and $n_0$ drops by 1.

*R2* is the mirror image: use the $\{p,m\}$-component of $v_{i-1}$. The junction is non-degenerate if $u_{i+1}\notin K$, and the toggle colour is $p$.

**Degeneracy lemma.** If R1 at $u_i$ is degenerate, then every other junction has missing colour $z_J:=p$. For R2, $z_J:=q$.

*Proof.* At $u_i$ itself the $v$-pair is $\{p,q\}\neq\{q,m\}$, so $K$ does not cross $u_i$ (L5). Now $u_{i-1}$ lies in the left segment of $u_i$, and $v_i$ in the right one. To reach $u_{i-1}$, $K$ must cross every other junction going around the cycle. By L5, crossing junction $u_j$ means $m_j=p$. ∎

**L7 [hand].** If $n_0\ge3$, at most one R junction is degenerate.

*Proof.* Suppose $J\ne J'$ are both degenerate, and let $J''$ be a third junction. By the degeneracy lemma, $m(J')=m(J'')=z_J$ and $m(J)=m(J'')=z_{J'}$. So $m(J)=z_J$. But $z_J$ is one of the $v$-colours of $J$, and so differs from $m(J)$. ∎

**L8 [hand].** Suppose $n_0\ge3$, there is no F junction, every R junction is degenerate, and at least one R junction exists. Then T1 applies.

*Proof.* By L7 there is exactly one R junction $J$. All the others are X, with missing colour $z_J$ (degeneracy lemma), so they expose only $z_J$. $J$ exposes $m(J)$ and $z_J$. The third non-$\beta$ colour $w$, which is the other $v$-colour of $J$, therefore has $E_w=0$. ∎

**L9. Rule S, the flip [hand].** Suppose every junction is X, $n_0\ge3$, and T1 fails. Let $J_1=u_i$ and $J_2=u_j$ be consecutive junctions, so that $u_{i+1},\dots,u_{j-1}$ contain no junction. Let $S$ be the segment between them, and write $(p_1,q_1,m_1)$ and $(p_2,q_2,m_2)$ for their data.

Choose $z\notin\{\beta,m_1,m_2\}$, and let $\{x,y\}$ be the other two non-$\beta$ colours. By L5 the $\{x,y\}$-component of any $\{x,y\}$-vertex of $S$ is exactly $S\cap W$, since neither $J_1$ nor $J_2$ has missing colour $z$. Swap it. Then:

- **$J_1$.** Since $z\ne m_1$, either $z=q_1$ or $z=p_1$.
  - If $z=q_1$: $u_{i+1}$ goes $m_1\to p_1$ and $v_i=q_1$ stays. The ring neighbours are $(m_1,p_1)$ with missing colour $m_1$, so $J_1$ is R1.
  - If $z=p_1$: $v_i$ goes $q_1\to m_1$ and $u_{i+1}$ goes $m_1\to q_1$. The missing colour becomes $q_1$, and the ring neighbours $(m_1,q_1)$ make $J_1$ R2.
- **$J_2$**, by the mirror computation.
  - If $z=p_2$: $u_{j-1}$ goes $m_2\to q_2$, giving R2.
  - If $z=q_2$: $v_{j-1}$ goes $p_2\to m_2$ and $u_{j-1}$ goes $m_2\to p_2$, giving R1.
- **Other junctions.** Their $v$-neighbours and ring neighbours lie outside $S$, so they are unchanged.

By L7 at least one of $J_1,J_2$ is non-degenerate. Apply L6 to it. That is 3 swaps in all, and $n_0$ drops by 1.

## 5. The strategy and its termination [hand]

Repeat the following, stopping as soon as the state is good:

1. If some $x\ne\beta$ has $E_x\le1$, apply **T1** (L2). Stop: the state is good.
2. Else, if a free junction exists, apply **F** (L4).
3. Else, if a non-degenerate R junction exists, apply **K** (L6).
4. Else apply **S** (L9).

**Why this works.**

- Step 1 catches every state with $n_0\le2$ (L3). So steps 2–4 run only when $n_0\ge3$.
- If step 4 is reached, all junctions are X: there is no F junction, and by L8 there is no R junction either.
- Each round of steps 2–4 lowers $n_0$ by exactly 1 using at most 3 swaps.
- The number of rounds is therefore at most $n_0-2$.
- The final T1 costs at most $n_x-1\le n-n_0-1\le n-3$ swaps, since $n_0\ge2$ when it runs.

This gives the bound in Theorem P. Since junctions are non-adjacent on the ring, $n_0\le\lfloor n/2\rfloor$.

- **Index bookkeeping.** Every index above is mod $n$. Each rule reads only $u_{i\pm1}$ and $v_{i-1},v_i$, plus whole Kempe components. For $n\ge8$ these are distinct vertices.
- **Segments when $n_0\ge3$.** These are proper arcs. A one-junction wrap never occurs in steps 2–4.
- **Small $n$.** No case-specific argument is needed. There are no starts for $n\le7$, and $n\ge8$ is all the lemmas use.

## 6. The 33 hard starts at $n=11$ [hand trace, computed]

These are the orbits where no single Kempe swap gives a fill or a singleton. The strategy handles every one as **F + T1**, with 3 swaps **[computed]**. The checker's example is $\beta=0$, with
$$u=0\,1\,2\,0\,1\,2\,3\,0\,2\,1\,3,\qquad v=2\,3\,1\,2\,3\,1\,2\,1\,3\,2\,1.$$

**Initial state.** The ring counts are $0{:}3,\ 1{:}3,\ 2{:}3,\ 3{:}2$, so there is no singleton. The junctions are:

- $u_0$: $(p,q,m)=(1,2,3)$ with ring neighbours $(3,1)$, so R1;
- $u_3$: $(1,2,3)$ with neighbours $(2,1)$, so F;
- $u_7$: $(1,3,2)$ with neighbours $(3,2)$, so R2.

The exposed vertices are $u_{10}=3$, $u_1=1$, $u_2=2$, $u_4=1$, $u_6=3$ and $u_8=2$. So $E_1=E_2=E_3=2$, and T1 fails.

**The moves.**

1. **F:** $u_3\to3$. Now $n_0=2$, and the exposed vertices are $u_{10},u_1,u_6,u_8$. So $E_2=1$.
2. **T1 with $x=2$:** zero the interior 2's, $u_2$ and then $u_5$. Colour 2 now occurs only at $u_8$, which is a singleton.

## 7. Checker results [computed]

`pole_hole_check.py` enumerates every proper colouring of $G_n-a$ (all labels, with $b$ of any colour) for $n=5,\dots,11$. It runs §5 on every no-singleton start and asserts the following:

- the segment lemma and the junction lemma at every state;
- every forced colour named in L4, L6 and L9;
- each move is an exact Kempe component, recomputed independently, and leaves a proper colouring;
- the one-vertex components in L1 and L4, and the exact component $S\cap W$ in L9;
- the degeneracy lemma whenever an R junction is degenerate;
- $(\ast)$, and L3;
- each round lowers $n_0$ by exactly 1 within 3 swaps;
- the total bound of Theorem P;
- the final state is good.

| $n$ | no-singleton orbits (labelled) | ends good | max swaps | rules used | not fixed by one swap |
|---|---|---|---|---|---|
| 5, 6, 7 | 0 | – | – | – | – |
| 8 | 32 (768) | all | 1 | T1 | 0 |
| 9 | 138 (3 312) | all | 2 | T1, K, S+K | 0 |
| 10 | 630 (15 120) | all | 2 | T1, F+T1, K | 0 |
| 11 | 2 442 (58 608) | all | 6 | 14 patterns, including S+K+T1 and K+K | 33 (792), all F+T1 with 3 swaps |

The orbit counts match `belt-joined-check.txt` and `belt-joined-check-residues.txt`.

**Coverage gap.** The degenerate branch of L6 never occurs at $n\le11$. In 36 048 R-junction tests across $n=9,10,11$, none was degenerate. So L7 and L8 rest on the hand proof alone.

## 8. What is proved and what is open

- **[hand]** Theorem P holds for every $n\ge5$, so the no-singleton pole case needs no citation. Together with `belt-joined.md` §2 (cases 1–2) and §3–§7, every hole of $G_n$ reaches a fill with no appeal to Florek.
  - Move count: at most $3\lfloor n/2\rfloor+n-9$ Kempe swaps at the pole.
  - Then one slide.
  - Then the belt walk: at most $2n$ slides, or one swap.
- **[open]** A constant bound. Breadth-first search gives at most 3 moves at $n\le11$ (`belt-joined-check.txt`), but the hand strategy is only shown to be linear.
  - A single swap changes the ring count of a colour by at most the number of segments its chain covers.
  - So a constant bound for large $n$ would need long chains, or swaps at $b$.
  - One such swap is the $(\beta,z)$-component of $b$. When every junction is X, its ring part is exactly the X junctions with missing colour $\ne z$.
- **[open]** Review. Math has not reviewed this page.
