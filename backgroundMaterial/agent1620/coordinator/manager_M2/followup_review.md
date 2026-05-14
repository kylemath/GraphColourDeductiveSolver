# Follow-up review: Reviewer 2 (LLM writing tells)

**Scope:** Revised `01-introduction.tex` and `coverpage.tex` in `KempeReconfigurationEnergy/paper/`, checked against the ten prior concerns and a fresh pass for new stylistic tells.

---

## Status of the ten prior fixes

| # | Concern | Status | Notes |
|---|---------|--------|-------|
| 1 | Opening sentence em-dash pair → commas | **RESOLVED** | Opening now uses a comma after “(4CT)” and a parenthetical “that every planar graph…” with no em-dash framing. |
| 2 | “Long and distinguished pedigree” + em-dash → cut padding | **RESOLVED** | Phrase removed; pedigree padding gone. |
| 3 | Em-dashes around “via a sequence of Kempe swaps” → commas | **RESOLVED** | Kempe-swap clause is set off with commas: “can be reconfigured, / via a sequence of Kempe swaps, into…”. |
| 4 | “This disproof is not a disproof of” → direct assertion | **RESOLVED** | Replaced by “The counterexamples refute only the optimality claim, not the constructive strategy itself…” with a concrete follow-on. |
| 5 | “Why Physics?” — padding, em-dashes, “landscape” overuse → tighten | **RESOLVED** | Section is shorter and more concrete (energy functional → discrete energy surface; Potts / Swendsen-Wang / embedding / TQFT line). No em-dashes in this subsection. “Landscape” is not used here; remaining uses are tied to protein folding (see counts below). |
| 6 | “The connection is not merely metaphorical” → delete | **RESOLVED** | Absent from the revised text. |
| 7 | Breathless TQFT conjunction → reorder, cut “directly” | **RESOLVED** | Single sentence links constructive 4CT → Kauffman/Penrose → TQFT; “directly” removed. |
| 8 | “A suite of” in abstract → cut | **RESOLVED** | Abstract says “We define eight energy functionals (including…)”. |
| 9 | Abstract energy list em-dash pair → parentheses | **RESOLVED** | List is in parentheses: “(including Magic Gem covariance, local entropy, surface tension rigidity, and defect interaction)”. |
| 10 | Abstract ST definition em-dash pair → parentheses | **RESOLVED** | Definition uses parentheses: “surface tension rigidity (the variance of normalized boundary size across Kempe chains)”. |

**Summary:** All ten items are **RESOLVED** in the reviewed files. No item remains partial or unaddressed for the specific wording called out earlier.

---

## Mechanical counts (revised files only)

**Em-dashes**

- **LaTeX `---` (em-dash):** none in `01-introduction.tex`; none in the abstract/body of `coverpage.tex`.
- **Unicode em dash (U+2014):** one occurrence in the **comment** on line 1 of `coverpage.tex` (`coverpage.tex — Title…`). It does not appear in the compiled manuscript text; optional cleanup for consistency with plain-ASCII comments.

**“Landscape”**

- **`01-introduction.tex`:** 1× — “protein folding landscapes” (contributions list).
- **`coverpage.tex`:** 1× — “protein folding energy landscapes” (abstract).
- **Total:** **2** — both in standard protein-folding terminology, not metaphorical overuse of “energy landscape” in the physics section.

---

## Fresh pass: possible new or residual LLM-adjacent tells

These are **minor** and do not reopen the earlier list; they are noted for polish if desired.

1. **Parallel “three” framing.** The abstract opens findings with “Three principal findings emerge” while the introduction contributions already feature “three discriminating signatures.” Not wrong, but slightly templated repetition; could vary one phrasing (e.g. “three patterns” / “three results”) if trimming duplication matters.

2. **Adverb “cleanly.”** “Local entropy cleanly discriminates” is confident and readable; some editors flag heavy -ly verdict adverbs in abstracts. Subjective; optional softening (“strongly,” “clearly” with data) only if the venue dislikes punchy claims.

3. **Rhetorical opener in “Why Physics?”** “What distinguishes safe paths from unsafe ones?” is a conventional section hook. Fine for a titled subsection; only a tell if the rest of the paper overuses rhetorical questions.

4. **Abstract density.** The added sentence on subsequent falsification at \(n \geq 10\) is substantive (good for honesty) and increases parenthetical load in one paragraph. Not an LLM tell per se; it reads like a careful authorial addition rather than filler.

5. **“We argue that”** in the physics subsection is measured hedging appropriate to a cross-domain claim — not a hedging cascade.

**No new issues found** matching the original classes: no hedging cascades, no false authority phrases, no restored corporate “suite” language, no em-dash pairs in the abstract or introduction body.

---

## Verdict

The revision **fully addresses** the prior Reviewer 2 list. **Em-dash tell patterns are cleared** from manuscript text in these two files; **“landscape”** appears twice, appropriately. A short optional pass could unify the comment header in `coverpage.tex` to ASCII and slightly de-duplicate “three … / three …” wording between abstract and introduction.

—Reviewer 2 (LLM writing tell detection), follow-up
