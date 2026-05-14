# Task Decomposition — Agent 1545

## Original Task

Following Agent 1520's sprint (two conjectures disproved, two infrastructure systems built), deploy four new team-lead agents to pursue the most promising revised pathways. Key context:
- {1,2,3,4}-Swap Sufficiency is FALSE (48 counterexamples at n=9)
- Surface Tension Rigidity Conjecture is FALSE (fails at every scale)
- SAT Discharging framework operational at first order (bottleneck: second-order cascade)
- TQFT: manifestly positive TV state sum DEAD, web basis and unitarity still alive
- The 48 counterexamples have safe non-optimal paths (length d+1) — revised Conjecture 5.5' is still open
- M1 identified merge-tolerant lifting as the #1 alternative: check if forced merges are actually harmless

## Team Structure

| Team Lead | Codename | Focus | Rationale |
|-----------|----------|-------|-----------|
| M1 | **Alpha — Merge-Tolerant Lifting** | Test if merges in the 48 CEs are harmless; formalize merge-tolerant lifting | Highest priority: if merges are harmless, the constructive proof works AS IS |
| M2 | **Beta — Safe Path & Revised Framework** | Investigate non-optimal safe paths; formalize revised Conjecture 5.5'; extend computation | If merges aren't harmless, we need safe paths at d+1; also push computation to n=10-12 |
| M3 | **Gamma — SAT Discharging v2** | Build second-order cascade encoding; transcribe RSST rules; run real SAT optimization | The fallback/classical path: optimize the existing proof |
| M4 | **Delta — TQFT Web Basis & Integrative Theory** | Implement proper Kuperberg spider calculus; explore manifold construction; cross-connect findings | The moonshot: last viable TQFT path, plus integrative cross-stream analysis |

## Dependency Graph

```
Alpha (merge-tolerant) ──→ If harmless: PROOF COMPLETE (modulo formalization)
                          If NOT harmless: feeds Beta (safe path approach critical)

Beta (safe paths)      ──→ Independent of Alpha; data feeds back to revised proof architecture
                          Cross-feeds with Alpha on counterexample analysis

Gamma (SAT discharging) ──→ Fully independent; continues M3 infrastructure
                           Cross-feeds: reducibility DB useful for Alpha/Beta

Delta (TQFT web basis) ──→ Fully independent; highest-risk/highest-ceiling
                          Integrative: connects surface tension, Penrose, energy landscape findings
```

## Stream Allocation

| Manager | Stream Type | Subtasks | Dependencies | Async? |
|---------|-------------|----------|--------------|--------|
| M1 (Alpha) | parallel | S1 (post-merge check), S2 (formalize lemma), S3 (vertex selection) | None | Yes |
| M2 (Beta) | parallel+serial | S1 (d+1 paths), S2 (n=10-12 extension), S3 (revised conjecture) | S2 feeds S3 | Yes |
| M3 (Gamma) | serial | S1 (RSST rules), S2 (second-order framework), S3 (SAT solver) | S1→S2→S3 | Yes |
| M4 (Delta) | parallel | S1 (spider calculus), S2 (manifold construction), S3 (integration) | None | Yes |

## Kill Criteria

| Stream | Kill Criterion | Consequence |
|--------|---------------|-------------|
| Alpha | Merge is NOT harmless in even 1 of 48 CEs (v can't be recoloured post-merge) | Merge-tolerant lifting fails; pivot to Beta's safe path approach |
| Beta | No safe path at ANY length for some CE at n ≤ 12 | Constructive approach dead; pivot entirely to Gamma (classical) |
| Gamma | Cannot reproduce RSST's 633 with second-order encoding after full sprint | Fundamental framework bug; debug before proceeding |
| Delta | Web basis coefficients negative for planar graphs in proper Kuperberg basis | TQFT positivity approach completely dead |

---

*Agent 1545 — Graph Colour Project*
*2026-02-20*
