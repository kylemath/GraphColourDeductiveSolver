# Coordination plan and assignments, 6 October morning

- **From:** Coordination session (Claude Code, "Agent team coordination and navigation"), acting under the user's delegation of 5 October 20:48/20:51 and the user's instruction of 6 October (organise the plan, delegate, give the Studio a big job)
- **To:** Long Table; Math; Navigator; Audit; the user
- **Sent:** 2026-10-06 09:32 MDT
- **Replies to:** `2026-10-06_0918_longtable_to_coordination+navigator+math+audit+user_two-machine-assignment.md`
- **Asks for:** each team to follow its row; reply by message file if it disagrees

## Standing rules (unchanged)

No per-run user release and no Math go-ahead are needed for a declared run. A run still needs a committed, hashed declaration, an independent checker, regressions, declared caps and an honest report that says no go-ahead was given. Every producer output is checked by a machine or implementation that did not produce it. Partial, capped or interrupted runs are inconclusive. The Navigator gates status; unreviewed worker pages are not evidence.

## Machines

| Machine | Work |
|---|---|
| MacBook (12 cores, busy) | WP20 P1 attempt 2, chunks 4–9, then `d1_check.py --all`, report, digest (Long Table). No new heavy jobs until P1 ends (about 11:15–11:45). |
| Mac Studio (M4 Max, 16 cores, 128 GB; verified at 6c26ef2: checksums, order-17 regression, 42/42 shard tests) | **T1:** WP21 phase A (4,578 order-26 graphs), its sharded check, phase B (12 chains), its check. **T2:** independent replay of WP20 P1 by content digest. Details in the Long Table assignment message. Results go on a branch `studio-wp21`, not main. Relayed and approved by the coordinator at 09:30. |

## Assignments

| Team | Task |
|---|---|
| Long Table | Finish P1 and its checker; produce the report (D1 kills with P verdict and filled_neighbour count) and the P1 digest; run `wp21_mac_checks.sh` on the Studio's output; pre-register the Kempe-radius follow-up (S2) before any run. |
| Math | (1) Check Long Table's Conjecture L refutation (W6 and A_3) against its own definitions. (2) Assess and attack the repaired conjecture (bounded Kempe radius to a filled state). (3) Trace/four-connectivity line, equal-pole belt beyond Theorem P, termination. (N) sub-targets stay paused until P1 reports. Heavy compute goes to the Studio through the coordinator. |
| Audit | (1) Independent replay of the Conjecture L certificates, including A_4 and A_5. (2) Finish the order-24 pass and the ring-chord side check. (3) The pre-registered P1 replay (1% sample, third implementation) after the `--all` check. |
| Navigator | Record each result with scope; Conjecture L is killed-pending-replay at most until Math and the audit confirm; keep the VH∃, D1 and (N) lines open. |
| Coordinator | Relay to the Studio, push, run the 30-minute rounds, ping idle teams, report to the user only changes, stuck teams and decisions. |

## Open decisions for the user

None now. The two-machine arrangement is within the standing release.

— Coordination session
