# 2b362955 replay at t = 0.041565: receiver violators (Studio, 7 Nov)

Stack: sol_c_repaired (e0ad3fcc) at 8313/200000, keep95p131f tables, masks and receivers, F2B = rules_zcons_minus_W18rejects.json (2b362955),
separator sep3r_f2bS_fix, all rotations, SEPCLASS=1, run by rot/run_w18.sh (logs rot/run/w18_d*.log). Bound for a degree-d receiver: load <= d - 6 + t.

**All violators are exact.** The separator reports them, and the Python exact re-check confirms each one (`exact violated` = `reported`). None is undecided: there is no timeout or cap.

Every other degree passes: d = 8 and d = 10..17 have 0 exact violators, and DP 18..30 and the Karp tail are clean.

## d = 7: 5 violated rows, 3 classes up to rotation and reflection (the log reports SEPCLASS classes separately); bound 1.041565

| # | link | apex word | exact load | excess over bound | rows in class |
|---|---|---|---|---|---|
| 1 | 5569757 | 5655667 | 1.074998584 | 0.033433584 | 1 |
| 2 | 5569757 | 5665667 | 1.074998584 | 0.033433584 | 3 |
| 3 | 5569757 | 5675667 | 1.074998584 | 0.033433584 | 1 |

## d = 9: 5 violated rows, 1 classes up to rotation and reflection (the log reports SEPCLASS classes separately); bound 3.041565

| # | link | apex word | exact load | excess over bound | rows in class |
|---|---|---|---|---|---|
| 1 | 555665666 | 697766656 | 3.116266335 | 0.074701335 | 5 |

