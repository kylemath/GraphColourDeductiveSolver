# K_frame_kill: w2 frame link 7696575 / s 5555977 above ring 15

Question: is some window of w2's frame (link 7696575, s 5555977; s1 = 9, x4 = 9 open) at ring 16-18 (19-20 if cheap) D or conservative-C (each X-component <= 1 ring vertex, no other edge inside, |X| <= 4), confirmed on a second engine?
Guess: yes, ~60%: a w2-centred window with the whole link plus the s'0/p/x2/x3 fives (five-cluster) at ring 16-17 goes C.
Plan-changer: if every ring 16-17 window is not D and kc-C finds no admissible X with small leftover, stop depth and go breadth to non-centred five 2-balls; if those also fail at 18, report the frame alive.
H-K kill line: some window at ring 16-18 is D or conservative-C on two engines; H-K dies if 0 hits among all windows built at rings 16-18.

## Result (10:33-12:06Z, 2 cores)
Windows: `kwin.py` = every connected subset I of the 13 known vertices (w2, L0 L1 L3-L6, s0-s3 s5 s6; L2 = s1 and x4 at
>= 9 stay ring), w2 in (fc7_) or out (fn7_), with a simple induced ring, on one gen.py layered disc; dedup by lemmaA ckey.
819 distinct windows (`all.txt`): ring 6-14: 351, 15: 131, 16: 143, 17: 117, 18: 62, 19: 15 (full window = ring 19, m 13).
Engine: explore's kc -C (built here as `kcc` from kc.cpp on nh6pv2), conservative admissibility (default, not -C2).
Tested (D then C |X|<=4), all not D and C=false:
| ring | tested | D | C | best leftover |
|---|---|---|---|---|
| 6-14 | 351/351 | 0 | 0 | - |
| 15 | 40/131 (m >= 8 first) | 0 | 0 | 1162 |
| 16 | 21/143 (m 11, 10, most m 9) | 0 | 0 | 2782 |
| 17 | 6/117 (all m 11) | 0 | 0 | 6402 |
| 18 | 1/62 (fc7_76.6575_5555..7, m 12; 42 min, 259 MB) | 0 | 0 | 20140 |
No hit, so no second engine was needed; kills.txt has no kill line. Best C leftover grows with ring (1.2k -> 2.8k -> 6.4k
-> 20k), so the frame shows no sign of dying at 19-20 from frame letters alone. H-K (some ring 16-18 window D or C) is
not confirmed: 0 hits among 28 windows at ring 16-18 (the highest-m ones); untested: 122 r16, 111 r17, 61 r18, all r19.
Logs: run_A.log (ring <= 15), run_A2.log, run_B.log (incl. the r18 run), r18a.kc.
