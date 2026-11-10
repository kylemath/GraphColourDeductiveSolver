# ST-111 RSST-substitute window 20 second check (Studio, 10 Nov): fix_63c8a193fe C X={I3-I9,I7-I8,R12-I8,R0-I9}
Source: hits_st111.tsv, id fix_63c8a193fe, ring 14 m 11, rows K4:8565766/5557656,8565766/5557657, lead confirm cfast:C-REDUCIBLE.
- iso: n/a (fix_ windows carry no b<d>_ window name; the kc line is taken as given from cov_windows.tsv; occurrence below ties it to the target rows)
- kc -t 600 -C -x {I3-I9,I7-I8,R12-I8,R0-I9}: adm=yes leftover 0 C-REDUCIBLE; cfast --fixed I3-I9,I7-I8,R12-I8,R0-I9: C-REDUCIBLE leftover 0
- Lean lean/CK5P20.lean (XRData.ok, admissibleX, foldSafeX): CK5P20 exit=0 wall=8s sorry=0 error=0 rss=3021MB 12:41
- rim pin R12-I8: R12 is a ring neighbour of I8 (ring nbrs 11,12); rotation of I8 [('I', 7), ('R', 11), ('R', 12), ('I', 2), ('I', 9), ('I', 10)]; flanked by (('R', 11), ('I', 2))
- rim pin R0-I9: R0 is a ring neighbour of I9 (ring nbrs 0,1); rotation of I9 [('I', 2), ('R', 0), ('R', 1), ('I', 3), ('I', 10), ('I', 8)]; flanked by (('I', 2), ('R', 1))
- Occurrence (K3CHK occurs, rotation-preserving): 7/8565766/5557656 face-set 1 rotation-preserving 1 OCCURS; 7/8565766/5557657 face-set 1 rotation-preserving 1 OCCURS
- **Result: PASS**
