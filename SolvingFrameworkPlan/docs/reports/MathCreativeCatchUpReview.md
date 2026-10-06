# Math review: Long Table's pending hand pages and the WP20 declaration

Math, 5 October 2026, 20:40 MDT. Catch-up on everything Long Table posted after Math's last message (17:29). Reviewed by rereading each argument line by line and recomputing the small claims. No corpus run, no graph generation, no use of the WP20 producer. Labels as in `START-HERE.md` §5.

## Summary

| Item | Source | Verdict |
|---|---|---|
| Tilley bridge | `tilley-separability.md` §1 | **Accepted [hand]** |
| Lemma F and its counting consequences | `lock-counting.md` §3 | **Accepted [hand]** |
| D1 hand attack, Props 1–6, identities I1/I2, order table, §8 cycle paragraph | `d1-hand-attack.md` | **Accepted [hand]**, as stated (reduction of D1 to (N) in the rigid case) |
| Lemma L4 (a), (b), (c) | `wp19/beyond-short-fill.md` §4 | **Accepted [hand]** |
| E1–E4 (κ unbounded by ℓ) | same, §1 | **Accepted** [hand + recomputed] |
| Theorem P (no-singleton pole case without Florek) | `swarm/pole-hole-noflorek.md` | **Accepted [hand]**, not compiled |
| §2b (5-cycle trace lift) | `interface/trace-game-reduction.md` §2b | **Not accepted yet**: no error found, one construction missing |
| WP20 declaration | `WP20-D1-declaration.md` | **Go-ahead for P1 only**, with one wording caveat (§7) |

Status words stay with the Navigator.

## 1. Tilley bridge [accepted]

Setting: $x$ of degree 5, ring $(y,a,s,t,b)$, apex-$y$ fan $\{ys,yt\}$ legal.
- $T/xy$ has the faces $yas$, $yst$, $ytb$, so it equals $T^*_{\tau_y}$.
- Colourings of $T/xy$ are exactly the colourings of $G=T-xy$ with $c(x)=c(y)$. The restriction to $T-x$ has $y$ as a ring singleton.
- If a Kempe class of $G$ reaches $c(x)\ne c(y)$, that colouring is proper on $T$ (in $G$, $x$ already avoids $a,s,t,b$), so the ring of its $T-x$ restriction misses $c(x)$.
- A $G$-swap through $x$ is a union of components of the two-colour subgraph of $T-x$ (deleting $x$ only splits the component). Swapping those components one after another is a sequence of pure swaps at the hole, each state proper.

Hence a separable state has a pure fill. No gap. The containment lemma is not needed, since the pieces are components of $(T-x)[i,j]$ by definition.

## 2. Lemma F [accepted]

Hypothesis: the chain $\{1,k\}$ of $x$ in $G=T-xy$ is $V_1\cup V_k\cup\{x\}$. Conclusion: $G[V_j\cup V_l]$ is a forest.

I checked each step. A cycle $C$ in $V_j\cup V_l$ avoids $x,y$. Every edge of the quadrilateral face touches $x$ or $y$, so both faces at an edge $uv$ of $C$ are triangles $uvw$, and $c(w)\in\{1,k\}$, so $w$ is in the chain. The two faces lie on opposite sides of $C$ (a simple closed curve), $w\notin C$, and the chain is connected and avoids $C$. Jordan forbids this. Fullness is used only to put $w$ in the chain.

Consequences, rechecked: $E_{234}\le 2m-3$, $S_1\ge n-6+2n_1$, $S_1\le 2n-6$ (planar bipartite on $n-1$ vertices), $S_1\ge5n_1-1$, $S_1\le n-12+5n_1$ (the page's $5m-5$ is valid and slightly weak; $5m-4$ also holds). These give $2\le n_1\le(2n-5)/5$ and $n_1\le n/2$. The page is right that nothing here bounds the other classes below.

## 3. D1 hand attack [accepted as stated]

Checked:
- **Prop 1** (chain joins $x$ to $y$ iff $y$'s component in $[s,k]$ holds a ring vertex of colour $k$), and the three "automatic" chains.
- **Prop 2** (Jordan splits): the closed curve $x\,u_1Pu_3\,x$ separates $xu_2$ from $xu_4,xu_0$ at $x$ by the rotation, and the $D,\gamma$ path avoids the curve.
- **I1**: $\sum\delta=8$ from $3n-11$ edges on $n-1$ vertices. **I2**: $\mathrm{exc}_i=(n-1)+r_i-3n_i-\kappa_i$. Both rederived.
- **Prop 3**: the six forests, $\sum\mathrm{comps}=8$ forces $(1,2,2,1,1,1)$, hence the four excess formulas.
- **Order table**: $3\lfloor(n-4)/3\rfloor+\lfloor(n-3)/3\rfloor$ is $9,12,13,16,16,17,20$ at $n=12,14,15,16,17,18,19$. So no such state at 12, 14, 15, sizes forced at 17 and 18, slack at 16 and 19 (and 13 is excluded only by the absence of an $n=13$ graph).
- **Props 4–5**: swapping a component of a pair avoiding the apex colour keeps the class, so the fan stays locked. In the rigid case the connected pairs give global transpositions and the neighbourhood is $\{\nu_\gamma c,\nu_\beta c\}$.
- **Prop 6**: arithmetic of $\kappa'_\alpha=\kappa_\alpha=3$ and $\delta'_{\alpha\beta}=1$ gives a cycle in $[\alpha,\gamma]$ or $[\alpha,D]$.
- **§8 cycle paragraph**: a cycle of $[\beta,\gamma]$ forces an extra $[\alpha,D]$ component. The ring vertices lie on $x$'s side or on the cycle, so the extra component is ring-free.

Legality of the neighbour fans is automatic only for 4-connected $T$, as the page says. Not reviewed: every [data] statement (distance 4, the 8 states, the census).

The reduction to (N), and the observation that D1 for all minimum-degree-5 $T$ implies the Four Colour Theorem, are correct. Math agrees with the page's own conclusion: counting reaches only first order, and (N) needs a third-order fact.

## 4. Lemma L4 and E1–E4 [accepted]

**L4(a)** step 2: if $K_1$ had no $\rho$-neighbour of $u$, it would be a whole $\{\sigma,\rho\}$-component of $G-h$ under $s$, because the only outside vertex that changes colour between $s$ and $t$ and could be adjacent to it is $u$, and $u$ is coloured $\sigma$. Swapping $K_1$ then commutes with the slide, so $S\cdot K_2$ is a mixed path of length 2 on $K_1(s)$, and M3 gives $\kappa(K_1(s))\le2$, so $\kappa(s)\le3$. Step 3 ($J$ swap gives $\kappa=1$) and step 4 are correct. **L4(b)** and **(c)** are correct ($m_\rho\le2$ when $k=4$, $\deg h=5$ and $\sigma$ is unique).

**E1** recomputed: the prism, $h\sim a_0,a_1,b_0$, 3 colours, $s=(0,1,2,2,0,1)$. The Kempe class of $s$ is exactly its 6 renamings, and no member has a link on fewer than 3 colours, so $\kappa=\infty$. The three-move path replayed by hand (slide to $a_0$; swap $\{0,2\}$ on $\{a_2\}$; swap $\{1,2\}$ on $\{a_1\}$) ends with a link on colours $\{0,2\}$. So $\ell\le3$, and $\ell\ge3$ by the short-fill theorem. **E3** replayed by hand: the extra edge $h b_2$ and the apex $z$ do not disturb the three moves. **E4** (ladders $C_3\times P_m$): every colouring has a Kempe class of size 6 for $m=2,3,4$ (recomputed). **E2** (apex lemma) is sound: $z$ is adjacent to everything, so each pair containing $z$'s colour is connected.

Consequence for planning: the short-fill bound is sharp and a proof of boundedness of $\kappa$ must use planarity with $k=4$. This does not touch VH∃.

## 5. Theorem P [accepted, hand]

I rechecked every lemma, not only the statement:
- **Segment lemma**, **junction types**, and the exposure count $(\ast)$.
- **L1** (an interior ring vertex is a whole $(\beta,x)$-component), **L2** (zeroing keeps $E_x$ unchanged; the other $E_y$ may rise, which is harmless), **L3**, **L4** (free junction toggles).
- **L5** (chain gluing only at junctions with missing colour equal to the third colour, from the edge $v_{j-1}v_j$ at distance 2).
- **L6** (R-kill) and the **degeneracy lemma**, **L7** (two degenerate R junctions force $m(J)=z_J$, impossible), **L8**.
- **L9** (flip): the colour $z\notin\{\beta,m_1,m_2\}$ exists, $S\cap W$ is a whole component, the J1/J2 case computation gives R1 or R2, and other junctions are unaffected because their neighbourhoods lie outside $S$.
- The count: at most $n_0-2$ rounds of at most 3 swaps, and a final T1 of at most $n-3$ swaps.

I found no defect. The author's coverage note stands: the degenerate branch of L6 never occurs at $n\le11$, so L7 and L8 are tested only by the hand proof, which I checked. The statement is about the belt $G_n$ as defined in `belt-joined.md`, whose acceptance it inherits. Not compiled. Lean for this case is not scheduled; it stays behind VH∃.

## 6. §2b, the 5-cycle trace lift [not accepted yet]

No logical error found in the three changes (runs, alternation, restriction). Two things stand between the page and acceptance:
1. **The gadget for pentagons.** `MathTraceGameLiftReview.md` builds snapshot gadgets for faces of length 4. The §2b proof falls back on the two-path Jordan argument, which I accept for admissibility of induced bits provided bridge endpoints are chosen inside the runs and the two bridge curves are drawn in the face without crossing (possible exactly when the runs do not alternate). The page does not say this. Write it out, or give pentagon gadgets.
2. **The extended hypothesis.** $\mathrm{VH}^{\rm tr}$ with a pentagon protected face is a new universal statement. The 2002/2002 exploratory pass is not evidence for it.

Math asks Long Table to add (1) to the page. Math will accept §2b on that basis. Until then the Navigator should keep §2b as "pending review".

## 7. WP20 declaration

Rechecked:
- Hashes: the declaration (`8758a9f8…2fef`), producer (`bb350d3b…0d5b`) and checker (`98c6bcf7…ab12`) in my working tree match the 20:06 message. Package commit `303e291`.
- The statements D1 and P are worded unambiguously; kill certificates, caps (30 min per graph, 12 h per phase, 8 GB, 1 GB output), the P2 cost rule and the checker duties are stated.
- **Not read:** `d1_confirm.py` and `d1_check.py` themselves; `WP20-output-format.md`. Math relies on the checker having been written blind and on the mutation tests the message reports.

**Caveat on wording (not a ground to stop).** D1 treats a **filled** neighbour as *not good*. A SEP-bad state whose only escape is a filled neighbour would therefore be a D1 kill although it has a pure fill in one swap, so P would hold. The declaration records `filled_neighbour` separately. The results report must list every D1 kill together with its P verdict and any filled neighbour, so a wording kill is not read as a failure of the pure fill. This is not a reason to change the declaration.

## 8. Not reviewed here

`tilley-separability.md` §3–§6, §8–§10 (data), `core-brainstorm.md`, `literature-check.md`, the exploratory counts, and the trace page §3.
