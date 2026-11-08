# ST-42 K-5 hit 04 second check (Studio, 8 Nov): b10_u6556656..5_.5.6...... C X={I0-I4,I4-I10,R7-I4}
Source: res_K5_r1516_05.tsv, id e1092364caab04c60266, ring 16 m 11, rows K4:6556656655/7566556657, lead confirm cfast:C-REDUCIBLE.
- kc line (= res kc column) interior + degrees vs K of window f10_6556656..5_.5.6...... (Ku): isomorphic
- kc -t 600 -C -x {I0-I4,I4-I10,R7-I4}: adm=yes leftover 0 C-REDUCIBLE; cfast --fixed I0-I4,I4-I10,R7-I4: C-REDUCIBLE leftover 0
- Lean lean/CK5H04.lean (XRData.ok, admissibleX, foldSafeX): CK5H04 exit=0 wall=4s sorry=0 error=0 rss=3021MB 04:08
- rim pin R7-I4: R7 is a ring neighbour of I4 (ring nbrs 7,8); rotation of I4 [('I', 0), ('I', 3), ('R', 7), ('R', 8), ('I', 10), ('I', 5)]; flanked by (('I', 3), ('R', 8))
- Occurrence (K3CHK occurs, rotation-preserving): 10/6556656655/7566556657 face-set 2 rotation-preserving 2 OCCURS
- **Result: PASS**
