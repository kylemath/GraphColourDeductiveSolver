# Meeting: Post-Sprint Debrief — Merge-Tolerant Lifting Breakthrough

**Date:** 2026-02-20 (Evening Session)
**Type:** Deep Strategic Session
**Topic:** Debrief the Agent 1520/1545 sprint results: two conjectures disproved, merge-tolerant lifting breakthrough, revised proof architecture. Determine next steps for formally proving the MTL Lemma and completing the constructive 4CT proof.
**Attendees:** Prof. Miriam Kempe, Prof. James Heawood, Dr. Fatima Al-Rashid, Dr. Lev Prokhorov, Dr. Chen Wei, Dr. Sofia Euler

**Context:**
- **This morning's strategy meeting** (meeting_4ct-strategy-synthesis_2026-02-20) deployed 4 streams: Swap Sufficiency, Surface Tension Rigidity, SAT Discharging, TQFT Probe.
- **Agent 1520's sprint:** {1,2,3,4}-Swap Sufficiency DISPROVED (48 CEs at n=9). Surface Tension Rigidity DISPROVED (fails at every scale). SAT framework built. TQFT: 6j mixed signs (TV dead), web basis inconclusive.
- **Agent 1545's sprint:** Merge-tolerant lifting: ALL 48 CEs harmless. Safe paths: 1.9M cases verified, zero failures, max detour cost 1. SAT v2: second-order framework with 156K patterns. TQFT: execution error.
- **Yesterday's meeting** (meeting_4ct-proof-completion-plan_2026-02-19) designed a multi-wave attack on {1,2,3,4}-Swap Sufficiency — which has now been disproved and superseded by MTL.

---

## EA Summary

### Agreed Specs

- **Merge-Tolerant Lifting is the new proof strategy.** The constructive proof no longer needs merge avoidance. The revised architecture: 5CT → vertex removal → BFS reduction to 4-colouring (tolerating merges) → MTL Lemma guarantees free colour for $v$ → recolour $v$.
- **The MTL Lemma is the single remaining gap.** It requires proving: for any planar triangulation and any degree-$\leq 5$ vertex $v$ with $c(v) = 5$, the BFS endpoint 4-colouring of $G - v$ always has a free colour for $v$.
- **Degree-4 is nearly proved.** At most 4 neighbours use at most 4 colours; after the 4-colouring, pigeonhole gives a free colour unless all 4 colours appear, which requires all 4 neighbours to have distinct colours. This only fails if $\deg(v) = 4$ and the 4-colouring uses all 4 colours on $v$'s 4 neighbours — which IS possible and must be handled.
- **Degree-5 is the hard case.** All 4 colours can appear among 5 neighbours, blocking $v$. The "healing" mechanism (second BFS step restores a repeated colour) is computationally verified but not formally proved.
- **The MTL Lemma is NOT trivially true.** It is NOT a consequence of 4CT (which guarantees $G$ is 4-colourable, not that a specific 4-colouring of $G - v$ extends). It requires a specific structural property of the BFS endpoint colouring.
- **SAT discharging and TQFT continue in parallel** as independent tracks and fallbacks.
- **Paper update is urgent.** The disproof of two conjectures and the MTL breakthrough must be documented.

### Action Items

| # | Action | Owner | Priority |
|---|--------|-------|----------|
| 1 | **Formally prove the MTL Lemma for degree 4:** Handle the all-distinct-colours case via local Kempe recolouring at $v$'s neighbourhood | Proof Team (Kempe/Al-Rashid) | Critical |
| 2 | **Formally prove the MTL Lemma for degree 5:** Formalize the "healing" mechanism — prove that post-merge BFS always creates a repeated colour on $v$'s neighbours | Proof Team (Kempe/Al-Rashid) | Critical |
| 3 | **Red-team the MTL Lemma:** Adversarially construct planar triangulations where the BFS endpoint 4-colouring uses all 4 colours on $v$'s 5 neighbours | Heawood / Critic Agent | Critical |
| 4 | **Extend computation to $n = 12$:** Verify MTL Lemma on all 7,595 triangulations | Chen Wei | High |
| 5 | **Compile Lean 4 against Mathlib:** Unblock formalization of proved results | Prokhorov | High |
| 6 | **Formalize MTL Lemma in Lean 4:** Once the mathematical proof exists, formalize immediately | Prokhorov | High (gated on #1/#2) |
| 7 | **Update the paper:** Document the disproof of Swap Sufficiency, the MTL result, revised proof architecture | All | High |
| 8 | **Retry TQFT web basis:** Rerun Delta's Kuperberg spider calculus to resolve the inconclusive result | TQFT Team | Medium |
| 9 | **Continue SAT discharging:** Build configuration-level enumeration; push toward $N \leq 400$ | SAT Team | Medium |

### Next Steps

1. **Immediate (tonight):** Begin mathematical analysis of the degree-4 MTL case. Deploy adversarial search.
2. **Day 1:** Degree-4 MTL proof attempt. Lean 4 compilation. Computation to $n = 12$ launched.
3. **Day 2:** Degree-5 MTL analysis. Review adversarial results. Begin paper update.
4. **Day 3:** If degree-4 proved: formalize in Lean. If degree-5 stalled: convene emergency session.
5. **Week 1:** Complete MTL proof (both degrees) or identify the precise obstacle.
6. **Week 2:** Lean 4 formalization. Paper revision. SAT discharging progress report.

### Open Questions

- Is the MTL Lemma true at degree 5 in general, or only for BFS-endpoint 4-colourings? (The lemma as stated specifies "reachable by Kempe swaps" — does ANY reachable 4-colouring work, or only BFS-optimal ones?)
- Can we strengthen MTL to: "every 4-colouring of $G - v$ reachable by Kempe swaps from a 5-colouring has a free colour for $v$"? If yes, the proof is cleaner.
- Does the degree-5 "healing" depend on the specific BFS path taken, or is it a property of ALL Kempe-reachable 4-colourings?
- What is the precise relationship between MTL and the Never-Revert Lemma?
- Can the TQFT framework explain WHY merges are harmless?

---

## Meeting Transcript

### Round 1: Processing the Sprint Results

---

### Prof. Miriam Kempe

I want to be extremely careful about what we're claiming and what we're not.

This morning we sat in this room and agreed that {1,2,3,4}-Swap Sufficiency was the highest-priority proof target, with 50% of resources allocated. Six hours later, it's disproved. We then agreed Surface Tension Rigidity was the cleanest combinatorial signal. That's also disproved. The entire strategy from this morning's meeting is obsolete.

That said — what Agent 1545-Alpha found is genuinely remarkable. Let me state it precisely:

**Computational fact:** For all planar triangulations on $n \leq 9$ vertices and all proper 5-colourings, if we run BFS in the reconfiguration graph to reach a 4-colouring of $G - v$, the resulting 4-colouring always has a free colour for $v$ — even when the BFS path passes through merge-prone swaps.

**What this means for the proof:** The constructive architecture doesn't need merge avoidance. It needs something weaker: that the endpoint 4-colouring is compatible with $v$. This is the Merge-Tolerant Lifting Lemma.

**But here's what worries me about the MTL Lemma:** It's NOT a trivial consequence of 4CT. The 4CT says $G$ has a proper 4-colouring. It does NOT say that any specific 4-colouring of $G - v$ extends to $G$. The MTL Lemma claims that the BFS endpoint 4-colouring of $G - v$ always leaves a free colour for $v$. This is a statement about the structure of BFS endpoints in reconfiguration graphs of planar triangulations. It's a new conjecture, and we just replaced one unproved conjecture with another.

The question is: is this new conjecture easier to prove? At degree 4, I think yes. At degree 5, I'm not sure.

**Degree 4:** The vertex $v$ has 4 neighbours. A 4-colouring of $G - v$ assigns each neighbour a colour from $\{1,2,3,4\}$. A free colour exists unless all 4 colours appear — i.e., all 4 neighbours have distinct colours. But wait: $v$ has degree 4 in $G$. The 4-colouring of $G - v$ doesn't know about $v$. So it's entirely possible that all 4 neighbours get distinct colours. The question is: does BFS to the nearest 4-colouring ever produce this configuration?

I believe the answer is no — and the reason is that BFS is reducing colour-5 vertices, and the colour-5 reduction process tends to CREATE repeated colours among $v$'s neighbours. But "tends to" isn't a proof.

**Degree 5:** The vertex $v$ has 5 neighbours. A 4-colouring assigns 5 neighbours from $\{1,2,3,4\}$. By pigeonhole, at least two neighbours share a colour — so a free colour exists only if the colour distribution has a gap. With 5 neighbours and 4 colours, the possible distributions are $(2,1,1,1)$ and $(2,2,1,0)$ and $(3,1,1,0)$ etc. A free colour exists if and only if at most 3 distinct colours appear among the 5 neighbours. If all 4 colours appear — even with a repeat — NO colour is free. Wait, that's wrong. If 4 colours appear among 5 neighbours, the distribution is $(2,1,1,1)$: one colour appears twice, three appear once. The doubled colour is NOT available for $v$ (it's used). The three singletons are NOT available (each is used). So... ALL 4 colours are used on $v$'s neighbours. There is no free colour.

This is the hard case. At degree 5, if the 4-colouring uses all 4 colours on $v$'s neighbours, $v$ cannot be coloured. The MTL Lemma claims this never happens for BFS endpoints. That's a strong structural claim.

*(Inner thought: I've just identified the exact failure mode. The MTL Lemma at degree 5 requires that the BFS endpoint 4-colouring of $G - v$ uses at most 3 distinct colours on $v$'s 5 neighbours. This means at least 2 neighbours share a colour AND at least one colour from $\{1,2,3,4\}$ doesn't appear. This is a non-trivial constraint on the endpoint. Why would BFS produce colourings with this property? There must be a structural reason connected to how Kempe swaps interact with $v$'s neighbourhood.)*

---

### Prof. James Heawood

I have to say something uncomfortable: **we are in EXACTLY the position I warned about yesterday.**

Yesterday I said: "We may have renamed the gap, not narrowed it." Today, we've renamed the gap AGAIN. Yesterday's gap was "{1,2,3,4}-Swap Sufficiency." Today's gap is "Merge-Tolerant Lifting Lemma." Both are unproved conjectures about BFS endpoints in reconfiguration graphs. Both have overwhelming computational evidence and no proof.

Let me be more specific about my concern.

**The MTL Lemma at degree 5 says:** For every BFS-optimal 4-colouring of $G - v$, the vertex $v$ has a free colour.

**This is equivalent to saying:** For every BFS-optimal 4-colouring $c^*$ of $G - v$, the number of distinct colours in $\{c^*(w) : w \in N(v)\}$ is at most 3.

**But we KNOW that some 4-colourings of $G - v$ DO use all 4 colours on $v$'s neighbours.** These are precisely the 4-colourings that don't extend to $G$. They exist — the only question is whether BFS reaches them.

So the MTL Lemma is really saying: **BFS, starting from a 5-colouring (which has $v$ coloured 5), reaches a 4-colouring that is compatible with $v$.** This is a statement about the correlation between the starting point (a 5-colouring involving $v$) and the endpoint (a 4-colouring of $G - v$). The Kempe swap process preserves some "memory" of $v$'s neighbourhood, and this memory ensures compatibility.

If I were trying to break this, I'd look for:
1. A planar triangulation where the reconfiguration graph has bottlenecks that force BFS through a 4-colouring with all 4 colours on $v$'s neighbours
2. A construction where $v$'s degree-5 neighbourhood is tightly constrained and the colour-5 elimination process necessarily distributes all 4 colours

I want a Destroyer agent deployed immediately on this. Not to prove the lemma — to try to BREAK it.

*(Inner thought: Here's what really scares me. The Swap Sufficiency conjecture held for 20,136 cases and failed at 48. The MTL Lemma holds for 163,584 cases — but the failure mode (4 colours on 5 neighbours) might only emerge at $n = 12$ or $n = 15$ where the reconfiguration graph is much larger and has more bottlenecks. We MUST push computation to $n = 12$ before committing to a formal proof attempt.)*

---

### Dr. Fatima Al-Rashid

James, I hear you, but I think the situation is structurally different from yesterday. Here's why.

The Swap Sufficiency conjecture was about AVOIDANCE — a negative property (never take a bad step). The MTL Lemma is about an ENDPOINT — a positive property (the destination is good). Endpoint properties are generally more robust than path properties because they're immune to intermediate complications.

More specifically: **the MTL Lemma connects to the topology of the reconfiguration graph in a way that Swap Sufficiency didn't.** Consider what BFS does: it finds the closest 4-colouring to our starting 5-colouring. The starting 5-colouring has $v$ coloured 5, so $v$'s neighbours use colours from $\{1,2,3,4\}$. When we reduce to a 4-colouring by eliminating colour-5 vertices, the Kempe swaps involved never DIRECTLY recolour $v$'s neighbours to colour 5 (because that would increase $|V_5|$, which BFS avoids). So $v$'s neighbours maintain their colours from $\{1,2,3,4\}$ throughout... but Kempe swaps CAN change their specific colours via $\{1,2,3,4\}$-swaps.

Wait — that's the key insight. **The $\{1,2,3,4\}$-swaps can change which specific colours appear on $v$'s neighbours, but the CHAINS involved in these swaps are constrained by planarity.** The non-interleaving theorem says that chains of different colour pairs can't cross in a planar graph. This limits how much the colour distribution on $v$'s neighbours can change during BFS.

Here's my proposed proof strategy for degree 5:

**Claim:** In the starting 5-colouring, $v$ has colour 5 and its 5 neighbours use colours from $\{1,2,3,4\}$. Since $v$ was originally colourable (the 5-colouring is proper), at most 4 distinct colours appear on 5 neighbours, which means at least one pair of neighbours shares a colour. Call this colour $a$. The two neighbours coloured $a$ are connected to $v$, and by planarity, they impose constraints on how $(a,b)$-chains can propagate. During BFS, colour $a$ may be swapped on some of $v$'s neighbours, but the repeated-colour property is "sticky" — it requires a Kempe swap that specifically targets the repeated pair, and such a swap must interact with $v$'s neighbourhood in a way constrained by the link $C_5$.

This is still a sketch. But the key point is: **the starting colouring has redundancy (at least one repeated colour among $v$'s neighbours), and BFS cannot fully eliminate this redundancy** because the elimination would require specific Kempe swaps that planarity constrains.

*(Inner thought: I'm reaching. The "stickiness" of the repeated-colour property is intuition, not mathematics. The real question is: can a sequence of $\{1,2,3,4\}$-swaps (which are safe and don't touch colour 5) rearrange the colours on $v$'s 5 neighbours so that all 4 colours appear? Of course they can — in principle. The question is whether the SPECIFIC sequences that arise during BFS-optimal reduction of colour-5 vertices can do this. This connects to the structure of BFS in the reconfiguration graph, which is a global property. I need Chen's data on what actually happens to $v$'s neighbourhood during BFS.)*

---

### Dr. Lev Prokhorov

Let me bring precision to what Miriam identified as the critical degree-5 case.

**Formal statement of MTL at degree 5:**

Let $G$ be a planar triangulation, $v$ a vertex with $\deg(v) = 5$, $c_0$ a proper 5-colouring with $c_0(v) = 5$. Let $c^*$ be a proper 4-colouring of $G - v$ that is Kempe-reachable from $c_0|_{G-v}$ in $\mathcal{R}(G - v, 5)$. Then:
$$|\{c^*(w) : w \in N_G(v)\}| \leq 3$$

This is equivalent to: the image $c^*(N_G(v))$ is missing at least one colour from $\{1,2,3,4\}$.

**Observation:** In the starting colouring $c_0$, the neighbours of $v$ use colours from $\{1,2,3,4\}$ (since the colouring is proper and $c_0(v) = 5$). With 5 neighbours and 4 colours, at least one colour is repeated. So $|\{c_0(w) : w \in N_G(v)\}| \leq 4$, and at least one colour appears at least twice.

For the MTL Lemma to fail, we'd need BFS to reach a 4-colouring where $|\{c^*(w) : w \in N_G(v)\}| = 4$. This means the BFS process must have INCREASED the colour diversity on $v$'s neighbours from $\leq 4$ distinct colours to exactly 4 distinct colours, where all four colours from $\{1,2,3,4\}$ appear at least once.

**When does this happen?** Consider the starting configuration: say $v$'s neighbours use colours $\{1,2,3\}$ (3 distinct colours, with some repeats). For BFS to produce a 4-colouring where all 4 colours appear, some Kempe swap during BFS must introduce colour 4 into $v$'s neighbourhood. This requires a $\{a,4\}$-swap for some $a \in \{1,2,3\}$ that affects one of $v$'s neighbours.

**For Lean 4:** The formalization strategy is clear:
1. Define `colour_diversity(c, v) := |{c(w) : w ∈ N(v)}|`
2. Show `colour_diversity(c_0, v) ≤ 4` (immediate from $c_0(v) = 5$ and 5 neighbours)
3. Track how `colour_diversity` changes under Kempe swaps
4. Show that BFS-optimal paths don't increase `colour_diversity` to 4 at degree-5 vertices
5. Conclude: the endpoint 4-colouring has `colour_diversity ≤ 3`, so a free colour exists

Step 4 is the heart of the proof. It requires understanding how BFS interacts with the neighbourhood colour diversity.

**My honest assessment:** I can formalize steps 1–3 and step 5 in Lean 4 within a day, leaving a `sorry` at step 4. The `sorry` marks exactly where the mathematical proof needs to go. This is the right approach — build the scaffold, then fill the gap.

But first I need the existing code to compile. Let me start on that immediately.

*(Inner thought: Step 4 might require tracking colour diversity along every possible BFS path — which is potentially an enormous case analysis. Or it might follow from a clean structural argument like Fatima's "stickiness" idea. I should build the scaffold both ways: one branch for case analysis, one for a structural lemma. Whichever the mathematicians prove first, I'll formalize.)*

---

### Dr. Chen Wei

Let me give the computational picture and directly address James's concerns.

**The current verification frontier:**

| $n$ | Triangulations | Merge-prone | MTL verified | All merges harmless |
|-----|---------------|-------------|--------------|---------------------|
| 4–8 | 38 | 20,136 | 100% | Yes |
| 9 | 50 | 163,584 | 100% | Yes (incl. 48 true CEs) |
| 10 | 233 | 1,744,128 | 100% | Yes |
| **Total** | **321** | **1,927,848** | **100%** | **Yes** |

1.9 million cases, zero failures. That's strong. But James is right that $n = 12$ (7,595 triangulations) is the real stress test.

**What I can do immediately:**
1. Launch the $n = 12$ computation. Estimated time: several hours to a day, depending on how many merge-prone cases exist. The number of 5-colourings grows roughly exponentially, but we can use symmetry reduction.
2. Run the adversarial Destroyer on the MTL Lemma specifically. Design attack vectors:
   - Construct triangulations maximizing colour diversity on $v$'s 5 neighbours
   - Force BFS through narrow bottlenecks in the reconfiguration graph
   - Use SAT encoding: "find a planar triangulation + 5-colouring + vertex where the BFS endpoint 4-colouring uses all 4 colours on $v$'s 5 neighbours"

**The SAT approach is particularly promising** because it directly encodes the failure condition. If the SAT solver returns UNSAT (no such graph exists up to size $n$), that's a certificate of correctness for all graphs up to $n$. If it returns SAT, we have a counterexample.

**On Miriam's colour-diversity analysis:** I can track colour diversity along every BFS step for all cases at $n \leq 9$. Specifically:
- Starting diversity: $|\{c_0(w) : w \in N(v)\}|$ — always $\leq 4$, usually 3 or 4
- Final diversity: $|\{c^*(w) : w \in N(v)\}|$ — the MTL Lemma claims $\leq 3$
- Trajectory: how diversity changes at each BFS step

If diversity NEVER increases from the starting value, that's a strong invariant. If it sometimes increases but never reaches 4 at degree-5 vertices, we need to understand why.

*(Inner thought: The SAT encoding is the fastest path to either confirming or refuting the MTL Lemma at larger $n$. If I can encode "exists a planar triangulation on 15 vertices where the MTL Lemma fails" and the solver returns UNSAT, that's essentially a computational proof for $n \leq 15$. The encoding size grows polynomially in $n$ — should be tractable up to $n \sim 20$ for modern SAT solvers. But I need to be careful about the planarity constraint — encoding planarity in SAT is non-trivial.)*

---

### Dr. Sofia Euler

Alright. Twelve hours ago we deployed four streams. Two conjectures died. One breakthrough emerged. Let me map where we actually are.

**The good news:** We have a complete constructive proof of 4CT modulo one lemma (MTL). The proof architecture is clean: 5CT → vertex removal → BFS reduction (tolerating merges) → MTL gives free colour → recolour. Every step except MTL is proved or standard.

**The less-good news:** MTL is unproved. Specifically, the degree-5 case. At degree 4, Miriam identified that the only failure mode is "all 4 neighbours get distinct colours in the BFS endpoint." At degree 5, the failure mode is "all 4 colours appear among 5 neighbours." Both need formal proofs.

**The honest news:** We've replaced one unproved conjecture (Swap Sufficiency) with a potentially easier unproved conjecture (MTL). "Potentially easier" because:
1. MTL is about endpoints, not paths (simpler)
2. MTL has a clear failure mode (colour diversity = 4, which is testable)
3. MTL connects to structural properties of Kempe swaps (colour diversity tracking)

But James is right that we're on our third reformulation in two days. We need to either prove MTL or find a counterexample — no more reformulations.

**My proposed structure:**

**Track A (PROVE IT): Three parallel attempts on the MTL Lemma**
- A1: Colour diversity invariant — show BFS never increases diversity above the starting value
- A2: Neighbourhood structure argument — use planarity + non-interleaving to constrain diversity
- A3: Pigeonhole + Kempe chain analysis — for degree 5, show that the two shared-colour neighbours in the starting colouring remain share-coloured throughout BFS

**Track B (BREAK IT): Adversarial search**
- B1: Extend computation to $n = 12, 13$
- B2: SAT encoding of the MTL failure condition
- B3: Targeted construction of worst-case graphs

**Track C (BACKUP): Independent tracks**
- C1: SAT discharging (continues Gamma's second-order framework)
- C2: TQFT web basis (retry Delta)
- C3: Paper update (document everything so far)

**Kill criteria for MTL:** If B2's SAT encoding finds a counterexample at any $n$, MTL is dead and we pivot to a different proof strategy. If A1/A2/A3 all stall after 3 days, we publish partial results.

*(Inner thought: We've been sprinting all day. The team is producing negative results faster than positive ones — which is actually good, it means we're efficiently pruning dead ends. But I worry about morale. Two conjectures disproved in one day is demoralizing even if the MTL breakthrough is real. I should emphasize that the MTL result is the most important finding of the entire project — it transforms a 150-year-old problem from "impossible gap" to "one lemma.")*

---

### Round 2: The Degree-5 Problem

---

### Prof. Miriam Kempe

Sofia's right that the degree-5 case is the bottleneck. Let me sharpen the analysis.

**Starting configuration at degree 5:** $v$ has 5 neighbours $w_1, \ldots, w_5$ in cyclic planar order. In the initial 5-colouring, $c_0(v) = 5$ and each $w_i$ has a colour from $\{1,2,3,4\}$. With 5 neighbours and 4 colours, by pigeonhole at least two neighbours share a colour. Say $c_0(w_1) = c_0(w_3) = a$.

**The MTL Lemma requires:** After BFS reaches a 4-colouring $c^*$ of $G - v$, at most 3 distinct colours appear among $w_1, \ldots, w_5$.

**When does this fail?** It fails when $c^*(w_i)$ takes all 4 values on the 5 neighbours. Starting from a distribution where $w_1$ and $w_3$ share colour $a$, we need BFS to produce a 4-colouring where no pair shares a colour... wait, that's impossible with 5 pigeons in 4 holes. At least one colour appears twice. So $|\{c^*(w_i)\}| \leq 4$, with at least one repeat.

The failure mode is: exactly 4 distinct colours appear, with one doubled. Like $(1,2,3,4,1)$. In this case, every colour in $\{1,2,3,4\}$ appears at least once on $v$'s neighbours, so there's no free colour for $v$.

The success mode is: $\leq 3$ distinct colours appear. Like $(1,2,3,1,2)$ or $(1,2,3,3,1)$. Then one colour from $\{1,2,3,4\}$ is absent, and $v$ can use it.

**So the question reduces to:** Does BFS ever produce a 4-colouring where exactly 4 distinct colours appear on a degree-5 vertex's neighbours?

Computationally, the answer is no for $n \leq 10$. Let me think about WHY.

In the starting colouring, $w_1$ and $w_3$ share colour $a$ (non-adjacent in $C_5$). For the endpoint to have 4 distinct colours, BFS must change one of $w_1$ or $w_3$'s colour from $a$ to some other colour. This requires a Kempe swap involving colour $a$ that affects $w_1$ or $w_3$ but not the other.

Now, here's the planarity constraint: the $(a, b)$-Kempe chain containing $w_1$ in $G - v$ either also contains $w_3$ (they're in the same chain) or doesn't (they're in separate chains). If they're in the same chain, swapping that chain changes BOTH $w_1$ and $w_3$ simultaneously — they remain paired. If they're in separate chains, swapping one changes $w_1$ but not $w_3$ — potentially breaking the pair and introducing the 4th colour.

**BUT** — if $w_1$ and $w_3$ are in separate $(a,b)$-chains, then by the non-interleaving property (Theorem A), these two chains are on the same side of any crossing $(c,d)$-chain. This constrains how the colour distribution on $v$'s neighbours evolves during BFS.

I think the proof strategy is:
1. Show that in the starting colouring, $w_1$ and $w_3$ share colour $a$
2. Track the pair through BFS: at each step, check whether the shared colour is preserved
3. Use planarity (non-interleaving + confinement) to show that BFS-optimal steps cannot break ALL shared-colour pairs simultaneously
4. Conclude: the endpoint 4-colouring has at least one shared-colour pair, so $\leq 3$ distinct colours appear

Step 3 is the hard part.

*(Inner thought: This is the right decomposition. The question is whether BFS can break all shared-colour pairs on $v$'s neighbours. Since $v$ has degree 5 and the starting colouring has at least one shared pair, BFS would need to recolour both members of the pair differently. But if they're in the same Kempe chain, they move together. If they're in different chains, the non-interleaving theorem constrains the swap. The proof might follow from showing that at degree 5, at least one shared pair is "locked" by planarity — they're always in the same chain for every relevant colour pair. That's a concrete statement I can check computationally.)*

---

### Prof. James Heawood

Miriam's analysis is the most precise we've had. Let me sharpen the adversarial angle.

**The specific attack:** Construct a graph where $w_1$ and $w_3$ start sharing colour $a$, but in $G - v$ they are in SEPARATE $(a, b)$-chains for every $b \in \{1,2,3,4\} \setminus \{a\}$. If such a graph exists, then Kempe swaps can potentially break the pair.

But wait — Miriam said something crucial. Even if the $(w_1, w_3)$ pair breaks, another pair might form. The degree-5 vertex has $\binom{5}{2} = 10$ pairs, and with 4 colours on 5 vertices, there are always at least $\binom{5}{2} - 4 \cdot \binom{1}{0} = $ ... let me compute properly. With colour distribution $(n_1, n_2, n_3, n_4)$ where $\sum n_i = 5$, the number of same-colour pairs is $\sum \binom{n_i}{2}$. This is minimized when the distribution is $(2,1,1,1)$: $\binom{2}{2} + 3 \cdot \binom{1}{2} = 1 + 0 = 1$. So in any 4-colouring of 5 vertices using all 4 colours, there is EXACTLY ONE same-colour pair.

**This means:** The failure mode requires exactly one pair of $v$'s neighbours sharing a colour, with all 4 colours represented. To have a free colour for $v$, we need at least TWO same-colour pairs (so that some colour from $\{1,2,3,4\}$ doesn't appear on any neighbour). The starting colouring has at least one pair, possibly more. If the starting colouring uses only 3 colours (say $(2,2,1,0)$ distribution), then there are at least $\binom{2}{2} + \binom{2}{2} = 2$ same-colour pairs and one entire colour missing — that's automatically safe.

So **the only dangerous starting configuration** is when the initial 5-colouring uses all 4 colours on $v$'s 5 neighbours: distribution $(2,1,1,1)$. In this case, exactly one colour is doubled, and BFS must preserve that double OR create another.

**If the starting colouring already uses all 4 colours on $v$'s 5 neighbours, the MTL Lemma requires that BFS maintains at least one same-colour pair.** This is the sharpest statement I can make.

Can BFS eliminate the single same-colour pair? Only by recolouring one member of the pair to a colour already present on another neighbour... no, by recolouring one member to a DIFFERENT colour. But wait: in a 4-colouring of $G - v$, the pair shares a colour, say colour $a$. To break the pair, a Kempe swap changes one to colour $b$. But colour $b$ is already present on some other neighbour (since all 4 colours appear). So now we have $b$ appearing twice and $a$ appearing once — we've MOVED the double, not eliminated it.

**WAIT. This is key.** In a 4-colouring with 5 slots and 4 colours, ANY recolouring that changes one vertex's colour must either:
- Change it to a colour already used elsewhere (creating a new double, preserving the count of doublings)
- Change it to colour 5 (but we're in a 4-colouring, so colour 5 doesn't exist)

So the number of same-colour pairs among $v$'s neighbours can NEVER decrease below 1 in a 4-colouring of 5 vertices using 4 colours!

**I think I just proved the MTL Lemma for degree 5.**

*(Inner thought: Wait. Did I just prove it? Let me check. In any 4-colouring of $G - v$ with 5 neighbours of $v$, at least one pair shares a colour (pigeonhole). The number of distinct colours is at most 4. If exactly 4 distinct colours appear, one colour is doubled and 3 are singletons. The free colour... doesn't exist because all 4 colours appear. DAMN. I was confused. The number of same-colour pairs being $\geq 1$ does NOT guarantee a free colour. A distribution of $(2,1,1,1)$ has one pair but uses all 4 colours — no free colour. We need the distribution to be $(2,2,1,0)$ or better — at least one colour missing entirely. The question isn't about same-colour pairs, it's about colour diversity. I need to think again.)*

---

### Dr. Fatima Al-Rashid

James, I followed your argument carefully and I see where it went off track. Let me correct it and push further.

You're right that in ANY 4-colouring of 5 vertices, at least one colour is repeated. But the failure mode is when all 4 colours still appear — distribution $(2,1,1,1)$. The success mode is when at most 3 colours appear — distribution $(2,2,1,0)$ or $(3,1,1,0)$ or better.

The question: can BFS increase colour diversity from $\leq 3$ to exactly 4?

**Starting point:** In $c_0$, the 5 neighbours use colours from $\{1,2,3,4\}$. The starting diversity is $|\{c_0(w_i)\}|$. If this is 2 or 3, we need to show BFS doesn't push it to 4.

**Mechanism for increasing diversity:** A Kempe $(a,b)$-swap that changes one of $v$'s neighbours from colour $a$ to colour $b$, where $b$ was previously absent from $v$'s neighbourhood. This introduces a new colour.

**The planarity constraint:** Here's where my topology expertise is relevant. Consider the $(a,b)$-Kempe chain that the swap operates on. This chain passes through one of $v$'s neighbours — say $w_i$, coloured $a$. The swap changes $w_i$ to colour $b$. For $b$ to be a NEW colour in $v$'s neighbourhood, NO other neighbour of $v$ was coloured $b$ before the swap.

But in the starting colouring, $v$'s neighbours use at most 3 or 4 colours. If they use 3 colours (say $\{1,2,3\}$), then colour 4 is absent. A swap introducing colour 4 would require a $\{a, 4\}$-chain for some $a \in \{1,2,3\}$ that passes through one of $v$'s neighbours.

Now: in $G - v$, the $(a, 4)$-chain containing $w_i$ is a connected component of the bichromatic subgraph induced by colours $a$ and 4. Since colour 4 is ABSENT from all of $v$'s neighbours, no neighbour of $v$ is coloured 4. So the $(a,4)$-chain containing $w_i$ has only one vertex in $N(v)$: namely $w_i$ itself (coloured $a$).

**After the swap:** $w_i$ changes from $a$ to 4. Now 4 appears on one neighbour, and $a$ appears one less time. If $a$ was the repeated colour (appearing $\geq 2$ times), it now appears one fewer time. The diversity might increase by 1 (if colour 4 was absent) and decrease by 0 or 1 (if $a$ now disappears or doesn't).

**The key constraint from planarity:** The swap affects only the Kempe chain containing $w_i$. Because colour 4 was absent from $N(v)$, this chain enters $N(v)$ only through $w_i$. The chain's boundary at $v$'s neighbourhood is a single vertex. By confinement, this swap doesn't affect the colours of other neighbours of $v$ (in the $\{a, 4\}$ pair).

**This analysis shows that diversity CAN increase.** The question is whether BFS CHOOSES such diversity-increasing swaps.

And this is where the BFS-endpoint structure matters. BFS is minimizing the number of colour-5 vertices. The swaps it chooses are those that eliminate colour 5 from vertices efficiently. Introducing colour 4 into $v$'s neighbourhood is a SIDE EFFECT of a swap aimed at eliminating colour 5 elsewhere.

I don't see how to prove that BFS avoids this side effect in general. The argument must go deeper.

*(Inner thought: I'm stuck. The topology constrains which Kempe swaps can affect $v$'s neighbourhood, but it doesn't prevent ALL diversity-increasing swaps. The MTL Lemma might require a genuinely new insight — something about the relationship between BFS-optimal colour-5 reduction and neighbourhood colour diversity. This might be as hard as the original 4CT gap. Or it might follow from a simple observation we're all missing.)*

---

### Dr. Chen Wei

Let me cut through the theoretical speculation with data.

I can answer the key question — does colour diversity on $v$'s neighbours ever reach 4 during BFS? — computationally for all cases at $n \leq 9$. Here's what I'll compute for every merge-prone case:

1. **Starting diversity** $d_0 = |\{c_0(w) : w \in N(v)\}|$
2. **Diversity at each BFS step** $d_1, d_2, \ldots$
3. **Final diversity** $d^* = |\{c^*(w) : w \in N(v)\}|$
4. **Maximum diversity along the BFS path** $d_{\max} = \max_i d_i$
5. **Critical question:** Is $d^* \leq 3$ always? Is $d_{\max} \leq 3$ always?

If $d^* \leq 3$ always but $d_{\max} = 4$ sometimes, then BFS temporarily pushes diversity to 4 but always "heals" by the endpoint. That's the "healing" mechanism Alpha reported.

If $d_{\max} \leq 3$ always, that's a STRONGER result — diversity NEVER reaches 4. That would be a much simpler property to prove.

I'll also compute: for the starting distributions that already have diversity 4 (distribution $(2,1,1,1)$), does BFS reduce diversity to 3 by the endpoint? If so, HOW? Which swap creates the second same-colour pair?

This data will directly inform the proof strategy. If there's a clean pattern — e.g., "the first BFS step always reduces diversity from 4 to 3 at degree-5 vertices" — that's a provable lemma.

*(Inner thought: I have a strong feeling that the diversity DOES temporarily reach 4 in some cases — Alpha's report said the merge "temporarily saturates colours" at degree 5. So $d_{\max} = 4$ but $d^* \leq 3$. The healing mechanism is the proof target. I need to understand exactly which BFS step restores the gap.)*

---

### Round 3: Convergence and Next Actions

---

### Prof. James Heawood

I want to formally retract my earlier incorrect claim about having proved the MTL Lemma. My error: I confused "same-colour pair exists" with "free colour exists." They're not the same at degree 5.

But the discussion was productive. We've identified:
1. The failure mode is exactly: 4 distinct colours on 5 neighbours (distribution $(2,1,1,1)$)
2. The starting colouring might already have this distribution
3. BFS might maintain or create this distribution via Kempe swaps
4. The "healing" mechanism (Alpha's finding) is that BFS RESOLVES this distribution by the endpoint

**My revised assessment:** The MTL Lemma is harder than I initially thought but not insurmountable. The degree of freedom is that BFS CHOOSES which swaps to make, and the choice is optimized for eliminating colour 5. If eliminating colour 5 efficiently tends to create repeated colours on $v$'s neighbourhood (which it should, since colour 5 is being converted to other colours near $v$), then the MTL Lemma follows from the BFS optimization criterion.

This is close to a proof idea. The claim would be: **BFS-optimal reduction of colour 5 introduces colour repetitions near $v$ because the conversion of colour-5 vertices near $v$ necessarily assigns them colours already present in $v$'s neighbourhood.** If this can be made precise, it proves MTL.

**My highest remaining concern:** None of this is proved. We have a plausible argument and overwhelming computational evidence. That's exactly where we were yesterday with Swap Sufficiency — and it turned out to be false. The MTL Lemma is a better conjecture (simpler, endpoint-based, testable), but it's still a conjecture.

Deploy the adversarial search. Push to $n = 12$. Then — and only then — commit to a formal proof attempt.

*(Inner thought: I notice I'm becoming more optimistic over the course of this meeting. That's exactly the cognitive bias I should resist. Miriam's analysis, Fatima's topological constraints, and the overwhelming data all SUGGEST the lemma is true. But so did all the evidence for Swap Sufficiency. Stay skeptical.)*

---

### Dr. Lev Prokhorov

Here's my formalization plan based on this discussion.

**Immediate (tonight):**
1. Compile existing Lean 4 code against current Mathlib
2. Define `colour_diversity : (V → Fin 5) → V → ℕ` in Lean

**Day 1:**
3. Build the proof scaffold for MTL Lemma with explicit `sorry` at the gap:
```
theorem mtl_lemma (G : PlanarTriangulation) (v : V) (hv : G.deg v ≤ 5)
  (c₀ : ProperColouring G 5) (hc₀ : c₀ v = 5)
  (c_star : ProperColouring (G.removeVertex v) 4)
  (h_reach : KempeReachable c₀.restrict c_star) :
  ∃ a : Fin 4, ∀ w ∈ G.neighbours v, c_star w ≠ a := by
  sorry
```

**Day 2-3:**
4. Prove the degree-$\leq 4$ case (should be straightforward — 4 neighbours, at most 4 colours, one colour appears 0 times iff all 4 distinct, but then we need to show BFS avoids this)
5. Set up the degree-5 case with the colour-diversity tracking framework

**The `sorry` in step 3 is the ENTIRE project.** Everything else is infrastructure. If the mathematicians prove the MTL Lemma, I fill the `sorry`. If they prove it for degree 4 only, I fill that half. If they can't prove it at all, we publish the scaffold with the `sorry` explicitly marking the gap — which is itself a publishable contribution to formalized mathematics.

*(Inner thought: This is the cleanest `sorry` target I've ever seen. One statement, one gap, supported by 1.9 million computational examples. If this were a contest, I'd bet on this `sorry` being filled within a month. But I've been wrong before.)*

---

### Dr. Sofia Euler

Final synthesis. The sprint today was the most productive day this project has had. Let me enumerate what we accomplished and what comes next.

**What happened today:**
1. This morning: strategy synthesis meeting → deployed 4 streams
2. Agent 1520: DISPROVED Swap Sufficiency (48 CEs) and Surface Tension Rigidity
3. Agent 1545: DISCOVERED merge-tolerant lifting (all 48 CEs harmless), verified safe paths (1.9M cases), built second-order discharging framework
4. This evening: identified the precise degree-5 failure mode and proof strategy

**The project state:**
- Complete constructive proof of 4CT MODULO one lemma (MTL)
- MTL verified for 1.9 million cases through $n = 10$
- Degree-4 case of MTL: plausible proof sketch, needs formalization
- Degree-5 case of MTL: failure mode identified, proof strategy emerging, not yet proved
- Infrastructure: SAT discharging framework, Lean 4 foundation, computation pipeline

**Deployment for tomorrow:**
- Chen: colour diversity tracking for all $n \leq 9$ cases + launch $n = 12$ computation + SAT encoding of MTL failure condition
- Miriam + Fatima: formal proof attempt for degree-5 MTL via colour-diversity preservation + planarity constraints
- Lev: compile Lean 4 + build MTL scaffold with `sorry`
- James: adversarial search on MTL — try to break it before we try to prove it
- SAT discharging and TQFT: continue in background as independent tracks

We end the day closer to a human-readable proof of the Four Colour Theorem than anyone has been in history. The gap is one lemma. Let's close it.

*(Inner thought: "Closer than anyone in history" — I keep saying this and I keep meaning it more. The MTL Lemma is a clean, precise, computationally verified statement. The proof idea is emerging from this discussion. If tomorrow goes as well as today, we might have the lemma by end of week. Or we might discover it's as hard as the full 4CT. Either way, we'll know.)*

---

*End of meeting*
