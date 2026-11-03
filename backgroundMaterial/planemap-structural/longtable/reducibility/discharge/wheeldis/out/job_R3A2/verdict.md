# job R3A2 (Opus / swarm Team A R3-A2): Studio checks (3 Nov)

## Independence statement
- **Engines:** Studio's own binaries, nothing rebuilt: kc loop/kc/kc (07e79fae), dfast18 out/job52/dfast18 (07cb1e0b), cfast
  ../studio15/cfast (de59e72f).
- **Lookup and frame tests:** Studio's own scripts, iso_lookup.py and frame_test.py. They run on explore's grow.py (kcline and
  induced embeddings), the same machinery as f2b_rulecheck.py.
- **Swarm code:** only their window generator, gen.py with binder.py, was run, as asked. It was run on a local copy where the only
  change is binder.py's hardcoded W path (out/job_A3W/apex/binder.diff).
- **Not opened:** Opus engine code and Team B material.
- **Inputs:** 1ccb5da4 ext_handoff_nov3/r3a2/, copied read-only into in/. All 41 md5s match MD5SUMS.txt.

## (2) The two D configurations
| config | ring, m | kc -C -s 60 -t 600 | dfast18 | cfast |
|---|---|---|---|---|
| t6_7_7665566_6765766_s2s3s4tuw2w3w4w5 (D11_config.txt) | 11, 9 | D: 7381/7381, ext 1754, depth 2 (gs) | D: 7381/7381, ext 1754, depth 5 | D: 7381/7381, bad 0, depth 5 |
| t6_8_77655556_65758586_s2s3s4s5tuw2w3w4w5w6 (relay addendum) | 12, 11 | D: 22144/22144, ext 4870, depth 3 (gs) | D: 22144/22144, ext 4870, depth 5 | D: 22144/22144, bad 0, depth 5 |

**Both are D on all three engines** (d11_engines.log, d12_engines.log). The swarm's figure for D11 (kc and dfast at 7381/7381,
depth 5) matches dfast18 and cfast. Our kc runs Gauss-Seidel passes, so it reports depth 2.

### (b) Already present? (iso_lookup.py, iso_lookup.log)
- **What was searched:** every committed kc line at rings 11 and 12, 6,338 distinct lines in all.
  - Sources: loop/k*/ (including k44 RSST 633 and k51 nl51 8,200), loop/studio/, out/, loop/kc/.
  - So the search covers the Tier A forbidden set (13,199), the A97 stack's kc lines, RSST 633 and the 2026 set (nl51).
- **How:** configuration isomorphism, i.e. induced embedding with exact degrees and triangles onto triangles. This covers rotation
  and reflection.
- **D11 (ring 11)** is isomorphic to **s5_u55767_66..6_.....**, in loop/studio/sender_held/sender_kills51.txt (explore's round-51
  sender kill). That set is held: per its README it is NOT in k3x or any LP registry. It is not in the Tier A args / tables or in the
  A97 args. **So D11 is not in our registry or forbidden set.**
- **D12 (ring 12)** has **no isomorphic configuration** among the committed kc lines. **D12 is not in our registry or forbidden
  set.**

### (c) Would adding them add receiver patterns? (frame_test.py, frame_test.log)
- **Test:** embed each configuration into every receiver 2-ball frame, with
  - d = 7, 8, 9, 10;
  - w0 = 5, 6, 7, 8;
  - every 5 / non-5 structure;
  - u fixed at d for d ≤ 8; the other degrees free in 5..8.

  Two modes were checked:
  1. **As a (w, s) receiver pattern:** embedding into u + w + s.
  2. **As a private-letter kill:** for the §14' tables and the full2ball rules, using one of w0's privates.
- **Result: 0 embeddings for both configurations, in every mode and degree.**
- **Positive control:** the k3x D window f7_.....55_.....55 gives 5,120 pattern embeddings and 1,792 private embeddings at d = 7
  (frame_ctrl.log). So the test does detect embeddings when they exist.
- **Why:** both configurations use the face apex t, a ring-3 vertex beyond the 2-ball (u, w, s, w0's privates). The receiver rows
  and their 2-ball tables never see it.
- **Consequence:** adding D11 or D12 to the D set adds **no receiver pattern, no §14' kill and no rule**. The dry-run pattern count
  is unchanged by construction: our pattern parser takes [epf]-names, and these configurations have no (w, s) image. Using them
  needs a new row family with t in the window, i.e. a 3-ball rule class.

## (1) A3W apex windows
- Generated with their gen.py at RMAX 17, for t = 7 and t = 8, for the 14 rows of rows.txt (out/job_A3W/apex/g_{t}_{LK}_{SV}.win).
  The windows at rings 15..17 total 3,762.
  - **t = 7:** 558 at ring 15, 682 at ring 16, 934 at ring 17.
  - **t = 8:** 348 at ring 15, 558 at ring 16, 682 at ring 17.
- **Compared with the swarm's t = 7 logs:**
  - tw/g_7_6667655_7776756.res: 43 names, all among our 202.
  - tw/g_7_77655556_65758586.res: 98 names, all among our 304.
  - So 0 of their names are missing from ours. Their logs are partial runs.
- **Run order:** these are being run on our window protocol now, before the remaining plain ring-16 A3W windows. The results go to
  out/job_A3W/verdict.md.
