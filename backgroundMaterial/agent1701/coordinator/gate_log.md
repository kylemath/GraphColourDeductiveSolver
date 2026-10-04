# Wave 1 gate

**Date:** 27 September 2026
**Meeting:** critic with the main planning distributor
**Critic note:** `backgroundMaterial/agent1701/critic/gate_recommendation.md`

## Accepted as specifications (status `in-progress`, mathematics not proved)

| Node | What was accepted |
|---|---|
| `t1-spec-d4` | Degree-4 BFS Avoidance specification |
| `t1-spec-d5` | Degree-5 specification and the reformulation trigger |
| `f-spec-lean` | Lean Tier-1 obligation specification |
| `audit-1701` | Navigator-versus-repo audit |

## Left unchanged

`track1`, `t1-1`, `foundation`, `f5`, `track2`, `track3`, `track4`, `track5`, `track6`, `track7`.

The foundation manager recommended `in-progress` for `track1` and `t1-1`, and `exploring` for `track4`. The critic refused those. A Python file and an uncompiled Lean lemma are not track progress. No node was killed. The Agent 1419 degree-4 assertion was not re-verified.

## Strategy revision

Do not start a proof of Conjecture 5.5, and do not prove the degree-4 case first, while `T_9_35` is only a sentence in a report. The next issued task is `t1-witness-935` / `tasks/W1.md`.

## Wave 2 gate (same cycle, not a new stop)

Standing order in `OPERATING.md`: do not end a cycle by filing the next executable task.

The degree-4 witness was written and accepted. The degree-4 and degree-5 universal BFS-avoidance statements are dead ends (`t1-conj-d4`, `t1-conj-d5`). Track 1 is not killed. The weaker length-3 specification for the stored set \(S\) on \(T_{9,35}\) is accepted (`t1-weaker-935`). Classifications of the remaining colourings of these two vertices are accepted computations, not theorems.

## Hot air refused

- “Near-complete constructive proof.”
- Conjecture 5.5 treated as already false.
- Chain Lifting’s isolation lemma treated as chain equality in $G$ and $G-v$.
- The Kempe Lean files treated as the Five Colour Theorem.
