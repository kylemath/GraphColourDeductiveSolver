# WP18 declaration: fan-selection length m(T)

Long Table, 5 October 2026. **Declaration for review. Nothing has run, and no producer code exists yet.** The producer and its regressions will be committed before any run. Nothing runs, at any order, until the math team sends an explicit go-ahead on this file.

## Why

`swarm/hole-induction.md` closes the induction if, at each minimum-degree-5 triangulation \(T\), one degree-5 vertex \(v\) and one legal fan \(\tau\) are chosen and every start they admit can be filled (VH∃, `SolvingFrameworkPlan/LongTableNextAttack.md` §1). Through order 20 every Kempe class at every degree-5 root contains a three-colour link. So VH∃ with unbounded moves **cannot fail** on orders 12–20, and this work package does not test it. It measures how short the fill becomes when \((v,\tau)\) is chosen, which is the only way a bounded candidate could become proof-shaped.

## Objects

- **Graphs:** spherical triangulations of minimum degree 5 from plantri 5.8 (`plantri -m5 -a n`), parsed and checked by `mass_core.parse_ascii`.
- **Legal fan:** at a degree-5 vertex \(v\) with link \(0..4\) in rotation order, \(\tau_i=\{i(i+2),\,i(i+3)\}\), legal when neither chord is an edge of \(T\).
- **Starts \(S(v,\tau)\):** proper 4-colourings of \(T-v\) whose two \(\tau\)-chords are bichromatic, up to renaming colours. These are exactly the restrictions of colourings of \(T^\ast_\tau\).
- **Moves**, on the pair (hole, colouring of \(T-\text{hole}\)), as in `swarm/icosahedron_fan.py`:
  - *Kempe swap:* exchange two colours on one bichromatic component of the current deletion; the hole stays put.
  - *Singleton slide:* if neighbour \(u\) carries a colour occurring once on the current link, write it on the hole; \(u\) becomes the hole.
- **Filled:** the current link uses at most three colours.
- **Length \(\ell(s)\):** fewest moves from start \(s\) to a filled state (breadth-first search).
- **Statistic:** \(L(v,\tau)=\max_{s\in S(v,\tau)}\ell(s)\), and \(m(T)=\min_{(v,\tau)}L(v,\tau)\).

## Cap

Breadth-first depth cap \(D=6\). A start not filled within 6 moves is recorded as \(\ell\ge 7\). That is **inconclusive**, not a pass and not a kill. A \((v,\tau)\) with any capped start has \(L(v,\tau)\ge 7\). \(m(T)\) is reported exactly only when some \((v,\tau)\) has every start below the cap.

## Phases

1. **P1, discovery:** orders 12, 14–18, every graph. There is no order 13.
2. **P2, secondary:** orders 19–20. These were the WP11 holdout. They are already spent for ranks and are labelled as a secondary check here, not a holdout.
3. **P3, holdout, above order 20:** order 21, all 192 graphs. Plantri output hash `5c203958…1c6d` (`plantri -m5 -a 21`). The night swarm swept order 21 only for q, lin and the WP11 survivors, never for fan lengths. Order 22 (651 graphs) is optional, once P3's cost is known.

Each phase is a single pass, with no tuning between phases.

## Resource limits

At most 30 minutes of wall-clock time per graph and 6 hours per phase, 8 GB of memory, and 200 MB of output per phase. A graph that hits a limit is recorded as interrupted with its partial counts. That is inconclusive, never a pass. An interrupted phase is reported as interrupted.

## Output

Per graph: the plantri index, the rotation hash, and \(L(v,\tau)\) for every degree-5 \(v\) and legal \(\tau\), together with the start count and the histogram of \(\ell\). Also \(m(T)\) and the maximum over \((v,\tau)\). One witness start (a colouring and a shortest move sequence) for every \((v,\tau)\) with \(L\ge 2\). An independent checker replays every witness sequence and confirms properness and the fill. The results and witness digests go in a `SHA256SUMS`.

## Regressions, committed before P1

- Icosahedron: 8 starts per fan, \(L=1\) at every \((v,\tau)\) (`swarm/icosahedron-fan.md`).
- Order 14, gyroelongated hexagonal dipyramid, \(v=U_0\), fan \(\{NL_0,NL_1\}\): the `fan-link.md` start has \(\ell=2\) (`order14_fan_check.py`, `order14-fan-check.txt`).
- A malformed witness (an improper colouring, or an illegal slide) must be rejected by the checker.

## Finds and kills

- **Find:** the smallest \(T\) with \(m(T)\ge 2\), and the smallest with \(m(T)\ge 3\). Order 14 already has \(L\ge 2\) at one \((v,\tau)\), but \(m\) there is unknown.
- **Candidate under test:** "\(m(T)\le 2\) for every \(T\)." It is **killed** by any graph with \(m(T)\ge 3\) found within the cap. It is not supported by any number of passes.
- **Not tested:** VH∃ itself, the vacancy hypothesis, or anything about the Four Colour Theorem.
