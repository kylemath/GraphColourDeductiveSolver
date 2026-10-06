# Degree-5 holes with exactly two degree-6 neighbours: a Theorem-HP-style attack

Math research worker, 6 October 2026. **Hand work only.** The machine was on low battery, so no code, script, build or computation was run; files were only read. Labels: [hand] derived here by hand, not machine-checked; [open]; [guidance] a machine result from another note, used only to steer, never as proof; [inferred] read off another note's recorded data, not rechecked. Nothing else was edited, and nothing was committed.

Sources: MathHighDegreeNeighbour.md (Theorem HP), MathReviewTheoremHP.md, MathRadiusGeometry.md (Theorem H, T4 §4), MathSixFiveHole.md, MathVacancyDRed/REFINEMENT.md and README.md, MathConjectureR.md (T4), and navigator revisions 119 and 122 (Lemma R\*).

## Verdict, first

1. **The open sub-case [open].** *Lemma R\*(5³6²).* Let T be a triangulation with no separating triangle. Let v be a vertex of degree 5 whose link has three vertices of degree 5 and two of degree 6. Then every doubly locked (DL) state at v has Kempe radius at most R₀, for an absolute constant R₀. There are two cases:
   - **(adj)**: link degrees (5,5,5,6,6). This is T4's class, so R₀ ≥ 4.
   - **(non)**: link degrees (5,5,6,5,6). No radius lower bound is recorded beyond the trivial 2.

   [guidance] The 2-ball game is reducible at depth 7 for (adj) in `vdred` and at depth 14 for (non) in `vdred_joint`. These results are exploratory. The (non) result has not been through the verifier, and the audit's independent implementation is still outstanding.
2. **[hand] What survives from HP.** The Jordan facts, F-starvation, B-starvation and the mirror all survive. AB is still a kill when its component stays inside the link and an endpoint has no a-neighbour. Lemma 3 survives as a *recipe*: each ring vertex is forced into K_F, forced out of it, or branched. Two new kill rules appear: the **E1′ kill for F** and its mirror for B (§2). Lemma 1 is replaced by pattern tables:
   - (adj): 48 ring patterns over the five frame positions of the 6s, of which 25 are not killed by one move;
   - (non): 49 patterns, of which 28 are not killed.
3. **[hand] The precise obstruction.** In HP's local-certificate automaton (moves F, B, AB; the starvation rules, the E1′ rules and the confined-AB kill; leaks branched adversarially), **neither class closes**:
   - **(adj)** The adversary survives forever on a 20-state set C ∪ C*, made of two F-cycles of length 10, swapped into each other by a confined AB at the 6-6 position. C needs two leak choices per turn of the cycle; C* needs none (§4).
   - **(non)** **All 28 surviving states** form a closed set: a deterministic 10-cycle Γ₁ plus an 18-state set Γ₂ with branches (§5).
   - In both classes every AB along these sets leaks, through a ring vertex coloured b (an m- or w-vertex next to x₀, x₁ or x₂) or through m₁ = a. The adversary joins the leak to w₃ (HP's mechanism), so AB becomes a self-loop. So **no radius bound follows from HP's three moves**; this does not mean the radius is unbounded.
4. **[hand] Partial bound (adj).** Every DL state at a (5,5,5,6,6) hole whose frame pattern lies **outside C ∪ C*** has radius **at most 4** (§4.3). [inferred] T4's two radius-4 states have pattern P2, which lies on C. Their recorded F-chain of 3 matches C's one exit, at M(C4), when the leak there is absent.
5. **Missing ingredient [open].** Branching each leak independently ignores planarity. The vdred game's non-crossing outside matchings ([guidance]: they make both 2-balls reducible) are what a hand proof must import (§6).

## 1. Setup [hand]

- **The frame.**
  - Rotate the DL state so the link reads (a,b,a,g,d) on x₀..x₄.
  - Lock 1 is a {b,g}-path P₁ from x₁ to x₃. Lock 2 is a {b,d}-path P₂ from x₁ to x₄.
  - S ⊂ {0,…,4} is the set of frame positions with degree 6.
  - w_t is the common outer neighbour of x_t and x_{t+1}. For t ∈ S, m_t is the middle outer neighbour of x_t.
- **The ring.** Every link vertex has bounded degree, so the ring is a closed 7-cycle w₄ [m₀] w₀ [m₁] w₁ [m₂] w₂ [m₃] w₃ [m₄] w₄, with the m_t present for t ∈ S. All ring edges are present. This is strictly more structure than HP, where w_{k−1}w_k could be missing. As in the HP review, the proof only uses "adjacent, so differently coloured", so coincidences between ring vertices can only remove cases.
- **Admissible colours.**
  - w₀, w₁ ∈ {g,d}; w₂ ∈ {b,d}; w₃ ∈ {a,b}; w₄ ∈ {b,g}.
  - m₀ ≠ a, m₁ ≠ b, m₂ ≠ a, m₃ ≠ g, m₄ ≠ d.
- **Endpoint conditions** (Theorem H, Step 1):
  - (E1) the outer neighbours of x₁ include g and d;
  - (E2) the outer neighbours of x₃ include b;
  - (E3) the outer neighbours of x₄ include b.
- **Position classes.** F moves S to S+2 and B moves S to S−2 (mod 5). The mirror sends t to 2−t, swaps g and d, sends w_t to w_{1−t} and m_t to m_{2−t}, and exchanges F with B.
  - (adj): S ∈ {01, 12, 23, 34, 40}, with 12 the mirror of 01 and 40 the mirror of 23.
  - (non): S ∈ {02, 24, 41, 13, 30}, with 41 the mirror of 13 and 30 the mirror of 24.
- **B is the inverse of F [hand, elementary].** F(s) is read in the frame starting at x₃. B on F(s) swaps the {a,g}-component of x₃ in F(s). That component is K_F with its colours swapped, so B(F(s)) = s whenever F(s) is DL. The F/B part of the Kempe graph is therefore a union of paths and cycles; the "F-orbit" and the "B-orbit" of a state are the same object.

## 2. Rules, and which HP lemmas survive [hand]

| HP item | status here |
|---|---|
| Jordan facts (x₀ ∉ K_F, x₂ ∉ K_B) | **survive** (no degree used) |
| F-starvation (x₂ has no d-neighbour, so F(s) is not DL) | **survives** |
| B-starvation (x₀ has no g-neighbour) | **survives** |
| mirror | **survives** |
| Lemma 1 (R1, R2, R3) | **replaced** by the tables of §3; most of the new patterns use m₁ ∈ {g,d}, an m-vertex coloured b, or w₄ = g / w₂ = d next to an m |
| Lemma 2, AB kill of R3 | **survives only in the form below.** In (non) the triple {x₀,x₁,x₂} always contains a 6. In (adj) at S = 34 the triple has degree 5, but x₃ and x₄ can keep an a-neighbour through w₃ = a or m₃ = m₄ = a (states W, W*). |
| Lemma 3 (F: R1 to R3 to R1) | **survives as a recipe** (below). The images no longer alternate between two types. |
| termination table | **fails**: cycles (§4, §5) |

**Kill rules** (each one-move kill gives radius ≤ 2):
- **F-starv.** No d among the outer neighbours of x₂.
- **B-starv.** No g among the outer neighbours of x₀.
- **AB.** The outer neighbours of x₀, x₁ and x₂ all lie in {g,d}, so the {a,b}-component of x₁ is exactly {x₀,x₁,x₂}. After the swap, x₃ or x₄ has no a-neighbour, so lock 1′ or lock 2′ fails.
- **F-E1′ (new).** After F the new middle vertex is x₄, and it needs a neighbour of colour g after the swap.
  - w₄ = g is forced out of K_F (it is adjacent to x₀), so it stays g.
  - w₃ = a is forced in (it is adjacent to x₃), so it becomes g.
  - So the rule can only fire when 4 ∈ S, w₃ = w₄ = b and m₄ = a, and K_F has no ring vertex: then m₄ cannot join K_F and stays a.
  - The other new conditions are automatic: E2′ is d at x₁, which holds by E1, and E3′ is exactly F-starvation.
- **B-E1″ (new; the mirror of F-E1′).** It fires when 3 ∈ S, w₂ = w₃ = b, m₃ = a, and K_B has no ring vertex.

**Transition recipe for F.** K_F is the {a,g}-component of x₂ and contains x₃. Each a- or g-coloured ring vertex is classified as follows:
- **Forced in** if it is adjacent to x₂ or x₃, or joined along the ring to a forced-in vertex.
- **Forced out** if it is adjacent to x₀ (Jordan), or joined along the ring to a forced-out vertex.
- **Branched** otherwise. A vertex can be branched only if K_F already contains some ring vertex, because a ring vertex has at least one outside neighbour, while x₂ and x₃ have none outside the ball. If K_F contains no ring vertex, then K_F = {x₂, x₃} and nothing branches.

After the swap, read the ring in the frame (x₃,x₄,x₀,x₁,x₂): w′_t = w_{t+3} and m′_t = m_{t+3}. The colours are renamed a→a, d→b, b→g, g→d. Then check E1 to E3 in the new frame.

## 3. Pattern tables [hand]

Notation: w = w₀w₁w₂w₃w₄, followed by the m's. Each count was enumerated by hand from the admissible colours, E1 to E3, and properness along the ring. Kills are marked †.

### (adj) (5,5,5,6,6): 48 patterns, 25 survive

- **S = 01** (7 patterns):

  | name | w | m₀, m₁ | status |
  |---|---|---|---|
  | P1 | dgdbg | b, a | survives |
  | P2 | ggdbg | b, d | survives |
  | P3 | ggdbg | d, d | †AB |
  | P4 | gdbab | d, a | survives |
  | P5 | dgbab | g, a | †F-starv |
  | P6 | ggbab | d, d | †F-starv |
  | P7 | ddbab | g, g | survives |

  Derivation: w₃ = b forces w₂ = d, w₄ = g and w₁ = g. w₃ = a forces w₂ = w₄ = b. Then (w₀, m₁, w₁) is one of (g,a,d), (d,a,g), (g,d,g) or (d,g,d), and m₀ is then determined, with two choices in the ggdbg row.
- **S = 12:** the mirrors M(P1) to M(P7). M(P3) is killed by AB, and M(P5), M(P6) by B-starv.
- **S = 23** (8 patterns):

  | name | w | m₂, m₃ | status |
  |---|---|---|---|
  | C1 | gdbab | g, d | survives |
  | C2 | gddab | b, b | survives |
  | C3 | gddab | g, b | survives |
  | C4 | dgbbg | d, a | survives |
  | C5 | dgbbg | d, d | survives |
  | C6 | dgdbg | b, a | survives |
  | C7 | dgbab | d, d | †B-starv |
  | C8 | dgdab | b, b | †B-starv |

- **S = 40:** the mirrors M(C1) to M(C8).
- **S = 34** (18 patterns):
  - A1: w = gdbab, m₃ = d, m₄ = g.
  - A2(m₃,m₄): w = gdbbb, with m₃ ∈ {a,d} and m₄ ∈ {a,g}. A2(d,a) is killed by F-E1′ and A2(a,g) by B-E1″.
  - Eleven of the 13 patterns with w₀w₁ = dg die by starvation: B-starvation if w₄ = b, F-starvation if w₂ = b.
  - The two survivors of that group are **W**: w = dgdag, m₃ = m₄ = b, and **W\***: w = dgdbg, m₃ = m₄ = a.
  - Survivors at S = 34: A1, A2(a,a), A2(d,g), W, W*.

### (non) (5,5,6,5,6): 49 patterns, 28 survive

- **S = 02** (7 patterns):
  - N1(m₂,m₀): w = gddbg, with m₂ ∈ {b,g} and m₀ ∈ {b,d}. N1(g,d) is killed by AB, since x₃ then sees d and b only.
  - N2: w = gdbab, m₀ = d, m₂ = g.
  - N3: w = dgdbg, m₀ = m₂ = b.
  - N4: w = dgbab, m₀ = g, m₂ = d.
- **S = 24** (10 patterns):
  - L1(m₂,m₄): w = gddbb, with m₂ ∈ {b,g} and m₄ ∈ {a,g}. L1(b,a) is killed by F-E1′.
  - L2: w = gdbab, m₂ = m₄ = g.
  - L3(w₄,m₄): w = dgdb·, m₂ = b, with (w₄,m₄) ∈ {(b,a), (b,g), (g,a)}. The two with w₄ = b are killed by B-starv.
  - L4(w₄,m₄): w = dgba·, m₂ = d, with (w₄,m₄) ∈ {(b,g), (g,b)}. (b,g) is killed by B-starv.
  - Below, **L3 := L3(g,a)** and **L4 := L4(g,b)**.
- **S = 13** (11 patterns). Write (w₀ m₁ w₁) first, then w₂, m₃, w₃, w₄:

  | name | (w₀ m₁ w₁) | w₂ | m₃ | w₃ | w₄ | status |
  |---|---|---|---|---|---|---|
  | O1 | dag | b | a | b | g | †F-starv |
  | O2 | dag | b | d | b | g | †F-starv |
  | O3 | dag | d | a | b | g | survives |
  | O4 | dgd | b | a | b | g | survives |
  | O5 | dgd | b | d | b | g | survives |
  | O6 | gad | b | d | a | b | survives |
  | O7 | dag | b | d | a | b | †B-starv |
  | O8 | dag | d | b | a | b | †B-starv |
  | O9 | gdg | b | d | a | b | †F-starv |
  | O10 | gdg | d | b | a | b | survives |
  | O11 | dgd | b | d | a | b | †B-starv |

- **S = 41 and S = 30:** the mirrors of S = 13 and S = 24.

## 4. (adj): the closed set C ∪ C* [hand]

### 4.1 Cycle C (two leak choices)

**P2** →F C3 →F M(C4) →F M(P7) →F **W** →F P7 →F C4 →F M(C3) →F M(P2) →F A2(d,g) →F P2.

- Every step was computed by the recipe of §2, and E1 to E3 were checked in each image. C is mirror-closed.
- **Branch at M(C4)** (S = 40; w = dgdbb, m₄ = a, m₀ = g):
  - K_F is forced to contain w₁.
  - m₄ is joined to x₄, w₃ and w₄ only, so it is branched.
  - If m₄ is out, F-E1′ fails and the image is not DL. The adversary therefore needs m₄ ∈ K_F, which requires an outside {a,g}-path from m₄ to K_F.
- **Branch at P7:**
  - K_F is forced to contain w₃, and m₁ (coloured g) is branched.
  - Out-branch: P7 → C5 → M(C2) → M(P3), which is an AB kill.
  - In-branch: m₁ joins K_F, giving C4.
- **AB along C:**
  - W is the only state where AB stays inside the link. There the swap gives W*, because x₃ and x₄ keep the a-neighbour w₃.
  - Every other state of C leaks through a ring vertex coloured b next to the triple (m₀, w₄ or w₂) or through m₂ = b.
  - **Self-loop lemma [hand, in the independent-branch model].** Suppose a swap of an {a,b}- or {g,d}-component of a link vertex keeps the frame and is forced to contain a ring vertex. Then the adversary may put every ring vertex of those two colours into the component. The ring pattern read in roles is then unchanged, so the move is a self-loop.

### 4.2 Cycle C* (deterministic)

**W\*** →F P4 →F C6 →F M(C1) →F M(P1) →F A1 →F P1 →F C1 →F M(C6) →F M(P4) →F W*.

No vertex is branched at any step, and no kill rule fires. AB is confined only at W*, where it gives W.

Because B = F⁻¹ = M F M and C ∪ C* is mirror-closed, B also stays inside the set. So **C ∪ C\* is closed under F, B and AB with adversarial leaks, and no kill fires on it.** That is the obstruction.

### 4.3 Bounds off C ∪ C* [hand]

The surviving states outside C ∪ C* are C2, C5, M(C2), M(C5) and A2(a,a). Each bound follows from "radius ≤ 1 + d" along the chains:

| state | chain to a kill | radius ≤ |
|---|---|---|
| A2(a,a) | F gives P3 (m₄ is forced into K_F by E1′), and P3 is an AB kill | 3 |
| M(C2) | F gives M(P3), an AB kill | 3 |
| C2 | B = M F M gives P3 | 3 |
| C5 | F gives M(C2) | 4 |
| M(C5) | B gives C2 | 4 |
| killed states | one move | 2 |

**So in class (adj), radius ≤ 4 off C ∪ C\*. On C ∪ C\* no local bound exists.**

**T4 consistency [inferred].**
- MathRadiusGeometry §4 gives the {a,b}-component of the middle vertex in T4's radius-4 states as {2,5,6,8,9,12,15,16}. In frame terms: x₀ = 8, x₁ = 9, x₂ = 5, m₀ = 12, m₁ = 14, w₃ = 2. This component contains m₀ and avoids w₀, m₁, w₁ and w₂, which forces the pattern **P2**.
- Its leak runs from m₀ through outside vertices to w₃, exactly HP's mechanism.
- The F-chain P2, C3, M(C4) followed by the out-branch at M(C4) has 3 DL states, matching the recorded chain 3 and radius 4 = 1 + 3.
- Not rechecked, because no code was run.

## 5. (non): every surviving state is in the obstruction [hand]

**Γ₁ (deterministic 10-cycle, mirror-closed):** N3 →F L2 →F M(O3) →F O6 →F M(L3) →F N2 →F L3 →F M(O6) →F O3 →F M(L2) →F N3.

**Γ₂ (18 states).** It consists of N1(b,b), N1(b,d), N1(g,b), N4; L1(b,g), L1(g,a), L1(g,g), L4; M(O4), M(O5), M(O10); O4, O5, O10; and M(L1(b,g)), M(L1(g,a)), M(L1(g,g)), M(L4). Its F-arrows are:
- N1(b,b) → L1(g,g); N1(b,d) → L1(b,g); N1(g,b) → L1(g,a); N4 → L4.
- L1(b,g) → M(O5); L1(g,·) → M(O4), where E1′ forces the leak choice; L4 → M(O10).
- M(O4) → O10; M(O5) → O10; M(O10) → O4 or O5 (m₁ branched).
- O4 → M(L1(g,a)) or M(L1(g,g)) (m₁ branched); O5 → M(L1(b,g)); O10 → M(L4).
- M(L1(g,a)) → N1(b,d); M(L1(g,g)) → N1(b,b); M(L1(b,g)) → N1(g,b); M(L4) → N4.

For example, N4 → L4 → M(O10) → O5 → M(L1(b,g)) → N1(g,b) → L1(g,a) → M(O4) → O10 → M(L4) → N4 is a 10-cycle.

- **AB:** it leaks in all 28 states, and in (non) the triple always contains a 6. At N3, for example, the forced footprint is {m₀, m₂}, and AB kills unless w₃ joins; the adversary joins it, so AB is a self-loop. AB is confined only in N1(g,d) (killed) and nowhere in Γ₁ ∪ Γ₂.
- **Conclusion:** the independent-branch automaton for (non) has **no** state with a local bound other than the one-move kills (radius ≤ 2). This is weaker than (adj), where at least the off-cycle states are bounded.
- [guidance] The joint-refinement result for (non), depth 14, comes entirely from the ring-free knowledge-retention rule, that is, from memory carried between moves.

## 6. Where the proof must go next [open]

- **What the obstruction relies on.**
  - Leaks are chosen independently at each step, with no memory: m₄ joined at M(C4), m₁ joined at P7, and every AB leak joined to w₃.
  - In vdred terms, the {a,b}|{g,d} matching that joins m₀ to w₃ at P2 must cut off the run of colours g and d on one side. Non-crossing matchings couple the leak of one swap to the isolation of the complementary colour runs.
  - Successive F moves cycle through the splits {a,g}, {a,b}, {a,d}, so a matching revealed at step i is relevant again at step i+3, provided the swaps in between do not touch the outside.
- **Candidate hand lemma [open].** Along C (and Γ₁), the leak choices required in one 10-cycle cannot all be realised by one sequence of non-crossing outside matchings consistent with P₁ and P₂. If true, C ∪ C* would yield a bound, and with §4.3, a bound for (adj).
- **Not tried:** the G swap ({g,d} of x₃x₄, which is a self-loop under total leak), and swaps seeded at ring vertices.

## 7. Killed lines

- **K-26-1** "HP's automaton (F, B, AB plus starvation) closes for two 6s": false; see the closed sets of §4 and §5 [hand, in the model].
- **K-26-2** "At S = 34 the triple has degree 5, so HP's AB kill applies": false; W and W* keep an a-neighbour at x₃ and x₄ through w₃ or m₃, m₄.
- **K-26-3** "(non) is locally easier because the 6s are separated": false for this automaton, since Γ₁ needs no leak choice at all. The machine difference (14 versus a loss under plain vdred) comes from memory, not from locality.
- **K-26-4** "Independent leak branching can certify any class in which every AB component contains a ring vertex": false; the self-loop lemma of §4.1 defeats it.
- **K-26-5** "F and B give two independent routes": no; B = F⁻¹ on DL images (§1).

## 8. Ledger

- [hand]:
  - the B = F⁻¹ remark;
  - the F-E1′ and B-E1″ kill rules;
  - the pattern tables (48 and 49 patterns; 25 and 28 survive);
  - all transitions listed;
  - the closed sets C ∪ C* and Γ₁ ∪ Γ₂;
  - the self-loop lemma;
  - radius ≤ 4 off C ∪ C* in (adj).
- [inferred]: T4's radius-4 states are P2 on C, with an exit at M(C4).
- [open]:
  - Lemma R\*(5³6²) in both cases;
  - the matching-coupled lemma of §6;
  - any radius lower bound for (non).
- **Every [hand] item above is unchecked by a second reader and by machine.**

## 8a. Check of intern A (interns-2026-10-06/intern-A.md, commit 648559b; class (5,5,5,6,6), 6s at frame positions {3,4}) [hand]

The Math lead asked for this check, relayed by the coordinator. I re-derived the pattern list for S = 34 independently, before reading intern A's list; it is in §3 above. Intern A writes patterns as w₀..w₄ only, with no m-colours.

**Re-derived list for S = 34.**
- The ring is w₄ w₀ w₁ w₂ m₃ w₃ m₄. Because x₁ has degree 5, {w₀, w₁} = {g, d}.
- Case w₀w₁ = gd: then w₂ = w₄ = b.
  - w₃ = a gives gdbab, with m₃ = d and m₄ = g.
  - w₃ = b gives gdbbb, with m₃ ∈ {a,d} and m₄ ∈ {a,g}, so 4 patterns.
- Case w₀w₁ = dg: the w-strings are dg{b,d}{a,b}{b,g}, 8 strings carrying 13 m-completions.
- Total: **10 w-strings, 18 full patterns.**

**Verdicts.**
- **(a) Jordan facts and starvation are degree-free: CORRECT. "The starvation kills fail when x₂ (or x₀) has degree 6": WRONG.**
  - F-starvation needs only that x₂ has no d-neighbour; that is HP §1, valid for any degree. A degree-6 x₂ has three outer neighbours, all inside the ball, so the rule can still be read and applied. It simply fires less often.
  - Example: P5 and P6 at S = 01 die by F-starvation, and C7 and C8 at S = 23 die by B-starvation, even though S contains 0 or 2 there.
  - What is lost at a degree-6 x_t is HP's two-element form of E1–E3, not the rule itself. Intern A's §1 sentence "any lock-end condition read at x_t is lost" is also wrong. The conditions hold in the weaker three-neighbour form (E2: b ∈ {w₂, m₃, w₃}; E3: b ∈ {w₃, m₄, w₄}).
- **(b) 10 patterns: CORRECT as a count of w-strings.** The list matches mine exactly: gdbab, gdbbb, and dg{b,d}{a,b}{b,g}.
  - **GAP:** the m-colours split these into 18 patterns, and the kills depend on m. For gdbbb, A2(d,a) dies by F-E1′ and A2(a,g) by B-E1″ (§2), while A2(a,a) and A2(d,g) survive.
  - The intern's derivation also says that "b ∈ {w₂,w₃}" and "b ∈ {w₃,w₄}" are lost. They are weakened (E2, E3 with m₃, m₄), not lost. With w₀w₁ = gd they are automatic, since w₂ = w₄ = b.
- **(c) dgbbb dies by B-starvation: CORRECT.** At S = 34 the outer neighbours of x₀ are w₄ = b and w₀ = d.
  - **gdbbb and dgdag escape both starvation rules: CORRECT.**
  - **"They are the residue": WRONG.** After all one-move kills (starvation, confined AB, E1′), five states survive at S = 34:
    - A1 = gdbab (HP's R1; it never had a one-move kill);
    - A2(a,a) and A2(d,g) = gdbbb;
    - W = dgdag, with m₃ = m₄ = b forced;
    - W\* = dgdbg, HP's R3, with m₃ = m₄ = a forced.
  - Intern A counts R3 as surviving in §3(i), but omits R1 = gdbab.
- **(d) The AB kill for R3 at S = 34 fails: CORRECT as a conclusion. The reason given, "m₃ and m₄ are unconstrained", is WRONG.**
  - At dgdbg, m₃ ≠ w₂ = d and m₃ ≠ g, so m₃ = a. Likewise m₄ ≠ w₄ = g and m₄ ≠ d, so m₄ = a. Both are **forced to be a**.
  - That is exactly why the kill fails. The component {x₀,x₁,x₂} is exact, as the intern says. After the swap, x₃ and x₄ keep the a-neighbours m₃ and m₄, so locks 1′ and 2′ can survive.
- **(e) F sends {3,4} to {0,1} and B sends it to {1,2}: CORRECT.** In general F sends S to S − 3 and B sends S to S + 3.
  - The intern's F-image of gdbbb, (g′,g′,d′,b′,g′) at {0,1}, is CORRECT for A2(d,·): it is my P2, with m₀ = b and m₁ = d.
  - **GAP:** "F leaves the ring unchanged" holds only for m₃ = d. For A2(a,·), m₃ = a is forced into K_F, and the image is P3, which dies by AB (§4.3).
  - At {0,1}, E1 has not lost the {g,d} condition. It becomes {w₀, m₁, w₁} ⊇ {g, d}, which P2 meets through m₁ = d.
  - The claim "these are exactly the pairs where a starvation kill is lost" inherits the error in (a).
- **(f) Repair: constrain the colours of m₃ and m₄: WRONG (vacuous) for R3.** At S = 34 the R3 state W\* has m₃ = m₄ = a forced by properness. The proposed colour condition is therefore never met by a DL state. Nor can the colours be "repaired" by a separate Kempe step without leaving the frame. This is one face of the §4 obstruction: W\* lies on the deterministic cycle C\*.

**Exact target for the sub-case, replacing "gdbbb and dgdag".**
- Not a single position: the residue is a set of F-cycles that rotates S through all five positions.
- For (adj) the target is the **20-state set C ∪ C\*** of §4. Its S = 34 members are A1 (gdbab), A2(d,g) (gdbbb with m₃ = d, m₄ = g), W (dgdag) and W\* (dgdbg).
- Every other DL state of the class has radius ≤ 4 [hand, §4.3]. This includes A2(a,a), which reaches the AB kill at P3 in one F step.
- **Target statement [open]:** DL states whose frame pattern lies on C ∪ C\* have bounded radius. With §4.3, this gives Lemma R\*(adj).

## 9. For the Mac Studio (through the coordinator; nothing was run here)

1. **Pattern and automaton check.** A new script, `lc_two_six.py`, is needed; write it independently and do not import vdred.
   - Input: a class, `adj` or `non`.
   - For each S: enumerate all 4^7 ring colourings; keep those that are proper and satisfy E1 to E3; apply the kills of §2; build the F graph by the recipe of §2, branching a vertex only when K_F contains a ring vertex; compute the adversary's greatest closed kill-free set under F, B = M F M and AB, with AB modelled by the self-loop lemma.
   - Expected:
     - `python3 lc_two_six.py --class adj` prints counts 7/7/8/8/18, 25 survivors, and a closed set of 20 equal to C ∪ C*;
     - `python3 lc_two_six.py --class non` prints counts 7/11/11/10/10, 28 survivors, and a closed set of 28.
   - Budget: one core, under a minute.
2. **T4 check.**
   - Command: `python3 lc_two_six.py --t4`, using T4's faces from MathConjectureR §3 with hole v = 4.
   - For each DL state, print S, the pattern, the F-chain and the radius.
   - Expected: the radius-4 states are P2 at S = 01, or its mirror M(P2) at S = 12, and their F-orbit leaves DL at M(C4).
3. **Machine guidance, rerun.** From `SolvingFrameworkPlan/docs/working/MathVacancyDRed/`:
   ```
   python3 -c "import family, vdred_joint; print(vdred_joint.solve_joint(family.config_from_degrees((5,5,5,6,6))))"
   python3 -c "import family, vdred_joint; print(vdred_joint.solve_joint(family.config_from_degrees((5,5,6,5,6))))"
   ```
   Expected: depth 7 and depth 14 (REFINEMENT §3). Then run REFINEMENT §4 item 1 (`verify.check` on a host graph for (5,5,6,5,6)).
4. **Test of the §6 lemma.** Rerun the vdred_joint strategy for (5,5,5,6,6) restricted to states whose ring pattern lies on C ∪ C*, and print the first move of each winning line. This tells us which non-F/B/AB swap, or which retained matching, breaks the cycle.
