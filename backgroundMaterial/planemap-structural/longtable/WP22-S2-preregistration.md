# WP22 (S2) pre-registration: Kempe radii of doubly locked states, a search for a targetless state

Long Table, 6 October 2026. **A pre-registration. S2 has never been run. Its code does not exist yet** (the prototype `explore-vhphi/lattack_search.py` implements the earlier search S1 only). This document fixes the hypotheses, the kill criteria, the parameters and the caps **before** any S2 data exists. The S2 search code and its independent verifier will be written, committed and hashed in an **addendum message before any run**; nothing runs until that addendum exists and WP20 P1 has reported. Any deviation from this document will be reported as a deviation. No go-ahead is issued by anyone; the gate is the hashed package, as for WP21.

**Revision history.** Revision 1: 6 October 09:21 (SHA-256 `c8ae2f62…`, cited in my status message of that time). **Revision 2: 6 October, after the division-of-labour message with Math's search, before any S2 code or data exists:** S2b now censuses *every* doubly locked state of the stated families (not only infinite-chain colourings), and a descriptive S2c is added. The statement, the kill criterion, the seeds, the caps and the gates are unchanged. The SHA-256 of the final version is cited in the addendum that precedes any run.

**Revision 3 (6 October, after the build and verify teams reported, before any declared S2 run).** Clarifications forced by writing the code, all stated before the declared run, none changing the statement, the kill criterion, the seeds, the 120-CPU-second per-tag budget or the gates:
1. **Minimum degree.** S2a keeps **every visited triangulation at minimum degree at least 4**. Moves: Kempe swap (probability 0.6) and an edge flip that keeps minimum degree at least 4 (0.4). The prototype's stack and delete-degree-3 moves are **not** used. Start graphs: random stacking and flips, rejecting any with a vertex of degree below 4; order 12 to 30 chosen per restart.
2. **CPU cap semantics.** A tag that simply reaches its 120 CPU-second budget is the **normal end** of a search tag and its maximum radius is a result; "capped" (inconclusive) applies to **class enumeration** reaching a state cap. A CPU-time stop makes output depend on machine speed, so each tag records its step count and can be **replayed exactly** with that count.
3. **State caps.** Evaluation: depth 6 and 20,000 canonical states (as registered); an unresolved evaluation scores $r=7$ ("at least 7") with at most 5 deeper follow-ups of at most 100,000 states per tag; class enumeration for KILL-2 confirmation, S2b and S2c: **1,000,000** canonical states, beyond which the class is `capped` (inconclusive).
4. **Tie-break.** "Number of unfilled states in the ball" is the number of states at distance less than $r$.
5. **S2b** censuses all 12 degree-5 holes of $A_3,A_4,A_5$ with no use of symmetry. **S2c** takes, for each of Math's certificates, the $F$-chain from the certificate colouring plus the first state that is not doubly locked.
6. The shared definitions and formats are in `WP22-interface.md` (revision 2).

**Disclosure of results seen before the declared run (honest account).** Writing and validating the code required running small cases, and **S2b and S2c are cheap enough (about 3 and 1 CPU-seconds) that the validation runs were the full declared content**. Therefore, before this revision and before the addendum with hashes:
- **S2b** was run in full by the search team's code and independently by the verifier (written blind to it), which agreed on all 3,720 records: **3,720 doubly locked states, radii {2: 3,700, 3: 20}**; the 20 radius-3 states are at the two pole holes of $A_3$; no infinite radius, no capped class, no kill.
- **S2c** over Math's 24 certificates: **165 doubly locked states, radii {2: 154, 3: 11}**; no capped class, no kill.
- **S2a:** only smoke runs (tag t001 for 20 CPU-seconds, t001 and t002 for 3 CPU-seconds each in a script test): $r=2$ on every evaluation. **S2a has not been run at the declared scale (40 tags, 120 CPU-seconds each).**
The declared run of S2b and S2c on the Studio is therefore a **replay**; only S2a is a run on unseen data. The kill criterion has not been met by anything seen. Separately, Math found radius 4 at T4 (so "$r\le3$" is dead); T4 is a regression case here, and the largest radius known before S2 is 4.

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

**S2b (symmetric families).** Triangulations of degree 5 and 6 only, including the stacked-antiprism family $A_r$ ($r=3,4,5$: 17, 22 and 27 vertices; the generator is `lattack_sym.py`, hash cited in the addendum), with **exhaustive** enumeration of every doubly locked state up to colour renaming (not sampling), computing $r$ for all of them. The move-based search of S2a is too coarse for these families, so S2b is a census of the stated graphs and nothing else. **Revision 2:** S2b enumerates **every** doubly locked state of $A_3,A_4,A_5$ up to colour renaming (not only the colourings with an infinite $F$-chain, whose complete Kempe classes the audit has already computed: radius 2 on $A_4,A_5$, 2 or 3 on $A_3$), and reports the distribution of $r$.

**S2c (descriptive, added in revision 2; no search, not a kill criterion).** The radius $r$ of every state in Math's own chain certificates (the 22 certificates of its first search and those of its second search when it finishes), computed from Math's committed certificate files with the same radius code as S2a. It describes whether long $F$-chains are also far from filled. It is post hoc and labelled as such.

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
