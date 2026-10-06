# Revision 110: WP21 phase A by evidence on studio-wp21 (checked once, not cross-checked); Studio go-aheads from the coordinator

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit
- **Sent:** 2026-10-06 11:43 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-06/2026-10-06_1140_user_to_coordination+longtable+math+navigator+audit_studio-go-aheads-from-coordinator.md`; branch `studio-wp21` commit `5b86c4a`
- **Asks for:** Long Table, run `wp21_mac_checks.sh` on the branch's phase A output on the first Mac; the Studio, push the phase B outputs listed in `RECORD.txt`

## User decision (11:40)

Go-aheads for project work on the Mac Studio come from the coordination session, not from the user directly; the Studio's own permission settings still apply (Kyle confirmed in the Studio session, by relay). Package, independent-check, cap and gate rules are unchanged.

## WP21 phase A, by evidence (read with `git show`; the branch was not checked out)

- The branch adds 33 files, all under `wp21/`, on top of `e6110ff`.
- `RECORD.txt`: `Kyles-Mac-Studio.local`, **Apple M4 Max, 16 cores, 128 GB**, head `e6110ff`, 16 workers, 09:30:07 to 11:38:30 MDT.
- `A-m5-26.json` on the branch hashes to `1371118b…a839`, equal to the relay and to `RECORD.txt`. Run ledger: complete, 34,312 CPU-s, none wasted, not capped (cap 43,200).
- Studio sharded check: `CHECK OK (all 23 ranges)`; its global record binds checker `93975b05` (the announced v2 `d1_check21.py`), declaration `8fdd1aa5`, input `24e381cb` and the output hash; unresolved 0.
- Producer counts (`A-report-numbers.md`): 4578 graphs complete; 75,337 degree-5 vertices; 34,687,219 unfilled states; `no_legal_fan` 588; SEP-bad 102 (depth 1, 11 graphs); `filled_neighbour_for_bad` 0; **D1 kills 0; P kills 0**; P capped 0; locked classes 939. The output carries the WP20 tag, as declared for phase A.

**Status: produced on the Studio and checked once there; not cross-checked on another machine. No result.** WP21 is now `in-progress`. When the first-Mac check agrees, phase A is recorded as computed: no D1 or P counterexample **among the 4578 sampled order-26 graphs**, nothing more.

**Phase B:** `RECORD.txt` lists hashes for `B.json`, `B-evaluated.txt`, `B-log.json` and `seeds-B.txt`, so it appears finished by 11:38:30, but those files are not on the branch. Unverified.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). No finite check is upgraded.
