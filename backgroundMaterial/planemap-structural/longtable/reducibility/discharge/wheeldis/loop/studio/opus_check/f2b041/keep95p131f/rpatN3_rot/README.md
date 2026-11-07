# ST-10: rpatN3 under the rotation-preserving reading (Studio, 7 Nov)

- **Builder:** out/job31/rpatN_studio.py (rpatN3 = s39o_rpatN3_studio.txt 0f7580c4; e153fc41 is the s39o copy with the identical 2,287-pattern set, header and annotation lines differ). It has its own embedding, which is a face-set reading: induced window adjacency (:69-76 of the original) and interior 3-cliques onto window faces (:53-60), with no rotation check. It does not use grow.embeddings.
- **Flag:** RPATN_ROT=1 (default off) reuses keep95p131f/rot/rotcheck.py: window rebuilt with grow.build2 at the embedding's own letters (free link letters coded 6; RPATN_ROT_DOT=5 is a diagnostic only), rotation-preserving test with c -> u. Flag off: byte-identical to 0f7580c4 (cmp).
- **Runs:** nl51 (8,200, the rpatN3 source): 2,226 patterns survive, 61 dropped. Keep-pool witnesses (11,891 non-RSST kc lines + 377 RSST from unavoidable.conf, the 12,268 forbidden set) rescue 1 (7 .556.65 .56..65 by f7_.556.65_.56..65). **Final: 2,227 kept, 60 without a rotation-preserving witness** (rpatN3_dropped_rot.txt).
- **Vs W18** (c03fa002 46 unjustified / 8b90a842 2,241 kept): **dropped by both 46; only by W18 0; only by Studio 14.**
- **The 14 (diag14.tsv):** each comes from one nl51 source with 2 face-set embeddings; both fail rotcheck at the centre (interior-neighbour cyclic order around u, both orientation signs) - a necessary condition for an embedding in a plane triangulation. Coding the free link letters as 5 instead of 6 rescues none. No other keep-pool configuration gives these patterns rotation-preservingly. To settle them we need W18's witness configuration for each of the 14; we will run rotcheck on exactly those, as for the 42 rules.

| pattern | nl51 source | rotcheck |
|---|---|---|
| 7 .56.575 .5.565. | nl3171_r13 | {'shift(at 0) / shift(at 0)': 2} |
| 7 .565N56 ..6555. | nl2861_r12 | {'shift(at 3) / shift(at 3)': 2} |
| 7 .575N56 .56555. | nl3185_r13 | {'shift(at 0) / shift(at 0)': 2} |
| 8 .5565.56 ..5..56. | nl5141_r13 | {'shift(at 0) / shift(at 0)': 2} |
| 8 .5565.65 ...65.5. | nl5135_r13 | {'shift(at 0) / shift(at 0)': 2} |
| 8 .5566.65 .565..55 | nl5255_r13 | {'shift(at 0) / shift(at 0)': 2} |
| 8 .56.5656 .5..5.5. | nl5130_r13 | {'shift(at 0) / shift(at 0)': 2} |
| 8 .565N575 .555555. | nl5526_r13 | {'shift(at 0) / shift(at 0)': 2} |
| 8 .575N575 .555555. | nl6352_r14 | {'shift(at 0) / shift(at 0)': 2} |
| 9 .55565.56 ....5.55. | nl7291_r13 | {'shift(at 0) / shift(at 0)': 2} |
| 9 .55655.56 ..5...55. | nl7296_r13 | {'shift(at 0) / shift(at 0)': 2} |
| 9 .55756.65 ..555..55 | nl7693_r14 | {'shift(at 0) / shift(at 0)': 2} |
| 9 .55756.65 .5655..55 | nl7801_r14 | {'shift(at 9) / shift(at 9)': 2} |
| 9 .56.65556 55..5.56. | nl7466_r14 | {'shift(at 0) / shift(at 0)': 2} |

## Follow-up (W18 witnesses for the 14, 42428ec3): all 14 are case (a); our full-pool search had a comparison restriction
- extra14_W18witness_rot.tsv (witness14.py): for every one of the 14, the W18 witness has a **rotation-preserving** embedding (every centre and placement tried) whose pattern is **more general** than the target and matches its window. It is not equal to it.
- **Cause:** our full-pool step counted a pattern as justified only when some pool configuration produced the **identical** pattern string. The pool scan and the rotation test were fine; the comparison was too strict. A witness pattern Q justifies P when, under one of the 2d rotations / reflections, every fixed position of Q is satisfied by P (digit = digit, N = a letter in {6,7,8,N}).
- **Fixed** (subsume_all.py, matching test over every rotation-preserving pool pattern: nl51 rebuild + non-RSST keep pool + RSST): **2,241 justified, 46 dropped; the 46 = W18's 46 exactly; 0 only-Studio, 0 only-W18.** Kept set = W18's rotation_justified (8b90a842) set. rpatN3_dropped_rot.txt is regenerated (46 lines); rpatN3_rotation_justified_studio.txt lists each kept pattern with its matching witness.
- The earlier "60 dropped / 14 only-Studio" result above is superseded.
