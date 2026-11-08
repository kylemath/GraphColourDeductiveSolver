# ST-67 bind2140 hit 02 second check (Studio, 8 Nov): b7_u55.6777_5..5.5. C X={I0-I4,I0-I6,R0-I0}
Source: res_K5_r15_150433_1.tsv, id 36d4ef77f83a3aa40cff, ring 15 m 10, rows K4:5566777/5675656, lead confirm cfast:C-REDUCIBLE.
- kc line (= res kc column) interior + degrees vs K of window f7_55.6777_5..5.5. (Ku): isomorphic
- kc -t 600 -C -x {I0-I4,I0-I6,R0-I0}: adm=yes leftover 0 C-REDUCIBLE; cfast --fixed I0-I4,I0-I6,R0-I0: C-REDUCIBLE leftover 0
- Lean lean/CK5P02.lean (XRData.ok, admissibleX, foldSafeX): CK5P02 exit=0 wall=9s sorry=0 error=0 rss=3021MB 21:42
- rim pin R0-I0: R0 is a ring neighbour of I0 (ring nbrs 0); rotation of I0 [('I', 3), ('I', 4), ('I', 5), ('I', 6), ('I', 1), ('I', 2), ('R', 0)]; flanked by (('I', 2), ('I', 3))
- Occurrence (K3CHK occurs, rotation-preserving): 7/5566777/5675656 face-set 1 rotation-preserving 1 OCCURS
- **Result: PASS**
