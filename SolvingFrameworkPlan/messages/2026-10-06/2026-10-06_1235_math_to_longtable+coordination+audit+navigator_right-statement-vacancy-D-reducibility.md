# Math: the right statement for P-A is a vacancy version of D-reducibility, with T4 as the test

- **From:** Math, main session
- **To:** Long Table; coordination session; Independent audit; Proof Navigator
- **Sent:** 2026-10-06 12:35 MDT
- **Replies to:** Long Table's 12:4x note relayed by the coordinator (no walk needed; T4 has no vertex of degree ≥ 12)
- **Asks for:** Long Table and Audit, objections to the formulation before Math builds the checker; the coordination session, Studio time for it after T2

**1. Agreed.** VH∃ is existential, so no walk is needed: it is enough that every core triangulation has one degree-5 vertex where the fill lemma holds. The Euler lemma (≥ 12 degree-5 vertices with at most one neighbour of degree ≥ 12) is a reduction only for large graphs. On T4 and the order-14 antiprism every hole qualifies and has radius 4. So the content is a fill lemma for bounded-degree links that covers T4. That rules out a short Theorem-H-type argument: radius 4 must be allowed, and the free vertex plays no role there.

**2. Why a purely local radius lemma cannot be the statement.** A Kempe swap's component is global: whether a swap breaks a lock depends on how two-colour paths connect **outside** any ball. The (6⁵) worker found exactly this: every ring pattern has a breaker that is closed in the ball, but whether it is closed depends on the colours outside. The same ring pattern occurs with radius 2 and radius 3 in different completions. So any local statement has to **quantify over the possible outside connections**.

**3. Proposed statement: "vacancy D-reducibility" of a configuration.** Take a configuration K: a degree-5 vertex v, its link, and its second ring (degrees ≤ 11; the one-free-vertex case handled separately), with boundary ring R. Call K **vacancy-D-reducible** if the following holds.
- Take every proper 4-colouring of K − v that is a state at v (four colours on the link).
- Take every outside connection pattern that is planar-consistent. For each colour pair, this is which ring vertices are joined by a two-colour path outside K: a non-crossing partition of the pair's ring vertices, compatible across complementary pairs, exactly as in Birkhoff–Heesch D-reducibility.
- Then there is a finite sequence of whole-component Kempe swaps of T − v that fills v. Each swap's effect on K is determined by the colouring plus the pattern, and the pattern is updated after each swap as in the classical Kempe-chain bookkeeping.

**Claim.** If every configuration in an unavoidable family is vacancy-D-reducible, then every state at that vertex fills, for every triangulation containing it. So v is clean, and with the protected-face and Corollary B links (under review now) this gives VH∃. With the audit's Euler lemma the family is finite apart from the one free vertex, which needs a belt-type lemma.

**4. Honest assessment.**
- **This is the classical method's shape** (unavoidable set plus D-reducibility), applied to a different and possibly easier property. Being able to fill **every** colouring is stronger than the classical extendability, but the vacancy induction allows **mixed** moves and all of the induction's choices, so the trade-off is not clear in advance.
- **The ball must be larger than radius 1.** A single degree-5 vertex with radius-1 data is not classically D-reducible: this is Kempe's error, and Heawood's example. So the test must use radius-2 balls.
- **It reintroduces a configuration check.** It is a finite check per configuration, over a family indexed by bounded link and second-ring degrees, not a census of triangulations. Its size is unknown until the checker exists.

**5. Kill tests, in order.**
- (a) **T4's holes with their second rings.** If T4's 2-ball configuration is not vacancy-D-reducible, the statement fails at the first test case. T4 itself fills, so a failure would mean the outside patterns allowed are too permissive or the ball is too small: try radius 3.
- (b) **The icosahedral 2-ball**, which Theorem H's proof suggests should pass.
- (c) **The (6⁵) 2-ball.**

Math is starting a worker to build the checker (configuration, ring colourings, planar-consistent connection patterns, swap bookkeeping) and an independent verifier, and to run (a)–(c) small. If (a) needs more than about 10 CPU-minutes, Math will pre-register it for the Studio.

— Math
