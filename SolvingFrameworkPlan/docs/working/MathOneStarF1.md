# One-star class F1 = (p,5,5,6,5): pattern automaton, silent kills, and the exact obstruction

Math research worker, 6 October 2026. **Hand work only** (battery rule): no code, script or build was run; files were only read. Labels: [hand] derived here, unchecked by a second reader or machine; [cited] from a reviewed note; [guidance] machine output from another team, used only for orientation; [open]. No other file was edited; nothing was committed.

Inputs read: MathRstar55566.md + review (Lemma G, confinement), MathHighDegreeNeighbour.md + review (HP Lemma 1–3, starvation, Jordan), MathRstar55656.md (Lemma SS, with Math's corrected hypothesis K_u ∩ N(t) = {u}), MathTwoSixNeighbours.md (F-E1′/B-E1″, recipe), pd2_lock_proof.md (Tait lock criterion and its corollary), MathConfinementAttack.md (Theorem A), MathRstarUnavoidable.md (where F1 comes from).

## Verdict, first

1. **No radius bound is proved for F1.** [open] What is proved [hand] is a complete reduction to one exactly stated obstruction (§6).
2. **[hand] Pattern automaton (§2–§3).** In the five frame positions there are **40 ring patterns**; **16 die by one move** (radius ≤ 2) and **24 survive**. The F-graph on the 24 survivors is a **deterministic 10-cycle Γ** (no leak choice at all) plus a **14-state set Γ′** with two binary branches. The confined swap G links them (N0 ↔ N2), as do silent swaps. B = F⁻¹, so Γ ∪ Γ′ is closed under F, B, G and all confined AB (there is none). [guidance] 24 equals the number of states the vacancy-D game loses here; I could not check that the two lists coincide (Studio item 1, §8).
3. **[hand] New kill family "silent-then-kill" (Lemma SK, §4).** It swaps a two-colour component of a ring vertex that avoids the link (so the link and frame are unchanged), and the new ring pattern is one of the 16 one-move kills or violates E1–E3. This contains Lemma SS (corrected) and AB\*. **Every state of Γ ∪ Γ′ has at least one SK kill** that the adversary must block by a *leak* (a Kempe connection to a link component). Tables in §5.
4. **[hand] Lemma P (lock-leak propagation).** "w2 lies in the lock-2 component of s" is the same statement as "w4 lies in the lock-1 component of F(s)". On Γ it identifies the leaks in four pairs. So one turn of Γ needs **15 independent leaks**: five AB\* leaks (at the R3 states), six G-component leaks (at R1 states), and four lock leaks.
5. **[hand] Partial bound.** r(s) ≤ 3 + d_L(s). Here d_L(s) is the F/B-distance from s (within Γ ∪ Γ′) to the nearest state at which some listed leak is absent, or at which a branch constraint (R1a, R1g, B0a, B0d) fails. All 16 killed patterns have r ≤ 2.
6. **[hand] Exact obstruction.** A targetless Kempe class at an F1 hole consists only of DL states with patterns in Γ ∪ Γ′, and every leak of §5 holds at every one of its states. Its F/B orbits are cycles whose pattern period is 10. One turn of Γ permutes the three non-repeated colours cyclically on the 2-ball.
7. **Diamond-freeness is not used anywhere** and does not help locally. It forces only deg u1 ≥ 6 and p ≥ 6, and no step reads a ring degree. (p = 5 is the class (5,5,5,6,5) of Theorem HP.)
8. **KILLED (§7):** G-F and G-B (p is unreadable where G is confined); confined AB (never occurs); single-state planarity contradictions at P1, O0 and R1g (none exist with these tools); the "Γ′ is impossible" idea (its non-connection constraints are consistent at one state).

## 1. Frame [hand / cited]

- **Link.** y0 = p (any degree), y1, y2 of degree 5, y3 of degree 6, y4 of degree 5, in rotation order. The mirror orientation (p,5,6,5,5) is the same class read in the reflected plane, and every argument is orientation-free. u_t is the common neighbour of y_t and y_{t+1} other than v. z is the middle outer neighbour of y3. A degree-5 y_t has neighbours exactly v, y_{t±1}, u_{t−1}, u_t, so the ring edges u0u1, u1u2, u3u4, u2z and zu3 exist. Nothing is read about p's other neighbours or about any ring degree. No separating triangle is assumed: it gives a chordless link, and coincidences can only add equalities, as in the HP review.
- **DL frame.** Link (a,b,a,g,d) on x0..x4. Lock 1 is a {b,g}-path x1~x3; lock 2 is a {b,d}-path x1~x4 [cited]. **k** = frame position of p. The 6 then sits at k+3, and the 5s sit at k+1, k+2 and k+4.

| k | repeat pair (middle) | x0..x4 | w0..w4 | m (middle of the 6) |
|---|---|---|---|---|
| 0 | {y0,y2} (y1) | y0 y1 y2 y3 y4 | u0 u1 u2 u3 u4 | m3 = z |
| 1 | {y4,y1} (y0 = p) | y4 y0 y1 y2 y3 | u4 u0 u1 u2 u3 | m4 = z |
| 2 | {y3,y0} (y4) | y3 y4 y0 y1 y2 | u3 u4 u0 u1 u2 | m0 = z |
| 3 | {y2,y4} (y3) | y2 y3 y4 y0 y1 | u2 u3 u4 u0 u1 | m1 = z |
| 4 | {y1,y3} (y2) | y1 y2 y3 y4 y0 | u1 u2 u3 u4 u0 | m2 = z |

- **Moves.** F swaps the {a,g}-component K_F of x2 (k → k+2). B swaps the {a,d}-component K_B of x0 (k → k+3). G swaps the {g,d}-component of x3. Jordan facts: x0 ∉ K_F and x2 ∉ K_B [cited].
- **One-move kills** [cited]: F-starvation, B-starvation, F-E1′, B-E1″, unlock, and Lemma SS with K_u ∩ N(t) = {u}.
- **Endpoint conditions.** E1: x1 has outer g and d. E2: x3 has outer b. E3: x4 has outer b. Each is read only where the vertex has bounded degree.
- **Pattern notation.** w0w1w2w3w4 followed by (m).

## 2. Pattern tables [hand]

Allowed colours: w0, w1 ∈ {g,d}; w2 ∈ {b,d}; w3 ∈ {a,b}; w4 ∈ {b,g}. The middle vertex m_t avoids c(x_t) and its two ring neighbours.

| k | all patterns | killed (rule) | survivors (name) |
|---|---|---|---|
| 0 | gdbab(d), gdbbg(a), gdbbg(d), dgbab(d), dgbbg(a), dgbbg(d), dgdab(b), dgdbg(a) | dgbab, dgbbg(a/d): F-starv | **A0** gdbab(d), **B0a** gdbbg(a), **B0d** gdbbg(d), **C0** dgdab(b), **D0** dgdbg(a) |
| 1 | {g,d}²·bab(g) (4), dgbag(b), ddbag(b), ggdbb(a/g), dgdbb(a/g), dgdbg(a) | ddbab, dgbab, dgdbb(a/g): B-starv; ggbab, dgbag: F-starv | **P1** gdbab(g), **Q1** ddbag(b), **R1a** ggdbb(a), **R1g** ggdbb(g), **T1** dgdbg(a) |
| 2 | gdbab(d), gddbg(b/d), dgbab(g), dgdbg(b) | none (x0 has degree 6 and a g-neighbour; x2 = p) | **N0** gdbab(d), **N1b**, **N1d** gddbg, **N2** dgbab(g), **N3** dgdbg(b) |
| 3 | gdbab(a), dgbab(a), dgbbg(a), dgdab(a), dgdbg(a), ggbab(d), ggdab(d), ddbab(g), ddbbg(g) | dgbab, dgdab, ddbab: B-starv; dgbbg, ggbab: F-starv | **O0** gdbab(a), **O1** dgdbg(a), **O2** ggdab(d), **O3** ddbbg(g) |
| 4 | gdbab(g), gddbb(b/g), dgbab(d), dgbag(d), dgdbb(b), dgdbg(b) | dgbab, dgdbb: B-starv | **L0** gdbab(g), **L1b**, **L1g** gddbb, **L2** dgbag(d), **L3** dgdbg(b) |

**Totals: 40 patterns, 16 killed, 24 survive.**

Notes on the table:
- Where E1–E3 are readable, they are imposed.
- F-E1′ / B-E1″ can fire only at k = 1 (x4 = y3) and k = 0 (x3 = y3), as branch conditions (§3).
- **Confined AB never occurs.** The triple contains p at k = 0, 1, 2. At k = 3 it needs w2 = d, w4 = g and m1 ∈ {g,d}, which no pattern has. At k = 4 it needs w4 = g, w2 = d and m2 ≠ b, which no pattern has.
- **Confined G** (K_G = {x3, x4}) occurs only at k = 2, in N0 and N2. G maps each to the other.

Sample derivation, k = 3 (x0 = y2, x2 = y4 and x4 = y1 have degree 5; x1 = y3 has degree 6; x3 = p):
- E1 at the 6 gives (w0, m1, w1) ∈ {(g,a,d), (d,a,g), (g,d,g), (d,g,d)}.
- E3 gives (w3, w4) ∈ {(a,b), (b,g)}.
- The ring edges are w4w0 (at x0), w1w2 (at x2) and w3w4 (at x4).
- This gives 1 + 4 + 2 + 2 = 9 patterns.

## 3. F-transitions [hand]

Recipe (MathTwoSix §2):
- An a/g ring vertex is **in** K_F if it is adjacent to x2 or x3, or to a vertex already in. It is **out** if it is adjacent to x0 or to a vertex already out.
- If p = x0, the g-neighbours of p are out. If p ∈ {x2, x3}, its g-neighbours are in.
- Read the image in the frame w′_t = w_{t+3}, m′_t = m_{t+3}, with roles a→a, d→b, b→g, g→d.

| k | transitions |
|---|---|
| 0 | A0→N3, B0a→N1d, B0d→N1b, C0→N2, D0→N0 |
| 2 | N0→L3, N1b→L1g, N1d→L1b, N2→L2, N3→L0 |
| 4 | L0→T1, L1b→R1g, L1g→R1a, L2→Q1, L3→P1 |
| 1 | P1→O1, Q1→O3, T1→O0. **R1a→O2 only if m4 ∈ K_F** (else F-E1′ kills). **R1g→O2 only if m4 ∉ K_F** (else F-E1′ kills). |
| 3 | O0→D0, O1→A0, O2→C0. **O3→B0d if m1 ∉ K_F; O3→B0a if m1 ∈ K_F.** |

The F-graph splits into two cycles:
- **Γ (deterministic):** A0 → N3 → L0 → T1 → O0 → D0 → N0 → L3 → P1 → O1 → A0. Its states alternate between R1 type (gdbab: A0, L0, O0, N0, P1) and R3 type (dgdbg: N3, T1, D0, L3, O1), as in HP and in Γ₁ of (5,5,6,5,6).
- **Γ′:** C0 → N2 → L2 → Q1 → O3 → {B0d → N1b → L1g → R1a, B0a → N1d → L1b → R1g} → O2 → C0.

**Absolute check of Γ** [hand]. I recomputed every step of Γ with actual colours A, B, G, D, where A is the invariant repeated colour.
- Start at A0 = (y0..y4; u0..u4; z) = (A,B,A,G,D; G,D,B,A,B; D).
- The ten F-swaps are {A,G}, {A,B}, {A,D}, {A,G}, {A,B}, {A,D}, {A,G}, {A,B}, {A,D}, {A,G}.
- After one turn the 2-ball reads (A,D,A,B,G; B,G,D,A,D; G). That is the start with B→D→G→B applied: **one turn of Γ permutes the three non-repeated colours cyclically on the ball.**

## 4. Lemma SK (silent then kill) [hand]

**Lemma SK.** Let s be DL. Let r be a ring vertex and c′ ≠ c(r), and let K be the {c(r), c′}-component of r in T − v. Suppose K contains **no link vertex**. Swapping K gives s′ with the same link colours and the same frame. If the ring vertices named in the kill condition, at their post-swap colours, satisfy one of the following, then r(s) ≤ 3:
- (i) a starvation rule (F-starv or B-starv at a degree-5 or degree-6 endpoint); or
- (ii) a violated endpoint condition E1, E2 or E3 at a bounded-degree endpoint.

*Proof.*
- K avoids the link, so the swap is one Kempe move and leaves the link and frame unchanged.
- Case (ii): s′ is not DL, so the unlock fills it. Total ≤ 2.
- Case (i): F(s′) or B(s′) is not DL, then unlock. Total ≤ 3.
- **Robustness.** K may contain further ring vertices of colours c(r) or c′, joined through the outside. Every kill used below reads only (a) vertices certainly in K, whose new colours are known, and (b) vertices whose colours lie outside {c(r), c′}. So the outcome does not depend on what else K contains. The one exception is O0, where two outcomes exist, and both kill (§5). ∎

Lemma SS (corrected) is the special case where the kill is "t has no c-neighbour". AB\* is the case c′ = a at w3.

A **leak** is the negation of the hypothesis "K contains no link vertex": r is Kempe-joined, in colours {c(r), c′}, to a link component.

**Lemma P (lock-leak propagation).** The following are equivalent:
- "w2 ∈ lock-2 component of s" (a {b,d}-statement);
- "w4′ ∈ lock-1 component of F(s)".

*Proof.* w′4 = w2. F does not touch b/d vertices, so the {b,d}-subgraph is unchanged, and lock 2 of s is lock 1 of F(s) (pd2 corollary). ∎

## 5. Leak tables [hand]

For each state I list every ring vertex r and every partner colour c′.
- A pair is **blocked** when it is locally joined to the link; this needs no leak.
- A pair is **neutral** when the silent swap gives another survivor.
- Otherwise it is an SK kill, and the table gives the leak that blocks it.

### 5.1 Γ

| state | leak needed (frame names) | blocked kill |
|---|---|---|
| A0 (k0) | λA1: w4 ∈ lock-1 comp | SS(x4,b): E3 |
| | λA2: {w0,w1} ∈ G-comp ({g,d} of x3x4) | w1→g, F-starv at x2 |
| N3 (k2) | λN: w3 ∈ AB-comp of the triple (AB\*) | E2 |
| | (neutral: {w0,w1} in {g,d} gives N1b) | — |
| L0 (k4) | λL1: {w0,w1,m2} ∈ G-comp | w0→d, B-starv |
| | λL2: w2 ∈ lock-2 comp | E2 |
| T1 (k1) | λT1: {w3,m4} ∈ AB-comp (AB\*) | E2 |
| | λT2: w4 ∈ lock-1 comp | B-starv |
| O0 (k3) | λO1: w0 ∈ G-comp; λO2: w1 ∈ G-comp | E1 at the 6, or B-starv if w0, w1 flip together |
| D0 (k0) | λD1: w2 ∈ lock-2 comp | w2→b, F-starv |
| | λD2: {m3,w3} ∈ AB-comp (AB\*) | E3 |
| N0 (k2) | λM1: w2 ∈ lock-2 comp | E2 |
| | λM2: w4 ∈ lock-1 comp | E3 |
| | (neutral: {w0,w1,m0} in {g,d} gives N2; G gives N2) | — |
| L3 (k4) | λK1: w3 ∈ AB-comp (AB\*) | E2 |
| | λK2: w4 ∈ lock-1 comp | B-starv |
| P1 (k1) | λP1: w0 ∈ G-comp | B-starv |
| | λP2: w1 ∈ G-comp | F-starv |
| O1 (k3) | λQ1: w3 ∈ AB-comp (AB\*) | E3 |
| | λQ2: w2 ∈ lock-2 comp | F-starv |

**Lemma P identifies four pairs:** λQ2 = λA1, λL2 = λT2, λD1 = λM2 and λM1 = λK2. I checked each pair in absolute colours: the vertices are u4, u3, u2 and u0, and the four F-swaps involved are {A,G}, {A,D}, {A,D} and {A,G}, each of which preserves the relevant pair.

**Absolute form of the G-component leaks.**
- At O0: u2 and u3 both lie in the {B,G}-component of y0y1.
- At P1: u4 and u0 (the two flanks of p) both lie in the {g,d}-component of y2y3.

### 5.2 Γ′ (same method; single pass, less checked)

| state | leaks needed |
|---|---|
| C0 | {w2,m3} ∈ lock-2; w4 ∈ lock-1 |
| N2 | w2 ∈ lock-2; {w4,m0} ∈ lock-1 |
| L2 | {m2,w2} ∈ lock-2; w4 ∈ lock-1 |
| Q1 | w1 ∈ G-comp; {m4,w4} ∈ lock-1 |
| O3 | m1's {a,g}-comp meets the link (else E1 fails); w3 ∈ AB-comp |
| B0d | {w0,w1} ∈ G-comp; w3 ∈ AB-comp; **m3 ∈ {a,d}-comp of x2 and m3 ∉ K_B** |
| B0a | {w0,w1} ∈ G-comp; **m3 ∈ K_B** |
| N1b, N1d, L1g | w3 ∈ AB-comp |
| L1b | {w0,w1} ∈ G-comp; w3 ∈ AB-comp |
| R1a | w0 ∈ G-comp; **m4 ∈ K_F** |
| R1g | w0 ∈ G-comp; w3 ∈ AB-comp; **m4 ∈ {a,g}-comp of x0 and m4 ∉ K_F** |
| O2 | m1 ∈ {a,d}-comp of the link; w2 ∈ lock-2 |

**Why R1g and B0d carry two-sided constraints.**
- If m4's {a,g}-component is link-free, the silent swap gives R1a with the same component, so m4 ∉ K_F there, and F-E1′ kills.
- If it contains x2 or x3, F-E1′ kills R1g directly.
- So in a targetless class the component reaches x0 and avoids K_F. B0d is the same argument through B-E1″.

## 6. The partial theorem and the exact obstruction [hand]

**Theorem F1-partial.** Let v be a degree-5 hole of class (p,5,5,6,5), with p of any degree ≥ 5 and no separating triangle meeting the ball. Let s be DL.
- (a) If the pattern of s is one of the 16 killed patterns, then r(s) ≤ 2.
- (b) Otherwise s ∈ Γ ∪ Γ′, and r(s) ≤ 3 + d_L(s).
  - Here d_L is the length of the F/B walk, which is deterministic except at the four branch states, to the first state where a §5 leak or a branch constraint fails.
  - A failed branch constraint gives a non-DL F/B-image, adding at most 2.

**Obstruction (exact).** v has infinite radius if and only if some Kempe class at v is targetless (L3 [cited]). A targetless class 𝒦 must satisfy all of the following:
- every state of 𝒦 is DL with a pattern in Γ ∪ Γ′;
- at every state, every leak of §5.1 or §5.2 (whichever applies) holds, and every branch constraint holds;
- 𝒦 is closed under all swaps. In particular, the neutral silent swaps (N3 ↔ N1b, N0 ↔ N2, N1b ↔ N1d, L1g ↔ L1b) either stay inside 𝒦 or are blocked by the corresponding G-component or lock leak;
- the F/B orbits in 𝒦 are cycles (MathRstar55656 4.2), with pattern period 10.

On Γ alone, one F-turn requires **15 independent connections**: AB\* at all five R3 states, two G-component flanks at O0 and at P1, the G-component at A0 and at L0, and four lock leaks. All of them must hold simultaneously along every turn. Each turn also permutes the 2-ball colours by a 3-cycle, so the ball returns only after three turns (30 F-steps).

**What a proof still needs [open].** Two things would each suffice:
- a coupling lemma showing that the AB\* leak at an R3 state is incompatible with the G-component leaks at the next R1 state. Candidate pairs: T1 → O0, which needs AB\* via {u2, z} and then u2, u3 both in the {B,G}-component of y0y1; and L3 → P1, which needs AB\* at u4 and then both flanks of p in K_G;
- or an invariant that changes along every turn of Γ, which the 3-cycle colour rotation suggests.

This is the same open step as Candidate Lemma C of MathRstar55656, now with two-flank G-leaks (O0, P1), which are stronger than anything in (5,5,6,5,6).

## 7. Killed and negative lines

- **G-F / G-B (R5³ style): KILLED.** G is confined only at k = 2 (N0, N2), where x2 = p. G-F would need to read p's neighbours. G-B at x0 = y3 fails, because m0 = d (N0) or w0 = d (N2) is present.
- **Confined AB: KILLED.** It never occurs (§2). The triple contains p for k ≤ 2, and the degree-6 vertex leaks it for k = 3, 4.
- **Single-state planarity contradiction: KILLED for the three strongest states.**
  - At P1, the curve x1 w0 Q w1 x1 (Q a {g,d}-path inside K_G) passes through p, which is coloured b. So {a,b}-paths cross it freely.
  - At O0, the curve y3 u2 R u3 y3 encloses z. z escapes in {A,D} through y3, which is on the curve.
  - At R1g, the curve x0 w0 S m4 x4 v (S an {a,g}-path) confines only w4, and every complementary path crosses at a curve vertex of a shared colour.
  - As in MathRstar55656's partial negative, the locks and leaks are all positive connections, so a contradiction needs two or more states.
- **"Γ′ is impossible": not shown.** The two-sided constraints at R1g and B0d are consistent at a single state.
- **Diamond-freeness: no local use.** It gives deg u1 ≥ 6 and p ≥ 6, and no step reads a ring degree.

## 8. Studio check spec (not run here)

New script `onestar_f1.py`, written independently, stdlib only, no imports from vdred or the producer.

1. **Automaton.** Enumerate the patterns per k from the §2 rules.
   - Assert the counts 8/11/5/9/7 = 40, the 16 kills and the 24 survivors.
   - Assert the §3 transitions and branches.
   - Compare the 24 survivors with the vacancy-D game's 24 lost states for (*,5,5,6,5), mapped through the frame table of §1.
2. **Graphs.** Use every F1 hole (both orientations) in:
   - `gen_tri --all`, orders 16–22;
   - the Phase C/D certificates with link (5,6,5,5,8) (the radius-5 example);
   - 200 random triangulations with p of degree 6–14.
   Skip graphs with a separating triangle.
3. **Per DL state.**
   - (a) Compute the pattern and assert it is in the table.
   - (b) If killed, assert r ≤ 2.
   - (c) If it survives, follow F (or B) along Γ / Γ′, and at each visited state evaluate every §5 leak exactly (a component computation). Let d_L be the first failure. Assert r(s) ≤ 3 + d_L, and r(s) ≤ 2 + d_L when that failure is an E-type kill.
   - (d) Log every state at which all leaks hold. Report the longest run along Γ with all leaks present, and **whether any F-cycle with all leaks present exists** (that would be the obstruction realised).
   - (e) Assert the Lemma P identities on every Γ step.
4. **Expected:** 0 violations of (a)–(c) and (e). The radius-5 certificate state should lie on Γ or Γ′ with d_L ≤ 2.
5. **Budget:** one core, under 10 minutes.

## 9. Ledger

- **[hand]:**
  - the frame table;
  - the 40-pattern table (16 killed, 24 survivors);
  - all F-transitions;
  - the absolute recomputation of Γ and the 3-cycle observation;
  - Lemma SK and Lemma P;
  - the leak tables (Γ checked twice, Γ′ once);
  - Theorem F1-partial;
  - the obstruction statement;
  - the kills in §7.
- **[cited]:** Jordan facts, starvation, F-E1′/B-E1″, unlock, Lemma SS (corrected), pd2 corollary, MathRstar55656 4.2, L3.
- **[guidance]:** 24 lost states in the vacancy-D game; radius 5 at (5,6,5,5,8).
- **[open]:**
  - a radius bound or finiteness for F1;
  - the R3→R1 coupling lemma;
  - a second reader;
  - the Studio run of §8.
- **Every [hand] item is unchecked by a second reader and by machine.**
