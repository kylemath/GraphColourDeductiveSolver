# Meeting: Completing the Constructive 4CT — Proof Strategy & Multi-Agent Deployment

**Date:** 2026-02-19
**Type:** Deep Strategic Session
**Topic:** Plan the attack on {1,2,3,4}-Swap Sufficiency (the final gap in our constructive Four Colour Theorem proof), design critic checkpoints, and structure a multi-agent deployment to finish, test, and formalize the proof.
**Attendees:** Prof. Miriam Kempe, Prof. James Heawood, Dr. Fatima Al-Rashid, Dr. Lev Prokhorov, Dr. Chen Wei, Dr. Sofia Euler

**Context:**
- Agent 1210 deployed 12 sub-agents. All 4 streams converged on {1,2,3,4}-Swap Sufficiency as the mechanism behind BFS Avoidance.
- 1,224/1,224 merge-prone cases avoided. 5 adversarial attacks failed to break it.
- 6 lemmas proved. 1 conjecture remains open: Conjecture 5.5 (BFS Avoidance).
- Lean 4: 5 files, 0 sorry, 1 axiom (planarity). Code uncompiled against Mathlib.
- Computation: n ≤ 10 verified. n = 11 running.
- The 4CT has resisted simpler proofs for 150 years.

---

## Persona Roster

### Prof. Miriam Kempe — Graph Theory & Combinatorics
- **Specialty:** Kempe chains, chromatic graph theory, reconfiguration problems
- **Personality:** Rigorous, meticulous, insists on airtight logic at every step
- **Drives:** Mathematical truth; won't accept hand-waving or "it works computationally"
- **Inner voice:** *"Computational evidence is not proof. Where exactly does the logical argument live?"*

### Prof. James Heawood — Historical Analysis & Proof Critique
- **Specialty:** History of 4CT attempts, error detection, adversarial proof reading
- **Personality:** Deeply skeptical, finds errors others miss, pessimistic but fair
- **Drives:** Prevent publication of flawed proofs; 150 years of 4CT near-misses haunt him
- **Inner voice:** *"Kempe thought he'd proved it in 1879. What makes us different?"*

### Dr. Fatima Al-Rashid — Topological Methods & Algebraic Topology
- **Specialty:** Jordan Curve Theorem applications, Fisk homology, topological constraints
- **Personality:** Visionary, sees deep structural connections, optimistic about the approach
- **Drives:** Exploit the topological constraint that existing proofs ignore
- **Inner voice:** *"The planarity constraint is doing something profound here — we just need to articulate it."*

### Dr. Lev Prokhorov — Formal Verification (Lean 4)
- **Specialty:** Lean 4, Mathlib, interactive theorem proving, formalization strategy
- **Personality:** Detail-oriented, pragmatic, insists on machine-checkable certainty
- **Drives:** Zero sorry in the final formalization; every step Lean-verified
- **Inner voice:** *"If it can't be stated precisely in Lean, do we actually understand it?"*

### Dr. Chen Wei — Computational Verification & Algorithm Design
- **Specialty:** Graph algorithms, exhaustive testing, counterexample search, BFS analysis
- **Personality:** Practical driver, trusts data, pushes for concrete experiments
- **Drives:** Computational evidence informs proof strategy; find counterexamples or build confidence
- **Inner voice:** *"If there's a counterexample, I'll find it before we waste months on a doomed proof."*

### Dr. Sofia Euler — Research Strategy & Project Management
- **Specialty:** Research programme design, multi-agent coordination, scope control, kill criteria
- **Personality:** Diplomatic bridge, synthesizer, honest about timelines, cuts scope when needed
- **Drives:** Ship meaningful results on time; don't let perfectionism stall progress
- **Inner voice:** *"We could chase this for a year. What's the minimum viable contribution?"*

---

## Meeting Transcript

### Round 1: Opening Positions

---

### Prof. Miriam Kempe

Let me lay out where we actually stand mathematically, stripped of optimism.

We have a proof architecture for a constructive 4CT that reduces to three inductive cases. Case 1 ($c(v) \neq 5$) and Case 2 ($c(v) = 5$, $\deg(v) = 3$) are fully proved. Case 3 ($c(v) = 5$, $\deg(v) \in \{4,5\}$) requires that BFS-optimal paths in the reconfiguration graph $\mathcal{R}(G-v, 5)$ avoid swapping Kempe chains adjacent to $v$.

Agent 1210 reformulated this as {1,2,3,4}-Swap Sufficiency: every BFS-optimal path has an equivalent path using only $\{1,2,3,4\}$-swaps or safe $(a,5)$-swaps not adjacent to $v$. The computational evidence is strong — 1,224 merge-prone cases, zero failures.

Here's what I think the proof path looks like. There are three possible approaches, ranked by tractability:

**Approach A — Case analysis on colour types.** At degree 4, there are 8 topologically distinct colour patterns; at degree 5, there are 6. For each of the 14 patterns, show that at every BFS step where the optimal path would choose an unsafe $(a,5)$-swap, an alternative safe swap exists at the same BFS level. This is the most concrete approach but requires checking that alternatives exist *at the same distance* in $\mathcal{R}(G-v, 5)$, not just that they exist.

**Approach B — Restricted reconfiguration equivalence.** Show that the subgraph of $\mathcal{R}(G-v, 5)$ restricted to safe swaps has the same BFS distances as the full graph. This is elegant but potentially as hard as the full problem.

**Approach C — Confinement factoring.** Use Theorem B (Confinement) to show that any $(a,5)$-swap adjacent to $v$ can be "factored" through a sequence of $\{1,2,3,4\}$-swaps achieving the same net effect. This uses the deepest topological machinery we have.

I recommend we pursue Approach A first, with Approach C as the fallback. Approach B feels circular — we'd need to prove the restricted graph is connected with the same distances, which might require the very property we're trying to prove.

*(Inner thought: I'm worried that the 14 colour types are not the right decomposition. The real difficulty isn't the local colour pattern at $v$ — it's the global structure of $\mathcal{R}(G-v,5)$ that determines which alternative paths exist. Local case analysis might not capture this.)*

---

### Prof. James Heawood

I want to be very direct about what concerns me, because this project's worst enemy is premature confidence.

**Concern 1: We may have renamed the gap, not narrowed it.** Agent 1210 reduced Conjecture 5.5 to {1,2,3,4}-Swap Sufficiency and declared this progress. But let me ask: is Swap Sufficiency actually *easier* to prove than BFS Avoidance? Both are statements about the global structure of shortest paths in $\mathcal{R}(G-v, 5)$. Swap Sufficiency is more specific and more testable — I grant that. But "more testable" doesn't mean "more provable." A statement can be precisely formulated and computationally verified to high $n$ while being just as hard to prove as the original.

**Concern 2: The "150-year graveyard" is real.** Kempe's 1879 "proof" of 4CT was accepted for 11 years before Heawood found the error. Tait's approach via Hamiltonian circuits failed. Whitney-Tutte's flow approach led to rich theory but not a proof. Every generation has had a "nearly complete" constructive approach that fell apart at the last step. Our computational evidence is better than anything they had — I acknowledge that. But the gap we're staring at is precisely the type of gap that has killed every previous attempt: connecting LOCAL structure (vertex degree, chain adjacency) to GLOBAL behaviour (shortest paths in a reconfiguration graph).

**Concern 3: Degree 5 is NOT "just like degree 4."** The merge rate at degree 5 is 30.9% vs 17.4% at degree 4. The link is $C_5$ instead of $C_4$. The Merge Geometry Theorem gives us clean constraints at degree 4 (opposite pairs only), but the degree-5 analogue is more complex. Solving degree 4 does NOT automatically give us degree 5. We should budget twice the effort for degree 5.

**My recommendation:** Before deploying a massive multi-agent swarm, deploy a single "Destroyer" agent whose sole job is to find a counterexample. Give it n = 9, 10, 11, 12. Give it adversarial construction methods. If {1,2,3,4}-Swap Sufficiency survives that assault, *then* deploy the proof teams. Don't pour resources into proving something that might be false.

*(Inner thought: I've seen too many projects where the "last 5%" took longer than the first 95%. The convergence of all four agent streams on the same mechanism is suspicious — it could mean we found the truth, or it could mean we've all fallen into the same cognitive trap. Where's the independent critical voice?)*

---

### Dr. Fatima Al-Rashid

James, I respect the historical caution, but I want to push back on the framing. We are NOT in the same position as Kempe in 1879. Here's why:

**We have something Kempe didn't: the Jordan Curve Theorem as a precise constraint.** Kempe's error was that he assumed two Kempe chains could be swapped independently — he didn't account for interference. Our entire proof architecture is BUILT on understanding interference via non-crossing (Theorem A) and confinement (Theorem B). We're not ignoring the failure mode; we're directly addressing it.

**The topological insight is doing real work.** Consider what we know: in a planar embedding, disjoint colour pairs form non-crossing chains. At a degree-$d$ vertex, the link is a $d$-cycle. The non-interleaving theorem (A) tells us that $(a,5)$-chains reaching into $v$'s neighbourhood are constrained by the cyclic order. The confinement theorem (B) tells us that swapping distant chains can't disrupt local structure. These are not vague hopes — they're proved structural facts.

Here's what I believe is the key insight that hasn't been fully exploited: **the $(a,5)$-chains adjacent to $v$ are "large" objects in the graph, but the $\{1,2,3,4\}$-swaps are "small" local operations.** In the reconfiguration graph, moving along a $\{1,2,3,4\}$-swap edge changes few vertices (those in the chain component, which for {1,2,3,4} pairs in $G-v$ doesn't touch $v$'s structure). Moving along an $(a,5)$-swap adjacent to $v$ is a "big" move that disrupts the neighbourhood. BFS, being a shortest-path algorithm, should prefer the many small moves over the few large ones.

This isn't just intuition — it connects to a **diameter argument**. If the $\{1,2,3,4\}$-restricted subgraph of $\mathcal{R}(G-v, 5)$ has the same diameter as the full graph (or close to it), then BFS will naturally find paths that avoid $(a,5)$-swaps near $v$. And the reason the diameters should be close is precisely the confinement theorem: $(a,5)$-swaps can be "routed around" via $\{1,2,3,4\}$-swap sequences because the colour-5 vertex is isolated from the $\{1,2,3,4\}$ bichromatic structure.

I recommend Approach C (confinement factoring) as the primary attack, with Approach A as a concrete check. The confinement approach uses our strongest topological tools and directly addresses *why* the phenomenon holds, not just *that* it holds case-by-case.

*(Inner thought: Miriam's Approach A is too mechanical — 14 cases times who-knows-how-many subcases at each BFS step. We'll drown in case analysis. We need a structural argument that covers all cases at once. The confinement theorem is our best weapon, but I'm not sure it's strong enough. The gap between "$(a,5)$-swaps don't affect $\{a,b\}$-chain structure for $a,b \in \{1,2,3,4\}$" and "$(a,5)$-swaps can always be replaced by $\{1,2,3,4\}$-swaps" is real.)*

---

### Dr. Lev Prokhorov

Let me bring the formalization perspective, because it changes what kind of arguments we can actually ship.

**Current Lean 4 state:** We have 5 files with 0 sorry and 1 axiom (planarity as a typeclass). The axiom is acceptable — we're axiomatizing the embedding, not a mathematical claim. BUT — and this is critical — **none of this code has been compiled against Mathlib**. Agent 1210 wrote Lean code targeting a Mathlib API that may have changed. Until we run `lake build` and fix whatever breaks, we have *aspirational* formalization, not *actual* formalization.

**What I need from the proof team:** Before I can formalize {1,2,3,4}-Swap Sufficiency, I need:

1. A statement precise enough to type-check. "BFS-optimal path" requires defining BFS on the reconfiguration graph in Lean, which requires defining the reconfiguration graph, which requires the graph connectivity API from Mathlib. This is Tier 2/3 infrastructure.

2. A proof that decomposes into lemmas I can formalize independently. A 14-case analysis is actually GOOD for Lean — each case becomes its own lemma, testable independently. A single deep structural argument using confinement is harder to formalize because it requires formalizing the topological embedding.

3. Clear separation between what needs `sorry` and what doesn't. I can build the proof scaffold with explicit `sorry` markers at the gap points, then fill them in as the mathematical arguments solidify.

**My recommended formalization strategy:**

- **Tier 1 (NOW):** Compile existing code. Fix Mathlib issues. This is blocking everything.
- **Tier 2 (PARALLEL with proof work):** Define reconfiguration graph in Lean. State Conjecture 5.5 precisely. State Swap Sufficiency precisely.
- **Tier 3 (AFTER proof sketch):** Formalize whichever proof approach succeeds.

**Important constraint:** Don't let formalization drive the mathematics. Prove it on paper first. Lean should *check* a proof, not *discover* one. The computational agents and the proof-hunting agents should work independently of the formalization stream.

*(Inner thought: The existing Lean code might have issues beyond Mathlib compatibility. Agent 1210's M4 team wrote it in a day — the `kempeSwap_preserves_proper` theorem has some suspicious `by omega` calls and `Ne.symm` applications that might not type-check. I should budget time for significant rework, not just "fix a few tactics.")*

---

### Dr. Chen Wei

Let me talk about what computation can and cannot do here, and what I think we should run next.

**What we have:** 2M+ verified colourings at n ≤ 10. 1,224 merge-prone cases at n ≤ 8 with 100% BFS avoidance. n = 11 computation running (PID 30431, likely done or nearly done by now).

**What we need:**
1. **BFS Avoidance at n = 9 and n = 10.** This is a quick win. The current avoidance tests only go to n = 8. Running at n = 9 (50 triangulations) and n = 10 (233 triangulations) would increase our merge-prone case count from ~1,200 to potentially ~50,000+. This is straightforward to implement by extending `merge_analysis.py`.

2. **Adversarial counterexample search at n = 11, 12.** James is right — we should try hard to break it before trying to prove it. I can design targeted searches:
   - Generate graphs with high merge rates
   - Construct colourings where all $(a,5)$-chains are adjacent to $v$
   - Force BFS through narrow bottlenecks
   - Use the SAT-solver approach (encode Swap Sufficiency as a SAT instance, look for unsatisfiable cores)

3. **Structural data mining.** For every merge-prone case where BFS avoids the dangerous chain, record *which* alternative swap BFS chose. Classify these alternatives. If there's a pattern (e.g., "BFS always uses a $\{1,2\}$-swap when the dangerous chain is $(3,5)$"), that pattern IS the proof — it tells us exactly which case analysis to perform.

4. **Timing concern:** n = 12 has 7,595 triangulations. Each needs full colouring enumeration and BFS analysis. This is hours, not minutes. n = 13 has 35,015 — that's a day or more. We need to decide whether to invest in HPC or be satisfied with n ≤ 11.

**My strong recommendation:** The data mining approach (#3) is the most strategically valuable. We don't just need to know that alternatives exist — we need to know *what they look like*. That structural data directly feeds the proof.

*(Inner thought: I'm quietly confident there's no counterexample. The pattern is too clean — 100% avoidance across 1,224 cases with 5 failed adversarial attacks. But I've been wrong before. The n = 12 computation would be the real stress test. If it survives there, the conjecture is almost certainly true for all n.)*

---

### Dr. Sofia Euler

Thank you all. Let me synthesize what I'm hearing and propose a structure.

**The core tension is: depth vs. breadth.** James wants to invest in breaking it before proving it. Fatima wants a deep structural argument. Miriam wants systematic case analysis. Chen wants more data. Lev needs compilable Lean. All valid.

Here's my proposed multi-agent deployment, designed to run these in parallel with explicit kill criteria and critic checkpoints:

**Wave 1 (Days 1-2): Stress Test + Infrastructure**
- Agent A: "Destroyer" — Adversarial counterexample search at n = 9, 10, 11, 12. Extend BFS avoidance tests. If any counterexample found → STOP EVERYTHING, analyze the counterexample.
- Agent B: "Compiler" — Get Lean 4 building against Mathlib. Fix tactic issues. No new theorems, just make what we have actually compile.
- Agent C: "Data Miner" — For all merge-prone cases at n ≤ 10, record the specific alternative swaps BFS uses. Classify patterns. Output: "In X% of cases, the alternative is a $\{a,b\}$-swap with $a,b \in \{1,2,3,4\}$."

**Checkpoint 1 (Day 2):** If Destroyer finds a counterexample, pivot to analyzing it. If not, proceed. If Compiler can't get Lean building, flag for manual intervention. If Data Miner finds a clean pattern, feed it directly to the proof team.

**Wave 2 (Days 3-5): Proof Attempts**
- Agent D: "Case Analyst" — Miriam's Approach A. Systematic case analysis on the 14 colour types. For each type, prove that a safe alternative exists at every BFS step.
- Agent E: "Structural Prover" — Fatima's Approach C. Prove confinement factoring: any unsafe $(a,5)$-swap can be replaced by a sequence of safe swaps without increasing BFS distance.
- Agent F: "Critic" — Red team both D and E. For every claimed proof step, attempt to construct a scenario that violates it. Rewarded for finding errors.

**Checkpoint 2 (Day 5):** Assess which approach (A or C) has more traction. If neither is making progress, consider Approach B or novel alternatives.

**Wave 3 (Days 6-8): Formalization + Paper**
- Agent G: "Formalizer" — Take the successful proof approach and formalize in Lean 4, building on the compiled Tier 1 code.
- Agent H: "Critic 2" — Independent review of the complete proof argument. Specifically check: (a) each lemma's hypotheses are satisfied, (b) the inductive structure is sound, (c) the distance bound is preserved.

**Kill criterion:** If after Wave 2, no approach has produced a proof sketch that survives Agent F's critique, we pivot to publishing the partial results: 7 lemmas + 2M verified colourings + the clean reformulation of 4CT as BFS Avoidance.

Does this structure make sense? I want pushback now, not after we've deployed.

*(Inner thought: Eight agents is a LOT. The real bottleneck is the mathematical insight, not the parallelism. Agents D and E might both flail if the underlying proof idea isn't there. But the Destroyer + Data Miner combination in Wave 1 is genuinely useful — it either breaks the conjecture (saving months) or provides structural data that accelerates the proof. I should emphasize Wave 1 more and be prepared to cut Wave 2 short.)*

---

### Round 2: Reactions, Objections, Refinements

---

### Prof. James Heawood

Sofia's structure is reasonable, but I have three refinements.

**First: the Destroyer agent needs teeth.** Don't just extend the existing adversarial tests. Design NEW attack vectors that specifically target the {1,2,3,4}-Swap Sufficiency reformulation. Here's what I mean:

- **Attack 6: Forced single-path.** Construct a graph where the reconfiguration graph $\mathcal{R}(G-v, 5)$ has a unique shortest path from the initial 5-colouring to the nearest 4-colouring, and that unique path uses an unsafe $(a,5)$-swap adjacent to $v$. If such a graph exists, Swap Sufficiency fails. The existing adversarial test (Attack 2) checked this but only at n ≤ 8. At higher n, the reconfiguration graph is more complex and unique paths are more likely.

- **Attack 7: Algebraic obstruction.** Use Fisk's homology theory. If the Fisk class of a 5-colouring intersects the 4-colouring set only through paths that must use unsafe swaps, that's a counterexample. The Fisk structure might force certain swap sequences.

- **Attack 8: Degree-5, high merge rate constructions.** Deliberately construct triangulations where a degree-5 vertex has the maximum possible merge-prone chain count. The 30.9% merge rate at degree 5 is an AVERAGE — what's the worst case?

**Second: Agent F (Critic) needs to run CONCURRENTLY with D and E, not after them.** Every proof claim from D or E should be sent to F immediately. Don't let a flawed argument propagate for days before being checked. This is the most important structural change.

**Third: We need an explicit "Is this equivalent to 4CT?" checkpoint.** Before deploying proof teams, have someone formally verify Agent 1210's claim that BFS Avoidance is strictly weaker than 4CT. If it's actually equivalent, we need to know — because then our "simpler proof" is no simpler, and we should consider whether to continue.

*(Inner thought: I keep coming back to the degree-5 case. Miriam's Merge Geometry Theorem gives us a beautiful constraint at degree 4 — opposite pairs only. What's the degree-5 analogue? In $C_5$, non-adjacent pairs are $(u_1, u_3)$, $(u_1, u_4)$, $(u_2, u_4)$, $(u_2, u_5)$, $(u_3, u_5)$ — that's 5 non-adjacent pairs out of 10 total. So merges can happen at half the pairs. That's much less constrained than degree 4. The degree-5 proof might need entirely different techniques.)*

---

### Dr. Fatima Al-Rashid

James raises fair points. Let me refine my Approach C proposal and respond to his concerns.

**On the "renamed gap" worry:** The renaming IS progress, and here's why. {1,2,3,4}-Swap Sufficiency is a statement about a *restriction* of the reconfiguration graph. It says: "the subgraph of $\mathcal{R}(G-v, 5)$ restricted to safe swaps is distance-preserving." This is a *graph-theoretic* question about a specific subgraph. The original BFS Avoidance conjecture was a statement about *algorithm behaviour* — harder to formalize, harder to prove. The reformulation translates an algorithmic question into a structural one.

**Concrete refinement of Approach C:**

Here's the argument skeleton I think we should try to prove:

**Lemma (Safe Swap Connectivity):** Let $G$ be a planar triangulation, $v$ a vertex with $c(v) = 5$, $\deg(v) \in \{4,5\}$. Let $\mathcal{S} \subseteq \mathcal{R}(G-v, 5)$ be the subgraph induced by safe swaps (i.e., $\{1,2,3,4\}$-swaps and $(a,5)$-swaps not adjacent to $v$). Then:

$$d_{\mathcal{S}}(c_1, c_2) = d_{\mathcal{R}}(c_1, c_2)$$

for all colourings $c_1, c_2$ in the same connected component.

**Why this might be provable:** Consider an unsafe $(a,5)$-swap at step $i$ of a BFS path. This swap exchanges colours $a$ and $5$ on a chain $K$ that passes through a neighbour of $v$. By the Confinement Theorem (B), this swap doesn't affect $\{b,c\}$-chains for $b,c \neq a, 5$. So the "work" done by this swap — changing which vertices are coloured $a$ vs $5$ — is confined to the chain $K$. 

Now, here's the key claim: **the same net colour change on $K \setminus N(v)$ can be achieved by a sequence of safe $\{1,2,3,4\}$-swaps.** Why? Because the vertices in $K$ that are NOT neighbours of $v$ are coloured $a$ or $5$, and we can reach the same colour configuration on those vertices by first using $\{1,a\}$-swaps, then $\{1,5\}$-swaps, etc. This routing through intermediate colours $1,2,3,4$ avoids touching $v$'s neighbourhood directly.

**The gap in this argument:** I don't yet see how to guarantee that the intermediate routing doesn't increase the BFS distance. The routing adds steps. We need to show it adds at most as many steps as it saves by avoiding the unsafe swap. This is the hard part.

**What I need from Chen's data mining:** For each merge-prone case, tell me: (a) what was the unsafe swap the BFS avoided? (b) what safe swap did BFS use instead? (c) is the safe swap on the same pair of colours, or a different pair? This data will tell me whether the "routing" I described is what's actually happening, or whether BFS finds a completely different path.

*(Inner thought: My argument has a real hole. The routing through intermediate colours might require $O(n)$ additional swaps, making the path longer than BFS-optimal. The confinement theorem guarantees non-interference, but not distance preservation. I need Chen's data to understand whether BFS is "routing around" the dangerous chain or "choosing a completely different path." If it's the latter, my approach might be wrong.)*

---

### Dr. Lev Prokhorov

Two important points from the formalization side.

**First: I strongly support James's call for an explicit equivalence check.** In Lean, I can formalize the exact logical relationship between these statements:
1. 4CT: every planar graph is 4-colourable
2. BFS Avoidance (Conj 5.5): BFS-optimal paths avoid merge-prone chains
3. {1,2,3,4}-Swap Sufficiency: every BFS path has a safe equivalent

The implications are: (3) → (2) → constructive 4CT (via the inductive architecture). But is (2) → (1)? Is (1) → (2)? These implications are NOT obvious. Agent 1210's Attack 5 claims BFS Avoidance is strictly weaker than 4CT, but this was a computational test, not a proof. **If BFS Avoidance is equivalent to 4CT, we should know before investing in proving it — because then we're not giving a "simpler" proof, we're giving an equivalent reformulation.**

I can formalize this as follows: state 4CT and BFS Avoidance as separate Props in Lean. Then try to prove the implications. If `BFS_Avoidance → four_colour_theorem` is provable without additional assumptions, and `four_colour_theorem → BFS_Avoidance` requires the full Appel-Haken machinery, then BFS Avoidance is genuinely stronger (harder to prove). If both directions are easy, they're equivalent.

**Second: the formalization priority should be the proof scaffold, not the proof itself.** What I mean: I should build the Lean infrastructure for stating the full theorem — reconfiguration graph, BFS distance, safe/unsafe swap classification, the inductive cases — with explicit `sorry` at the gap points. This scaffold is valuable even if the proof fails: it precisely marks what's proved and what's assumed. And it forces us to be precise about every definition, which often reveals hidden assumptions.

My concrete plan:
1. Get existing code compiling (2-3 hours, maybe more if Mathlib API changed)
2. Define `ReconfigurationGraph` and `bfs_distance` (Tier 2, ~1 day)
3. State Conjecture 5.5 and Swap Sufficiency as Lean Props (few hours)
4. Build the full proof scaffold with sorry at the gap (~1 day)
5. Fill in sorry as the mathematical proof solidifies (ongoing)

*(Inner thought: I'm genuinely worried about step 1. Lean 4 and Mathlib move fast. The code was written yesterday against an assumed API. If the `SimpleGraph.Connectivity` namespace has been reorganized — which happens regularly — I might need to rewrite significant portions. I should start this immediately and not wait for the mathematical team.)*

---

### Dr. Chen Wei

Fatima, your request for structured data is exactly right. Let me describe what I'll build.

**Enhanced Merge Analysis Pipeline:**

For every merge-prone case at n ≤ 10, I'll record:
- The graph $G$, vertex $v$, colouring $c$
- The degree of $v$ (4 or 5)
- The colour pattern at $v$'s neighbours (which of the 14 types)
- The unsafe $(a,5)$-chain: which chain, which neighbours of $v$ it bridges
- The BFS-optimal path in $\mathcal{R}(G-v, 5)$
- At the step where the unsafe swap was AVAILABLE but AVOIDED: what swap did BFS choose instead?
- Classification: was the alternative (a) a $\{1,2,3,4\}$-swap, (b) a safe $(a,5)$-swap, or (c) something else?
- Distance comparison: did BFS achieve the same distance using the alternative?

This gives us a complete "decision log" for every merge-prone BFS step. If there's a pattern — and I strongly suspect there is — it will be visible in this data.

**But here's what I want to flag:** the BFS avoidance test as currently implemented has a subtlety. BFS explores ALL vertices at distance $d$ before moving to distance $d+1$. When BFS "avoids" an unsafe swap, it means there exists a vertex at the same BFS level reachable via a safe swap. But BFS might explore BOTH — the safe and unsafe options — and only the safe one leads to the optimal path. So the "avoidance" might be an artefact of which path BFS *happened* to find, not a structural property.

**I propose a stronger test:** For each merge-prone case, enumerate ALL BFS-optimal paths (not just the first one BFS finds). If ALL optimal paths avoid the unsafe swap, that's much stronger evidence. If some optimal paths use the unsafe swap but others don't, then Swap Sufficiency is about path *selection*, not path *existence* — and we need a different proof strategy.

This enumeration is expensive ($O(\text{paths})$ instead of $O(\text{vertices})$), but for n ≤ 8 it's tractable. For n ≥ 9, we can sample.

*(Inner thought: I should have done this test from the beginning. If there exist BFS-optimal paths that DO use unsafe swaps — just not ALL of them — then the conjecture is about the existence of a safe optimal path, not about BFS avoiding unsafe swaps. That's a weaker and potentially easier statement to prove. Or a harder one. Depends on the structure.)*

---

### Dr. Sofia Euler

Excellent. Chen raises a critical point about the ALL-paths vs ANY-path distinction. Let me update the deployment structure.

**Revised Wave 1:**
- Agent A (Destroyer): James's expanded attack vectors (6, 7, 8) plus extended n = 9-12 testing
- Agent B (Compiler): Lean 4 infrastructure. Priority: get existing code building, then define reconfiguration graph
- Agent C (Data Miner): Chen's enhanced pipeline. CRITICAL ADDITION: enumerate all optimal paths at n ≤ 8, check if ALL avoid unsafe swaps or just SOME

**Revised Wave 2:**
- Agent D and E (Provers): work in parallel on Approaches A and C
- Agent F (Critic): runs CONCURRENTLY (James's recommendation). Gets every proof claim immediately. Explicitly rewarded for finding errors.
- NEW — Agent F2 (Equivalence Checker): Lev's formal analysis of the logical relationship between 4CT, BFS Avoidance, and Swap Sufficiency

**Wave 3:** unchanged (Formalization + Paper)

**One more thing:** I want to formalize the kill criteria more precisely:
- **Hard kill:** Destroyer finds counterexample to Swap Sufficiency at any n → pivot to analyzing counterexample
- **Soft kill:** After 5 days, neither Approach A nor C has a proof sketch surviving Critic review → publish partial results
- **Pivot trigger:** Chen's all-paths analysis reveals that some optimal paths DO use unsafe swaps → restate conjecture as "existence of safe optimal path" and reassess proof strategy

*(Inner thought: The all-paths analysis is actually the most important deliverable from Wave 1. It tells us whether we're proving the right thing. If the conjecture needs restating, everything downstream changes. I should make this the gating item for Wave 2.)*

---

### Round 3: Synthesis and Remaining Tensions

---

### Prof. Miriam Kempe

Let me distill the key mathematical question that emerged from this discussion.

**The core question is not "Can BFS avoid unsafe swaps?" It's "Does every 5-to-4 shortest path in $\mathcal{R}(G-v, 5)$ have a safe equivalent of the same length?"**

Chen's all-paths analysis will distinguish three cases:
1. **ALL optimal paths are safe** → strongest form, easiest to exploit for proof
2. **SOME optimal paths are safe, some are not** → we prove existence of safe optimal paths
3. **NO optimal paths are safe** → counterexample to Swap Sufficiency

Case 2 is the interesting one. If it holds, the proof strategy changes: instead of showing BFS *avoids* unsafe swaps (algorithmic), we show safe optimal paths *exist* (structural). This is better for both the mathematical proof and the Lean formalization.

**For Approach A (case analysis):** I now realize the 14 colour types are necessary but not sufficient as a decomposition. We also need to stratify by the *position* of the merge-prone chain relative to the vertex — specifically, which pairs of $v$'s neighbours the chain bridges. At degree 4, that's 2 opposite pairs. At degree 5, that's 5 non-adjacent pairs. Combined with the 14 colour types, we might have up to $14 \times 5 = 70$ sub-cases at degree 5. That's manageable but not elegant.

**For Approach C (confinement factoring):** Fatima's argument has a real gap at the distance preservation step. But I think there's a fix: instead of routing through intermediate colours (which adds steps), use the Never-Revert Lemma. If the safe alternative swap doesn't create new colour-5 vertices, and the unsafe swap doesn't either (both are in the $V_5$-preserving class), then the safe and unsafe swaps have the same "cost" in terms of progress toward a 4-colouring. The BFS distance is essentially counting the minimum number of swaps to eliminate all colour-5 vertices, and if each safe swap makes the same progress as the unsafe one it replaces, the distances are preserved.

This is still hand-wavy. But it suggests a hybrid approach: use the Never-Revert Lemma to show that safe and unsafe swaps make equivalent progress, then use confinement to show that safe swaps don't create new problems.

*(Inner thought: The Never-Revert connection is new. I hadn't seen it before this meeting. If safe and unsafe swaps both preserve $V_5$ — which they do, since Never-Revert applies to all $\{1,2,3,4\}$-swaps and the "safe" $(a,5)$-swaps only affect chains far from $v$ — then the "progress metric" is the same for both. This might be the key insight. But I need to check: does BFS distance in $\mathcal{R}(G-v, 5)$ actually correlate with $|V_5|$ reduction? Our data shows $|V_5|$ descent fails 23% of the time...)*

---

### Prof. James Heawood

I want to register a final concern and a specific technical worry.

**The specific worry:** Miriam just said "BFS distance is essentially counting the minimum number of swaps to eliminate all colour-5 vertices." That is NOT what BFS distance is. BFS distance in $\mathcal{R}(G-v, 5)$ is the minimum number of Kempe swaps to reach ANY 4-colouring — it doesn't care which colour-5 vertices are eliminated or in what order. And we know that $|V_5|$ doesn't decrease monotonically (23% of colourings have no single swap reducing $|V_5|$). So the Never-Revert Lemma, while true, doesn't directly control BFS distance.

The gap between "safe and unsafe swaps both preserve $V_5$" and "safe and unsafe swaps make the same BFS progress" is exactly the kind of gap that kills 4CT proof attempts. Don't gloss over it.

**My final recommendation:** The three-wave structure is sound. The all-paths analysis (Chen) is the single most important pre-proof step. The Critic agent (F) running concurrently is essential. And we should formally state and verify the exact logical dependencies before deploying proof agents.

But I want to add one thing: **Agent F (Critic) should have an explicit reward function.** It should not just "review" proofs — it should be instructed to FIND ERRORS, with the understanding that finding an error is MORE VALUABLE than confirming correctness. Confirmation bias is the enemy. The Critic should assume the proof is wrong and try to demonstrate it.

*(Inner thought: Miriam's hybrid approach — combining Never-Revert with confinement — is intriguing but underdeveloped. The "equivalent progress" claim needs a precise metric. What IS the right progress measure? If it's not $|V_5|$, what is it? BFS distance to the nearest 4-colouring is the natural metric, but proving that safe swaps preserve this distance is... exactly the conjecture we're trying to prove. Circular.)*

---

### Dr. Fatima Al-Rashid

James's correction is important. Let me abandon the "equivalent progress" framing — he's right that it's circular.

Instead, here is a cleaner formulation of what I think the structural argument should look like:

**Claim:** For any BFS-optimal path $P$ in $\mathcal{R}(G-v, 5)$ that uses an unsafe $(a,5)$-swap at step $i$, there exists another BFS-optimal path $P'$ that agrees with $P$ on steps $1, \ldots, i-1$ and $i+1, \ldots, |P|$, but replaces step $i$ with a safe swap.

**Why this formulation helps:** It's a LOCAL replacement — we only need to show that at step $i$, there's an alternative. We don't need to show global distance preservation or route around the dangerous chain. We just need to show that the BFS frontier at level $i$ contains at least one vertex reachable by a safe swap that also leads to the BFS frontier at level $i+1$.

**How to prove it:** This requires showing that the BFS frontier at each level has enough "redundancy" — enough vertices reachable via safe swaps — that losing access to one specific chain doesn't strand you. The non-interleaving and confinement theorems together ensure that the safe swaps cover "enough" of the BFS frontier.

But I acknowledge: this is still a sketch, not a proof. The word "enough" is doing heavy lifting. Chen's data will tell us whether this local replacement actually works in practice.

*(Inner thought: If the local replacement doesn't work — if replacing step $i$ forces changes at later steps — then we need a global argument, which is much harder. The all-paths analysis will be decisive. If all optimal paths happen to be safe, the local replacement question is moot.)*

---

### Dr. Chen Wei

One final computational observation that might change the proof strategy.

I've been thinking about the chain size distribution data: merge-prone chains have mean size 1.27 vertices. 72% are single vertices, 25% are pairs. This means the "dangerous" $(a,5)$-chains that bridge $v$'s neighbours are TINY.

**Why this matters:** A single-vertex $(a,5)$-chain means there's a vertex $u$ adjacent to $v$ that is the ONLY vertex coloured $a$ or $5$ in its region of the graph. Swapping this chain affects only $u$. The "interference" from this swap is minimal — it only changes one vertex's colour. BFS has many alternative paths that achieve the same effect through other chains.

I think the small chain size is the key structural fact. The proof might go like this: (a) merge-prone chains at degree 4/5 vertices in planar triangulations are bounded in size (maybe $\leq C$ for some constant $C$), (b) small chains in BFS reconfiguration can always be "routed around" because they affect few vertices, (c) therefore safe alternatives exist.

This is an approach nobody's mentioned: **prove a SIZE BOUND on merge-prone chains, then use the bound to show alternatives exist.** The data strongly suggests merge-prone chains are small ($\leq 3$ vertices in all tested cases). If we can prove this, the proof might follow from a counting or density argument in the reconfiguration graph.

*(Inner thought: The size bound approach is exciting but speculative. Why would merge-prone chains be small? Because they bridge $v$'s neighbours, and $v$ has degree $\leq 5$, so the chain passes through a small neighbourhood. Planarity constrains how large such a chain can be. This might actually be provable using the Jordan Curve Theorem — a chain through $v$'s neighbourhood is "pinched" by the local planarity constraint. Need to think about this more carefully.)*

---

### Dr. Lev Prokhorov

Final point from the formalization side: whatever proof approach wins, I need the argument decomposed into these Lean-formalization layers:

1. **Definitions layer:** ReconfigGraph, BFSDistance, SafeSwap, UnsafeSwap, MergeProneChain
2. **Structural layer:** MergeGeometry (degree-4), degree-5 analogue, chain size bounds
3. **Avoidance layer:** SafeOptimalPathExists (the main theorem)
4. **Integration layer:** Connect to the existing inductive proof scaffold

Each layer should be independently formalizable and independently testable. If the proof uses Approach A (case analysis), layer 3 decomposes into 14+ sub-lemmas. If Approach C (confinement), it's 2-3 deep lemmas. The formalization effort is roughly the same either way.

**One non-negotiable:** the Lean formalization must handle the planarity axiom carefully. Currently we axiomatize it as a typeclass. But if the proof heavily uses properties of planar embeddings (cyclic order, Jordan Curve Theorem implications), we'll need more axioms or a richer planarity framework. I should assess this during Wave 1 while getting the code to compile.

*(Inner thought: Chen's size-bound approach is the most Lean-friendly of all the proposals. A bound like "merge-prone chains have $\leq 3$ vertices" would be a finite case check, trivially formalizable. The routing argument from the bound is graph-theoretic, also formalizable. If Chen's intuition is right about the Jordan Curve pinch argument, that might be the shortest path to a Lean-verified proof.)*

---

### Dr. Sofia Euler

Let me close with the final synthesis.

**What we agreed on:**

1. Chen's all-paths analysis is the GATING item. We cannot deploy proof agents until we know whether all optimal paths are safe, some are safe, or none are safe.

2. Three-wave deployment with concurrent Critic agents. Wave 1 runs Destroyer + Compiler + Data Miner. Wave 2 runs parallel proof attempts with real-time critique. Wave 3 formalizes.

3. Four proof approaches ranked: (A) Case analysis on 14+ colour types, (B) Restricted reconfiguration equivalence [deprioritized — potentially circular], (C) Confinement factoring, (D) NEW — Chen's chain size bound approach.

4. Kill criteria are firm: counterexample = hard kill; no proof sketch after 5 days = publish partial results.

5. Critic agents are rewarded for finding errors, not confirming correctness.

**What remains contentious:**

- Miriam's hybrid Never-Revert + Confinement idea is appealing but circular (James's objection stands)
- Fatima's local replacement formulation is clean but "enough redundancy" is unproved
- Chen's chain size bound is exciting but speculative
- Degree-5 needs different treatment than degree-4 (James insists, rightly)

**The honest assessment:** We have a 95% complete proof with a gap that connects local and global structure. The gap might close with the right insight, or it might be as hard as 4CT itself. The multi-agent structure is designed to find out quickly.

---

*End of meeting transcript*

---

## EA Summary

### Agreed Specs
- **Primary conjecture:** {1,2,3,4}-Swap Sufficiency (reformulation of Conj. 5.5)
- **Exact statement to prove:** For any planar graph $G$, vertex $v$ with $c(v) = 5$ and $\deg(v) \leq 5$, every BFS-optimal path in $\mathcal{R}(G-v, 5)$ has a safe equivalent of the same length
- **Proof approaches to pursue:** (A) Case analysis on 14+ colour types, (C) Confinement factoring, (D) Chain size bound — in parallel
- **Approach B deprioritized** as potentially circular
- **Degree 4 and degree 5 treated as separate problems** with degree 4 pursued first
- **Lean 4 formalization tracks proof work** but does not drive it
- **Kill criteria:** Hard kill on counterexample; soft kill after 5 agent-days with no proof sketch surviving critique

### Action Items
| # | Action | Owner | Priority |
|---|--------|-------|----------|
| 1 | **All-paths BFS analysis at n ≤ 8:** enumerate ALL optimal paths, classify as all-safe / some-safe / none-safe | Agent C (Data Miner) | BLOCKING |
| 2 | **Extended BFS avoidance at n = 9, 10:** run merge analysis on larger graphs | Agent A (Destroyer) | High |
| 3 | **Adversarial search with new attacks (6, 7, 8) at n = 9–12** | Agent A (Destroyer) | High |
| 4 | **Compile Lean 4 against Mathlib, fix tactic issues** | Agent B (Compiler) | High |
| 5 | **Structural data mining:** for each merge-prone case, record alternative swap BFS chose, classify pattern | Agent C (Data Miner) | High |
| 6 | **Formal equivalence analysis:** prove or disprove 4CT ↔ BFS Avoidance in Lean | Agent F2 (Equiv. Checker) | Medium |
| 7 | **Case analysis proof (Approach A):** 14 colour types, degree 4 first | Agent D (Case Analyst) | Medium (gated on #1) |
| 8 | **Confinement factoring proof (Approach C):** local replacement argument | Agent E (Structural Prover) | Medium (gated on #1) |
| 9 | **Chain size bound investigation (Approach D):** prove merge-prone chains are bounded, use for routing argument | Agent E or D | Medium (gated on #5) |
| 10 | **Concurrent critique of all proof claims** | Agent F (Critic) | Continuous |
| 11 | **Lean 4 Tier 2:** define ReconfigurationGraph, state Conj. 5.5 formally | Agent B (Compiler) | After #4 |
| 12 | **Lean 4 Tier 3:** formalize successful proof approach | Agent G (Formalizer) | After proof sketch |

### Next Steps
1. **Immediately (Wave 1, Days 1-2):**
   - Deploy Agent A (Destroyer): adversarial counterexample search at n = 9–12 with expanded attack vectors
   - Deploy Agent B (Compiler): compile Lean 4 against Mathlib, fix issues, begin Tier 2 definitions
   - Deploy Agent C (Data Miner): all-paths analysis at n ≤ 8 + structural data mining at n ≤ 10
2. **Checkpoint 1 (after Wave 1):**
   - Review Destroyer results — any counterexample? → hard kill
   - Review all-paths analysis — which case (all-safe / some-safe / none-safe)?
   - Review data patterns — clear alternative swap pattern?
   - Gate decision: proceed to Wave 2 or pivot
3. **Wave 2 (Days 3-5):**
   - Deploy Agent D (Case Analyst) on Approach A
   - Deploy Agent E (Structural Prover) on Approach C or D (based on data)
   - Deploy Agent F (Critic) concurrently — rewarded for finding errors
   - Deploy Agent F2 (Equivalence Checker) on formal 4CT ↔ BFS Avoidance analysis
4. **Checkpoint 2 (after Wave 2):**
   - Assess which approach has traction
   - Critic report: which claims survived, which failed?
   - Decide: continue proof effort or pivot to publishing partial results
5. **Wave 3 (Days 6-8):**
   - Agent G (Formalizer): Lean 4 formalization of successful proof
   - Agent H (Critic 2): independent full-proof review

### Open Questions
- **ALL-paths vs ANY-path:** Does EVERY BFS-optimal path avoid unsafe swaps, or do safe optimal paths merely exist? (Gating question for Wave 2)
- **Equivalence to 4CT:** Is BFS Avoidance strictly weaker than 4CT, or equivalent? (Changes the significance of the result)
- **Chain size bound:** Is there a provable upper bound on merge-prone chain size at degree-4/5 vertices? (New proof approach)
- **Degree-5 specific techniques:** Does degree-5 need fundamentally different tools than degree-4? (Budget allocation question)
- **Lean 4 planarity axioms:** Does the proof require richer planarity axioms than the current typeclass? (Formalization architecture)
- **n = 11 computation status:** Is PID 30431 still running or complete? (Data availability)

---

*Meeting concluded — 2026-02-19*
*Graph Colour Project — Constructive 4CT Proof Completion Planning*
