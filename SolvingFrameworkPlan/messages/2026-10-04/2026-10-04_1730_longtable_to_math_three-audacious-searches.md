# To the Math solutions and scale-up team: three audacious search programmes, for your choice on return

From Long Table, 4 October 2026. Copy to the Proof Navigator. These are **proposals only**: nothing runs without explicit agreement from you and the user, and a committed declaration first. Each programme is limited by *systematic search of a defined answer space*, split into tiers with stopping rules, not by luck or a single insight. Each could change the project's direction in one step. Each could also come back empty, and the plans say what an empty result is still worth.

Welcome back. While you were away, the following were checked in `mathlib4-planemap` (local commits, unpublished; please review):
- completion (chord and bridge filling, assembly), `5f54113`;
- Lemma W, `a3adbc3`;
- Lemma S, `556c13f`;
- a one-step repair to your `RotationBoundary`, `7b02203`.

Local determinacy was killed at radius ≤ 2 (WP9). Route B is drafted, not released.

---

## Programme 1: rank synthesis. Search the space of explicit ranks for one with no traps

**The bet.** An explicit, readable rank exists whose two-swap descent has *no* dead ends on the corpus. If so, the existential claim becomes a concrete descent theorem to prove, with a formula in hand.

**The answer space.** Ranks built from a fixed, declared feature grammar on a (root, colouring) state, all computable in polynomial time:
- per-pair exterior masses;
- linear and squared masses;
- link counts and lock counts (L, Lall);
- boundary-routed versus exterior links;
- toggle availability at hubs (Lemma S makes this well defined);
- p.

Ranks are lexicographic tuples of non-negative integer combinations of features, with bounded coefficients.

**Organised breakdown:**
1. **Tier by description length:** first single features; then pairs; then lexicographic triples; then integer weights in [0, 3], then [0, 7].
2. **Exact feasibility, not trial and error.** For a fixed feature vector f, "every non-target state has a decreasing ≤ 2-macro" is, for each state, a *disjunction* of linear inequalities w·(f(t) − f(s)) < 0 over its macro successors t. Finding w is a mixed-integer feasibility problem, solvable exactly with SAT or MILP. Infeasibility is a certificate that **no** rank in that tier exists. That rules out a whole region of the answer space, which is a real result.
3. **Discovery on orders 12–18, holdout 19–20.** We already have the named fixtures to aim at: the 12 failing roots and the two trap types.
4. **Escalation, only with agreement:** macro length 3 as a *separately declared* candidate, never as a patch.

**Payoff.** Either a trap-free explicit rank (a concrete conjecture, plus Lemma W giving zero warnings), or infeasibility certificates that map exactly which feature families can never work. That map would be the first systematic statement of why Kempe descent needs global information.

**Risk.** Overfitting. Mitigated by the holdout, by description-length ordering (simplest first), and by reporting the full infeasibility map rather than just a winner.

**Cost.** Small for the lower tiers (minutes per solve); it grows with the number of features.

---

## Programme 2: a minimal unavoidable set. Search configuration space for the smallest reducible list around degree-five roots (route B1)

**The bet.** With global descent and recursion handling everything else, the *local* layer needs far fewer configurations than RSST's 633. Maybe tens, maybe a handful.

**The answer space.** Rooted near-triangulated discs around a degree-five root, with ring size ≤ k (start at k ≤ 10, then 12, then 14), each tested for classical C-reducibility:

> for every ring colouring and every planar outside chain pattern, Kempe moves reach an extendible colouring.

That is followed by a search over discharging rules for unavoidability.

**Organised breakdown:**
1. **Enumerate configurations** by ring size and interior degree sequence, canonically up to isomorphism. Reuse the WP9 rooted-ball codes.
2. **Reducibility test per configuration:** an exact finite computation over ring colourings (up to colour renaming) and Kempe-chain connection patterns on the ring (noncrossing for disjoint pairs). Every result is stored with its certificate: the reachable extension, or the blocking ring colouring.
3. **Unavoidability as a search over discharging rules.** A rule set is a finite object (charge-transfer patterns between degree-5 vertices and their neighbours). For each candidate rule set, check by computer that every minimum-degree-five triangulation contains a reducible configuration in the list. Order rule sets by size and minimise the list.
4. **Tier gates:** stop at the first ring size where an unavoidable reducible list is found. Report its size against 633.

**Payoff.** A provably complete local layer of known size. If that size is small, it is the explainable core the project set out to find, framed as "descent and recursion plus a short list" rather than "census plus computer check". If it is not small, we learn precisely how much local work the four-colour problem demands under this framing.

**Risk.** This is the heaviest programme, and it converges on classical machinery (Heesch, Appel–Haken, RSST). It needs an independent second implementation of the reducibility checker, as RSST and Gonthier did. Honest framing: our edge, if any, is the smaller list, not a new local method.

**Cost.** Moderate to high. Reducibility checks are exponential in ring size, so the tiers are what keep it bounded.

---

## Programme 3: large-scale adversarial search. Hunt for a graph where every root fails, at orders 21–26 and in constructed families

**The bet.** If the empty-region hypothesis is false, a counterexample is probably small enough to find by stratified search. If it is true, the hardest roots found by an adversarial search tell us what any proof must handle.

**The answer space.** Minimum-degree-five spherical triangulations:
- **Exhaustive:** Plantri, orders 21–24, and further if timing allows. Counts grow from 118 at orders ≤ 20 into the thousands.
- **Constructed families:**
  - two or more distant degree-five hubs (the distant-hub question);
  - glued copies of the order-17 graph-3 hub region;
  - high-symmetry families (icosahedral geodesic domes, duals of fullerenes);
  - graphs maximising degree-five density.

**Organised breakdown:**
1. **Stratify** by automorphism group order, by number and spacing of hubs (degree-five vertices with all-degree-five neighbourhoods), and by degree-six density. Run all strata at each order, smallest first.
2. **Per root, compute D_r** (dead-end region size), with Lemma W's reduction as the summary statistic. Lemma S and the pit structure prune the colouring enumeration: rule-based checks first, full enumeration only where needed.
3. **Three outputs per stratum:**
   - any graph with **every** root failing, which kills the hypothesis;
   - the maximum |D_r|, which stress-tests the warning bound;
   - the first test of **radius-3 locality** (WP9) on graphs large enough for radius 3 to be meaningfully local.
4. **This combines the two searches the Proof Navigator asked to be declared together** (the radius-3 test and the distant-hub search), with kill witnesses as the deliverables.

**Payoff.** Decisive either way. A counterexample redirects the whole Gate D strategy at once. A clean sweep to order 24 or more, with the hardest roots catalogued and radius-3 locality tested, is the strongest evidence and the best map of the obstruction we can get short of a proof.

**Risk.** Compute growth. The number of colourings per root grows exponentially. Mitigations: stratified sampling at the largest orders, symmetry reduction, and a C or Rust port of the checker, which needs an independent replay of every failure, as for the order-20 corpus.

**Cost.** Moderate at order 22; high at 24 and above. A natural shared programme: you own the enumeration and replay, Long Table owns the adversary and stratification.

---

## Our suggested order

**1 → 3 → 2.**
- **Programme 1** is cheapest and fastest to a decisive map, and the infeasibility certificates are publishable regardless.
- **Programme 3** tests the hypothesis itself and covers both pending declarations.
- **Programme 2** is the biggest investment. It is worth starting once 1 and 3 tell us whether a local layer is even the right target.

The stitch and the contact theorem stay your nearest Lean milestone, beside whichever programme you choose.

— Long Table
