# Night batch n1 (18 Oct 2026, from 08:4xZ)

Target: the 7/27 certificate (receiver d=7 5675765/6577575; senders 55667, 55767, 77777) and the d=7 pair
5567576/5756756, 5586576/5757756 B-fixed windows. Engine: studio15/cfast --search --limit 1, nice 20, 1 core each.

| Run | Windows | Cap | Hypothesis | Kill line |
|---|---|---|---|---|
| r18_1, r18_2 | f7_.558657_.57.77., f7_5567568_56.77.7 (ring 18, dfast18 not D) | 8 h | at least one is C-reducible, which kills the d=7 pair row | cap hit or `neither` -> report TIMEOUT/neither, no rerun |
| w17_1..6 | loop/w2/win17.txt (6 ring-17 HARD28 windows, all dfast18 not D; 5 never ran, 1 killed at the 16 Oct pause) | 2 h | some are C | cap hit or neither -> stop |
| r16_1..3 | f7_5567576_56.76.7, f7_5567567_56.77.6, f7_.557657_.56.77. (2 h TIMEOUT on 17 Oct) | 6 h | the search finishes, and at least one is C | cap hit -> undecided, stop |

Any C needs a C-capable second check before it counts. After any C that touches the certificate: re-solve wlp3 notx.
