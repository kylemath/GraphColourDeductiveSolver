# ST-67 bind2140 hit 05 second check (Studio, 8 Nov): b8_u76676556_.5..656. C X={I1-I2,I3-I4,R4-I2,R6-I3}
Source: res_K5_r16_201644_3.tsv, id 4ca54c1b40bc28570ee0, ring 16 m 13, rows K4:76676556/65666566, lead confirm cfast:C-REDUCIBLE.
- kc line (= res kc column) interior + degrees vs K of window f8_76676556_.5..656. (Ku): isomorphic
- kc -t 600 -C -x {I1-I2,I3-I4,R4-I2,R6-I3}: adm=yes leftover 0 C-REDUCIBLE; cfast --fixed I1-I2,I3-I4,R4-I2,R6-I3: C-REDUCIBLE leftover 0
- Lean lean/CK5P05.lean (XRData.ok, admissibleX, foldSafeX): CK5P05 exit=0 wall=4s sorry=0 error=0 rss=3020MB 02:56
- rim pin R4-I2: R4 is a ring neighbour of I2 (ring nbrs 3,4); rotation of I2 [('I', 9), ('I', 3), ('I', 0), ('I', 1), ('R', 3), ('R', 4)]; flanked by (('R', 3), ('I', 9))
- rim pin R6-I3: R6 is a ring neighbour of I3 (ring nbrs 6,7); rotation of I3 [('I', 9), ('R', 6), ('R', 7), ('I', 4), ('I', 0), ('I', 2)]; flanked by (('I', 9), ('R', 7))
- Occurrence (K3CHK occurs, rotation-preserving): 8/76676556/65666566 face-set 2 rotation-preserving 2 OCCURS
- **Result: PASS**
