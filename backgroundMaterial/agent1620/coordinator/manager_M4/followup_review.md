# Follow-up review: Discussion & Conclusion (Reviewer 4 — Structure, Redundancy, Speculation Control)

**Manuscript:** revised `05-discussion.tex` and `06-conclusion.tex` (KempeReconfigurationEnergy)  
**Date:** 2026-04-08

This note tracks the prior 11 issues, three residual concerns, and any new overstatement introduced by the revision.

---

## Status of prior issues (1–11)

| ID | Prior concern | Status | Notes |
|----|----------------|--------|--------|
| **1** | Redundant ~20-line restatement of findings in conclusion → compress to ~5-line summary | **RESOLVED** | Findings are now a short `\paragraph{Principal findings.}` block (three items, falsification noted). The conclusion is no longer dominated by a blow-by-blow repeat of the paper. |
| **2** | TQFT Basin–Sign as fact → “tempting to conjecture” + “no direct evidence” | **RESOLVED** | Explicit: “It is tempting to conjecture… but we have no direct evidence for this correspondence.” |
| **3** | TQFT remark: SO(3) rigidity + Colin de Verdière → “We speculate”, cut CdV | **RESOLVED** | Remark opens with “We speculate…”; CdV chain removed; falsification of ST rigidity is integrated. |
| **4** | Sheaf section purely definitional → disclaimer | **RESOLVED** | Clear upfront: potential outline, no paper results depend on it, no sheaf-theoretic theorems proved. |
| **5** | Rigidity → \(H^1\) + planar-positivity overreach → qualify | **RESOLVED** | “Suggestive (but unproven) analogy,” speculative \(H^1\) link with “not verified,” “tentatively define,” and open status of implications. |
| **6** | Chromatic Basin hedging dropped mid-paragraph → keep “We speculate” | **RESOLVED** | Paragraph begins with “We speculate…” and ends with “analogy is suggestive but unverified.” |
| **7** | Beraha remark → replace “should be most pronounced” with honest “no evidence” | **RESOLVED** | Remark states explicitly that there is “no evidence connecting the two.” |
| **8** | Discharging + falsified ST → falsification caveat | **RESOLVED** | Dedicated sentences on falsification of ST rigidity and why the discharging-style hope is undermined. |
| **9** | MG reducibility criterion untested → “We have not tested this” | **RESOLVED** | Closing sentence: “We have not tested this idea computationally.” |
| **10** | Open questions overstatements (three sub-issues) → downgrade | **RESOLVED** | Questions are framed with limits: \(n=10\) “consistent with” but ST fails; TQFT item is “conjectured” and requires “substantial additional work”; composite potential is a “major undertaking beyond the scope.” |
| **11** | “Broader perspective” extraordinary claim → rewrite entirely | **RESOLVED** | Replaced by a modest closing: descriptive tools, what persists vs. falsified, speculative connections, no resolution claimed. |

---

## Residual concerns from the first review

| ID | Residual concern | Status | Notes |
|----|------------------|--------|--------|
| **R1** | TQFT bullet: “precisely” for 6j correspondence — theorem vs. analogy | **NOT ADDRESSED** | The Kempe-swap bullet still reads: the rotation “is **precisely** the action of a recoupling coefficient in the Turaev–Viro state sum.” Basin–Sign language is now hedged elsewhere, but this bullet retains maximal-confidence wording without citing a proved equivalence. **Suggestion:** soften to “can be modeled as” / “is analogous to” or cite a precise theorem if one exists. |
| **R2** | Discharging analogy: analogies read as correspondences | **PARTIALLY RESOLVED** | Wording uses “analogous to,” “continuous analog,” and “potential locations,” which is better. The list structure still parallels discharging steps one-for-one; a one-line reminder that these are heuristic parallels (as in the TQFT/chromatic blocks) would close the gap. |
| **R3** | Opening conclusion lists all eight functionals by name (overlap with methods) | **NOT ADDRESSED** | The first paragraph still names the full suite (Potts, Magic Gem, electrostatic, surface tension, entropy, ruggedness, defect interaction). **Suggestion:** replace with “the eight functionals of Section~\ref{sec:methods}” or a single umbrella phrase to avoid repeating the methods catalog. |

---

## New speculation or overstatement from the revision?

**No major new speculative claims** were introduced relative to the prior review’s targets. The revision is globally more careful.

**Minor watchpoints (not necessarily errors):**

- **Conclusion opening:** “grounded in the tetrahedral color embedding that maps the constructive Four Colour Theorem into the language of \(\mathrm{SO}(3)\) gauge theory” is a strong framing sentence. It is not new hedging; if the introduction/methods do not justify “gauge theory” at that level of specificity, consider softening to “\(\mathrm{SO}(3)\) / rigid-motion viewpoint” or similar.
- **Discussion TQFT bullets (first item block):** The Penrose/Kauffman items are factual; the Kempe/6j item remains the main precision risk (see R1).

---

## Summary judgment

The revision **substantially addresses** the prior review: redundancy in the conclusion is fixed, Basin–Sign and related claims are properly hedged, sheaf and chromatic passages are qualified, Beraha and MG testing gaps are honest, ST falsification is integrated in both discussion and conclusion, open questions are toned down, and the closing “broader perspective” is appropriate.

**Remaining work for a clean pass on Reviewer 4’s checklist:** (i) resolve **R1** by adjusting or justifying “precisely” in the 6j bullet; (ii) optionally trim **R3** by not re-listing all eight functionals in the conclusion; (iii) optional one-line hedge for **R2** on discharging.

---

## Next steps (concrete)

1. Edit `05-discussion.tex` TQFT item on Kempe swaps / \(6j\) symbols: replace or support “precisely.”
2. Optionally shorten `06-conclusion.tex` opening paragraph to reference Section `\ref{sec:methods}` instead of enumerating functionals.
3. Optional: add a single sentence in `\subsection{Connection to Discharging}` that these are motivating analogies, not established graph–discharging equivalences.

**Feasibility of clearing remaining items:** High (local wording edits only).
