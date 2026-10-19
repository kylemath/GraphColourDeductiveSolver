# RSST 2.126 and 8406.123 under our contract (Long Table 22:33Z, BORROWED-CHANNEL-2.md at 2417a735)

Source: the repo's RSST data that produced the rsst* verdict lines: studiointel/routeb/rsst/unavoidable.conf (2.126 at
line 55, 8406.123 at line 11853), as kc lines by loop/k44/rsst2kc.py in loop/k44/rsst.txt (line 4 rsst003_2o126,
line 434 rsst433_8406o123); lines.txt here. Explore's results were not read first.

Near-triangulation (ntcheck.py: every interior wheel one cycle, Euler 2):
- 2.126: ring 8, m 4, interior degrees 6,5,6,5 (I0, I2 the 6-6 edge, I1, I3 the five tips), as the doc says.
- 8406.123: ring 12, m 8, interior degrees 8,5,7,6,5,5,5,5 (the doc's 8,7,6,5,5,5,5,5).

Our contract: both REFUSED (kill line met).
- 2.126: kc -C -s 60 -t 600 D=false; C=false, |X| <= 4, 701 admissible of 3,213 tested, best leftover 11. dfast18
  D=false. cfast search finds no X.
- 8406.123: kc D=false; C=false, 22,514 admissible of 46,937, best leftover 10. dfast18 D=false. cfast search no X.
- Neither timed out. RSST's own X (loop/k44/rsst_verdicts_C2.txt) merges ring vertices: 2.126 X={R0-I0,R2-I0,R4-I2,
  R6-I2} joins R0~R2 and R4~R6; 8406.123 X={I0-I2,R0-I0,R2-I0,R4-I2} joins R0~R2~R4. Our ring-merge guard holds both.
No f-name, no twoeng run, no new head.
