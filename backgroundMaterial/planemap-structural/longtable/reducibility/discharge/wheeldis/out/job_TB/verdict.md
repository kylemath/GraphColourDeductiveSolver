# job TB (Opus Tier B request, relay of 2 Nov 22:06Z): Studio two-engine checks

**Result: 28 / 28 PASS, 0 FAIL.**
- Part (1), 12 E lines: **12 PASS**. Of these, 3 are D and 9 are C, each on both engines with the same X.
- Part (2), 16 K lines: **16 PASS**. Of these, 14 are D2 → D and 2 are C2 → C with X {I4-I5}, on both engines.
- Item (3), RSST "none": ignored, as instructed.

## Independence statement
- **Code:** Studio's own binaries, nothing rebuilt:
  - kc = loop/kc/kc (07e79fae)
  - dfast18 = out/job52/dfast18 (07cb1e0b)
  - cfast = ../studio15/cfast (de59e72f)
- **Driver:** out/job_TB/drive_TB.py (Studio). It runs the window protocol of out/job_tw1/drive_tw1.py: `kc -C -s 60 -t 600` plus
  dfast18, with `cfast --fixed X` for any kc X. C lines run `kc -t 600 -C -x {X}` and `cfast --fixed {X}`.
- **Input:** tierB28.txt, written verbatim from the relay (md5 6869bdde).
- **Not opened:** Opus engine code and Team B material.

## Notes
- **X records.**
  - Every recorded X has |X| ≤ 4, so the LT override (|X| ≥ 5) did not apply. The ring-merge guard is in our engines as built.
  - drive_TB.py's record lookup also picked up the next record line's X for the k38 names. Those extra rows show `parse=fail`
    or `adm=no` and are ignored. Only the name's own X, and kc's own X, are used.
- **Rows 5, 7, 8: kc rejects the recorded k38 X.** These are f7_..65757_..65..., f7_..65757_..55... and f7_..56757_...5....
  - The recorded X in k38/kills_x.txt comes from cfast's choice. kc rejects it (`adm=no`: a rim-pinned X).
  - cfast passes with that recorded X (leftover 0).
  - kc's own window finds another X: {I0-I2}, {I0-I2} and {I0-I4,I1-I5,R1-I0,R8-I5} respectively. cfast --fixed with kc's X is
    also C-REDUCIBLE with leftover 0 (cfast_kcX.log).
  - So all three pass with the same X on both engines (kc's X).
  - Row 8's X is rim-pinned (R1, R8). foldSafeX was not run here; it would be needed if the entry is used under the
    rim-pinned rule.
- **Records for the K lines** (matched on the full kc line):
  - 10 lines have an existing two-engine record in tw1 / tw2 / tw3 / tw4 (kills_batch*.txt, done.txt: kc(t600) = D, dfast18 = D),
    which agrees with the fresh rerun.
  - The 6 p60 / x60 lines have no record, so their fresh rerun is the only evidence.
  - All 16 were rerun fresh on both engines.

| # | name | part | expected | kc | 2nd engine | X | record / rerun | |
|---|---|---|---|---|---|---|---|---|
| 0 | f7_5567576_.....5. | E C | C | X adm, leftover 0 | cfast fixed, leftover 0 | {I0-I4} | k34/fill_kcc.out; rerun | PASS |
| 1 | f7_5567576_5....5. | E D | D | D | dfast18 D | – | rerun | PASS |
| 2 | f7_5567576_5....56 | E D | D | D | dfast18 D | – | rerun | PASS |
| 3 | f7_5567576_5.5...6 | E D | D | D | dfast18 D | – | rerun | PASS |
| 4 | f7_5667576_..5.... | E C | C | X adm, leftover 0 | cfast, leftover 0 | {I0-I1,R2-I1,I6-I7,R0-I7} | k38/kills_x.txt; rerun | PASS |
| 5 | f7_..65757_..65... | E C | C | recorded X adm=no; own X | cfast, leftover 0 (both X) | kc {I0-I2} | k38; rerun | PASS (kc X) |
| 6 | f7_5675767_.5..... | E C | C | X adm, leftover 0 | cfast, leftover 0 | {I0-I1,I0-I3,I0-I6,R14-I6} | k38; rerun | PASS |
| 7 | f7_..65757_..55... | E C | C | recorded X adm=no; own X | cfast, leftover 0 (both X) | kc {I0-I2} | k38; rerun | PASS (kc X) |
| 8 | f7_..56757_...5... | E C | C | recorded X adm=no; own X | cfast, leftover 0 (both X) | kc {I0-I4,I1-I5,R1-I0,R8-I5} | k38; rerun | PASS (kc X; pinned) |
| 9 | f7_..57556_...65.. | E C | C | X adm, leftover 0 | cfast, leftover 0 | {I0-I2} (LT X also passes) | k37 fill_kcc / lt_x; rerun | PASS |
| 10 | f7_..57556_...66.. | E C | C | X adm, leftover 0 | cfast, leftover 0 | {I0-I2} (LT X also passes) | k37; rerun | PASS |
| 11 | f7_5566757_...5... | E C | C | X adm, leftover 0 | cfast, leftover 0 | {I0-I1} | k37; rerun | PASS |
| 12 | r7766556_6567566_w0_priv57 | K | D2 | D | dfast18 D | – | tw1 + rerun | PASS |
| 13 | r7766556_6567566_w0_priv59 | K | D2 | D | dfast18 D | – | tw1 + rerun | PASS |
| 14 | r7766556_6567566_w1_priv75 | K | D2 | D | dfast18 D | – | tw1 + rerun | PASS |
| 15 | r7766655_6567659_w1_priv66 | K | D2 | D | dfast18 D | – | tw1 + rerun | PASS |
| 16 | p60_9656775_5556655_w4_55 | K | D2 | D | dfast18 D | – | rerun (no record) | PASS |
| 17 | p60_9656775_5556655_w4_56 | K | C2 | C | cfast, leftover 0 | {I4-I5} | rerun (no record) | PASS |
| 18 | r7766556_6567566_w0_priv66 | K | D2 | D | dfast18 D | – | tw2 + rerun | PASS |
| 19 | r7766655_6567659_w1_priv75 | K | D2 | D | dfast18 D | – | tw2 + rerun | PASS |
| 20 | r7766556_6567566_w1_priv95 | K | D2 | D | dfast18 D | – | tw3 + rerun | PASS |
| 21 | r7766655_6567659_w1_priv95 | K | D2 | D | dfast18 D | – | tw3 + rerun | PASS |
| 22 | p60_9656775_5556655_w4_65 | K | C2 | C | cfast, leftover 0 | {I4-I5} | rerun (no record) | PASS |
| 23 | x60_9656775_5556655_w5_95_..5.65. | K | D2 | D | dfast18 D | – | rerun (no record) | PASS |
| 24 | x60_9656775_5556655_w5_95_.5..65. | K | D2 | D | dfast18 D | – | rerun (no record) | PASS |
| 25 | x60_7666567_5665565_w6_59_...5565 | K | D2 | D | dfast18 D | – | rerun (no record) | PASS |
| 26 | r7665566_6675676_w0_priv66 | K | D2 | D | dfast18 D | – | tw4 + rerun | PASS |
| 27 | r7766556_6567566_w1_priv66 | K | D2 | D | dfast18 D | – | tw4 + rerun | PASS |

Raw outputs are in results.tsv (one row per check) and cfast_kcX.log.
