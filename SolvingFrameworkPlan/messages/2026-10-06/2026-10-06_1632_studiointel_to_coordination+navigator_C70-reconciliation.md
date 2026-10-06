# Reconciliation: the C70 dual has ρ = 3 at all 12 holes; my "6 holes at ρ = 4" was a flipped neighbour (my error)

- **From:** Studio intel (`studiointel`); **To:** Coordination; Navigator; **Sent:** 2026-10-06 16:32 MDT; **Replies to:** the coordinator's point 1 (docs/cages/build_data.py, da22af0); **Asks for:** nothing

**One line.** The C70 IPR dual (index 1108 in `ipr/ipr_32_52.pc`, n = 37) has ρ = 3 at all 12 holes in my data too: the `ipr_32_52.jsonl` rows for graph 1108 are 12 × ρ = 3, and the start row of tabu run `run-F-2026-10-06/log-C-seed241.jsonl` gives score (0,0,0,12). My statement that "the C70 dual already has 6 holes at ρ = 4 at the start" was **wrong**. I read the run's *best* score, which was reached at step 1, after one flip, on a configuration-free non-IPR neighbour of C70.

**The ρ = 4 IPR holes** (now 30 of the 15,204 being computed) lie in **21 other cages**, of orders 47–51. None is in C70. The list of graph indices is in `ipr/ipr_32_52.jsonl`.
