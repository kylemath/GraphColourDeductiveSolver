# WP21 declaration: D1 and P on a fresh order (26), and an adversarial search

Long Table, 5 October 2026. **A declaration. Nothing has run on the declared data.** The producer, driver, independent checker and regressions are committed before any phase. **No go-ahead is issued by anyone**: under the coordination session's ruling (`messages/2026-10-05/…` and `START-HERE.md` §5 step 2) and the user's direct word to Long Table, the gate is this complete hashed package, announced in `messages/`, run within its declared caps. The report will state that no go-ahead was given. Math reviews afterwards and the Navigator gates success; success needs an audit replay.

## Why

WP20 P1 tests D1 and P on order 25 exhaustively. It cannot reach rare graphs at larger orders, where exhaustive runs are too costly ($91{,}441$ graphs at order 26, $1{,}204{,}737$ at order 28, $16{,}248{,}772$ at order 30). Two pre-registered, capped probes extend the reach:

- **Phase A** samples order 26 by a frozen hash rule, a fresh order for these statements.
- **Phase B** searches adversarially for graphs where D1 or P fails, by flipping edges toward graphs with many SEP-bad or locked states.

## Statements (unchanged from WP20)

**D1** and **P**, with every definition (state, admitting fan, separable, SEP-bad, pure neighbour, good, depth, locked classes, kill certificates, `capped`, `inconclusive`) exactly as in `WP20-D1-declaration.md`, SHA-256 `8758a9f8409f17b4ca755d7688ba9f1bc996d35e40d0c173b5f9e64a3ca62fef`, and with the clarifications in `WP20-output-format.md`. The statements are fixed now and are not adjusted between phases. A kill is a D1 kill (a SEP-bad state, with at least one legal admitting fan, none of whose pure neighbours is good, equivalently a depth $\ge2$ state) or a P kill (a state whose complete pure Kempe class contains no filled state). **Every report lists each D1 kill with its P verdict and its `filled_neighbour_for_bad` count.**

## Phases

**Phase A (fresh order, sample).**
- **Full list:** `plantri -m5 -a 26` stdout, SHA-256 `88acad1180f8dafa35f7f0d03deb220f2266c746e6ea1fa70e76e10ec32276a8` (91,441 graphs; the same hash pre-registered in WP20).
- **Selection:** the graphs whose 0-based index $i$ in that output satisfies $\mathrm{int}(\mathrm{sha256}(\texttt{"WP21-A-"}+\mathrm{str}(i))_{\text{first 8 hex}},16)\bmod20=0$. This is 4,578 graphs. The selection file's SHA-256 is `24e381cbc4a0a65092fb2689f57bbb8163fad2d17573bf552a2ffcc42964ba31`. The rule is fixed before any graph is evaluated; the checker re-derives it from the full list.
- A pass says only that no counterexample occurs **among the sampled graphs**. Nothing is claimed about the other graphs of order 26.

**Phase B (adversarial search), run after A.**
- **Order:** 26. Flips preserve the order.
- **Seeds:** the 12 graphs of phase A with the greatest objective (below), ties broken by smaller index in the selection file. If fewer than 12 have positive objective, the remaining seeds are the lowest-index graphs of the selection.
- **Moves:** edge flips of `wp21_search.py` that keep a simple spherical triangulation with minimum degree 5.
- **Objective (to maximise), summed over the graph's degree-5 vertices:** $1000\times(\text{D1 kills}+\text{P kills}+\#\{\text{SEP-bad states of depth}\ge2\})+20\times\#\{\text{SEP-bad states}\}+\#\{\text{locked classes}\}$.
- **Search:** 12 independent chains, one per seed, each a simulated annealing run of **400 flips**: initial temperature $\max(10,\,0.5\times f_0)$, cooled linearly to 0, Metropolis acceptance. Chain $c$ uses a deterministic RNG seeded from $\mathrm{sha256}(\texttt{"WP21-chain-"}+c)$ (first 12 hex digits). Every evaluated graph (accepted or not), $12\times401=4{,}812$ in all, is recorded.
- **What B proves:** only that the search found, or did not find, a counterexample. It is not a holdout test and says nothing about graphs it did not visit.

## Resource limits and caps

- **Time:** at most 30 minutes per graph (checked inside enumeration and breadth-first search), and 12 hours of wall time per phase.
- **CPU:** phase A at most **12 CPU-hours**; phase B at most **24 CPU-hours** (each chain also has a 6,000-CPU-second cap, after which it stops). A phase that reaches its cap stops and is reported as capped. Capped is inconclusive, never a pass. Estimates, from WP20 timing at order 22 and the P1 run so far, are about 9 CPU-hours for A and about 14 for B.
- **Memory:** at most 8 GB per worker, enforced in the loop. **Output:** at most 1 GB per phase.
- **Interruptions:** interrupted graphs keep their completed vertices and are marked interrupted; inconclusive, never a pass.

## Producer, driver, checker

- **Producer:** `d1_confirm.py` (unchanged, SHA-256 `bb350d3b9579b984188a270a58d682562d170dc41c159ac4528a340fbd1fd0b5`). Phase A runs it on the selection file; phase B calls its `analyse_graph` unchanged.
- **Driver:** `wp21_search.py` (phase B only), and `wp21_sample.py` (phase A input).
- **Checker:** `d1_check21.py`, an adaptation of the WP20 independent checker, which imports no producer code. It adds: an independent check that every graph is a valid minimum-degree-5 spherical triangulation (simple, symmetric, $3n-6$ edges, every directed edge in one triangular face, $2n-4$ faces); a flag verifying that the phase-A input equals exactly the rule-selected lines of the full list; and flags for the expected input hash and sample rule. Check set: every graph with a SEP-bad state, a kill, or an unresolved vertex; the graphs whose index satisfies $\mathrm{int}(\mathrm{sha256}(\texttt{"WP21-"}+\mathrm{str}(i))_{\text{first 8 hex}},16)\bmod20=0$; and, for phase B, the 20 graphs of greatest objective. Where the cost is at most 6 CPU-hours the checker runs with `--all`.
- **Binding by hash:** every output records the SHA-256 of this declaration, of every producer and driver source file, and of its input. The checker refuses a different declaration hash.

## Regressions (committed and passing before phase A)

- The checker accepts the producer's output on orders 16, 17 and 18 with `--all`, rejects one corrupted count, one corrupted witness and one wrong input hash, and **rejects a graph that is not a valid triangulation** (a planted fault).
- The driver is **deterministic**: two runs with the same seeds and tag give byte-identical evaluated files.
- Every flip made in 440 random flips of the order-18 graphs leaves a valid minimum-degree-5 triangulation (face-traced).
- The selection rule is re-derived by the checker on the full order-26 list and gives the stated 4,578 lines.

## What is not claimed

D1 and P are universal. A pass on a sample or a search is not evidence for all graphs or all orders. A kill is a counterexample to D1 or P as worded in WP20. Neither statement is a claim about the vacancy hypothesis itself.
