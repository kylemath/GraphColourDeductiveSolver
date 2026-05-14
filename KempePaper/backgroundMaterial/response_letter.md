# Point-by-Point Response to Reviewers

**Manuscript:** *Physical Energy Functionals for Kempe Chain Reconfiguration: Spin Glasses, Magic Gems, and the Four Colour Theorem*

**Author:** Kyle Elliott Mathewson

**Date:** 2026-04-08

---

We thank all three reviewers and the editor for their careful, constructive, and substantive reports. We have revised the manuscript to address every concern raised. Below we respond point by point, organized by reviewer, indicating exactly what was changed and where.

---

## Response to Reviewer A (Structural Graph Theory Referee)

### A1. "The paper is too thin on theorem-level advances."

**Response:** We agree that the paper's strengths are exploratory and computational rather than theorem-driven. Rather than adding a theorem we cannot yet prove, we have reframed the paper honestly as an exploratory computational study. The abstract (`coverpage.tex`) now opens with "Computational experiments on the 48 colorings..." rather than presenting the findings as general structural results. The contributions list (`01-introduction.tex`, item (iii)) now explicitly says "computational signatures observed at $n = 9$" rather than implying general properties. We believe this reframing is more appropriate for the current state of the work.

### A2. "The strongest empirical claims are based on only 48 counterexample colorings."

**Response:** The abstract now explicitly states the sample size: "Computational experiments on the 48 colorings of two counterexample triangulations at $n = 9$ vertices yield three observations." This makes the scope clear from the first page.

**Changed in:** `coverpage.tex` (abstract, lines 26–27).

### A3. "The abstract and introduction oversell the TQFT / Penrose / gauge-field connection."

**Response:** Three specific changes address this:

1. **Abstract** (`coverpage.tex`): "linking the constructive Four Colour Theorem to topological quantum field theory" → "suggesting geometric connections to topological quantum field theory that remain to be made rigorous."

2. **Introduction, "Why Physics?" subsection** (`01-introduction.tex`): "the entire reconfiguration process becomes a walk through a space of SO(3)-valued gauge fields on the graph. This links the constructive 4CT to Kauffman's reformulation..." → "reconfiguration can be viewed metaphorically as a walk through a space of SO(3)-valued fields on the graph. This picture is reminiscent of Kauffman's reformulation ... though making these connections precise remains an open problem."

3. **Outline** (`01-introduction.tex`): "develops connections" → "explores speculative connections."

### A4. "A conjecture that is already stated to fail is still given major narrative weight."

**Response:** The contributions list (`01-introduction.tex`, item (iv)) now immediately notes the falsification: "We note that this conjecture was subsequently falsified at $n \geq 10$." The conclusion (`06-conclusion.tex`) has been restructured to lead with the two surviving findings (entropy, kinetic traps) and treat surface tension rigidity as a "third candidate signal ... subsequently falsified."

**Changed in:** `01-introduction.tex` (contributions list), `06-conclusion.tex` (Principal findings paragraph).

### A5. "Separate claims into proved / computationally supported / conjectural / falsified."

**Response:** The revised discussion section (`05-discussion.tex`) now opens with an explicit statement: "None of the correspondences below have been made rigorous; they are presented as potential research directions, not as established results." The TQFT subsection title now includes "[Speculative]" and opens with "The observations in this subsection are heuristic analogies; no rigorous correspondence has been established." The limitations section now includes a new item 6 on code–paper definition alignment.

**Changed in:** `05-discussion.tex` (opening paragraph, TQFT subsection title and lead sentence, new limitation item 6).

### A6. Alternative venue suggestion.

**Response:** We appreciate this advice and are considering an experimental mathematics or reconfiguration-focused venue for resubmission. The revised framing is intended to be appropriate for such outlets.

---

## Response to Reviewer B (Combinatorics + Statistical Mechanics Referee)

### B1. "The extended Potts Hamiltonian collapses to defect counting on proper colorings."

**Response:** This is already acknowledged in the paper at `03-methods.tex` (following Definition 3.6): "For proper colorings, the first term vanishes identically ($J$-term $= 0$), so the Hamiltonian reduces to $H(c) = h \cdot |\{v : c(v) = 5\}|$." We have not changed this text, as the reviewer correctly notes it is already stated. No additional revision needed.

### B2. "TQFT, Penrose, and gauge-field language is much stronger rhetorically than the evidence supports."

**Response:** See A3 above. All three key passages have been weakened. Additionally, the discussion section (`05-discussion.tex`) now opens with an explicit disclaimer and the TQFT subsection carries a "[Speculative]" label.

### B3. "The surface-tension storyline is weakened by the paper's own admission."

**Response:** See A4 above. The narrative now leads with what survived and treats surface tension rigidity as a falsified hypothesis documented for the record.

### B4. "Several energies are ad hoc probes rather than physically derived laws."

**Response:** The revised discussion opening (`05-discussion.tex`) now frames all connections as "potential research directions, not established results." The new limitation item 6 (`05-discussion.tex`) explicitly notes that implementations use different conventions than the paper definitions and characterizes the functionals as exploratory.

### B5. "Tone down the abstract sharply."

**Response:** Done. The abstract (`coverpage.tex`) no longer claims a TQFT link, uses "observations" instead of "findings," explicitly states the sample size, and leads with the falsification of finding (3).

### B6. "Give distributions, effect sizes, and fuller aggregate summaries."

**Response:** This is a fair request that we have not fully addressed in this revision. The current text reports means for the entropy discrimination. Adding full distributional analysis would require regenerating figures and extending the computational pipeline, which we flag as future work. We have added the sample size to the abstract to make the evidence base transparent.

### B7. "Any wording that suggests a rigorous TQFT link already exists" must be toned down.

**Response:** Done across `coverpage.tex`, `01-introduction.tex`, and `05-discussion.tex`. See A3 above.

### B8. "Any language implying the energy functionals have isolated a proof mechanism."

**Response:** The abstract now says "observations" rather than "findings." The discussion opening explicitly says the functionals "do not, by themselves, prove that safe paths exist."

### B9. "Surface tension rigidity as an enduring structural law" without noting failure.

**Response:** Every mention of surface tension rigidity now immediately references the falsification. See A4.

---

## Response to Reviewer C (Computational Graph Theory Referee)

### C1. "Triangulation-generation mismatch: manuscript says plantri, code uses face-splitting + edge-flipping."

**Response:** This was the most concrete factual error in the manuscript. The computational pipeline paragraph (`03-methods.tex`, Section 3.9) has been completely rewritten. It now accurately describes the actual algorithm:

> "Triangulations were generated by an inductive enumeration: starting from $K_4$, each $(n-1)$-vertex triangulation is extended to $n$ vertices by splitting every triangular face ... Within each vertex count $n$, the set is then closed under edge flipping until no new isomorphism classes appear; isomorphism filtering uses `networkx.is_isomorphic`. The resulting counts were verified against the OEIS sequence A000109 (which agrees with `plantri`'s published counts, providing independent confirmation)."

**Changed in:** `03-methods.tex` (Section 3.9, Computational Pipeline).

### C2. "Figure-generation pipeline mismatch."

**Response:** This is a valid concern about the repository's documentation, not the manuscript text. The manuscript itself does not describe the figure pipeline in detail. We acknowledge this issue and plan to clean up the `README.md` and `generate_energy_figures.py` paths in a subsequent repository update. The manuscript revisions do not affect the figures themselves.

### C3. "Definition drift between paper and code."

**Response:** Three specific definition mismatches have been addressed with new remarks in `03-methods.tex`:

1. **Surface tension** (all boundary edges vs. foreign-color-only edges): New Remark 3.12 (`rem:st-boundary`) explains: "Definition [surface tension] counts all edges from $K$ to $V \setminus K$... The computational implementation restricts the count to edges whose far endpoint carries a color outside the active pair $(a,b)$... The all-boundary definition is the one used for the rigidity analysis in Section 4."

2. **Ruggedness** ($|K|^{2/3}$ vs. $|K|$): New Remark 3.14 (`rem:ruggedness-impl`) explains: "The computational implementation uses the simpler linear ratio $\sigma(K)/|K|$ ... All figures in Section 4 report the linear variant. The theoretical definition retains the $2/3$ exponent as the natural isoperimetric baseline; for the small chains in our data ($|K| \leq 9$), the two normalizations are monotonically related."

3. **Entropy** ($\log$ vs. $\log_2$): The definition (`def:entropy`) now explicitly uses $\log_2$ with the note: "we use $\log_2$ throughout; the base choice affects the scale of entropy values but not their ordering across colorings."

Additionally, a new limitation item 6 in `05-discussion.tex` addresses code–paper alignment globally.

**Changed in:** `03-methods.tex` (new Remarks `rem:st-boundary` and `rem:ruggedness-impl`; updated entropy definition), `05-discussion.tex` (new limitation item 6).

### C4. "Artifact gap for larger-scale claims."

**Response:** We have added a reproducibility paragraph to the conclusion (`06-conclusion.tex`): "All computational results reported in this paper can be reproduced from the accompanying code repository. Triangulation counts at each order were independently verified against OEIS sequence A000109." We plan to add a frozen artifact bundle (JSON summaries for all 48 counterexamples and the $n = 10$ census) in a subsequent repository update.

### C5. "Rewrite computational pipeline to match actual code."

**Response:** Done. See C1.

### C6. "Add a compact reproducibility appendix."

**Response:** Partially addressed. The new reproducibility paragraph in the conclusion references the repository. A full appendix mapping each figure to a specific script invocation is planned for a subsequent version.

### C7. "Create and commit a stable artifact bundle."

**Response:** Planned for a subsequent repository update. This is a code/repository task rather than a manuscript revision.

### C8. "Explicitly document which module definitions are authoritative."

**Response:** Done. See C3. Each new remark explicitly states which definition governs the reported results.

### C9. "Add one regression-style check that recomputes headline paper numbers."

**Response:** Planned for a subsequent repository update. The existing test suite (`tests/test_plan2.py`, `tests/test_physical_analogies.py`) covers correctness of the core operations and triangulation counts, but does not yet regression-test the specific headline numbers from the paper.

---

## Response to Editor Synthesis

### E1. "Decide what paper this really is."

**Response:** We have chosen to position the paper as an exploratory computational study with physical heuristics, not as a theorem-driven combinatorics paper. The revised abstract, introduction, and discussion all reflect this positioning.

### E2. "Rewrite the abstract and introduction to remove any suggestion that a rigorous TQFT bridge has been established."

**Response:** Done. See A3.

### E3. "Split claims into proved / computationally supported / speculative / falsified."

**Response:** The revised discussion section opens with explicit framing. The TQFT subsection is labeled "[Speculative]." The contributions list qualifies items (iii) and (iv). The conclusion leads with survivors and explicitly reports the falsification.

### E4. "Fix the methods section so the triangulation-generation description matches the code."

**Response:** Done. See C1.

### E5. "Clean up the figure pipeline."

**Response:** Planned for a subsequent repository update. See C2.

### E6. "Clarify which definitions are authoritative."

**Response:** Done. See C3.

### E7. "Archive the exact n=9 and n=10 artifacts."

**Response:** Planned for a subsequent repository update. See C7.

### E8. "Add at least one real theorem if resubmitting to a combinatorics journal."

**Response:** Acknowledged. The current revision targets an experimental mathematics or reconfiguration venue. If we later target a combinatorics journal, we will pursue a theorem about local entropy or kinetic trap structure.

---

## Summary of All Changes

| File | Changes |
|------|---------|
| `coverpage.tex` | Toned down TQFT claim; added sample size; reframed "findings" as "observations"; explicit falsification note |
| `sections/01-introduction.tex` | Removed "gauge fields" language; marked TQFT as open problem; qualified contributions (iii) and (iv); "explores speculative connections" |
| `sections/03-methods.tex` | Rewrote pipeline to match actual code; added Remark on surface tension boundary convention; added Remark on ruggedness implementation; clarified entropy log base |
| `sections/05-discussion.tex` | Added speculative framing to opening; "[Speculative]" label on TQFT subsection; weakened Magic Gem / Penrose language; new limitation item 6 on code–paper alignment |
| `sections/06-conclusion.tex` | Restructured principal findings (survivors first, falsified third); weakened TQFT open question; added reproducibility paragraph |

All changes compile cleanly (19 pages, zero warnings, zero undefined references).
