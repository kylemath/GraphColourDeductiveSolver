# Lyapunov certificates on the vacancy slide

4 October 2026. Seed: Lyapunov functions and barrier certificates, including Parrilo's sum-of-squares certificates and discrete Lyapunov functions on graphs. Variability seed 88. This note does not claim a four-colour proof, and it does not search the corpus.

A state is a hole together with a proper 4-colouring of the remaining triangulation. A legal slide moves the hole to a boundary vertex whose colour appears once. The slide writes that colour onto the old hole, so the multiset of colours on the coloured vertices is unchanged. Kempe swaps and the equal-pole star swap are different moves. The function asked for has to fall along a legal move and has to be computed from the current hole and the current colouring.

The pairs $(\mathrm{shortLinks}, q)$ and $(H, q)$ already fall on all 21 published mass traps and then stick: $(\mathrm{shortLinks}, q) = (0, 96)$ at the degree-6 vertex 11 of order 17 graph 3, and $(H, q) = (0, 111)$ at root 0, colouring 37. Both pairs are constant on the exchange below, so this note does not refit them.

## The exchange is one coloured map

Order 17, graph 0, has automorphism group of order 4. The published stuck states are root 9, colouring 18, and root 14, colouring 21. Both have sorted population $(4,4,4,4)$, hole degree 5, $p = 1$, and $q = 138$. The singleton slide each way exchanges them.

The involution

$$
\varphi = (0\ 12)(1\ 11)(2\ 16)(3\ 13)(4\ 6)(7\ 10)(8\ 15)(9\ 14),
$$

fixing vertex 5, is a rotation-preserving automorphism of this triangulation. Transporting colouring 18 along $\varphi$ reproduces colouring 21 with the colours unpermuted. A second, orientation-reversing involution does the same after swapping canonical colours 0 and 1. Both checks use the published colourings and the one stored rotation of this graph.

Consequently every function of the coloured map — population, degree, boundary word up to dihedral action, $q$, $\mathrm{shortLinks}$, $H$, any polynomial in those quantities — takes the same value at the two ends. The geometric slide has a well-defined decrease only for a function that breaks $\varphi$.

## Five candidates

Seed 88 keeps the four constructions named in the seed and selects one more. The extra list is Sontag's control Lyapunov, Branicky's multiple Lyapunov functions, a Willems storage function, the path-complete graph Lyapunov function, and an occupation-measure barrier. Index $88 \bmod 5 = 3$, so the fifth candidate is the path-complete function. Its elementary piece on a 2-cycle is the label of the hole.

| Candidate | On the 9↔14 slide | On slides in general | Needs the list of 4-colourings | Verdict |
|---|---|---|---|---|
| Strict height on the slide digraph | one arrow rises | the class is empty | no | KILL |
| Parrilo polynomial in the colour counts | constant | constant | yes, off $G_n$ | KILL |
| Barrier certificate for a bad population | constant | constant | yes, off $G_n$ | KILL |
| Rantzer density | divergence cancels | reversible chain | the target set does | KILL |
| Path-complete pieces, and the hole label | equivariant reading is constant | the label changes | no | KILL |

## 1. Strict discrete Lyapunov on the slide graph — KILL

A discrete Lyapunov function on a directed graph is a real height that falls on every arc. It exists exactly when the digraph has no directed cycle: around a cycle the drops telescope, and a strict drop on every arc sums to a negative number on the empty telescoping sum.

The slides $9 \to 14$ and $14 \to 9$ are such a cycle. Summing $V(14) - V(9)$ and $V(9) - V(14)$ gives 0, so at least one arrow has nonnegative change. The same identity kills every common strict Lyapunov of the slide dynamics, at every polynomial degree. Parrilo's sum-of-squares program is a sufficient SDP for a polynomial inequality of this kind. The linear program that asks for $V(s') \le V(s) - 1$ on every slide is already infeasible, so the SDP stays infeasible when more monomials are added.

Feasibility of a height that falls on every legal slide: **Low**. The exchange is the obstruction.

## 2. Sum of squares in the colour counts — KILL

Let $n_0,n_1,n_2,n_3$ be the colour counts on the coloured vertices, and let $\pi$ be that 4-tuple written in nondecreasing order. A slide preserves the multiset, so every polynomial $p(n_0,n_1,n_2,n_3)$, and every function of $\pi$, is constant on every slide. The exchange is one instance: both ends have $\pi = (4,4,4,4)$.

Parrilo's certificate would ask for $- \Delta p$ to be a sum of squares along the legal vector field. Along a slide the difference is the zero polynomial, which is a sum of squares and certifies only a weak Lyapunov. The user-facing rule kills a function that is constant on a slide.

The one case where a function of $\pi$ is already a Lyapunov sits on a different move. On Florek's graph $G_n$ with $n = 3k+2$, the equal-pole star swap changes the partial counts $(2, 2k+1, 2k+1, 2k+1)$ into $(k+2, k+1, 2k+1, 2k+1)$, and filling the freed colour produces $(k+2, k+2, 2k+1, 2k+1)$. For $k = 2$ the sorted tuples are $(2,5,5,5)$, then $(3,4,5,5)$, then $(4,4,5,5)$. The $L^1$ distance to Florek's set $\{(4,4,5,5)\}$ therefore runs $3 \to 1 \to 0$. Slides leave it at 3. That distance is legal on this family because Florek enumerated the full counts. It is a Lyapunov of the star swap. It is constant on slides, so it is not a Lyapunov of the slide.

On a general spherical triangulation the same formula replaces $\{(4,4,5,5)\}$ by the set of sorted counts of the 4-colourings. That set is the theorem. The order-17 exchange is not a state of $G_8$: its coloured population sums to 16, and $(4,4,5,5)$ sums to 18.

Feasibility on the equal-pole star swap in the Florek family: **High**. Feasibility of any polynomial in the colour counts as a slide Lyapunov: **Low**. Feasibility of the same distance on a general triangulation: **Low**.

## 3. Barrier certificate — KILL

A barrier certificate in the sense of Prajna and Jadbabaie is a function $B$ with $B \le 0$ on the initial set, $B > 0$ on the unsafe set, and with the dynamics unable to cross from $\{B \le 0\}$ into $\{B > 0\}$. Sum-of-squares supplies a sufficient condition for the crossing inequality. The certificate is an invariance statement. It does not force a trajectory to reach a fill.

On $G_8$ the distance in candidate 2 is this kind of barrier for the slide dynamics: the population $(2,5,5,5)$ stays at distance 3 under every slide, so no slide path enters the enumerated set $\{(4,4,5,5)\}$. The star swap is the move that crosses it. That is the conserved-charge barrier already recorded for this family.

Read as a search function on a general triangulation, the unsafe set has to be named. Taking it to be the populations that never appear in a 4-colouring imports that list. Taking it to be the stuck orbits imports a pass/fail label. Taking it to be $\{p = 1\}$ gives $B = p$, which equals 1 at both ends of the exchange and at every scored landing of the 21 traps. A storage function with zero supply on slides, in Willems' sense, reproduces the same invariant: on a cycle the storage is constant.

Feasibility of the population barrier as a confinement statement for slides on $G_8$: **High**, and the escape is the star swap, which is already proved for equal poles. Feasibility of a barrier that separates the exchange from a fill using only the current hole and colouring: **Low**.

## 4. Rantzer density — KILL

Rantzer's dual replaces a decreasing function by a positive density whose flux has positive divergence, and concludes that almost every trajectory approaches the equilibrium. On a finite graph the divergences sum to zero. They cannot be strictly positive on every unfilled state.

The exchange already shows the cancellation. Let $\alpha$ be the flux of $9 \to 14$ and $\beta$ the flux of $14 \to 9$. The divergences are $\beta - \alpha$ and $\alpha - \beta$. Both are positive only if a number is positive and negative. The stationary choice $\alpha = \beta$ gives divergence 0, which is the density analogue of a function constant on the exchange. Slides are involutions on the whole reconfiguration graph, so the same cancellation holds on every component: the simple random walk has a stationary distribution and does not drain onto a proper subset of holes.

A density that treated fillable states as the equilibrium has to know which states are fillable. That is the third kill.

Feasibility of a density certificate that forces the vacancy into a fill: **Low**.

## 5. Path-complete pieces and the hole label — KILL

A path-complete graph Lyapunov function assigns several functions to the modes and demands a drop only after switching from one piece to another. On the exchange the two pieces $V_{9} = \mathbf{1}_{\mathrm{hole}=9}$ and $V_{14} = \mathbf{1}_{\mathrm{hole}=14}$ do that: each arrow leaves the piece that equals 1 and arrives at the piece that equals 0. Two steps later the hole and the colouring are restored. The bookkeeping drops; the state returns. A contraction along every infinite slide word is incompatible with that return.

The single function $V(r, c) = r$, the plantri label of the hole, is the corresponding control Lyapunov. It is evaluable from the hole alone. It changes on every slide, and $V(9) = 9 \ne 14 = V(14)$, so the three literal screens — constant on the exchange, constant on a slide, undefined without a 4-colouring — do not remove it.

$\varphi$ does. It identifies the two coloured states and swaps the labels 9 and 14, so the sign of $V(14) - V(9)$ reverses when the same geometric slide is written in the transported labeling. The decrease is a property of the numbering, not of the coloured map. Every equivariant reading of this candidate is constant on the exchange and dies with candidates 1–4.

The minima of the label are lowest vertex numbers, not fillable holes. From colouring 18 the slide to vertex 3 drops the label from 9 to 3 and lands on a degree-6 hole whose boundary still has four colours ($q = 126$ in the published recompute). $K_5$ with one vertex deleted has a legal slide along every boundary vertex and has no 4-colouring; the same label stops at the smallest index with the hole still open. A control barrier or an occupation measure whose zero set is exactly the fillable states needs that set as input, and dies by the third screen.

Feasibility of a symmetry-breaking label, or of a path-complete switching certificate, as a rank that reaches a fill: **Low**.

## Feasibility

An equivariant function that falls on every legal slide: **Low**, refuted by the 2-cycle.

An equivariant control Lyapunov that stays constant on the exchange and falls on some other move: **Low**. That is the search which produced $(\mathrm{shortLinks}, q)$ and $(H, q)$, already stuck at $(0, 96)$ and $(0, 111)$.

The $L^1$ distance from the sorted counts to $\{(4,4,5,5)\}$, as a Lyapunov of the equal-pole star swap on $G_n$: **High**. The same formula on a general triangulation: **Low**.

A polynomial or density certificate of slide progress that does not consult a 4-colouring: **Low**. The cycle obstruction is independent of degree, and the divergence obstruction is independent of the choice of positive weights.

## Next step

Keep the star-swap distance on the Florek family as the Lyapunov of that one Kempe move. Do not score another function of the colour counts, and do not score another pair built from $q$, against the 21 traps. The exchange has no invariant strict decrease; the open hand argument is the unequal-pole belt, which this note does not enumerate.

## Verdict

**KILL ALL.**
