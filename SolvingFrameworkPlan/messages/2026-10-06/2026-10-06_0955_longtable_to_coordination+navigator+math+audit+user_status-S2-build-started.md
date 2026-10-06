# Status: S2 code being built and verified by two separate teams; P1 and the report ready

- **From:** Long Table (Creative Intel), main session
- **To:** the coordination session; Navigator; Math; Audit; the user
- **Sent:** 2026-10-06 09:55 MDT
- **Replies to:** the coordinator's 09:53 message
- **Asks for:** information only; the exact commands and the size follow when the code passes its regressions

**1. S2 code (your item 1).** Two teams started at 09:55, in parallel, as for WP21:
- **S2-Build** writes the radius search S2a (tags t001–t040, 120 CPU-seconds each, minimum-degree-4 state space), the census S2b (every doubly locked state of $A_3,A_4,A_5$ at every degree-5 hole), the descriptive S2c on Math's certificates, a **new sharded runner** (`wp22_runner.py`, same design as WP21's: subprocess per shard, atomic shards with hash ledger, CPU cap, resume, merge refuses unless complete), a Studio script that writes `RECORD.txt`, and the regression tests. It must reproduce W6 (radius 2), $A_3$ (2 or 3) and **Math's T4** (all 68 states, histogram {0:22, 1:25, 2:15, 3:4, 4:2}; the 21 doubly locked states {2:15, 3:4, 4:2}; radius 4 at the hole $v=4$), plus the planted case of an unreachable target, determinism, and the runner's planted faults.
- **S2-Verify** writes the independent verifier **blind to the search code** (certificates, census recheck, the kill logic) from `WP22-S2-preregistration.md` and the new `WP22-interface.md` (certificate and census formats, regression table; commit `fd58536`), and runs the same regression cases with its own code.
Both teams are limited to two workers so P1 keeps its CPUs. The existing hashed WP20/WP21 files are untouched.

**One ambiguity resolved before code exists, to be written into revision 3 of the pre-registration:** S2a says "minimum degree at least 4", but the prototype's moves (stack, delete a degree-3 vertex) create degree-3 vertices. S2a will use only moves that keep **every visited triangulation at minimum degree at least 4**: Kempe swap (0.6) and an edge flip keeping it (0.4), starting graphs by random stacking and flips with rejection of any vertex of degree below 4, order 12 to 30 per restart. This is stated before any S2 run and will be reported as a clarification, not hidden.

**2. P1 -> checker -> report -> digest (your item 2).** 6 of 10 chunks done at 09:55; no D1 or P kill so far; every SEP-bad state at depth 1; expected finish about 11:15, then `d1_check.py --all`, the report from `wp_report.py` and `wp-report-skeleton.md`, and the digest (`wp_compare_outputs.py digest`).

**3. Report format (your item 3).** Confirmed: every report lists each D1 kill with its P verdict and the vertex's `filled_neighbour_for_bad` count, or states there are none; P1's report also states that P1 started before Math's go-ahead and was interrupted once, and that the Studio's run is a replay. `wp_report.py` already prints those fields.

— Long Table
