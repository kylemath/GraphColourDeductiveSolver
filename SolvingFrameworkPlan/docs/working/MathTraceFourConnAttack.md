# Attack on the universal trace-game hypothesis and on four-connectivity of a least plain VH-exists failure

Math research worker, 5 October 2026. Hand work only. No census, no declared experiment, no plantri. One tiny Python check (icosahedron, §6). Nothing here is a status change.

**Verdict, stated first.** Neither (1) nor (2) is proved. I found no proof and no counterexample. What this page adds is (a) an exact reformulation of when a root and fan are good, in terms of the "repeat pair" of each stuck state, which makes the quantifier "one pair for every start" concrete; (b) a sharper relative target R+ for (2) that allows landings on separator vertices of type 4|4, with a sound lift; (c) an exact account of where each route breaks; (d) the one lemma I think would unlock progress. Every claim carries [hand], [computed], [cited] or [open].

Sources used: START-HERE.md; MathTriangleCarryResearch, MathFourConnectedResearch, MathTraceGameLiftReview, MathVHCoreAdvance, MathFixedHoleReview, MathHighDegreeLandingResearch; `interface/trace-game-reduction.md`; vh-exists.md (definitions only). I did not re-derive their accepted results.

---

## 1. Setting (as accepted)

(G, φ) with φ a triangle, an induced 4-cycle or an induced 5-cycle (face), vertices off φ of degree ≥ 5. For φ a triangle and G four-connected this is the core of VH_C. States: hole h off φ, proper 4-colouring of G − h. Moves: whole-component Kempe swaps (φ may be recoloured) and singleton slides to off-φ vertices. Filled: link of h uses ≤ 3 colours. The trace game adds admissible bridge bits for 4- and 5-faces; I treat the triangle case fully and say where bits change things.

---

## 2. New exact reformulation: good pair = common repeat vertex

Let v be an off-φ vertex of degree 5 with link x0,…,x4 (cyclic). In an unfilled state all four colours occur on the link, so exactly one colour is repeated, on a nonadjacent pair {xj, xj+2}. Call it the **repeat pair** of the state. There are five possible repeat pairs; they are the five edges of the pentagram on x0..x4 (a 5-cycle: pairs {j,j+2}).

**[hand] Lemma 2.1 (fan admission).** The fan with apex xi (chords xi–xi+2, xi–xi+3) admits exactly those colourings whose link has xi as a singleton colour, i.e. xi ∉ repeat pair. (This is the accepted apex-singleton classification; I only restate it in terms of the pair.) So a state with repeat pair {xj, xj+2} is admitted by exactly three fans: those at the other three vertices.

**[hand] Proposition 2.2 (criterion).** Assume the four-connected core, where all five fans are legal at every degree-5 vertex. Let 𝒯(v) be the set of repeat pairs of *targetless* states at v (states whose permitted move component contains no filled state). Then the fan with apex xi is good at v **iff** xi lies in every pair of 𝒯(v). Hence:
- v has a good fan iff all pairs of 𝒯(v) share a common vertex (𝒯(v) empty counts as good);
- v has no good fan iff 𝒯(v) contains two **disjoint** pentagram edges. Indeed, a family of edges of a 5-cycle with no common vertex must contain two disjoint edges (three pairwise-intersecting edges would form a triangle, and the pentagram is a 5-cycle). Pairs disjoint from {x0,x2} are {x1,x3} and {x1,x4}.

This is the same as Math's hitting formulation (FourConnected §5) but exposes that *two* targetless states suffice to ruin a vertex, not a covering of all five fans by many states.

Consequence [hand]. VH_C fails in the core iff at every degree-5 vertex v off φ (at least 7 of them, order ≥ 12) there are two targetless states at v with disjoint repeat pairs. This is a very rigid, almost "paired" condition; it does not need a component to be large, only to hit two specific link patterns at every root.

This is not a proof of anything; it is the form in which the two obstructions below are best stated.

---

## 3. What a failure of (1) looks like, exactly

Let C be a targetless component, S its hole projection. Accepted: S is off φ, connected, closed under off-φ neighbours of every degree-5 member (mobility), has ≥ 3 projected neighbours at each degree-5 member, contains a cycle if all holes have degree 5, and (core) the order is ≥ 12.

**[hand] Observation 3.1 (what a targetless degree-5 state must look like).** Take an unfilled state at v with link colours (α, β, α, γ, δ) at (x0..x4), repeat pair {x0,x2}. The only single swaps that could remove a colour are changes of the singleton vertices:
- x1 (colour β) is nonadjacent to x3, x4. It becomes γ or δ iff the {β,γ}-component of x1 misses x3, or the {β,δ}-component of x1 misses x4. So targetless requires **both locks**: a {β,γ}-path x1–x3 and a {β,δ}-path x1–x4 in T − v.
- x3 (γ) is nonadjacent to x0,x1; x0 is α and the neighbour x2 (α) would be dragged into the swap, so only x3 → β is a possible elimination, and it is the same lock as x1–x3. Likewise x4 → β is the same lock as x1–x4.
- changing x0 or x2 alone never removes a colour (α stays on the other).
So the stuck states are exactly those with both locks; this is just the Kempe double-lock picture [hand, standard].

**[hand] Observation 3.2 (planar consequence, same-state).** Close the first path through v: the Jordan curve (v, x1, …, x3, v) separates x2 from {x4, x0}; the second (v, x1, …, x4, v) separates x0 from {x2, x3}. The paths use colours β, γ, δ only, so the α-vertices x0 and x2 lie in different components of any bichromatic graph in colours {α, κ} (κ ≠ β, δ gives κ = γ). Hence the {α,γ}-component of x2 (which contains x3, adjacent) misses x0, and swapping it yields link (α, β, γ, α, δ): a new unfilled state at v with repeat pair {x0, x3}. So from a targetless state with repeat pair {0,2} a single swap reaches a state with repeat pair {0,3}, which shares x0. Likewise the symmetric swap on the other side.

Observation 3.2 shows that repeat pairs at the same hole within one targetless component move along pentagram edges that share a vertex ({x0,x2} to {x0,x3}). It does not by itself produce two disjoint pairs ({x1,x3} or {x1,x4} are two steps away), and it does not forbid them. So a 'pairs are confined' argument cannot be local at v: single swaps in the stuck state tend to rotate the pair. This is a candid dead end for showing each component has a common repeat vertex.

**What would be needed for (1)** (face a triangle, four-connected core): show the move graph has a targetless component only if at some v, 𝒯(v) is contained in the star of one vertex. Mobility only says S is large and closed; it does not control repeat pairs. I could not bound 𝒯(v).

**Why the existing finite evidence does not transfer.** The 435 + 4004 + 2002 members are orders ≤ 18, and a targetless component simply does not appear in them (not "has common repeat vertex": it is empty). The icosahedron check below (§6) is of the same kind. The universal statement needs an argument that targetless components do not exist or are confined, and neither mobility nor the lock structure above prohibits a branching all-degree-5 projection.

**Where the trace game (faces of length 4, 5) differs [hand].** The same criterion holds with 'targetless' meaning targetless in the position space (state, admissible bit assignment). The bits only enlarge the adversary's options. The accepted lifts say a win for (A, Q) lifts to (G, φ), so a least failure has no separating 3-, 4-, or 5-cycle with ≥ 2 interior vertices on each side; that is cyclic 5-connectivity of the least failure, nothing about the move dynamics.

**[hand] Small remark, pentagon and quadrilateral members have many interior vertices.** For a chordless face of length b with k interior vertices, the interior edge count is 3k+b−3 and the interior degree sum is that plus m, where m ≤ 3k−6 is the number of interior–interior edges. Requiring all interior degrees ≥ 5 gives k ≥ 9−b (k ≥ 4 for b=5, k ≥ 5 for b=4, k ≥ 6 for b=3). At equality the interior graph is maximal planar, but then some interior vertex lies strictly inside the interior graph's outer face and has degree ≤ its interior degree, which is 3 for the smallest cases (K4 for b=5, bipyramid for b=4): contradiction. So k ≥ 5 for b = 5 and k ≥ 6 for b = 4; the data show orders 11–17 for G, i.e. larger k in fact. Consequently the hypothesis "≥ 2 interior vertices" in the 5-face extension excludes only the 5-wheel (k = 1), since k = 2,3,4 do not occur. [hand, elementary; not needed elsewhere.]

---

## 4. (2): four-connectivity of a least plain VH-exists failure

Known and accepted: in any failure, every vertex of every separating triangle has degree ≥ 6 (fixed-hole theorem); a least failure of VH_C is four-connected; there is no interior witness; the innermost completed side A of a separating triangle F is four-connected, has interior degrees ≥ 5, F-vertices of degree ≥ 4 in A, and ≥ 6 interior degree-5 vertices.

### 4.1 New relative target R+, with a sound lift

Math's target R asks for an F-good pair in (A, F): every hole stays off F. Using Math's balanced degree-six theorem, this can be relaxed.

Call f ∈ F **landable** (relative to T) if deg_T(f) = 6 and d_A(f) = d_B(f) = 4.

**[hand] Target R+.** In A there are a degree-5 root r off F and a legal fan such that for every admitted start there is a filling path whose holes lie off F except that the *last* hole may be a landable vertex f ∈ F, reached by a slide from an off-F vertex.

**[hand] Lemma 4.1 (soundness).** R+ for the innermost completion A of a separating triangle F of T lifts to (r, fan) being a good pair of T.
*Proof.* All holes before the landing are strictly interior to A with unchanged T-neighbourhoods, so every step lifts (accepted interior-path lift). The landing slide's source is interior, so the singleton condition is the same in T. At f the global degree is 6 with 4|4 split; MathHighDegreeLanding §2 fills the fixed hole in ≤ 3 swaps for every proper colouring of T − f, all components avoiding the two other separator vertices. The fan is legal in T because a chord absent in A between two vertices of A would have to be an edge through B between vertices of F, which are already adjacent in A; and r's link vertices not on F are interior. ∎

R+ weakens R only by landable vertices; it is unconditional on the type of f only through facts about T not visible in A (d_B(f)). So the right relative class for the induction labels each F-vertex of A with deg_A(f) and a flag.

I could not prove R+ either. It helps only when a stuck path would naturally exit through a type-4|4 vertex; which of those occur depends on B, which the induction does not see.

### 4.2 Routes that I tried, and exactly where each breaks

**Route A (minimality applied to A directly).** If every f has d_A(f) ≥ 5, A is itself a min-degree-5 triangulation, smaller than T, so it has a good pair for plain VH∃ by minimality. Breaks: the path may put the hole on F (a vertex of global degree ≥ 6, with d_A(f) = 5 and d_B ≥ 3), and the lift needs a fixed-hole fill at global degree ≥ 6 with a side degree split not 4|4; this is MathHighDegree §3/§3a only conditionally (needs a pure fill in B). No argument controls where plain good paths go. This is the same obstruction as "no interior witness", seen from the inside.

**Route B (replace B by a smaller cap C).** T' = A ∪ C with C a disc bounded by F with interior degrees ≥ 5 and d_A(f)+d_C(f)−2 ≥ 5. For d_A(f) = 4 we need d_C(f) ≥ 3, but d_C(f) = 3 at all three vertices forces C to be the single stacked vertex of degree 3, not allowed [hand: the face on edge pq opposite A has a third vertex w adjacent to both, so w is the unique C-neighbour of p and q, hence of all three, giving a degree-3 interior vertex]. With all d_C(f) ≥ 4 the curvature identity n5 = 6 + Σ(d_C(f)−4) + Σ_H(d−6) gives ≥ 6 interior vertices, and the core bound (order ≥ 12 for four-connected members of the relative class) gives ≥ 9 if C is itself four-connected. So replacement shrinks T only when B has more than ~9 interior vertices, and then the good pair of T' may lie in C or use F: breaks at the same place as Route A. [hand for the cap statements; the "~9" uses Math's accepted order bound.]

**Route C (use both sides).** Choose A innermost and B arbitrary. Every separator vertex is degree ≥ 6 so d_A(f) + d_B(f) ≥ 8. If some d_A(f) = 4 then d_B(f) ≥ 4 and the transfer theorem (3a) reduces landing at f to a pure fill in B; if d_A(f) ≥ 5 then d_B(f) ≥ 3 and (3) gives κ_T ≤ κ_B + 1 only for d_B = 3. Neither gives a fixed bound, because fixed-hole pure fill of a degree ≥ 5 hole is not available (it is the old Kempe problem). Breaks at: degree-5-or-more landing needs a fixed-hole theorem Math has only for degree 5 on a separating triangle and balanced degree 6.

**Route D (choose F cleverly).** Among all separating triangles take F with innermost A and with the number of landable vertices maximal. Breaks: no relation is known between landability and good paths; also failure of any f to be landable gives no interior witness for the class.

### 4.3 Exact obstruction, in one sentence

The induction class "min degree ≥ 5" is not closed under taking a side of a separating triangle (boundary vertices drop to 4), and the stronger classes in which it is closed (VH_C, VH^tr) require paths to avoid the interface, which is exactly the property that plain good pairs do not provide. The gap is therefore the same as (1): four-connectivity of a least plain failure is equivalent in effect to an F-avoiding or F-landable good pair on the side, i.e. to R or R+, which are four-connected-case statements about the very dynamics that are open.

---

## 5. The next lemma that would unlock progress

I think one lemma would decide (1) in the triangle-face core and by Route A/R+ most of (2):

**[open] Lemma ★ (pentagram confinement).** In the four-connected core with protected triangle φ, there is an off-φ degree-5 vertex v such that all targetless states at v have repeat pairs sharing one link vertex.

Equivalent (Prop. 2.2) to the existence of a good pair. Partial attacks that are consistent with the accepted pieces:
1. Show a targetless component's hole projection contains a degree-5 vertex v, all of whose neighbours' repeat pairs are *pinned* by the two locks of Observation 3.1 (the two lock paths together with φ and the fan structure constrain 𝒯 at the neighbours). Concretely, relate the repeat pairs at adjacent degree-5 holes under a slide; I could not get a relation because the colours of the two non-link neighbours of the new hole are unconstrained by the old state.
2. Find an *invariant* of the pair (v, state) that a Kempe swap in a component missing the link cannot change but that distinguishes {0,2} from {1,3}, for example orientation of the lock paths relative to φ (a Jordan side). Observation 3.2 shows swaps rotate the pair along pentagram edges; the invariant would have to be a winding or parity of the lock paths around φ. If the two lock paths necessarily separate v from φ in a specified pattern, then pairs on the φ side could be forced to share a vertex. This is the one geometric idea not yet used (φ appears in the accepted arguments only through slide prohibition).
3. A weaker, finite and checkable statement that would be a *sound guide* for a Lean/hand attack: for every four-connected core member of order ≤ 18, some off-φ degree-5 v has 𝒯(v) empty (stronger) or common. This is a census, so it is not run here and not permitted without a declaration.

For (2) the corresponding lemma is **R+** (or R) on the innermost side; Lemma ★ with φ = F handles R (all holes off F) only where the targetless components are absent or confined, and R+ adds the landable exits. A proof of ★ for triangle φ would give R and hence VH∃ outright by Math's reduction; so (2) would become unnecessary rather than separately needed.

---

## 6. Finite sanity check [computed, not evidence for any universal claim]

Script in the scratchpad (not committed): icosahedron (12 vertices, all degree 5), protected face {0,1,2}, hole off the face, all proper 4-colourings of T − h up to colour renaming and all hole positions off φ. Moves: whole-component swaps and slides to off-φ vertices. Result: 180 canonical states, 1 connected move component, 0 targetless components. So the move graph is connected and every state reaches a fill; 𝒯(v) = ∅ for every v. This agrees with the 435/4004/2002 exploratory readings and with Prop. 2.2 (empty 𝒯 is good). It says nothing about orders where branching traps could appear.

---

## 7. Dead ends, plainly

- Singleton counting and mobility cannot exclude a branching all-degree-5 targetless component (Math's own conclusion; I did not improve it).
- Observation 3.2 shows repeat pairs rotate along pentagram edges under single swaps in the stuck state itself, so a "pairs are confined" argument cannot be local at v; it needs a non-local invariant (idea 2 in §5), which I did not find.
- No reduction of VH∃ or of (2) to a smaller minimum-degree-5 triangulation preserves the protected property; the cap computation shows reduction by capping costs ≥ 9 vertices and the pair may enter the cap.
- The balanced-6 theorem gives a legitimate extra exit (R+), but the exit type depends on B, which the induction cannot see; so R+ cannot be made a clean closed class without labelling data from B.
- I made no attempt to prove the trace game for faces of length 4, 5 beyond the lift statements; the same targetless criterion holds with bits, but bits only enlarge the adversary, so any proof for the triangle case must be repeated with the bit dynamics, which are themselves frozen-pair constrained and appear no easier.
- I did not find any contradiction with an existing accepted statement; nothing here corrects another team's page.

## 8. Claim ledger

- Prop. 2.2 (criterion), Obs. 3.1, Obs. 3.2, Lemma 4.1, cap statements in 4.2, the k-bound remark: [hand]. Lemma 2.1 restates an accepted lemma.
- Icosahedron count: [computed], tiny, no universal content.
- Lemma ★, R, R+, (1), (2): [open].
