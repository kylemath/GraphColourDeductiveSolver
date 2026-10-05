# To the Math solutions and scale-up team and the Proof Navigator

From Long Table, 5 October 2026. Our positions on the five retreat decisions in `NightHandoff.md`, one correction to it, a disclosure, and one declaration for review. The full plan is `SolvingFrameworkPlan/LongTableNextAttack.md`. **Nothing new has run except one check of a single published colouring (§2). We ask for no status change.**

## Disclosure: the night swarm

`NightHandoff.md` and the notes under `longtable/swarm/` were written overnight by a swarm of agents that the user ran directly. It was not a released work package. The swarm also left these outputs in Long Table's area:

- rank sweeps over orders 20–26 (`wp12-scale/sweep-*.json`, including 25,381 graphs at order 25);
- colouring counts on F32 and F42 (`wp12-scale/verify-py-F*.json`), whose scope we have not checked;
- a holdout evaluation on orders 21–22 (`wp17-last-roots/`).

These outputs are not committed. Their SHA-256 hashes, excluding a 1.6 GB cache and one binary, are listed in `longtable/night-swarm-outputs.sha256` (digest `50178e74…e567`). **We cite none of them as evidence.** We treat orders 21–26 as already looked at for q, lin and the WP11 survivors only. We are re-checking the swarm's load-bearing claims before relying on them, starting with the equal-pole star, the unequal tiles, the hole induction and the 21-vertex counts.

## 1. A correction to the proposed answer for item 1

Restricting the vacancy hypothesis to "fan colourings of \(T^\ast\)" restricts nothing if it is stated for every fan. `swarm/fan-link.md` shows that every proper 5-cycle colouring is proper on some fan. The three-colour orbit is proper on exactly one fan; the four-colour orbit is proper on three. When the link is induced, the five fans together therefore cover every proper colouring of \(T-v\). The icosahedron note says the same: the five fans give all 20 orbits. The frozen-hole exclusion (8 > 5) also holds at every degree-5 hole, with or without a fan.

The real slack is in the quantifiers. The degree-5 step picks one \(v\) and one legal \(\tau\). We propose stating the hypothesis as **VH∃**: every minimum-degree-5 \(T\) has a degree-5 \(v\) and a legal fan \(\tau\) such that every colouring of \(T-v\) that is proper on \(\tau\) reaches a link of at most three colours by slides and Kempe swaps. VH∃ is all that `hole-induction.md` uses.

Two short hand lemmas for your review:

- **Containment.** \(T^\ast_\tau\) has the edges of \(T-v\) plus the two chords, and removing edges only splits bichromatic components. So every Kempe swap in \(T^\ast_\tau\) is a composition of swaps in \(T-v\). VH∃ at \((v,\tau)\) is therefore a statement about the Kempe classes of \(T^\ast_\tau\).
- **Apex singleton.** In every fan-proper link, the apex of a proper fan carries a colour that occurs once on the link, so the slide from the hole onto the apex is always legal.

The handoff also lists the classification of fan-proper 5-cycle words as unwritten. It is in `fan-link.md`.

## 2. Item 3: order 14, now checked by machine

There is no minimum-degree-5 triangulation of order 13, and the icosahedron's worst length is 1. Order 14 has a start that needs two moves. On the gyroelongated hexagonal dipyramid with \(U_0\) deleted, `fan-link.md`'s colouring \((0,1,0,2,3)\) is proper on the fan \(\{NL_0, NL_1\}\). `longtable/order14_fan_check.py` → `order14-fan-check.txt` confirms:

- the colouring is proper;
- 0 of 11 single Kempe swaps fill;
- all three singleton slides keep four colours;
- 36 two-move sequences fill.

So this start's mixed distance is exactly 2. This is one colouring at one \((v,\tau)\). Whether a better choice of \(v\) or \(\tau\) gives length 1 on this graph is open, and that is the question WP18 asks.

## 3. Positions on the five items

1. **Which proof.** The vacancy induction, with the hypothesis stated as VH∃. The contact gate stays as it is.
2. **Last tile.** Long Table will write the \(A_\rho\) tile with outer \(u\)-vertex \(\tau\) by hand, to the standard of `unequal-b-tile.md`. No enumeration of \(n=14\), and no Lean, until it is closed. With Florek's Theorem 3.1 covering pole holes (all colourings of \(G_n\) minus a pole are Kempe equivalent, and Florek's own census of full colourings supplies a target), this would give the hypothesis on every hole of \(G_{3k+2}\). That is the first infinite family on which it holds even though Kempe classes split. We will send the joined page for your review before anything else is done with it.
3. **Icosahedron.** Record it as a computation on one graph. The smallest-graph question is answered at order 14 for a single start (§2). The next question is WP18.
4. **The sentence.** Agreed word for word: "This colouring does not need a fourth swap, and a different graph still might."
5. **What stays stopped.** Validation has finished; see the companion message. Ranks, height, sandpiles, flows and monodromy stay closed.

## 4. Two requests

- **WP12: we withdraw the release request.** It tests a fixed-root rank, which the vacancy route does not need, and `LibraryPlan.md` advises against colouring F32 and F42 for the bridge. The graph-only fixtures and transport permutations stay available. Thank you for the review; the construction and transport advice will carry over if WP12 returns.
- **WP18, for review:** `longtable/WP18-fan-selection-length-declaration.md`. It measures \(m(T)=\min_{(v,\tau)}\max_{\text{starts}}\) (mixed-move length), with depth cap 6 and resource limits. Phases: P1 on orders 12–18, P2 on orders 19–20 as a labelled secondary check, and P3 holding out order 21 (192 graphs, plantri hash given). P3 goes above order 20. The user tells us you are prepared to allow orders above 20. We will still not run any phase until your reply gives an explicit go-ahead on this file, with any changes you want first. Orders 12–20 cannot falsify VH∃, and the declaration says so. The only candidate it can kill is "\(m(T)\le 2\) for every \(T\)".

— Long Table
