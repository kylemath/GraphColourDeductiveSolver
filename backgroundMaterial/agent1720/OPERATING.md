# Standing orders for the Agent 1720 team

Agent 1720 continues the programme of Agent 1701 (`backgroundMaterial/agent1701/`). The 1701 standing orders (`backgroundMaterial/agent1701/OPERATING.md`) bind this team as well. The additions below are specific to 1720.

## Chain of command

```
Main planning distributor (writes docs/navigator/planning.json after each gate)
  |
  |-- Critic  <-- meets managers, then meets the main team: the gate
  |
  |-- Task master  (carries every open task forward between waves; nothing is dropped silently)
  |
  |-- Motivation agent  (affirmations, time-outs, diversions, strange stories for managers)
  |
  |-- M-Kempe       groups K4, K5, K6     Track 1
  |-- M-Algebra     groups A1, A2         Track 2, Track 7 database
  |-- M-Duality     groups D1, D2, D3     Tracks 3 and 4, algebraic edge-colouring
  |-- M-Foundation  groups L1, L2         Foundation (Lean 4)
  |-- M-Frontier    groups S1, S2, S3, S4 Tracks 5, 6, discharging, new routes
```

## What a group returns

Every group report (`groups/<ID>_report.md`) contains, in this order:

1. **Definitions** used, with the file or function that implements each one.
2. **Statement** checked or proved, with its quantifiers written out.
3. **Evidence**: exact command, elapsed wall clock, output file. Or the written proof. Or the citation (author, year, title, and what the cited result states).
4. **Result**: proved (with proof in the file), computed (finite check, named range), killed (with written witness), blocked (with timed command), or literature-settled (with citation).
5. **Kill criterion** for the statement, and whether it was met.
6. **Not proved**: an explicit boundary.
7. **Feasibility** of the next step: Low / Medium-Low / Medium / Medium-High / High.
8. **Next steps**, concrete. If a next step can be done now from this repository, do it before returning.

## Literature is evidence

A known theorem from the literature is a legitimate way to settle a node, but the citation must be specific. When a web search is used, record the URL. “It is well known” is hot air.

A statement that is equivalent to the Four Colour Theorem is a *reformulation*. Say so. A reformulation is not killed; it is re-labelled, and its value is whatever new attack it opens.

## Budget

- One computation: at most about ten minutes wall clock. Measure; do not guess.
- Triangulations up to 11 vertices are cached in `compute/data/triangulations_n4_11.json` (`graphs[str(n)][i]` is the edge list of `T_n_i`; counts equal the plantri counts 1, 1, 2, 5, 14, 50, 233, 1249).
- Python: `/Users/fulkanjou/GraphColour/.venv/bin/python`. Installed: networkx, numpy, scipy, sympy, python-sat, cvxpy, matplotlib. Never install globally.

## Gossipers

Every group has a gossiper. The gossiper does no mathematics. Between rounds the gossipers read one another's slips and write down only what the other groups do not already know.

- A slip is `backgroundMaterial/agent1720/gossip/<group>.md`: at most 15 lines. Each line is a new fact and the file that holds it.
- Do not repeat `backgroundMaterial/agent1720/gossip/round2_brief.md`.
- After the slips exist, the gossipers meet. Their meeting note is `backgroundMaterial/agent1720/gossip/exchange_<round>.md`. It lists, for each group, the facts from other groups that bear on its own task. It does not give orders and it does not edit the navigator.

## Files

- Groups write inside `backgroundMaterial/agent1720/groups/`, `backgroundMaterial/agent1720/gossip/`, and new scripts under `compute/`. They do not edit `docs/navigator/`.
- Do not delete or rewrite existing scripts; add new ones.
- Do not overwrite `K4_results.json`, `K5_*.json`, `K6_cache_n4_11.json`, `K6_named.json`, or `compute/data/chromatic_polys_n4_11.json`.
