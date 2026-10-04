# Agent 1701 — Wave 1 task decomposition

**Issued by:** main planning distributor
**Date:** 27 September 2026
**Gate:** critic meeting with the main planning team. No node is checked off or killed before that meeting.

## Why this wave

The Proof Navigator still marks every track unstarted. The repository’s Plan 2 record (`SolvingFrameworkPlan/ExecutiveSummary_Plan2_Status.md`) says six Kempe lemmas are proved and one conjecture remains: BFS Avoidance (Conjecture 5.5), open at degrees 4 and 5. That record has not been gated against the files. This wave produces specifications and an audit. It does not prove the Four Colour Theorem.

Tracks 2–7 stay unstarted unless the audit cites files that already exist.

## Managers

| Manager | Groups | Combines |
|---|---|---|
| M-Kempe | K1, K2 | Degree-4 and degree-5 BFS Avoidance specifications |
| M-Foundation | F1, F2 | Navigator audit and Lean Tier-1 obligation specification |

A manager sends a group’s draft back until the spec has all of: definitions, formal statement, acceptance test, cited evidence, kill criterion, and an explicit boundary of what is not proved.

## Tasks

| ID | File | Navigator node | Output |
|---|---|---|---|
| K1 | `tasks/K1.md` | `t1-spec-d4` | `groups/K1_spec.md` |
| K2 | `tasks/K2.md` | `t1-spec-d5` | `groups/K2_spec.md` |
| F1 | `tasks/F1.md` | `audit-1701` | `groups/F1_audit.md` |
| F2 | `tasks/F2.md` | `f-spec-lean` | `groups/F2_spec.md` |

Do not edit `docs/navigator/planning.json` or `docs/navigator/data.js`. The main team writes the board after the gate.

## Standing order

`OPERATING.md` in this folder binds every later wave. Do not end a cycle by filing the next executable task. Do the task. The wave-1 gate stopped after issuing `tasks/W1.md`. That stop is the mistake this order forbids.
