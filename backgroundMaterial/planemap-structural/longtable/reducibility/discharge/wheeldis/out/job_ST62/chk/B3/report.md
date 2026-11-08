# ST-62 bind61 B3 (Studio, 8 Nov): b9_u5555...67_......65. C X={I0-I1,I5-I6,R0-I0,R2-I5}
Source: bind46 bind61 cfast:C-REDUCIBLE, id 23ef876e9180d60b4269, ring 15 m 9, claimed rows 6.
- kc line (= res kc column) interior + degrees vs K of window f9_5555...67_......65. (Ku): isomorphic
- kc -t 600 -C -x {I0-I1,I5-I6,R0-I0,R2-I5}: adm=yes leftover 0 C-REDUCIBLE; cfast --fixed I0-I1,I5-I6,R0-I0,R2-I5: C-REDUCIBLE leftover 0
- Lean lean/CK5FB3.lean (XRData.ok, admissibleX, foldSafeX): CK5FB3 exit=0 wall=3s sorry=0 error=0 rss=3020MB 16:13
- rim pin R0-I0: R0 is a ring neighbour of I0 (ring nbrs 0,1,2); rotation of I0 [('I', 5), ('I', 6), ('I', 1), ('I', 2), ('I', 3), ('I', 4), ('R', 0), ('R', 1), ('R', 2)]; flanked by (('I', 4), ('R', 1))
- rim pin R2-I5: R2 is a ring neighbour of I5 (ring nbrs 2,6); rotation of I5 [('R', 6), ('I', 8), ('I', 6), ('I', 0), ('R', 2), ('I', 7)]; flanked by (('I', 0), ('I', 7))
- Occurrence (K3CHK occurs, rotation-preserving) on 6 claimed rows: 6 occur. 9/555556667/578587656 face-set 1 rotation-preserving 1 OCCURS; 9/555557666/587565678 face-set 1 rotation-preserving 1 OCCURS; 9/555566675/785876565 face-set 1 rotation-preserving 1 OCCURS; 9/555576665/875656785 face-set 1 rotation-preserving 1 OCCURS; 9/555666755/858765657 face-set 1 rotation-preserving 1 OCCURS; 9/555766655/756567858 face-set 1 rotation-preserving 1 OCCURS
- **Result: PASS**
