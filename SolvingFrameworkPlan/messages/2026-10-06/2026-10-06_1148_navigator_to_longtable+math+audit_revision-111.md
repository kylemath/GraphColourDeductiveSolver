# Revision 111: WP21 phase B by evidence (checked once, not cross-checked); Studio P1 replay started

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit
- **Sent:** 2026-10-06 11:48 MDT
- **Replies to:** branch `studio-wp21` commit `98358d0`; the coordinator's relay of the Studio's T2 start
- **Asks for:** Long Table, run `wp21_mac_checks.sh` on phases A and B on the first Mac

## Phase B, by evidence (read with `git show`; not checked out)

- The four output files on the branch hash to the values in `RECORD.txt` of the phase A commit: `B.json` `edf0bb57…3376`, `B-evaluated.txt` `def852ac…17e4d1`, `B-log.json` `f1d8e011…b9c2`, `seeds-B.txt` `6582d4e8…7065`.
- Run ledger: complete, 30,687 CPU-s, none wasted, not capped (cap 86,400). The report binds declaration `8fdd1aa5` and producers `d1_confirm.py` `bb350d3b` and `wp21_search.py` `b905888e` (the announced v2 hashes); tag WP21.
- Producer counts: 4812 evaluated graphs; 77,786 degree-5 vertices; 35,346,675 unfilled states; `no_legal_fan` 0; SEP-bad 1626 (all depth 1, 115 graphs); `filled_neighbour_for_bad` 0; **D1 kills 0; P kills 0**; P capped 0; locked classes 6158. The best chain objective is 1000 (chain 1). With no kill and no state of depth 2 or more, the objective is 20 × SEP-bad + locked classes, so this value is **not** a kill signal.
- Studio sharded check: `CHECK OK (all 25 ranges)`, binding checker `93975b05`, the output hash and the evaluated-graph list; unresolved 0.

**Status: produced on the Studio and checked once there; the first-Mac cross-check is pending. No result.** Phase B is an adversarial search. A pass would say only that **this search found no D1 or P counterexample among the 4812 graphs it evaluated**, nothing about order 26 as a whole.

## Studio T2 (the coordinator's relay)

T2 started 11:45:13 on the Studio (pid 32591, 254 shards). It is a **replay** of WP20 P1, not original data, compared with the first Mac by content digest. A difference between machines is reported, not smoothed. No file seen yet.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). No finite check is upgraded.
