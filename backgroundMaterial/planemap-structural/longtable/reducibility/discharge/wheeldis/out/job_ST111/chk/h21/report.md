# ST-111 RSST-substitute window 21 second check (Studio, 10 Nov): fix_404d45e819 C X={I0-I2,I4-I5,R11-I2,R4-I5}
Source: hits_st111.tsv, id fix_404d45e819, ring 13 m 6, rows K4:565668/575777,565678/575755,565678/575757,565678/777757,565778/577755,565788/577755, lead confirm cfast:C-REDUCIBLE.
- iso: n/a (fix_ windows carry no b<d>_ window name; the kc line is taken as given from cov_windows.tsv; occurrence below ties it to the target rows)
- kc -t 600 -C -x {I0-I2,I4-I5,R11-I2,R4-I5}: adm=yes leftover 0 C-REDUCIBLE; cfast --fixed I0-I2,I4-I5,R11-I2,R4-I5: C-REDUCIBLE leftover 0
- Lean lean/CK5P21.lean (XRData.ok, admissibleX, foldSafeX): CK5P21 exit=0 wall=7s sorry=0 error=0 rss=3020MB 12:41
- rim pin R11-I2: R11 is a ring neighbour of I2 (ring nbrs 11,12); rotation of I2 [('I', 1), ('R', 11), ('R', 12), ('I', 0), ('I', 3), ('I', 5)]; flanked by (('I', 1), ('R', 12))
- rim pin R4-I5: R4 is a ring neighbour of I5 (ring nbrs 4,5); rotation of I5 [('I', 2), ('I', 3), ('R', 4), ('R', 5), ('I', 4), ('I', 1)]; flanked by (('I', 3), ('R', 5))
- Occurrence (K3CHK occurs, rotation-preserving): 6/565668/575777 face-set 1 rotation-preserving 1 OCCURS; 6/565678/575755 face-set 1 rotation-preserving 1 OCCURS; 6/565678/575757 face-set 1 rotation-preserving 1 OCCURS; 6/565678/777757 face-set 1 rotation-preserving 1 OCCURS; 6/565778/577755 face-set 1 rotation-preserving 1 OCCURS; 6/565788/577755 face-set 1 rotation-preserving 1 OCCURS
- **Result: PASS**
