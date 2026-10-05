# Long Table: next line of attack

4 October 2026, late evening, for the 5 October retreat. Updated 5 October: the order-14 check has been run, the WP7 sentence fixed, and the messages sent. Written by Long Table after reading every message from the other two teams through revision 57, the Night Handoff at revision 70, `LibraryPlan.md`, `SwarmConsolidation.md`, and the swarm notes behind them. This is a plan only. Nothing below has been run, and no status words are claimed.

## What the other teams are waiting on from us

| Asked by | Request | State in the tree |
|---|---|---|
| Navigator, rev 57; Handoff item 5 | Completed validation directory, digests and commit | **Done but not reported.** `wp11-validation/` was committed in `f8ef782` and corrected in `bba6203`. Results `644dc472…0ddea`, certificates `dbeed9d4…0c2e0`. No message was sent, so revision 57 still says "in progress", and the handoff blocks every new census on this report. |
| Math, validation acknowledgement | Narrow the WP7 sentence to "The minimum-mass singleton pair is joined directly along the boundary cycle." | **Not done.** `WP7-results.md:30` still says "The singletons are joined directly along the boundary cycle." |
| Math, WP12 review | Revised WP12 declaration, adapter contract, three phases, resource caps | **Not started.** See §5. We propose to park WP12. |

Sending these is the first thing to do. It unblocks the census rule in item 5 and costs nothing.

## Outputs from the night swarm

The user confirmed that these outputs came from an overnight swarm of agents run on the user's instruction. The swarm's own report is `NightHandoff.md`. The agents were many and fast, but less careful than a declared work package. Their outputs are exploratory. Before any of them is cited, Long Table re-checks it, starting with the claims the plan leans on: the equal-pole star, the unequal tiles, the hole-induction deduction, and the 21-vertex counts. §1 and §3C already correct two of the handoff's claims.

Long Table's area holds outputs that no message has reported and that no declaration covers:

- `wp12-scale/sweep-{20..26}-all.json` and `sweep-23-26.log`: rank sweeps over plantri orders 20–26, including 25,381 graphs at order 25. They score q, lin and the WP11 survivors.
- `wp12-scale/verify-py-F32-r0.json` and `verify-py-F42-r0.json`: colouring counts on the WP12 fixtures. `IndependentInquiryReport.md` says "No full colouring search on either larger fixture ran". The two statements conflict, or the file counts something narrower. We have not checked which.
- `wp17-last-roots/holdout_eval.json` with `triangulations-min5-21.txt` and `-22.txt`: a holdout evaluation on orders 21–22.

Math's WP12 reply says no run above order 20 has been released. These runs were the night swarm's, made on the user's instruction rather than under a team release. **Proposal:** cite none of them as evidence. Tell both teams that they exist and where they came from, with paths and hashes. Treat orders 21–26 as already looked at for q, lin and the survivor ranks, but not for anything declared below. Find out what the F32/F42 files actually count before saying anything about them.

## 1. A correction to the handoff's proposed answer for item 1

The handoff proposes spending the morning on "the vacancy hypothesis restricted to fan colourings of \(T^\ast\)". Long Table's own `swarm/fan-link.md` shows that this restriction is weaker than it sounds:

- Every proper colouring of a 5-cycle is fan-proper. The three-colour orbit \((0,1,0,1,2)\) is proper on exactly one fan, the one at the vertex whose colour is unique. The four-colour orbit \((0,1,0,2,3)\) is proper on three fans.
- When the link is an induced 5-cycle, all five fans are legal. The union over the five fans of their restrictions is then **every** proper colouring of \(T-v\). The icosahedron note says the same thing: "the union over the five fans is all 20 orbits."
- The frozen-hole exclusion (8 > 5) holds for **every** degree-5 hole, fan or no fan.

So "fan colourings" restricts nothing as long as the hypothesis is stated for all fans. The real slack in `hole-induction.md` lies in its quantifiers. The degree-5 step chooses **one** vertex \(v\) and **one** legal fan \(\tau\). It needs a fill only for the colourings that \(\tau\) admits, and only at that \(v\). The hypothesis as written asks for every vertex \(h\) and every colouring.

**Proposed statement for the retreat (VH∃):**

> For every spherical triangulation \(T\) of minimum degree 5, there is a degree-5 vertex \(v\) and a legal fan \(\tau\) at \(v\) such that every proper 4-colouring of \(T-v\) that is proper on \(\tau\) reaches a link of at most three colours by a finite sequence of singleton slides and Kempe swaps in deletions of \(T\).

VH∃ is all that `hole-induction.md` uses, and it is implied by the handoff's hypothesis. It reintroduces a selection, but a weak one: a pair \((v,\tau)\) only has to work, and bad roots such as 17:0 roots 4 and 6 may simply be avoided.

Feasibility that VH∃ suffices for the induction: **High**, by reading the degree-5 step. Feasibility of VH∃ itself: open, as before.

### A small lemma to write first

**Containment.** \(T^\ast_\tau\) contains \(T-v\) plus two chords. Removing edges only splits bichromatic components. So every Kempe swap in \(T^\ast_\tau\) is a composition of Kempe swaps in \(T-v\) on the same colour pair. It follows that the set reachable from a start contains the start's whole \(T^\ast_\tau\)-Kempe class. VH∃ at \((v,\tau)\) is therefore a statement about **Kempe classes of \(T^\ast_\tau\)**, not about single colourings. This is a hand lemma of a few lines. It belongs in `hole-induction.md`, and the math team should review it.

## 2. Handoff item 3 is already answered, by hand

The handoff asks for the smallest triangulation whose fan colourings need more than one Kempe swap. There is no minimum-degree-5 triangulation of order 13, and the icosahedron (order 12) has worst length 1. So the first candidate is order 14, and `fan-link.md` already has one: the **gyroelongated hexagonal dipyramid** with \(U_0\) deleted. Its link \((U_1,N,U_5,L_0,L_1)\) is coloured \((0,1,0,2,3)\), the colouring is proper on the fan \(\tau_1=\{NL_0, NL_1\}\), and no single Kempe swap reduces the link.

Long Table checked the three slides by hand tonight. All three keep four colours:

| Slide | New hole | Link colours after the slide | Colours |
|---|---|---|---|
| \(U_0\to N\) | \(N\) | \(U_0..U_5 = 1,0,3,0,2,0\) | 4 |
| \(U_0\to L_0\) | \(L_0\) | \(U_0,U_5,L_5,S,L_1 = 2,0,1,0,3\) | 4 |
| \(U_0\to L_1\) | \(L_1\) | \(U_0,U_1,L_0,L_2,S = 3,0,2,1,0\) | 4 |

So this fan start needs **at least two mixed moves**. The machine check is `longtable/order14_fan_check.py` → `order14-fan-check.txt`. The colouring is proper, 0 of 11 single Kempe swaps fill, all three slides keep four colours, and 36 two-move sequences fill. The mixed distance is exactly 2. So order 14 is the smallest order at which a fan start needs more than one move of either kind. The icosahedron count is then exactly what the handoff proposes to call it: a computation on one graph and nothing more.

This does not settle VH∃ at order 14. A different \(v\) or \(\tau\) might do better: this colouring is improper on \(\tau_0\) and \(\tau_2\).

## 3. Lines of attack, in order

### A. The belt theorem: every hole of \(G_{3k+2}\) (Long Table hand work; math review)

This is the most finishable result in hand. It would be the first infinite family on which the vacancy hypothesis holds even though Kempe classes split. Florek shows \(G_n\) has at least \(\lfloor n/6\rfloor\) Kempe classes.

1. **Pole holes.** Florek's Theorem 3.1 says all colourings of \(G_n\) minus a pole are Kempe equivalent. Florek also enumerates full colourings of \(G_n\), and their restrictions have a three-colour pole link. So every pole-hole start reaches a fill by swaps alone. This is citation plus a paragraph; it does not appeal to the Four Colour Theorem.
2. **Belt holes, equal poles.** The star swap, `TwoPoleStarEscape.md`, is written for every \(n=3k+2\).
3. **Belt holes, unequal poles.** \(A_\tau\), the \(B\) orientation and the cap are written. **The \(A_\rho\) tile with outer \(u\)-vertex \(\tau\)** remains. Write it by hand, to the standard of `unequal-b-tile.md`. Do not enumerate \(n=14\).
4. Write one page that joins 1–3 into a statement for every hole of \(G_{3k+2}\), with the case split made explicit. Then ask the math team to review it before any Lean work.

**Kill:** a colouring of that tile, with the outer \(u\)-vertex coloured \(\tau\), from which no slide sequence returns a prepared zero within the tile. Then this case needs a swap, and the belt statement goes back to Medium.

Feasibility of the tile: **Medium-High**, as the handoff says. Feasibility of the joined page once the tile exists: **High**.

### B. Measure VH∃ on graphs already in the census (Long Table adversary tooling)

Through order 20, every Kempe class at every degree-5 root contains a three-colour boundary. So VH∃, with no bound on moves, **cannot fail** on orders 12–20, and no computation there can kill it. Say so in every message. What computation can show is structure: whether choosing \((v,\tau)\) collapses the length.

- **Statistic:** \(m(T)=\min_{(v,\tau)}\max_{\text{starts}}\) (fewest mixed moves to a link of at most three colours). Compute it with the start-length per \((v,\tau)\) beside it.
- **Domain:** discovery orders 12–18 first. Orders 19–20 were the WP11 holdout. They may be read only as a labelled secondary check, because they are not fresh for a new statistic. The math team is expected to allow orders above 20. Order 21 (and 22 if it is affordable) is then the fresh holdout for \(m(T)\). The night swarm swept 21–26 only for q, lin and the WP11 survivors, never for fan-move lengths. Above order 20, nothing runs until math's message gives an explicit go-ahead on this declaration.
- **Order of work:** declare and commit the statistic, the move model (shared with `icosahedron_fan.py`) and the search cap. Send it to math for review. Run only after an explicit go-ahead, and only after the validation report has gone out.
- **Find (not kill):** the smallest \(T\) with \(m(T)\ge 2\), and the smallest with \(m(T)\ge 3\). Order 14 is the first place to look, by §2.
- **What would matter:** if \(m(T)\le 2\) on all of 12–18 while \(\max_{(v,\tau)}\) grows, then "at a well-chosen \((v,\tau)\), two mixed moves" becomes a bounded, proof-shaped candidate. It is different from the budgets already killed, which were budgets at every start or at frozen later holes. If \(m(T)\) grows with order, that candidate dies and we report it.

### C. Hand lemmas (Long Table writes; math decides what to compile)

1. **Containment** (§1).
2. **Apex singleton.** In every fan-proper link, read from the apex of a proper fan, the apex colour is unique on the link. So the slide \(v\to\) apex is always legal. This is trivial, but it is the only move guaranteed at every start.
3. **Correction to the handoff.** The handoff says "a classification of which 5-cycle words are proper on a fan was not written." It was: `swarm/fan-link.md` gives two orbits and the proper fans of each. The handoff should point to it, not open it as new work.

### D. Park WP12 (tell math)

WP12 tests a fixed-root rank, q, on isolated-pentagon fixtures. That serves the contact-theorem route, which the handoff no longer proposes as tomorrow's proof. `LibraryPlan.md` and `isolated-local.md` already say not to colour F32 or F42 for the bridge. Proposal: withdraw the request for experimental release. Keep the graph-only fixtures and transport permutations for later, and say so to math so their review effort is not wasted.

## 4. Long Table's positions on the five retreat items

1. **Which proof.** Vacancy induction, with the hypothesis stated as VH∃ (§1), not as "fan colourings". The contact gate stays as it is.
2. **Last tile.** Agree. Long Table offers to write it by hand. No \(n=14\) and no Lean until it is closed.
3. **Icosahedron.** Record it as a computation. The smallest-graph question has a hand answer at order 14 (§2), pending a machine check. The next question is \(m(T)\), not a new graph.
4. **The sentence.** Agree, word for word: "This colouring does not need a fourth swap, and a different graph still might."
5. **What stays stopped.** Validation **finished**. Report it now (table above), together with the disclosure of the night swarm's outputs.

## 5. What not to do

- Do not run \(m(T)\), at any order, before math has replied with an explicit go-ahead on its declaration.
- Do not cite the order 21–26 sweeps or the F32/F42 counts.
- Do not score another fitted rank: `rank-kill.md`, and the 9↔14 equivariance kill.
- Do not colour F32 or F42.
- Do not call VH∃ "supported" because orders 12–20 pass. Those orders cannot fail it.

## Outgoing messages (sent 5 October)

1. `2026-10-05-longtable-to-math-and-navigator-validation-complete.md`: directory, both digests, commits `f8ef782` and `bba6203`, and the WP7 sentence fixed in the same commit.
2. `2026-10-05-longtable-to-math-and-navigator-retreat-positions.md`: §1 to §4, the WP12 parking, and the disclosure of the night swarm's outputs.
