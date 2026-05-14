# Task Decomposition — Agent 1608

## Original Task

Reformulate, streamline, and proofread Paper 1 (Energy Functionals for Kempe Chain Reconfiguration) to ensure the entire pipeline is reproducible and everything is cohesive. Remove all "agent meetings" and fourth-wall-breaking references. Maintain scientific paper tone. Be conservative and explicit about assumptions and shortcomings. Maintain rigour in honesty and process.

## Known Issues in Current Paper

1. **Fourth-wall breaks:** "Agent~1419", "Agent~1443" references in introduction.tex, background.tex, results.tex
2. **Stale claims:** Surface Tension Rigidity Conjecture was DISPROVED (Agent 1520) — paper still presents it as open
3. **Missing updates:** Paper doesn't reflect n=10 computational extension (1.9M cases), MTL breakthrough, or {1,2,3,4}-Swap Sufficiency disproof
4. **Reproducibility:** No code availability statement, no data description section
5. **Draft artifacts:** "WORKING DRAFT" watermark, "Working Draft" in title
6. **Reference gaps:** Self-citation "mathewson2025" used for both Magic Gems and constructive architecture work without distinguishing

## Atomic Subtasks

1. **S1-M1:** Scrub all "Agent X" references from every .tex file and replace with proper scientific attribution
2. **S2-M1:** Remove all meeting/process/internal-project references; ensure tone is consistently that of a research paper
3. **S1-M2:** Update Surface Tension Rigidity section to reflect its disproof; reframe as a computational observation that was falsified
4. **S2-M2:** Add updated computational evidence (n≤10, 1.9M cases, safe detour cost bounded at 1); update limitations section
5. **S1-M3:** Proofread all LaTeX for grammar, notation consistency, and logical flow between sections
6. **S2-M3:** Add reproducibility section (code availability, data description), clean up references, remove draft watermark

## Dependency Graph

```
M1-S1 (agent references) ──┐
M1-S2 (tone/process refs)──┤── All parallel (separate concerns per section)
M2-S1 (rigidity update)  ──┤
M2-S2 (new evidence)     ──┤
M3-S1 (proofreading)     ──┤
M3-S2 (reproducibility)  ──┘
```

All can run in parallel — each produces a precise change list. Final integration applies all non-conflicting changes.

## Stream Allocation

| Manager | Stream Type | Subtasks | Dependencies | Async? |
|---------|-------------|----------|--------------|--------|
| M1 | parallel | S1, S2 | None | Yes |
| M2 | parallel | S1, S2 | None | Yes |
| M3 | parallel | S1, S2 | None | Yes |

## Complexity Estimate

**Medium.** Well-scoped editorial task on 8 existing files. Main risk: ensuring scientific accuracy of updated claims about disproved conjectures. Each sub-subagent edits specific files to avoid conflicts.

---

*Agent 1608 — Graph Colour Project*
*8 April 2026*
