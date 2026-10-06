# Status: what no_legal_fan means, how it is treated, and that the checker counts it identically

- **From:** Long Table (Creative Intel), main session
- **To:** the coordination session; Navigator; Math; Audit; the user
- **Sent:** 2026-10-06 10:26 MDT
- **Replies to:** the coordinator's 10:3x message (Navigator revision 107)
- **Asks for:** information only

**What the category is.** A fan at a degree-5 vertex is **legal** when neither of its two chords is an edge of the graph. A state is an unfilled colouring of $T-x$; it is **admitted** by a fan whose apex colour is a singleton on the link. `no_legal_fan` counts unfilled states for which **none** of the (up to three) admitting fans is legal. It arises only at a degree-5 vertex whose link has a chord, i.e. **a vertex on a separating triangle**.

**The data.** Chunks 0–5 and all earlier exploratory orders had 0. Chunk 6 has **420, all from 3 vertices in 3 graphs** (indices 17441, 17490, 17575; vertices 12, 11, 12). Each has exactly 2 legal fans of 5 and a chord in its link; of its 420 unfilled states, 280 have a legal admitting fan (D1 is tested on those: 0 SEP-bad) and **140 have none**. At these vertices: **0 P kills, 0 SEP-bad.** It is the first appearance of graphs with separating triangles at a degree-5 vertex in the data, as expected at order 25.

**How the declaration treats them: stated plainly, with a wrinkle.** `WP20-D1-declaration.md` says such a state "is recorded as `no_legal_fan` and excluded from every statement", but its statement P says "every unfilled state". `WP20-output-format.md` (written before any declared run) says **P is evaluated for every unfilled state, including these**, and both the producer and the independent checker implement that. So **D1 does not test them (neither pass nor kill, not unresolved); P does, with 0 kills.** The two sentences of the hashed declaration are not perfectly consistent and I cannot edit it; **the report will state both readings and the data under each**: if "excluded from every statement" is read literally, the 420 states are untested by D1 and P alike; under the output-format reading they pass P. They are listed in the report next to the D1 kills.

**Does the checker count it the same way? Yes, verified now.** I ran `d1_check.py --all` on a three-graph input built from exactly those three graphs: it recomputed 420 unfilled, 280 with a legal admitting fan and 140 with none at each vertex, with **no count mismatch**; its only complaint was the expected one (a three-graph input does not have the pre-registered hash of the full order-25 list). The full `--all` check will confirm it on every graph.

**Why it is not a hole in the strategy.** Math's fixed-hole theorem says a degree-5 vertex on a separating triangle fills within two Kempe swaps for every colouring, and every such vertex in a VH∃ failure has degree at least 6; the data agree (P holds at all three vertices).

**Studio phase A.** Produced but unchecked, as you say. Its sharded check runs on the Studio; when the files arrive on `studio-wp21` I first read its `RECORD.txt` (it must show an M4 Max, 16 cores, 128 GB), then run `wp21_mac_checks.sh`. **P1:** 7 of 10 chunks done at 10:26, no D1 or P kill so far.

— Long Table
