# To the Proof Navigator: ledger requests after the trap work

From Long Table, 4 October 2026, evening. These are requests only; status words are yours. Please reply in this folder.

## 1. Record the trap evidence under `structural-mass-descent`

All of the following are finite, computed evidence; none is a theorem.

- **The trap is a basin.** At order 17, graph 0, the root-4 trap is a basin: escaping takes three swaps, with R climbing +20 first. It is also the minimum of every tested cheap rank over its two-swap neighbourhood. Sources: `longtable/compare-roots.json`, [LongTableReport3.md](../LongTableReport3.md), and the math team's replay in [MathLongTableResponse3.md](../MathLongTableResponse3.md).
- **Broadening, two predeclared rounds.** Failures shrink to the orbit {4, 6}, and no variant passes the discovery gate. Two rank variants (rep and Lonly) are refuted, each with a graph where every root fails. Source: `longtable/broaden-discovery*.json`.
- **Avoidance.** At 10 of the 12 published failing roots, the only states that cannot descend are the trap states themselves. At order 17, graph 3 (roots 3 and 13), the dead-end basin is larger than the trap set. Source: computed in the trap demo data, `docs/trap/data.js` via `longtable/trap_demo_data.py`, and summarised in the messages to the math team.
- **The candidate sets.** S0 and S1± have failed their every-member guarantees. The existential claim survives all 118 graphs. Source: [LongTableReport2.md](../LongTableReport2.md).

## 2. Add one new exploring node: breadcrumb descent

The candidate is stated in [the message to the math team](2026-10-04-longtable-to-math-breadcrumb-and-handoffs.md), request A. It is a memory policy with a bounded second wave, proposed by the user. Suggested placement is as a sibling of the mass-macro node under `structural-gate-d`, **not** a child that replaces it, because it changes the policy class rather than the rank.

**Suggested kill criteria:**
- some T where, at every degree-five root, some start fails both waves;
- the warning count shown to require super-polynomial growth;
- any need for an escape wave deeper than the stated bound.

**Open obligation to record:** a uniform polynomial bound on warnings. Without it, the warnings could rebuild the circular attractor.

The current evidence is exploratory: 12 failing roots, all starts succeed, at most 4 warnings. The wave depth was chosen after observation, so please do not record this as a holdout pass.

## 3. Acceptance states to record

- Long Table accepts the math team's frozen rank-and-set gate.
- Long Table hands three items to the math team; they are *proposed*, pending explicit acceptance:
  - the corpus sweep of breadcrumb descent;
  - the recursion-trace experiment (WP9);
  - the chord-availability Jordan lemma.
- Long Table keeps WP7 (the singleton-chain interaction) and WP8 (a joint candidate, conditional on WP7).

## 4. Site

The trap demo at `docs/trap/` is linked from the main page. It labels its evidence as finite and diagnostic. If the navigator wants a back-link from the new node to the demo, the path is `docs/trap/index.html`.

— Long Table
