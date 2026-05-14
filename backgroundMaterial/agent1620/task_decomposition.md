# Task Decomposition — Agent 1620

## Original Task

Act as a skeptical journal reviewer. Deploy a multi-agent review team to find holes in the argument or clarity of the paper, identify errors indicative of LLM paper generation and lack of precise logic and thought, and remove LLM writing style tells. Apply fixes directly.

## Atomic Subtasks

1. **M1:** Mathematical rigour audit — check every definition, proposition, conjecture, and proof for logical gaps, circular reasoning, unsupported claims, imprecise statements
2. **M2:** LLM writing tell detection — find hedging, filler, vague-but-impressive-sounding claims, repetitive structure, over-enthusiastic language, false precision, and fix each instance
3. **M3:** Claim verification — check that every empirical claim in the text matches the computational pipeline, that numbers are internally consistent, and that the abstract/conclusion don't overstate results
4. **M4:** Structure and redundancy — find repeated content between sections, check that the logical flow is tight, remove padding, ensure every paragraph earns its place

## Stream Allocation

| Manager | Stream | Focus | Async? |
|---------|--------|-------|--------|
| M1 | parallel | Mathematical logic | Yes |
| M2 | parallel | LLM tells + prose style | Yes |
| M3 | parallel | Empirical claims + internal consistency | Yes |
| M4 | parallel | Structure + redundancy | Yes |

All streams are independent and can run in parallel. Each reviewer produces a list of specific issues AND applies fixes directly to the .tex files in the public repo.

## File Assignments (to avoid edit conflicts)

- M1: `02-background.tex`, `03-methods.tex` (mathematical content)
- M2: `01-introduction.tex`, `coverpage.tex` (prose-heavy, most LLM-tell-prone)
- M3: `04-results.tex` (empirical claims)
- M4: `05-discussion.tex`, `06-conclusion.tex` (speculation-heavy, redundancy-prone)

---

*Agent 1620 — Graph Colour Project*
*8 April 2026*
