# RSST-ROTSUB: rotation-respecting kills for W6r's 4,398 mirror-only leaves  [P]

W6b, round 16. Input: round6/W6r-replay/rsst_fp/rot/results/mirror_only_states.tsv
(4,398 leaves: d7 2,590 / d8 1,370 / d9 406 / d10 32).

## Method
- The window and the rotation test are W6r's rot.py, copied unchanged (md5 1f48d41b...; code/rot.py):
  - rot.window builds the window with fw_bb numbering;
  - kc_rotation takes a config's rotation from its graph;
  - all_embs + rot_ok enforce one global chirality.
- Hosts are u and every w/s/private with letter <= 8. A leaf's 9+ is a non-host, and so is its middle.
- Prefilter: the W6b bitmask matcher (induced, exact degrees). Then every plain embedding is checked for rotation. Code: code/rotkill.py.
- Pool A (8,509 configs; rotations built for all, 0 rejected):
  - nl51 (8,200; s39o/nl51_kc.txt);
  - the W6b round11/12 SUB/SUB2 window pool (r14rule2e pool_all_kc.txt, 310).
- Pool B (3,462 configs not already in pool A, by kc body): read as DATA only. No outside code was run.
  - swarm/outside/fullstack_t0 registry kc_lines: 878; 295 are not RSST.
  - swarm/outside/beat_633_588/pool_input.txt: 4,095 configs, converted to kc with python3 -I.
- Greedy: code/greedy.py, over each leaf's set of rotation killers (results/all_leaves.tsv.gz, column rot_killers).

## Results
| degree | leaves | closed by pool A (rotation-respecting) | of these, also by pool B new configs | open |
|---|---|---|---|---|
| d7  | 2,590 | 2,590 | 2,390 | 0 |
| d8  | 1,370 | 1,370 | 1,367 | 0 |
| d9  |   406 |   406 |   406 | 0 |
| d10 |    32 |    32 |    32 | 0 |
| total | 4,398 | 4,398 | 4,195 | **0** |

- **Every mirror-only leaf has a rotation-respecting kill in pool A.**
  - Per leaf there are 1 to 31 rotation killers (mean 4.3).
  - In all, 420 distinct configs kill some leaf.
- **Pool B is not needed.**
  - Its 3,462 new configs (not in pool A) close only 4,195 of the leaves.
  - Every config the pool B greedy picks is an nl51 config that pool A also contains.
- **Step 3 (refining 9-as-non-host) is moot**, because no leaf is left open.
  - Note that refining a leaf cannot close the leaf itself.
  - A leaf's own all-9+ instance is a concrete state, and kills never use a 9+ vertex.
  - So refinement can only close the refined sub-states, never the leaf.

### Greedy minimal added set (pool A): 15 configs, 0 left
| pick | leaves | type (our check) | ring |
|---|---|---|---|
| nl0079_r11 | 2,349 | D (dfast18) | 11 |
| nl3357_r13 | 1,012 | D | 13 |
| nl0196_r12 | 374 | D | 12 |
| nl1297_r14 | 225 | D | 14 |
| nl1835_r13 | 202 | D | 13 |
| nl0021_r11 | 56 | D | 11 |
| fw_ac168199bf | 46 | C (cfast C-REDUCIBLE; I1-I5; round12 vc_fw_windows: valid_contract True, lean_admissibleX True) | 13 |
| nl7105_r14 | 36 | D | 14 |
| nl5384_r14 | 36 | D | 14 |
| fw_6c46307791 | 25 | D | 12 |
| nl6917_r15 | 19 | D | 15 |
| nl3144_r13 | 8 | D | 13 |
| nl1684_r12 | 4 | D | 12 |
| nl6785_r15 | 3 | D | 15 |
| nl5981_r14 | 3 | D | 14 |

- **Our reducibility check (step 4):**
  - The swarm mscreen ran with W13 kcc_o3, dfast18 and cfast, timeout 900 s.
  - All 15 picks are confirmed: 14 D and 1 C.
  - Files: results/used15_res.tsv and logs/used15.log.
- **Greedy picks per degree:**
  - d10: nl0079_r11 32.
  - d9: nl0079_r11 406.
  - d8: nl0079_r11 1057, nl1835_r13 202, nl7105_r14 36, nl5384_r14 36, nl6917_r15 19, nl0021_r11 10, nl1684_r12 4, nl5981_r14 3, nl6785_r15 3.
  - d7: nl3357_r13 1012, nl0079_r11 854, nl0196_r12 374, nl1297_r14 225, nl0021_r11 46, fw_ac168199bf 46, fw_6c46307791 25, nl3144_r13 8.
- **nl51 alone (no windows): 13 configs, but 71 d7 leaves are left open** (links 5657578/5657579).
  - These are the fw_f7c75a21e2 mirror cases.
  - They need a W6b window: fw_ac168199bf or fw_3ff67ce5f7.
- **The picks are mostly Whitney partners of W6r's mirror-only killers.**
  - For example, nl0078_r11 -> nl0079_r11, nl3352_r13 -> nl3357_r13, nl0194_r12 -> nl0196_r12.
  - On the 40-leaf test (results/test40_leaves.tsv), nl0194_r12 is plain-only (mirrored), while nl0196_r12 kills with the rotation respected.
- **Alternative greedy with pool B names (also 0 left):**
  - nl5459_r16, nl1732_r13, nl6039_r13 and nl5798_r13 replace nl7105/nl5384/nl6917/nl6785.
  - All four are in nl51.

## Caveats
- The rotation test is W6r's rot.py, used as is. I did not re-derive it independently.
- The host and letter conventions follow W6r's mirror_only_states encoding: a 9+ site is drawn as an 8 and is never a host.

## Files
code/ (rotkill.py, greedy.py, rot.py copy); results/ (all_leaves.tsv.gz, greedy.json, used_names.txt, used15_batch.tsv, used15_res.tsv, test40_leaves.tsv); pools/ (pool B kc conversions, gz); logs/.
The reducibility screen engine is /tmp/swarm-W13b mscreen.py; it is not copied here.
