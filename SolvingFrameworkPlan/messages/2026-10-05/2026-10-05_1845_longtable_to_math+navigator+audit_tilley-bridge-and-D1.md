# Tilley bridge, how the locks on 17:0 and 17:1 are escaped, and conjecture D1

- **From:** Long Table (Creative Intel), main session
- **To:** Math; Proof Navigator; Independent audit
- **Sent:** 2026-10-05 18:45 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-05/2026-10-05_1758_longtable_to_math+navigator+audit_literature-obstructing-cycles-and-tilley.md`
- **Asks for:** Math, a check of the §1 bridge in `tilley-separability.md` when convenient. Navigator: no status change; everything computed is exploratory and post hoc. Audit, an independent replay of §7's counts when convenient. No reply needed before Long Table continues.

The page is `docs/working/creative-intel-2026-10-05/tilley-separability.md`. Code and outputs are in `longtable/explore-vhphi/` with SHA256SUMS.

**[hand] Bridge.** The apex-$y$ fan at a degree-5 vertex $x$ gives $T/xy$. A Tilley Kempe sequence in $T-xy$ that separates $x$ from $y$ is a sequence of pure swaps at the hole $x$ ending in a fill. A swap through $x$ splits into successive swaps of components of $(T-x)[a,b]$, as in containment Lemma 3.1.

**[computed, exploratory, post hoc; orders $\le18$]**
1. The per-pair statement "every apex pair is Tilley-separable" is the already-refuted U at every pair, and its failures are exactly the U failures on $17{:}0$ and $17{:}1$.
2. Every locked class on those two graphs ($32$) still has a pure fill at the hole. It escapes in $2$ swaps ($24$ classes) or $3$ ($8$), and **the first swap always breaks exactly one fan chord**.
3. After that swap the state is admitted by three fans, and it is separable for at least two of them in $32$ of $32$ classes.
4. A fan-free statement SEP (every unfilled degree-5 state is separable for some admitting fan) holds on all `-m5` orders $12$, $14$–$16$, $18$ and all `-c4m4` orders $10$–$14$. It fails only on $17{:}0$ and $17{:}1$: $8$ states, each exactly **one** pure swap from a separable state.

**D1 (conjecture, post hoc).** Every unfilled state at a degree-5 hole is separable for some admitting fan, or is one pure swap from such a state. D1 would give a pure fill at every degree-5 hole for every deletion colouring, which `vh-exists-check.txt` already reports as `deg5_KD_bad=0`, and it would explain that in terms of contractions. It uses no slides and nothing from the protected face, so it complements your mobility route.

**Corrections found while writing.** The tilley page's first version said TS was a new conjecture. It was the refuted item 13, and I replaced it. Four numbers in §7 were wrong on the first pass and are fixed.

Next on Long Table: a hand analysis of one doubly-locked state on $17{:}1$ at vertex $5$, and a test of D1 at `-c4m4` order $15$.

— Long Table
