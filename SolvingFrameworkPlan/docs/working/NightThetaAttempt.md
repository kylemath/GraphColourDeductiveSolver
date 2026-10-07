# Night: the lock theta at a degree-5 hole (proof attempt on |DD_j| ≤ room_j)

Night swarm worker, 6 October 2026 (written about 23:50 MDT). **Exploratory. Hand work, unreviewed.** Labels: [proved] means a complete hand proof is given here; [sketch] means the argument is outlined and the gaps are named; [conjecture] means unproved. [computed] marks small single-core checks. The scripts were in the session scratchpad and were not committed. They used all degree-5 holes of the 42 gentri graphs at orders 16–19 (tri16–tri19).

Definitions follow `MathQuarterFloorBijections.md` (§0–§5) and `MathQuarterFloorFinal.md`. For an unfilled state s ∈ U_j the link reads (α, μ, α, A, B) at positions j..j+4. The vertices are m = x_{j+1}, a = x_{j+3} and b = x_{j+4}, and K := comp_{α,A}(x_{j+2}).

## Verdict

- **No proof of |DD_j| ≤ room_j.** The theta structure is real and gives exact, sphere-only statements at the level of a single state (§1–§3). It also gives a necessary condition for DL→DL (§3), but nothing that bounds DD_j by room_j.
- **Obstruction.** Every step proved here uses only Jordan separation on the sphere, plus Kempe moves near the hole. A minimal counterexample to 4CT satisfies all of these steps, and so do its targetless classes made entirely of DL rotation cycles (Theorem A). So the theta can only enter a proof together with a **counting** input of 4CT strength. §5 makes this precise.
- **Most promising next lemma:** the two-curve meander classification of §6. My first guess there, "every DD state forces an interior chain", was refuted by the data (395 counterexamples).

## 1. The theta, built correctly

**The locks share μ-vertices in general.** A lock-1 chain P₁ (an m–a path in {μ,A}) and a lock-2 chain P₂ (an m–b path in {μ,B}) can meet at any μ-vertex. [computed] Over the 5,787 DL states, |comp_{μ,A}(m) ∩ comp_{μ,B}(m)| has the following distribution: 1 in 379 states, 2 in 781, 3 in 1,135, 4 in 1,876 and 5 in 1,616. So the naive picture, in which the chains share only m, is the exception.

**Lemma 1.1 (theta) [proved].** Let s be DL, and fix chains P₁ and P₂. Let w be the last vertex of P₂ (oriented from m to b) that lies on P₁.
- w is coloured μ, since {μ,A} ∩ {μ,B} = {μ}. The case w = m is allowed.
- The paths β_m = v·m·P₁[m,w], β_a = v·a·P₁[a,w] and β_b = v·b·P₂[b,w] are internally disjoint paths from v to w. Here P₁[m,w] and P₁[w,a] are two pieces of one path, and P₂(w,b] avoids P₁ by the choice of w.
- So Θ = β_m ∪ β_a ∪ β_b is a theta graph in T with poles v and w.

Θ uses colours μ, A and B (and v) only. **It contains no α-vertex.**

**Proposition 1.2 (region assignment) [proved].** By Jordan's theorem for theta graphs, Θ cuts the sphere into three open discs: R_ma (bounded by β_m ∪ β_a), R_ab and R_bm. In the rotation at v, the three spokes vm, va and vb split the link as follows:
- the sector m → a contains x_{j+2};
- the sector a → b contains no link vertex (a and b are adjacent);
- the sector b → m contains x_j.

The edge v x_i leaves v inside its sector, and x_i ∉ Θ because it is coloured α. Hence:
- **x_{j+2} ∈ R_ma and x_j ∈ R_bm.**
- R_ab contains no link vertex.

The same statements hold for every choice of (P₁, P₂).

**Corollary 1.3 [proved].** Write C₁ = v·m·P₁·a·v and C₂ = v·m·P₂·b·v.
- K avoids C₂, so it stays on x_{j+2}'s side, and **K ∌ x_j**. This is L2 (⇒ R₊₃ is defined); it is pd2 Corollary (i) again.
- Likewise comp_{α,B}(x_{j+2}) avoids C₁, so it lies in R_ma and misses x_j and b.
- Hence **in a DL state the {α,A}- and {α,B}-subgraphs are both disconnected.** At most 4 of the 6 bichromatic subgraphs are connected. This is the audited "no frozen DL state" lemma, re-derived here.
  - [computed] Over the 5,787 DL states, the number of connected bichromatic subgraphs is 0, 1, 2, 3 or 4, in 76, 822, 1,987, 2,160 and 742 states respectively. The value is never 5 or 6.

**The α-vertices after rotation [proved].** s′ = R₊₃s has its α-vertices at x_j and x_{j+3} = a.
- x_j stays in R_bm.
- a moves from A to α, so the vertex a of Θ is recoloured. Every A-vertex of P₁ that lies in K also becomes α.
- **The old theta is destroyed exactly along P₁ ∩ K.** That set always contains a. P₂ is untouched, because K contains no μ- or B-vertex.

## 2. How the theta transforms under R₊₃

**Proposition 2.1 [proved].** Let s ∈ D_j and s′ = R₊₃s ∈ U_{j+3}. Then:
- μ′ = B, A′ = μ and B′ = A;
- m′ = b, a′ = m and b′ = x_{j+2}.

The theta's branches change as follows:
- **β_b (via P₂) survives** and becomes the new lock-1 chain (this is lock transfer: lock 1′ = lock 2 as vertex sets);
- **β_a dies**: a is recoloured α;
- the new lock-2 chain Q, from b to x_{j+2} in {A,B} of s′, **must be built from scratch**.

The new theta has a B-coloured pole w′ ∈ P₂ ∩ Q.

**Pentagram structure [proved].** Along a Γ-chain s₀ → s₁ → … the swapped components K_t change as follows.
- K_t meets the link-edge boundary exactly at the link edges e_{j+1} = x_{j+1}x_{j+2} and e_{j+3} = x_{j+3}x_{j+4}. These are the only link edges with exactly one end in K.
- The next swap is K_{t+1} = comp_{α,μ}(x_j) in s′, with link-edge boundary {e_{j+4}, e_{j+1}}.
- The chords therefore run through the pentagram {5/2}: {1,3} → {4,1} → {2,4} → {0,2} → {3,0} (relative to j). Consecutive chords share an endpoint.
- In Tait colours the link word is (p,p,q,p,r), and the triple colour cycles p → r → q.

So labelled rotation chains have period 15 in (chord, Tait pair). Up to renaming only the index period of 5 remains, which matches "cycle length ≡ 0 mod 5".

## 3. The DL→DL condition in theta terms

**Proposition 3.1 (escape criterion) [proved].** If s ∈ DD_j, then **every** lock-1 chain P₁ of s contains an A-vertex outside K. Contrapositive: if every A-vertex of comp_{μ,A}(m) lies in K, then R₊₃s is not DL.

*Proof.* Let Q be a lock-2′ chain in s′, coloured A and B in s′, from b to x_{j+2}.
- By 1.2, x_{j+2} ∈ R_ma, and b ∉ closure(R_ma) because b ∉ C₁. So Q meets C₁ − v.
- Every vertex of C₁ − v has an s′-colour in {μ, A (= A-vertices not in K), α (= A-vertices in K)}.
- Q's colours are A and B, so the meeting point is an A-vertex of P₁ that lies outside K. ∎

[computed] Over orders 16–18, all 554 DD states have such a vertex. Of the 1,710 DL states that are not DD, 839 (49 %) are caught by the contrapositive. So **the criterion is necessary but far from sufficient.**

**Twin rotation [proved + computed].** The alternative swap σ(comp_{α,A}(x_j)) differs from R₊₃ only by a renaming and by a swap of the {α,A}-components that avoid the link. So it can only escape when {α,A} has three or more components.
- [computed] Of the 1,129 DD states at orders 16–19, 873 have exactly 2 {α,A}-components; their twin is again DL, as it must be.
- 175 escape through the twin. 81 have three or more components and the twin is still DL.
- So "use the other component" does not close DD_j.

## 4. Monotonicity along DL chains (question 3)

- **No monotone quantity exists [proved, trivially].** Any state function is periodic along an all-DL Γ-cycle, and such cycles exist (length up to 880; MathQuarterFloorFinal adversarial row).
- [computed] At orders 16–19 there are no Γ-cycles, and the longest path has d(P) = 6.
- The only canonical periodic data are the chord sequence (period 5) and the triple Tait colour (period 3) from §2. They are forced locally, so they cannot carry class-level room.
- **Reconciliation [sketch].** Any argument must be **class-level**: it has to pay for a DL chain with non-DL or filled states that are not Γ-neighbours of the chain (the per-j matching radius grows to 7 at order 24).
  - A natural candidate source of such room is the "spare" components, i.e. {α,A}- and {α,B}-components that avoid the link. They exist, but §3 shows they do not always pay.

## 5. Where χ = 2 enters, and the torus

Planarity is used at exactly two steps, and each is one Jordan curve with two sides:

1. **Proposition 1.2 / Corollary 1.3.** The closed lock chain C₂ (or C₁) separates x_j from x_{j+2}. This gives L1/L2, so "R₊₃ is defined ⇔ lock 2", so Γ-degree = number of locks, and so the whole class identity. It also gives the disconnection of {α,A} and {α,B}.
   - On the torus, C₂ can be non-separating. The coordinator's torus control (local-runs/18-torus-floor/, commits a8ff093 and ba51875) has a frozen state at n = 16: every bichromatic subgraph is connected, the link uses four colours, and the state is DL with K ∋ x_j, so R₊₃ is undefined.
   - **This is exactly the step in 1.3 that fails** [proved, as the logical locus]: "K avoids C₂ ⇒ K misses x_j" needs C₂ to separate.
2. **Proposition 3.1.** Q must cross C₁. The same two-sides step is used again.

**Why the theta alone cannot prove the lemma [proved, meta].** Both uses above, and everything in §1–§3, hold verbatim in a planar minimal counterexample to 4CT. Theorem A gives a targetless class there: F = 0 and Γ consists entirely of DL cycles, so DD_j = D_j > 0 = room_j. So an argument that uses only Jordan (qualitative χ = 2) and Kempe moves cannot give |DD_j| ≤ room_j. **The quantitative χ = 2 (Euler, hence unavoidability) must enter as well.** The torus data agree: the torus fails already at the single-state level (frozen states), before any counting is needed. On the sphere, the single-state level is safe (§1.3), and the gap is purely class-level.

## 6. The single most promising next lemma

**Reconnection model [proved, hand; worth an independent check].** Work in Tait language: the dual of T − v is cubic with five dangling edges e_j..e_{j+4} carrying the word (p,p,q,p,r).
- R₊₃ swaps the (p,r)-path B₁ from e_{j+1} to e_{j+3}. B₁ reads p r p … r p; let its r-edges be y_i z_i for i = 1..k, in order.
- Delete those r-edges from the old (q,r)-subgraph. What remains is a set of non-crossing arcs on the two sides of B₁, joining the stubs y_i and z_i and the boundary points e_{j+2} (on one side) and e_{j+4} (on the other).
- Old structure: arcs plus the pairs (y_i, z_i). New (r,q)-structure: the same arcs plus the shifted pairs (e_{j+1}, y₁), (z₁, y₂), …, (z_k, e_{j+3}).
- **R₊₃s ∈ D_{j+3} iff, in the new structure, e_{j+4} is joined to e_{j+1}** (otherwise it is joined to e_{j+3}).

**First guess, refuted [computed].** I conjectured that every DD state forces a (q,r)-**cycle** (an interior Kempe chain) that crosses B₁. That would have meant every DD state carries a pattern-preserving move, ready for an injection into room_j. **It is false.** At orders 16–19, split by DD and by whether some r-edge of B₁ lies on a (q,r)-cycle:

| | some r-edge on a cycle | all r-edges of B₁ on C |
|---|---|---|
| DD | 734 | 395 |
| not DD | 3,462 | 1,196 |

So in 395 of the 1,129 DD states, every r-edge of B₁ lies on the single old path C, and no interior chain is involved.

**Next lemma: the two-curve case [conjecture, to be formulated exactly].** Assume every r-edge of B₁ lies on C. The reconnection is then a pure **meander** of two curves with interleaved endpoints:
- B₁ runs from e_{j+1} to e_{j+3};
- C runs from e_{j+2} to e_{j+4};
- the data are the order in which C visits the k r-edges of B₁, and the side of each stub (fixed by the Heawood signs along B₁).

Two steps follow:
1. Classify when the shifted pairing joins e_{j+4} to e_{j+1}. This is a finite combinatorial question about meanders, so it is provable.
2. Then ask whether a DD meander forces, somewhere else in the class, a state from room_j. One route is through the swap of C itself, the {α,μ}/{A,B} chain through x_{j+2} and x_{j+4}, which keeps the link pattern.

This is the first place where a single, explicit planar object (one meander) controls DL→DL. Euler's formula for meanders (counting the regions between B₁ and C) is the natural way for quantitative χ = 2 to enter. It must fail on the torus, where B₁ and C need not cross.

**Decisive test.** At orders 16–24, restrict to the two-curve DD states. Record the meander permutation and the stub sides, and check whether DD is a function of the meander alone. It must be, by the reconnection model, so this tests the model. Then list the meanders that occur in DD versus non-DD states.
