# ST-104 t102 container hit 15c second check (Studio, 9 Nov): b8_u.555785._....55.. C X={I4-I5,R4-I5}
Source: container_hits_t102.tsv, id 8f1a9c79bf4eb1eab387, ring 14 m 9, rows K4:55557858/58565557,55557858/58565558,55557858/59565557, lead confirm cfast:C-REDUCIBLE.
- kc line (= res kc column) interior + degrees vs K of window f8_.555785._....55.. (Ku): isomorphic
- kc -t 600 -C -x {I4-I5,R4-I5}: adm=yes leftover 0 C-REDUCIBLE; cfast --fixed I4-I5,R4-I5: C-REDUCIBLE leftover 0
- Lean lean/CK5P15c.lean (XRData.ok, admissibleX, foldSafeX): CK5P15c exit=0 wall=4s sorry=0 error=0 rss=3020MB 09:30
- rim pin R4-I5: R4 is a ring neighbour of I5 (ring nbrs 4,5,6); rotation of I5 [('I', 6), ('I', 8), ('R', 4), ('R', 5), ('R', 6), ('I', 7), ('I', 4), ('I', 0)]; flanked by (('I', 8), ('R', 5))
- Occurrence (K3CHK occurs, rotation-preserving): 8/55557858/58565557 face-set 1 rotation-preserving 1 OCCURS; 8/55557858/58565558 face-set 1 rotation-preserving 1 OCCURS; 8/55557858/59565557 face-set 1 rotation-preserving 1 OCCURS
- **Result: PASS**
