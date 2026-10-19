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

## Row 3: 8 85586556/66656565, finished 17:15Z (wall 15,923 s)
- **KILLED**: 40 two-engine kills, all D (kc D + dfast18 D), 0 C. They are at rings 14 (4), 15 (16) and 16 (20). The
  lowest are a8_u.558655._.665.5.., a8_u.558655._.66565.., a8_u855..556_66...5.5 and a8_u855..556_66...565 (ring 14).
- All 2,464 ring <= 16 windows run (40 kc D, 2,424 neither). After the first kill, 812 ring 17-18 windows were skipped.
- Files: row_8_85586556_66656565/kills.txt, results.txt, STATUS, and the kill windows' kc / dfast18 outputs.

## Long Table 18:09Z reorder: K=2 push on the 2/13 binders (rows 11 and 12 first)
- Rows 1 and 2 finalised (f-name collection wrapped up at a clean point, about 18:12Z; runners and engine children
  TERMed after their last completed window):
  - Row 1, 8 86555665/56586665: **KILLED**. 415 two-engine kills (284 D, 131 C) at rings 11-16; 2,398 of 2,655
    ring <= 16 windows run (257 not run), 247 ring 17-18 skipped.
  - Row 2, 8 86555665/56576665: **KILLED**. 489 kills (400 D, 89 C) at rings 11-16; 2,619 of 2,738 ring <= 16 run
    (119 not run), 185 ring 17-18 skipped.
- Rows 4-9 paused with SIGSTOP on each runner and its engine chain (12 processes, state T, 0 % CPU; PIDs in
  paused_pids.txt). The in-flight engines' wall alarms will fire on resume, so the plan is to relaunch fresh runners
  (completed windows are skipped). Paused time counts against nothing.
- 19:25Z 19 Oct: row 11 (binder 7 7665566/6765766, ring 17-18 todo, 225 windows), 6 parallel parts from 18:10Z:
  **SURVIVES**, 0 two-engine kills. 218 kc neither, 7 kc timeout at -t 600 (all ring 18: a7_u76..566_67....6,
  a7_u7665..6_67...6., a7_u7665..6_.7...66, a7_u76..566_67...6., a7_u7665..6_676...6, a7_u76..566_6...766,
  a7_u7665..6_6.6..66), 0 kc D, 0 kc C. Hypothesis (two-engine kill at ring <= 18) not met on the windows decided;
  the 7 timeouts carry no verdict.
- 20:15Z 19 Oct: row 11 addendum (Long Table 19:27Z; out/job52/row11_open.py, the row10_open method with kc -t 10800
  on a dfast18 D): the 7 ring-18 kc timeouts all **dfast18 D=false** (868-1,222 s each). No D, so no kc -t 10800 run
  and no cfast (no kc X). Row 11 final: 225/225 windows decided, 0 two-engine kills; the hypothesis (a two-engine
  kill at ring <= 18) fails on this binder row.
- 20:37Z 19 Oct: row 12 (binder 7 7766556/6576576, ring 16-18 todo, 414 windows), 6 parallel parts from 18:10Z:
  **SURVIVES**, 0 two-engine kills. 403 kc neither (99 ring 16, 192 ring 17, 112 ring 18), 11 kc timeouts at -t 600
  (all ring 18: a7_u77665.._65.6..6, a7_u77665.._6.76..., a7_u77665.._6576..., a7_u7.66556_6.7...6,
  a7_u776..56_657...., a7_u77665.._.57...6, a7_u77665.._6..6..6, a7_u776..56_.57...6, a7_u7766556_6.7...6,
  a7_u7766..6_.57...6, a7_u776..56_65...76), 0 kc D, 0 kc C.
