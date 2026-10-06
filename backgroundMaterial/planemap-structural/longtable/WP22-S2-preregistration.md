# WP22 (S2) pre-registration: Kempe radii of doubly locked states, a search for a targetless state

Long Table, 6 October 2026. **A pre-registration. S2 has never been run. Its code does not exist yet** (the prototype `explore-vhphi/lattack_search.py` implements the earlier search S1 only). This document fixes the hypotheses, the kill criteria, the parameters and the caps **before** any S2 data exists. The S2 search code and its independent verifier will be written, committed and hashed in an **addendum message before any run**; nothing runs until that addendum exists and WP20 P1 has reported. Any deviation from this document will be reported as a deviation. No go-ahead is issued by anyone; the gate is the hashed package, as for WP21.

## Why S2, and what was already seen

Conjecture L (an absolute bound on chains of doubly locked F-iterates) is false as stated: a chain of length 6 (witness W6, 20 vertices) and an all-locked periodic F-orbit on the 17-vertex triangulation $A_3$ (`l-attack.md`, verified independently by the lead). The L-Attack team proposed a repaired conjecture, which S2 tests. **S2 was formulated after seeing these data** (Kempe radii: $r=2$ for W6, $r\in\{2,3\}$ on $A_3$, $r=2$ on the colourings tested of $A_4,A_5$). So any bound $R$ read from those values is post hoc.

## Definitions

- **State:** a plane triangulation $T$, a vertex $v$ of degree 5, and a proper 4-colouring $s$ of $T-v$ whose link has four colours. **Doubly locked** and the rotation $F$ are as in `MathConfinementAttack.md` Step 1 and `MathCleanVertexAttack.md` Theorem C (the definitions the lead verifier uses).
- **Kempe class of $s$ (hole fixed at $v$):** all colourings reachable from $s$ by whole-component two-colour swaps of $T-v$, taken up to renaming of colours.
- **Filled:** the link uses at most three colours.
- **Radius $r(s)$:** the least number of such swaps from $s$ to a filled state; $r(s)=\infty$ if the Kempe class contains no filled state.

## Statement

**Conjecture R.** There is an absolute $R$ such that $r(s)\le R$ for every doubly locked state at a degree-5 hole of every plane triangulation. $r(s)=\infty$ for a doubly locked state is exactly a **targetless component at $v$** in the setting without a protected face; so R implies that every degree-5 vertex is clean in that setting, and is as strong as the clean-vertex statement. It is post hoc.

## Searches and what counts as a kill

**S2a (hill-climb).** State space, moves and acceptance as in the prototype `lattack_search.py` (minimum degree at least 4, order 12 to 30; moves: Kempe swap, edge flip, stack, delete a degree-3 vertex; seeds as below). **Objective to maximise:** $r(s_0)$ computed by breadth-first search over Kempe swaps of $T-v$ to depth at most 6 and at most 20,000 canonical states, tie-broken by the number of unfilled states in the ball; the start state must be doubly locked.

**S2b (symmetric families).** Triangulations of degree 5 and 6 only, including the stacked-antiprism family $A_r$ ($r=3,4,5$: 17, 22 and 27 vertices; the generator is `lattack_sym.py`, hash cited in the addendum), with **exhaustive** enumeration of every doubly locked state up to colour renaming (not sampling), computing $r$ for all of them. The move-based search of S2a is too coarse for these families, so S2b is a census of the stated graphs and nothing else.

**KILL-2.** A doubly locked state at a degree-5 hole whose Kempe class is **exhaustively enumerated and closed** (the search reaches no new state) **with no filled state in it**, i.e. $r=\infty$ by complete enumeration. A class larger than the state cap is `capped`, which is inconclusive and never a kill or a pass. A KILL-2 certificate (the graph as oriented triangles, $v$, the colouring) is re-verified by a separate verifier, written from the definitions by a team that has not read the search code, which enumerates the class by its own code; and it is then rechecked against the project's protected-face definitions before anything is called a targetless component of the core.

**RESULT (not a kill).** The maximum $r$ reached per tag (S2a), the maximum $r$ over the census (S2b), and the distribution of per-restart best values. A finite maximum is not evidence for R, and a large finite value is not a kill.

## Seeds, caps, resources

- **Seeds:** `random.Random("wp22|s2a|<tag>")` for tags `t001` to `t040`; S2b has no randomness. Deterministic given the tag.
- **Caps:** one process per tag; 120 CPU-seconds per tag (`time.process_time`); at most 2 workers on the first Mac and at most 14 on the Studio, with the same per-tag cap; 40 tags is about 80 CPU-minutes. Orders at most 30. Breadth-first search at most 20,000 states and depth 6 per evaluation. A tag that reaches its cap stops and is reported as capped; capped is inconclusive.
- **No plantri;** no use of orders 25 or 26 data; no graph from WP20 P1 or WP21 is used as a seed.

## Gates (all before any run)

1. WP20 P1 has reported (the checker `--all` passed, report posted).
2. The S2 search code, the S2b census code and the independent verifier are committed, tested (determinism across reruns; planted faults: a corrupted class, a corrupted witness; the search reproduces $r=2$ on W6 and $r\in\{2,3\}$ on $A_3$), and their SHA-256 hashes are announced in an **addendum message** that also states the machine.
3. This document's SHA-256 is cited in that addendum. Changing it after that point is a new pre-registration.

## What is not claimed

Nothing about VH∃, about the core, or about states with a protected face. W6 has degree-3 vertices, and $A_r$ has no protected face. A pass (no KILL-2) is a statement about the graphs visited.
