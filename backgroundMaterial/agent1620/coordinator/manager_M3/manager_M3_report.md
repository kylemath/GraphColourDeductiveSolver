# Reviewer 3 Report: Empirical Claims and Internal Consistency

**Reviewer:** Reviewer 3 (Empirical Claims & Internal Consistency)
**File reviewed:** `paper/sections/04-results.tex`
**Date:** 2026-04-08

---

## Summary

Nine substantive edits were applied to `04-results.tex`. The section had no arithmetic errors but contained multiple precision, scope, and editorializing issues. The most serious was a factually incorrect trajectory description ("smooth descent" for a non-monotone path). All energy values lacked units/normalization context. Several claims lacked explicit scope (which colorings? which triangulation? an average or a single instance?).

---

## Findings and Edits

### 1. Table Consistency — PASS

Table 1 reports 24 CE colorings for $T_{9,25}$ and 24 for $T_{9,35}$. Total = 48. Every textual reference to "48 counterexamples" in the file is consistent:
- Line 10: "all 48 counterexample colorings" ✓
- Line 167 (now 177): "all 48 counterexample colorings (24 in $T_{9,25}$, 24 in $T_{9,35}$)" ✓
- Line 162 (now 172): "within the 48 counterexamples at $n = 9$" ✓

No edits required.

### 2. Energy Values — FIXED (3 issues)

**Issue 2a: No units or normalization context.** The Magic Gem trajectory gave values $0.619 \to 0.556 \to 1.224$ (unsafe) and $0.619 \to 1.481 \to 1.077 \to 1.992$ (safe) with no indication of units or normalization.

**Fix:** Added "(dimensionless; defined in Section~\ref{sec:mg-energy})" to the paragraph opening. The global $E_{\mathrm{MG}}(G, c) = \sum_v E_{\mathrm{MG}}(v, c)$ is a sum of squared norms — dimensionless by construction.

**Issue 2b: "Smooth descent" is factually wrong.** The safe trajectory $0.619 \to 1.481 \to 1.077 \to 1.992$ is non-monotone: step 2 descends ($1.481 \to 1.077$, $-0.404$) but step 3 ascends ($1.077 \to 1.992$, $+0.915$). The original text claimed "subsequent steps find a smooth descent to a 4-coloring." This is incorrect.

**Fix:** Changed parenthetical label from "(ridge then settle)" to "(ridge then non-monotone)." Replaced the prose with an explicit step-by-step account: energy increases by $0.862$, decreases by $0.404$, reaches the 4-coloring at $1.992$. Removed the false "smooth descent" claim.

**Issue 2c: Single coloring vs. aggregate.** The trajectory values are for a single representative coloring, but the text presented them as if they characterized all counterexamples. The figure caption correctly said "a representative counterexample coloring" but the paragraph text did not.

**Fix:** Added "The following values are for a single representative counterexample coloring in $T_{9,25}$."

### 3. Entropy Values — FIXED (1 issue)

**Arithmetic check:** $2.055 - 1.784 = 0.271$. ✓

**Issue:** The $\bar{S}$ notation (overbar) implies an average, and the text said "For $T_{9,25}$:" — but it was ambiguous whether this averaged over all 24 CE colorings or was for one specific coloring.

**Fix:** Changed to "For $T_{9,25}$ (averaged over all 24 counterexample colorings):"

### 4. Surface Tension Scope — FIXED (2 issues)

**Issue 4a:** The Surface Tension Rigidity paragraph (Section 4.2) presented $\rho_{ab}(c_{\text{unsafe}}) = 0$ and $\rho_{ab}(c_{\text{safe}}) > 0$ without specifying scope. The reader couldn't tell if this held for one coloring, one triangulation, or all 48 CEs. (The explicit "all 48" scope only appeared later in the Evidence paragraph.)

**Fix:** Prepended "Across all 48 counterexample colorings at $n = 9$," to the paragraph.

**Issue 4b:** "maximally rigid, inflexible configuration" — double superlative with identical meaning.

**Fix:** Changed to "rigid configuration with no structural variability."

### 5. Ridge Height — FIXED (2 issues)

**Issue 5a:** "$\Delta E_{\mathrm{MG}} \approx 0.86$ (for $T_{9,25}$) to $0.96$ (for $T_{9,35}$)" reads as a continuous range, but these are two discrete values for two specific triangulations.

**Fix:** Changed to "$\Delta E_{\mathrm{MG}} = 0.862$ for $T_{9,25}$ and $0.96$ for $T_{9,35}$."

**Issue 5b:** Precision mismatch. The trajectory gives $1.481 - 0.619 = 0.862$ to 3 decimal places, but the ridge height was stated as "$\approx 0.86$" (2 decimal places). The "$\approx$" is unnecessary — $0.862$ follows exactly from the stated trajectory values.

**Fix:** Changed "$\approx 0.86$" to "$= 0.862$." Added "(each computed from a representative counterexample coloring in the respective triangulation)" for scope.

### 6. ALL-PATHS Census (87.6%) — NOT IN SCOPE (noted)

The claim "87.6% of (graph, coloring, vertex) triples are universal" appears in `02-background.tex` (line 90), not in `04-results.tex`. Two issues exist:

1. **Missing denominator.** The percentage is unverifiable without knowing the total number of (graph, coloring, vertex) triples at $n \leq 8$. The text should state this count.
2. **"striking pattern"** (line 88 of background) — editorializing adjective that should be cut.
3. **"remarkably small"** (line 100 of background) — vague modifier that should be replaced with a quantified comparison or cut.

**No edit applied** (outside scope of `04-results.tex`). These are flagged for the reviewer handling `02-background.tex`.

### 7. Falsification Remark — FIXED (3 issues)

**Issue 7a:** "Falsified by subsequent exhaustive computation at $n \geq 10$" — no specifics on what was found. How many counterexamples? What was the falsification mechanism?

**Fix:** Added ": instances with $\rho_{ab} = 0$ for safe swaps were identified, violating the conjecture's implication." This makes the falsification direction explicit (the conjecture claims $\rho_{ab} = 0 \implies$ unsafe; falsification = finding $\rho_{ab} = 0$ with a safe swap).

**Residual concern:** The exact count of counterexamples at $n \geq 10$ is still missing. If this data exists, it should be stated. If it doesn't, the remark should say "at least one instance."

**Issue 7b:** "holds perfectly at $n = 9$" — "perfectly" is redundant with "holds for all 48 counterexamples."

**Fix:** Changed to "holds for all 48 counterexamples at $n = 9$."

**Issue 7c:** "it breaks down at larger scales" — vague.

**Fix:** Changed to "it does not generalize to $n \geq 10$."

### 8. LLM Imprecision Patterns — FIXED (3 instances in results)

| Original | Replacement | Location |
|---|---|---|
| "cleanest discrimination" | "strongest discrimination ... among the eight functionals tested" | §4.2, Local Entropy |
| "clearest separation" | "largest separation between safe and unsafe distributions" | Fig. 1 caption |
| "precisely analogous" | "analogous" | §4.3, kinetic trap |

Two additional instances found outside `04-results.tex` (not edited):
- "striking pattern" in `02-background.tex` line 88
- "remarkably small" in `02-background.tex` line 100

---

## Verified Arithmetic

| Claim | Check | Status |
|---|---|---|
| $24 + 24 = 48$ CE colorings | Matches table and all text references | ✓ |
| $\Delta S = 2.055 - 1.784 = 0.271$ | Correct | ✓ |
| Unsafe step 1 delta: $0.619 - 0.556 = 0.063$ | Added to text | ✓ |
| Unsafe barrier: $1.224 - 0.556 = 0.668$ | Added to text | ✓ |
| Safe ridge: $1.481 - 0.619 = 0.862$ | Added to text; fixes $\approx 0.86$ | ✓ |
| Safe step 2 delta: $1.481 - 1.077 = 0.404$ | Added to text | ✓ |
| $d_{\text{safe}} - d_{\text{opt}} = 3 - 2 = 1$ | Matches table and text | ✓ |

---

## Residual Issues (require author response)

1. **$n \geq 10$ counterexample count.** The falsification remark should state how many (graph, coloring, vertex) triples at $n \geq 10$ violate the conjecture. If the count is unknown, say "at least one instance."

2. **87.6% denominator.** The ALL-PATHS census in `02-background.tex` gives a percentage without a denominator. The total number of triples at $n \leq 8$ should be reported.

3. **$T_{9,35}$ ridge height.** The ridge height $\Delta E_{\mathrm{MG}} = 0.96$ for $T_{9,35}$ is stated without showing the underlying trajectory. For verifiability, the full trajectory for $T_{9,35}$ should either be shown (as done for $T_{9,25}$) or the starting energy should be given so the reader can reconstruct the calculation.

4. **Entropy: single representative vs. all 24.** The trajectory paragraph (Magic Gem) now correctly says "single representative coloring." The entropy paragraph says "averaged over all 24." The paper should clarify whether this average has low or high variance — a mean of $2.055$ is less informative if the standard deviation is $0.5$ than if it is $0.01$.

5. **"paradoxically" (line 60).** The word "paradoxically" in the entropy interpretation is retained. It is defensible here (the paradox is genuine and explained in the next sentence), but a referee at a skeptical journal may flag it. Consider replacing with "counterintuitively" or just removing it.
