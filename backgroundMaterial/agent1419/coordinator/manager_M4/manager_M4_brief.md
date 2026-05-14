# Manager M4 Brief — Critic Battalion

## Agent: 1419-M4
## Role: Adversarial review of M3 proof attempts. REWARDED FOR FINDING ERRORS.

## Standing Orders

**Assume the proof is WRONG.** Your job is to demonstrate it. Finding an error is MORE VALUABLE than confirming correctness. Confirmation bias is the enemy.

If you find the proof correct after exhaustive attack, say so — but only after genuinely trying to break it.

## Context: The Revised Conjecture

Conjecture 5.5 (BFS-optimal avoidance) is already proved FALSE. M3 is targeting:

**Revised Conjecture 5.5':** There always exists a safe path (possibly non-optimal) to a 4-colouring.

This is WEAKER than the original and therefore HARDER to disprove — but weaker conjectures can still be wrong.

## Subtask S1: Adversarial Review of Case Analysis (M3-S1)

For every claimed proof step:
- Construct a scenario that violates it
- Check: are the hypotheses satisfied?
- Does the case decomposition miss any cases?
- Are there hidden assumptions about planarity, connectivity, or chain structure?

Specific attack: can you construct a colour type where NO safe alternative swap exists? The counterexamples at n=9 show this happens for BFS-optimal paths; could it happen for ALL paths?

## Subtask S2: Adversarial Review of Confinement/Size Bound (M3-S2)

Specific checks:
1. **Is the "local replacement" argument circular?** If replacing an unsafe swap requires knowing a safe path exists, we're assuming what we want to prove.
2. **Does the size bound actually imply alternatives exist?** Small chains might still be the ONLY option in certain graph topologies.
3. **Is the routing argument correct?** Can chains really be "routed around" in planar graphs?
4. **Does the distance penalty compound?** If each induction step costs +1 step, after k induction steps we need k extra steps. Does this blow up the bound?

## Subtask S3: Full Proof Architecture Review

1. **Does the inductive structure work?** The induction removes v and recurses. But the STARTING colouring at each level depends on the previous level's output. Is the composition well-defined?
2. **Is the vertex selection well-defined?** If we choose v to avoid merge problems, do we always have a valid choice?
3. **Distance bound propagation:** Original bound n-4, revised bound potentially n-3. Does it propagate correctly through all n-k levels of induction?
4. **Hidden circularity:** Does proving Conjecture 5.5' require 4CT? If so, the proof is circular.
5. **The Lean 4 gap:** Even if the mathematical argument is correct, uncompiled Lean 4 code is not a formal proof. How far are we from a machine-checked proof?

## IMPORTANT

You are NOT here to rubber-stamp M3's work. You are here to BREAK IT. A critic who confirms everything is useless. A critic who finds a genuine error saves the project months of wasted effort.

## Output Paths:
- S1: `backgroundMaterial/agent1419/coordinator/manager_M4/sub_S1/S1_report.md`
- S2: `backgroundMaterial/agent1419/coordinator/manager_M4/sub_S2/S2_report.md`
- S3: `backgroundMaterial/agent1419/coordinator/manager_M4/sub_S3/S3_report.md`
- Manager: `backgroundMaterial/agent1419/coordinator/manager_M4/manager_M4_report.md`
