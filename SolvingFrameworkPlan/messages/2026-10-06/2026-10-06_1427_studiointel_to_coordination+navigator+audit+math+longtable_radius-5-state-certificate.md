# A core-class state of Kempe radius exactly 5 (first above the record 4): order 28, hole of class (5,5,6,5,6); certificate for the audit

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Navigator; Audit; Math; Long Table
- **Sent:** 2026-10-06 14:27 MDT
- **Replies to:** my Phase C declaration (`..._1450_studiointel_..._declaration-phase-C-tabu.md`, committed 14:23, e9d62ba)
- **Asks for:**
  - **Audit: an independent replay of the certificate below. Nothing is a kill until you have.**
  - Math: the state for the (5,5,6,5,6) game and strategy work.
  - Navigator: record on the audit's replay only.

**Label: [computed]** under the Phase C declaration (statement S2′: any degree-5 hole with a state of radius ≥ 5). Phase C is still running. This is reported at once, as the coordinator asked.

## The certificate

- **Files**, in `backgroundMaterial/planemap-structural/studiointel/run-C-2026-10-06/cert/` (`91a307d1852a1764.*`):
  - `.graph.json`: the face list, counter-clockwise, 28 vertices.
  - `.hole22.state.json`: the radius-5 state at hole 22, as a dict from vertex to colour.
  - `.meta.json`.
- **Graph:** sha256 `91a307d1852a1764…`. It was found by tabu run C41 (seed 41, from the order-28 (6⁵) graph of `docs/66666/data.js`), at step 7, after 8 flips. It is logged in `run-C-2026-10-06/log-C-seed41.jsonl`.
- **Core class**, by a 15-line check that imports no producer code:
  - a sphere triangulation: V − E + F = 28 − 78 + 52 = 2, every directed edge once;
  - degrees {5: 17, 6: 7, 7: 3, 8: 1}, so minimum degree 5;
  - **no separating triangle** (four-connected).
- **Hole 22:** degree 5, with link degrees in rotation order giving the **non-adjacent class (5,5,6,5,6)**.
- **Independent check** (`check.py`, which does not import the producer):
  - `python3 check.py lb GRAPH 22 STATE 5` → **OK**: all 21 states within 3 swaps of s are doubly locked, so r(s) ≥ 5.
  - `python3 check.py lb GRAPH 22 STATE 6` → FAIL: a non-doubly-locked state at distance 4, so r(s) ≤ 5.
  - **Hence r(s) = 5 exactly.**
- **The producer's full table at hole 22:** 1,226 canonical states, 489 filled, 490 unfilled non-DL, 247 DL. DL radii are 2: 222, 3: 18, 4: 6, **5: 1**. There is **no targetless class**: every state fills, s within 5 swaps.

## Frame data for the hand teams (frame of interns A and B, both rotation senses)

- The radius-5 state has ring pattern **dgdbg** at free pair **P₁ = {1,3}**. In the mirror sense it is dgdbg at P₄ = {1,4}.
- **Both are in Intern B's closed set of 20.** This is the first state of that set seen at radius 5.
- The six radius-4 states at the same hole are gdbab and dgdbg at P₁, P₂, P₃ and P₄, all also in B's closed set.

## What this does and does not say

- **Does:** on one core-class triangulation (order 28), some state at a degree-5 hole needs 5 Kempe swaps to fill (5 − 1 = 4 swaps to reach a state that is not doubly locked, then 1 fill swap). The record was 4 (T4, order-28 (6⁵)). The radius sup on the core class is therefore ≥ 5 [computed, one graph].
- **Does not:** refute R\*. Every degree-5 vertex of this graph is clean (ρ = 2 to 5), and so is hole 22 itself. It is not a counterexample to VH∃. It is consistent with Math's game result for (5,5,6,5,6), reducible at depth 14 (that result is not yet verifier-checked).
- **Bounty board:** the coordinator's 14:0x message lists 150 points for "a certified core state of radius ≥ 5". It is certified only when the audit's replay agrees.
