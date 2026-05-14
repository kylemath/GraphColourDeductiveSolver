# Follow-up review — Reviewer 1 (Mathematical Rigour)

**Manuscript:** revised `02-background.tex` and `03-methods.tex` (Kempe Reconfiguration Energy project).  
**Scope:** Map each prior finding to **RESOLVED**, **PARTIALLY RESOLVED**, or **NOT ADDRESSED**; note any **new** issues.

---

## Issue-by-issue verdicts

| Issue ID | Original concern | Verdict | Comment |
|----------|------------------|---------|---------|
| **1.1** | 4/5-color confusion in inductive case analysis | **RESOLVED** | Induction is clearly on a **4**-coloring of $G'$; the alternative route is explicitly a **5**-coloring of $G'$ with Kempe reduction to a 4-coloring. Cases 1–3 distinguish degree and “fewer than four distinct neighbor colors” vs “all four colors appear,” avoiding the earlier mix-up. |
| **1.2** | Proposition on Kempe/rotation falsely claimed a rotation “fixes orthogonal plane” | **RESOLVED** | `prop:kempe-rotation` states the correct action: exchange $\mathbf{v}_a \leftrightarrow \mathbf{v}_b$ and $\mathbf{v}_c \leftrightarrow \mathbf{v}_d$, fix $\mathbf{v}_5=\mathbf{0}$, with axis through edge midpoints and proof by explicit $R_{12}$ example. |
| **1.3** | “Six $180^\circ$ rotations generating $S_4$” — count, group, embedding | **RESOLVED** | Text now distinguishes **three** distinct $180^\circ$ rotations (axes from complementary edge pairs), identifies them with **$V_4 \subset \mathrm{SO}(3)$**, and separates **permutation** action (six transpositions generating **$S_4$**) from **rotational** symmetry (**$A_4$**), with explicit note on reflections vs rotations. |
| **1.4** | Chromatic polynomial formula wrong (extra exponential factor) | **RESOLVED** | `02-background` gives $P(G,q)=\lim_{\beta\to\infty} Z$ with standard $Z=\sum_\sigma e^{-\beta H(\sigma)}$; `03-methods` `rem:potts-chromatic` states the extended $h$-term limit counts **4**-colorings, not the full $P(G,q)$ — consistent and no spurious factor. |
| **2.1** | Opaque inner product computation | **RESOLVED** | `prop:tet-geom` proof spells out squared distance via coordinate differences, centroid, and inner product via sign/parity (“exactly one coordinate agrees in sign, two disagree”). |
| **2.2** | Proposition proof confused about “other” colors under swap | **RESOLVED** | Proof states exchange of the complementary pair, vacuity on a $(a,b)$-chain, and explicit $(1,2)$ calculation. |
| **3.1** | Protein folding analogy called “direct” | **RESOLVED** | Wording is **“By analogy (not formal equivalence)”** with explicit caution about continuous vs discrete settings. |
| **3.3** | TQFT / spin-1 / $6j$-symbol claims overstated | **RESOLVED** | Connection is framed as **suggestive**; **$6j$ / rigorous TV link** is explicitly **open**. Spin-1 is correctly tied to $\mathbb{R}^3$ / $\mathrm{SO}(3)$. |
| **3.4** | $2/3$ exponent unjustified | **RESOLVED** | `def:ruggedness` adds a clear caveat: classical $\mathbb{R}^3$ isoperimetric motivation, **no** rigorous graph-level justification, contrast with planar $1/2$ and expansion dependence. |
| **3.5** | Swendsen–Wang description too vague | **RESOLVED** | Fortuin–Kasteleyn percolation, cluster-wise recoloring, and structured contrast with deterministic two-color Kempe moves are spelled out. |
| **4.1** | $\rho$ notation conflict (charge vs rigidity) | **RESOLVED** | Charge density remains $\rho$; rigidity uses **$\Gamma$** with an explicit footnote-style sentence in `def:st-rigidity`. |
| **4.2** | “Electric field gradient” misnomer | **RESOLVED** | Renamed to **discrete electric field magnitude** via **max** over neighbors of $|\phi(v)-\phi(u)|$. |
| **4.3** | Sign convention change uncommented | **RESOLVED** | `def:potts-ham` cross-references `sec:phys-models` and states equivalence of penalizing monochromatic edges under the two conventions. |
| **5.1** | Unsafe swap “incident to” imprecise | **PARTIALLY RESOLVED** | `def:unsafe-swap` is more precise (merge of two chains **both** containing a neighbor of $v$). Residual ambiguity: “in some color pair involving $a$ or $b$” could still benefit from a one-line example or pointer to the census section. |
| **5.2** | Defect interaction sum domain ambiguous | **RESOLVED** | `def:defect-interaction` sums over **unordered** pairs $\{v,w\}$ with $c(v)=c(w)=5$, with $d_G$ graph distance. |
| **5.3** | Open vs closed neighborhood discrepancy | **RESOLVED** | Magic Gem uses **$N[v]$**; entropy uses **$N(v)$** with explicit remark and $p_{c(v)}=0$ for proper colorings. |
| **6.1** | Robertson cited for triangulation counts | **RESOLVED** | Pipeline cites **plantri**, Whitney, and **OEIS A000109** for triangulation counts (not Robertson for that purpose). |
| **7.1** | “Chromatic monotony” undefined | **NOT ADDRESSED** | `rem:mg-interp` still uses the phrase without definition (acceptable as minor editorial debt; still a gap for pedantic readers). |
| **7.2** | Color-5 “pulls centroid toward imbalance” oversimplification | **PARTIALLY RESOLVED** | The mechanism (zero vectors at color 5) is implicit; the sentence remains heuristic and could be sharpened (e.g., “reduces the number of nonzero summands / shifts the average”). |
| **7.3** | “Phase transition” used informally | **NOT ADDRESSED** | ALL-PATHS bullet still says **“phase transition”** without statistical-mechanics qualification (minor). |
| **7.4** | Eight functionals vs possible nine | **NOT ADDRESSED** | Introduction still claims **eight** functionals; no reconciliation if surface tension $\sigma/\bar\sigma$ are counted separately from $\Gamma$, etc. |

---

## New issues introduced or remaining risks

1. **Klein four-group wording (low risk):** The narrative correctly identifies three involutory rotations and $V_4$; a very picky reader might ask for an explicit statement that these three rotations **with identity** form $V_4$ (the text is clear enough in context).

2. **Unsafe swap vs graph distance in census (clarity):** No new mathematical error, but the disproved conjecture still uses **BFS-optimal** language while the census discusses **optimal paths** — ensure notation $d_{\mathrm{opt}}$ / $d_{\mathrm{safe}}$ is aligned everywhere in the full paper.

3. **Minor LaTeX/brace hygiene:** In `prop:tet-geom`, the enumerate label uses `[label=(\alph*)]` — confirm package (`enumitem`) is loaded in the master file to avoid build issues (not visible from section files alone).

4. **Residual informal language (carryover):** “Chromatic monotony,” “phase transition,” and the eight-vs-nine count remain the main **editorial** loose ends; none rises to the level of the original four critical errors.

---

## Bottom line

The revision **adequately addresses all four critical mathematical errors** and **substantially addresses the major and moderate issues**, with **5.1**, **7.2**, and the **minor 7.x** items still carrying small residual gaps. No **new critical** errors were identified in the revised sections reviewed here.

**Next steps (for authors):** (i) One clarifying sentence or example for **unsafe swaps**; (ii) define or replace **“chromatic monotony”**; (iii) footnote or rephrase **“phase transition”**; (iv) verify and, if needed, correct the **functional count** or the section heading.

---

*Reviewer 1 (Mathematical Rigour) — follow-up pass on revised `02-background.tex` and `03-methods.tex`.*
