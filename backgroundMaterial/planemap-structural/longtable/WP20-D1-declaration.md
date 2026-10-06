# WP20 declaration: pre-registered separability conjectures at degree-5 holes, order 25

Long Table, 5 October 2026. **A declaration. Nothing has run on the declared data.** The producer, the independent checker and the regressions are committed before any phase. The user released the run in chat on 5 October 2026 ("do both 1 and 2 and then also run 2"). **Math's written go-ahead naming this file and its commit has not been received**; Math has posted nothing since 17:29. The chronology is recorded in the results report.

## Why

D1 and SEP were formulated after the data on min-degree-5 triangulations of orders 12–18 and 4-connected triangulations of orders 10–16 (`SolvingFrameworkPlan/docs/working/creative-intel-2026-10-05/tilley-separability.md` §7, §10). Data a statement was fitted on cannot test it. This declaration tests the statements below, worded exactly as here, on order 25, which none of them has seen. The statements are fixed now and will not be adjusted.

Orders 19–24 are spent for confirmatory use (`START-HERE.md` §5). They are **not** used here.

## Objects

- **Graphs:** plantri 5.8 (source tarball SHA-256 `e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8`) with `-m5 -a n`. Graph indices are 0-based in plantri output order. Rotations are the ASCII rotation systems.
- **Fans at a degree-5 vertex $x$:** the ring $r_0,\dots,r_4$ is the rotation at $x$. Fan $j$ has apex $r_j$ and chords $r_jr_{j+2}$, $r_jr_{j+3}$ (indices mod 5). It is **legal** when neither chord is an edge of $T$.
- **State at $x$:** a proper 4-colouring $c$ of $T-x$, up to renaming of colours, whose ring uses exactly four colours (an **unfilled** state). A **filled** state has a ring using at most three.
- **Admitting fans:** a legal fan $j$ **admits** $c$ when $c(r_j)$ occurs exactly once on the ring. An unfilled state has exactly three singleton ring positions; the admitting fans are the legal ones among them.
- **Separable for fan $j$:** let $G=T-xr_j$ (delete the edge). Colour $x$ with $c(r_j)$, so that the colouring is a proper colouring of $G$. $c$ is **separable for fan $j$** when some colouring reachable from it by Kempe swaps in $G$ has $c(x)\neq c(r_j)$. A Kempe swap in $G$ exchanges the two colours on one whole component of the two-colour subgraph of $G$, $x$ included.
- **SEP-bad state:** an unfilled state with at least one admitting legal fan, that is not separable for any admitting legal fan. A state with no legal admitting fan is recorded as `no_legal_fan` and excluded from every statement.
- **Pure neighbours of a state:** the states obtained by one Kempe swap of $T-x$ (the hole stays at $x$, $x$ is absent): choose two colours and one whole component of their bichromatic subgraph of $T-x$, and exchange. Neighbours are taken up to renaming. A neighbour is **good** when it is unfilled and separable for some admitting legal fan. A filled neighbour is **not** good for D1; it is recorded separately (`filled_neighbour`).
- **Pure fill:** a sequence of Kempe swaps of $T-x$ ending in a filled state.

## Pre-registered statements and what kills each

| Id | Statement | Killed by (certificate) |
|---|---|---|
| **D1** | At every degree-5 vertex of every minimum-degree-5 triangulation, every unfilled state is separable for some admitting legal fan, **or** has a pure neighbour that is good (as defined above; in particular unfilled and separable). | An unfilled state with at least one legal admitting fan that is SEP-bad **and** none of whose pure neighbours is good. The certificate lists the graph, $x$, the colouring, the admitting fans, and for every neighbour its verdict. |
| **P** | At every degree-5 vertex, every unfilled state has a pure fill. | An unfilled state whose complete hole-fixed Kempe class (all states reachable by pure swaps) contains no filled state. A class is enumerated completely; if enumeration exceeds 200,000 states the verdict is `capped`, which is inconclusive and never a pass or a kill. |

**Recorded, not tested as statements:**
- **SEP count:** the number of SEP-bad states per graph and per vertex, with every SEP-bad state's witness. SEP itself ("no SEP-bad state") is already false at 17:0 and 17:1 and is **not** a pre-registered statement.
- **Depth of SEP-bad states:** the least number of pure swaps from a SEP-bad state to a **good** state (unfilled, with a legal admitting fan, separable for some admitting legal fan; a filled state is traversed but is never the target), computed by breadth-first search over all states to depth 3 (`depth: 1`, `2`, `3`, or `>3`). A depth $\ge2$ is a D1 kill by definition.
- **Locks:** the number of locked apex classes (Tilley), and for each its colour-class sizes in $T-x$. Recorded only.
- A state whose search exceeded any limit is `inconclusive`, never a pass.

**What a pass means.** Every statement is universal, so a pass says only that no counterexample occurs among the graphs run. Reports state kills, certificates and counts only.

## Phases

1. **P1, holdout: order 25, every graph.** The plantri stdout must hash to `92e482edefb9ff4c5fbb77b2121366b2c3a88cf8001fecafa1ae29025e60d989` ($25{,}381$ graphs). No sampling and no exclusion.
2. **P2, optional: order 26, every graph.** Plantri stdout hash `88acad1180f8dafa35f7f0d03deb220f2266c746e6ea1fa70e76e10ec32276a8` ($91{,}441$ graphs). **Run only if P1's total CPU time was at most 6 CPU-hours.** The rule is fixed now; a higher cost means P2 does not run.

Each phase is one pass, with no tuning between phases. A kill in P1 does not stop P2, and a killed statement is still reported in P2, labelled as already killed. P1 is not rerun after any change to the producer; a producer fault is fixed and the phase is rerun from scratch, with both runs reported.

## Resource limits

- **Time:** at most 30 minutes per graph and 12 hours of wall time per phase. Deadlines are checked inside colouring enumeration and breadth-first search.
- **Interruptions:** an interrupted graph keeps every completed vertex and is marked `interrupted`. That is inconclusive, never a pass.
- **Memory:** at most 8 GB per worker, enforced by the same in-loop hook that checks deadlines (`resource.getrusage`). Past the limit the graph is recorded as interrupted with reason `memory`.
- **Output:** at most 1 GB per phase. Past the limit, witnesses are dropped and the phase is marked `truncated`; counts continue.
- **Accounting:** every degree-5 vertex of every graph appears in the output with its state count, SEP-bad count, depth histogram, `no_legal_fan` count, P verdict counts and status (`complete`, `interrupted`, `capped`). A statement is never counted as passed on a graph with an unresolved vertex.
- **Binding by hash:** the output records the SHA-256 of this declaration, of every producer source file, and of the plantri stdout. The checker refuses an output whose declaration hash differs from the committed version of this file.

## Independent checker

`longtable/d1_check.py` imports no producer code. It was written from this declaration only, by a team that did not read the producer. It must:
- verify the hashes above;
- recompute, with its own colouring enumerator, Kempe code and plantri parser, every statistic for **every graph that has a SEP-bad state, a D1 or P kill, or an unresolved vertex**, and for a fixed sample of graphs: the graphs whose index $i$ satisfies $\mathrm{int}(\mathrm{sha256}(\texttt{"WP20-"}+\mathrm{str}(i))_{\text{first 8 hex}},16)\bmod 50=0$ (about 2%);
- re-verify every kill certificate and every SEP-bad witness from scratch;
- compare counts exactly with the producer's output, and report any mismatch as a fault that stops the phase.

## Regressions (committed and passing before P1)

On orders already seen, which are not fresh data: the producer reproduces order 16 ($0$ SEP-bad), order 17 ($8$ SEP-bad states: $4$ at 17:0 and $4$ at 17:1, all depth $1$, $32$ locked classes), order 18 ($0$ SEP-bad). The checker agrees with the producer on all of these graphs. The checker rejects an output with one deliberately corrupted count and one corrupted witness.

## What is not claimed

D1 and P are universal statements. A pass at order 25 (and 26) is not evidence for all orders. A kill is a counterexample to D1 or P as worded here. Neither statement is a claim about the vacancy hypothesis; P is the strong pure form at degree-5 holes, which `swarm/vh-exists-check.txt` already records at orders $\le20$.
