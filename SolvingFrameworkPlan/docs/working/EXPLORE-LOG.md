# Exploration log (newest first; protocol in EXPLORE-LOOP.md) [exploratory, engine level]

## Round 62 (21 Oct 2026, 08:08Z-): H-A83NF, do the rows of Opus's valid A83 fb-off cert die at ring <= 15?

**Pre-registered 08:08Z, before any containment or engine run on this list.** Opus 08:07Z: the fb-off nosep cert
`loop/opus/P_own_lp/s44/run_A83nf/cert_q44nfA83L.json` (Opus commit 9dd82e31, md5 ea86f98d; A83 240b5a08, l3q + rpatN3,
fb off) is valid, lower 132/1301 = 0.1015 against upper 0.1059; its 33 receiver rows (`binders_canon.txt`, md5 949f9d75)
replace round 61's fb nosep list. Round 61's queue is stopped after its current row r61c (76665566/55666665, on the new
list too); its window cache carries over.
- **Part 1, containment** (`loop/k55/row55.py`) on all 33 at main ea8944db (A86 = 2,715 D / 1,232 C) + 2026 set, and
  canon_key lookup (`loop/k59/canon59.py`) against the row files and this log for rows already swept.
- **Part 2, kill sweep** (`loop/k56/q56.py`, ring <= 15, DNW 3): the rows not dead at A86 and not already swept at ring
  <= 15, by |w|, face rows included in weight order (the top three rows include face rows).
- **Hypothesis.** The non-face rows die at ring <= 15 as in rounds 56-61; the face rows mostly do not. **Kill line:** under
  half of the swept non-face |w| dies at ring <= 15.
- **Guess.** Part 1: 5-8 of the 33 dead at A86 (60 percent; rounds 59a, 60f and 61b kills sit on near rows). Part 2: at
  least 70 percent of the swept non-face |w| dies (55 percent); at most a third of the swept face rows die (65 percent).
- **Part 1 result (08:12Z).** 9 of the 33 rows are dead through u at A86 (`loop/k62/row62.txt`), no 2026 hit: the top row
  7667565/7966555 (-0.0461) by r61b's f7_5657667_555...6 family; 7656667/6557655 and 7666567/5665565 (= r60f) by r60f's
  f7_..56776_..5.55. family; 9657656/5666555, 9657656/5667555, 7657665/7665665, 7566576/6676655, 8657656/6667556 and
  7657665/7665765 by r59a's f7_..56756_....66. family. Dead |w| 0.0961 of 0.3865. Guess 5-8 missed (9). Of the 24 alive,
  4 are already swept at ring <= 15 with no kill (7766656/6566556 at Studio for 16-18; 9656775/5556655, r60b, to-do 106
  windows for Studio; 7665566/6675676 and 7766556/6566576 to ring 16) and r61c 76665566/55666665 is finishing in round
  61's queue. Queue `loop/k62/rows62q.txt`: 19 rows (15 face, 4 non-face) by |w|, r62a 7676655/6667656 first, DNW 3, taking
  over when r61c closes (`loop/k62/q62.log`).
- **08:30Z, r61c (76665566/55666665, d8 non-face, -0.0042 here) dies; round 62's queue takes over.** Round 61's queue
  had run 1429 of the row's 2352 ring <= 15 windows in 32 minutes, with a kill already in hand, so I stopped it by hand
  (the rest were slow d8 ring-15 windows) and ran minkill47 on what was done: 26 kills, 26 f-names, 7 minimal (smallest
  f8_...55666_...66.5., ring 13, D on kc + dfast; 2 more D, 4 C, one with X={I0-I7,I1-I8,R0-I0} on a single ring vertex).
  Files `loop/k47/r61c_kills*` (cb4283d9). Admission head adm62a on main cc47b00a (k3x = A86), regression
  byte-identical: +16 D, +10 C (26 names, none on main), 0 lost, ring-merge and letter-9 guards unchanged,
  `loop/k62/adm62a/` (k3x_D d3901238, k3x_C 9001e009). The queue `loop/k62/rows62q.txt` started 08:30Z with r62a
  7676655/6667656 (1046 windows at ring <= 15), DNW 3.
- **08:59Z, r62a (7676655/6667656, d7 5-5-5 face row, -0.0461) has no kill at ring <= 15** (1046 windows, 0 kills),
  as expected for a d7 face row. To-do 622 windows (304 at ring 16, 189 at 17, 129 at 18),
  `loop/k47/win52_7_7676655_6667656_todo.txt` (md5 6794f7c7a7a4edf5b163172a78403c05). adm62a admitted at b253a4ad (A87 = 2,731 D / 1,242 C).
  Next r62b 7665566/7765766 (face, -0.0461).
- **09:06Z, r62b (7665566/7765766, d7 face row, -0.0461) has no kill at ring <= 15** (935 windows, 0 kills). To-do 391
  windows (114 at ring 16, 158 at 17, 119 at 18), `loop/k47/win52_7_7665566_7765766_todo.txt` (md5 01403e0e8691f73a56a36a0d3ba48ea6), held for Studio
  behind its three queued rows. Next r62c 7766655/6567659 (face, -0.0224).
- **09:11Z, the Formal thread's pair batch 4** (`/mnt/project-files/general-rule/triplewheel/kills_batch4.txt`, md5
  ae008728, copied to `loop/k60/in60/`): two kc kills at ring 16 in open cells, 7665566/6675676 w0 priv66 and
  7766556/6567566 w1 priv66. Containment at A87 (`loop/k60/cont60.py`, adm62a's k3x): neither holds a registry or 2026
  configuration (`loop/k60/cont60_batch4.txt`), so both are new. They go into kpriv (a record since Opus s49) once
  Studio's second engine is in; no explore core spent on them.
- **09:17Z, kpriv v4.** Studio tw4 (main ef61be62, out/job_tw4/done.txt): both batch 4 windows are D on kc and dfast18,
  adjacency checked. Added as g7_7665566_6.....6_w0:66 and g7_7766556_65....._w1:66 (ring 16, D2), each isomorphic to
  my own window. `loop/k60/kpriv.txt` = `kpriv_v4.txt` (md5 e286be4b8b0eb5117b0612ae54de90b6): 16 engine kills, 31 containment patterns;
  grid: 7766556 w1 and 7665566 w0 each dead 10 of 25. Copies in /mnt/project-files/explore/pair60/.
- **09:25Z, r62c (7766655/6567659, d7 face row, -0.0224) has no kill at ring <= 15** (876 windows, 0 kills). To-do 328
  windows (153 at ring 16, 101 at 17, 74 at 18), `loop/k47/win52_7_7766655_6567659_todo.txt` (md5 d94566865ea43bbab4e7437bd3e7f7c7), held. So far
  the three swept d7 face rows of the list have no kill at ring <= 15, as guessed. Next r62d 755676556/756556665
  (d9 face, -0.0142, 2888 windows at ring <= 15).
- **11:22Z, r62d (755676556/756556665, d9 face row, -0.0142) dies at ring 14.** The row's 7000 s cap ended the drive
  before every ring <= 15 window ran; 60 kills, 60 f-names, 10 minimal (3 D and 2 C at ring 14, 3 D and 2 C at ring 15),
  e.g. f9_...556755_...665... (ring 14, D on kc + dfast). Files `loop/k47/r62d_kills*` (bfd676a4). Admission head adm62b
  on main 031289d1 (k3x = A87), regression byte-identical: +41 D, +19 C (60 names, none on main), 0 lost, guards
  unchanged, `loop/k62/adm62b/` (k3x_D 4ebe6db2, k3x_C 3fd7d7d2). First face row of the list to die, a d9 hub as in
  round 58. Main 031289d1 promotes A83 [E2]: 132/1301 <= t* <= 0.105884. Next r62e 7556656656/7565555555 (d10 face).
- **11:26Z, r62e (7556656656/7565555555, d10 face row, -0.0096) dies at ring 14.** I stopped its drive by hand once
  kills were in hand and every ring <= 13 window had run (1054 of 4573 ring <= 15 windows done; the cap would have spent
  about two hours more on the ring 14-15 windows). Rule from here on, as for r61c: a row with a kill in hand and its
  ring <= 13 windows done is closed without waiting for the rest. 19 kills, 19 f-names, 5 minimal, all ring 14 and D on
  kc + dfast (e.g. f10_...5665665_....555555). Files `loop/k47/r62e_kills*` (1e215181). Admission head adm62c on main
  322cb1ad (A88), regression byte-identical: +19 D (19 names, none on main), 0 lost, guards unchanged,
  `loop/k62/adm62c/` (k3x_D 5dc8fa5a, k3x_C 3fd7d7d2 unchanged). Second face row of the list to die (a d10 hub).
  The queue restarted at 11:26Z on r62f 7675566/7566676 (non-face, -0.0092).
- **11:59Z, r62f (7675566/7566676, non-face, -0.0092) dies at ring 12.** All 1047 ring <= 15 windows ran: 19 kills,
  19 f-names, 2 minimal: f7_...5576_...665. (ring 12, C, X={I0-I1}) and f7_..65576_..66.5. (ring 13, C, X={I0-I1}).
  Files `loop/k47/r62f_kills*` (fff481c3). Admission head adm62d on main ee836bb3 (A89), regression byte-identical:
  +3 D, +16 C (19 names, none on main), 0 lost, guards unchanged, `loop/k62/adm62d/` (k3x_D 53611985, k3x_C a6dc9722).
  Next r62g 7665567/5765765 (face, -0.0078).
- **12:29Z, r62g (7665567/5765765, d7 face row, -0.0078) dies at ring 14**, the first d7 face row of the list to die
  (face w3 w4 s3, link 7665567, not the 7766556 family). All 1155 ring <= 15 windows ran: 21 kills, 21 f-names,
  2 minimal, f7_.556776_....55. and f7_5566776_....5.. (both ring 14, C, X={I0-I1}). Files `loop/k47/r62g_kills*`
  (c7ee18cc). Admission head adm62e on main 0355bbbd (A90), regression byte-identical: +8 D, +13 C (21 names, none on
  main), 0 lost, guards unchanged, `loop/k62/adm62e/` (k3x_D 704f2b00, k3x_C f68473fd).
- **12:57Z, Studio's ring 16-18 runs on the two swept non-face rows: no kill** (Studio 12:56Z, main 875ed193 / merge
  2671621c). 7766656/6566556 (k47, 652 windows): kc D or C on 0, neither on 630, 22 ring-18 windows hit the 600 s kc
  limit (out/job_k47/, on main at f6098c1d, timeouts.txt 22 lines). 9656775/5556655 (k47b, 106 windows, out/job_k47b/):
  kc D or C on 0, neither on 105, 1 ring-18 timeout. Asked Studio to run the 23 timeouts at kc -t 10800 before the face
  rows k47d/k47e, since a D there kills a row of |w| 0.033 or 0.024; Long Table set the order instead (12:58Z): A84
  upper, the s52c Lean batch, k47d, k47e, then the 23 timeouts with a kill line (stop if the first 8 give nothing).
  Studio's k47c (7676655/6667656) is running.
- **14:29Z, r62h (65656565555/65555667576, d11 face row, -0.0060) dies at ring 12.** It ran to the 7000 s cap (the
  early-close rule was not applied: nothing watched for it): 465 kills, 257 f-names, 12 minimal f-names (2 D at ring 12,
  5 D and 3 C at ring 14, 7 C at ring 15 among the 17 minimal windows), e.g. f11_.......5565_......57665 (ring 12, D,
  a placement avoiding u). Files `loop/k47/r62h_kills*` (fab77d05). Admission head adm62f on main f6098c1d (A91),
  regression byte-identical: +242 D, +15 C (257 names, none on main), 0 lost, guards unchanged, `loop/k62/adm62f/`
  (k3x_D de05aafd, k3x_C 379ee1d8). From 14:31Z `loop/k62/early62.py` applies the early-close rule by itself (stop,
  minkill47, mark the row closed, restart the queue). Next r62i 7556676/7567566 (face, -0.0060).
- **15:05Z, r62i (7556676/7567566, d7 face row, -0.0060) has no kill at ring <= 15.** All 1090 ring <= 15 windows ran
  (kc -C, then dfast/cfast) in 36 min: 0 kills. The 595 windows left (293 at ring 16, 183 at 17, 119 at 18) are in
  `loop/k47/win52_7_7556676_7567566_todo.txt` (3aeb605d). It is the fourth d7 face row with no kill at ring <= 15
  (after r62a-c); the to-do is held behind Studio's current order and goes to Long Table with the next admission head.
  Next r62j 7655566/6759677 (811 windows at ring <= 16, 693 at ring <= 15). Logged 15:08Z.
- **15:14Z, r62j (7655566/6759677, d7 face row, -0.0060) has no kill at ring <= 15.** All 693 ring <= 15 windows ran in
  9 min: 0 kills. To-do `loop/k47/win52_7_7655566_6759677_todo.txt` (69241d00): 235 windows (113 at ring 16, 79 at 17,
  43 at 18), held with r62i's. So far 5 of the 7 d7 rows in this queue have no kill at ring <= 15 (r62a-c, i, j); the d >= 9
  rows r62d, e, h all died. Next r62k 65565656556/65666666665 (d11). Logged 15:16Z.
- **15:38Z, r62k (65565656556/65666666665, d11 face row, -0.0052) dies at ring 15.** early62.py closed it on its own
  (first automatic close): 2 kills once all 921 ring <= 13 windows were done (1647 of 3379 ring <= 15 done). Minimal kill
  f11_..556565655_.........5. (ring 15, m 11, C with X = {I0-I4} on both engines: kc -C and cfast fixed X); its
  superset f11_..556565655_........65. is D on both engines. Files `loop/k47/r62k_kills*` (774ee3bb). Admission head
  adm62g on main dfaae8ee (A92), regression byte-identical: +1 D, +1 C, 0 lost, guards unchanged (ring-merge hold 3,
  letter-9 0), `loop/k62/adm62g/` (k3x_D 8a238386, k3x_C 26c6c0fe). Next r62l 7556656656/6565555555 (d10 face, 5038
  windows at ring <= 15). Logged 15:39Z.
- **15:41Z, adm62g admitted at main 152388f6 (A93 = 3,045 D / 1,306 C, md5 match).** Per Long Table, the r62i and r62j
  ring 16-18 to-dos (3aeb605d, 69241d00) went to Studio for its face-row slot, ahead of the 23 timeouts.
- **15:39Z, r62l (7556656656/6565555555, d10 face row, -0.0046) was already dead at A93.** early62.py closed it in a
  minute from the cache: 21 kills, 5 minimal f-names (all D at ring 14). 19 of the 21 are r62e's names, already on main
  since adm62c: r62e's row differs only at s0 (7 against 6), and row55 at A93 finds 19 registry names inside r62l's
  1.5-ball. So rows62_alive.txt (built at A86) was stale for it. Files `loop/k47/r62l_kills*` (f01b7133). Head adm62h on
  main 21d03c99 (A93) adds only the 2 new minimal D names, f10_..55665665_.....55555 and f10_.55.656656_.5..55.55.
  (ring 14): +2 D, +0 C, 0 lost, guards unchanged, `loop/k62/adm62h/` (k3x_D 76334228, k3x_C 26c6c0fe); optional.
- **16:00Z, r62m (9657765/5556655, non-face, -0.0046) has no kill at ring <= 15** (858 windows, mostly cached from round
  59). To-do `loop/k47/win52_7_9657765_5556655_todo.txt` (5e361e87): 108 windows (83 at ring 16, 25 at 17), held.
- **16:03Z, recheck of the rows not yet run against A93 + adm62h** (`loop/k62/row62_A93.txt`): r62o 7655667/6657655 holds
  12 registry names (e.g. f7_.556776_....55., r62g's kills, adm62e), so it is already dead; marked `R56_r62o.DONE` and the
  queue skips it. r62n, p, q, r, s hold nothing. Next r62n 7766555/6576956 (face). Logged 16:03Z.
- **16:01Z, r62n (7766555/6576956, d7 face row, -0.0046) dies at ring 13.** Most of its ring <= 13 windows were cached,
  and early62.py closed it in its first minute: 6 kills, 1 minimal, f7_..55776_..56.5. (ring 13, m 9, C with X = {I0-I3}
  on both engines). The d7 rows run so far: r62f, g, n died; r62a, b, c, i, j have no kill at ring <= 15.
- **16:03Z, r62o (7655667/6657655) closed the same way**, before its skip marker took effect: 4 kills, minimal
  f7_.556776_.5..55. (ring 14, C), the registry name already on main from adm62e. Head adm62i for both rows on main
  949eb544 (A94, adm62h admitted): regression byte-identical, +4 D, +4 C, 0 lost, guards unchanged, `loop/k62/adm62i/`
  (k3x_D 7c229314, k3x_C 9f8cfe39); files `loop/k47/r62n_kills*`, `r62o_kills*` (62ebab34). Row55 at adm62i: r62p, q, r,
  s still hold nothing (`loop/k62/row62_A94i.txt`). Next r62p 6556656656/6565655655 (d10 face, 5090 windows at ring
  <= 15). Logged 16:05Z.
- **16:06Z, admissions.** adm62h is on main at 949eb544 (A94) and adm62i at cff84a19 (A95 = 3,051 D / 1,310 C), both
  md5 match. Long Table: keep r62m's to-do held (small weight; its neighbour r60b survived ring 18). New rule: before
  each row, re-check the alive list against the current main (row55, as for r62o); explore reruns it after every close.
- **16:13Z, the A83 fb-off list at A95** (row55 of all 33 rows against main cff84a19, `loop/k62/row62_A95_all.txt`):
  19 rows dead, |w| 0.1646 of 0.3865 (42.6%; 0.0961 at A86). 14 alive (0.2219): 6 of them at Studio for ring 16-18
  (7676655/6667656, 7665566/7765766, 7766655/6567659, 7556676/7567566, 7655566/6759677 queued; 7766656/6566556 and
  9656775/5556655 already ran there with no kill), 7665566/6675676 and 7766556/6566576 ran there earlier (job57face, no
  kill), r62m held, and r62p, q, r, s still to run here. Long Table 16:12Z: target an upper below 0.1; Opus starts a
  stacked solve on A95; finish this list (d >= 8 first: only r62p is left, and it is running), then switch to the
  stacked solve's binders as soon as they arrive.
- **16:24Z, r62p (6556656656/6565655655, d10 face row, -0.0018) dies at ring 15.** early62.py closed it after 20 min
  (all 1029 ring <= 13 windows done, 2095 of 5090 ring <= 15): 4 kills, all D at ring 15, minimal
  f10_..55665665_..5.55.55. (m 14, kc + dfast). Files `loop/k47/r62p_kills*` (56e122fc). Head adm62j on main cff84a19
  (A95): regression byte-identical, +4 D, +0 C, 0 lost, guards unchanged, `loop/k62/adm62j/` (k3x_D e1029e2d, k3x_C
  9f8cfe39). Row55 at adm62j: r62q, r, s hold nothing (`loop/k62/row62_A95j.txt`). Every d >= 8 row of the list is now
  dead. Next r62q 7666675/7575755 (d7, non-face). Logged 16:25Z.
- **16:27Z, r62q (7666675/7575755, d7 non-face row, -0.0015) dies at ring 14.** early62.py closed it 2 min in (500
  ring <= 13 windows done): 3 kills, 2 f-names, both D on kc + dfast at ring 14, minimal f7_.576666_55.5.5. (m 11) and
  f7_5766667_5.5.5.5. Files `loop/k47/r62q_kills*` (10b01f1c). Head adm62k on main 5e5cfd02 (A96, adm62j admitted):
  regression byte-identical, +2 D, +0 C, 0 lost, `loop/k62/adm62k/` (k3x_D d76bc52f, k3x_C 9f8cfe39). Row55 at adm62k
  (`loop/k62/row62_A96k.txt`): both names sit inside r62r 7666675/7565755 too, so r62r dies with this head (it is
  running; early62.py will close it from the cache); r62s 7766555/6566959 holds nothing. Logged 16:27Z.

## Round 61 (21 Oct 2026, 06:53Z-): H-A83N, do the rows of Opus's A83 nosep cert die at ring <= 15?

**Pre-registered 06:53Z, before any containment or engine run of this round.** Opus 06:51Z: the A83 nosep cert
`loop/opus/P_own_lp/s44/run_A83/cert_q44fbA83L.json` (e484da88, Opus commit 9757148b; l3q + rpatN3 + fb6 cap 3 on
240b5a08, upper FEASIBLE 0.105884 one engine, lower 0.0990, loose), 36 canonical receiver rows (`loop/k61/rows61_all.txt`),
to be weighed with the keeppen duals of round 60. canon_key (`loop/k59/canon59.py`, `loop/k61/lookup61.txt`) against every
row file in loop/k4*, k5*, k60 and this log: 19 rows new (8 face, 11 non-face); 17 seen, of which 7766556/6576576 and
7665566/6675676 are the exhausted face rows and most others are round 59's unswept filler queue (r59c on).
- **Part 1, containment** (`loop/k55/row55.py`) on all 36, registry main 517b0129 (= 7cd777a3's k3x) + 2026 set.
- **Part 2, kill sweep** (`loop/k56/q56.py`, ring <= 15, DNW 2 while the third core runs pair work): the non-face rows
  not dead and not exhausted, by |w|, merged ahead of round 60's remaining face rows; then the new face rows by |w|.
- **Hypothesis.** Most non-face rows die at ring <= 15, as in rounds 56-59. **Kill line:** under half of the non-face |w|
  dies at ring <= 15.
- **Guess.** Part 1: 0-2 rows already dead (60 percent). Part 2: at least 70 percent of the non-face |w| dies (55 percent);
  at most 2 of the 8 new face rows die (70 percent).
- **Part 1 result (06:56Z).** 4 of the 36 rows are dead through u at main 517b0129, all by round 59a's minimal kill
  `f7_..56756_....66.` (ring 13, C, X={I3-I4}, admitted after the cert's base 240b5a08): 8657656/6667556, 7566576/6676655,
  7657665/7665765 (new) and 7657656/7666556, all non-face; no 2026 configuration hits a row through u (`loop/k61/row61.txt`).
  Guess 0-2 missed (4). Sweep queue `loop/k61/rows61q.txt`: 34 rows (r60f first, then the non-face rows by |w|, then the
  face rows, round 60's r60c-r60g merged in by |w|), started 06:54Z, DNW 2 (`loop/k61/q61.log`).
- **06:59Z, pre-registered before any verdict: the two other open five cells of the pair grid**, by the same
  windows. 7766655/6567659 w0 cell 95 (b = 5 next to s6, a on the ring; a = 5 is already dead) and 7666567/5665565 w6
  cell 59 (a = 5 next to s6, b on the ring; b = 5 is already dead). `loop/k60/pw60.py` base window plus
  `loop/k60/pw60x.py` grown by every subset of the other exact apexes, ring <= 16: 6 windows for 7766655 w0 (all ring
  16; s6 = 9 is open, so the base already has ring 16), 12 for 7666567 w6 (2 at ring 15). Run in `loop/k60p` (drive45,
  NW 1, STOP 0), 7766655 first since r60f's row sweep may make 7666567 moot. **Hypothesis:** as at 9656775 w5, one
  added 5 apex beside the pair kills the cell. **Kill line:** no window of a cell dies. **Guess:** 7766655 w0 dies
  (35 percent: the open s6 leaves less of the ring closed), 7666567 w6 dies (55 percent).
- **The two other open five cells, result (07:09Z).** 7666567/5665565 w6 cell 59 dies: the two ring-15 windows
  `...5565` (adds s3, s4) and `5..5565` are D on kc and dfast (`loop/k60p/KILL`), so **a = 5 next to s6 at w6 is dead for
  every b**; the 10 ring-16 windows were not run (stopped once the cell was dead). 7766655/6567659 w0 cell 95: all 6
  windows (ring 16) are not D on kc (reached 24-59 percent of the classes) and kc found no C for any, so that cell is not
  dead; the kill line holds for it. Guesses: 7666567 dies (55 percent) right, 7766655 dies (35 percent) not. With
  9656775 w5, 8 of the 9 link 7s of the pair table have no five private left; the one open five cell is 7766655/6567659
  w0, b = 5 next to the >= 9 apex s6, a >= 6. None of the 5 pair-table rows is a row of Opus's A83 nosep cert except
  7665566/6675676 (canon59), so the queue core went back to the row sweep (q61 restarted with DNW 3, 07:09Z, resuming from
  the window cache).
- **kpriv v3 (07:09Z).** `loop/k60/kpriv.txt` (md5 2b824170064aa2afe94224945449c218; v2 kept as `kpriv_v2.txt`): 14 engine kills
  (v2's 11 plus g7_.656775_..5.65._w5:.5, g7_.656775_.5..65._w5:.5 and g7_7666567_...5565_w6:5., the minimal ones by
  letters), 31 containment patterns unchanged. `loop/k60/kpriv60.py` now reads a grown window's apex letters from its
  x60 name; each new kill is checked isomorphic to my own window and contains no registry or 2026 configuration. Grid
  `loop/k60/pair60_grid.txt`: 9656775 w5 dead 10 of 25, 7666567 w6 dead 9 of 25. Copies in /mnt/project-files/explore/pair60/.
- **07:19Z, r60f (7666567/5665565, round 60's keeppen binder) dies at ring 14.** Its ring <= 15 windows gave 17 kills,
  17 f-names, 2 minimal: f7_..56776_..5.55. (ring 14, C, X={I0-I5}) and f7_5666776_....5.. (ring 15, C, X={I0-I7}).
  Files `loop/k47/r60f_kills*` (8e891e37). Admission head adm61a on main 1985544f, regression byte-identical: +4 D,
  +13 C (17 names, none on main), 0 lost, ring-merge and letter-9 guards unchanged, `loop/k61/adm61a/` (k3x_D cf3a0094,
  k3x_C 7575c7ca). Its pair windows (Long Table 05:40Z, if no kill) are not needed. Next row r61a 7766656/6566556 (07:21Z).
- **07:28Z, r61a (7766656/6566556, the top non-face row, = round 59's r59b) has no kill at ring <= 15.** All 1159
  ring <= 15 windows ran (r59b had done the 776 at ring <= 14): 0 kills. To-do for Studio: 652 windows (213 at ring 16,
  295 at 17, 144 at 18), `loop/k47/win52_7_7766656_6566556_todo.txt` (md5 2c099d2c0f4f94e6f55e6179a1c18085). adm61a was
  admitted at bd503acc (A85 = 2,711 D / 1,231 C). Next row r61b 7667565/7666555 (07:29Z).
- **07:58Z, r61b (7667565/7666555, non-face) dies at ring 13.** Its 1185 ring <= 15 windows gave 5 kills, 5 f-names,
  1 minimal: f7_5657667_555...6 (ring 13, D, kc + dfast). Files `loop/k47/r61b_kills*` (6f29eda1). Admission head adm61b
  on main 183648ae (k3x = adm61a), regression byte-identical: +4 D, +1 C (5 names, none on main), 0 lost, guards
  unchanged, `loop/k61/adm61b/` (k3x_D c1b1b4e1, k3x_C 6c27df6f). Main 183648ae records Opus s49: the private-split row
  key is not funded, kpriv.txt stays as a record, the lever is registry kills on the binders; so no more pair windows
  here, all cores stay on the row sweep. Next row r61c 76665566/55666665 (d8, 07:59Z).

## Round 60 (21 Oct 2026, 05:36Z-): H-A83, do the top binders of Opus's A83 keeppen solve die at ring <= 15?

**Pre-registered 05:36Z, before any containment or engine run of this round.** Opus 05:25Z: the A83 keeppen (l3q + rpatN3
+ fb6 on 240b5a08) converged at t = 0.105884, one engine, not a bound; its top receiver rows (keeppen duals, not yet the
nosep cert's canonical binders). Long Table 05:25Z: these come first, ahead of the round 59 filler and the 59s census
(both paused at 05:36Z); check against main 7cd777a3 and the 2026 set, then windows at rings 12-15; reconcile with the nosep
cert when it lands. Rows `loop/k60/rows60k.txt`. canon_key (`loop/k59/canon59.py`):
- 7665566/6675676 (dual -0.0281) is the exhausted face row (rounds 57-58: every window to ring 18 run, no kill); no rerun.
- 9656775/5556655 (-0.0210, non-face) was in round 55's A67 list, never swept.
- New: face rows 7766655/6567659 (-0.0200), d9 755676556/756556665 (-0.0143), 7655667/7657655 (-0.0118), d10
  7556656656/7565555555 (-0.0087); non-face 7666567/5665565 (-0.0107).
- **Part 1, containment** (`loop/k55/row55.py`) on all 7, main 7cd777a3 (k3x = adm59a's, efdd2d6c / 808b8aff) + 2026 set.
- **Part 2, kill sweep** (`loop/k56/q56.py`, ring <= 15, DNW 3) on the 6 rows that are not exhausted, non-face first.
- **Hypothesis.** Both non-face rows die at ring <= 15. **Kill line:** neither does.
- **Guess.** Part 1: no hit (75 percent). Part 2: both non-face rows die (65 percent); of the 4 face rows, the d9 and d10
  rows die and the two d7 rows do not (40 percent).
- **05:36Z, part 1: no hit** (`loop/k60/row60.txt`): none of the 7 rows holds a configuration of the registry at 7cd777a3
  (4,505 with RSST) or of the 2026 set. Guess right. Part 2 started 05:36Z (`loop/k60/rows60q.txt`, log `loop/k60/q60.log`).
- **05:38Z, Long Table's add-on (b): the bare 5-5-5 triangle is not reducible** (expected so; a run to cite). Three interior
  5s, ring 6, kc line `t555_r6 6 3 0,4,5;0,1,2;2,3,4 1,2;0,2;0,1` (`loop/k60/tri/`): kc -C D=false (31 classes, 17
  reached), C=false (|X| <= 4, 121 admissible X tested, best leaves 2); dfast D=false. Add-ons (a) triple wheel and (c)
  reach-2 census follow the A83 rows.
- **05:47Z, add-on (a), the C3 triple wheel (Kyle's logbook, via Long Table 05:26Z; coordinator 05:39Z/05:42Z): our kc
  agrees on all 10 windows, and none of them is a new configuration.** My own builder (`loop/k60/tw60.py`, free disc,
  each u_i of row 7766556/6567566 with link w0, w1 = u_(i+1), u_(i+2) counterclockwise) finds the wheel realisable (45
  vertices, 27 closed), and its windows C_13, C_14 and C_18 are isomorphic (`loop/k60/tw/iso60.py`, networkx) to the
  "Formal problem statement" thread's TC3_C13/C14/C18 (ring 15 each). Our kc -C on their 10 lines (data copy in
  `loop/k60/tw/in/`, `kc3b.log`): D on C13, C14, C18, P11, both P12 and P10 (ring 14-15); neither D nor C (|X| <= 4) on
  P7, P9 and P8, as their kc said. Our dfast: D on my tw13 (depth 10, 31 s); the rest of the dfast runs were stopped,
  as Studio's dfast18 already has the second engine. **Containment** (`loop/k60/tw/twreg60.py`, registry main 7cd777a3):
  the wheel's closed vertices hold RSST 62 (C), RSST 80 (D) and RSST 137 (C), three placements each, and one RSST 137
  placement lies inside the two-hub window P11: {u0, w4, w5, w6, s6, w0 = u1, w0's private next to s6} (`twreg60.txt`).
  So the two-hub windows and the wheel are already excluded by the registry. For the LP: P11 is row 7766556/6567566
  plus w0's two privates (both 5, as u1 has the same row), radius 2 from u0. A receiverR2 row fixes only u, link and
  apexes, so pcheck cannot see a configuration that needs a link private; rows split by the big link vertices'
  privates would be needed (told Long Table 05:52Z).
- **05:52Z, pair table by containment** (`loop/k60/pair60.py`, for the other thread's pair census: rows 7766556/6567566,
  7665566/6675676 and 7766655/6567659, each link 7 w_k, its privates a (next to s_k) and b (next to s_(k-1)) at 5..9).
  First lines, 7766556/6567566 at w0: b = 5 dies by RSST 137 (priv55 also RSST 62, priv65), a = 5, b = 6 by RSST 187;
  priv57, 58, 59, 66 and 67 open (registry 70-81 percent of their open completions). Sent to that thread with our
  earlier results on its rows (rounds 52-53, 57-58).
- **06:09Z, Formal thread's pair census, batch 1 (10 kc D lines, data copy `loop/k60/in60/`): 6 already hold a registry
  configuration** (`loop/k60/cont60.py`, `cont60_batch1.txt`): 7766655/6567659 w1 priv55, 56, 57, 59 (RSST 187), priv65
  (RSST 221), 7665566/6675676 w0 priv75 (RSST 180). The other 4 hold no registry or 2026 configuration and our kc -C says
  D on each (`loop/k60/in60/kc4.log`): 7766556/6567566 w0 priv57 (ring 17), w0 priv59 (16), w1 priv75 (16),
  7766655/6567659 w1 priv66 (16); Studio's dfast18 has them. Naming check: my own pair windows (`loop/k60/pw60.py`)
  are isomorphic to theirs name for name (a = private next to s_k). If they hold, w0's private next to s0 at 5 dies on
  7766556/6567566 for every partner but 8 (priv58, ring 18, running there).
- **06:07Z, r60b (9656775/5556655, non-face): no kill at ring <= 15** (851 windows; 106 at ring 16 left,
  `loop/k47/win52_7_9656775_5556655_todo.txt`). r60f (7666567/5665565) started 06:07Z.
- **06:09Z, pre-registered at launch (no verdict read yet): pair windows on r60b** (Long Table 05:40Z: pair windows for the
  round 60 non-face rows with no kill). My builder `loop/k60/pw60.py`: u + every exact link vertex + s_(k-1), s_k + w_k's
  privates at (a, b), for the link 7s w4 and w5 (50 windows, rings 14-21, `loop/k60/pairkc/pw_9656775.txt`). Containment
  (`pairkc/cont_9656775.txt`): w5 55 and 65 hold registry configurations, w5 56 and 66 hold 2026 ones; the 13 open ones at
  ring <= 16 run here (`loop/k60p/`, drive45 copy, NW 1, STOP 0, kc -C then dfast/cfast). **Hypothesis:** a pair window
  kills at least one (a, b) child at ring <= 16. **Kill line:** none of the 13 dies. **Guess:** 2-4 of the 13 die
  (50 percent), mostly with a five among a, b.
- **06:22Z, private-split kills file, version 1** (Long Table 06:19Z ruling: name form g<d>_<link>_<s>_w<k>:<pp>, kept out of
  k3x in out/job30/kpriv.txt, which Long Table commits to main; the LP reads it only through a split row key). Built by
  `loop/k60/kpriv60.py` as `loop/k60/kpriv.txt` (md5 3f3bb86315179f1a8898a5ec6153b62d): 6 engine kills (the Formal thread's
  4, two-engine on Studio main cff0fe6f plus our kc; r60b's w4:55 D and w4:56 C from the pair windows here) and 5
  containment patterns (RSST 062, 137, 187 and nl1338 placements). Each engine kill is named from my own window and
  checked isomorphic to the line the engines ran on. Reading of a 9 in a pair name: the private is on the ring, so
  g7_7766556_6.....6_w0:5. (priv59) kills w0's private next to s0 at 5 whatever the other private is; with RSST 137 at
  w0:.5, w0 of 7766556/6567566 has no five among its privates in any surviving completion, and w1 loses the five next
  to s1 (RSST 137 at w1:5.; w1:75 kills one more cell).
- **06:44Z, r60b pair windows: 3 of the 13 open ones at ring <= 16 die, all at w4** (`loop/k60p/`, KILL): w4:55 D (ring 15,
  kc + dfast), w4:56 and w4:65 C (ring 16, X = {I4-I5}, interior only, kc -C + cfast --fixed leftover 0). No kill at w5
  (59, 95, 99 at ring 15; 57, 69, 75, 96 at 16) or at w4 59, 95, 99. Hypothesis held, kill line not hit; guess (2-4)
  right. The row stays alive: w4 with a five beside a 5 or 6 dies, everything else is open (ring 17-21 windows not
  run). w4:55 and w4:56 are in kpriv v1; w4:65 goes into v2.
- **06:44Z, the Formal thread's batches 2 and 3**: containment (`loop/k60/cont60_batch2.txt`, `cont60_batch3.txt`):
  7665566/6675676 w0 priv95 holds RSST 180; 7766655/6567659 w0 priv55, 56, 59 hold nl1323_r15 (2026 set). The other 4
  (7766556/6567566 w0 priv66 ring 17, w1 priv95 ring 15; 7766655/6567659 w1 priv75 ring 16, w1 priv95 ring 15) are D on
  Studio's kc + dfast18 (main 9ce86aa4, 4dffd10a); our kc -C: D on w0 priv66 and 7766655 w1 priv75
  (`loop/k60/in60/kc_b2.log`), batch 3 running.
- **06:49Z, pair table done and kpriv version 2.** pair60 finished in a fast containment-only mode (FAST=1, RESUME=1, the cells
  already counted kept their coverage numbers) on the 3 face rows and the 2 non-face round 60 rows, 9 link 7s x 25 cells
  (`loop/k60/pair60.txt`). Grid with the engine kills (`loop/k60/grid60.py` -> `pair60_grid.txt`): dead cells per link 7
  are 10, 9 (7766556 w0, w1), 9 (7665566 w0), 5, 10 (7766655 w0, w1), 9, 7 (9656775 w4, w5), 9, 6 (7666567 w0, w6). Every
  five among a link 7's privates dies on 6 of the 9 (both sides); the open five cells are 7766655 w0 b = 5 with a >= 6,
  9656775 w5 b = 5 with a >= 7, 7666567 w6 a = 5 with b >= 7. Cells with both privates >= 6 are open almost everywhere
  (E at 7766556 w0:66 and 7766655 w1:66). kpriv v2 (`loop/k60/kpriv.txt`, 11 engine kills, 31 containment patterns).
- **06:50Z, pre-registered before any verdict: grown pair windows on 9656775/5556655 w5, the open five cells** (b = 5, next to
  s4, with a >= 7). `loop/k60/pw60x.py`: the pair window plus every subset of the other exact apexes s0, s1, s2, s6, at ring
  <= 16 (38 windows, `loop/k60/pairkc/x60_9656775_w5.txt`; cells 95 = a on the ring, 75, 85), run in `loop/k60p` (drive45,
  NW 1, STOP 0). **Hypothesis:** a window with a on the ring dies, so b = 5 dies at w5 for every a. **Kill line:** no
  window dies. **Guess:** some 95 window dies (45 percent): the ring-14 ones add the 5s s1, s2 beside s4's side.
- **Grown pair windows on 9656775/5556655 w5, result (06:59Z).** Stopped after 15 of the 38 windows, all 13 at ring <= 15
  and 2 at ring 16, because the hypothesis was settled. 12 windows are D on kc and dfast (`loop/k60p/KILL`): 10 of the
  95 cell (a on the ring) and 2 of the 75 cell; a 13th (75 `..5.65.`, ring 16) was D on kc when dfast was stopped. Only
  the windows adding s6 alone (`....655`) are not D. The smallest kills add one 5 apex beside the pair: `..5.65.` (s2)
  and `.5..65.` (s1), ring 15, and `.55.65.` (both) at ring 14. A 95 kill leaves a on the ring, so it holds for every a:
  **b = 5 at w5 is dead for every a**, the hypothesis holds and the kill line (no window dies) is not hit. Guess (some 95
  window dies, 45 percent) right. Name for kpriv: g7_.656775_..5.65._w5:.5 (and the s1 twin).

## Round 59s (21 Oct 2026, 05:26Z-): H-SAT, does capacity transport pay the face row 7766556/6567566 in every completion?

**Pre-registered 05:26Z, before any run of this census.** Long Table 05:13Z (doc "Capacity transport rule",
https://claude.ai/artifact/CjS4g6uaJQyT1nuAdswLzG; first before the round 59 filler rows, 05:18Z; diagnostic only, nothing
admitted). Stage 1 equal split (each 5 splits its unit over its neighbours of degree >= 7); stage 2: an overloaded big u
sends each adjacent big v with spare min(sigma(u)/k(u), kappa(v)/m(v)). On the row (u = 7, link 7766556, s 6567566):
w5 pays u 1, w4 pays u 1/2 (s3 = 7), so L(u) = +1/2, to go to w0 and w1.
- **Window:** u's 2-ball closed (u, link and s all exact), w0's privates p0a (next to s0), p0b (next to s6) and w1's p1a
  (next to s0), p1b (next to s1) each 5..9; a private at 5..8 is closed and its neighbours become slots; every other
  boundary vertex is a slot 5..9 (9 = >= 9, never exact). Open fillings only (each slot above its disc degree); the
  closing fillings' share is reported beside. `loop/k59/sat59.py` (frame from chain59.py).
- **Loads:** L(w0) = -1 + sum over w0's 5-privates x of 1/l(x); L(w1) = -1 + 1/l(s1) + sum over w1's 5-privates of 1/l(x);
  l = number of neighbours of degree >= 7 (letters 7, 8, 9). kappa = max(-L, 0).
- **Dead** if the registry (main 517b0129 k3x + RSST 582) holds a configuration in the window, or u is saturated: k = number
  of w0, w1 with spare >= 1, and kappa(v)/m(v) >= 1/(2k) for each. m(v) is counted two ways: m_lo = u (+ the other link 7
  if it is overloaded) and m_hi = m_lo + v's large privates (their loads lie outside the window). Long Table's short form
  (kappa(w0), kappa(w1) >= 1/4) is reported too; the 2026 set is matched apart.
- **Hypothesis (Long Table):** every completion dies. **Kill line:** a survivor the registry does not kill falsifies the
  rule on this row.
- **Guess.** Survivors exist (70 percent), where w0's two privates are 5s that pay it in full (w0 then carries a 5-5 edge of
  its own, the arrangement the 44/421 cert gives it).

## Round 59 (21 Oct 2026, 05:08Z-): H-FB6, do the new binders of Opus's A78 fb6 cert die at ring <= 14, and does a run of face 7s force a configuration?

**Pre-registered 05:08Z, before any containment, engine or census run of this round.** Coordinator 05:01Z: next round on
the newest shared cert, row55 first, then the non-face rows not yet swept; plus Opus's census question. Newest shared
cert: `loop/opus/P_own_lp/s44/run_A78/cert_q44fbA78L.json` (Opus 54c2c642; l3q + rpatN3 + fb6 cap 3 on A78 b6dc7610,
128 ring-merge hold-outs; nosep lower VALID 0.093306161 after exact repair, upper still 0.109439357), 48 receiverR2 rows
(sum |w| 0.3998), as `loop/k59/rows59_all.txt` from `binders_canon.txt`. Opus's A83 solve is still in K. canon_key
(`loop/k59/canon59.py`) against every row in loop/k4*, k5* (contents and file names) and this log:
- 7766556/6567566 (27.35% of |w|) is the exhausted face row (rounds 57-58, rule-side).
- 7656766/6556656 (0.43%) and d8 76555566/66757666 (0.02%) are r58j and r58f, dead and admitted at 240b5a08, after A78.
- **43 rows are new: 34 non-face (61.67% of |w|), 11 face (10.53%).** Two of the 34 (7566576/6676655, 7656765/7556766)
  were in round 55's A67 list but never swept. Face rows here include d11 65556565556/65955559565, d10
  7556656655/6565555656 and d8 76556755/76567666.
- **Part 1, containment** (`loop/k55/row55.py`): registry at main 93441313 (out/job30 k3x, 2,704 D / 1,214 C) and the
  whole 2026 set on all 48 rows, through u or avoiding it. Control: r58f and r58j must hit their own kills.
- **Part 2, kill sweep** (`loop/k56/q56.py`, ring <= 14, DNW 3) on the new rows Part 1 leaves, non-face by |w| first, then
  face rows; leftovers' ring 15-18 windows go to Studio as to-do files, kills to Long Table as admission heads.
- **Part 3, face-7 chain census** (Opus's question: does a long run of face 7s in their sea of 6s force a registry
  configuration?). Default reading unless Opus refines it: a chain of L face 7s, each paying a k-vertex 6 (fb6) that is
  adjacent to the next face 7; chain bigs exactly 7, chain 6s exactly 6, faces 5-5-5, every other vertex of the chain's
  1-ring free over 5..8 and 9 (9 = >= 9, never fixed in a window). Coverage = share of fillings holding a configuration
  of the main registry, RSST or the 2026 set, for L = 1, 2, 3.
- **Hypothesis.** Most new non-face rows die at ring <= 14, as in rounds 56-58. **Kill line:** less than half of the new
  non-face |w| (30.8% of the cert) dies at ring <= 15 here or at Studio. For Part 3: coverage climbs with L but stays
  below 100% at L = 3 (no termination lemma from the registry alone).
- **Guess.** Part 1: 1-4 new rows hit, beyond the 2 controls (55 percent). Part 2: at least 80% of the new non-face |w|
  dies at ring <= 14 (60 percent); at most 3 of the 11 face rows die (65 percent). Part 3: L = 1 under 90%, L = 3 under
  100% (60 percent).
- **05:09Z, part 1: 3 new rows are already dead** (`loop/k59/row59.txt`, 36 s; registry at 93441313 = 4,498 with RSST).
  d8 76656566/56655665 (11.16% of |w|) holds r58d's f8_...65656_...6556., 7666766/7556565 (1.87%) r58i's
  f7_..66676_..55.5., 7667656/7566556 (0.55%) f7_5676676_5..5..5; every hit runs through u (`loop/k59/sites55_rows59hit.txt`),
  so A83 drops them. Controls pass: r58f (40 hits) and r58j hit. No 2026 hit on any row. Guess right (3 new rows).
  Part 2 started 05:10Z on the other 42 (`loop/k59/rows59q.txt`, r59a-r59ap, log `loop/k59/q59.log`).
- **05:13Z, Opus: this cert is a weak nosep cert** (lower 0.0933, below the [E2] 44/421; fb6 is about 0 in the converged
  A78 solution), so its non-face rows mostly reflect nosep looseness, not the true binders; round 58's s42a list stays the
  better weight. The queue runs on as cheap filler; the A83 fb6 L cert's rows go to its head when it lands. Part 3: Opus
  confirms reading (a) and the defaults; low priority (Long Table parked longer chain keys unless fb6 leaves the face rows
  binding at A83), so it runs when the queue is idle.
- **05:18Z, r59a (8657656/6667656, 10.07% of |w|) dies at ring 13.** Its 748 ring <= 14 windows (05:10-05:16Z) gave 7 kills,
  7 f-names (3 D, 4 C), 1 minimal: f7_..56756_....66. (ring 13, C, X={I3-I4}). Files `loop/k47/r59a_kills*` (d411d8fc).
  Admission head adm59a on main 18eecb9e, regression byte-identical: +3 D, +4 C (7 names), `loop/k59/adm59a/`
  (k3x_D efdd2d6c, k3x_C 808b8aff).

## Round 58 (21 Oct 2026, 00:40Z-): H-A78, do the new binders of Opus's A78 solve die at ring <= 14?

**Pre-registered 00:40Z, before any containment or engine run of this round.** Opus 00:37Z: s42a, l3q + rpatN3 on A78
(b6dc7610, 2,660 D / 1,170 C) minus the 128 ring-merge hold-outs (`loop/opus/P_own_lp/s42a/exname_A78.txt`), one engine,
nosep LOWER VALID 44/421 = 0.104513 (keeppen t = 0.109439); cert `s42a/run_A78/cert_q42aA78L.json` (md5 0c88b25b) with
13 receiverR2 rows. Opus sent the top 10 (140/421 of |w|; `loop/k58/rows58.txt`); the other 3 are asked for. canon_key:
the two 4/421 rows are the exhausted face rows 7766556/6576576 and 7665566/6675676 (round 57). The 8 new rows: 3
non-face (8677656/5566555 24/421, 76765656/66565565 and 76567656/76675555 12/421 each) and 5 face rows (7766556/6567568
and 8665556/7675865 24/421 each; 76555566/66757666, 8665566/6765765 and d11 65655565565/66659665666 12/421 each).
7766556/6567568 differs from the exhausted top A74 row 7766556/6567566 only at s6 (8 for 6).
- **Part 1, containment** (`loop/k55/row55.py`): registry at b6dc7610 (hits by one of the 128 hold-outs marked) and the
  whole 2026 set, on the 10 rows, through u or avoiding it.
- **Part 2, kill sweep** (`loop/k56/q56.py`, ring <= 14, DNW 3) on the 8 new rows by |w|, non-face first within a weight;
  leftovers' ring 15-18 windows to Studio. Kills go to Long Table as admission heads.
- **Hypothesis.** The 3 non-face rows die at ring <= 14; at most 1 of the 5 face rows does. **Kill line:** fewer than 2 of
  the 3 non-face rows die at ring <= 15 (here or at Studio).
- **Guess.** Part 1: no hit (70 percent). Part 2: all 3 non-face rows die at ring <= 14 (55 percent, after round 57's two
  ring-15 rows); no face row dies at ring <= 14 (60 percent), the 8s next to the face notwithstanding.

- **00:41Z, part 1: no hit** (`loop/k58/row58.txt`): none of the 10 rows holds a configuration of the registry at b6dc7610
  (4,410 with RSST) or of the 2026 set, through u or avoiding it, so the 128 hold-outs do not matter here. Guess right.
  Part 2 started 00:40Z (`loop/k58/rows58q.txt`, r58a-h, log `loop/k58/q58.log`).
- **00:42Z, the other 3 rows** (Opus 00:41Z; L cert at b4b974a8, md5 0c88b25b47eba186b06bcbfb3ae309b8 checked): 7666766/6556565
  and 7656766/6556656 (2/421 each, non-face) and d10 6556665566/6565565655 (1/421, face), all new, no registry or 2026 hit
  (row58.txt rerun on 13 rows). They run after r58h as `loop/k58/rows58q2.txt` (r58i-k, log `loop/k58/q58b.log`). The
  13 rows' |w| is 145/421; non-face 52/421, of it 48/421 in r58a, d, e.
- **00:47Z, r58a (8677656/5566555, 24/421) dies at ring 13.** Its 721 ring <= 14 windows (00:40-00:46Z) gave 2 C kills, 2
  f-names, 1 minimal: f7_..65686_..5555. (ring 13, X={I0-I1}). Files `loop/k47/r58a_kills*` (ecd187e1). Admission head
  adm58a on main 41990698 (registry = b6dc7610), regression byte-identical: +2 C (2 names), `loop/k58/adm58a/`.
- **00:51Z, face rows r58b (7766556/6567568) and r58c (8665556/7675865), 24/421 each: no kill at ring <= 14**, as guessed
  (adm58a admitted at bc898a8b). r58b's 697 windows took a minute (shared with the exhausted 7766556/6567566); r58c's
  680 took 3. To-dos `loop/k47/win52_7_7766556_6567568_todo.txt` (486: 24/117/185/160 at ring 15/16/17/18, md5
  9c495355abf87a206dd2281ff96661cc) and `win52_7_8665556_7675865_todo.txt` (584: 200/174/123/87, md5
  b55a18fbe17053cfbb33117bb636e537). Net of every window Studio's job5x already ran (same name, same window):
  `loop/k58/face58_7_7766556_6567568_rest.txt` (350, md5 f10a3dc4b8c63f86921d26316badfbad) and
  `face58_7_8665556_7675865_rest.txt` (566, md5 a378f87bd7518487a658c3cfe6e042a3), 31c62876.
  Long Table 00:51Z: face rows go to the fb6 rule first; only their ring-15 windows run here once the queue is clear.
- **00:59Z, r58d (d8 76765656/66565565, 12/421) dies at ring 12.** Its 1,105 ring <= 14 windows (00:50-00:57Z) gave 9
  kills, 6 f-names (4 D, 2 C), 1 minimal: f8_...65656_...6556. (ring 12, D). Files `loop/k47/r58d_kills*` (10084eee).
  Admission head adm58d on main bc898a8b, regression byte-identical: +4 D, +2 C (6 names), `loop/k58/adm58d/`.
- **01:09Z, r58e (d8 76567656/76675555, 12/421) dies at ring 13.** Its 1,055 ring <= 14 windows (00:57-01:07Z) gave 9
  kills, 5 f-names, all C, 2 minimal: f8_..567656_....555. (ring 13, X={I0-I1}) and f8_.656.656_.55..66. (ring 14,
  X={I0-I1,I0-I3,I1-I7,R9-I8}, one ring vertex). Files `loop/k47/r58e_kills*` (c157eb56). Admission head adm58e on main
  a7ac801e, regression byte-identical: +5 C (5 names), `loop/k58/adm58e/`. All 3 non-face rows of the top 10 are dead
  at ring 12-13 (48/421).
- **01:48Z, two face rows die, one does not** (adm58e admitted at 55732ff4).
  - r58f (d8 76555566/66757666, 12/421, a run of four 5s in the link) dies at ring 11: 1,261 windows (01:08-01:19Z), 51
    kills, 40 f-names, 1 minimal f-name f8_...55556_....576. (ring 11, D).
  - r58g (8665566/6765765, 12/421): no kill at ring <= 14 (723 windows, 01:19-01:21Z). To-do
    `loop/k47/win52_7_8665566_6765765_todo.txt` (713: 224/192/181/116 at ring 15/16/17/18, md5
    2fe1b45802fb043d5e5c6440005acf70); net of Studio's runs `loop/k58/face58_7_8665566_6765765_rest.txt` (676, md5
    0d76f470b537463d7f19601273accc13).
  - r58h (d11 65655565565/66659665666, 12/421) dies at ring 14: 1,848 windows (01:22-01:46Z), 19 kills, 19 f-names, 2
    minimal, both C with u and 8 link vertices only: f11_...55565565_........... (X={I0-I5}) and
    f11_...55655565_........... (X={I0-I3}).
  Files `loop/k47/r58f_kills*`, `r58h_kills*` (898fd2f2). One admission head for both, adm58fh on main 55732ff4,
  regression byte-identical: +30 D, +29 C (59 names, none on main), `loop/k58/adm58fh/`. The face-row guess (none dies
  at ring <= 14) was wrong for 2 of 5: a long 5-run in the link (r58f) or a d11 hub (r58h) is not the d7 face lock.
- **02:37Z, the 3 small rows all die at ring 14** (adm58fh admitted at 5fa0ba6c). r58i (7666766/6556565, 2/421): 808
  windows, 2 kills, 1 f-name f7_..66676_..55.5. (C, X={I0-I1}). r58j (7656766/6556656, 2/421): 914 windows, 1 kill
  f7_5676676_5..5..5 (C, X={I1-I7,I5-I6,R11-I6,R13-I7}, two components with one ring vertex each). r58k (d10 face
  6556665566/6565565655, 1/421): 2,493 windows (01:59-02:36Z), 48 kills, 14 f-names, 5 minimal (2 D, 3 C). Files
  `loop/k47/r58i_kills*`, `r58j_kills*`, `r58k_kills*` (e41819e5). One admission head adm58ik on main 37b5a51a
  (registry = 5fa0ba6c), regression byte-identical: +10 D, +6 C (16 names), `loop/k58/adm58ik/`.
- **02:37Z, verdict on H-A78 at ring <= 14: the hypothesis holds, the kill line is not hit.** All 5 non-face rows die
  at ring 12-14 (r58a, d, e, i, j; 52/421), and 3 of the 6 new face rows too (r58f ring 11, r58h and r58k ring 14;
  25/421). Dead: 77/145 of the 13 rows' |w|. Left: the face rows r58b, r58c, r58g (60/421) and the two exhausted face
  rows (8/421). Guesses: part 1 right; all 3 top non-face rows at ring <= 14 right (55 percent); no face row dying
  wrong (3 of 6 died). Ring-15 check of r58b, r58c, r58g (24 + 188 + 222 windows net of Studio,
  `loop/k47/win58_7_*_r15.txt`, STOP=1 per row) started 02:37Z, as Long Table asked (00:51Z).
- **03:09Z, face rows' ring-15 check: no kill.** r58b 24, r58c 188, r58g 222 windows (02:37-03:07Z), all run, 0 kc D,
  0 kc C accepted by cfast, 0 kc timeouts. Their ring 16-18 windows wait on Opus's fb6 rule (Long Table 02:38Z: fb6
  reaches all three).

## Round 57 (20 Oct 2026, 17:57Z-): H-A74, do the new binders of Opus's A74 solve die at ring <= 14?

**Pre-registered 17:57Z, before any containment or engine run of this round.** Opus 17:54Z (cc Long Table): l3q + rpatN3
(the whole `loop/k51/nl51_kc.txt` as raw patterns) on A74 (main 95ba762d, 2,645 D / 1,156 C), one engine, 20/183 =
0.109290 <= t* <= 1/9, cert `s39o/run_n3_A74/cert_q39n3A74L.json` (md5 9ba47b69). 10 receiverR2 rows, |w| 74/183
(`loop/k57/rows57.txt`). canon_key against every row in this log and in loop/k4*/k5* files:
- 4 face rows were swept before at ring <= 16 with no kill (todo files for Studio exist): 7766556/6567566 (18/183, top),
  7766556/6566576 (= 7655667/6756656 mirrored, 10/183), 7766556/6576576 (6/183), 7665566/6675676 (= 7665566/6765766
  mirrored, 2/183). Together 36/183 (48.6 percent of the |w|). Not rerun here; they are rule-side (round 53).
- 6 rows are new: 7656766/6666555 (15/183), 7666566/6566666 (10/183), d10 6565665656/6556565565 (5/183), 7665566/6775676
  (4/183, a 5-5-5 face row), 7766656/6577556 and 7656766/6656565 (2/183 each). Five of them have no two adjacent 5s in
  the link (non-face).
- **Part 1, containment** (`loop/k55/row55.py`, then `sites55.py`): registry at 95ba762d and the whole 2026 set (verdicts
  from `loop/k53/nl54d_verdicts.txt`), on all 10 rows. Hits that avoid u are listed apart, since rpatN3 only matches
  through u.
- **Part 2, kill sweep** (`loop/k56/q56.py`, ring <= 14, DNW 3) on the 6 new rows by |w|; minkill47; a row with no kill
  sends its ring 15-18 windows to Studio. Kills go to Long Table as admission heads (adm.py on current main).
- **Hypothesis.** The 5 new non-face rows die at ring <= 14, as every non-face row has (rounds 50-56). **Kill line:**
  fewer than 3 of the 5 die at ring <= 14.
- **Guess.** Part 1: no hit through u (rpatN3 holds the whole set); a hit that avoids u in at most 2 rows (60 percent).
  Part 2: all 5 non-face rows die at ring <= 14 (65 percent); the face row 7665566/6775676 does not (75 percent). That
  would kill 34/183 of the 74/183 (45.9 percent of the |w|); the rest is face rows.

- **17:58Z, part 1: no hit at all** (`loop/k57/row57.txt`, 15 s): none of the 10 rows holds a configuration of the
  registry at 95ba762d (4,381 with RSST) or of the 2026 set, through u or avoiding it. So sites55 has nothing to list.
  Guess right on both counts (no hit through u; at most 2 off u). Part 2 started 17:58Z (`loop/k57/rows57q.txt`, r57a-f,
  log `loop/k57/q57.log`).

- **18:14Z, r57a (7656766/6666555, 15/183) dies at ring 14.** Its 978 ring <= 14 windows (17:58-18:12Z) gave 4 kills,
  2 f-names, both minimal and C: f7_..56766_...655. (X={I0-I1,I1-I7,R1-I0}, one ring vertex) and f7_..65676_..66.5.
  (X={I0-I5}); files `loop/k47/r57a_kills*` (3f914cbe). Admission head adm57a on main 989bec15, regression
  byte-identical: +2 C (2 names), `loop/k57/adm57a/`.
- **18:22Z, r57b (7666566/6566666, 10/183) dies at ring 13** (adm57a admitted at 05f86461). Its 879 ring <= 14 windows
  (18:13-18:21Z) gave 3 kills, 3 f-names, all D; the minimal one is f7_..65666_..66.5. (ring 13). Files
  `loop/k47/r57b_kills*` (757968f3). Admission head adm57b on 05f86461, regression byte-identical: +3 D (3 names),
  `loop/k57/adm57b/`.
- **18:53Z, r57c (d10 6565665656/6556565565, 5/183): no kill at ring <= 14** (adm57b admitted at ff24fa64). All 2,120
  ring <= 14 windows ran (18:21-18:52Z). Unlike r56g's alternating wheel, the link has two 6-6 steps, so r56g's ring-15
  kills do not fit. Its 15,783 ring 15-18 windows (2,900 at 15, 5,802 at 16, 5,120 at 17, 1,961 at 18; the whole
  wheel is ring 16) are in `loop/k47/win52_10_6565665656_6556565565_todo.txt` (md5 31a7d98e0053a5206669992f5f856195,
  3b6b0676) for Studio.
- **18:55Z, r57d (face row 7665566/6775676, 4/183): no kill at ring <= 14**, as guessed. Its 753 ring <= 14 windows took 2
  minutes (most replayed from the cache: it shares windows with the 7665566/6765766 family). 463 ring 15-18 windows are
  left (65 at 15, 131 at 16, 178 at 17, 89 at 18; `loop/k47/win52_7_7665566_6775676_todo.txt`, md5
  c3751a267e7101d4b76856e3c41d9edc, 746b73e0). Rule-side with the other face rows for now (Long Table 17:59Z). Long
  Table 18:54Z: Studio runs r57c's ring 15 from the top (job57c); this machine takes it from the bottom once the queue
  ends (`loop/k47/win57c_r15_rev.txt`, STOP=1).
- **18:58Z, r57c dies at ring 15 (Studio job57c, dc7e2902):** 37 two-engine kills, all D (kc + dfast18), in the first 65
  ring-15 windows. minkill47 on Studio's KILL / A_*.out (window file md5 equal to ours): 12 f-names, 3 minimal, all
  ring 15 with 13 interior vertices: f10_..56566565_...5.5.55., f10_..56566565_..5..5.55., f10_..56566565_..55...55.
  (u, 8 link vertices and three 5s of the second ring). Files `loop/k47/r57c_kills*` (a046cdd6). Admission head adm57c on
  main 601538bd, regression byte-identical: +12 D (12 names, none on main), `loop/k57/adm57c/`. The bottom-up run here
  never started (stopped before r57f closed).
- **19:01Z, r57e (7766656/6577556, 2/183, non-face): no kill at ring <= 14** (adm57c admitted at 38a59465). Its 658 ring
  <= 14 windows took 5 minutes (many cached). The second non-face row of this round past ring 14 (with r57c). 1,054
  windows left (274 at 15, 286 at 16, 252 at 17, 242 at 18; `loop/k47/win52_7_7766656_6577556_todo.txt`, md5
  c2a78cfe1dc8899490163c6a8269938b, 10b99675). Studio is on CXInt, so its ring 15-16 windows (`loop/k47/win57e_r1516.txt`,
  560) run here on 3 cores when the queue ends, STOP=1.
- **19:08Z, r57f (7656766/6656565, 2/183) dies at ring 13.** Its 914 ring <= 14 windows (18:59-19:07Z) gave 12 kills, 12
  f-names, 3 minimal, all C at ring 13: f7_...5676_..56.5. (X={I0-I1,I2-I3,R2-I0,R8-I2}, two components with one ring
  vertex each), f7_..65676_..5..5. (X={I0-I5}), f7_..65676_..65.5. (X={I0-I1}). Files `loop/k47/r57f_kills*`
  (2c06b9b0). Admission head adm57f on main 9c9b030f (= 38a59465's registry), regression byte-identical: +12 C (12
  names, none held by the ring-merge guard), `loop/k57/adm57f/`.
- **19:08Z, verdict on H-A74 at ring <= 14: the hypothesis fails in part, the kill line is not hit.** 3 of the 5
  non-face rows die at ring <= 14 (r57a 14, r57b 13, r57f 13; the kill line was fewer than 3). r57c died at ring 15 at
  Studio, and r57e has no kill at ring <= 14 (its ring 15-16 run here from 19:07Z). Dead so far: 32/183 of the 74/183
  (43.2 percent of the |w|); left: the 5 face rows (40/183) and r57e (2/183). Guesses: part 1 right; part 2 wrong on
  all 5 non-face rows dying at ring <= 14 (65 percent), right on the face row 7665566/6775676 not dying (75 percent).
  Lesson: non-face d10 rows with two 6-6 steps and d7 rows with a 7-7 pair can need ring 15.
- **19:10Z, the face rows at Studio.** Studio's job52 already ran every ring 16-18 to-do window of 7766556/6567566 (352,
  finals committed on main 19:10Z), 7766556/6576576 (414) and 7665566/6765766 (225), and 213 of 7655667/6756656's 243,
  all with 0 two-engine kills. Left: 30 ring-18 windows of 7655667/6756656 and 319 of r57d (`loop/k57/face57_7_*_rest.txt`,
  36e47b3c). Long Table's kill line for job57face is met, so it is not running; the face rows stay rule-side.
  Correction 19:11Z: 7766556/6567566's finals reached main only at b3c6bddf; all 352 of its windows had run (343 kc
  neither, 9 ring-18 kc timeouts), so its rest file is void. Studio runs r57d (rest file, all rings) and r57e rings 17-18.
- **21:30Z, r57e ring 15-16: no kill.** All 560 windows (274 at 15, 286 at 16; 19:07-21:28Z, 3 cores) ran with 0 two-engine
  kills and 0 kc timeouts. Its rings 17-18 are at Studio.

## Round 56 (20 Oct 2026, 08:43Z-): H-RPN, do the 13 binders of Opus's rpatN solve die, to the 2026 set or to our windows?

**Pre-registered 08:43Z, before any containment or engine run of this round.** Long Table 08:41Z: with rpatN (round 55's 35
configurations fed in through u; Opus 4da3d055, `loop/opus/P_own_lp/s39o/run_n/cert_q39nL.json`, 636/5071 <= t* <=
0.125956 on A67, one engine) the binders move to d8 and d10 rows. 13 receiverR2 rows, |w| 0.234865, none seen before
(canon_key against every row in this log and in loop/k4*/k5* row files): d10 6556565565/6566669666 (23.5 percent),
then 75566556/86666965, 85565856/65666565, 86567565/55568555, d7 8586566/6555565 and d10 6556565565/6566668666 (11.2
percent each), and 7 smaller (`loop/k56/rows56.txt`).
- **Part 1, containment** (`loop/k55/row55.py`, then `sites55.py`): A67's registry and the whole 2026 set, each hit marked
  with its round 54d verdict (rings 6-14 all D; ring 15 under way, now on one worker). A hit by a configuration not yet
  run is run ahead on our engines. Hits that avoid u are listed apart, since rpatN only matches through u.
- **Part 2, kill sweep** (round 54's queue, `loop/k47/q54.py` logic as `loop/k56/q56.py`): win45 windows in each row's
  1.5-ball, drive45 (kc -C -t 600, dfast, cfast --fixed) on ring <= 14 only, NW 2 beside round 54d, rows by |w|;
  minkill47 on the kills; a row with no kill at ring <= 14 sends its ring 15-18 windows to Studio. Kills go to Long
  Table as admissions (twoeng-ready files).
- **Hypothesis.** Most of the 13 die at ring <= 14: every non-face row so far died at ring 12-14 (rounds 50-54), and
  none of these has the 5-5-5 face shape. **Kill line:** fewer than half of the |w| dies at ring <= 14.
- **Guess.** Part 1 finds no hit through u (rpatN already took those), and at most 2 rows with a hit by a configuration
  confirmed after rpatN or one that avoids u (60 percent). Part 2: at least 10 of the 13 die at ring <= 14 (65
  percent); the d10 rows die at ring 12-13, like the two d10 binders of round 50.

- **08:44Z, part 1: 5 of the 13 rows hold a 2026 configuration, all through u** (`loop/k56/row56.txt`,
  `loop/k56/sites56.txt`): 86567565/55568555 and 85658656/65555555 (nl1683_r12, nl7047_r13, nl7089_r13), d7
  8586566/6555565 (nl5571_r12), 85658655/65555666 (nl5226_r13, nl7047_r13), 85555856/65856665 (nl2606_r13). These are 6
  configurations, all D on both engines (`loop/k56/row56_hits_kc.txt`), none among round 55's 35, and they carry 32.5
  percent of the |w| (0.076251 of 0.234865). No registry hit, and no hit that avoids u. The guess (no hit through u)
  was wrong: rpatN took only the 35, so the next rows are hit by others. The confirmed list so far (6,053 D, rings
  6-15 in part) is in `loop/k56/nl54d_confirmed_D_kc.txt` for a full rpatN intake. The 8 rows left (67.5 percent of the
  |w|) go to part 2.

- **09:46Z, r56a (d10 6556565565/6566669666, 23.5 percent) dies at ring 13-14.** Its 2,182 ring <= 14 windows
  (08:45-09:46Z, NW 2) gave 86 two-engine kills: 47 D and 35 C at ring 14, 2 C and 2 D at ring 13. These reduce to 43
  f-names and 6 minimal: f10_...5565655_........5. (ring 13, C), f10_...5565655_.....66... (14, D), and four C at ring
  14. Twoeng-ready files are `loop/k47/r56a_kills*` (f282e4bf), sent to Long Table 09:47Z.
- Round 54d's ring 15: Studio took the remainder as job54e, in reverse order from nl8192 (Long Table agreed 08:46Z).
  Its batch 1 (ff9c1f83) gave 404 lines, all D, and its nl54d is at 450 of 610 at ring 16-18, all D. This machine's
  one worker goes up from nl1283 and stops where the two meet.

- **09:48Z, admission head adm56a** (`loop/k54/adm.py` on main 6f74ffd2, regression byte-identical: +25 D, +18 C,
  43 names); Long Table admitted it at cd2e2f2f (2,580 D / 1,115 C).
- **10:06Z, r56b (d8 75566556/86666965, 11.2 percent) dies at ring 12-14.** Its 1,146 ring <= 14 windows (09:46-10:06Z)
  gave 27 kills, 3 minimal: f8_...55665_...66... (ring 12, C), f8_55665567_......5. (13, D), f8_...65576_...66.5.
  (14, C); files `loop/k47/r56b_kills*` (44894a8d). Admission head adm56b on cd2e2f2f, regression byte-identical:
  +19 D, +8 C (27 names), `loop/k56/adm56b/` (10:07Z).

- **10:42Z, r56c (d8 85565856/65666565, 11.2 percent) dies at ring 13-14** (adm56b admitted at 5304f959). Its 1,473
  ring <= 14 windows (10:06-10:42Z) gave 30 kills, 4 minimal, all C: f8_...55865_...565.. and f8_.5565.56_.....56.
  (ring 13), f8_...56585_....665. and f8_..565586_....565. (14); files `loop/k47/r56c_kills*` (f6f1fd10). Admission
  head adm56c on 5304f959, regression byte-identical: +11 D, +19 C (30 names), `loop/k56/adm56c/` (10:43Z).

- **10:45Z, r56d (d10 6556565565/6566668666, 11.2 percent) dies to r56a's kills** (adm56c admitted at dbb8509c). It
  differs from r56a only at s7 (8 for 9), so the window cache answered it in 2 minutes. Its kill files are
  byte-identical to r56a's: the same 86 kills, 43 names and 6 minimal f-names, all already on main since cd2e2f2f. No
  admission is needed; the rpatN cert kept it only because it predates adm56a (10:46Z).

- **11:30Z, r56e (d10 6566565665/6655556556, 3.9 percent) dies at ring 14.** Its 2,033 ring <= 14 windows
  (10:45-11:30Z) gave 18 kills, 5 minimal (4 C, 1 D, all ring 14: f10_...5656656_.......55.,
  f10_...5665656_.....5556., _.....6555., _....5..55. (D), _...5...55.); files `loop/k47/r56e_kills*` (a5a70479).
  Admission head adm56e on dbb8509c, regression byte-identical: +8 D, +10 C (18 names), `loop/k56/adm56e/` (11:31Z).

- **11:59Z, r56f (d8 85586565/66655556, 3.4 percent) dies at ring 14** (adm56e admitted at 387326d2). Its 1,464 ring
  <= 14 windows (11:30-11:59Z) gave 10 D kills, 2 minimal: f8_...55856_...6665. and f8_...55865_...6655.; files
  `loop/k47/r56f_kills*` (1cb4c561). Admission head adm56f on 387326d2, regression byte-identical: +10 D (10 names),
  `loop/k56/adm56f/` (12:00Z).

- **12:05Z, r56g (d10 6565656565/6666666666, 1.9 percent): no kill at ring <= 14** (adm56f admitted at eb3813b4). All
  1,470 ring <= 14 windows were run (11:59-12:05Z; many replayed from the cache). The row is the alternating 6-5 d10
  wheel with every s = 6. Its 15,292 ring 15-18 windows (1,547 at 15, 3,120 at 16, 4,825 at 17, 5,800 at 18) are in
  `loop/k47/win52_10_6565656565_6666666666_todo.txt` (md5 00668f512330fe42bccc1886cf21f399, 3838695a) for Studio (12:07Z).

- **12:37Z, r56h (d10 6566565665/6655566555, 1.3 percent) dies at ring 14.** Its 2,150 ring <= 14 windows
  (12:06-12:37Z) gave 47 kills, 25 f-names and 4 minimal. 3 of the minimal ones are r56e's (already on main); the new
  one is f10_.5656.5656_..55...55. (D). Files `loop/k47/r56h_kills*` (b2b9c623). Admission head adm56h on eb3813b4,
  regression byte-identical: 7 of the 25 names already on main, +16 D, +2 C, `loop/k56/adm56h/`.
- **12:38Z, verdict on H-RPN: the hypothesis holds, the kill line is not hit.** 12 of the 13 binders die. 5 die to 6
  configurations of the 2026 set (32.5 percent of the |w|), 6 to ring 12-14 windows (r56a, b, c, e, f, h) and 1 to
  r56a's kills (r56d). Together that is 98.1 percent of the |w|. Only r56g (1.9 percent, the alternating 6-5 d10 wheel)
  has no kill at ring <= 14; its ring 15-18 to-do is held until Opus's A72 list shows whether it still binds. Guesses:
  part 1 was wrong (5 rows, not <= 2), part 2 right (at least 10 of 13 die). The d10 rows died at ring 13-14 rather
  than 12-13.
- **14:16Z, r56g dies at ring 15 (Studio job52d10 batch 1, 1a340174, ring 15 lines 1-1,066).** 16 two-engine kills, 3
  f-names (`loop/k47/minkill47.py` on Studio's KILL / A_*.out; window file md5 equal to ours): the whole wheel
  f10_5656565656_.......... (ring 15, D, kc + dfast18) and two C names with interior-only X, f10_.565656565_..........
  (u and 9 of the 10 link vertices) and f10_...5656565_......66.. (both X={I0-I3}). The first C sits inside the row's
  link alone, so the row dies whatever its second ring holds. Re-run here (kc -C, dfast, cfast --fixed): same verdicts,
  same class counts and X as Studio. Files `loop/k47/r56g_kills*` (311068f8). Admission head adm56g on main 3e801c10,
  regression byte-identical: +1 D, +2 C (3 names, none already on main), `loop/k56/adm56g/`. With it all 13 rpatN
  binders are dead. Studio's remaining ring 15-16 windows of this row can only add redundant kills.

## Round 55 (20 Oct 2026, 06:23Z-): H-NLROW, does a 2026 configuration sit inside a binder of the A67 l3q cert?

**Pre-registered 06:23Z, before any containment run of this round.** Opus 06:20Z (sent at Long Table's request): the
l3q-only cert on registry A67 (main 2c97e14d, 2,555 D / 1,097 C; 0.127123 <= t* <= 0.128958, one engine) has 45
receiverR2 binders (Opus 93b85890, `loop/opus/P_own_lp/s33z/run_A67/cert_q66L.json`); 8666655/5677657 no longer binds
(slack 0.078). Round 54c's ring-8 surprise says the 2026 set holds small D configurations that RSST's 633 lacks, and
Long Table means to feed the confirmed set into the LP as raw patterns (round 54d). This round previews that: which
binders the set kills outright.
- **Tool** `loop/k55/row55.py`: for each binder row, cen54's frame with no slots (u, the link and the second ring,
  exact vertices only, letter 9 never exact); containment (round 42/44 matcher) of A67's registry (as fam51: RSST 582
  plus the k3x names) and of the 2026 set. A hit means the configuration sits wholly inside the row's 1.5-ball. Each
  2026 hit is marked with its round 54d verdict if it has one. One core, while round 54d runs on two.
- **Bar.** A67's registry has no hit in any binder (the LP would not use a row that holds a registry configuration).
- **Hypothesis / kill line.** At least one of the 45 binders holds a 2026 configuration. Kill line: none does, so the
  set can only reach these rows one ring out, through the privates.
- **Guess.** Kill line hit (70 percent): round 51 found no row hits in three face rows, and the binders are rows the
  LP keeps exactly because nothing small sits inside them.

- **06:24Z, run** (`loop/k55/row55.py`, 37 s; rows `loop/k55/rows45_A67.txt`; result `loop/k55/row55_A67.txt`). 27 of
  the 45 binders hold a 2026 configuration wholly inside their 1.5-ball: 35 distinct configurations at rings 8-15
  (`loop/k55/row55_hits_kc.txt`). All 35 are D on kc -C and dfast: 31 from round 54d's run, plus 4 (nl4516_r15,
  nl7091_r14, nl7546_r14, nl8104_r14) run ahead at 06:25Z. The 27 rows carry 0.198798 of the 0.372122 receiver |w|
  (53.4 percent). Not hit: the top binder 7766556/6576576 (19 percent), its siblings 7766556/6566576 and
  7766556/6567566, 7766555/6566959, 7665567/5765765, 9656775/5556655, 7665566/6675676, and 11 others. On the d7 rows
  the configuration uses u itself. For example, 7576565/7557766 holds nl0278_r11 = u, w1..w4, s1, s2 (degrees 7, 5,
  7, 6, 5, 5, 5; `loop/k55/row55_emb_samples.txt`).
- **The bar failed on one row.** A67's registry hits the d12 binder 555555555555/757575757575 seven times
  (f7_.....55_....575, f10_........55_.......575, f11_...; for instance a 7 at s0 with its fives w0, w1, s1, s11).
  None of these configurations uses u. Either the LP's admissibility check only looks at configurations through u,
  or the matchers differ: a question for Opus. The other 44 rows have no registry hit.
- **06:28Z, verdict on H-NLROW: the hypothesis holds (27 of 45), the kill line is not hit; the guess (70 percent on the
  kill line) was wrong.** RSST's 633 and our k3x names miss small configurations that the 2026 set has, around u and
  its link. Once Studio's rpatD route takes in the two-engine list (round 54d), these 27 rows should leave the LP,
  provided its pattern match looks at the whole 1.5-ball.

- **06:31Z, hit sites** (Opus 06:30Z: their admissibility check, and rpatD, embed a configuration only with a vertex on u;
  off-centre matching may come later as a flag). `loop/k55/sites55.py` lists every embedding with its vertex map
  (`loop/k55/sites55_rows45_A67.txt`). All 27 rows have a hit that runs through u, so matching through u is enough
  for all of them. The d12 row's 6 registry configurations and nl0040_r8 avoid u, but nl8199_r13 (a 12 with ten
  fives) runs through u there. Every hit uses only exact vertices of the row's 1.5-ball (Opus's strict condition).

## Round 54d (20 Oct 2026, 04:37Z-): H-NL95, do our two engines confirm the published 2026 set?

**Pre-registered 04:37Z, before any engine run of this round.** Long Table 04:35Z (in place of round 53b, stopped
04:36Z): run all 8,200 configurations of the 2026 set (`loop/k51/nl51_kc.txt`, md5 b9bc6e8bd9b86cf3a95873c05d9e7c34)
through our engines for a two-engine list. The confirmed ones enter the LP as raw patterns by Studio's rpatD route,
the way the RSST D patterns did (no twoeng guard change).
- **Tool** `loop/k53/nl54e.py` (cen53's verdict rule: kc -C -s 60 -t 600; a kc D re-run on dfast, ring <= 16, or
  dfast18; a kc C on cfast --fixed with kc's X; cache and outputs `loop/k53/N54_*`, so the 8 of round 54c replay). NW 3,
  smaller rings first. Rings 6-15 here (7,590 configurations). Rings 16-18 (610, `loop/k53/nl54d_r1618.txt`, md5
  51e894e4440bcf3b8c03018cc9537ccf) go to Studio if the ring-15 rate puts them past about 6 hours here (ring 14 took
  about 11 core-seconds each in round 54c, mostly dfast).
- **Bar.** The paper says every configuration in the set is D-reducible.
- **Hypothesis / kill line.** At least 95 percent come out D or C on both engines. Under 90 percent: stop and report the
  mismatches (a contract difference or a bug on one side).
- **Guess.** Every configuration at ring <= 15 comes out D on both (90 percent); no MISMATCH-D or CFAST-REJECTS at all
  (85 percent); any shortfall is kc timeouts at ring 16-18.

- **14:04Z, done: all 8,200 configurations are D on both engines** (`loop/k53/imp54d.py`, list `loop/k53/nl54d_verdicts.txt`,
  md5 952575cace5f1137365bfcff8e1fcd84). This machine ran rings 6-14 (5,895) and part of ring 15 (`N54_res.txt`). Studio
  ran rings 16-18 (job54d, 610, kc + dfast18) and the ring-15 remainder (job54e, 1,535), both on main at da31feea, with
  input md5s equal to ours. Every Studio name has kc D=true, dfast/dfast18 D=true and a KILL line D. 494 configurations
  ran on both machines with 0 disagreements. By ring: 1, 1, 5, 15, 60, 210, 779, 2,025, 2,799, 1,695, 526, 69, 15 (rings
  6-18). No C, no MISMATCH-D, no CFAST-REJECTS and no timeout.
- **Verdict on H-NL95: the hypothesis holds (100 percent, bar 95), the kill line is not hit. Guesses: right on ring <= 15
  all D (90 percent) and on no mismatch (85 percent); wrong that any shortfall would be timeouts at ring 16-18, since
  there was none.** The confirmed list is `loop/k51/nl51_kc.txt` itself (md5 b9bc6e8bd9b86cf3a95873c05d9e7c34).
- **14:08Z, 8,202 vs 8,200 (Long Table 14:05Z): the two missing ones are the one-vertex configurations, a vertex of degree 3
  and a vertex of degree 4** (ring 3 and ring 4). The repo README says the directory holds the set "except for a vertex
  of degree 3, 4"; our base (minimum degree 5) already excludes both. Not a parse drop: the files run D0000-D8199 with
  no gap and all 8,200 parse. Not duplicates: `loop/k53/dup54.py` gives 8,200 distinct canonical forms, with or without
  reflections (self-test: 21 relabelled and mirrored copies all match their originals).

## Round 54c (20 Oct 2026, 04:02Z-): H-NL54, does the published 2026 set kill any survivor of 8666655/5677657?

**Pre-registered 04:02Z, before any containment or engine run of this round.** Coordinator 03:56Z, from the user's
literature points (point 1): search the public 2026 set (Inoue, Kawarabayashi, Miyashita, Mohar, Thomassen, Thorup,
github.com/near-linear-4ct/reducible-configurations, MIT, HEAD c2ce7a96; 8,200 .conf files, already converted to kc
lines in round 51 as `loop/k51/nl51_kc.txt`) for every configuration that sits inside the survivors of the last d7
face binder, and list its 7-next-to-7 and triangle-of-7s shapes with ring size. The set is a map only: a
configuration counts here only after kc -C and dfast/dfast18 (D) or cfast --fixed (C) pass it on our side, the same
rule as round 44's RSST set, and anything admitted is proved by our engines and Lean.
- **Tool** `loop/k53/cen54.py` with a new XREG option: the 2026 set is added to the registry for containment (same
  matcher, letters 5..8 only, 9 never exact), each part reports its coverage with and without the 2026 set and every
  minimal requirement that only a 2026 configuration supplies, and XOUT writes those configurations' names. Same frame
  and settings as round 54b part 2 (14 slots, FOCUS 3,6, TORDER joint,single,6,3, RLOC 14, every window cached).
  Then every 2026 configuration that supplies a requirement goes through kc -C -t 600, dfast (ring <= 16) or dfast18,
  and cfast --fixed on a kc C (cen53's verdict rule, own cache `N54_*`), NW 3; the census is rerun with only the
  confirmed ones. Shapes: `loop/k53/nl54c.py` counts the configurations with a 7-7 edge, a 7-7-7 triangle and a
  7-5-5/5-5-5 kite (a 7 next to a face of three 5s), by ring size.
- **Bars.** Round 54b's census: 86.68 percent of 6,103,515,625 fillings, part p41 >= 6 / apex 6-9 at 79.19 percent,
  every filling with all free slots >= 7 uncovered, 0 of 25 children dead.
- **Kill line.** No confirmed 2026 configuration covers a filling of the big part with all free slots >= 7: the set
  does not reach this binder inside the frame, and the row stays on the rule side.
- **Guess.** Kill line hit (80 percent). Round 51 found the set adds nothing to the face rows beyond our registry; the
  all->= 7 box puts 7s and 8s in every free slot, and the set's 7-clusters need rings 14-18, which the frame's 3-ball
  may not hold. Coverage of the whole row rises by under 1 point (70 percent).

- **04:03-04:31Z, census with the 2026 set** (`loop/k53/cen54.py` XREG, log `loop/k53/cen54c_7_8666655_5677657.txt`;
  the engine windows replay round 54b exactly from the cache). Configurations of the set that fit each part: 168, 158,
  221 and 176. Eight supply a requirement that nothing of ours covers (`loop/k53/nl54c_need.txt`, md5
  633fefa2d39feaba2b31f7659071f63c): nl0004_r8, and seven at ring 14 (nl2192, nl2974, nl2975, nl2976, nl2982, nl6210,
  nl6741). All eight are D on kc -C and dfast (`loop/k53/nl54e.py`, `N54_res.txt`, 04:32Z), so they count.
  - Part p41 = 5, apex 6-9: nl0004_r8 (a ring-8 5-6-5-6-5: w4 = 6 and s4 = 6 with their common fives w5 and p41,
    plus s5) sits inside the fixed vertices, so it closes the part outright; round 54b had left 20,544 fillings there.
    Our windows never tried it because round 54b only ran windows at the 7s.
  - Part p41 >= 6, apex 6-9: 79.19 to 80.14 percent (+36,996,288). Of that, nl0004_r8 again gives +27,331,200 (with
    tp41/s4 = 5 and apex 6), nl6741_r14 +7,908,864 (p01 = 6, p02 = 5, p03 = 6), and the other five +2.4 million between
    them, all with a five in some slot.
  - Fillings with every free slot >= 7: 4,782,969, uncovered 4,782,969 with or without the set. With every free slot
    >= 6: 198,180,864 uncovered, with or without it.
  - Whole row 86.68 to 87.29 percent; children 0 of 25 dead (84.24-94.20 to 85.00-94.31 percent).
- **04:33Z, the same box one step wider** (`loop/k53/box54c.py`, containment only): add the ring-3 neighbours of s0,
  s1 and s2 (6 more slots, 20 in all) and take the part with p11, p21, p31, p41 and the apex at 6-9. Box: round 54b's
  14 slots at 7-9, the 6 new ones at 5-9 (74,733,890,625 fillings). The registry covers 3.36 percent, and every one of
  its 11 box hits needs fives at the new slots on the far side (beside s1 and s2) plus p11 or p21 = 7. The 2026 set
  covers 1.45 percent, all of it inside the registry's 3.36 (both together: 3.3636 percent, the same). Nothing of
  either touches the lock at s3 and s6.
- **Shapes** (`loop/k53/nl54c.py`, list `loop/k53/nl54c_shapes.txt`): of the 8,200 configurations, 6,882 have a 7,
  3,795 a 7-7 edge (rings 10-18, most at 14-15), 686 a 7-7-7 triangle (rings 12-18), 486 a cluster of four or more 7s
  (rings 13-18), and 1,141 a 7 next to a 5-5-5 face (642 of them also with a 7-7 edge).
- **04:34Z, verdict on H-NL54: the kill line is hit.** No configuration of the 2026 set covers a filling of the big part
  with all free slots >= 7, and one ring wider it adds nothing the registry does not already have. The set's
  7-clusters do not reach the lock at s3 and s6 inside this frame; the row stays on the rule side. Guess (kill line
  hit, 80 percent): right; coverage up by under a point (70 percent): right, +0.61. Surprise: a ring-8 configuration
  missing from our registry closes the p41 = 5 part, because round 54b had restricted the windows to the 7s.

## Round 54b (20 Oct 2026, 00:52Z-): H-S54, split and kill on the two d7 face binders left in the 11/75 cert

**Pre-registered 00:52Z, before any engine window of this round.** Long Table 00:51Z: every non-face binder of Opus's
11/75 cert is dead (round 54); the two left are d7 face rows, 8556856/7565666 (face w1 w2 s1) and 8666655/5677657 (face
w5 w6 s5), both -1/75. Studio is offered 8666655/5677657 at ring 15-18; explore runs round 53's split and kill on both
once 8556856/7565666's ring <= 14 sweep closes (stopped there if it has no kill; its ring 15-18 to-do goes to Studio).
- **Tool** `loop/k53/cen53.py` unchanged (slots: the privates of each exact non-5 link vertex and the ring-3 vertices
  beside the face, letters 5..9, 9 = >= 9; apex parts; registry containment, then engine windows with ORDER=fives, 1-2
  slots at 5..8, ring <= 16, kc -C -t 600 / dfast / cfast --fixed; exact coverage of the fillings). Registry: main
  3d6c4f9a's k3x (2,552 D / 1,097 C, the copy checked for r54p) plus round 44's RSST set. NW 3, 7,000 s cap per row,
  8556856/7565666 first.
- **Hypothesis (Long Table):** as for round 53's binder, >= 75% of each row's one-ring-out extensions die. **Kill line:**
  under 50%: the row is the rule side's (z6 or the stacked solve must pay it).
- **Guess:** neither row reaches 75% (55%); the apex = 5 part dies in both (each has a 6 beside the face on the apex
  side: s2 = 6, s4 = 6), 80%.

- **01:01Z, 8556856/7565666: every extension covered by the registry, no engine window needed** (`loop/k53/cen53_7_8556856_7565666.txt`).
  The row itself holds a registry configuration (f7_..56856_...566., inside the fixed vertices), as round 54's r54o
  sweep found at ring 14; the apex = 5 part also holds f10/f11/f7 ones. cen53 then crashed on its total line (a
  division by zero when every part is covered by the registry); fixed in cen54.
- **01:18Z, 8666655/5677657 stopped at 82.28 percent (Long Table 01:14Z redirect).** Slots p01 p02 p03 p11 p21 p31 p41,
  apex ts4/s5/s6, ts6, tp01/s6, tp41/s4 (11, 48,828,125 fillings). Apex = 5: all covered by the registry. Apex 6-9:
  registry 72.62 percent, plus 16 two-engine kills at ring 12-15 (7 D, 9 C; `loop/k53/cen53_7_8666655_5677657.txt`,
  verdicts in `G_res.txt`) -> 77.85 percent of that part, 82.28 percent of the row, when it was stopped with most of its
  45,800 windows unrun.
- **01:37Z, re-registered as round 54b part 2: s3/s6 splits on 8666655/5677657** (Long Table 01:14Z; the drawing thread
  runs the same splits on its own engine). Long Table's lock map puts most run-outs on s3 (46-70 percent) and s6 (21-46
  percent), the two 7s of ring 2; each has one private ring-3 neighbour, ts3 and ts6 (next to that s alone).
  - **Tool** `loop/k53/cen54.py` (cen53 plus J3S, FOCUS, the child table, a shared cap, and the total-line fix):
    J3S=3 adds s3's three ring-3 neighbours tp31/s3, ts3, tp41/s3 to the slots (14 slots, 6,103,515,625 fillings;
    p41 = 5 now changes the induced structure, so 4 parts). Engine windows: verdicts already cached first (cen53's 16
    kills replay for free), then joint windows (a ring-3 slot next to s3 and one next to s6 other than the apex, both
    inside), then single windows (ts3 or ts6 inside); no other window. 1-2 slots per window at 5..8, ring <= 16,
    ORDER=fives, kc -C -t 600 / dfast / cfast --fixed, registry main 3d6c4f9a (`adm54p`) plus round 44's RSST set.
    NW 3, 7,200 s cap shared over the parts by their uncovered fillings.
  - **Registry alone (dry run, cap 0, 01:21-01:35Z, `loop/k53/cen54dry_7_8666655_5677657.txt`):** 80.69 percent of
    the 14-slot fillings. The two apex = 5 parts are covered; p41 = 5 with apex 6-9 is at 78.25 percent; p41 >= 6
    with apex 6-9 is at 75.27 percent. Per child (ts6, ts3) the registry covers 76.81-91.60 percent, so no child is
    dead yet. A KMAX 3 dry run was stopped after 10 min of window enumeration, so the run is at KMAX 2.
  - **Children:** the 25 letter pairs (ts6, ts3) in 5..9. A child dies when every extension of it (the other 12
    slots) is covered. Fillings coverage is reported too.
  - **Hypothesis (Long Table):** the split children die at ring <= 16. **Kill line:** fewer than 50 percent of them die
    (13 or fewer of 25), and then the row goes to the rule side.
  - **Guess:** the kill line is hit, 85 percent: no child dies outright (75 percent), and fillings coverage ends at
    84-88 percent. The drawing thread's 19 single-slot windows at ring 13-16 had no D (relayed 01:25Z), and a child
    with ts3 or ts6 = 9 (degree >= 9) can never have that slot inside a window.

- **01:45Z, cen54 relaunched with Studio taking ring 15-16 (no engine verdict of the 01:38Z start counts; it was stopped
  at 01:41Z and again at 01:44Z while enumerating, its log is in `loop/k53/cen54run1_7_8666655_5677657.txt`).** Changes
  before any new verdict: (1) a third window tier from the drawing thread (01:43Z, kc surgery on the ring-12 face
  window: D exactly when s3's ring contacts drop to <= 3), "two at one 7": s3 or s6 inside with two of its slot
  neighbours (p31, p41 and the three ring-3 ones for s3; p01, the apex, ts6, tp01/s6 for s6). Run order: cached,
  joint, two at one 7, single. (2) Long Table 01:14Z: Studio has ring 15-16 slots, so RLOC=14 runs only cached windows
  and windows at ring <= 14 here, and DUMP writes the uncached ring 15-16 windows of the three tiers, in run order and
  deduplicated by kc line, to `loop/k53/win54s_7_8666655_5677657_r1516.txt` for Studio. Their verdicts come back into
  the census cache, and a rerun then counts every window exactly. Hypothesis, kill line and guess unchanged.

- **01:52Z, run order back to the pre-registered one (Long Table 01:48Z).** The exposure lemma failed on real windows (the
  drawing thread, 01:47Z: with two of s3's ring-3 neighbours inside the window is still not D at ring 13-16, 7 of 22
  done). cen54 now takes the order as TORDER; the run (restarted 01:51Z, before any new verdict) uses
  `joint,single,6,3`: the pre-registered joint and single windows first, then the two-at-one-7 windows (s6, then s3).
  The 01:48Z start used `joint,6,3,single` and was stopped while enumerating.

- **02:05Z, part p41 = 5, apex 6-9 closed here: 100.00 percent (20,544 of 976,562,500 uncovered).** Registry 78.25
  percent plus 75 two-engine kills (4 D, 71 C, rings 11-15; 161 windows run, 6,876 skipped as covered). 24 of the 25
  children (ts6, ts3) are dead; ts6 = 9, ts3 = 9 is at 99.95 percent. Every uncovered filling has p31, ts6, tp31/s3,
  ts3 and tp41/s3 all >= 9 (s3 with every outer contact of degree >= 9, which no window can hold). Many kills are
  joint windows, e.g. g7_-....655_....657_......5..6..5. (C, ring 13). The two apex = 5 parts are registry-covered.
- **02:41Z, Studio batch 1 (main 315a6285, `out/job54s/`): the 336 joint windows at ring 15-16 are done, 218 two-engine C
  kills, 0 D, 0 cfast rejections.** `loop/k53/imp54.py` reads Studio's drive45-format files and writes cen53-rule
  verdicts to `loop/k53/S_res.txt` (346 windows with both engines in, 223 C and 123 none; kills equal Studio's KILL).
  They go into the census cache once the running census closes; a rerun then counts them exactly.

- **02:51Z, every ring <= 14 split window run here: 86.68 percent of the 14-slot fillings, 0 of 25 children dead.**
  The big part, p41 >= 6 with apex 6-9 (3,906,250,000 fillings), went from registry 75.27 percent to 79.19 percent:
  2,836 windows run, 857 skipped as covered, 7 kills (3 of them ring-15 replays from cen53), and its 72 joint windows
  gave none. Per child in that part: ts6 = 5 is at 89.8-90.9 percent; ts6 >= 6 is at 75.4-79.9 percent; ts3 hardly
  matters. Every filling with all free slots >= 7 is uncovered. The p41 = 5 part dies through the extra five beside
  s3 and s4; with p41 >= 6 the s3/s6 windows at ring <= 14 do almost nothing. Log `loop/k53/cen54_7_8666655_5677657.txt`.
- **02:52Z, census rerun with Studio's batch 1 merged into G_res.txt** (`loop/k53/merge54.py`, 346 lines), same settings:
  ring <= 14 and Studio's ring 15-16 verdicts replay from the cache.

- **03:41Z, rerun with Studio's batch 1: no change, 86.68 percent and 0 of 25 children dead** (the first rerun, 02:52Z,
  was cut by a container restart; rerun 03:15-03:41Z, `cen54r` in the k53 log). All 223 of Studio's ring 15-16 C kills
  are p41 = 5 windows, in the part the ring <= 14 kills had already closed; the 72 joint windows that can reach the
  p41 >= 6 part gave nothing at any ring.
- **03:42Z, verdict on H-S54 part 2: the kill line is hit.** 0 of the 25 split children (ts6, ts3) die: every ring <= 14
  window of the three tiers was run here, and every joint window at ring 15-16 at Studio. The children stand at
  84.24-94.20 percent over all parts. They live in the part p41 >= 6, apex 6-9, which is at 79.19 percent. Its uncovered
  fillings include every filling with all free slots >= 7, and none with p01 = 5, p21 = 5 or p11 <= 6. Still unrun:
  9,049 single and two-at-one-7 windows at ring 15-16 that can reach that part (trimmed Studio file
  `loop/k53/win54t_7_8666655_5677657_r1516.txt`, md5 bccd67a0f6c1aaa0d2fb3449454d8e4a, d8ab6e2b; the 10,552 p41 = 5
  lines left in the full file can change nothing). For a child to die, those windows would have to cover its
  all->= 7 fillings, which no window at ring <= 14 touched. So the call is the rule side for 8666655/5677657.
  Guess (kill line hit, 85 percent): right, including "no child dies outright". The fillings coverage guess (84-88
  percent) was right too, at 86.68 percent. The surprise was the p41 = 5 part: a five at p41 beside s3 and s4 opens
  joint s3+s6 windows that die at ring 11-14.

- **03:46Z, Studio's job 54s stopped (Long Table 03:43Z; main c21a5dd1): lines 1-777 done, 577 two-engine kills (523 C,
  54 D).** 573 are p41 = 5 windows (the closed part). The other 4 (g7_u86...55_5...657_5.......5..... and three
  siblings, C) all have p01 = 5 and ts6 = 5, inside the p01 = 5 fillings the census already covered, so the census
  stays at 86.68 percent with 0 of 25 children dead. All 777 verdicts are in `S_res.txt` and G_res.txt (the 5 windows
  cut mid-confirmation, `out/job54s/STOPPED.txt`, have none). The trimmed 54t file waits at Studio as idle filler.

## Round 54 (19 Oct 2026, 21:56Z-): H-L3Q, do the receiver binders of Opus's l3q solve die at ring <= 16?

**Pre-registered 21:56Z, before any engine window of this round.** Long Table 21:53Z: Opus's l3q rule solve (11f050ea, one
engine, provisional, on registry 7360eb92) pays the face binder 7665566/6675676 by rule and reaches upper 0.147857 /
lower 47/320. Its receiver binders (lower cert, `opus/P_own_lp/s28q/s28A60L.log`) are what kills must move now, ahead
of round 53b's 87 tight patterns (which matter less once the face is paid by the rule). Queue `loop/k47/rows54.txt`,
by dual: d10 6565656565/6556666666 (0.078), d7 8658656/6665555 (0.025), seven rows at 0.0125 (d8 76656656/56655565,
85656765/56665565, 85566556/66666855, 85556655/66866666, 76665656/56566655, d7 8568656/6655555; and 86555665/56586665,
not queued: it died at Studio as Job 52 row 1, admitted in 3cfd7f18, after the solve's 7360eb92), d7 8658656/6665556
and d8 76656566/56655565 (0.006), and d8 75666556/66666565 (0.044) last here: it is the only face row of the list
(5-5-5 face w5 w6 s5), the kind that survived ring 16 every time in rounds 52-53, so it is offered to Studio.
None of these rows was swept before in any orientation (canon_key against every win45 file and this log).
- **Tool** `loop/k47/q54.py`: q52r16 and stop14 in one driver. Per row, win45 windows in the 1.5-ball at ring <= 16,
  drive45 (kc D / kc -C -t 600, dfast / cfast --fixed, STOP=0, NW 3, 7,000 s cap), stopped once every ring <= 14 window
  is done and the row has a two-engine kill (or at its first kill after that); minkill47 f-names; a row with no kill at
  ring <= 16 gets its remaining ring <= 18 windows written as a Studio to-do file.
- **Hypothesis (Long Table):** the d10 and d8 binders die by ring <= 14, as the earlier d10s did. **Kill line:** they
  survive ring <= 16.
- **Guess:** every non-face row dies at ring <= 14 (each 80%; all ten 35%), as every non-face row of rounds 50-52 did;
  the face row 75666556/66666565 survives ring 16 (65%).
- **Also closed at 21:56Z: 8765556/6575965 (r52d, s22hL 0.020), pre-empted for this round.** No two-engine kill at ring
  <= 15 or in 164 of its 176 ring-16 windows; its 106 windows not run (12 at ring 16, 66 at 17, 28 at 18) are in
  `loop/k47/win52_7_8765556_6575965_todo.txt` for Studio. It is not a binder of the l3q solve.
- **22:00Z, d8 face row 75666556/66666565 moved (Long Table 21:57Z, Studio 21:58Z).** Studio runs its ring 15-16 and
  17-18 windows (`loop/k47/win54_8_75666556_66666565_r1516.txt`, 1,563, and `_r1718.txt`, 542; 2438e43f); explore runs
  ring <= 14 (1,611 windows) after the queue (R54_r54k.DONE marks it skipped by q54; scratchpad post54.sh runs it, then
  round 53b).
- **22:15Z, d10 6565656565/6556666666 (r54a, dual 0.078) dies at ring 14.** No kill at ring <= 13 (902 windows); at ring
  14 (957 windows) 16 two-engine kills (15 C, 1 D), 9 f-names (1 D, 8 C,
  twoeng on `loop/k47/r54a_kills*`: 1 D both engines, 8 C same X, 0 mismatch), every X interior-only ({I0-I1},
  {I0-I2}, {I0-I5}), so the ring-merge guard holds none. Inclusion-minimal: f10_...5656565_.......5.. (C) and
  f10_...5656565_......5... (C), both ring 14, m 9. Hypothesis right for this row (dies by ring 14).
- **22:27Z, d7 8658656/6665555 (r54b, dual 0.025) dies at ring 14.** No kill at ring <= 13 (575 windows); at ring 14 (309
  windows) 4 two-engine D (twoeng on `loop/k47/r54b_kills*`: 4 D both engines), 4 f-names, minimal f7_..56856_...566.
  (ring 14, m 9: the hub, link run 5-6-8-5-6 and s-letters 5-6-6). Hypothesis right for this row.
- **22:48Z, d8 face row 75666556/66666565 (dual 0.044) dies at ring 12 on our own windows.** Long Table 22:33Z asked for
  RSST 8406.123 (rsst433; interior u, w0, w7, w1, w5, w6, s5, s7) on kc as an independent engine: kc D false (as in
  k44), kc -C conservative false (|X| <= 4, best leftover 12; `loop/k54/rsst433_kc.out`). The same interior is this
  row's window a8_u75...556_.....5.5 (ring 12): also neither. But its neighbour a8_u75...556_.....565 (add s6 = 6) is
  C on kc -C with X={I0-I3} and on cfast --fixed (leftover 0). The row's ring <= 12 windows (477) were then run on both
  engines in `loop/k54/` (drive45 and minkill47 copies, own A_kcc.out and KILL, NW 1): 3 two-engine kills, 3 f-names
  (twoeng: 1 D, 2 C same X, 0 mismatch), every X {I0-I3}, interior-only. Minimal: f8_...55675_...565.. (C, ring 12, m
  9) and f8_..556665_..5..... (C, ring 12, m 8: the face w5 w6 s5 with the link run w1..w4 = 5666 and the hub). Guess
  (face row survives ring 16) wrong. Studio's ring 15-18 files for this row are no longer needed; its ring <= 14 run here
  is dropped.
- **22:57Z, d8 76656656/56655565 (r54c, dual 0.0125) dies at ring 12.** 82 two-engine kills at ring 12-14 (ring 12: 4 D,
  4 C), 72 f-names (twoeng: 32 D, 40 C same X, 0 mismatch); one C has ring edges in X ({I0-I5,I1-I2,R2-I0,R0-I2}: R2
  and R0 stay in different classes, so no ring merge), the rest interior-only. Minimal: f8_...56656_.....56. (C X={I3-I4},
  ring 12, m 8) and three at ring 14.
- **23:19Z, queue change (Long Table 23:18Z).** Opus's 11/75 cert (l3q on 3cfd7f18) has d7 8658656/6665556, d8
  76656566/56655565 and d7 8658656/7665555 at -2/75 after the three killed above. 76656566/56655565 is not a typo for
  76656656/56655565: canon_key gives 56566766/55565566 and 56656676/55566556, two rows (both were in the l3q list).
  New order after 85656765/56665565 (running): r54i 8658656/6665556, r54j 76656566/56655565, then `rows54b.txt`: r54l
  8658656/7665555 (new, never swept), then r54e-h (the remaining 0.0125 rows).
- **23:23Z, d8 85656765/56665565 (r54d, l3q 0.0125; not in the 11/75 cert) dies at ring 13.** 19 two-engine kills at ring
  13-14 (ring 13: 1 D, 1 C), 18 f-names (twoeng: 8 D, 10 C same X, 0 mismatch); 6 C carry one ring edge each (X = {I0-I1,
  R5..R8-I1}: one ring vertex per X, so no ring merge), 4 are interior-only. Minimal: f8_...56765_....55.. (D, ring 13, m
  8), f8_...56585_....655. (C, ring 13) and five at ring 14. Opus 23:19Z sent the 11/75 cert's full list (3e9b61bd): four
  -1/75 rows added to `rows54b.txt` after r54l (d7 8666655/5677657 and 8556856/7565666, both face rows; d8
  76556675/66665555 and 76765656/55556665), ahead of r54e-h (not in that cert).
- **23:25Z, d7 8658656/6665556 (r54i, -2/75 in the 11/75 cert) dies at ring 14 by r54b's four f-names** (`r54i_kills*`
  byte-identical to `r54b_kills*`: the killing windows avoid s6, the one letter the rows differ in). Already admitted on
  main with r54b (0c11734b); nothing new to admit. It shows in the 11/75 cert only because that cert is on 3cfd7f18.
- **23:29Z, admission head for r54d (Long Table 23:24Z: Studio silent).** Main already held r54a, r54b, r54k12 and r54c
  (Studio, 22:25-23:03Z; registry 2,435 D / 1,060 C). r54d's 18 f-names through main's own twoeng and guards on main
  21b1a8a1 (scratch copy): 2,443 D / 1,070 C, +8 D +10 C = exactly the 18, 0 lost, ring-merge / prefix / letter-9 0 new,
  regression byte-identical. This session pushes only to its own branch, so the result is `loop/k54/adm54d/` (k3x
  files + RUNLOG entry, 09a6a667) for Long Table to copy onto main.
- **23:45Z, d8 76656566/56655565 (r54j, -2/75) dies at ring 11.** 40 two-engine kills at ring 11-14 (ring 11: 1 D;
  12: 2 D; 13: 5 D, 2 C), 40 f-names (twoeng: 29 D, 11 C same X, all X interior-only, 0 mismatch). Minimal:
  f8_...65656_...5556. (D, ring 11, m 10) and three at ring 14. Admission check on main fd5ac400 (`loop/k54/adm.py`):
  2,472 D / 1,081 C, +40 exactly, 0 lost, guards 0 new; files in `loop/k54/adm54j/` (3b5fd9c2).
- **23:46Z, d7 8658656/7665555 (r54l, -2/75) dies at ring 14 by r54b's four f-names** (`r54l_kills*` byte-identical to
  `r54b_kills*`; the windows avoid s0, where the rows differ). Already on main. All three -2/75 rows of the 11/75 cert
  are dead; the -1/75 rows start with d7 8666655/5677657 (face row).
- **23:56Z, d7 face row 8666655/5677657 (r54m, -1/75): no kill at ring <= 14** (735 windows). Its ring 15-16 (491 windows,
  ~2 h here) is moved behind the other -1/75 rows: `rows54c.txt` runs d8 76556675/66665555, d8 76765656/55556665, the
  d7 face row 8556856/7565666, then r54m's ring 15-16, then r54e-h.
- **00:29Z, d8 76556675/66665555 (r54n, -1/75) dies at ring 13.** 85 two-engine kills at ring 13-14 (ring 13: 13 D, 5
  C), 85 f-names (twoeng: 72 D, 13 C same X, all X interior-only, 0 mismatch); 11 minimal, e.g. f8_...56675_.....55.
  (C, ring 13, m 8) and f8_...55675_...66.5. (D, ring 13). Admission check on main 33720b50 (00:30Z): 2,544 D / 1,094 C,
  +85 exactly, 0 lost, guards 0 new; files in `loop/k54/adm54n/`.
- **00:49Z, d8 76765656/55556665 (r54p, -1/75) dies at ring 13.** 11 two-engine kills at ring 13-14 (ring 13: 2 D),
  11 f-names (twoeng: 8 D, 3 C same X, interior-only, 0 mismatch); minimal f8_...65656_...5.66. (D, ring 13, m 9) and two
  at ring 14. Admission check on main 15bc20c7 (00:50Z): 2,552 D / 1,097 C, +11 exactly, 0 lost, guards 0 new; files in
  `loop/k54/adm54p/`. Every non-face binder of the 11/75 cert is now dead; left are the two d7 face rows.
- **01:00Z, d7 face row 8556856/7565666 (r54o, -1/75) dies at ring 14.** 4 two-engine D, 4 f-names: f7_..56856_...566.
  (r54b's minimal, already on main: the row contains it outright, which round 54b's registry step confirms, 100 percent of
  both apex parts) and three new, f7_.556856_...566., f7_.556856_.5.566., f7_.556856_.56566.. Admission check on main
  58aab9b0 (01:02Z): 2,555 D / 1,097 C, +3 D exactly, 0 lost, guards 0 new; files in `loop/k54/adm54o/` (7b7afa11). So of
  the 11/75 cert's binders only the d7 face row 8666655/5677657 is left (Studio has its ring 15-18 to-do, 778 windows,
  4099e8f5).

## Round 53b (19 Oct 2026, 21:42Z-): H-T87, do any of Opus's 87 tightest survivors of the face binder die at ring <= 16?

**Pre-registered 21:42Z, before any engine window of this round.** Long Table 21:28Z, from Opus s26r (e6bf1acb): face
binder 7665566/6675676 (Opus's orientation; the mirror of explore's 7665566/6765766). In its tightest one-ring-out
survivors the six privates are 666666 and ring 3 is all 5 or 6 except t = r13, the apex next to s2, s3 and s4, at 7,
8 or >= 9: 29 ring-3 words per value of t, 87 patterns (`s26r/tight29.txt`). Every ring-3 five sits on the far side
of the wheel (r0-r8 and r19, around w0, w1, w6 and their privates); r9-r18 on the face side are all 6 apart from t.
Run ahead of the other five non-family rows, right after 8765556/6575965.
- **Tool** `loop/k53/tight53.py` (on cen53): builds each exact 3-ball in Opus's frame (ring-3 order checked vertex by
  vertex against Opus's touch list), then 1. registry containment of the whole 3-ball (twoeng snapshot `tw54`: 2,413 D
  and 1,007 C on both engines, the three X-mismatch C names Studio holds out excluded); 2. windows: connected sets of
  exact vertices (9 = >= 9 is never in a window) with at most 8 vertices, at least 3 fives, free ring <= 16,
  deduplicated by kc line across the 87 patterns, run most fives first, then smaller ring, then most patterns served;
  kc -C -t 600, kc D on dfast, kc C on cfast --fixed with kc's X (cen53's engines; cen53's own verdicts reused where
  the kc line is identical). A pattern dies at its first two-engine kill; windows serving only dead patterns are
  skipped. NW = 3, 7,000 s cap. Names h7_<u><w>_<s>_<privates>_<r0..r19>.
- **Hypothesis (Long Table):** some of the 87 die. **Kill line:** all 87 survive ring <= 16 (no two-engine D or C
  among the windows tried). Ring 17-18 windows of the survivors go to Studio as usual.
- **Guess:** all 87 survive, 70%. The far-side fives are two steps or more from the face, and the face side looks
  like the binder's 1.5-ball (no kill to ring 18) with sixes around it. If anything dies it is a pattern with three or
  more far-side fives close together (as 56665566666667666665), through a window that does not contain the face.
- **Tool check before this pre-registration (21:36-21:42Z, cap 0, no engine run).** Registry: none of the 87
  contains any of the 3,986 registry configurations. Windows at MMAX 8, FMIN 3, ring <= 16: 4,276 distinct kc lines
  (18 with five fives, 415 with four, 3,843 with three; by ring 6-13: 900, 14: 911, 15: 1,303, 16: 1,162).
- **03:43Z, engine run started** as pre-registered (registry `tw54`, NW 3, 7,000 s cap), now that round 54b has closed.
- **04:35Z, engine run restarted** (the container restart at about 03:56Z killed it after 117 verdicts; those replay
  from `T_res.txt`), same command and cap.
- **04:36Z, stopped for round 54d** (Long Table 04:35Z: the 2026 set on our engines instead). Verdicts so far stay in
  `T_res.txt`; the run resumes from them later.


## Round 53 (19 Oct 2026, 18:24Z-): H-S53, split and kill, do the surviving face rows die one ring out, piece by piece?

**Pre-registered 18:24Z, before any engine window of this round.** Coordinator 18:10Z, from the user's sprint plan
("split and kill"): extend each surviving face row by the degrees just outside it and attack each extension on its
own. Extensions that die become registry kills; the survivors go to Opus via Long Table as the sharper binders a face
rule should read.
- **Tool** `loop/k53/cen53.py` (census50 + cen51 for receiver rows). Slots: the privates of each exact non-5 link
  vertex (census50's) and the ring-3 vertices next to s_(i-1), s_i, s_(i+1) of each 5-5-5 face w_i w_(i+1) s_i,
  each 5..9 (9 = >= 9, never exact). For 7665566/6765766 that is 10 slots (p01 p02 p11 p21 p51 p61, and next to the
  face w3 w4 s3: t(p21,s2), the apex t(s2,s3,s4), t(s4), t(s4,p51)), so 5^10 fillings. A five at the apex closes
  off its two ring-3 neighbours (they become adjacent), so the fillings are split into the apex = 5 part and the
  apex 6..9 part, each with a letter-independent structure (checked). The builder gained a ring vertex with no
  outward neighbour for this (cen53.LZ).
- **Method.** 1. Registry containment (census50's matcher: 582 RSST on two engines + explore's twoeng names, 3,337
  configurations). 2. Engine windows: connected interiors of the row's exact vertices plus 1-2 slots at letters
  5..8, ring <= 16 on this machine, fewer slots first, then more fives, then smaller ring; kc -C -t 600, kc D on
  dfast, kc C on cfast --fixed with kc's X; a window whose requirement is already covered is skipped. Coverage is
  the exact count of fillings in the union of requirement cylinders. Ring 17+ windows go to Studio as to-do files.
- **Rows**, by weight: 7665566/6765766 (the 0.231 binder's mirror), then Long Table's list 7665566/6675666,
  7655666/6756666, 7655667/6756656, 7765566/6575666, 7655566/6759676, then 7766556/6576576 and 7766556/6567566.
  2 h engine cap per row here.
- **Kill line, per row:** the row is killed when every filling is covered. Otherwise the uncovered set, per slot
  and in closed form where it is a product, is the survivor reported to Long Table.
- **Tool check before this pre-registration (18:18-18:21Z, registry only, no engine run).** On 7665566/6765766 the
  apex = 5 part is covered entirely: with the apex t(s2,s3,s4) = 5, {w3, s3, apex, s2} (5, 5, 5, 6) is a ring-7
  configuration inside the row (rsst001, also f7_.....55_.....65; re-run here on kc and dfast, both D). The apex
  6..9 part is 69.56% covered (19 minimal requirements, all RSST). Total 75.65%; uncovered 2,378,112 of 9,765,625,
  including all 59,049 fillings with every slot >= 7 and 1,028,352 of the 1,048,576 with every slot >= 6. The same
  tool on 7665566/6675666 without ring-3 slots reproduces round 50's census exactly (80.34%, 3,072 survivors).
- **Guess:** engine windows add less than 5 points on the apex 6..9 part of 7665566/6765766 (the uncovered fillings
  with every slot >= 6 have no five beyond the face), 70%. On every other face row, apex = 5 is covered by the
  registry alone wherever the face has a 6 next to it on the apex side (as s2 here), 75%.

- **18:45Z, registry step on all eight face rows** (`loop/k53/cen53_<row>.txt`; a slot-name sort bug crashed six rows'
  first runs at the engine step, fixed and rerun 18:28-18:44Z). Coverage of the 5^k fillings by the registry alone:

  | row | slots | apex = 5 | apex 6-9 | total |
  |---|---|---|---|---|
  | 7665566/6765766 (0.231 binder) | 10 | 100% | 69.56% | 75.65% |
  | 7665566/6675666 | 10 | 100% | 83.84% | 87.07% |
  | 7655666/6756666 | 10 | 100% | 83.84% | 87.07% |
  | 7655667/6756656 | 11 | 100% | 86.06% | 88.85% |
  | 7765566/6575666 | 11 | 100% | 86.32% | 89.06% |
  | 7655566/6759676 | 12 | 72.07% | 63.75% | 65.41% |
  | 7766556/6576576 | 11 | 100% | 68.13% | 74.50% |
  | 7766556/6567566 | 11 | 100% | 78.11% | 82.49% |

  Apex = 5 dies by the same ring-7 kite (the face's two 5s on the apex side, the apex, and the 6 beside them) in
  every row that has a 6 next to the face on the apex side. 7655566/6759676 has 7 and >= 9 there, so its apex = 5
  part is not covered. Second guess right (8 of 8 as predicted).

- **19:28Z, 7665566/6765766 engine step, order changed (explore's call).** First run 18:29-19:27Z in the pre-registered
  order (fewer slots, then more fives): 526 windows, 2 kills, both one five-slot windows: g7_-..655.._..65..._...5......
  (p21 = 5, ring 8, D) and g7_u76.5566_6..5..._..5....... (p11 = 5, ring 14, C X={I0-I2}). After its five-slot windows
  the order reached one-slot windows at 6-8, which add no five to a row whose only fives are the face. Restarted with
  more fives first, then fewer slots (ORDER=fives), verdicts kept (G_res.txt), for the rest of the 2 h cap (3,700 s).
  Separately, Studio's row 11 (this row at ring 17-18, 225 windows, bcf5d050): no kill; 218 kc neither, 7 ring-18 kc
  timeouts now on dfast18.

- **20:32Z, 7665566/6765766 (the 0.231 binder) after the engine step: 83.77% of its extensions die; survivors named.**
  The two engine runs (526 + 369 windows, 2 h cap reached at 20:31Z) found 10 two-engine kills (4 D, 6 C, every C
  with an interior-only X), all in the apex 6-9 part, e.g. g7_-..655.._..65..._...5...... (p21 = 5, ring 8, D) and
  g7_-.6655.._..65..._..55...... (ring 11, C X={I0-I1}). With the registry they cover 79.71% of the apex 6-9 part, so
  8,180,473 of 9,765,625 fillings (83.77%, from 75.65%). Recount with every cached kill in
  `loop/k53/cen53_final_7_7665566_6765766.txt`.
  - **Every private at 5 now dies** (p01, p02, p11, p21, p51, p61), and so does apex = 5.
  - **Survivors: apex >= 6 and all six privates >= 6.** Three ring-3 vertices beside the face can still be 5 in
    some survivors: t(p21,s2) next to s2, t(s4) and t(s4,p51) next to s4 (195,840, 122,880 and 169,728 survivors
    with that one slot at 5). 1,028,352 of the 1,048,576 fillings with every slot >= 6 survive, and all 59,049 with
    every slot >= 7.
  - First guess (engines add less than 5 points on the apex 6-9 part) was wrong: they added 10.15 points, all from
    windows with a five among the slots.
  Explore's cores go next to the six non-family rows (8765556/6575965 started 20:32Z), the face rows' engine steps
  after, unless Long Table reorders.

## Round 52 (19 Oct 2026, 12:44Z-): H-F18, do the surviving face receivers die at ring 17-18?

**Pre-registered 12:44Z, before any engine run on these targets.** Gap G2. Long Table, 12:41Z: Opus's stage 21 is
null (the sender weight moves to H0-big siblings), so the 55769 census is dropped as moot (stopped 12:41Z after 1,940
windows: registry covers 51.0% of its 3 x 5^12 fillings, plus 2 new D windows at ring 8; not a result). New priority:
ring 17-18 reducibility of the surviving face receivers, split with Studio by whole rows.
- **Rows** (13, no two are mirrors): 7665566/6765766 (cert_s22hL dual 0.112, the only one with s22hL weight), then
  by family.json dual 7766556/6576576 (0.104), 7766556/6567566 (0.101), 86555665/56586665 (0.016), 86555665/56576665
  (0.013), 85586556/66656565 (0.008), 8655567/5685756 (0.006), 8765556/6575866 (0.006), and the dual-0 rows
  7655666/6756666, 7655667/6756656, 7665566/6675666 (R*-like to ring 16), 7765566/6575666, 7655566/6759676 (R*-like
  to ring 14).
- **Split.** Explore: 7665566/6765766, then 7766556/6576576 and 7766556/6567566 (2 h each, `loop/k47/q52row.sh`).
  Studio: the other ten, whole rows, 6 h each, from `loop/k47/win52_<row>_todo.txt` (the row's ring <= 18 windows
  not yet run).
- **Method** as rounds 45-51: win45 windows of the row's 1.5-ball at ring <= 18 (letter-9 vertices never in a window),
  kc -C (-t 600) with D re-run on dfast (ring <= 16) or dfast18, C on cfast --fixed with kc's conservative X.
  Explore runs ring <= 16 with STOP=0, then ring 17-18 with STOP=1 (first two-engine kill closes the row).
- **Kill line, per row:** no D/C window at ring <= 18 means the row survives. A row that hits its cap is reported
  as undecided with the windows left. Rows are reported as they close; kills go the usual twoeng route.
- **Guess:** the rows already R*-like to ring 16 stay R*-like at 17-18 (70% each). Of the unswept rows, at least
  one dies at ring <= 16, as 7676556 and 8665566 did at 14 (65%).
- **Addition (pre-registered 12:45Z; Long Table, 12:44Z): the six non-family receivers of cert_s22hL**, after the
  13 family rows, heaviest first: 8765556/6575965 and 8765556/6575966 (0.020 each), d = 8 77665656/65665555 (0.020),
  d = 10 6556655556/6665669665 (0.010), d = 9 765556565/566966665 (0.007), d = 7 9559656/6665555 (0.003; w0 >= 9 never
  in a window). Ring <= 16 first; ring 17-18 only for a row that survives to 16. Same caps and kill line. Explore runs
  them after its three family rows (`loop/k47/rows52.txt`). Guess: at least four of the six die at ring <= 16, as the
  non-face rows did (65%).

- **14:39Z, 7665566/6765766 (explore): undecided at the cap.** No D/C window at ring <= 16 (all 1,287 windows; best
  kc leftover 128 at ring 14, 288 at ring 15, 648 at ring 16). Ring 17 hit the 2 h cap after 11 of 144 windows (kc
  about 322 s per ring-17 window on this machine, max 440 s; best leftover 1,350); ring 18 (92 windows) not started.
  The 225 ring 17-18 windows left are in `loop/k47/win52_7_7665566_6765766_todo.txt`, for Studio.
- **14:43Z, change of split (explore's call, reported to Long Table).** At ~322 s per window, explore's ring 17-18 phase
  covers about 30 windows in what is left of a 2 h cap, so it cannot close a row. From 7766556/6576576 on, explore runs
  each row at ring <= 16 only (STOP=0, `loop/k47/q52r16.sh`, same cap) and a row with no kill there gets its ring 17-18
  windows written to `loop/k47/win52_<row>_todo.txt` for Studio. 7766556/6576576 was restarted under it at 14:44Z
  (about 3 min of ring <= 12 windows lost; drive45 resumes from A_kcc.out). The kill line is unchanged.

- **16:28Z-16:31Z, Studio's rows (Studio's reports).** Rows 1-3 die: 86555665/56586665 and 86555665/56576665 at ring
  11 (D), 85586556/66656565 at ring 14 (D); 373, 459 and 40 two-engine kill windows so far, f-names still being
  collected. 7655566/6759676 **survives** (final, Studio commit 0bc4f723): no two-engine kill in 255 windows to ring
  18; 4 ring-18 windows timed out on kc at 600 s and are on dfast18, with any D to be confirmed by kc -t 3600; best
  kc leftover 256 bad classes at ring 15.
- **16:39Z, 7766556/6576576 (explore): no kill to ring 16, undecided at the cap.** 1,197 of 1,296 ring <= 16 windows
  run, none D or C, no kc timeouts (best leftover 144 at ring 14, 328 at ring 15, 656 at ring 16); 99 ring-16 windows
  not reached. Its 414 windows left (99 at ring 16, 192 at ring 17, 123 at ring 18) are in
  `loop/k47/win52_7_7766556_6576576_todo.txt`, for Studio. 7766556/6567566 started at 16:39Z.
- **16:39Z, tally.** Of the 13 family rows: 3 dead (Studio rows 1-3), 1 survives to ring 18 (7655566/6759676), 2
  undecided with their remainder at Studio (7665566/6765766, 7766556/6576576), 7 running (6 at Studio, 1 here).

- **Addition (pre-registered 17:07Z, before any engine run on these targets; Long Table 17:06Z): the 2/13 production
  binders** (Opus 20ee527a, 0125c46b). The face row 7665566/6675676 (0.231) is the mirror of 7665566/6765766 (same
  canon_key), so it is not swept again: its ring 17-18 remainder is already first in Studio's Job 52 queue. The two
  d = 10 rows (0.038 each) are new to every round's log and go ahead of the six non-family rows: 6565665656/6555555565
  (no 5-5-5 face next to the centre) and 6565555665/6665956566 (two faces, w3 w4 s3 and w5 w6 s5, around the centre's
  run of four 5s; s4 >= 9 never in a window). Ring <= 16 on explore (`q52r16.sh`, 2 h cap); a row with no kill there
  sends its ring 17-18 windows to Studio. Kill line unchanged. Guess: 6565665656/6555555565 dies at ring <= 14, as
  every non-face row has (75%); 6565555665/6665956566 dies at ring <= 14 through its run of fives, as d = 9
  655566556 did (60%).

- **17:19Z, Studio rows 3 and 10 final.** 7655566/6759676 survives with every window decided (the 4 ring-18 kc timeouts
  are dfast18 D=false; Studio 85134cf8). 85586556/66656565 is killed (Studio c503910a): 40 two-engine D
  windows at ring 14-16 give 20 distinct f-names (mirror pairs), and one inclusion-minimal f-name,
  f8_..556855_..5.566. (ring 14, m = 11). twoeng passes all 20 as D on both engines. They are in
  `loop/k47/s52r3_kills*` (from `loop/k47/minkill52.py`, minkill47 reading a Studio row folder) and go to Studio
  for admission. Admitted 17:21Z (registry ffa42f2d: 1,920 D / 841 C, +20 D, guards 0).

- **18:09Z, 7766556/6567566 (explore): no kill to ring 16, stopped early for the binders.** The user asked for full
  effort on whatever binds now (relayed 18:08Z). This row has no weight in the 2/13 bound, so explore stopped it 27 min
  before its cap to start the d = 10 binders. 1,305 of 1,421 ring <= 16 windows run, no D/C. Its 352 windows left (116
  at ring 16, 167 at ring 17, 69 at ring 18) are in `loop/k47/win52_7_7766556_6567566_todo.txt`, for Studio.
  6565665656/6555555565 started at 18:09Z, then 6565555665/6665956566.

- **18:22Z, d = 10 6565665656/6555555565 (2/13 binder, 0.038): dies at ring 13.** Stopped once dead (1,300 of 11,004
  ring <= 16 windows run, so ring 15-16 is not needed): 97 two-engine kills (16 D at ring 13, 81 D at ring 14), 59
  f-names, 5 inclusion-minimal, e.g. f10_...5656656_....55.55. (ring 13, m = 12). twoeng passes all 59 as D on both
  engines; `loop/k47/r52j_kills*`, to Studio for admission. Guess (dies at ring <= 14, 75%) right.
  6565555665/6665956566 started at 18:23Z (stopped once dead at ring <= 13, if it is).

- **18:26Z, Studio rows 1-2 final (Studio e2cb4e69).** 86555665/56586665: 415 two-engine kills (284 D, 131 C) at ring
  11-16, 381 f-names (twoeng: 255 D, 126 C, all pass), 7 minimal, lowest f8_..555665_........ (ring 11, D).
  86555665/56576665: 489 kills (400 D, 89 C), 446 f-names (twoeng: 357 D, 89 C), 8 minimal, same lowest. Files
  `loop/k47/s52r1_kills*`, `s52r2_kills*` (minkill52), to Studio for admission.

- **18:29Z, d = 10 6565555665/6665956566 (2/13 binder, 0.038): dies at ring 13.** Stopped once dead (1,295 of 7,469
  ring <= 16 windows): 22 two-engine kills (9 D and 11 C at ring 13, 2 D at ring 14), 22 f-names (twoeng: 11 D, 11 C
  with the same X, all pass), 4 minimal, e.g. f10_...5555665_.......5.. (ring 13, D). No name holds a 9. Files
  `loop/k47/r52k_kills*`, to Studio for admission. Guess (dies at ring <= 14 through its run of fives, 60%) right.
  Both 2/13 d = 10 binders are dead; the six non-family rows are next on explore's queue after round 53's binder run.

## Round 51 (19 Oct 2026, 01:54Z-): H-W0, do the binder's 7-sender rows die, and do its survivors die at ring 17?

**Pre-registered 01:54Z, before any engine run on these targets.** Gap G2. Long Table, 01:52Z: Opus's stage-14 certificate
has two co-tight d = 7 rows, 7665666/6566565 and 7655666/6756666. They are the 7s that act as sender w0 to the binder
7665566/6675666. Neither row has been swept before (canonical keys 5666766/6565656 and 5566676/5666667), and round 44's
RSST patterns miss both (eligible and broad-only alike). 3 cores.
- **Part 1, the two rows.** win45.py at ring <= 14 first, all windows, kc + dfast/dfast18 + kc -C with |X| <= 4
  (drive45.py, STOP=0). Only if a row has no kill there, its ring 15-16 windows (A16). Then minkill47.py, and twoeng via
  Studio. Hypothesis (Long Table): each dies at ring <= 16; a kill changes what w0 can afford. **Kill line:** no D/C
  at ring <= 16 means R*-like; report it and stop. Guess: 7665666/6566565 dies at ring <= 14 (three 5s in its s word
  and a 5 in its link, like the d = 9 rows that died). 7655666/6756666 has the binder's 55 pair with one 5 in s, so it
  is closer to the binder. I give it 40% that it dies.
- **Part 1b (pre-registered 02:08Z; Long Table, 02:08Z): two relay binders from s18r (9/52)**, run after part 1 and
  before part 2: d = 10 6565656565/6655666666 (canonical 5656565656/5666666665) and d = 7 7655667/6756656 (canonical
  5566776/5665667). Neither has been swept before, and the RSST patterns miss both. Each runs at ring <= 14 first, then
  ring 15-16 only if no kill. Hypothesis: each dies at ring <= 16. Kill line: no D/C at ring <= 16 means R*-like;
  report it and stop. The third binder, 5566766/5666667, is round 50's row (R*-like) and is not rerun. Guess: d = 10
  dies at ring <= 14 (ten link letters alternating 6 and 5, like the d = 9 rows that died). d = 7 7655667 has the
  5-5-5 face (w2, w3, s2) again, between two 7s, so I give it 40%.
- **Part 1c (pre-registered 02:38Z; Long Table, 02:36Z): s19c (6/35 on 09d8ac38) secondary binders**, low priority,
  after part 1b and before part 2: d = 9 655566556/757656565, d = 7 7676556/7759565, d = 7 7655566/6759676. The fourth,
  d = 7 7666566/5656656, is 7665666/6566565 (part 1) under reflection (canonical 5666766/6565656), so it is not rerun.
  Same method and kill line. Two rows carry an s letter 9 (degree >= 9). win45.py now leaves letter-9 vertices out of
  windows, since a 9 is never exact; no earlier swept row had a 9. Guess: d = 9 dies at ring <= 14. The two d = 7 rows
  with a 9 at s3 die at ring <= 14 (both have a 556 or 555 run next to a 5 in s), 60%.
- **Part 1d (pre-registered 02:47Z; Long Table, 02:46Z): s19r's top binder d = 7 7765566/6575666** (canonical
  5566776/5666657, new), last in the binder list, before part 2. Same method and kill line. It has the 5-5-5 face
  (w3, w4, s3) under two 7s, one ring from the binder, so I give it 40%. d = 10 6565656565 already runs first after
  part 1, as asked.
- **Part 1e (pre-registered 03:11Z; Long Table, 03:10Z): s20c (8/47) binders d = 7 8665566/5675665** (canonical
  5566866/5665567) **and d = 8 76566656/65566556** (canonical 56665676/56655665). Both are new, and they run after
  7765566, before part 2. Same method and kill line. The queue now reads its rows from `loop/k47/rows51.txt`
  (q51f.sh), so later additions need no restart. Guess: 8665566 has the 5-5-5 face (w3, w4, s3) under an 8, so 40%.
  The d = 8 row has four 5s in s and two in its link, so it dies at ring <= 14 (70%).
- **Part 1f (pre-registered 05:39Z; Long Table, 05:39Z).** On 880d25c6 (Studio admitted r10b: 841 D / 633 C, dcount
  15,881), s21c shows the d = 10 row has left the dual. Its top receiver, 7765566/6575666, moves up to run right after
  7655667. Two new d = 9 rows go last, before part 2: 765556565/566956665 (canonical 555656576/695666556) and
  655665556/666559575 (canonical 555665566/595566657). Both have one s letter 9, which win45 leaves out of windows.
  Same method and kill line. Guess: both die at ring <= 14, since they have a 555 run in the link like the d = 9 rows
  that died (60% each).
- **Rule change (07:03Z; Long Table, 07:02Z).** Three of three face rows were R*-like at ring 16. So face rows
  (7765566, 7676556, 7655566, 8665566, d = 9 655566556) now run to ring <= 14 only. A kill there falsifies the face
  hypothesis and is reported at once; no kill is logged as "face row, presumed R*-like (ring 14)". Non-face rows
  (d = 8 76566656 and the two new d = 9 rows) keep the ring-16 kill line and run first. Part 2 follows as the one
  pattern-side test left for the face family. Order: 7765566 (ring 14, running), 76566656, 765556565, 655665556, then
  the face rows, then part 2 (`loop/k47/rows51.txt`).
- **7765566/6575666 (s21c's top receiver): face row, presumed R*-like (ring 14).** All 763 windows at ring <= 14 ran
  (578 already run, 07:02-07:06Z), with 0 mismatches and no D or C. The best ring-14 leftover is 128
  (a7_u..65566_.57566.). It ran under the face rule, so it stopped at ring 14. `r7j_kills*` is empty.
- **Part 3 (pre-registered 07:09Z, Long Table 07:08Z; result 07:25Z): the published set D of Inoue, Kawarabayashi,
  Miyashita, Mohar, Thomassen, Thorup (arXiv:2603.24880).** Published configurations are allowed as registry patterns
  once our two engines verify them; their rules are not. Hypothesis: some configuration in D is reducible on our
  engines and contains a face-family row, so it kills the family. Kill line: no candidate matches the family, or none
  survives twoeng. Guess: no row match, since our own ring <= 16 windows of these rows were never reducible.
  - Fetched by git from github.com/near-linear-4ct/reducible-configurations (MIT, HEAD c2ce7a96). It has 8200 .conf
    files, not 8202: the README says the set is D minus the degree-3 and degree-4 vertices. Rings 6-18 (69 at ring
    17, 15 at ring 18). All 8200 rings are free-completion cycles. 7040 have every degree <= 8, and 955 contain a
    7-5-5 / 5-5-5 kite. As kc lines: `loop/k51/nl51_kc.txt`.
  - `loop/k51/nl51.py` uses round 44's containment. **No configuration in D appears in the 1.5-ball of any face row**
    (7665566/6675666, 7655666/6756666, 7655667/6756656; reflections are included because all images are matched).
    **Kill line met: no candidate matches the family, so there was nothing to run on the engines.** Guess right.
  - One ring out (each row's 2-ball, privates 5..9): for 7665566 and 7655666, D covers exactly the cases our
    registry already covers (12,553 of 15,625; with no private 5, 1,024 of 4,096). For 7655667 (7 privates), D adds
    576 cases (registry 64,877 of 78,125, with D 65,453), all with a private 5. The no-5 cases stay at 7,168 of
    16,384. So D does not reach the big-privates survivors either. `loop/k51/nl51_hits.txt` lists D's requirements.
  - The d = 8 sweep (76566656) was paused 07:10-07:16Z for this and then resumed.
- **d = 8 76566656/65566556 (s20c, non-face) dies at ring 12** (07:49Z; all 1497 windows at ring <= 14, 824 run
  before the pause, 0 mismatches; 07:16-07:48Z). 98 kill windows and 53 f-names (twoeng: 28 D, 25 C, all C with
  the same X on both engines). Minimal: f8_.656.656_.55..55. (D, ring 12), f8_...56665_......55 (C, ring 12),
  f8_...56665_.....65. and f8_...56665_....6.5. (C, ring 13). Guess (70% at ring <= 14) right. It stopped at ring 14
  because it has kills. Twoeng-ready: `loop/k47/r8b_kills*`. Studio admitted all 53 (07:53Z): registry 5fa0adb0,
  869 D / 658 C, dcount 15,909.
- **d = 9 765556565/566956665 (part 1f, non-face) dies at ring 12 (C)** (08:40Z; all 2125 windows at ring <= 14,
  159 already run, 0 mismatches; 07:49-08:40Z). 168 kill windows and 168 f-names (twoeng: 93 D, 75 C with the same
  X). 19 are minimal: f9_...556565_....5.... and f9_..5556565_......... (C, ring 12), then 5 at ring 13 and 12 at
  ring 14. Guess (60%) right. Twoeng-ready: `loop/k47/r9f_kills*`. Studio admitted all 168 (08:45Z): registry 35aeebb8, 962 D / 733 C,
  dcount 16,002. (Studio's parser rejects f-names with a 9; win45 and win51 never put a 9 in a window.)
- **d = 9 655665556/666559575 (part 1f, non-face) dies at ring 12** (09:57Z; all 2942 windows at ring <= 14, 55
  already run, 0 mismatches; 08:40-09:56Z). 591 kill windows and 514 f-names (twoeng: 457 D, 57 C with the same X).
  17 are minimal, 8 of them at ring 12: e.g. f9_..5556655_......... (D) and f9_...555665_.....5... (C). Guess (60%)
  right. Twoeng-ready: `loop/k47/r9g_kills*` (Studio admitted all 514 at 10:09Z: registry 4b28f532, 1,419 D / 790 C,
  dcount 16,459). **All non-face rows of round 51 have died** (7665666, both d = 10,
  d = 8 76566656, both d = 9), at ring 12-13; every face row tried is R*-like. Face rows at ring 14 now run.
- **Face rule falsified for the d = 9 face row 655566556/757656565 (10:02Z, reported at once): it dies at ring 12.**
  With 1228 of 3290 ring-14 windows run: 185 two-engine kills (ring 12: 38 D, 3 C; ring 13: 150 D, 1 C), 0
  mismatches. The kills avoid the face: the smallest, a9_u.5556655._......... (D, ring 12), is the 9-centre and its
  link run w1..w7 = 5556655 with no s vertex. So a 5-5-5 face at a 9 dies through the centre's fives; the face
  hypothesis stands for the d = 7 rows only. The same window kills family.json's receiver 9 655566556/759556565
  (same link). The row runs on to the end of ring 14.
  - Complete (11:13Z; all 3290 windows, 0 mismatches; 09:57-11:12Z): 681 kill windows and 599 f-names (twoeng: 540 D,
    59 C with the same X). 17 minimal, 5 at ring 12 (e.g. f9_..5556655_......... D, f9_...556655_.....5... C).
    Twoeng-ready: `loop/k47/r9e_kills*`. Studio admitted them (11:14Z; 65 D and 11 C were already in from r9g):
    registry 03c34729, 1,894 D / 838 C, dcount 16,934.
- **Face rule falsified for the d = 7 face row 7676556/7759565 (11:21Z, reported at once): it dies at ring 14 (D).** All
  612 windows at ring <= 14 ran (113 already run; 11:12-11:21Z), 0 mismatches. 3 kill windows and 3 f-names (twoeng:
  3 D). Minimal: f7_5567676_..5..5. (a7_u7676556_..5...5): the 7-centre, its whole link and s2 = s6 = 5. It holds
  the face's link fives w4, w5 but not the apex s4, so the kill does not use the face triangle. This is family.json's
  receiver 7676556/7759565 itself (dual 0.055-0.058 in all three certs), now dead. Twoeng-ready: `loop/k47/r7h_kills*`.
  Studio admitted the 3 (11:23Z): registry 0125c46b, 1,897 D / 838 C, dcount 16,937.
- **7655566/6759676: face row, presumed R*-like (ring 14)** (11:25Z; all 628 windows at ring <= 14, 335 already run,
  11:21-11:24Z; 0 mismatches, no D or C). Best leftovers: 32 at ring 12, 64 at ring 13, 128 at ring 14
  (a7_u7655566_.75.6..). `r7i_kills*` is empty.
- **Face rule falsified for 8665566/5675665 too (11:37Z, reported at once): it dies at ring 14 (C).** All 938 windows
  at ring <= 14 ran (401 already run; 11:24-11:36Z), 0 mismatches. 8 kill windows and 6 f-names (twoeng: 3 D, 3 C
  with the same X). Minimal: f7_.556686_....55. (a7_u86655.6_5.....5, C, X = {I0-I6}). It holds the face's link
  fives w3, w4 but not the apex s3. So of the face rows at ring 14, 7676556 and 8665566 die without using the apex,
  while 7765566 and 7655566 stay R*-like at ring 14, and 7665566, 7655666, 7655667 at ring 16. Twoeng-ready:
  `loop/k47/r7k_kills*`. Studio admitted the 6 (11:41Z): registry fbc18afa, 1,900 D / 841 C, dcount 16,940.
- **fam51 (11:37Z, on the 26 senders; registry snapshot 582 RSST + 2,735 twoeng names, 3,317 configurations).**
  **Kill line met within a minute: the face family survives.** The three heaviest contexts (55667 [0,0,0,1,0|1,0],
  [0,0,0,0,0|1,1], [0,0,1,1,0|0,0]; max dual 0.101, 0.097, 0.058) are registry-dead in all 32 cases. The fourth,
  **55769 [0,0,1,0,0|0] (dual 0.055 st18hL, 0.058 st19wL), survives at its all-6 case**: v = 5, link 5,5,7,6,>=9,
  H0 = H1 = H3 = H4 = 6, H2 big, F3 = 6. Its 10 exact vertices give 142 windows (139 distinct), all at ring <= 14;
  none is D, kc -C finds no X, and the whole exact set (ring 14) has best leftover 260. Our 4 non-registry-dead
  cases of this context are exactly Opus's 4 admissible ones. Guess (70% survives) right. `loop/k51/F_*`,
  `loop/k51/fam51_family_1f025ab7.txt` (copy of the run log).
- **Survey (pre-registered 11:39Z, after the kill line; minutes of CPU): every sender, no stop** (SURVEY=1), to list
  which contexts our engines kill outright and which cases survive, for Opus's stage 20. Not a claim and no kill
  line; any kills go to Studio as usual. Guess: about half the 26 contexts die (the 12 registry-dead ones plus a few).
  - **Survey result (11:47Z; 11:39-11:46Z, 1,437 distinct windows, 0 mismatches): 16 of the 26 contexts die in
    every case, 10 survive.** 12 die on the registry alone (Opus's 8 inadmissible ones and 55667 [0,1,0,0,0|1,1],
    [0,1,0,1,0|0,0], [0,1,0,1,0|1,0], 55758 [0,0,0,0,0]); 4 more need engine windows: 55767 [0,0,0,0,0|0] and
    [0,0,1,1,0|0], 55858 [0,0,0,0,0], 55668 [0,1,0,0,0|0,0]. Engine kills: 14 windows, all D on both engines (twoeng
    14 D, 0 C), e.g. p5_u556.._.6..._..5.. at ring 8; list in `loop/k51/fam51_survey_kills.txt`.
  - Survivors (context: surviving cases in slot order, see the log): 55769 [0,0,1,0,0|0] (4 cases) and
    [1,0,1,0,0|0] (all 16); 55667 [1,0,1,1,0|0,0] (2); 55669 [1,0,1,0,0|0,0] (8), [0,1,0,0,0|1,0] (1),
    [0,1,0,0,0|0,0] (1); 55686 [1,0,0,1,0|0,0] (1); 55959 [0,0,0,0,0] (4); 55668 [0,1,0,1,0|0,0] (1); 55676
    [1,0,1,1,0|0,0] (1). In every survivor the all-6 case survives. The 10 carry 0.005-0.058 each; the dead 16
    include the three heaviest (0.101, 0.097, 0.058). Guess (about half die) right. `loop/k51/fam51_survey.txt`.
- **Census one ring out of 55769 [0,0,1,0,0|0], all-6 case (pre-registered 11:48Z; Long Table, 11:39Z), before any
  run.** Opus's stage 21 has not reported yet (96a5cd72), so the hold rule does not apply. `loop/k51/cen51.py`. One ring
  out = the 13 vertices of the exact set's ring other than w4: H2 (7, 8, >= 9), p21 p22 (privates of w2), p41 p44 (w4's
  privates next to H3/H4) and 8 ring-3 vertices next to H0 H1 H3 H4 F3; letters 5..9, 3 x 5^12 fillings.
  - Coverage: registry containment first, then engine windows (interior = exact vertices plus 1-3 slots at letters
    5..8, free-completion ring <= 16; fewer slots, more fives, smaller ring first; covered requirements skipped).
    Exact count of covered fillings. Cap 2 h (engines 6,000 s).
  - **Kill line** (Long Table: "nothing in the uncovered part shrinks below the all-6 core"), read as: every filling
    with all 13 slots >= 6 stays uncovered, so the case survives one ring out with nothing smaller to aim at.
  - **Guess:** coverage comes from fillings with a 5 next to the core; the all->= 6 fillings stay uncovered, so the
    kill line is met (75%).
- **fam51 dry run on family.json (Opus 1f025ab7, copied to `loop/k51/family_1f025ab7.json`; 10:02Z, no engines).**
  `loop/k51/fam51.py`: each sender context's exact cases (Opus's expansion, admissible or not) are first matched
  against our registry (582 RSST + 2,203 twoeng names; census50's matcher, interior onto exact vertices only). All 8
  contexts Opus marks inadmissible are registry-dead in every case, and so are 55667 [0,1,0,0,0|1,1], 55667
  [0,1,0,1,0|0,0], 55667 [0,1,0,1,0|1,0] and 55758 [0,0,0,0,0] (Opus: 4, 8, 4 and 4 admissible cases). 14 contexts
  keep 1-16 cases. A sender's exact vertices give windows only up to ring 14-16, so ring 17-18 arises only for the
  receivers. Order: senders by max dual, heaviest first, then the receivers.
- **Part 2 re-pointed (pre-registered 09:33Z; Long Table, 09:32Z), before any engine run on the new target.** Opus's
  stage 19 and 19b oracles (loop/opus/P_own_lp/FINDINGS.md) show that the LP rebuilds 10/63 from whichever members
  of a face five's context family are left, so a kill counts only if it covers the whole family. The generic ring-17
  probe below is replaced. Target: the 5-5-5 face at a 7 with w3 = 6, the near hats fixed, and every sibling sender
  context, as listed by Opus in P_own_lp/s19e/family.json (work from that file; not written yet at 09:33Z).
  - **Method.** Each member, expanded over its small vertices (5 or 6), big vertices left on the ring. Windows at
    ring 17-18 (and below), dfast18 + kc for D, cfast + kc -C with conservative X for C. Runs after 655665556 and the
    four face rows at ring 14.
  - **Hypothesis:** every family member has a D/C window at ring <= 18. **Kill line:** any member with no D/C window
    at ring <= 18 means the family survives; stop and report which member. **Cap:** 1 h per member, 8 h in total.
  - **Letter 9 (adopted 09:32Z):** a 9 in a link or s-word means exactly 9 in a name; names with a 9 are excluded and
    logged, and Studio is warned before any 9s appear.
  - **Guess:** the family survives (70%). The 7-centred view of the same faces had no window at ring <= 16, and the
    members with H0 or the far hats big leave those vertices on the ring, so their windows are weaker still.
- **Part 2, if cores remain: the binder's census survivors at ring 17.** These are the cases with every private >= 6 and
  p51 >= 7. A new generator, `loop/k47/win51.py`, takes windows of the binder's 2-ball that use at least one private,
  with each private in the window at an exact letter its survivor set allows (6..8, p51 7..8; a 9 is never exact).
  Ring 17 windows are ordered by more fives, then more sixes, and the first 200 run with a 600 s cap per window.
  Hypothesis (Long Table): some survivor sub-context becomes D or C at ring 17. **Kill line:** 0 kills in the first
  200 windows; stop and report the best leftover. Guess: 0 kills. The survivors have no 5 beyond the binder's three,
  and ring 15-16 got no closer than leftover 256.

**Result so far (02:38Z).**
- **7665666/6566565 dies at ring 12 (D).** All 1139 windows at ring <= 14 ran, 0 mismatches: 39 kill windows and 33
  f-names (twoeng: 22 D, 11 C). Minimal: f7_...6566_...665. (D, ring 12) and f7_..66566_..5..5. (D, ring 12), then
  f7_..56676_...5.5. (C, ring 13) and f7_5666766_...5... (C, ring 14). Guess right. Twoeng-ready: `loop/k47/r7e_kills*`.
  This also settles s19c's 7666566/5656656, its mirror image.
- 7655666/6756666: no kill at ring <= 14 (875 windows, 0 mismatches). Its ring 15-16 windows have been running since
  02:19Z (1372 at ring <= 16, 910 already run).
- **7655666/6756666: kill line met at ring <= 16, so the row is R*-like; reported, and stopped there.** All 1372
  windows ran (the last 9 after the first job hit its 2-hour limit at 03:54Z), 0 mismatches, slowest kc 237 s. None
  is D, and kc -C finds no X at |X| <= 4. The best leftovers, all with u, w and s2 in the window, are 128 at ring 14
  (a7_u7655666_..56..6), 256 at ring 15 and 512 at ring 16. They double with each ring, as for the binder. Guess (40%
  that it dies) was on the wrong side. Like the binder, it has the 5-5-5 face (w2, w3, s2) next to the 7-centre.
- **d = 10 6565656565/6655666666 dies at ring 13 (C)** (1832 windows, 110 already run, 0 mismatches; 03:59-04:31Z).
  26 kill windows and 14 f-names (twoeng: 4 D, 10 C). Minimal: f10_...5656565_......55.. (C, ring 13) and
  f10_...5656565_........55 (C, ring 14). Guess right. Twoeng-ready: `loop/k47/r10b_kills*`.
- d = 7 7655667/6756656: no kill at ring <= 14 (784 windows, 375 already run). Its ring 15-16 windows (1411 at ring
  <= 16) started 04:38Z. The queue job hit its 2-hour limit at 05:11Z with 249 ring-16 windows left. From now on each
  row runs as its own job (`q51row.sh`), so one job fits inside the limit.
- **7655667/6756656: kill line met at ring <= 16, so R*-like; reported, and stopped there** (07:02Z; all 1411 windows,
  0 mismatches; the last 249 ring-16 windows took 05:11-07:01Z, slowest kc 285 s). None is D, and kc -C finds no X at
  |X| <= 4. Best leftovers: 144 at ring 14, 256 at ring 15 (a7_u7655667_..56.56), 656 at ring 16. Guess (40%) was on
  the wrong side. That makes three rows with a 5-5-5 face next to the 7-centre (7665566, 7655666, 7655667), and all
  three are R*-like. Only 7665666, which has no such face, died.

## Round 50 (18 Oct 2026, 22:29Z-): H-RL, do the relay class's new receivers die at ring <= 14?

**Pre-registered 22:29Z, before any engine run on these targets.** Gap G2. Long Table, 22:28Z: on 42c4c876 the relay
class's dual (19/102, one engine) has two receivers not yet swept, d = 7 7665566/6675666 and d = 10
6556656556/6665656665. The d = 9 relay rows still bind: 656565665/665666566 (round 47 B, paused at 1526 of 2212
windows) and 656656665/665555555 (not swept before; new to this loop). Senders 66669 and 56696 are shared with the
main line (round 49). Queued after round 49, 3 cores.
- **Order.** d = 7, then finish round 47 B's d = 9 row, then d = 9 656656665/665555555, then d = 10.
- **Method** as rounds 47-49: win45.py at ring <= 14, drive45.py (STOP=0) in loop/k47, minkill47.py. Windows whose
  names were already run for another row are counted from the window files as they are built, before their engine run.
- **Hypothesis:** each row dies at ring <= 14. **Kill line:** a row with no two-engine kill at ring <= 14.
- **Guess.** d = 7 dies at ring <= 13 (its 55 pair sits between 6s as in 7765556). d = 9 656656665/665555555 dies
  early, ring <= 12, since eight of its nine s letters are 5. d = 10 dies at ring 13-14 (less sure, about 60%).

**Result so far (23:04Z).**
- **d = 7 7665566/6675666: kill line met.** All 864 windows at ring <= 14 ran (22:43-22:51Z; 92 names already run, no
  earlier kills), 0 mismatches. None is D, and kc -C finds no X at |X| <= 4 for any of them. Round 44's RSST
  patterns miss the row too (eligible and broad-only alike). The row has a 5-5-5 face (w3, w4, s3) next to the 7-centre;
  every other letter is 6 apart from w0 = s2 = 7. Guess wrong. Next for it: ring 15-16 (win45 A16), queued after the d = 10 row.
- **d = 9 656565665/665666566 (round 47 B), complete** (all 2212 windows, 0 mismatches): 90 kill windows, 73 f-names
  (twoeng: 28 D, 45 C with the same X). 11 minimal, first at ring 13 (C): f9_...565656_......56.,
  f9_...565665_......5.. and f9_..5656565_......... . Twoeng-ready: `loop/k47/r9b_kills*`.
- d = 9 656656665/665555555 running since 23:03Z: 3150 windows, 225 already run, none already kills. RSST patterns miss it.
- d = 10 6556656556/6665656665: RSST patterns miss it. It is queued next.

**Pre-registered 23:07Z (Long Table, 23:05Z), before either run: two follow-ons for d = 7 7665566/6675666.**
- **Ring 15-16 sweep** (win45 A16, drive45 STOP=0), after the d = 10 row. Hypothesis: some window at ring 15-16 is D or
  C on both engines. **Kill line (Long Table):** no D/C at ring <= 16 means the row is R*-like and goes to the rule
  side. Guess: about 40% that it dies.
- **Growth census one ring out** (`loop/k50/census50.py`, as round 42 for R*), run between the d = 9 and d = 10 rows. The
  row fixes u, w and s, so one ring out is the 6 privates of the non-5 link vertices (2 at w0, 1 each at w1, w2, w5,
  w6), letters 5..9 with 9 never exact. That is 15,625 cases, so the census is exhaustive rather than a 50k sample.
  The forbidden set is the verified registry as this loop sees it: the 582 two-engine RSST configurations plus every
  explore name that twoeng accepts. It is reported separately for RSST alone and for RSST plus explore. Guess: 20-40%
  covered, about 0% of the cases with no private 5.

**Note 23:28Z (Long Table, 23:27Z).** The new main-line receiver, d = 7 7665566/6665766 (s16, ab3f252b, 2/5), is
7665566/6675666 reflected (w_i -> w_-i, s_i -> s_-i-1). Both have canonical key 5566766/5666667, so they are the
same row. Its ring <= 14 result is therefore already known: no kill in 864 windows. The census and the ring 15-16
sweep above serve both lines. New order (q50d.sh): census, then the d = 7 ring 15-16 sweep, then the d = 10 row.

**Result, 19 Oct (01:29Z).**
- **d = 7 7665566/6675666 (= main line 7665566/6665766) at ring 15-16: kill line met, so the row is R*-like and goes to
  the rule side on both lines.** All 1374 windows at ring <= 16 ran (510 of them new at ring 15-16; 23:54Z-01:22Z), 0
  mismatches, slowest kc run 182 s against a 600 s limit. None is D, and kc -C finds no X at |X| <= 4 for any of them.
  The best leftovers at ring 15 are 256 (a7_u7665566_.6.566. and a7_u7665566_6..56.6). Guess (about 40% that it dies)
  was on the wrong side.
- **Growth census of the same row one ring out (23:54Z, `loop/k50/census50_7_7665566_6675666.txt`).** Exhaustive over
  15,625 cases. The registry is 582 RSST configurations plus 1402 explore names (twoeng: 804 D, 598 C with the same X;
  the 3 broad-only C kills from k38 are excluded). No configuration sits in the row itself. **80.3% is covered**: every
  case with a 5 among the six privates (11,529 of 11,529) dies, and so do the no-5 cases with p51 (the private of w5)
  equal to 6 (1,024; rsst098). Each private 5 kills on its own: rsst180 at p01 or p02, rsst052 at p11 or p61, rsst025,
  rsst050 or f7_...5565_....... at p21, and rsst050 at p51. **Survivors: 3,072 cases, exactly those with every private
  >= 6 and p51 >= 7.** Explore names cover nothing that RSST does not. With a 9 one ring out, 77.6% is covered; with
  every private >= 7, 0%. Guess (20-40%) was too low. For the rule side, the row needs paying for only when its six
  privates are all big (p51 >= 7).
- **d = 9 656656665/665555555, complete (23:54Z, 3150 windows, 0 mismatches): dies at ring 13.** 398 kill windows, 383
  f-names (twoeng: 295 D, 88 C). 29 minimal f-names, 15 of them at ring 13 (8 C, 7 D), e.g. f9_...565665_.......55 (C)
  and f9_...565666_....55.5. (D). Guess (ring <= 12) was one ring too low. Twoeng-ready: `loop/k47/r9d_kills*`.
- **d = 10 6556656556/6665656665: dies at ring 14.** 2097 windows (none run before). 1097 had run when the queue hit its
  2-hour limit at 01:28Z; 13 of them are two-engine kills, all at ring 14 (10 D, 3 C). The rest resumed at 01:29Z.
- **d = 10, complete (01:51Z; 2097 windows, 0 mismatches; resumed again after a container restart at 01:41Z).** Dies at
  ring 14: 19 kill windows, 19 f-names (twoeng: 11 D, 8 C). 7 minimal, all at ring 14 (5 C, 2 D), e.g.
  f10_..55665565_.......... (C) and f10_...5566565_......65.. (D). Guess (ring 13-14) was right. Twoeng-ready:
  `loop/k47/r10a_kills*`.
- **Round 50 closed.** Of the relay class's four rows, three die (both d = 9 at ring 13, d = 10 at ring 14). The d = 7
  7665566 family, which is also the main line's row, has no kill at ring <= 16 and goes to the rule side.

## Round 49 (18 Oct 2026, 22:11Z-): H-R9, does the d = 9 receiver of the new 1/5 dual die, and how far do patterns reach its senders?

**Pre-registered 22:11Z, before any new engine run on these targets.** Gap G2. Long Table, 22:09Z: with round 48 loaded
(42c4c876 + r_5..r_8), Opus's main line stays at exactly 1/5 (8592bb50) with a 3-row dual: receiver d = 9
656566565/665656666 (1/5), senders 66669 (3/5) and 56696 (1/5) in their s14 contexts. 3 cores. Round 47 B's d = 9
relay row is paused at 1526 of 2212 windows.
- **Receiver.** Round 44's eligible patterns miss it (only broad-only rsst588 hits). win45.py at ring <= 14 gives 2201
  windows. 538 of them have names already run in loop/k47 (the d = 9 relay row), and **7 of those are already
  two-engine kills (known before running).** The rest run now in loop/k47 (drive45.py, STOP=0). Hypothesis: it dies at
  ring <= 14; kill line: it does not.
- **Senders, s14 contexts.** All in this receiver: 66669 at w1, w6 and w8 (its 9 is u itself), 56696 at w3. Kills that
  contain each wheel are read off as in round 48.
- **Senders, one-ring coverage (grow49.py).** As round 46 B, with one change: a link letter 9 means degree >= 9. So that
  vertex is never an exact image, and its privates are left out of the 2-ball's exact vertices and slots (their
  number and adjacencies depend on the true degree). Columns: all fillings; with a 5 in ring 2; with no 5; with every
  ring-2 letter >= 7; and (Long Table) with a 9 in ring 2.
- **Guess.** The receiver dies at ring <= 14 (it already does). 66669's coverage is under 5% (no 5 in the wheel apart
  from the centre, so RSST configurations need several ring-2 fives). 56696's is 30-60%.

**Result, receiver and s14 contexts (22:42Z; 2201 of 2201 windows, 0 mismatches).** Hypothesis confirmed.
- d = 9 656566565/665656666: 100 two-engine kill windows (31 D, 69 C), first at ring 13. They have 85 distinct f-names,
  and twoeng gives 30 D and 55 C with the same X on both engines. Inclusion-minimal: 16 windows, 11 f-names, all C (5
  at ring 13, 6 at ring 14). Ring 13: f9_...565656_......56., f9_...565665_......5.., f9_...565665_....56... and
  f9_..5656565_......... . Twoeng-ready: `loop/k47/r9c_kills*`.
- Sender wheels in this row: 56696 at w3 is in 31 of its 83 wheel windows' kills, smallest at ring 13 (C,
  a9_u.565665.._..56.....). 66669 has kills at all three places, each smallest at ring 14 (C): w1 4 of 29, w6 3 of 19,
  w8 4 of 20.

**Result, senders' one-ring contexts (22:44Z; `loop/k46/grow49_<word>.txt`).** Guess half right: 56696 is in range, but
66669 is well above 5% overall. Only its contexts with no 5 are that low. Covered = some verified RSST configuration
appears in the 2-ball (a 9 is never an exact image).
- Both words have their 9 in the link already (it is u in the receiver). So Long Table's 9 column counts fillings
  with a 9 in ring 2.

| sender | fillings | all | with a 5 in ring 2 | no 5 | all >= 7 | with a 9 in ring 2 |
|---|---|---|---|---|---|---|
| 56696 | 390,625 | 49.2% | 57.6% | 7.4% | 0% | 46.3% |
| 66669 | 1,953,125 | 29.9% | 34.1% | 3.0% | 0% | 27.4% |

- The pattern is the same as rounds 46 and 48: contexts with a 5 in ring 2 die often, and those without one almost never
  do. A 9 in ring 2 lowers coverage only a little.

## Round 48 (18 Oct 2026, 21:48Z-): H-R15, does the 1/5 receiver die, and how much of its senders' one-ring contexts can patterns cover?

**Pre-registered 21:48Z, before any new engine run on these targets.** Gap G2. Long Table, 21:47Z: on aee20e3b, Opus's
main line gives t* = 1/5 on one engine (d065b212; Studio checking). The dual has 4 rows: receiver d = 7
7765556/6575765 (2/5) and senders 55757, 55767, 57667 (1/5 each), in their s13 contexts. 3 cores. Round 47's 58778
ring 15-16 run is cancelled, since that sender left the dual.
- **Receiver.** RSST containment (round 44's 582) misses it. It is a sibling of round 47 B's 7765556/6575766 (only s6
  differs). Of its 944 windows at ring <= 14, 738 have the same names as windows already run there. **Known before
  running:** 20 of those are two-engine kills, the smallest at ring 10 (a7_u...5556_...576., which does not use s6).
  The other 206 windows run now (win45.py/drive45.py as round 47). Hypothesis: it dies at ring <= 14 (already met);
  kill line: it does not.
- **Senders, cert_s13 contexts.** All three sit in that receiver: 55767 at w3, 55757 at w4, 57667 at w5. `ctx47.py`-style
  read-off of kills that contain each wheel.
- **Senders, all one-ring contexts (Long Table: report the fraction covered).** As round 46 B (grow46.py): each word's
  2-ball with free ring-2 letters 5..9, and the fraction of fillings in which a verified RSST configuration appears.
  Guess: about 50-70% covered, and none of the fillings with all ring-2 letters >= 7.
- **Then.** Resume round 47 B's d = 9 row (756 of 2212 run, 6 C kills at ring 13 so far).

**Result, receiver and cert_s13 contexts (21:52Z; 944 of 944 windows, 0 mismatches).** Hypothesis confirmed.
- d = 7 7765556/6575765: 46 two-engine kills (28 D, 18 C), first at ring 10. Minimal: f7_...5556_...576. (D, ring 10,
  m 8; it also kills the sibling 7765556/6575766) and f7_5556776_...5.5. (D, ring 13).
- Senders in this row: 55767 at w3 has a wheel-containing kill at ring 12 (D); 55757 at w4 and 57667 at w5 both have
  one at ring 10 (D, the same window).
- Round 47 B, the two d = 7 relay rows (complete): 7765556/6575766 has 27 kills, minimal f7_...5556_...576. (D, ring
  10). 7766556/6566575 has 4 kills, minimal f7_.556776_.5.5.5. (C, ring 14) and f7_5566776_...5.5. (D, ring 14).
- Twoeng-ready: `loop/k47/r7c_kills*`, `r7b1_kills*` and `r7b2_kills*`.

**Result, senders' one-ring contexts (21:52Z; `loop/k46/grow46_<word>.txt`).** Guess about right (55757 is above the
range). Covered = some verified RSST configuration appears in the sender's 2-ball:
- 55767: 69.4% of 9.77M fillings covered. Of the fillings with no 5 in ring 2, 0.8% are covered; of those with every
  ring-2 letter >= 7, 0%.
- 55757: 77.3% of 1.95M covered; no-5 fillings 11.7%; all >= 7, 0%.
- 57667: 62.8% of 48.8M covered; no-5 fillings 3.7%; all >= 7, 0%.
- So, as for round 46's pair: most contexts with a 5 in ring 2 die (78%, 87% and 68%), and almost none without one. These
  sender rows stay; a rule has to pay for a sender whose second ring has no 5.

## Round 47 (18 Oct 2026, 21:03Z-): H-R29, do the two receivers of the 2/9 dual die inside their 1.5-balls?

**Pre-registered 21:03Z, before any engine run.** Gap G2. Long Table, 21:02Z: on the round 44/45 registry Opus gets
t* = 2/9 on one engine (f1a052b4; Studio checking). Every row of the 11/47 dual is killed. The new dual has 6 rows:
receivers d = 7 8655675/5756585 (2/9) and d = 8 75576556/78756665 (1/9), and senders 55667, 56668 (2/9), 55767,
58778 (1/9). Receivers first, at ring <= 14. 3 cores.
- **RSST check first (done at 21:03Z).** Round 44's eligible patterns miss both rows. The d = 7 row holds only a
  broad-only RSST configuration (rsst115, 5675..._.5.....), which stays out.
- **Windows.** win45.py at ring <= 14: 923 windows for the d = 7 row, 1189 for the d = 8 row (`loop/k47/`). Ring 15-16
  (371 and 1089 more) only if a row has no kill at ring <= 14. Engines and naming as round 45 (drive45.py STOP=0,
  minkill45.py with the w_i rule).
- **Hypothesis and kill line (Long Table's).** At least one of the two rows has a two-engine D/C kill at ring <= 14.
  Kill line: neither does.
- **Guess.** Both die at ring <= 14 (about 75% each), as every receiver since round 43 has.
- **Then.** The four senders in their cert_s9 contexts, as round 46 part A.
- **Part B (added 21:04Z, before any part-B run).** Long Table, 21:03Z: Opus's 6-relay class on the same registry gives
  217/1129 (about 0.192) on one engine (0de80394), with different receivers. They matter if the relay becomes the main
  line: d = 7 7765556/6575766 (0.149) and 7766556/6566575 (0.140), and d = 9 656565665/665666566 (0.035). Round 44's
  eligible patterns miss all three. Windows at ring <= 14: 816, 899 and 2212. Same engines, hypothesis (at least one
  row dies at ring <= 14) and kill line (none does). They run after part A's two rows. Guess: the two d = 7 rows die
  (about 70% each). The d = 9 row is less likely (about 50%), since it has only four fives, none adjacent.
- **Senders.** All seven cert_s9 sender contexts sit inside part A's two rows (55767 at w2 and 55667 at w3 of the
  d = 7 row; 58778 at w6 of it and at w1, w2 of the d = 8 row; 56668 at w5, w6 of the d = 8 row). So part A's sweep
  covers them, and `ctx47.py` reads off kills that contain each wheel. A 58778 wheel alone has ring 15, so it has no
  window at ring <= 14. Its contexts need ring 15-16 windows, which run last.

**Result part A (21:29Z; both rows complete at ring <= 14, 0 incomplete, 0 mismatches).** Hypothesis confirmed; guess
right for both rows.
- d = 7 8655675/5756585: 74 two-engine kills (37 D, 37 C), 71 f-names, first at ring 11. The 4 minimal are all C:
  f7_..55675_....5.. (ring 11), f7_..55685_....55. (12), f7_...5675_....58. (14) and f7_..56758_...5... (14).
- d = 8 75576556/78756665: 21 kills (15 D, 6 C), 11 f-names, first at ring 13. The 3 minimal f-names are
  f8_...55675_...665.. (C, ring 13), f8_..576556_...5.66. (D, 14) and f8_55675576_..5...5. (D, 14).
- Senders (`ctx47.py`): 55767 at w2 dies to a wheel window at ring 13 (D), 55667 at w3 at ring 11 (D), and 56668 at
  w5 and w6 at ring 13 (C). 58778 has no wheel window at ring <= 14 (its wheel alone has ring 15).
- Twoeng-ready: `loop/k47/r7a_kills*.txt` and `r8a_kills*` (twoeng scratch run on loop/k47/*: D 43, C 39, X mismatch 0).

## Round 46 (18 Oct 2026, 20:51Z-): H-SEND, do the two senders carrying 11/47 die to windows around them?

**Pre-registered 20:51Z, before any engine run.** Gap G2. Long Table, 20:44Z: the no-T 11/47 dual (cert_s7.json, Opus
fa4705f2, second engine Studio) rests mostly on two sender rows, 55677 (8/47) and 56687 (6/47). 3 cores.
- **Part A (Long Table's task).** The senders' contexts in cert_s7: every receiver row of cert_s7 with a 5 at w_i whose
  link word is 55677 or 56687. There are 14 contexts in 7 receivers (all 7 receivers except 8567655/6655656). Windows:
  win45.py windows of those rows at ring <= 14 that contain the whole sender wheel (u, w_i-1, w_i, w_i+1, s_i-1, s_i).
  That gives 1039 distinct windows, ring 10-14 (`loop/k46/ctx46_A.txt`, `ctx46_A.map`). Engines as round 45
  (drive45.py, STOP=0).
- **Hypothesis and kill line (Long Table's).** At least one sender context in cert_s7 has a two-engine D/C kill at ring
  <= 14. Kill line: none does. **Known before running:** round 45's kill f7_..55855_..6666. (D, ring 13) holds the
  56687 wheel at w1 of 8558655/6665666. So for 56687 the hypothesis is already met in one context. The open part is
  how many of the 14 contexts die, and whether 55677 dies in any.
- **Part B (added).** The sender row is one word for every context, so a kill in some contexts does not remove it. Only
  a death in every context does. One ring of growth, as round 42: the sender's 2-ball (centre 5, its link, a ring 2 of
  10 slots for 55677 and 12 for 56687, letters 5..9 with 9 = at least 9, fresh third ring). Count the fillings in which
  one of round 44's 582 verified RSST configurations appears (RSST appearance, as round 42). Report the survivors.
- **Guess.** A: 10 or more of the 14 contexts have a kill that contains the wheel. B: survivors exist for both words,
  mainly with big ring-2 letters (as R* in round 42). If so, patterns cannot remove the sender rows, and the relay
  rule has to carry them.

**Result (21:03Z; part A stopped at 813 of 1039 windows when Long Table moved the targets: on the round 44/45
registry, 55677 and 56687 no longer bind).**
- **A.** Hypothesis confirmed; guess right. All 14 contexts have a two-engine kill that contains the sender wheel. The
  smallest kills are at ring 10 (7557565/6566666, 7565765/6855555 w6), 11, 12 (both d = 8 75657565 rows) and 13
  (8558655/6665666, 76565565/57765865). Per-context counts: `loop/k46/sum46.txt`.
- **B.** Guess right. One ring out, the 582 verified RSST configurations leave 31.4% of 55677's 9.77M fillings and
  52.6% of 56687's 244M. Every filling with all ring-2 letters >= 7 survives, for both words. So patterns alone cannot
  remove a sender row. A sender in an all-big ring 2 has to be paid for by a rule.

## Round 45 (18 Oct 2026, 20:17Z-): H-TOP, does the top dual row die to one of our own windows inside its 1.5-ball?

**Target changed 20:22Z, still before any engine run.** Long Table (20:12Z, read 20:22Z) replaced the 9 rows: Opus's solve
with rule T + L2 + rsstD + the full k43 batch gives t* = 11/47 on one engine (Studio checking at bbd46d73), and the
binding receivers are d = 7 7565765/6855555 (4/47); d = 7 8566655/6656656, 7557565/6566666, 8558655/6665666,
7557656/6565665 and d = 8 76565565/57765865 (2/47 each); d = 8 75657565 with 66656665 and with 55655565 (1/47 each).
Round 44 B's preview hits 7 of the 8 with configurations kc already calls D or C; it misses only d = 7
8558655/6665666. That row is this round's target (ring <= 14: 1029 windows; ring 15-16: 494 more). Bars, engines and
kill line as below; 8556855/7565666 is dropped. Guess unchanged (no kill at ring <= 14, about 70%).

**Pre-registered 20:17Z, before any engine run.** Gap G2. Long Table, 19:59Z: the next kill-sweep targets are the 9
receiver rows of Opus's cert_s6.json (t* = 5/21, 9a914f8c), by dual weight, ring <= 14 first. Round 44 part B's preview
(below) hits 8 of the 9 rows by RSST containment; the one it misses is the top row. 3 cores.
- **Target.** d = 7, link 8556855, s 7565666 (dual weight 0.0635, the largest receiver row). If round 44's two-engine
  filter leaves any other of the 9 rows with no eligible containment hit, that row joins this round in weight order.
- **Windows.** `loop/k45/win45.py` (round 43's win43.py for any row): every connected induced subset of the 15 fixed
  vertices (u, w_i, s_i) at exact degrees, simple ring. Ring <= 14: 927 windows; ring 15-16: 324 more, run only if
  ring <= 14 has no kill. One change from round 43: a window holding s_(i-1) and s_i states w_i's 5-ness in its name
  (F/N), because s_(i-1)-s_i is an edge iff w_i = 5 (see round 44's finding on round 43's names).
- **Engines.** `loop/k45/drive45.py` (copy of drive43.py), STOP=0: kc -C on every window; kc D goes to dfast; kc C goes
  to cfast `--fixed` with kc's X. A kill is D on both engines or C with that shared conservative X. Kills get f-names
  and twoeng-ready files as in round 43 (minkill.py), with the w_i fix.
- **Hypothesis and kill line.** Long Table's: at least one row has a D/C configuration at ring <= 14; kill line: none
  of the 9 does. Round 44 B answers this for 8 rows (pending its two-engine filter); this round answers it for the
  top row. Kill line for the top row: no window at ring <= 16 is a two-engine kill.
- **Guess.** No kill at ring <= 14 (about 70%). RSST containment misses the row in the 1.5-ball, and round 43's
  minimal kills were all RSST-like windows. If it survives, RSST's own route needs vertices past s (privates), which a
  receiver row cannot state, so the row has to be paid for by a rule, not forbidden.

**Result (20:41Z; ring <= 14 complete, 1029 windows, 0 incomplete, 0 mismatches).** Guess wrong; the row dies inside its
1.5-ball. Ring 15-16 not run (a kill exists at ring <= 14).
- 13 two-engine kills (12 distinct f-names), all D on kc and dfast, first at ring 13. Two are inclusion-minimal, both D at ring 13:
  f7_..55855_..6666. (m 10) and f7_..55865_..665.. (m 9). Neither is an RSST containment (round 44 B misses this row).
- The same kills also hit the 19:59Z top row d = 7 8556855/7565666, which RSST containment missed too. So all 9 rows
  of the 19:59Z list and all 8 of the 20:12Z list now have a two-engine kill at ring <= 14.
- Twoeng-ready files: `loop/k45/kills.txt`, `kills_kc.out`, `kills_df.out` (twoeng scratch run: D 12, mismatch 0).

## Round 44 part B (20:17Z): RSST containment patterns for d = 7..11 (Long Table, 20:00Z)

**Set by Long Table at 20:00Z; written into this log at 20:17Z, after a preview run at 20:13Z on all 633 configurations
(before the two-engine filter).** Hypothesis: the RSST C set (kc -C plus cfast `--fixed` with a conservative X) kills at
least one of the 9 cert_s6 rows. Kill line: none of the 9 rows is hit. Broad-only configurations are kept out.
- **Method.** `loop/k44/gen44.py`: round 42's embedding code on the 1.5-ball the LP's rows describe (u, w_i, s_i;
  s_(i-1)-s_i an edge iff w_i = 5), exact degrees (u = d, w/s 5..8), induced, interior triangles onto faces. Each
  embedding gives a pattern (d, slot letter sets) in wlp3's NF form (slot w_i = i, s_i = d + i), including w_i's
  5-ness when both s_(i-1) and s_i are used. Dihedral images identified; implied patterns dropped.
- **Sanity checks (preview).** The round-43 binder row d = 8 85556565/65866655 is hit by RSST 7322.126 (as round 43
  found on two engines). R*'s 16 fillings are not hit (as rounds 41-42 found).
- **Preview (all 633, before the filter).** 413 patterns (d = 7: 167, 8: 150, 9: 63, 10: 21, 11: 11), from 341
  configurations. 8 of the 9 rows are hit; the top row, d = 7 8556855/7565666, is not.

**Result part A (20:34Z).** No kill line crossed: 0 mismatches. `loop/k44/rsst_verdicts.txt`:
- **D2: 249**, D on kc and on dfast. This is exactly the set RSST labels D (no contraction).
- **C2cons: 333**, C on kc -C with a conservative X that cfast `--fixed` accepts with leftover 0 (333 of 333 kc X's
  accepted).
- **None: 51**, all labelled C by RSST (ring 8-14). kc -C exhausts every conservative X of size <= 4 on each.
  Diagnostics on all 51 (`rsst_verdicts_C2.txt`, not registry; finished 20:44Z): RSST's own X is not
  conservative-admissible on kc (adm=no, 51 of 51), and it is C on kc -C2 broad and on cfast `--fixed` with RSST's X
  (51 of 51). All 51 are broad-only on both engines, as guessed. The cfast `--search` column was not run.
- So 582 of 633 (92%) are registry-eligible on our two engines (guess: about 85% of the C ones; actual 333/384 = 87%).

**Result part B (20:34Z).** Hypothesis confirmed.
- **Patterns.** From the 582 eligible configurations: 377 inclusion-minimal patterns (d = 7: 153, 8: 136, 9: 57,
  10: 20, 11: 11), in `loop/k44/pats44.txt` (NF lines `d k slot mask ...` plus a readable form and the source configs).
- **Windows.** `mkf44.py` writes 377 f-names (a not-5 w_i is written as both 6 and B), each with the window cut at the
  embedding from a representative 2-ball. All 377 cuts have the source configuration's ring and interior size. On
  `drive44.py` (kc -C, dfast, cfast `--fixed` with kc's X), all 377 are two-engine kills: 196 D and 181 C, with no
  mismatch. Job 30's twoeng.py, run in a scratch copy on `loop/k44/*`, loads all 377 (D 196, C 181, X mismatch 0).
- **Rows.** Long Table's 9 rows (19:59Z): 8 hit, all but d = 7 8556855/7565666. Long Table's 8 new rows (20:12Z,
  t* = 11/47): 7 hit, all but d = 7 8558655/6665666, which goes to round 45. On each hit row, every hitting
  configuration is D2 or C2cons.
- **Side finding.** Round 43 named 16 windows that held s_(i-1) and s_i but not w_i (= 8 in the row) with w_i left
  free. Those names also matched rows with w_i = 5, where s_(i-1)-s_i is an edge and the window does not appear.
  All 16 are implied by sound registry names (checked on main's twoeng output). Each one's corrected name (w_i = 8
  stated) is already a two-engine kill. They are removed from `loop/k43/kills*` (`kills_drop44.txt`), and win45.py and
  gen44.py state w_i in that case. No bound is affected.
- **Note for the LP.** Main's twoeng output already forbids 3 of the 19:59Z d = 8 rows: 85556565/66866665 by
  f8_...55565_........, and 75656575/56665555 and 76556565/58565765 by f8_...56565_......... So cert_s6 predates the
  full k43 batch, which fits Long Table's 20:12Z note.

## Round 44 (18 Oct 2026, 20:00Z-): H-RC, which RSST configurations are reducible on our two engines with a conservative X?

**Pre-registered 20:00Z, before any run.** Gap G2. Follows round 43: the 1/4 binder died to RSST 7322.126, a C
configuration, while the LP registry has only RSST's D ones (Studio rsstD). 3 cores. Long Table told at 20:00Z, and may
redirect.
- **Set.** All 633 configurations of `studiointel/routeb/rsst/unavoidable.conf`, ring 6-14, written as kc/dfast lines
  (`loop/k44/rsst2kc.py`). RSST's labels: 249 with no contraction (D), 384 with a contraction of 1-4 edges (C).
- **Engines.** kc -C (D, then conservative C) and dfast on all. For a kc C, cfast `--fixed` with kc's X. For any
  configuration kc -C leaves not C: kc broad (kcc2 -C2), cfast `--search`, and cfast `--fixed` with RSST's own
  contraction set.
- **Output.** A table `loop/k44/rsst_verdicts.txt`: per configuration, RSST label; kc/dfast D; conservative C (with the
  shared X); broad-only C; or neither.
- **Bars and kill line.** Any configuration RSST labels D that kc or dfast calls not D, or any kc/dfast D mismatch, is
  reported first. That would mean a ring-order or format bug in the conversion, or an engine bug.
- **Guess.** All 249 D agree on both engines. Of the 384 C, about 85% are conservative on both engines. The rest
  (contractions with two ring vertices in one component, like 2.126 and 126.8168 in round 42) are broad only.

## Round 43 (18 Oct 2026, 19:35Z-): H-D8, is the new 1/4 binder (d = 8 85556565/65866655) reducible inside its patch or one ring out? (Long Table, 19:33Z)

**Pre-registered 19:35Z, before any run.** Gap G2. Top priority, ahead of part C's R* queue (its driver died with the
container, at 37 of 106 ring-17 windows). 3 cores.
- **Why.** The K = 2 bound is t* = 1/4 [E2] (Studio d64c8442, Opus b5e6763d). Certificate: 1/4 receiver d = 8 u,
  link w0..w7 = 85556565, s 65866655 (s_i between w_i and w_i+1), plus senders 55688 (w1, w7), 66668 (w5), 55858
  (w2), 58668 (w3). Every letter of u's row is exact and every s-slot touches a five, so any window inside the patch
  kills the whole row. No RSST-D pattern forbids it (Opus).
- **Part A (inside the patch).** Every connected induced subset of the 17 fixed vertices (u, w0-w7, s0-s7) at exact
  degrees, the rest free ring (`loop/k43/win43.py`). That gives 2,229 windows with a simple ring <= 17: ring 6-14:
  1,671, 15: 393, 16: 135, 17: 30. Run kc -C (D, then conservative C) in ring order, fives-heavy first within a
  ring, on 3 cores. A kc D needs dfast/dfast18 too, and a kc C needs cfast `--fixed` with kc's X (leftover 0). The
  round stops at the first two-engine kill.
- **Part B (one ring out).** The privates of the non-5 link vertices: three at w0 (8), one at w4 (6), one at w6 (6),
  each 5..9+, so 3,125 cases. Run round 42's containment (RSST 633 + explore's twoeng kills), then windows with the
  surviving privates as interior for the five-heavy survivors.
- **Bars.** A two-engine kill in A forbids the row [E2], and the LP must be re-solved. B kills the row only if every
  private case dies. Long Table's kill line: no D and no conservative C to ring 16 on the patch plus one ring.
- **Guess.** No kill in A. Opus found no RSST-D containment, and the 8 at w0 next to two fives (w1, w7) gives large
  rings. B: private fives at w0 die often (an 8 between fives), but the all-big privates survive, as at R*.

**Round 43 part A, first kill (19:40Z): the binder row is C-reducible at ring 10, on two engines with a conservative X.**
- Window `f8_...55565_...5....` (my name `a8_u.55565.._.5......`): u (8) + w1..w5 (5, 5, 5, 6, 5) + s1 (5). Ring 10,
  m = 7. kc -C: C with X = {I0-I1} = the single interior edge u-w1 (the 8 to its five). cfast `--fixed I0-I1`: C,
  leftover 0. cfast `--search` also finds its own X ({R0-I0,R2-I0,I0-I2,I0-I4}, leftover 0). Not D on either engine
  (kc and dfast agree: ext 575, reached 2,177 of 2,461). Files: `loop/k43/kills.txt`, `kills_kc.out`, `kills_cf.cfast`
  (f-names, twoeng-ready); raw `A_kcc.out`, `A_cf.out`.
- Every letter of the window is one of the row's exact letters, so the row 85556565/65866655 is forbidden [E2]. It
  fixes w1-w5 and s1 only, so the five-slot encoding would drop it. It needs Job 30's link-word + non-five-slot
  pattern type, as the dropped list did.
- It was the 96th window (ring 10). Guess "no kill in A" was wrong.
- **Amendment (19:40Z, before more runs):** the remaining ring <= 14 windows run on with STOP=0, with every kill recorded,
  so that Studio gets a batch of d = 8 patterns for the re-solve instead of one. Part B is dropped, since the row is
  already dead.

**Round 43 result (19:59Z): 383 of the 1,671 sub-patch windows at ring <= 14 kill the row on two engines (184 D, 199
C with a conservative X), and 7 of them are inclusion-minimal** (`loop/k43/KILL`, `kills_min.txt`; twoeng-ready
`kills.txt`, `kills_kc.out`, `kills_df.out`, `kills_cf.cfast` with 382 distinct f-names). There were 0 kc/dfast
mismatches, and cfast accepted kc's X on every kc C.
- By ring (D / C / neither): 6-9: 0/0/90; 10: 0/2/90; 11: 12/13/221; 12: 59/36/280; 13: 70/55/332; 14: 43/93/275.
- Minimal kills:
  - `f8_...55565_........`, ring 10, m 6: the 8 with consecutive neighbours 5,5,5,6,5 and nothing else. C, X = u-w1.
    This is exactly RSST 7322.126 (checked: centre adjacent to all, path 5,5,5,6,5). Its mirror 5,5,6,5,5 is RSST
    7326.122.
  - `f8_...56565_........` (ring 11, C).
  - D at ring 11-12: `f8_.555.565_......5.`, `f8_...55585_....565.`, `f8_...55656_.....66.`, `f8_...55856_...5655.`.
  - `f8_.5558565_......6.` (ring 14, C).
- **Reading [I].** The 1/4 binder is an RSST C configuration. The registry has only RSST's D configurations (Studio
  rsstD: 158 patterns, Lean-backed D), and those in the five-slot encoding only. RSST's C configurations, checked on
  our two engines with a conservative X and loaded through the non-five-slot pattern type, are the obvious next batch
  for the LP.

## Round 42 (18 Oct 2026, 11:33Z-): H-DEF, does every R* filling die within one ring of growth? (Long Table's target, 11:29Z)

**Pre-registered 11:33Z, before any run.** Gap G2. Option D, round 18's defect-style method, on R*'s 16 open fillings.
2 cores, with part C's ring-17 queue on the third.
- **Growth.** One ring beyond R's patch: the six privates of the non-5 link vertices (p1 of w1, p2a/p2b of w2,
  p4a/p4b of w4, p5 of w5), each in {5, 6, 7, 8, 9+}. That gives 16 x 5^6 = 250,000 closed cases. Each case is u's
  2-ball at exact degrees (u, w0-w6, s0-s6, the six privates; `gen.build` with fresh third-ring vertices), with 9+
  never matched as an exact degree.
- **Forbidden set.** RSST's 633 configurations (`studiointel/routeb/rsst/unavoidable.conf`), plus explore's
  two-engine D/C windows (rounds 37-38's six w2-frame kills, and Job 30's `k3x_D.out` / `k3x_C.cfast` where their input
  lines are on disk).
- **Containment.** My own code (`loop/k42/`, extending `loop/d3/d3_rsst.py`). An injective map of the configuration's
  interior into the 2-ball's 21 exact-degree vertices, with exact degrees, induced, and interior triangles onto faces.
  Embeddings are enumerated once on the 2-ball's fixed structure, as degree requirements on the variable slots.
- **Checking.** Every configuration that kills a case is cut from the patch and checked by kc (D) or kc -C conservative
  (C), plus dfast or cfast `--search`. A case counts as dead only on two engines.
- **Bars and kill line.** Long Table's hypothesis is that all 16 fillings die within this ring. Any filling with a
  surviving closed case kills it. Survivors are reported, grouped by which privates are at 5/6, and the all-big ones go
  to new u-centred windows next (Opus's step ii).
- **Guess.** The hypothesis dies. Opus's `F_free_slots` found every RSST hit needs a private at 5 or 6, and round 39's
  p5 = 7 windows are not D/C, so at least the 3^6 = 729 cases per filling with every private in {7, 8, 9+} survive. I
  expect about 2,000 survivors per filling, with RSST killing most cases that have a private five.

**Round 42 result (11:42Z): the hypothesis dies. Every one of the 16 fillings keeps surviving closed cases after one ring
of growth: 160,552 of 250,000 cases survive under conservative two-engine kills, and 134,232 if broad-X kills count**
(`loop/k42/grow.py`, `tally.py`, `cases_cons.txt`, `hits.txt`).
- **Structure.** The 2-ball has 21 exact-degree vertices, 47 edges and 27 faces among them, the same for every letter
  choice (checked on 3). Of the 645 configurations (633 RSST + 12 explore), 15 embed with a requirement that does not
  put a 5 at s1/s4. That gives 19 requirement patterns.
- **Two engines on every killer.** Each (configuration, image) was cut from a representative 2-ball (24 windows, ring
  8-14; every RSST cut has RSST's own ring size). RSST 2.3701166 (ring 12) is D on kc and dfast. The other 23 are C
  on cfast `--search`. For 20 of them, kc -C finds a conservative X that cfast `--fixed` accepts with leftover 0
  (`cut_kcc.out`, `cut.cfast`, `cut_fixedkc.cfast`). The other 3 are RSST 2.126 (ring 8) and 126.8168 in both
  orientations. Those are C only with a broad X on both engines (kc -C2 and cfast agree; 2.126's X is RSST's own four
  ring-to-interior edges).
- **What one ring forces** (conservative; privates p1 at w1, p2a/p2b at w2 next to s1/s2, p4a/p4b at w4 next to s3/s4,
  p5 at w5):
  - p5 = 5 always dies (RSST 122.126, ring 9).
  - p1 = 5 dies only by the broad 2.126. Conservatively it dies only with s1 = 7 and p2a = 5 (2.504980).
  - s1 = 6 forces p1 >= 7, p2a >= 6 and (p2a, p2b) != (6, 5). s4 = 6 forces p4b >= 6 and (p4a, p4b) != (5, 6).
    These come from RSST 2.211701966, 122.1031, 126.61686/126.490086, and rounds 37-38's two w2-frame kills.
  - Everything else survives, including all 3^6 = 729 cases per filling with every private >= 7.
- **Survivors per filling (conservative):** 66: 4,332; 67-69: 5,700; 76: 9,120; 77-79: 12,000; 86 and 96: 9,500;
  87-89 and 97-99: 12,500.
- **Next binder candidates, as Long Table asked.** The most five-heavy survivors:
  - (9,9) with privates 55555x (every private a 5 except p5 >= 6).
  - (7,7) with 565556.
  - (6,6) with 775576.
  These are where new windows (Opus's step ii: R* plus the privates as interior) are most likely to bite.
- Against the bar and guess: the kill line fired on all 16 fillings. Guess "about 2,000 survivors per filling" was low.
  Containment kills far less than guessed, because only 15 of 645 configurations reach a private at all.

## Round 41 (18 Oct 2026, 10:26Z-): H-SUBC, does the C stage kill any of R*'s 16 open fillings at a window inside R's patch that is not u + all link?

**Pre-registered 10:26Z, before any run.** Gap G2, part C continued (coordinator's order, 10:14Z: round 39, then the 16
open fillings). 2 cores, in place of part C's ring-17 queue, which resumes after.
- **Why.** Opus's `C_kc_ring17` (`f_all.txt`, branch claude/project-thread-7uelj0, commit e2b0ea90) lists every
  connected induced subset of R's 15 fixed vertices with s1, s4 at 6-8 (9+ left as ring), excluding round 34's u + all
  link windows: 2,780 at ring 6-18. Opus ran kc D only on 1,131 of them at ring <= 16, all not D for the 16 fillings.
  None has had a C stage. kc -C adds it at a few seconds per window at ring <= 15.
- **Run.** `loop/k34/fill3.txt` = Opus's 1,383 windows at ring <= 15 + round 34's fillwin windows, in ring order, through
  part C's own driver (`drive.py`, NW=2), which skips windows already run. Coverage by name: s1 and s4 at '.' cover every
  letter, a letter covers itself. Same engine rules as part C: a kc D needs dfast, every 4th not-D window at ring <= 16 also
  gets dfast, and a kc-C C goes to cfast `--search` before it counts.
- **Bars.** Any C covering a filling with s1, s4 >= 6 kills it on one engine, and goes to cfast and to the coordinator as a
  kill line. 0 C: windows inside R's patch are exhausted for D and C at ring <= 15, and the 16 fillings need vertices
  outside the patch (Opus's reading).
- **Kill line.** A kc/dfast D mismatch, or a kc-C C that cfast calls not C.
- **Guess.** 0 C. Most of these windows have 2-6 interior vertices, and part C's u + all link windows got 0 C for the
  16 at ring 13-16 (best leftover 96).

**Round 41 result (11:28Z): no kill. All 1,383 sub-patch windows at ring 6-15 are not D and not C, so the 16 open
fillings stay open** (`loop/k34/fill_kcc.out`, names `x7_*`; `fillings.txt` still reads 9 of 25 killed, all D2).
- By ring: 6-12: 399, 13: 243, 14: 327, 15: 414. That is every window in Opus's `f_all.txt` at ring <= 15, so Opus's
  156 of 414 at ring 15 is now complete for D as well as C.
- dfast ran on 347 of them (every 4th not-D window) and agrees with kc on all 347, with 0 mismatches.
- Closest to C, as leftover over ext, is about 0.8% at ring 14-15: `x7_u5675..5_667...5` (ring 14, leftover 150) and
  `x7_u5675.65_6...7.5` (ring 15, leftover 320). Both are the u + w0-w3 + w6 + s0/s6 corner around the w0 and w6 fives.
- Against the bars: 0 C, so windows inside R's patch are exhausted for D and C at ring <= 15 (and for u + all link
  windows to ring 16, part C). The 16 fillings need vertices outside the patch, which matches Opus's reading. Guess
  "0 C" was right.
- Ran 10:27-11:27Z, on 2 cores to 10:59Z and 3 after round 39 stopped. The same driver now continues part C's
  u + all link queue at ring 17 on 3 cores.
- Part C status (13:43Z): 35 of 106 ring-17 u + all link windows are done on 1 core. None is D or C, so still 9 of 25
  fillings are killed. The best ring-17 leftover is 1,340. There are no kc/dfast mismatches. Long Table keeps it on one core
  until Job 30 run A's binders arrive.

## Round 40 (18 Oct 2026, 10:14Z-): H-C2V, does kc -C2 agree with cfast on X's with two ring vertices in a component? (Long Table, 10:12Z)

**Pre-registered 10:14Z, before any run.** Round 38's kills 2, 4 and 5 rest on such an X. Short validation; round 39's
core is paused for it.
- **Set** (`loop/kcc/mkval2.py 15`, fixed rule). Every registry cfast output (40 files; round 37/38's own kill files
  excluded). Keep a configuration if it is not D, cfast's working X (C) or best X (not C) has a component holding two
  or more ring vertices, its input line is in the wheeldis *.txt files, and its ring is <= 15. That gives 1,534:
  132 C and 1,402 not C, rings 8-15. All 132 C run, plus every 4th not-C in ring order.
- **Test.** kc -C2 -x with cfast's X. Pass on a configuration: kc admits the X, and kc's exact leftover equals
  cfast's (0 for C). Also reported: kc -C2's own C/not-C verdict against cfast's.
- **Kill line.** Any leftover mismatch, or a kc -C2 C where cfast says not C, that survives a recheck. Then kc broad
  mode is not trusted, and round 38's kills 2, 4 and 5 stay single-engine [E1].
- **Guess.** 0 mismatches. A few cfast X's are inadmissible for kc -C2 (its distance-4 rule is stricter), and those
  are reported, not counted as mismatches.

**Round 40 result (10:19Z): passes, with 0 mismatches on 483 configurations** (`loop/kcc/val2_run.txt`, `val2_kcc2.txt`).
- Leftover equal on all 132 C, which is leftover 0 with cfast's X. Leftover equal on all 351 not-C, with cfast's best X.
- kc -C2 admits every one of cfast's 483 X's, each with two or more ring vertices in one component. The guess "a few
  inadmissible" was wrong: none were.
- kc -C2's own verdict matches cfast's on all 483: 132 C / 351 not C.
- So kc broad mode agrees with cfast on this X shape. Separately, Studio re-ran cfast with kc's conservative X fixed
  on round 38's kills 2, 4 and 5 (Studio commit 361ad2dc): all C, leftover 0. All six round 37-38 kills are therefore
  conservative two-engine C.
- Process note: the pause missed. The dfast job I meant to stop had already exited, so this ran 4 minutes on a 4th
  core alongside round 39.

## Round 39 (18 Oct 2026, 09:55Z-): H-P5, does p5 = 7 make R* reducible? (Opus's fourth floor arrangement)

**Pre-registered 09:55Z, before any run.** Gap G2. 1 core, after round 38 stops.
- **Why.** Opus's 11/71 floor (`loop/opus/H_floor_check`) needs w6's sender row with z-letters (w4, p5) = (7, 7).
  There, w6's two rootings (at u and at s5) share one variable, so u still pays (1 - t)/2 - T6. If R* with p5 = 7 is
  reducible, the adversary must pick p5 != 7. The two rootings then split, and that floor no longer holds as
  stated.
- **Windows** (`loop/k39/p5win.py`). u + all seven link vertices + any subset of {s0, s2, s3, s5, s6} at R's letters,
  + s1 and s4 each absent or at 6-8, + p5 = 7 (w5's second-ring neighbour between s4 and s5). 77 windows have a
  simple ring <= 18: ring 16: 10, 17: 19, 18: 48. Five of the ring-16 windows cover all 16 open fillings and five
  cover 4 each. At ring 17, 2 cover all 16, 12 cover 4 and 5 cover 1.
- **Engines.** kc -C in ring order. A D needs dfast too, and a C needs cfast `--search` too. Ring 16 first, then
  ring 17 for as long as the round lasts.
- **Bars.** A kill covering (6,6) breaks the 11/71 floor as stated. A kill covering all 16 fillings with p5 = 7
  makes every rule-T bound through w6 use split rootings. No kill: the fourth arrangement stands at ring <= 16 (17).
- **Kill line.** kc/dfast D mismatch, or a kc-C C that cfast calls not C.
- **Guess.** No kill at ring 16. p5 = 7 adds a big vertex at the edge of the window, and big vertices rarely help
  reducibility.

**Round 39 result (10:59Z): no kill. 0 of 16 windows are D or C at ring 16-17, so 0 of 16 fillings die with p5 = 7**
(`loop/k39/fill_kcc.out`, `targets.txt`). The round stopped at its cap after 16 of the 29 windows at ring <= 17.
- Ring 16: all 10 windows. Ring 17: 6 of 19, including both ring-17 windows that cover all 16 fillings
  (`qb2582f426debb95f`, `qe471d5d905b19648`, leftover 14,400 and 10,142). The other 4 cover 4 fillings each.
- Best leftover is 608 at ring 16 (`q837e5a91adbd7029`). Ring 17 leftovers are 1,920 to 14,400.
- dfast agrees with kc on all 3 windows it ran (classes, ext and reached are equal).
- Against the bars: no kill, so Opus's fourth arrangement (w6's rootings sharing one variable at p5 = 7) stands at
  ring <= 16, and at ring 17 for every window that covers (6,6). Guess "no kill at ring 16" was right.
- Not run: 13 ring-17 windows covering 1-4 fillings each, and the 48 at ring 18.

**Round 39 interim (10:26Z): ring 16 is 0 of 10 windows D or C, so 0 of 16 fillings die with p5 = 7 at ring 16.** Best
leftover 608 (`q837e5a91adbd7029`). dfast agrees with kc on the 3 windows it ran (reached 230,668, 198,006 and
659,330). Ring 17 continues on 1 core to the round's cap.

## Round 38 (18 Oct 2026, 09:52Z-): H-W38, how far does w2's cap climb if its binding frames are killed one by one?

**Pre-registered 09:52Z, before any code.** Gap G2. 1 core, beside part C.
- **Why.** Round 37 killed link 7665575 at w2 with one ring-13 window. The cap then sits at the next frame
  (0.1852, link 7665675). If frames keep dying cheaply, w2/w4 stop limiting Rule T or the L2 transfer.
- **Loop.** Start from round 36's 62,140 w2 arrangements (`k36/rows_w2.txt`) minus round 37's kill. Each step:
  1. Find the binding frame, argmin over surviving rows of (34/27 - yload)/k.
  2. Build its windows: centre w2 + the link vertices around any nonempty subset of its link fives (as gen28's
     variants), or the whole link, + any subset of the s-slots next to them, at the frame's letters (9+ left open).
  3. Run kc -C in ring order up to ring 15, stopping at the first kill. D needs kc + dfast. C needs kc-C + cfast
     `--search`.
  4. A kill removes every surviving row that agrees with the window in the frame's own orientation. Then repeat.
  Stop when a binding frame survives all its windows to ring 15, or after 40 minutes.
- **Report.** The kills in order, each with its window and verdicts. The cap at stop, and R's first-order row
  t >= (0.7 - 2 cap)/2.7. The frame that stops the loop. w4 gets the same numbers, since no window reads s0 or s5.
- **Bars.** Cap >= 0.35 at stop: w2/w4 no longer block t* = 0 through R. Cap stuck at 0.1852: the first frame
  already resists.
- **Kill line.** Any kc/dfast D mismatch, or a kc-C C that cfast calls not C.
- **Guess.** 3-6 frames die, and the loop stops near 0.25 at a frame whose binding fives sit at L3 and L6 with
  big neighbours.

**Round 38 result (10:08Z): 5 more frames die (C on two engines), and w2's cap climbs from 0.1852 to 0.2454**
(`loop/k38/greedy.py`, `greedy.out`, `kills.txt`, `kills.cfast`, `commonx.py`). It ran 85 windows in 12 minutes,
and nothing was D.

| step | binding frame (link / s) | cap | killing window (ring) | rows removed | X common to kc and cfast |
|---|---|---|---|---|---|
| 1 | 7665675 / 5966577 | 0.1852 | f7_5667576_..5.... (14): whole link + s'0 | 625 | yes, conservative |
| 2 | 7696575 / 5556577 | 0.1924 | f7_..65757_..65... (13) | 100 | cfast's X, broad only |
| 3 | 7675675 / 5556577 | 0.1924 | f7_5675767_.5..... (15) | 125 | yes, conservative |
| 4 | 7696575 / 5555577 | 0.1968 | f7_..65757_..55... (12) | 100 | cfast's X, broad only |
| 5 | 7695675 / 5555577 | 0.1968 | f7_..56757_...5... (13) | 250 | cfast's X, broad only |
| 6 | 7696575 / 5555977 | **0.2454** | none at ring <= 15 | - | STOP |

- In steps 2 and 4, kc's own conservative X is the single interior edge {I0-I2}. cfast reports a size-4 X with two ring
  vertices in one component, which kc accepts only under -C2 (leftover 0). kc -x gives the same leftover 0 on both.
- Step 1 kills every w2 frame with link 7665675 (the window fixes only the link and w0). Opus's floor work on that
  frame is therefore moot.
- **Caps after the kills, by filling letter:** s1 = 6: 0.2778 (link 7669675, k = 4). s1 >= 7: 0.2454 (link 76a6575 with a = s1 /
  5555977, k = 3). R's first-order row then gives t >= 0.054 at (6,6), 0.066 at (6, >=7) and 0.078 otherwise.
- The stopping frame has three T inflows (s'0, p, x2 all 5) and yload 0.52, so its slack is not small. It binds only
  because k = 3.
- Against the bars: neither 0.35 nor stuck at 0.1852. Guess check: "3-6 frames die, stop near 0.25" was right (5
  died, stop at 0.245). "Binding fives at L3 and L6" was wrong: the stopping frame's fives are L4 and L6, with three
  s-fives feeding T.
- `kills.cfast` is cfast's own output for the 5 windows, cpat-ready once Job 30's pattern type exists.

## Round 37 (18 Oct 2026, 09:47Z-): H-W37, is w2's worst frame reducible? (coordinator's go, 09:42Z)

**Pre-registered 09:47Z, before any code.** Gap G2. Uses the core freed by the broad C run.
- **Why.** Round 36's cap T_max = 0.1506 at s1 = 6 comes from one link word at w2, 7665575, with s-words
  5.65677, 5.65777, 5.66677, 5.65877 and 5.65977 (bounds 0.151-0.167). The next link word, 7665675, gives
  0.1852, and s1 >= 7 gives 0.1924. Killing those five frames raises the w2/w4 cap to 0.1852. Then the first-order
  R row is t >= 0.122 at (6,6).
- **Windows.** Centre w2 (degree 7), the whole link 7665575 at exact letters, and any subset of the s-slots s'0 = 5,
  s'5 = 7, s'6 = 7, and (x2, x3, x4) taken from the five target patterns (6,5,6), (6,5,7), (6,6,6), (6,5,8),
  (6,5,9+). A 9+ slot can only be left open. Windows are deduplicated under the link's symmetry, built with gen28,
  and run in ring order up to 18.
- **Engines.** kc D, with each D re-run on dfast (ring <= 16) or dfast18. kc -C on every not-D window: a C there is
  one engine, and cfast at Studio is the second.
- **Bars.** All five frames die: the cap at s1 = 6 rises to 0.1852. Only the x3 = 5 frames (the three-five
  triangle) die: the cap rises to 0.1637, the 5.66677 frame. None die: the 0.15 cap stands.
- **Kill line.** Any kc/dfast mismatch.
- **Guess.** The x3 = 5 windows with x2, x4 fixed are D at ring <= 15 (three mutually adjacent fives beside two 6s
  are crowded). The 5.66677 frame is not D but C.

**Round 37 result (09:51Z): all five worst frames are C on two engines, through one ring-13 window**
(`loop/k37/`: `framewin.py`, `drive37.py`, `fill_kcc.out`, `targets.txt`, `cwin.cfast`).
- The driver ran 38 of 799 windows, at rings 11-13, before every target was dead. Nothing is D.
- `f7_5566757_...5...` (ring 13) covers all five targets. It is w2 (degree 7) + its whole link 7665575 + w0 (the
  five at s'0, next to u and w1). It is **C with X = {w2-u} (I0-I1)** on kc-C (conservative; 1 X tested) and on
  cfast (`--search`: same X, leftover 0).
  - Both engines agree on classes 66,430, ext 8,537 and reached 59,788.
  - X is one interior edge, so G/X is loopless and smaller with no global condition.
- `f7_..57556_...65..` (ring 11, 656 only) and `f7_..57556_...66..` (ring 12, 666 only) are also C on both engines.
  kc-C uses X = {I0-I2} (size 1), and cfast's first working X is a size-4 triad set.
- The window fixes none of x2, x3, x4 or p. So it kills every w2 frame with link 7665575, and the w4 mirror too:
  the window doesn't use s0 or s5, the only letters where w2's and w4's frames differ.
- **Effect (first order, from `k36/rows_w2.txt`):** the next link word, 7665675 (k = 2), sets the s1 = 6 cap at
  0.1852. s1 >= 7 stays at 0.1924. R's row then gives t >= 0.122 at (6,6) and >= 0.116 elsewhere. This round
  doesn't recompute Opus's second-order floor (11/71), whose worst frame is now dead.
- **LP note.** No five of w2 has all four of its slots fixed in this window, so wlp3/sep3 cannot use it as a
  pattern (`parse` needs at least one). It needs the link-word + non-five-slot pattern type, which is Job 30
  part A's sep3x extension.
- Guess check: "x3 = 5 windows D at ring <= 15" was wrong (nothing is D). "5.66677 C" was right, but the kill is
  broader than guessed: one window with no x-slot fixed.

## Check (18 Oct 2026, 09:43Z): does H7's defect D3 contain RSST #110? (coordinator, 09:22Z) Yes, and it is D on kc

This is a verification check, so it was not pre-registered. It used my own containment code
(`loop/d3/d3_rsst.py`), not `rsst_contain.py` or Opus's `rsst_in_defect.py`.
- **Patch.** D3 = `5|55667|776675755|75576667557657`, built with b8b/rings.py `Layered` plus 4 all-6 rings.
  - 135 vertices have an exact degree. Y is 11 fives and 10 sevens, as in README §7.1.
  - Outer-ring vertices are never images.
- **Containment.** An injective map of the configuration's interior, with exact degrees, onto an induced
  subgraph, sending every interior triangle onto a patch face.
- **#110, 0-based** (RSST `122.140`, ring 10, interior 5,5,5,5,7,7; this matches Opus's description).
  - 2 embeddings with 1 image, vertices 1, 2, 6, 7, 16, 17. All of them are in Y.
  - Cut out of the patch, it has a simple chordless 10-ring. **kc: D** (classes 2,461, ext 496, all reached,
    depth 5). RSST's own count is ext 496.
  - Opus had dfast D, so this is now D on two engines, and the RSST file agrees.
- **#110, 1-based** (`126.36666`, ring 14, interior 5,5,6^6,7). It also occurs in D3 once, not inside Y. kc gives
  D (ext 18,435, equal to RSST's).
- **Reading.** D3 contains a D-reducible configuration, so it cannot sit in a minimal counterexample. The H7 floor
  (t* >= 1/21 for rule classes (a)-(c), README §7.1) holds against R_opt only. It is R_opt-specific and says
  nothing once #110 joins the forbidden set.

## Round 36 (18 Oct 2026, 09:28Z-): H-W2, how much Rule-T inflow can w2/w4 take under the 7/27 y? (coordinator's go, 09:22Z)

**Pre-registered 09:28Z, before any code.** Gap G2. Runs on 1 core beside round 34 part C (2 cores).
- **Why.** Rule T (Opus, `loop/opus/G_ruleT_lp/FINDINGS.md` on branch 7uelj0) lets R's fives w0 and w6 send T
  across their 6-spokes w1, w5 to w2, w4 instead of to u, so R's row becomes t >= (0.7 - T0 - T6)/2.7. That only
  helps if w2 and w4 can take the load. t* = 0 needs T0 + T6 = 0.7; t* < 1/4 needs 0.025; t* < 0.22 needs 0.106.
- **Object.** w2 seen as a receiver of degree 7 under R* with an open filling (s1 >= 6). Its link is
  (u 7, w1 6, s1 a, e, e', s2 7, w3 5) and its s-word is (w0 5, p, x2, x3, x4, s3 7, w4 7), with a in {6,7,8,9+}
  and e, e', p, x2, x3, x4 in {5,...,9+}: 62,500 arrangements. w4 is the mirror image (s4 for s1), same numbers.
- **Filters.** sep3's own `c` check (the 5/6 transition table, RBIG 7-wheels, every forbidden pattern) with the
  j28_13 pattern set plus `loop/n9/win9-31`, and w1's 6-wheel (w2, a, p, s0 = 6, w0 = 5, u) not in R6 (R fixes
  the slot sep3 leaves free).
- **Quantities.** yload = sum over w2's link fives of the j28_13 y of their rooted words (w3 always gives
  y[7|7777] = 4/27). k = number of T inflows at w2: s-slots that are 5 between a (big, 6) link pair. R's own
  (u, w1, w0) gives one in every arrangement. Report max yload against the bar 34/27, the worst arrangement, and
  T_max = min over arrangements of (34/27 - yload)/k: the uniform T per inflow that w2 takes with y and t held
  at the 7/27 solution (first order; y only falls under T, so it is an upper bound on w2's load).
- **Check first.** sep3's `q` on the j28_13 y must give max d = 7 load 34/27 over all arrangements (the file's own
  line). Otherwise the y parse or the pattern set is wrong and nothing is reported.
- **Bars.** T_max >= 0.35: w2/w4 can absorb what t* = 0 needs from R, so the T job is worth Studio's cores. T_max
  below 0.0125: R's own w2/w4 block even t* < 1/4 at first order; T needs a re-solved y at w2, which L2's
  u -> w2 transfer can already try, so part 2 of the job is not worth running before part 1.
- **Kill line.** The check above fails, or the c-check accepts R itself at u (it must, as R is the LP binder).
- **Guess.** Some arrangement tight at 7/27 fits w2's frame (566 d = 7 rows are tight), so max yload = 34/27 and
  T_max = 0 at first order. If not, T_max is under 0.1.

**Round 36 result (09:40Z): w2 and w4 can each take T = 0.15 at first order, and they cap Rule T near
t = 0.155** (`loop/k36/w2load.py`, `w2load.txt`).
- Checks pass. sep3 on the j28_13 y (4 decimals) gives d = 7 max 1.2593 against the bar 1.2593. The c check accepts
  R at u. The pattern set is 16,401 patterns and 104 RBIG wheels. The missing r_3-r_8 files carry only d = 10.
- Of 62,500 w2 arrangements, sep3's c check rejects 360. The spoke's 6-wheel check rejects none, so w4 (spoke far
  letter s5 = 7, not 6) gives the same numbers as w2.
- Max yload is 1.1087, against a bar of 1.2593. That is link 7665575 s 5x65677 (any x), at s1 = 6. Its fives are
  e (7|5566, 0.7407), e' (7|5567, 0.2199) and w3 (7|7777, 0.1481). It has k = 1, the inflow from R's own w0.
- T_max (y and t held at 7/27) is 0.1506. The binding filling letter is 6. For s1 >= 7 it is 0.1924, set by a k = 3
  frame (7676575 / 5556577, yload 0.6821). Counting outflow from w2's own fives changes nothing.
- k: 45,399 arrangements have k = 1, 15,031 have k = 2, 1,590 have k = 3 and 120 have k = 4.
- In Opus's R row t >= (0.7 - T0 - T6)/2.7 these caps give 0.148 at (6,6), 0.132 at (6, >=7) and 0.117 when both
  are >= 7.
- **Second order, a floor [hand, one engine].** In the worst frame, five e's only big neighbour is w2. Its only
  6-spoke at w2 is s1, and that spoke's z is w1 = 6, so e has no T route and sends all of 1 - t to w2.
  - 7|7777 has no 6-spoke, and its five rootings share one variable, so each gets at least (1 - t)/5.
  - Taking e's other word (7|5567, shared with s2) as 0, w2's row gives T0 <= 2.2t - 0.2 at s1 = 6.
  - Combined with Opus's R row at filling (6,6): t >= 1.1/7.1 = 0.155. This holds for Rule T without an L2
    transfer out of w2, while R*(6,6) and that w2 frame stay unforbidden.
- **Against the bars:** 0.15 sits between 0.0125 and 0.35. w2/w4 don't block T below 1/4 or 0.22, but they can't
  take what t* = 0 needs from R (0.35 each).
- Guess check: "some tight row fits w2's frame, T_max = 0" was wrong. The worst frame has slack 0.15. The fallback
  "under 0.1" was also wrong.
- **Next kill target [I].** The worst frame holds a triangle of three fives (e, e', and x3 between them) next to the
  6 at s1. If u + w2 + that frame is reducible, the cap at s1 = 6 rises towards 0.19.

## Round 35 (18 Oct 2026, 08:54Z-): H-KCC, a C-reducibility mode for kc, then C on R's windows

**Pre-registered 08:54Z, before any code.** Gap G2. Runs while round 34 part C uses the cores.
- **Why.** The 7/27 certificate rests on R alone (round 34 amendment), and R has no D window among its B-fixed ones.
  C is the other route. cfast (single engine) has timed out at ring 16 on binder windows. A second C engine is also
  what the charter needs before any C kill counts.
- **Definition (my own derivation, no cfast/dfast/Lean source read).** X is a set of 1-4 free-completion edges,
  each with at least one interior end. It is admissible (conservative) if every component of the graph (V, X)
  holds at most one ring vertex and no free-completion edge outside X joins two vertices of one component. Then
  G/X is loopless and smaller, so it is 4-coloured by minimality. Its colouring gives a proper ring colouring
  that extends to K/X: an interior colouring with each component one colour and every other edge proper. K is C
  if no ring class left unreached by the D-closure extends to K/X. Admissible sets with two ring vertices in a
  component (RSST's triad cases) are left out, so this can only miss C verdicts, never add one.
- **Engine.** kc `-C`: after the closure, enumerate admissible X by size and test unreached classes in a fixed
  shuffled order, with early exit at the first one that extends. Report C with the first working X, or not-C
  with the smallest leftover found. `-x FILE` evaluates given X exactly (full leftover count).
- **Validation.** cfast outputs with verdicts: `job27/k2a.cfast` (82 configurations, 11 C) and
  `out/job28/r_12.cfast` (77, 15 C), plus `out/def_r1.cfast` (74, 4 C). (a) For cfast's best or working X,
  whenever my admissibility accepts it, my exact leftover equals cfast's. (b) Every kc C is cfast C. (c) Report
  how many cfast C my conservative set misses.
- **Kill line.** A leftover mismatch, or a kc C that cfast calls not C, which survives a recheck: kc-C is not
  trusted and nothing is run on R.
- **Then.** kc-C on R's ring 16-17 B-fixed windows and on any round-34 part C window that is not D. Bar: any C on
  kc-C (with cfast to follow at Studio) breaks the 7/27 certificate.
- **Guess.** Validation passes after one fix. Leftover counts match. kc-C misses 10-25% of cfast's C (the triad
  cases). R: 0 or 1 C among its 3 B-fixed windows at ring 16-17.

**Round 35 validation (09:08Z): passes with no fix** (`loop/kcc/`, `mkvalc.py`, `cmpc.py`, `valc_kcc.txt`).
- 163 configurations from the three files have input lines (k2a 82, r_12 77, def_r1 the 4 C ones); 30 are cfast C.
- (a) Exact leftover equals cfast's on all 145 of cfast's X that my admissibility accepts. The other 45 (cfast best X
  of not-C configurations) put two ring vertices in one component, so I don't test them.
- (b) 30 of 30 cfast C are kc-C C, and 133 of 133 cfast not-C are kc-C not-C. (c) kc-C misses none of the 30.
- Edge model agrees: kc-C's subset count equals cfast's admissible + inadmissible on every one checked (e.g. 12,950 at
  24 edges). Guess check: "one fix" was pessimistic, and "misses 10-25%" was wrong (0 missed).
- Running kc-C now on R's ring 16-17 B-fixed windows (1 core, beside round 34 part C).

## Round 34 (18 Oct 2026, 08:43Z-): H-K34, do the 7/27 binder's last windows, or the other tight d = 7 rows' untested windows, hold a D? (coordinator's overnight plan, 08:40Z)

**Pre-registered 08:43Z, before any run.** Gap G2 (K = 2 LP at t* = 7/27).
- **Why.** The x = 0 dual certificate at 7/27 (`out/wlp3_j28_13.txt`, same in `out/wlp3x_j29_13_notx.txt`) has one
  receiver row: d = 7 link 5675765 s 6577575 (weight 0.37), plus senders 55667, 55767, 77777. Its B-fixed windows
  (|S| >= 2 of its three fives, `gen28.variants`, any ring): ring 11 {0,6} not D; ring 16 {0,3}
  `f7_.556757_.56.77.` in Studio's queue (`out/job28/in_13.txt`, no verdict); ring 17 {3,6} `f7_.556757_.57.77.`
  and {0,3,6} `f7_5567576_56.77.7`, never run. That is every window this row has.
- **Part A.** kc (Gauss-Seidel) on those 3 windows. Any D is checked at once with `bin/dfast` (ring 16) or
  `bin/dfast18` (ring 17), which are independent of kc. Both D means the certificate row is forbidden [E2] and the LP
  must be re-solved.
- **Part B.** The round-13 tight family (`out/job28/tight_13.txt`, 566 d = 7 rows tight at the 7/27 solution, 560
  still free by `w2.py cover`) has 1,729 untested B-fixed windows at ring <= 18 (72 more pending at Studio):
  ring 10-14: 571, 15: 389, 16: 307, 17: 301, 18: 161 (`loop/k34/t13_r18.txt`). Run in ring order on 3 cores, kc
  and dfast both, until the 45-minute cap; the rest goes to the next round.
- **Bars.** A: 1+ D of 3 changes the plan (the 7/27 certificate breaks). 0 of 3 means the certificate row has no
  B-fixed window left at all, so route A (ring 17-18 at u) is closed for it and its fate is C (Studio's cfast) or a
  window centred at a neighbouring 7. B: report D windows, rows newly forbidden (by `w2.py cover`), and kc/dfast
  agreement on every window both ran.
- **Kill line.** Any kc/dfast verdict mismatch stops the round and is reported before anything else.
- **Guess.** A: 0 of 3 D (the row's ring-11 window has low ext and round 17 got 0 D of 6 at ring 17). B: about a
  quarter of the ring <= 14 windows D (round 14 got 178 of 636), fewer at 15-16, and 50-150 rows newly forbidden.

**Amendment 08:50Z, before part C runs (part A's kc verdicts are in: 0 of 3 D).** Reading the certificate: the
fives of R are at link positions 0 (word 55667, one big neighbour, u), 6 (55767, two 7s, u and s5, mirror images in
the five's link) and 3 (77777). With rooted-word rules a five sends at least 1 - t in total, so y[7|5566] >= 1 - t,
y[7|5576] >= (1 - t)/2, y[7|7777] >= (1 - t)/5, and R's load is <= 1 + t. Adding: 1.7(1 - t) <= 1 + t, so
t >= 7/27, with dual weights 10/27, 10/27, 5/27, 2/27 (the 0.3704/0.3704/0.1852/0.0741 above). So **no kill other
than R itself (or one of its three sender types) can move the y-class LP below 7/27**, and part B cannot move t*
while R stands. Part B drops to after part C.
- **Part C.** R's windows beyond B-fixed: u + all seven link vertices + any subset of the seven s-vertices, all at
  R's letters (`loop/k34/fullwin.py`, 116 distinct windows: ring 13: 10, 14: 12, 15: 20, 16: 38, 17: 20, 18: 12,
  19: 4; the window with every s fixed, `f7_5567576_5657757`, is ring 17). kc on all, dfast on ring <= 16, dfast18 on any kc D
  at ring >= 17. Bar: any D on both engines forbids R and breaks the 7/27 certificate. Guess: 0 D (the 7-wheel
  part is shared by every window, and the B-fixed ones are all far from D).

**Second amendment 08:58Z, before any part C window ran (the first chain never started).** The certificate reads
only the fives' words, which use s0, s2, s3, s5, s6. s1 and s4 sit next to no five, so an LP row with any letters
there has R's load. Forbidding R alone just moves the binder to another filling. The object to kill is R*: link
5675765 with s0, s2, s3, s5, s6 at R's letters and (s1, s4) one of 25 fillings in {5,6,7,8,9+}^2. (The Opus team
reports via the coordinator that RSST's 128.136, C at ring 11, sits in the fillings with a 5 at s1 or s4. That is
RSST's verdict, not ours yet.)
- **Part C, as run.** `loop/k34/fillwin.py`: u + all seven link vertices + any subset of {s0, s2, s3, s5, s6} + s1
  and s4 each absent or at a letter 5-8. That gives 710 windows at ring 13-25 (13: 10, 14: 20, 15: 43, 16: 85,
  17: 106, 18: 121, 19: 119, 20: 90, more above). Coverage includes mirror images. `loop/k34/drive.py` runs kc in
  ring order on 3 workers up to ring 20. It skips a window once every filling it covers is killed. A kc D is re-run
  on dfast (ring <= 16) or dfast18 (17-19), and a filling counts as killed only when both say D. Every 4th not-D
  window at ring <= 16 also gets dfast, as an agreement check.
- **Bar.** R* is forbidden by D if all 25 fillings die. Report the killed fillings and the cheapest window for each.
- **Guess.** The fillings with a 5 at s1 or s4 die to D at ring <= 16 (an extra five next to the link). Most of the
  16 others survive D, which leaves them to C (round 35).

**Round 34 part A result (09:08Z): 0 of 3 D on both engines.** kc and dfast/dfast18 agree on classes, ext and
reached for all three (`loop/k34/binA_kc.out`, `binA_dfast.out`): ring 16 `f7_.556757_.56.77.` reached
352,695 / 1,793,614; ring 17 `f7_.556757_.57.77.` 629,529 and `f7_5567576_56.77.7` 1,907,986 of 5,380,840. Every
B-fixed window of R is now tested and not D, so route A at u is closed for R by B-fixed windows. Part C (fillings)
is running: the 9 fillings with a 5 at s1 or s4 died at ring 13 on both engines (`f7_5567576_5....5.` and two
others), as guessed.

**Part C interim (09:15Z).** Driver v2 (`drive.py`, 09:12Z) runs kc -C per window: D, then the round-35 C stage
if not D. The per-filling table is `loop/k34/fillings.txt`, and v1's D-only output is kept as `fill_kc_v1.out`.
- The 9 fillings with a 5 at s1 or s4 die to `f7_5567576_5....5.`: the 7-wheel 5675765 with s6 = 5 and s4 = 5 (its
  mirror has s1 = 5), ring 13, D on kc and dfast (ext 9,300, reached 66,430 of 66,430).
- These 9 are exactly the fillings where a big neighbour of u can be R-shaped. Around w2 the link reads
  u 7, w1 6, s1, e, e', s2 7, w3 5, which is a rotation of 5675765 only as 7655675 (s1 = 5); w4 likewise with
  s4 = 5. The LP's binder R itself is filling (5, 5), the self-paired case. That fits L2's transfers giving nothing
  [I].
- The LP can't use this kill yet. sep3/sep3x patterns carry codes only at five positions, and s1, s4 sit next to no
  five. Sent to the coordinator: a pattern type with letters at non-five s positions, then an L2 re-solve [I,
  untested].
- Base windows (no s1/s4, cover all 25 fillings): the 11 at ring 13-15 are not D and not C. kc -C on R's B-fixed
  windows: ring 16 `f7_.556757_.56.77.` not C (105,151 admissible X, best leftover 1,332); ring 17
  `f7_5567576_56.77.7` not C (200,526 admissible X, best leftover 3,424). In both, the C stage took under 3 s after
  the closure.

## Round 33 (18 Oct 2026, 02:54Z-): H-KC, an independent D-closure engine for k19 (coordinator's job, 02:49Z)

**Pre-registered 02:54Z, before any code.** Not on the paused L2 line.
- **Why.** k19 (`6:6:6|6:6:6|6:6:6|6:6:6|8:666:6`, ring 19, 48,427,561 classes), the K <= 1 gate key, has one
  reducibility verdict: Studio's dfast18 D (ext 3,909,279, depth 4; `studio14b/part00.out`). Its Lean run now lands
  22-25 Oct. The gate needs a second engine independent of dfast.
- **Engine.** `wheeldis/loop/kc/kc.cpp`, a C++ port of my Python closure `loop/kempe_w7_5666567.py` (textbook
  Birkhoff/Heesch Kempe D-closure: for some pairing, every coarsest admissible chain partition, i.e. a non-crossing
  partition of the ab-runs with its Kreweras complement on the cd-runs, has a swap of whole chains that lands on a
  good class). Ring classes ranked directly (no 4^n table), extension by backtracking, witnesses cached per class
  and pairing. **No dfast, cfast or Lean source is read.** Only dfast's output lines are used, to compare.
- **Validation, before k19.** (a) c7_5666567 (ring 13, not D, reached 53,690, depth 18; my Python already matches
  dfast here). (b) At least 40 ring 10-16 windows from `loop/n9` and `loop/w2` with dfast verdicts, at least 10 of
  them not D, picked by a fixed rule (every k-th line). (c) The ring-17 not-D key `6:6:6|6:6:6|6:6:6|6:6:6|6:8:6`
  (reached 3,387,935 of 5,380,840) and one ring-17 D key from `studio14b`. (d) One ring-18 D key if time allows,
  which also prices k19.
- **Pass** if D/not-D, classes, ext and reached all equal dfast's on every validation key. Depth is reported in
  Jacobi mode as a further check, not a bar.
- **Kill line.** Any D/not-D or reached mismatch on a validation key that survives a recheck with the Python
  reference: the engine is not trusted, k19 is not run on it, and the mismatch is reported. If C++ and Python agree
  against dfast, that is reported at once as a dfast discrepancy.
- **k19.** Single core, Gauss-Seidel order, checkpointed so it can resume across this container's 2-hour job limit.
  Reported: D/not-D, classes, ext, reached, passes, time.
- **Guess.** Validation passes after one or two bug fixes; k19 comes back D with ext 3,909,279, in 2-6 hours.

**Round 33 result (04:15Z): H-KC passes; k19 is D on an independent engine** (`wheeldis/loop/kc/FINDINGS.md`).
- Validation, final build: 98 ring 10-16 windows (80 not D), c7_5666567, the ring-17 not-D and D keys and a ring-18
  D key. Classes, ext, reached and D equal dfast on every key; Jacobi depth equal on all 101 where compared.
- **k19: D = true**, classes 48,427,561, ext 3,909,279 (both equal to dfast18), reached all, 3 Gauss-Seidel passes,
  25 minutes and 683 MB on one core.
- Jacobi rerun (05:15Z): depth 4, equal to dfast18's; 59 minutes.
- No dfast, cfast or Lean source read. Guess check: "one or two bug fixes" was pessimistic (none needed); "2-6
  hours" was long (25 minutes).

## Round 32 (17 Oct 2026, 04:58Z-): H-L2f, does the floor move once the d = 8 binders are gone? (coordinator's go, 04:58Z)

**Pre-registered 04:58Z, before the run.**
- **Why.** Round 31 forbade both d = 8 rows that bound round 30's LP at 15/83. Free binders left: the d = 7 pair
  5567576/5756756 and 5586576/5757756, and two d = 9 rows.
- **Run.** Round 30's setup plus win31 (`loop/n9/run32.sh`): j28_12.args plus `loop/l2/full_extra.args`, maxit 60,
  no iteration started after 1500 s, 1 core, 2-hour wall so it finishes with its report.
- **Bars.** t* moves if it ends at least 0.005 below 15/83 (under 0.1757); it holds if within 0.005. The go stands if
  under 0.22. Kill line (coordinator's): converged t* >= 0.22, or still rising at the cap with no binder reachable by
  an untested small window at ring <= 16. Reported: t*, convergence, and the binders by row and by degree.
- **Guess.** It holds near 15/83: the d = 7 pair carries 0.193 of round 30's 0.36 dual weight.

**Superseded (17 Oct 17:30Z, coordinator state):** Studio's Job 29 L2 with exact transfer columns gives t* = 7/27
exactly on the full registry. Every restricted-LP value from rounds 23-32 (1/5, 7/33, 9/43, 15/83, 0.169) was
under-separated; charge-sharing gives no gain. The window kills themselves stand (second-engined).

**Round 32 result (07:00Z): inconclusive. Killed at the 2-hour wall before its report; t* = 29/172 = 0.1686 at
iteration 9 and still rising** (`wheeldis/loop/n9/FINDINGS.md`).
- Iteration 9's y-only separation (d = 7-13) ran 70 minutes and was not checked against tmax; the final solve and
  report did not fit in the rest of the wall. No binders, tight rows or dump.
- 0.1686 is under 15/83 but is a rising lower bound, so "moves" vs "holds" cannot be scored. Go stands (under 0.22);
  kill line's binder clause cannot be checked.
- Fix committed to l2.py (unused so far): `binout=FILE` after every solve, tmax checked inside y-only separation,
  a tmax-cut run never reported converged.
- Line paused (coordinator) until Studio's queue returns.

## Round 31 (17 Oct 2026, 04:52Z-): H-B30, do small windows forbid round 30's d = 8/9 binders?

**Pre-registered 04:52Z, before any dfast run.**
- **Why.** Round 30 holds the transfer LP at 15/83 on six rows (`loop/n9/bind30.txt`). The two d = 7 rows have no
  untested window at ring <= 16 outside Studio's queue; the four d = 8/9 rows have 31.
- **Windows.** Those 31 (`loop/n9/win31.txt`; f8: 4 at ring 12, 4 at 13, 6 at 14, 5 at 15; f9: 5 at 15, 7 at 16),
  dfast on 3 cores, 30-minute cap.
- **Lives** if at least 2 of the 4 d = 8/9 binders are forbidden; **dies** if none is.
- **Guess.** Two die, both d = 8 (round 16: 31% of d = 8/9 windows D; d = 9 windows at ring 15-16 ran 6 D of 185 in
  round 25).

**Round 31 result (04:57Z): H-B30 lives; both d = 8 binders forbidden** (`wheeldis/loop/n9/FINDINGS.md`).
- 31 windows, **9 D**: 9 of 19 at d = 8, 0 of 12 at d = 9.
- Forbidden: 85675765/55555555 and 56565585/69695665. Free: the two d = 9 rows (no window left at ring <= 16) and the
  d = 7 pair (Studio's 3 queued windows, then 2 at ring 18; none at ring 17).
- Guess check: "two die, both d = 8" was right.
- **Paused here** (coordinator, 04:53Z) until Studio's second engine and its d = 7 queue return. win31 is added to
  `loop/l2/full_extra.args` but no LP has run with it.

## Round 30 (17 Oct 2026, 04:02Z-): H-L2e, is 9/43 near the converged transfer LP? (coordinator's go, 03:57Z)

**Pre-registered 04:02Z, before the run.**
- **Why.** Round 28 stopped at maxit 8 after 6 minutes with t* flat at 9/43 for 5 iterations. Round 29 then forbade
  4 of its 9 binders.
- **Run.** `l2.py` with j28_12.args plus `loop/l2/full_extra.args` (now with win29; the 6-sea defect files left out
  until Studio's second engine and name mapping), maxit 60, no iteration started after 1500 s, 1 core, 2-hour wall
  (`loop/n9/run30.sh`). Converged means an iteration adds no row.
- **Bars.** The go stands if t* at the end is under 0.22. Kill line (coordinator's): converged t* >= 0.22, or t*
  still rising at the cap with no binder reachable by an untested small window at ring <= 16. Reported: t*, its
  convergence status, and the top binders by row and by degree.
- **Guess.** Not converged at the cap; t* ends between 9/43 and 0.215, with d = 7 rows binding.

**Round 30 result (04:52Z): t* = 15/83 = 0.1807 from iteration 5 through 8; the last iteration added 0.25% more
rows, so close to converged but still a lower bound** (`wheeldis/loop/n9/FINDINGS.md`).
- The drop from 9/43 comes from win29's four D windows forbidding start-set rows. It leans on single-engine verdicts
  (win25/25b/27/29) until Studio's second engine passes them.
- Go stands with margin; kill line not met.
- Binders: d = 7 5567576/5756756 and 5586576/5757756 (0.096 each), d = 8 85675765/55555555 and 56565585/69695665
  (0.048 each), d = 9 565656565/668556866 and 565565565/685885865. None forbidden. 31 untested windows at ring <= 16,
  all at the d = 8/9 binders; the d = 7 two have none outside Studio's queue.
- Guess check: "between 9/43 and 0.215" was wrong; it fell to 15/83.

## Round 29 (17 Oct 2026, 03:57Z-): H-B28, do small windows forbid round 28's binders?

**Pre-registered 03:57Z, before any dfast run.**
- **Why.** Round 28 holds the full-registry transfer LP at 9/43 on nine rows (`loop/n9/bind28.txt`): eight d = 7
  (dual 0.353 in all) and one d = 9 (0.021). None is forbidden yet.
- **Windows.** Their 14 untested small B-fixed windows at ring <= 16 not already in Studio's queue
  (`loop/n9/win29.txt`; 1 at ring 12, 3 at 13, 1 at 14, 6 at 15, 3 at 16), dfast on 3 cores, 20-minute cap.
- **Lives** if at least 3 of the 9 binders are forbidden; **dies** if none is.
- **Guess.** Two die. Round 27 killed 2 of 3 binders, but most of these are d = 7 rows whose ring <= 14 windows
  were already tested in rounds 14-15.

**Round 29 result (04:00Z): H-B28 lives; 4 of 9 binders forbidden** (`wheeldis/loop/n9/FINDINGS.md`).
- 14 windows, **4 D**, all d = 7. Forbidden: the two heaviest (5775656/6565579, 5675765/6557576) and two v-side rows
  with 7s in the link. Five stay free, among them d = 9 565656565/677667766.
- Guess check: "two die" was low; four did.

## Round 28 (17 Oct 2026, 03:49Z-): H-L2d, the transfer LP with the full registry (coordinator's go, 03:44Z)

**Pre-registered 03:49Z, before the run.**
- **Why.** Rounds 25-27 forbid three of the four rows that held round 26 at 7/33, and l2.py did not load Studio's
  r_12 partial output (which forbids the fourth's neighbour 5567576/5756656).
- **Run.** `l2.py` with j28_12.args plus every registry `.out` with a D verdict it lacked (`loop/l2/full_extra.args`:
  r_12.partial, z_lone_studio_dfast18, def_b7_k5d14, fans, b7/k5_d14, and all explore windows). 1 core, tmax 1500 s,
  maxit 8, wall sized for round 26's last iteration (`loop/n9/run28.sh`). Values are lower bounds unless converged.
- **Bars.** The go stands if t* at the end is under 0.22. Kill line (coordinator's): converged t* >= 0.22, or t*
  still rising at the cap with no binder reachable by an untested small window at ring <= 16. Reported: t*, its
  convergence status, and the top binders by row and by degree.
- **Guess.** t* reads about 0.20-0.21 at the cap, not converged; 5576576/5756756 and other d = 7 rows bind.
- **Caveat.** win25, win25b and win27 are single-engine (dfast) until Studio's second engine passes them.

**Round 28 result (03:56Z): t* = 9/43 = 0.2093 from iteration 3 through 7, not converged (maxit reached at 6
minutes); the go stands as a lower bound** (`wheeldis/loop/n9/FINDINGS.md`).
- Only f/e/p-named files load: r_12.partial added 37 patterns; z_lone_studio_dfast18 (62 D), the hash-named defect
  files and fans add none (wlp3 parses `[epf]<d>_` names only).
- Kill line not met: not converged, not rising, binders reachable.
- Binders: eight d = 7 rows (dual 0.353; heaviest 5775656/6565579 and 5675765/6557576) and one d = 9 row
  565656565/677667766 (0.021). None is forbidden; they have 14 untested windows at ring <= 16, 6 more in Studio's queue.
- Guess check: "0.20-0.21, d = 7 rows bind" was right.

## Round 27 (17 Oct 2026, 03:44Z-): H-B26, do small windows forbid the 7/33 binders?

**Pre-registered 03:44Z, before any dfast run.**
- **Why.** Rounds 25-26 hold the transfer LP at 7/33 on four rows (`loop/n9/bind25.txt`): d = 7 5576576/5756756,
  5675765/9555596, 5567576/5756656 (already forbidden in Studio's job 28 partial output), and d = 10
  5656556565/6576565765.
- **Windows.** Their 16 untested small B-fixed windows at ring <= 16 (`loop/n9/win27.txt`; 1 at ring 11, 2 at 13,
  3 at 14, 7 at 15, 3 at 16), dfast on 3 cores, 30-minute cap.
- **Lives** if at least 2 of the 3 free binders are forbidden; **dies** if none is.
- **Guess.** One dies, likely the d = 10 row (round 24: 47% of d = 10 windows D, against 11% at d = 9).
- No LP rerun inside this round; the next LP run should also load `out/job28/r_12.partial.out`.

**Round 27 result (03:47Z): H-B26 lives; 2 of the 3 free binders forbidden** (`wheeldis/loop/n9/FINDINGS.md`).
- 16 windows, **6 D**: 2 of 5 at d = 7 (ring 13), 4 of 11 at d = 10.
- Newly forbidden: d = 7 5675765/9555596 and d = 10 5656556565/6576565765. Still free: **5576576/5756756** (the
  heaviest, dual 0.12; Studio's dfast18/cfast has its other windows).
- Guess check: "one dies" was low; two did.

## Round 26 (17 Oct 2026, 02:41Z-): H-L2c, where does the transfer LP settle with every explore window?

**Pre-registered 02:41Z, before the run.** Round 25's 6-iteration check read t* = 7/33 and was not converged.
- **Run.** `l2.py` (round 20/23's restricted transfer LP) with win14, win8, win89, win9 and win25 as patterns, to
  convergence or a 45-minute cap, 1 core (`loop/n9/run26.sh`). The value at the cap is a lower bound.
- **Go stands** (round 23's bar) if t* at the end is under 0.22; **L2 looks weak** if it is above 0.25 (13/49 =
  0.265 without transfers); in between, neither.
- Also recorded: the binding rows by degree, which pick round 27's window targets.
- **Kill line (coordinator, added 02:42Z after launch, before any of the run's output was read).** H-L2c dies if
  the converged t* is at least 0.22, or if t* is still rising at the cap and no binder is reachable by small windows
  (no untested B-fixed window at ring <= 16). Reported: t* with its convergence status, and the top binders by row and
  by degree.
- **Caveat.** win25 (and so the binder's kill) is single-engine (dfast) until Studio's second engine passes it.

**Round 26 result (03:42Z): t* = 7/33 = 0.2121 from iteration 3 through 8, not converged; the go stands as a lower
bound** (`wheeldis/loop/n9/FINDINGS.md`).
- 115,587 rows at iteration 8, still adding about 37,000 v-side rows per iteration. The cap is checked only between
  iterations; iteration 9 ran past the 60-minute wall and the run was killed before its report.
- Kill line not met: not converged, not rising, and the binders have untested small windows.
- Binders (from round 25's solve at the same 7/33): d = 7 5576576/5756756 (dual 0.12), 5675765/9555596,
  5567576/5756656, and d = 10 5656556565/6576565765. 5567576/5756656 is already forbidden by a D window in Studio's
  `out/job28/r_12.partial.out`, which l2.py does not load. The four have 16 untested windows at ring <= 16.
- Guess check: "climbs to 0.215-0.225" was wrong; it never left 7/33.
- **Guess.** It climbs a little and stops near 0.215-0.225, with d = 7 rows binding.

## Round 25 (17 Oct 2026, 01:47Z-): H-N9b, ring 15-16 windows for the 39 rows round 24 left free

**Pre-registered 01:47Z, before any dfast run.**
- **Why.** Round 24 left 39 of its 218 rows free (33 d = 9, 6 d = 10), the binder 559565656/565566666 among them.
  t* stays at 1/5 until the binder dies.
- **Windows.** All 202 untested small B-fixed windows of the 39 rows at ring 15-16 (`loop/n9/win25.txt`, built by
  `w2.py build ... ds=9,10`): the binder's 11 first (8 at ring 15, 3 at 16), then 82 ring 15, then 106 ring 16.
  dfast on 3 cores, 45-minute wall cap; windows not reached are reported as untested.
- **H-N9b lives** if the binder is forbidden, or if at least 13 of the 39 rows (1/3) are; **dies** if the binder stays
  free and at most 3 rows (under 10%) are forbidden.
- **Guess.** The binder stays free: its 9 tested windows all failed, and only 11% of d = 9 windows were D at ring
  <= 14. About 5-8 of the 39 rows die, mostly the d = 10 ones.

**Round 25 result (02:40Z): H-N9b lives; the binder 559565656/565566666 is forbidden** (`wheeldis/loop/n9/FINDINGS.md`).
- dfast ran 185 of the 202 windows in the cap (17 ring-16 ones not reached): **10 D**, 6 of the binder's 11.
- 5 more d = 9 rows forbidden, the binder among them: 184 of 218 (84.4%); d = 9 now 28 of 56. 34 rows stay free.
- **LP check (after the verdict).** `l2.py` with every explore window, 6 iterations: **t* = 7/33 = 0.2121**, not
  converged; d = 7 rows bind again (5576576/5756756 heaviest) plus one d = 10 row.
- **Correction [I].** More patterns only delete rows, so round 23's true t* is at least 7/33 too: its 1/5 was an
  under-separated lower bound, not the floor. Still under round 23's 0.22 bar, still unconverged.
- Guess check: "binder stays free" was wrong; "5-8 rows, mostly d = 10" was wrong too (5 rows, all d = 9).
- **Tail (02:56Z).** The 17 windows the cap missed: 6 D, no new row forbidden. The 34 free rows have no untested
  window at ring <= 16 left.

## Round 24 (17 Oct 2026, 01:06Z-): H-N9, small windows against the d = 9 five-heavy family (coordinator's go)

**Pre-registered 01:06Z, before counting or any dfast run.**
- **Why.** Round 23's transfer LP is held at 1/5 by one d = 9 row, 559565656/565566666 (five fives, one big). With
  transfers, d = 9 rows whose fives have no usable big are the floor.
- **Family.** Every d = 9 arrangement with the maximum number of fives allowed by the current patterns (j28_12 plus
  win14/win8/win89; sep3 enumeration with unit weights), and with no 7/8 link vertex. Counted first.
- **Windows.** Round 14/16's small B-fixed windows (`w2.py build ds=9`, |S| = 2-3, u exact 9, N(S) exact) not yet
  tested, ring <= 14 (ring 15 if there are fewer than 100 at ring <= 14), dfast on 3 cores.
- **H-N9 lives** if the D windows forbid at least half of the family; **dies** under 10%.
- **Guess.** About 40%. Round 16 forbade 77% of Studio's d = 9 tight rows, but those carried 7s and 8s near the fives;
  here the fives sit in a 6-sea, where windows are larger and less often D.

**Round 24 result (01:45Z): H-N9 lives on the family as built, 179 of 218 rows forbidden (82.1%); the binder is
still free** (`wheeldis/loop/n9/FINDINGS.md`).
- **Deviation.** The sep3 max-fives enumeration timed out, so the family is the LP's own tight rows: d = 9/10 rows
  tight at a 4-iteration rerun of round 23 (t* = 1/5) with no 7/8 link vertex. 56 at d = 9, 162 at d = 10. No
  existing pattern forbade any of them.
- **Windows.** 413 untested at ring <= 14, **140 D**: 16 of 148 centred at a 9, 124 of 265 at a 10.
- **Coverage.** d = 9: 23 of 56 (41%, between the bars on the population the pre-registration named). d = 10:
  156 of 162.
- **Binder.** 559565656/565566666 stays free, so t* stays at 1/5 and the LP was not rerun. 39 rows stay free;
  they have 202 untested windows at ring 15-16 (the binder 11).
- Guess check: "about 40%" was right for d = 9; d = 10 is far easier.

## Round 23 (16 Oct 2026, 23:28Z-): H-L2 again, with the explore windows as patterns

**Registered 23:28Z, after a first look (not a clean pre-registration).** Rounds 20 and 22 used only the j28_12
patterns. Our own windows (`loop/w2/win14.out`, `win8.out`, `win89.out`) already forbid some of their binders, so I
reran both LPs with them (`l2.py ... pat=...`).
- **Seen before registering.** No transfers: t* rises from 0.2405 to 7/27 over 40 iterations, not converged
  (`l2_notx_w40.txt`). With transfers, 3 iterations: **t* = 1/5**, held by one d = 9 row with no 7/8 neighbour
  (559565656/565566666, the lone-five counting bound); 43 of 46 HARD28-like rows slack (`l2_x_w3.txt`).
- **Now running.** The transfer LP to convergence (60 iterations or 45 minutes).
- **Survives** (H-L2, round 20's bar) if the converged t* < 0.22; **dies** if it climbs above 0.25.
- **Guess.** It climbs, as the baseline did (start set now 1,453 rows, so separation does more work), and settles
  near 0.22-0.23. Above the lone-five 1/5 either way.

**Round 23 result (00:53Z): H-L2 survives with the explore windows. t* = 1/5 held for 11 iterations** (185,503
rows, 19,700 transfer columns; stopped at the time cap, not converged; `wheeldis/loop/l2/l2_x_w.txt`).
- One row binds: d = 9, 559565656/565566666 (three lone fives and a 5-5 pair next to a single 9), dual 1/5. No d = 7
  or d = 8 row binds. 23 of 46 HARD28-like rows in the LP are slack.
- Same patterns without transfers: t* >= 7/27 and still rising at 40 iterations (`l2_notx_w40.txt`).
- Reading: round 20 stalled because self-paired d = 7 rows bound; our small windows forbid them. With them gone,
  big-big transfers relieve every d = 7 and d = 8 row, and the bound drops to a d = 9 lone-five row that has no
  usable big neighbour. That is a go signal for Studio to build L2 properly (restricted LP, so it can only overstate
  the gain), and it names the next target: the d = 9 lone-five rows.
- Guess check: "climbs to 0.22-0.23" was wrong; it never moved from 1/5.

## Round 22 (16 Oct 2026, 23:00Z-): H-S, do Schnyder-orientation transfers break the 7/27 floor? (k's pick)

**Pre-registered 23:00Z, before any build.** Idea and bars are mine; k chose to run it (decision card, 22:57Z).
- **Why.** Round 20 stalls at 7/27 on d = 7 rows next to an identical copy: a rule that sees both 2-balls cannot
  orient the edge. Every planar triangulation has a 3-orientation (Schnyder wood): each interior vertex has exactly 3
  out-edges. A rule may read it, and reducibility is unaffected.
- **LP.** Round 20's restricted LP at its start set (Studio's 3,181 tight rows plus the 617 family), no separation.
  Each arrangement becomes one row per orientation of u's big edges consistent with out-degree 3 (the small
  neighbours take the rest; the orientation is adversarial). Variables a[tau] (tail sends to head) and b[tau]
  (head sends to tail) per oriented edge type. Round 20's symmetric rules are the special case a = x, b = x reversed,
  so t* <= 7/27. Rows only raise t*, so a start-set t* >= 7/27 is a trustworthy kill.
- **Survives** if t* < 0.25 at the start set (then build v-side separation with orientation). **Dies** if t* = 7/27.
- **Guess.** Dies at exactly 7/27. The binders have 5 small neighbours, so the adversary can orient both big edges
  either way, and the worst case over the two orientations gives |a - b| back. Orientation helps only where
  out-degree 3 forces a big edge, i.e. rows with 5+ bigs, which do not bind.

**Round 22 result (23:08Z): H-S dies, t* = 7/27 exactly** (`wheeldis/loop/l2/s2_orient.txt`; the symmetric check
`s2_sym.txt` gives 7/27 on the same set). 11,673 oriented rows, 1,944 transfer columns. The dual of each binder
splits across its orientations ({} and {4} for 5765756/5556666), so the adversary undoes any tail-to-head rule.
- Reading: two identical overloaded 7s cannot help each other, whatever the rule reads. Charge must leave the pair
  (distance >= 2 from u), or the pair must be reducible (Studio: 3 of 5 binders killed, 2 at ring 15-16).
- Guess check: "dies at exactly 7/27" held.

## Round 21 (16 Oct 2026, 17:22Z-): H-A', can a HARD28-like row be forbidden through a neighbouring 7? (coordinator's test)

**Pre-registered 17:22Z, before any matching.** Design and bars are Long Table's message of 17:20Z; the guess is mine.
- **Views.** For each of the 49 HARD28-like rows (`loop/lf/seeds.txt`) and each exact link 7 v of u: v's arrangement
  as fixed by u (`pairs.py view`: 5 link letters, 2-4 s letters). 32 views; every free letter over 5, 6, 7, 8, 9
  (9 = 9+, matched only by B). 15,625 fillings per view (one view 3,125).
- **Kill per filling.** A registered D/C window centred at v (every f7_/e7_/p7_ name with a D or C verdict in the
  registries, w2.py matching), or a reducible wheel at v or at one of v's link fives/sixes (R5, R6 for every p,
  RBIG). Existing verdicts only.
- **A view is closed** if every filling is killed. **H-A' lives** if at least 1/3 of the 49 rows have a closed
  view; **dies** if fewer than 1/6 do. Only rows with an exact link 7 can have one.
- **Guess.** Dies. Most HARD28-like rows have 8s, not 7s, next to u (32 views over 49 rows), and free s letters
  at v leave fillings with no five next to v's fives. About 3 rows closed.

**Round 21 result (17:25Z): H-A' dies, 0 of 49 rows closed.** Details in `wheeldis/loop/ap/FINDINGS.md`.
- 25 rows have an exact link 7, giving 32 views and 487,500 fillings. 89% are not killed by any v-centred D/C window
  or wheel; per view 58%-99%. 94% of the misses carry an 8.
- So on the current registry, L1 v1 (forbid u's row through its neighbour v) gets nothing on these rows.
- Narrow test: existing verdicts only; kills centred at v only (many misses would die at v's fives); exact 7s only.
- Guess check: "dies, about 3 closed" was right on the verdict and high on the count.

## Round 20 (16 Oct 2026, 15:41Z-): H-L2, do big-big transfers lower t* materially? (coordinator's test)

**Pre-registered 15:41Z, before any build.** Design and bars are Long Table's message of 15:32Z. The edge type, the
v-side separation and the guess are mine.
- **LP.** wlp3_j28_12's senders, rooted variables y and pattern set (sep3; 10 d = 10 patterns from Studio's
  `r_5..r_8.out` are not in this checkout). Rows are whole arrangements (d, link, s). Start set: Studio's 3,181
  tight rows (d = 7, 8, 9) and the 617-row d = 7 family. Without transfers this set reproduces t* = 13/49 (it holds
  the dual certificate); that is the baseline check.
- **Transfers.** A variable x[tau] >= 0 per oriented edge type tau = (deg u, deg v, the two sides of the edge
  uv, unordered), side = (common neighbour c, the vertex at u and c, the vertex at v and c). Both endpoints see all
  of it: at u, link k and its sides are L[k-+1], L[k-+2], S[k-1], S[k]; at v the same letters read off v's link.
  A row with a big link vertex gets -x[u->v] + x[v->u]. Degrees use letters 7, 8, 9 (9 = at least 9).
- **v side (cutting planes).** For every tau with x > 0, the heaviest arrangement at the receiving end that shows
  tau (5 link and 2 s letters fixed, the rest free over 5-9, its own transfer terms included) is found by a DP over
  6-letter states, then checked against R5/R6, RBIG and every pattern (sep3 `c`). Degrees 7, 8 and 9-12 for letter
  9. Violated allowed arrangements are added; y-only sep3 separation (d = 7-14) adds violated rows elsewhere.
  Iterate to no violation.
- **Survives** if t* < 0.22, or if the 49 HARD28-like rows all go slack. **Dies** if t* stays above 0.25 because
  v's rows bind. Report what binds.
- **Caveat.** Restricted LP, not a bound: rows outside what the separation reaches (y-only sep3 dedups by 5-path,
  degrees >= 13) are missing, so it can only overstate the gain. Kill-side results are trustworthy; survive-side
  results are a go signal for Studio to build L2 properly.
- **Guess.** t* falls, but not below 0.22: about 0.24. The slack big neighbours of round 19 absorb some load, but
  the d = 8 and d = 9 rows are tight too, so their v-rows start binding quickly. Most HARD28 rows go slack.

**Round 20 result (16:09Z): H-L2 dies. t* = 7/27 = 0.2593 with transfers (baseline 13/49 reproduced).** Details in
`wheeldis/loop/l2/FINDINGS.md`.
- t* stayed 7/27 at iterations 0-6 (up to 86,791 rows, 9,672 transfer columns). Stopped at the hour cap.
- What binds: five d = 7 u-rows, no d = 8-10 v-row. Three of them fit as their own 7-neighbour, so the edge reads the
  same from both ends and any 2-ball edge rule moves no net charge across it. The other two trade 2/9 and both bind.
- 44 of 49 HARD28-like rows go slack. The transfers do relieve them; the bound moves to self-paired d = 7 rows.
- Guess check: "about 0.24, v-rows bind" was wrong on both counts. The binders are u-rows next to their own copy.

## Round 19 (16 Oct 2026, 15:25Z-): H-B0, can a joint (u, v) LP beat the single-receiver bound? (coordinator's test)

**Pre-registered 15:25Z, before any build.** Test design is Long Table's message of 15:22Z. The precise kill reading and
the guess are mine.
- **Pairs.** As round 12's `certpair.py`: B fits at a link big v of A (degrees match, v's arrangement agrees with
  every letter A fixes). Certificates: Studio rounds 10, 11 and 12, and the explore oracle. Also the 49 HARD28-like
  rows of round 18 against every fitting row of the 617-row d = 7 tight family.
- **Union.** One patch built from A at u. B supplies v's p slots and v's ring-3 letters. Unknown letters are filled
  with 6 and never sit inside a configuration.
- **Configurations.** Centred at u or at v, over every S (|S| >= 2) of the centre's fives: B-fixed (S + N(S)) and
  receiver-centred (S + 5/6-neighbours), with defect_check2's ring repair. Each is looked up by `la.ckey` against
  every existing D/C verdict that has a dfast line. No new dfast or cfast.
- **Kill classes.** *single*: inside the centre's own arrangement (A at u, or B at v), which a single-receiver LP
  already sees. *joint*: the configuration needs letters from both arrangements.
- **H-B0 lives** if, for some certificate, every fitting pair is infeasible by a joint kill, or by a single kill on
  the *other* receiver (A's only consistent neighbours are forbidden). **H-B0 dies** if feasible pairs survive for
  every certificate.
- **Guess.** Joint kills are rare: B-fixed configurations at u or v live inside one 2-ball, so only ring repair can
  mix letters. H-B0 dies on the certificates. The HARD28-like rows may still show the lever: many of their
  fitting neighbours are already forbidden.

**Round 19 result (15:31Z): H-B0 dies as pre-registered. The slack at u's big neighbours is the positive side for B.**
Details in `wheeldis/loop/av/FINDINGS.md`.
- 23 fitting pairs over the certificates of Studio rounds 9-12 and the explore runs. 10 were built: **0 joint
  kills**. Every kill is single (the stale receivers are forbidden on their own by later verdicts). 13 pairs could
  not be built: Layered cannot close a ring-3 degree-5 vertex with three inner neighbours.
- Why: a configuration centred at u or v over its own fives lies inside that centre's 2-ball. Only pinched-ring
  repair mixes letters. Pair infeasibility from u/v-centred configurations is not the lever.
- 41 of the 49 HARD28-like rows (12 of the 15 HARD28) have a link 7/8 at which **no** row of the LP's tight set
  (617 d = 7 plus 1,519 d = 8) fits. Every arrangement possible there is slack at t*, so a transfer along that edge
  would lower u's row without making v bind. That supports option B through transfer variables, not pair rows.
- Guess check: "joint kills rare, H-B0 dies on the certificates" held.

## Round 18 (16 Oct 2026, 14:29Z-): H-LF, are the HARD28 rows artefacts of receiver-centring? (coordinator's test)

**Pre-registered 14:29Z, before any search.** Design and bars are Long Table's message of 14:23Z; the guess is mine.
- **Rows.** The 15 HARD28 rows plus the 34 other HARD28-like rows of `supply.py`: 49 rows.
- **Search.** `defectb9` (defectc9 with letters 5-9 on rings < K and the 2-ball fix of defectb7): centre 7, link and
  s fixed to the row, p slots free, K = 3, CMIN = 1. A 9 in a row is an exact 9 here, a sub-case of "degree >= 9".
- **Check.** Every leaf through `defect_check2 bf` (every 7 in the patch, every S). Existing verdicts only: f-named
  verdicts (Studio's r_*, explore windows) are bridged by canonical key (lemmaA `la.ckey`). No new dfast or cfast.
  A leaf that is not killed (SURVIVES or open) counts as surviving.
- **H-LF leads** if at least 2/3 of rows have no surviving leaf. **H-LF dies** if at least 1/3 of rows have one.
- **Caveat.** A search that puts a sea of 6s from ring 3 outward rules out isolated defects only. It does not show
  that a row is sound to forbid.
- **Guess.** Most rows have no leaf at all at K = 3: a 2-ball with 8s and 9s rarely closes into a positive defect
  inside a 6-sea (round 10's 7 binders had none at K = 3). So H-LF leads, and mostly vacuously. If that happens I
  will add K = 4 with letters 5-7 on the new ring (5-minute cap per row) as a less vacuous probe.

**Round 18 result (15:20Z): H-LF leads, with heavy caveats.** Details in `wheeldis/loop/lf/FINDINGS.md`.
- K = 3 (letters 5-9): 0 leaves in all 49 rows. Complete, but vacuous.
- K = 4 (free letters 5-7; every row capped at 2 minutes, cut from the pre-registered 5 to fit the hour, so incomplete): 1,521 leaves in 22 rows (4 of the 15
  HARD28). **All 1,521 are killed by existing verdicts** (1,042 through the f7_ bridge), and none of the kills is at
  the row's own 7. The nearest killing 7 is a link vertex of u for 45%, in ring 2 for 48%, and only in ring 3 for 7%.
- By the bars: 49/49 rows have no surviving leaf. The guess (mostly vacuous) held at K = 3 and not at K = 4.
- Reading: where these rows complete at all, a configuration centred at a neighbouring 7 kills them. That points
  the gate at a neighbour-aware LP rather than at ring 17+ windows at u. A 6-sea search rules out isolated defects
  only; it does not make a row sound to forbid.

## Round 17 (16 Oct 2026, 14:18Z-): ring-17 windows for the HARD28 rows

**Pre-registered 14:18Z, before any dfast run.**
- **Why.** Studio caps Job 28 at ring 16, so its 15 HARD28 rows get no more tests. Their exact windows sit at ring
  17-21. dfast handles rings up to 19, and a ring-17 test should take a few minutes.
- **Run.** The 6 untested ring-17 windows of the HARD28 rows (`loop/w2/win17.txt`). They cover 7 of the 14 rows still
  free (one window is shared by 3 rows, one of them already dead).
- **H-W5.** At least 2 of the 6 are D.
- **Kill.** 0 of 6.
- **Guess.** 1 of 6. Exact windows at ring 14 were D 21% of the time in round 14, and these carry 8s.

**Round 17 result (16:45Z): H-W5 dies, 0 D of 6.** The first run was vacuous: `bin/dfast` skips rings > 16, so all
6 came back SKIP (`win17_dfast16cap.out`). Rerun with `bin/dfast18`, one window at a time: all 6 are not D
(`loop/w2/win17.out`), at 4-7 minutes and about 25 MB each on one core. No cfast yet. Guess (1 of 6) was close.
Price of option A (inferred from these 6): a ring-17 B-fixed window costs about 5 core-minutes in dfast, and these
gave nothing.

## Round 16 (16 Oct 2026, 14:16Z-): small windows at d = 8 and d = 9

**Pre-registered 14:16Z, before any build of dfast lines.** (I counted the windows by ring; no new verdicts.)
- **Why.** Studio's round-12 tight set has 1,519 d = 8 rows and 1,435 d = 9 rows next to its 227 d = 7 rows. Job 28
  attacks only the d = 7 ones. Once the d = 7 rows are forbidden, these are the next to bind, and their small windows
  are almost all untested (about 2,200 at ring <= 14).
- **Configurations.** Round 14's small windows (|S| = 2-3, u at exact degree 8 or 9, N(S) exact, 9 -> B).
- **Run.** The untested ones at ring <= 14, after round 15 frees the cores.
- **H-W4.** They forbid at least 30% of the 2,954 d = 8/9 tight rows.
- **Kill.** Under 5%.
- **Guess.** A lower D rate than at d = 7 (about 15% of windows), and about 25% of the rows.

**Round 16 result (17:19Z): H-W4 survives, strongly.** 687 of 2,201 windows D (31%; guess 15%), in
`loop/w2/win89.out`. Coverage of Studio's round-12 d = 8/9 tight rows (`loop/w2/cov89.txt`): **1,911 of 2,954
forbidden (64.7%)**: d = 8 800 of 1,519, d = 9 1,111 of 1,435 (bar 30%; guess 25%). Before this round no d = 8 row
was forbidden by any registry window. The D windows go to Studio as patterns; the next LP shows what t* does.

## Round 15 (16 Oct 2026, 14:15Z-): 8-relaxed windows against the rows round 14 left

**Pre-registered 14:15Z, before any dfast run.** (I counted the untested windows first; no verdicts were looked at.)
- **Why.** Round 14 left 427 of 617 rows. 331 of them have an 8, and an exact 8 pushes the windows to ring 15-21.
  One HARD28 row died to a window whose 8s were free (B).
- **Configurations.** An 8-relaxed window is a round-14 window (|S| = 2-3) with every 8 made a free ring vertex
  (B = 7/8/9). 7s stay exact. One D forbids the window with 7, 8 or 9 in those places.
- **Run.** The 565 untested 8-relaxed windows of the 331 rows, at ring <= 16.
- **H-W3.** They forbid at least 5 of the 14 HARD28 rows still free, and at least 20% of the 331 rows.
- **Kill.** 0 HARD28 rows and under 5% of the 331.
- **Guess.** About 15% of windows D (below round 14's 28%, since 8s move onto the ring). About 4 HARD28 rows, about
  20% of the 331.

**Round 15 result (16:12Z): neither bar met; leans dead.** 23 of 565 windows D (4.1%; guess 15%). Coverage of the
617-row family (`loop/w2/cov3.txt`) goes from 190 to 218 forbidden: 28 more rows, 8.5% of the 331 with an 8 (live
bar 20%, kill bar 5%). **0 of the 14 free HARD28 rows** fall (kill side). 46 of the 49 HARD28-like rows stay free.
Freeing the 8s does not reach the HARD28 rows; with round 20, the binding d = 7 rows are now self-paired ones.
The 23 D windows (`loop/w2/win8.out`) go to Studio as patterns.

## Round 14 (16 Oct 2026, 14:05Z-): small B-fixed windows across the d = 7 tight family

**Pre-registered 14:05Z, before any build.**
- **Why.** Studio's round 12 reached t* = 13/49. Its certificate has 4 d = 7 receivers with mostly shared fives (7-5-7).
  Job 28 tests the largest S first, at most 3 per arrangement, so the small windows are skipped.
- **Small windows.** A small window is a B-fixed configuration with |S| = 2 or 3 and u at exact degree 7. Its f7_
  name has '.' outside S's letters, so one D forbids every arrangement that contains the window.
- **Family.** `loop/e7/tight7.txt` (478 rows), plus Studio's round-12 certificate, plus the HARD28 example
  5567586/5758756.
- **H-W2.** Untested |S| <= 3 windows at ring <= 14, plus the D windows already in the registries, forbid at least
  30% of the family.
- **Kill.** Under 5%.
- **Guess.** About 20%.

**Round 14 result (14:12Z): H-W2 survives, just.** Details in `wheeldis/loop/w2/FINDINGS.md`.
- 617 distinct d = 7 rows. 636 untested windows at ring <= 14; **dfast: 178 D** (28%).
- Rows forbidden: 73 before (Studio's round-12 partial verdicts), **190 after (30.8%)**. The bar was 30%, and the
  guess was 20%.
- The 7-5-7 family with letters 5-7 is gone: 20 of 21 rows with only shared fives die.
- What survives has an 8 near S. Exact 8s put the windows at ring 15-21.
- The 4 receivers of 13/49 were already forbidden by Studio's round 12. Shared fives carry 81% of its sender weight.
- HARD28: each row's only window at ring <= 16 is the 5-5 pair (not D). One row still dies, to a window from a 9-row
  sibling whose B also matches 8.

## Round 13 (16 Oct 2026, 14:15Z-): receiver-free windows with a big link vertex (the 3/11 family)

**Pre-registered 14:15Z, before any build.**
- **Family.** The d = 7 arrangements tight at a 3/11-style optimum. These are the tight rows of my round-9 runs
  (`hr1_base`, `hr1_long`, `hr1_or1`) and the certificate receivers of Studio's rounds 9-11.
- **Configurations.** Like round 7's `ufree.py`, but S may contain fives whose non-u neighbours include link bigs:
  - S + N(S) - u, with 7/8 at exact degree and u on the ring with its degree free;
  - S has 2-4 fives in an arc of at most 5 link positions;
  - one D verdict forbids the window at every d = 7..17.
- **H-E7.** Windows of this kind that are D at ring <= 15 forbid at least half of the tight d = 7 arrangements.
- **Kill.** Under 10%.
- **Guess.** About 30%: the 575 windows with every s = 6 die, and the ones with s = 5 next to the 7 do not.

**Round 13 result (14:00Z): H-E7 dies.** Details in `wheeldis/loop/e7/FINDINGS.md`.
- 478 tight d = 7 arrangements gave 752 windows. 73 have a simple ring, and 56 have ring <= 15.
- **dfast: 0 D of 56**, against a guess of 30%.
- Why: at d = 7, a 5-position window wraps around the 7. Its ring is not simple, and the repair puts u back in at
  exact degree, which is Job 28's B-fixed family.
- So the 3/11 family cannot be killed with d-free windows, as the lone fives were. It needs B-fixed configurations at
  u = 7, run on the whole tight family rather than one certificate pair per round.

## Round 12 (16 Oct 2026, 13:50-14:10Z): H-AV, pair averaging between adjacent bigs

**Pre-registration.** Long Table's message of 13:47Z: pair rows charge(u) + charge(v) <= 2t take t* below 3/11;
kill if t* stays >= 3/11. I added no guess before computing.

**Result: H-AV dies, exactly for the pair-row model.** Details in `wheeldis/loop/av/FINDINGS.md`.
- Studio's round-11 certificate (`out/wlp3_j28_11.txt`) has two receivers, 5756575/6565666 and 5765756/5566666.
  Each can sit next to a consistent copy of itself (`pairs.py`).
- So the same dual combination, written with pair rows, certifies t >= 3/11 in the pair model.
- The same holds for Studio's round 10 and for the explore oracle certificate (`certpair.py`).
- This does not settle transfers that depend on both 2-balls (class b): the self-pair edge is oriented.

**Reading.** The 3/11 plateau is a family, the way 2/7 was lone fives. In the current pair every five is shared with
a link 7 (senders 56677 / 66677 / 56776). The proposed attack is the lone-five playbook: count the family, then use
edge-centred configurations (two adjacent 7s with their common fives).

## Round 11 (16 Oct 2026, 12:40Z-): binder coverage with degree 8 and deeper defects

**K-cap (H-K), withdrawn before any run.**
- The coordinator proposed forbidding arrangements with more than K letters >= 7.
- That is not sound: no lemma bounds the bigs in a receiver's 2-ball, and round 10 shows that dense arrangements
  complete to locally consistent defects.
- It would also delete 559 of the 562 tight rows at the 33/119 optimum. Only 3 have <= 2 bigs.

**Pre-registered 12:42Z.**
- **Binders.** The 4 that `b7f.out` does not forbid: 5575576/6666656, 5765575/7565777, 5567576/6755556 and
  5765756/5556666.
- **Question.** Do they complete to positive isolated defects that survive R_opt+, either at K = 4 with letter 8,
  or at K = 5 (capped)?
- **H-B8.** Every completion found dies to R_opt+.
- **Kill.** A completion survives with every configuration tested.
- **Guess.** The letter-8 K = 4 searches finish under the 20-minute cap for at most 2 of the 4. K = 5 is far from
  complete. Everything found dies, mostly at the centre.

**Round 11 result (13:46Z).** Details in `wheeldis/loop/b7/FINDINGS.md`.
- **K = 4 with letter 8** (20-minute cap): 1,634 leaves, complete for 5575576. All are killed by the existing
  registry, every one by a D, and they stay killed with `strict7`.
- **K = 5, letters 5-7** (10-minute cap): 423,160 leaves.
  - Checked: all of the two small sets and a 1/50 or 1/20 sample of the two large ones, 10,309 leaves in total.
  - All are killed, after 452 new dfast tests at ring <= 14 (216 D).
- **H-B8 survives** (the K = 5 part is sampled).
- **Guess check.** Only 1 of the 4 letter-8 searches finished, not "at most 2". Kills were mostly at the centre in
  round 10; I did not re-split them here.

## Round 10 (16 Oct 2026, 12:30Z-): do the d = 7 LP binders sit inside an isolated defect? (coordinator's suggestion)

**Pre-registered 12:30Z, before any matching.**
- **Binders.** 7 arrangements at d = 7: the 5 from the 33/119 baseline certificate (`wlp3_hr1_base.txt`) and the 2 from
  the oracle certificate (`wlp3_hr1_or1.txt`).
- **Question.** Can a binder's 2-ball (u = 7, link and s fixed, p slots free) be completed to an isolated positive
  defect (README §7 test G) centred at u?
  - K = 2 is impossible by inspection: every binder has an s letter that is not 6, at distance 2.
  - So the test is K = 3 (`loop/g9/g9_K3_c7.out`, complete, letters 5-8, CMIN 1) and K = 4 (`c7k4.txt`, partial).
- **H-B7.** No binder completes to a K = 3 leaf. Any K = 4 completion dies to R_opt+, like every K <= 4 defect so far.
- **What each answer means.**
  - No completion: the binders are not test-G obstructions near u. They are obstructions of the rooted-word rule
    class only, so a richer rule (README §7 classes a-c) or larger configurations could remove them.
  - A completion that survives R_opt+: a test-G defect. Then t* > 0 for every finite-reach rule, and H7 dies.
- **Limit.** Defects whose non-6 part reaches distance >= 4 from u are not covered (K >= 5).
- **Guess.** 0 completions at K = 3. At K = 4, a few completions, all killed by B-fixed configurations at other 7s.

**Round 10 result (12:30-13:00Z).** Details in `wheeldis/loop/b7/FINDINGS.md`.
- **K = 3:** no binder completes. That holds for all 7, letters 5-8.
- **K = 4** (letters 5-7, complete for these 2-balls, via `defectb7`, a defectc8 with the 2-ball fixed):
  - 5 binders complete, with 2,064 leaves in total. 5575576/6666656 and 5676575/6556666 have no completion.
  - All 2,064 die to R_opt+, every one by a D configuration, and they stay dead with `strict7`.
  - Kills: the existing registry gives 1,973. New dfast at rings 10-15 gives the rest: 105 D of 260 at ring <= 14,
    2 of 8 at ring 15.
- **By-product: 4 B-fixed D configurations that forbid binders directly** (`loop/b7/b7f.out`; rebuilt by gen28 and
  rerun with dfast):
  - **f7_5567576_56.75.7** (r15) forbids the heaviest baseline binder, 5675765/6575575 (dual 0.20). That binder's
    1,536 K = 4 completions all die to it at the centre.
  - f7_5656757_657.555 (r13) and f7_..65757_..6555. (r12) forbid 5675756/7555565.
  - f7_..55756_..6666. (r13) forbids the oracle binder 5676575/6556666.
- **Verdict: H-B7 survives.** Near u (K <= 4) the d = 7 binders are not test-G obstructions, and 3 of the 7 are now
  forbidden as patterns. I guessed a few K = 4 completions, all killed at other 7s; in fact most kills sit at the
  centre.
- **Not run:** K = 4 with letter 8; K >= 5.

## Rounds 8-9 (16 Oct 2026, 10:00-12:10Z): H-L3, then the two-step rule class (H-R1)

**Round 8, H-L3** ("the remaining lone-five arrangements cannot be killed from distance-2 data"): dies as worded.
Details and table in `wheeldis/loop/lone/FINDINGS.md`. The surviving completions of A1 (d = 10, link 5656556565,
every s = 6) have a big vertex p at distance 2 from u, reached from a lone five through a 6.

**Ring-16 batch (background, finished 11:05Z).** Receiver-free: 3 D of 20 (`u10.out`). B-fixed: 6 D of 29 (`b10.out`).
- Recount with every pattern so far (`lone10.txt`): d = 9 max 4 lone fives (2 arrangements), d = 10 max **5** (15),
  d = 11 max 6 (7), d = 12 clear.
- **A1 is dead**: its link contains the window 5565655 with s = 666666, the ring-16 receiver-free D configuration
  z_5565655_666666. So the six-lone-five counting bound at d = 10 (2/7) is gone. The counting bounds left are
  1/5 (d = 9), 1/6 (d = 10), 1/7 (d = 11).

**Round 9, H-R1, pre-registered 11:10Z before any LP run.**
- Coordinator wording: a 5 -> 6 -> big rule takes t* below 2/7 at d = 10. A1's death overtakes that, so it is tested
  against the new one-step baseline t_B.
- **Hypothesis.** A 5 -> 6 -> big rule lowers t* below t_B.
- **Definitions.** A lone five w_i has a *second-ring route* if a 6-neighbour has a neighbour at distance 2 from u that
  the arrangement leaves open (the p slot of a link 6, w_i-1 or w_i+1) or fixes as big. Routes that only reach
  third-ring vertices do not count.
- **Test.**
  - Baseline: wlp3s (stall 25) with every pattern so far (pats0, u*.pat, b*.out, out/job28/r_2-4, loop/g9 D outputs).
  - Oracle: forbid each binding lone arrangement in which every lone five has a second-ring route, as if the rule
    fully relieved it, and rerun.
  - The oracle ignores the load the rule puts on p, so it is optimistic for H-R1.
- **Kill.** Any of these kills H-R1:
  - the oracle's t equals t_B;
  - the oracle's new bound is set by an arrangement with a lone five that has no second-ring route;
  - the baseline binders are not lone arrangements at all.
- **Guess.** t_B is between 1/5 and 1/4 and is set at d = 9 (link 566565656, four lone fives, all on link 6s with p
  slots). H-R1 then survives the oracle. It still needs the p-small completions to be reducible.

**Round 9 result (11:05-12:10Z, over the 30-minute cap because each LP iteration takes about 40 s).**
- **Baseline** (`loop/lp/wlp3_hr1_base.txt`, stall stop): t* >= 0.2773 (33/119), so the guess was wrong.
  - The certificate is five **d = 7** receivers, each carrying 0 or 1 lone five; the largest dual is on
    5675765/6575575.
  - d = 10 has slack (load 4.11 against 4.28). d = 9 still had a violated row at the stop, so the true t* can be
    higher.
  - A stall-80 copy (`hr1_long`) stopped with the same certificate (33/119) after 80 flat iterations, still with
    violated rows at d = 8 and 9. So the separation is degenerate there, and the one-step t* is only known to be
    >= 33/119.
- **Relief against load at the binders.**
  - Each binder has at most 1 lone five that the rule could relieve.
  - Each also has 1-2 second-ring fives (an s = 5 next to a link 6) that would send z into u through that 6, plus
    open p slots.
  - So with one z per target class, the rule adds at least as much load as it removes.
- **Oracle** (`hr1_or1`): the 4 routed binders forbidden, warm start. Stall stop at t >= 3/11 (0.2727).
  - Its certificate is two d = 7 receivers: 5676575/6556666 (1 lone five, 2 inflow fives) and 5765756/5556666
    (**no lone five**, 2 inflow fives).
- **Verdict: H-R1 dies (inferred, not a solved two-step LP).**
  - The binders moved to d = 7.
  - The oracle's bound rests on a receiver with no lone five to relieve.
  - Every binder takes at least as much two-step inflow as it sheds.
  - The spec for a faithful LP is `wheeldis/loop/lone/TWOSTEP.md`. It is not worth building while the binders sit at
    d = 7, where Studio's certificate loop already works.
- **G9:** the centre-8 K = 3 search is complete. The remaining 1,429 ring-1 words gave 0 leaves, so all 376 die.

## Rounds 6-7 (16 Oct 2026, 08:35-10:00Z): the LP floor after the d = 7 certificate, and the lone-five family

**Certificate (G2).** A1308's S = (0,5) at ring 14 is C (cfast, |X| = 1; `loop/rules/cert_bf.cfast`). So every
arrangement in the 5/17 and 1/5 certificates now has a reducible B-fixed configuration: 4 D, 1 C.

**LP after forbidding them (`loop/lp/`).**
- `loopfast.py` is a local Job 28 loop that takes the largest S first. `wlp3s.py` is wlp3 with an early stop: once t
  has not risen for 25 iterations it stops, and the dual of the rows found so far is a valid certificate that t* is
  at least the printed t.
- Result: **t* >= 2/7** (5/17 before). A full run stayed at 2/7 for about 90 iterations before I stopped it.
- The 2/7 is carried by a single receiver: d = 10, link 5656556565.
  - All six of its fives are **lone**: u is their only neighbour of degree >= 7.
  - So 6(1 - t) <= 4 + t for any rule that moves charge from a 5 to its big neighbours. This is a counting
    obstruction, so only reducibility removes it.
  - Its ring-16 B-fixed sets are D, and so is a ring-14 one. The next round moved to a sibling arrangement.
- Long Table then gave the LP loop itself to Studio (loop28b), so this thread stopped its loop.

**Lone-five family (`loop/lone/`).**
- **Question.** Which arrangements have more than d - 6 lone fives and contain no forbidden pattern?
  - `lone.py` answers it with sep3, using weight 1 on lone rooted words.
  - Before this round the answer was non-empty for every d = 9..15: up to 4, 6, 7, 8, 8, 9, 10 lone fives.
  - d >= 16 is clear on the old patterns alone (checked up to d = 20; the maximum is floor(2d/3)).
- **Receiver-free configurations** (`ufree.py`).
  - The configuration is S plus all neighbours of S except u, at exact degree. u stays on the ring with its degree
    free, so the configuration is the same at every d.
  - **62 of them are D**, at rings 10-15. Examples: z_55655_5665 (r10); z_55655_6666 (r12), two adjacent five-pairs
    with a 6 between them and every s = 6; z_556556_66666 (r14).
  - As patterns for d = 7..17 (`u*.pat`), they clear d = 13, 14, 15.
  - What is left: d = 9: 3 arrangements, d = 10: ~59, d = 11: 13, d = 12: 2.
  - These went to Studio as wlp3 patterns.
- **B-fixed sets of lone fives** for the rest (`bfix.py`, `iter.sh`). At ring <= 15, 24 more configurations are D.
  - 48 arrangements are left: d = 9: 2, d = 10: 31, d = 11: 13, d = 12: 2.
  - Most of them are lone fives alternating with 6s (e.g. 5656565656 with every s = 6), or 556 blocks with every s = 6.
  - Ring 16 is running in the background: 20 receiver-free configurations, plus 29 B-fixed at d = 9, 11, 12. Studio
    covers d = 10 at ring 15-16.
- **Reading (a hypothesis, not checked).**
  - In a real map, a 6 next to a lone five whose other neighbours are all 6 is the Job 17 D 6-wheel 566666.
  - So these arrangements need a big vertex at distance 3, which an arrangement that records only w and s letters
    cannot see.
  - If ring 16 does not clear them, the LP needs either third-ring letters in the arrangement or rules that pass charge
    through a 6.

**G9, defects with an 8 or a big centre (`loop/g9/FINDINGS.md`).**
- Ring letters 5-8 at K <= 3: every leaf with an 8 dies to a D receiver-centred configuration. Centre 8 is partial and
  still running.
- Centres 9-12:
  - K = 2 has no leaves. With ring 2 all 6, a ring-2 vertex next to a five is a Job 17 D 6-wheel (566666 or 556666).
  - K = 3 (capped) gave 1,952 leaves. All die after 1,801 new ring <= 12 dfast runs.
- The LP's d = 10 arrangement cannot be completed to a K = 3 defect.

**G7 closed for K <= 4.** The full audit of all 418,551 candidates had 0 nosimple and 0 bf_nosimple kills.
defect_check2 now counts an unrepaired non-simple ring as open.

**Kernels.** Both ring-9 lemma-A kernels went to Studio as dfast lines (`loop/lemmaA/kern9.txt`). The first is
certified in Lean (dcheck/LemmaAKern9.lean, Studio).

**What changes.**
1. The LP's obstruction after d = 7 is the lone-five family at d = 9..12. It is a pure counting bound, so the lever is
   reducibility, not the rule class.
2. Receiver-free configurations are the efficient tool. One verdict covers every receiver degree.

## Rounds 4-5 (16 Oct 2026, 07:40-08:50Z): stepped up, four parallel streams

Kyle asked for more effort, so four gaps ran at once: three workers plus this thread. Each stream has a FINDINGS.md
under `wheeldis/loop/`.

**R (G2, rules; `loop/rules/FINDINGS.md`, LP only).**
- **Question.** Can a richer rule class beat the 5/17 bound at d = 7?
- **Answer.** No. The 5/17 dual certificate rests on two receiver arrangements, R1 (link 5567576, s 5755556) and
  R2 (link 5576576, s 5756656), with weights 1:2.
  - Their shared 7s are mirror images over the union of both arrangements.
  - So no rule that sees only that union can separate them. Classes (b) and (c) both stay at 5/17.
  - The lever is reducibility of R1 and R2, not the rule class. This corrects README §6.1's reading.
- On the HARD d = 7 rows, class (c) lowers the floor from 11/39 to 1/5. Its certificate uses A1402, A1308 and A2581.

**R follow-up: are the certificate arrangements reducible?** (`loop/cert_bf.py`, `loop/rules/cert_bf*.{txt,out}`)
- **Yes, for four of the five.** Every B-fixed S was built and run through dfast (24 configurations, rings 11-16).

| arrangement | B-fixed S that are D (ring) | not D |
|---|---|---|
| R1 | (0,4) r12, (1,4) r13, (0,1,4) r13 | (0,1) r11 |
| R2 | (0,4) r13, (0,1,4) r15 | (0,1) r12, (1,4) r15 |
| A1402 | (0,1,4) r15 | 3 others |
| A2581 | (0,2,5) r14 | 3 others |
| A1308 | none of 7 tested | (0,1,4) at ring 16 pending |

- So the 5/17 certificate falls once these configurations are forbidden, and so does most of the 1/5 one.
- Job 28 did not see this: it tries the smallest-ring S first, which is (0,1) here and is not D. It should try the
  largest S first.

**A (G1, lemma A; `loop/lemmaA/FINDINGS.md`).**
- **Question.** Is lemma A ("a 7 with >= k fives carries a reducible B-fixed configuration") true as a finite
  statement over every neighbourhood?
- **Answer. No, not as a blanket lemma.**

| case | D at ring <= 14 | rest |
|---|---|---|
| k = 5, degrees <= 7 | 252 of 291 | 39 misses, all on link 5557557, with untested ring 15-16 candidates |
| k = 4, outer 8 / 9+ allowed | ~3% | candidates mostly at ring >= 17, ~10^6 CPU-h |
| k = 3 | 290 of 421 instances | 87 with none at ring <= 15 |

- Round 1's 186/186 came from 6-sea defect patches, whose neighbourhoods are mostly 6s.
- So K = 2 stays defect- and LP-driven, as in Job 28.
- By-product: 29 of 40 k = 5 hits reduce to one ring-9 kernel. It is u = 7 with fives at w0, w1, w2, and
  s0 = 5, s1 = 7, s2 = 5. It is cheap to put in Lean.

**E (G4/G7, appears; `loop/appears/FINDINGS.md`).**
- **Is "non-simple ring ⇒ killed" in defect_check2 sound?** Not as a rule. A census graph (p25#6000) has an
  unrepairable chord and no short separating cycle.
- **Does it ever fire?** Not on a 1/20 sample of the 418,551 K <= 4 candidates: all 352,886 non-simple rings there
  were repaired by the fill. A full rerun is in progress.
- **B2 for receiver-centred configurations.** It extends to the interior (hand sketch).
- **Rings.** In 38,872 census graphs, 11,187 (u, S) rings stay non-simple after the fill. They are chords and folds;
  there are no pinches.
- So "appears" needs one of two things: PinchWalk extended to arcs of length 1-2, or the plan listing the filled
  variants.

**K = 5 defects (G8; this thread; `loop/defectr.cpp`, `loop/defectr2.cpp`, `loop/k5hunt.sh`, `loop/export_keys.py`).**
- **New tools.**
  - `defectr` is a randomised `defectc`.
  - `defectr2` also prunes inside the DFS whenever a 7 has a reducible receiver-centred key (8,827 keys at d = 7).
  - Validation at K = 3: the pruning removes 3,840 leaves; defect_check2 kills 3,833 of them and leaves 7 open. The 7
    are pinched cases, which the key test ignores.
- **Without pruning.** About 950 K = 5 candidates were sampled. All were killed by plain receiver-centred
  configurations.
- **With pruning.** About 660 randomised seeds (centres 5 and 7, strict tables) produced 0 R_opt survivors.
- **Guided.** All 15 extensions of D3 to K = 5 are killed.
- **Conditional on A3.** Complete K = 5 runs (centres 5 and 6, 45 min cap) have produced 0 leaves so far.
- **Caveat.** These are samples, not a complete search. All defect searches use degrees 5-7 only, so clusters with a
  vertex of degree >= 8 are untested (new gap G9).

**What changes.**
1. Give Job 28 the B-fixed sets of R1, R2, A1402 and A2581, which are D now, as forbidden patterns and re-solve. Order
   gen28 variants largest S first.
2. Drop "K = 2 = lemma A" from the plan wording. Keep the ring-9 kernel as a Lean candidate.
3. In defect_check2, make an unrepaired non-simple ring "open" instead of "killed".

## Round 3 (16 Oct 2026, ~06:25Z): gap G3, is lemma B (7-wheel 5666567 C-reducible) real?

**Question.** E1/E2 (and D1/D2 under R_opt) die only to the cfast C-candidate 5666567. Does a second engine agree?
**Result: yes, two engines now.** `wheeldis/loop/kempe_w7_5666567.py` (+ `.out`) is written from textbook definitions
without reading dfast/cfast/Lean. It reproduces cfast exactly: 66,430 ring classes, 7,372 extend, D-closure 53,690
good and 12,740 bad (fixpoint after 19 levels). It cross-checks its coarsest-partition shortcut against brute force on
600 sampled classes (0 disagreements).
- X = {I0-I1, I0-I3, R2-I3} (|X| = 3; bigwheels.txt indexing) is admissible (no loop), and all 2,668 classes that
  extend after contraction are good. The |X| = 4 variant with R0-I2 added gives the same 2,668 classes and also works.
- cfast found 437 working X of size <= 4 on the defect-indexed copy, so the verdict does not hang on one X.
**Next.** Lean, as for CWheels.lean (Job 21). This wheel is cheap at ring 13. Then lemma B counts at the programme's standard.

## Round 1 (16 Oct 2026, 05:15-06:10Z, cloud thread "pace"): gap G1, what kills the defects near 7s?

**Question.** D1-D3 avoid R_opt but die to B-fixed configurations. Is there one simple family behind that?
**Guess.** Yes: 7s with many five-neighbours. D3's ten 7s have 4,4,3,3,3,3,2,2,1,1 fives.
**Would change the plan if:** assuming that family reducible leaves no K <= 4 defect. Then G1 reduces to one lemma
instead of a 5·10^5 CPU-h B-fixed enumeration.

**Probe 1a, sample** (`wheeldis/loop/bfsample.py`). Took every 7 in the R_opt-free K = 3 patches of charge >= 0 (all
centres; `bin/defectc ... 3 0`: 171 + 337 + 1,056 patches). Built every B-fixed configuration (u + S + all links of
S at exact degree, |S| >= 2). Ran dfast on 25 random ones per class at ring <= 14.

| fives at u | D fraction for \|S\| = 2 | for \|S\| = 3 | for \|S\| = 4 | for \|S\| = 5 |
|---|---|---|---|---|
| 2 | 8/25 | | | |
| 3 | 14/25 | 19/25 | | |
| 4 | 12/25 | 22/25 | 24/25 | |
| 5 | 15/25 | 22/25 | 21/25 | 24/25 |

**Probe 1b, per instance** (`loop/bfinst.py`, ring <= 15, largest S first, stop at the first D). This asks whether
every 7 with >= 3 fives has some D B-fixed configuration. After 150 distinct instances:

| fives at u | instances | some B-fixed config D at ring <= 15 |
|---|---|---|
| 3 | 90 | 81 (9 not) |
| 4 | 46 | 46 |
| 5 | 14 | 14 |

**Probe 1c, conditional defect search** (`loop/mktables.py` marks every 7-wheel with >= T fives as bad, then
`bin/defectc`, then `defect_check2.py` against the existing R_opt registry; 600 s cap per run):

| assumed reducible | K = 3 (complete, centres 5/6/7) | K = 4 (partial, capped) | survivors of R_opt |
|---|---|---|---|
| 7 with >= 3 fives | 2 / 22 / 0 candidates | c5 47, c6 107, c7 1,092 | **only E1 and E2** |
| 7 with >= 4 fives | 4 / 30 / 1 | running | none at K = 3 |

E1 and E2 are the two defects that die only to the 7-wheel C-candidate 5666567 (cfast, |X| = 4, triad).

**Reading.**
- Under (A) "every 7 with >= 3 five-neighbours carries a reducible configuration" and (B) "5666567 is C-reducible",
  no K <= 4 defect found so far survives. The K = 4 searches are partial.
- (A) holds on every 7 with 4 or 5 fives sampled (60/60). For exactly 3 fives it holds 81/90. The 9 misses are the
  next round.
- So G1 now looks like two lemmas, not an enumeration. H7b and Studio Job 28 (complete runs) are the confirmation.

**Next rounds.**
- R2: the 9 three-five misses. Do C, larger S with B >= 8 fixed, or ring 16 (dfast18) kill them?
- R3 (G3): an independent closure for 5666567, as abec3fca did for w66666.
- R4 (G2): forbidden-pattern LP with (A) as patterns at d = 7, to see whether a rule reaches t* <= 0.
