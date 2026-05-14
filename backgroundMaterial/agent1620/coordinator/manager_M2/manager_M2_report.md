# Manager M2 Report — LLM Writing Tell Detection

**Reviewer:** Reviewer 2 (LLM Writing Tell Detection)
**Files reviewed:** `01-introduction.tex`, `coverpage.tex`
**Date:** 2026-04-08

---

## Summary

Ten edits across two files. The introduction had the bulk of the problems: six em-dash splices, one "not merely X" construction, one padding sentence with false authority, one double-negative hedging construction, one paragraph with two instances of "landscape" plus vague phrasing, and one breathless multi-conjunction sentence. The coverpage abstract had one corporate filler phrase ("a suite of") and two sets of em-dash pairs.

No issues were found with: hedging cascades, false authority phrases ("it is well established"), or repetitive list template structure. The enumerated contributions list (§1.4) is genuinely varied in structure. The abstract is dense with specific content and does not read as promotional.

Final "landscape" count after edits: 2 (both in the technical phrase "protein folding [energy] landscapes," which is standard terminology in biophysics). Before edits: 4.

---

## Issues Found and Fixes Applied

### 1. Em-dash pair in opening sentence (intro, line 5–6)

**Pattern:** Unnecessary em-dashes (#9)

**Before:**
```latex
The Four Colour Theorem (4CT) — every planar graph admits a proper
$4$-coloring — was first proved by Appel and Haken~\cite{appel1977}
```

**After:**
```latex
The Four Colour Theorem (4CT), that every planar graph admits a proper
$4$-coloring, was first proved by Appel and Haken~\cite{appel1977}
```

**Rationale:** Standard parenthetical commas are sufficient. The em-dashes add visual noise to the very first sentence.

---

### 2. "Long and distinguished pedigree" + em-dash (intro, line 16–20)

**Patterns:** Padding sentence (#7), false authority (#4), unnecessary em-dash (#9)

**Before:**
```latex
This approach has a long and
distinguished pedigree — Kempe's original 1879 ``proof'' was exactly
this strategy, and Heawood's 1890 counterexample showed only that a
particular Kempe swap could merge two chains, not that the entire
strategy fails.
```

**After:**
```latex
Kempe's 1879 ``proof'' used exactly
this strategy; Heawood's 1890 counterexample showed only that a
particular swap could merge two chains, not that the strategy itself
fails.
```

**Rationale:** "Long and distinguished pedigree" is adjective-laden padding. The pedigree is Kempe (1879) and Heawood (1890) — just state the facts. Removed the em-dash, tightened "Kempe's original" to "Kempe's" (year already implies original), and "particular Kempe swap" to "particular swap" (Kempe is already the context).

---

### 3. Em-dash pair around parenthetical (intro, line 24–26)

**Pattern:** Unnecessary em-dashes (#9)

**Before:**
```latex
one must show that the 5-coloring of $G - v$ can be reconfigured —
via a sequence of Kempe swaps — into a coloring where two neighbors of
```

**After:**
```latex
one must show that the 5-coloring of $G - v$ can be reconfigured,
via a sequence of Kempe swaps, into a coloring where two neighbors of
```

**Rationale:** Commas work fine here. The em-dashes add false drama to a straightforward parenthetical.

---

### 4. Double-negative hedging + em-dash (intro, line 40–42)

**Patterns:** Hedging (#3), unnecessary em-dash (#9)

**Before:**
```latex
This disproof, however, is not a disproof of the constructive strategy
itself. In every counterexample, \emph{safe} non-optimal paths exist —
they simply require one or two extra steps.
```

**After:**
```latex
The counterexamples refute only the optimality claim, not the
constructive strategy itself: in every case, \emph{safe} non-optimal paths
exist, requiring one or two extra steps.
```

**Rationale:** "This disproof is not a disproof of" is an awkward double-negative that reads like the writer is nervous. The rewrite is a direct positive assertion. Merged two sentences into one; eliminated the em-dash.

---

### 5. "Why Physics?" opening paragraph — padding, em-dashes, "landscape" overuse, vague claim (intro, line 50–56)

**Patterns:** Padding (#7), unnecessary em-dashes (#9, two instances), "landscape" overuse (#10), vague phrasing

**Before:**
```latex
The existence of safe paths raises the question: \emph{what
distinguishes safe paths from unsafe ones?} If we view the
reconfiguration graph as a discrete energy landscape — each coloring
assigned an energy by some functional — then safe and unsafe paths
correspond to different trajectories through this landscape. We propose
that ideas from statistical physics, specifically anti-ferromagnetic
spin models and disordered systems, provide the right language.
```

**After:**
```latex
What distinguishes safe paths from unsafe ones? If we assign each
coloring an energy via some functional, the reconfiguration graph becomes
a discrete energy surface, and safe versus unsafe paths trace distinct
trajectories. We argue that anti-ferromagnetic spin models and disordered
systems provide the discriminating tools.
```

**Rationale:** Five changes: (a) Cut the padding lead-in "The existence of safe paths raises the question:" — the question can stand on its own under the "Why Physics?" heading. (b) Eliminated two em-dash splices. (c) Changed "landscape" to "surface" (was 4 uses across both files, now 2). (d) Cut "through this landscape" (second "landscape" instance). (e) Replaced vague "provide the right language" with "provide the discriminating tools" — the paper uses these models to discriminate safe from unsafe paths, so say that.

---

### 6. "Not merely metaphorical" — deleted (intro, line 58)

**Pattern:** "Not merely X, but Y" construction (#2)

**Before:**
```latex
The connection is not merely metaphorical. A proper $k$-coloring of a
graph $G$ is precisely a ground state of the anti-ferromagnetic Potts
model on $G$ at zero temperature.
```

**After:**
```latex
A proper $k$-coloring of a
graph $G$ is precisely a ground state of the anti-ferromagnetic Potts
model on $G$ at zero temperature.
```

**Rationale:** The single most recognizable LLM tell in the paper. The three sentences that follow (Potts ground state, chromatic polynomial = partition function, Kempe swap = Swendsen-Wang update) already prove the connection is exact. The preamble sentence adds no information and screams "an LLM wrote this."

---

### 7. Breathless TQFT conjunction (intro, line 71–74)

**Pattern:** Over-enthusiastic conjunctions (#6)

**Before:**
```latex
This connects the constructive 4CT directly to
topological quantum field theory (TQFT), and specifically to
Kauffman's reformulation of the 4CT via the Penrose
evaluation~\cite{kauffman1990}.
```

**After:**
```latex
This links the constructive 4CT to Kauffman's reformulation via the
Penrose evaluation~\cite{kauffman1990} and, more broadly, to
topological quantum field theory (TQFT).
```

**Rationale:** The original packs "directly to X, and specifically to Y" into one breathless sentence — an LLM pattern of escalating grandiosity. The rewrite puts the specific, citable connection (Kauffman/Penrose) first and the broader umbrella (TQFT) second, ordered from concrete to general. Cut the unnecessary intensifier "directly."

---

### 8. "A suite of" — coverpage abstract (line 14)

**Pattern:** Padding (#7), corporate/marketing language

**Before:**
```latex
We introduce a suite of physical energy functionals for the Kempe chain
```

**After:**
```latex
We introduce physical energy functionals for the Kempe chain
```

**Rationale:** "A suite of" is corporate product-launch language. The abstract already says "eight" later; no need for a vague quantifier up front.

---

### 9. Em-dash pair in abstract — energy functional list (coverpage, line 22–24)

**Pattern:** Unnecessary em-dashes (#9)

**Before:**
```latex
We define eight energy functionals — including Magic Gem
covariance, local entropy, surface tension rigidity, and defect
interaction — and evaluate them on the first known counterexamples to
```

**After:**
```latex
We define eight energy functionals (including Magic Gem
covariance, local entropy, surface tension rigidity, and defect
interaction) and evaluate them on the first known counterexamples to
```

**Rationale:** Parentheses are the correct punctuation for an inline list within a sentence.

---

### 10. Em-dash pair in abstract — surface tension definition (coverpage, line 30–31)

**Pattern:** Unnecessary em-dashes (#9)

**Before:**
```latex
surface tension rigidity — the variance of normalized boundary
size across Kempe chains — provides a combinatorial signature of
```

**After:**
```latex
surface tension rigidity (the variance of normalized boundary
size across Kempe chains) provides a combinatorial signature of
```

**Rationale:** Same as #9. A parenthetical definition belongs in parentheses.

---

## Patterns NOT found (clean)

| Pattern | Status |
|---|---|
| Hedging cascades ("may potentially...could possibly") | Not present |
| False authority ("It is well established that") | Not present |
| Repetitive list structure (every item same template) | Contribution list varies structure — clean |
| Abstract selling rather than summarizing | Abstract is content-dense — clean |
| "landscape" > 2 uses | Reduced from 4 to 2 (both standard technical usage) |

## Net effect

- **Words cut:** ~65 (from ~870 to ~805 across both files)
- **Em-dashes eliminated:** 8 (5 pairs + 2 singles → 0 remaining)
- **"Not merely" constructions removed:** 1
- **Padding sentences deleted:** 2 ("long and distinguished pedigree," "not merely metaphorical")
- **Vague claims replaced with specific ones:** 1 ("provide the right language" → "provide the discriminating tools")
