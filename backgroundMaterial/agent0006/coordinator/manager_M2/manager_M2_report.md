# Manager M2 Report: Integration Plan

**Agent:** 0006-M2  
**Date:** 18 February 2026  
**Task:** Map existing ProofNavigator tracks to Agent 1221 analysis. Design new data.js nodes for passing items. Produce complete integration plan.  
**Sub-agents:** M2-S1 (track mapping), M2-S2 (integration plan)  
**Dependencies:** M1 filtered lists (6 strategies, 9 cross-domain areas passing threshold)

---

## Executive Summary

M2 produced a complete integration plan that grows the ProofNavigator from 7 tracks to 11 tracks, adds 18 new sub-goals across existing and new tracks, and reorganizes priorities to align with Agent 1221's three-track research programme.

### Structural Changes

| Change | Count | Details |
|--------|-------|---------|
| New tracks added | 4 | Track 8 (Refined Discharging), Track 9 (Proof Mining), Track 10 (Hadwiger), Track 11 (Formal Methods & ATP) |
| New sub-goals on existing tracks | 13 | F4b, t1-5, t1-6, t4-5, t4-6, t5-3, t5-4, t6-3, t6-4, t7-5, t7-6, t7-7, plus Area 18 note |
| Sub-goals on new tracks | 18 | t8-1 to t8-4, t9-1 to t9-5, t10-1 to t10-3, t11-1 to t11-5, plus F4b |
| Tracks downgraded | 2 | Track 2 (Chromatic Polynomial), Track 3 (Flows) |
| Total ProofNavigator nodes after update | ~65 | Up from ~40 |

### Priority Realignment

**Critical (start immediately):**
- Foundation (5CT in Lean 4, including new F4b)
- Track 8 (Refined Discharging — highest feasibility strategy, no existing track)

**High (start within 1–2 months):**
- Track 1 (Kempe Swap Game)
- Track 4 (TQFT / Penrose)
- Track 9 (Proof Mining)
- Track 11 (Formal Methods & ATP — infrastructure for all tracks)

**Medium (start within 3–6 months):**
- Track 5 (Spectral / Colin de Verdière)
- Track 6 (Sheaf Cohomology)
- Track 7 (Computational Discovery)
- Track 10 (Hadwiger)

**Low (retain for context, defer active work):**
- Track 2 (Chromatic Polynomial)
- Track 3 (Nowhere-Zero Flows)

---

## Cross-Track Dependencies

```
Foundation ──→ ALL TRACKS (infrastructure)
Track 11 (ATP) ──→ ALL TRACKS (Lean 4 libraries)
Track 8 (Discharging) ←→ Track 9 (Proof Mining): complementary
Track 1 (Kempe) ←→ Track 8 (Discharging): Kempe chains in reducibility
Track 4 (TQFT) ←→ Track 6 (Sheaf): categorical tools shared
Track 7 (Discovery) ──→ ALL TRACKS (computational evidence)
Track 5 (Spectral) ←→ Track 10 (Hadwiger): μ(G) and minor theory
```

---

## Key Design Decisions

### 1. Separate Track 8 (Discharging) vs. Merging with Track 9 (Proof Mining)

**Decision: Separate tracks.**  
**Rationale:** Strategy 4 and Strategy 5 are complementary but have different methodologies (SAT optimization vs. Coq analysis), different toolchains, and different success criteria. A researcher working on SAT-based rule search (Track 8) needs different infrastructure than one instrumenting the Coq proof (Track 9). Their outputs converge — a smaller unavoidable set (Track 8) with clustered reducibility arguments (Track 9) — but the work is independent.

### 2. Track 11 (Formal Methods) as Dedicated Infrastructure Track

**Decision: Dedicated track rather than dispersed Lean 4 sub-goals.**  
**Rationale:** Currently, Lean 4 formalization appears as a sub-goal in every track (F1-F5, t1-4, t2-1, t3-1, etc.). This creates coordination problems — who owns the shared planar graph library? Track 11 centralizes this: it owns the Lean 4 infrastructure (planar graphs, Kempe chains, reducibility checker) and other tracks consume it. This prevents duplicated effort and ensures consistent API design.

### 3. Area 18 (Discrete Geometry) as Sub-goal, Not Track

**Decision: Note/sub-goal rather than full track.**  
**Rationale:** Circle packing provides a geometric embedding tool, not a proof strategy. It's best used as a computational/visualization aid for Track 1 (understanding Kempe chains in geometric settings). Adding a 12th track for a tool would dilute the structure.

### 4. Tracks 2 and 3 Retained but Downgraded

**Decision: Retain, add below-threshold annotation, do not remove.**  
**Rationale:** Both tracks have infrastructure value (chromatic polynomial formalization, Tutte duality) that feeds other tracks. Removing them would require restructuring existing sub-goals. The cost of retention is low (they sit at "unstarted" with no active resources). **Escalated to Coordinator for final approval.**

---

## Self-Assessment (Tripartite Dialogue)

**Craftsperson:** The integration plan is comprehensive. Every passing item has a home. The priority alignment with §6 is tight. The new track designs include appropriate kill criteria and cross-references.

**Skeptic:** 11 tracks might be too many. The ProofNavigator's visual design (tree structure) may become cluttered. Also: the new tracks (8-11) have no `files` entries yet — they need actual code files created to be actionable. And I'm uncertain whether "Formal Methods & ATP" is coherent as a single track or whether it's too diffuse (Lean 4 infrastructure + AI proof search + HoTT = three different things).

**Mover:** 11 tracks is manageable — the visual hierarchy handles it. Track 11 can always be split later if the HoTT component diverges. The plan is ready for implementation. Ship it with the caveat that Track 11's scope should be reviewed after 2 months.

---

## Deliverables

1. `sub_S1/S1_report.md` — Track mapping with recommended updates per track
2. `sub_S2/S2_report.md` — Complete integration plan with new data.js nodes
3. This report — Consolidated decisions and priority alignment

---

*Manager 0006-M2 — 18 February 2026*
