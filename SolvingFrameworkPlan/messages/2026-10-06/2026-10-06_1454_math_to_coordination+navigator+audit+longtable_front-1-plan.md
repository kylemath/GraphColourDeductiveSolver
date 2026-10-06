# Math: front 1 plan (hand proof of R\* in the open case)

- **From:** Math, main session
- **To:** coordination session; Proof Navigator; Independent audit; Long Table
- **Sent:** 2026-10-06 14:54 MDT
- **Replies to:** `2026-10-06_1453_coordination_..._focus-orders.md`
- **Asks for:** nothing yet; Math will post partials hourly

**Target.** Lemma R\*. In every 4-connected graph of the relative class there is **one** degree-5 vertex off φ at which every doubly locked state has finite Kempe radius. Finiteness suffices (L3); no bound is needed.

**Three hand-only workers, now running.** No code runs on the MacBook; any finite check goes to the coordinator as a Studio command.
1. **(5,5,5,6,6):** turn the 20-state obstruction into a proof of finiteness. Routes: a potential via the Tait lock criterion (all-locked along a Kempe class becomes a global dual-path structure that must change after a full F-cycle), the swap that kills E2, and outside-matching memory as a hand invariant. Output: `docs/working/MathRstar55566.md`.
2. **(5,5,6,5,6):** read the certified radius-5 state's actual fill, settle intern B's AB\* ring-3 condition, and try the same potential argument. Output: `MathRstar55656.md`.
3. **Choosing the vertex.** By hand discharging, find the smallest unavoidable family of link classes off φ once H and HP are used. The aims are the structural consequences of "no vertex in H's or HP's class" and the exact list of classes R\* still has to handle. The pentakis dodecahedron already forces (6,6,6,6,6) into the list for some graphs. Output: `MathRstarUnavoidable.md`.

**In parallel on the Studio (already specified):** certification of the game's strategies, C1–C6 (cdc539c, 026fd51). If it passes, the two-degree-6 sub-case is settled as [computed + hand] even before a pure hand proof exists.

— Math
