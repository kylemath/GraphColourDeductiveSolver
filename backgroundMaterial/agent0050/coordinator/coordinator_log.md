# Coordinator Log — Agent 0050-C

**Agent:** 0050-C
**Main Agent:** 0050
**Date:** 18 February 2026

---

## Iteration 1 — 18 February 2026

### Manager Status

| Manager | Stream | Status | Quality Gate |
|---------|--------|--------|--------------|
| M1 | Computational Verification ("The Engineers") | Complete | **Passed** — 12/12 tests |
| M2 | Theoretical Formalization ("The Mathematicians") | Complete | **Passed with caveat** — Lemma not proved |

### Cross-Manager Checks

- [x] **No conflicting assumptions between managers** — M1 and M2 independently discovered the external-vertex requirement for non-crossing checks. Their conclusions align.
- [x] **No duplicated work across streams** — M1 builds infrastructure, M2 builds theory. Clean separation.
- [x] **Integration points identified and addressed:**
  - M1-S3's non-crossing data confirms M2-S1's Theorem A predictions ✓
  - M1-S2's $\mathcal{R}(T,4)$ connectivity matches M2's Fisk theory ✓
  - M1-S1's "all 5-colourings reduce" is consistent with (but doesn't prove) M2-S3's Lemma ✓
- [x] **All escalated questions addressed** — M2-S3 raised the circularity concern, which is documented in escalations.md

### Cross-Team Convergence Points

1. **External vertex insight:** Both teams (M1-S3 via debugging, M2-S1 via proof structure) arrived at the same conclusion: the local non-crossing check is valid only at external vertices. This is a genuine mathematical insight that emerged from the competition.

2. **Small-case triviality:** Both teams note that $n \leq 6$ cases are "too easy." M1 finds max path length 2; M2 finds all cases resolvable by 1 swap. The hard cases (if they exist) are at larger $n$.

3. **Fisk and 4CT circularity:** $\mathcal{R}(T,4)$ connectivity follows from Fisk + 4CT. Neither team can prove it independently. This is a fundamental limitation of Plan 2's current approach.

### Competition Results

**Winner of Iteration 1: TIE — with M1 having slight edge.**

| Criterion | M1 (Engineers) | M2 (Mathematicians) |
|-----------|---------------|---------------------|
| Tests passed | 12/12 | N/A (theoretical) |
| Novel insights | External-vertex methodology (via debugging) | Theorems A, B, classification |
| Hard results | All 5-colourings reduce for $n \leq 6$ | Colour Elimination Lemma FAILED |
| Impact | Working code + verified data | Theoretical framework + identified obstacle |

M1's edge: they produced working, tested code that verifies claims. M2 produced important theory but couldn't close the key lemma.

M2's strength: they identified the EXACT obstacle (Chain Disconnection Lemma) that is the bottleneck for the entire Plan 2 approach. This is arguably the most important output of the iteration.

### Cross-Pollination Directives

**For M1 (next iteration):**
1. Extend verification to $n = 7, 8$ — look for harder cases
2. Specifically test M2-S3's Chain Disconnection Lemma computationally
3. Track not just "does reduction exist?" but "what is the minimum path length?" and "which swap is needed?"
4. Log cases where the sequential elimination strategy (processing colour-5 vertices one at a time) would fail with restricted swaps

**For M2 (next iteration):**
1. Formalize the Chain Disconnection Lemma as a precise conjecture
2. Explore the three resolution approaches (distance, ordering, multi-step) more deeply
3. Look at the problem from the reconfiguration perspective: R(G,5) is connected (Las Vergnas-Meyniel), so ANY 5-colouring can reach ANY other. Can we characterise which 5-colourings are "close" to 4-colourings in R(G,5)?
4. Consider a different proof architecture: instead of sequential elimination, prove that the diameter of R(G,5) from any 5-colouring to the nearest 4-colouring is bounded

### Decisions Made

1. **Keep both teams active for iteration 2.** Both produced valuable work. The competition structure is working.
2. **Prioritize Chain Disconnection Lemma.** This is the bottleneck. M1 should test it computationally, M2 should attempt to prove it.
3. **Extend to $n = 7, 8$.** This is where hard cases are most likely to emerge.

### Notes

The iteration revealed a clean separation of difficulty:
- **Easy part (done):** Single-vertex recolouring, non-crossing at external vertices, Fisk group computation
- **Hard part (open):** Multi-vertex sequential elimination, chain interference between recolouring steps

Plan 2's central thesis — that planarity constrains Kempe chain interference enough for a constructive 4CT proof — remains neither confirmed nor refuted. The computational evidence ($n \leq 6$) supports it, but the theoretical analysis identifies a specific obstacle that might be as hard as 4CT itself.

---

## Final Assessment

**All streams:** Complete (Iteration 1)
**Cross-stream integration:** Verified — no conflicts, strong alignment
**Ready for iteration 2:** Yes — with clear directives for both teams

**Craftsperson says:** Both teams produced solid work. The infrastructure is production-quality, the theory is rigorous where it applies, and the obstacle is precisely identified.

**Skeptic says:** The Colour Elimination Lemma failure is the elephant in the room. If the Chain Disconnection Lemma is as hard as 4CT, Plan 2 may be a dead end. The small-case evidence is encouraging but doesn't rule out obstruction at larger $n$.

**Mover says:** We've built a complete toolkit and identified the exact mathematical question that needs answering. This is substantial progress. The next iteration should focus 80% of effort on the Chain Disconnection Lemma — computationally and theoretically.

---

## Iteration 2 — 18 February 2026

### Manager Status

| Manager | Stream | Status | Quality Gate |
|---------|--------|--------|--------------|
| M1 | Computational Verification ("The Engineers") | Complete | **Passed** — 17/17 tests, n=8 verified |
| M2 | Theoretical Formalization ("The Mathematicians") | Complete | **Passed** — CDL reformulated, near-proof found |

### Cross-Manager Checks

- [x] **No conflicting assumptions between managers** — Both agree the strict CDL is false. Both agree unrestricted elimination works computationally.
- [x] **No duplicated work across streams** — M1 produces data, M2 produces theory. Clean separation maintained.
- [x] **Integration points identified and addressed:**
  - M1's CDL disproval directly informed M2's pivot to Never-Revert Lemma ✓
  - M1's distance = n-4 pattern matches M2's inductive bound (n-4 steps) ✓
  - M1's degree distribution correlation matches M2's structural explanation ✓
- [x] **All escalated questions addressed** — M2-S3's inductive proof gap is documented in escalations.md

### Key Findings — Both Teams

#### 1. Strict CDL is FALSE (M1 finding, M2 acknowledged)
The "safe swaps only" approach fails starting at n=6. At n=8, 11/14 triangulations have restricted-elimination failures. Even 5 preparatory safe swaps don't help.

#### 2. Unrestricted Elimination ALWAYS works (M1 finding)
Over 45,000 attempts across all triangulations n <= 8, zero failures. Every ordering works with unrestricted swaps.

#### 3. Max R(G,5) Distance = n-4 (M1 finding, tight bound)
| n | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|
| Max dist | 0 | 1 | 2 | 3 | 4 |

This pattern is exact for all tested n. M2's inductive argument predicts this bound.

#### 4. Never-Revert Lemma (M2 finding, trivially proved)
Kempe swaps on {1,2,3,4} pairs never produce colour 5. This eliminates the need for the strict CDL entirely. The set of colour-5 vertices can only shrink under such swaps.

#### 5. Near-Complete Inductive Proof (M2 finding)
An inductive argument on vertex count nearly proves the linear distance bound. Gap: Kempe chain correspondence between G and G-v when adding a degree-5 vertex back.

### Competition Results

**Winner of Iteration 2: TIE — both teams delivered critical results.**

| Criterion | M1 (Engineers) | M2 (Mathematicians) |
|-----------|---------------|---------------------|
| Key finding | CDL disproved + unrestricted works | Never-Revert Lemma + near-proof |
| Data produced | n=7, n=8 complete verification | 3 reformulated conjectures |
| Novel insight | Distance = n-4 pattern | Inductive proof architecture |
| Hard result | 45,000 tests, 0 failures | Partial theorem with identified gap |
| Impact | Redirected M2's theory | Framework for constructive 4CT proof |

M1's edge: they DISPROVED the CDL, which is a hard computational result that reshaped the entire theoretical direction. Their distance = n-4 observation is potentially the most important finding of both iterations.

M2's edge: they FOUND A NEAR-PROOF. The Never-Revert Lemma is trivial but transformative. The inductive argument, if the gap closes, constitutes a constructive proof of 4CT with explicit O(n) swap bound.

### Cross-Pollination Directives

**For M1 (next iteration):**
1. Push to n=9 (50 triangulations) — does distance = n-4 hold?
2. Test the inductive argument computationally: for each triangulation on n=8, remove a min-degree vertex, verify the restricted problem on n-1 vertices, then add the vertex back and verify one more swap suffices
3. Profile the "hardest" colourings (max distance): what structural properties do they share?
4. Generate a database of ALL swap sequences for n <= 7 — monotone paths where |V_5| decreases at each step

**For M2 (next iteration):**
1. Close the inductive proof gap: prove Kempe chain correspondence between G and G-v
2. Formalize the argument for non-triangulation planar graphs
3. If the gap doesn't close: explore whether the BFS distance argument (Strategy C) can be made rigorous using expansion properties
4. Write up the complete argument (with gap clearly marked) as a draft paper section

### Decisions Made

1. **CDL is dead — pivot complete.** Both teams now focus on the unrestricted approach + distance bound.
2. **The inductive proof gap is THE open question.** Both iterations narrowed from "how to prove 4CT" to "how do Kempe chains behave when adding a vertex." This is genuine progress.
3. **Extend to n=9 next iteration.** The distance = n-4 pattern needs testing at n=9 (50 triangulations).

### Notes

The iteration produced a dramatic pivot. The strict CDL — which seemed like the natural approach — is false. But the failure revealed something better: unrestricted elimination works and the Never-Revert Lemma makes it theoretically sound. The inductive argument is the closest anyone has come to a Kempe-swap proof of 4CT in this project.

The honest assessment: the gap in the inductive proof (Kempe chain correspondence when adding a vertex) might be equivalent to 4CT itself. If so, Plan 2 has achieved a CLEAN REFORMULATION but not a proof. However, the reformulation is much more specific and attackable than the original question.

Progress score: 7/10 (up from 5/10 in iteration 1). We've gone from "can we even reduce 5 to 4?" to "we have a near-complete proof with one identified gap."

---

## Final Assessment (Iteration 2)

**All streams:** Complete
**Cross-stream integration:** Verified — strong alignment, CDL pivot was smooth
**Ready for iteration 3:** Yes — with clear focus on the inductive proof gap

**Craftsperson says:** Both teams delivered exceptional work. M1's data is comprehensive and reveals a striking pattern (distance = n-4). M2's theoretical pivot was rapid and productive — the Never-Revert Lemma and inductive argument represent genuine mathematical progress.

**Skeptic says:** The inductive proof gap is worrying. "Near-complete" proofs of 4CT have a long history of failing when the last gap turns out to be as hard as the original problem. The distance = n-4 pattern could fail at n=9 (50 triangulations might reveal a counterexample). We must not get ahead of ourselves.

**Mover says:** Two iterations in, we've built comprehensive computational infrastructure (17 tests, 6 Python modules), proved rigorous lemmas (A, B, Never-Revert), and identified a near-proof with a concrete gap. This is the most productive state the project has been in. Push to n=9, attack the gap, and see what happens.

---

*0050-C — 18 February 2026*

---

## Iteration 3 — 18 February 2026

### Manager Status

| Manager | Stream | Status | Quality Gate |
|---------|--------|--------|--------------|
| M1 | Computational Verification ("The Engineers") | Complete | **Passed** — 23/23 tests, n=9 verified |
| M2 | Theoretical Formalization ("The Mathematicians") | Complete | **Passed** — Chain Lifting proved (partial), draft paper produced |

### Cross-Manager Checks

- [x] **No conflicting assumptions between managers** — Both agree: chain lifting works for {1,2,3,4} pairs (proved), unproved for (a,5) pairs (but zero computational failures).
- [x] **No duplicated work across streams** — M1 builds optimized infrastructure, M2 formalizes theory. Clean separation.
- [x] **Integration points identified and addressed:**
  - M1's zero-merge finding directly validates M2's chain lifting framework ✓
  - M1's tightness breaking informs M2's bound analysis ✓
  - M1's monotone path data confirms M2's analysis that strict monotonicity fails ✓
  - M2's draft paper incorporates all of M1's computational tables ✓
- [x] **All escalated questions addressed** — M2's (a,5)-chain merge question is the ONE remaining open problem.

### Key Findings — Iteration 3

#### 1. n=9: ALL reduce, max distance = 4 (M1 finding)
50 triangulations, 282,300 five-colourings. Every single one reaches a 4-colouring. The bound n-4=5 holds, but the tight bound breaks — max distance is only 4.

#### 2. Chain Lifting Lemma for {1,2,3,4} pairs: PROVED (M2 finding)
When c(v) = 5, the (a,b)-chains for a,b ∈ {1,2,3,4} are identical in G and G-v. Trivially true because v is not in the bichromatic subgraph.

#### 3. Zero chain merge failures in inductive lift (M1 finding)
42,168 colourings tested, 518 specific (a,5)-swaps in BFS paths examined. Zero merges. Even though (a,5)-chains merge ~12% in general, BFS-optimal paths never use chains that merge.

#### 4. Strict |V_5|-monotonicity fails (~51% at n=9) (M1+M2 finding)
Not all 5-colourings have strictly monotone reduction paths. But BFS shortest paths are weakly monotone.

#### 5. Draft paper section: COMPLETE (M2 deliverable)
10 sections, full mathematical rigour. Clearly separates proved results from conjectures. Located at `deliverables/draft_paper_section.md`.

### Competition Results

**Winner of Iteration 3: TIE — strongest iteration yet from both teams.**

| Criterion | M1 (Engineers) | M2 (Mathematicians) |
|-----------|---------------|---------------------|
| Key finding | Zero merge failures | Chain Lifting Lemma (proved for {1,2,3,4}) |
| Scope | n=9 (50 graphs, 280K colourings) | Complete draft paper (10 sections) |
| Novel insight | BFS paths avoid mergeable chains | {1,2,3,4}-chains identical in G and G-v |
| Hard result | 23 tests, 0 failures | Formal proof + gap identification |
| Impact | Strongest computational evidence base | Publication-ready document |

### Cross-Pollination Summary (All Iterations)

| Iteration | M1 finding → M2 impact | M2 finding → M1 impact |
|---|---|---|
| 1 | External-vertex methodology → Theorem A proof | Chain Disconnection Lemma → CDL testing |
| 2 | CDL disproved → Never-Revert pivot | Inductive argument → distance computation |
| 3 | Zero merges → validates chain lifting | Chain Lifting for {1,2,3,4} → theoretical framework for lift |

### Cumulative Results (Iterations 1-3)

**Proved:**
- Theorem A (Non-Interleaving) ✓
- Theorem B (Confinement) ✓
- Never-Revert Lemma ✓
- Chain Lifting for {1,2,3,4} pairs ✓
- Degree-5 Classification (8 types, all resolvable by ≤ 1 swap) ✓

**Disproved:**
- Strict CDL (safe-swaps-only) ✗ — fails at n=6

**Computationally Verified (not proved):**
- All 5-colourings reduce to 4-colourings for n ≤ 9 (280K+ colourings)
- Distance bound d ≤ n-4 (tight for n=4..8, holds but not tight for n=9)
- Chain lifting for BFS paths (including (a,5)-swaps): 0 failures in 42K+ tests
- R(G,5) connected for n ≤ 9
- R(G,4) has 1 Fisk class for n ≤ 9

**Infrastructure:**
- 7 Python modules
- 23 tests (all passing)
- Multi-source BFS optimization (n=9 in 13s)
- Complete draft paper section

**One Open Gap:**
Prove that (a,5)-Kempe chains used by BFS-optimal paths in G-v don't merge in G when c(v) = 5.

### Decisions Made

1. **The project has converged.** Three iterations have progressively narrowed from "can we prove 4CT via Kempe swaps?" to ONE specific open question about (a,5)-chain merge avoidance. This is genuine mathematical progress.

2. **The draft paper section is the primary deliverable.** It documents everything: proofs, conjectures, computational evidence, and the open gap. It's ready for review and potential publication (with the gap marked).

3. **If another iteration is warranted:** it should focus exclusively on proving (or disproving) Conjecture 5.4 (chain merge avoidance for BFS paths). Approaches: structural characterization of when BFS paths use non-mergeable chains, or proof that degree-≤-5 vertices can't merge the specific chains BFS selects.

### Progress Score

**Iteration 1:** 5/10 (infrastructure + obstacle identification)
**Iteration 2:** 7/10 (CDL pivot + near-proof)
**Iteration 3:** 8.5/10 (chain lifting proved for {1,2,3,4}, gap reduced to one specific conjecture, n=9 verified, draft paper complete)

---

## Final Assessment (Iteration 3 / All Iterations)

**All streams:** Complete (3 iterations)
**Cross-stream integration:** Verified — exceptional alignment throughout
**Deliverable:** `deliverables/draft_paper_section.md` — complete mathematical document

**Craftsperson says:** Three iterations of sustained, rigorous work. We proved 5 lemmas, tested 280K+ colourings across 73 triangulations, and wrote a 10-section paper. The Chain Lifting Lemma for {1,2,3,4} pairs is a genuine result — trivial but transformative. The zero-merge observation is the strongest computational evidence we've produced.

**Skeptic says:** The (a,5)-gap is still open. "Zero failures in 42K tests" is compelling but not a proof. The tightness breaking at n=9 suggests our understanding is incomplete — the true distance bound might be sublinear, which would make the gap easier to close but also means our current bound is crude. Honest assessment: the gap might be as hard as 4CT itself. But the REFORMULATION (from 4CT to chain merge avoidance) is genuinely new and might be approachable by local combinatorial methods.

**Mover says:** We've built the most comprehensive computational study of Kempe reconfiguration for small planar graphs that I'm aware of. The theoretical framework is clean and nearly complete. The draft paper is publication-quality. If the gap closes, it's a constructive proof of 4CT. If it doesn't, it's a substantial contribution to graph colouring theory. Either way, this was a productive sprint.

---

*0050-C — 18 February 2026*
