# Job 52: ring <= 18 reducibility of the surviving face-receiver rows (Long Table 19 Oct 12:45Z)

- Inputs: explore round 52's 10 row files win52_<d>_<link>_<s>_todo.txt, from bcb72b47 by path (counts as relayed:
  2902 / 2923 / 3276 / 1257 / 992 / 155 / 243 / 165 / 784 / 255). The pre-registration is EXPLORE-LOG round 52.
- **H52 (pre-registered by explore):** each row dies at ring <= 18. **Kill line per row:** a two-engine D (kc +
  dfast18) or C (kc + cfast --fixed with kc's X, leftover 0) window. Otherwise SURVIVES, or CAPPED at 6 h of wall
  clock.
- Runner: job52.py, one orchestrator per row, in ring order.
  - kc -C -s 60 -t 600 (loop/kc/kc). A kc D goes to dfast18 (out/job52/dfast18 = the 18 Oct build of
    wheels/studio/dfast18.cpp, ring <= 19; sha256 8e47c25f05d59d6b...). A kc C goes to studio15/cfast --fixed X.
  - After the first two-engine kill, only ring <= 16 windows are run on that row.
  - At most 4 concurrent ring 17-18 dfast18 / cfast calls (memory: about 2.3 GB each after 60 s at ring 17, estimated
    15-25 GB at a ring-18 peak).
  - Nice 10. k19 and j31r2 are untouched.
- Readiness smoke test (12:47Z), on ring 10 a7_u..55..5_..5...5:
  - kc 0.11 s (33 MB), dfast18 0.02 s, cfast 0.15 s. All three agree: D=false, 2,461 classes, 787 reached.
  - On ring 17 w17L_3, all three accepted the window and ran the full 60 s alarm.
  - Runner tested on known r7a kills: D a7_u..55675_..5.5.. (kc D + dfast18 D) and C a7_u..55675_....5.. (kc X={I0-I4}
    + cfast leftover 0).
- Started 12:50Z, all 10 rows in parallel. Nothing is admitted to any registry: explore does minkill and the f-names
  first.

## Row 10: 7 7655566/6759676, finished 16:28Z (wall 13,067 s)
- **SURVIVES**, with 4 windows undecided. 255 windows run: 251 kc "neither" (no D, no C) and 4 kc timeouts at the
  -t 600 limit, all ring 18: a7_u7655..6_675..76, a7_u7..5566_6...676, a7_u76..566_6...676, a7_u765..66_.7...76.
  No two-engine kill.
- Best leftover: 256 bad classes (0.04 % of classes) at a7_u7655566_675...6 (ring 15), X={I0-I5,I10-I11,R8-I5,R8-I11}.
- Row 10 addendum (Long Table 16:31Z), 19 Oct 16:33-17:12Z: the 4 ring-18 kc timeouts were run on dfast18
  (row10_open.py: heavy slots, 30 s poll behind rows 11 and 12, 20 GB floor, 6 h per window). All 4 are
  **dfast18 D=false**: a7_u76..566_6...676 (1,100 s), a7_u7655..6_675..76 (1,339 s), a7_u765..66_.7...76 (694 s),
  a7_u7..5566_6...676 (1,049 s). No cfast was run (there is no kc X). dfast18 peaked at about 9.6 GB RSS on ring 18.
- **Row 10 final: SURVIVES**, with all 255 windows decided: 251 kc "neither" and 4 dfast18 D=false. No two-engine
  kill. Best leftover 256 (ring 15).
