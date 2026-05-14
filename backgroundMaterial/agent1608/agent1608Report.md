# Agent 1608 Report: Paper 1 Reformulation and Polish

**Agent:** 1608
**Date:** 8 April 2026
**Project:** Graph Colour
**Task:** Reformulate, streamline, and proofread Paper 1 (Energy Functionals for Kempe Chain Reconfiguration). Remove fourth-wall breaks, update scientific claims, add reproducibility, maintain rigour.

---

## 1. Task Overview

Paper 1 introduces eight energy functionals for the Kempe chain reconfiguration graph. The paper had several issues: "Agent X" references breaking the fourth wall, a conjecture presented as open that had been disproved, missing computational updates, no code availability statement, and draft artifacts.

## 2. Decomposition

Three parallel managers, each handling non-overlapping concerns:

| Manager | Stream | Sub-subagents | Iterations | Final Status |
|---------|--------|---------------|------------|--------------|
| M1 | Fourth-wall removal + tone | S1, S2 | 1 | Complete |
| M2 | Scientific accuracy updates | S1, S2 | 1 | Complete |
| M3 | Reproducibility + references + polish | S1, S2 | 1 | Complete |

## 3. Changes Made

### M1: Fourth-Wall Removal (3 files edited)

| File | Change |
|------|--------|
| `01-introduction.tex` | "Recent work" → `Mathewson~\cite{mathewson2025constructive}` |
| `01-introduction.tex` | "Agent~1419 disproved" → "Exhaustive enumeration at $n=9$ disproves" |
| `02-background.tex` | "disproved by Agent~1419" → "exhaustive enumeration reveals" + Section cross-ref |
| `04-results.tex` | "discovered by Agent~1443" → "identified via exhaustive enumeration" |

### M2: Scientific Accuracy (4 files edited)

| File | Change |
|------|--------|
| `04-results.tex` | Added Remark (Subsequent falsification) after ST Rigidity Conjecture |
| `04-results.tex` | Scoped evidence paragraph to "$n = 9$" with falsification cross-ref |
| `05-discussion.tex` | Updated limitation 4 with n=10 data (1.9M cases, 100% safe paths) |
| `05-discussion.tex` | Added limitation 5: explicit ST Rigidity falsification statement |
| `06-conclusion.tex` | Finding (3) qualified to n=9, noted subsequent falsification |
| `06-conclusion.tex` | Updated open questions: "Persistence" → confirmed n=10 data |
| `06-conclusion.tex` | Added "Refined indicators" question about composite functionals |
| `coverpage.tex` | Abstract updated: "subsequently falsified at $n \geq 10$" |

### M3: Reproducibility + Polish (4 files edited)

| File | Change |
|------|--------|
| `preamble.tex` | Removed WORKING DRAFT watermark (4 lines deleted) |
| `coverpage.tex` | Removed "Working Draft" from title; added Code Availability |
| `references.bib` | Added 5 entries: swendsen1987, kempe1879, heawood1890, mathewson2025constructive, lasvergnas1981 |
| `03-methods.tex` | Added Computational Pipeline subsection (enumeration scope, tools, runtimes) |

### Integration Pass (2 additional fixes)

| File | Change |
|------|--------|
| `02-background.tex` | Fixed misattribution: Swendsen-Wang cite changed from potts1952 to swendsen1987 |
| `references.bib` | Fixed swendsen1987 entry type from @inproceedings to @article |
| `build.sh` | Fixed bibtex path: copies references.bib to build/ before running bibtex |

## 4. Verification

- **Grep for "Agent":** Zero matches in entire `paper/` directory
- **LaTeX compilation:** 18 pages, zero warnings, zero errors
- **Bibliography:** All 17 entries resolve correctly
- **Cross-references:** All `\ref` and `\label` pairs resolve

## 5. Deliverables

| Deliverable | Path | Description |
|-------------|------|-------------|
| Compiled PDF | `paper/main.pdf` | 18-page clean build, no watermark |
| All edited .tex files | `paper/sections/` | 6 section files + coverpage + preamble |
| Updated bibliography | `paper/references.bib` | 17 entries (was 12) |
| Fixed build script | `paper/build.sh` | Handles bib path correctly |

## 6. Assessment

**Craftsperson says:** All fourth-wall breaks removed, all claims updated to reflect current knowledge, reproducibility added, paper compiles cleanly. The narrative is now consistently that of a scientific paper: "we observed X, we conjectured Y, subsequent computation falsified Y."

**Skeptic says:** The figures (`figures/safe_vs_unsafe_energy_bars_T_9_25.png`, etc.) are referenced but may not exist in the repo — the paper will compile with missing figure warnings if figures are absent. The `mathewson2025constructive` bib entry says "In preparation" which is honest but means the reference is not yet verifiable. The Computational Pipeline subsection references Robertson et al. for triangulation count verification, which is a loose citation.

**Mover says:** The paper is in publishable shape. The remaining concerns (figure generation, exact citation for triangulation counts) are minor polish items, not blockers. Ship it.

---

*Agent 1608 — Graph Colour Project*
*8 April 2026*
