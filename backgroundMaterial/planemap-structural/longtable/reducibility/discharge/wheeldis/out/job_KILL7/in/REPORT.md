# B1: dual-guided kills on keep95p131f (Opus Team B, round 6, 5 Nov 2026)

This is Team B's hand-back report. The Opus coordinator saved it here because the harness refused the worker's own write. Labels: [P] means D on at least two engines; [M] means measured (HiGHS floating point, not an exact check).

## Bottom line
- **7 new kill6 entries [P]: the strongest result.**
  - Each comes from a window at ring 12-13 that is D on all five engines (kcc, kc, dfast, dfast18, A_rsst dfast).
  - Each entry removes one letter for the private neighbour of a link 6.
  - Together they change the coefficients of **22 W7-certificate receiver rows, which hold 34.3 % of the certificate's receiver mass**. These include row #2, 6755566/7775768 (12.9 %), and row #3, 5556677/7576757 (12.4 %).
  - The 6-relay mask goes from 30 to 28, so that private must have degree ≥ 7.
  - **Over the certificate's own rows [M]:** t goes from 0.025678 to −0.0356.
  - **Pool LP [M]:** the LP over the 38,542 receiver rows in W7's pool, plus all 20,676 sender rows and the cons2 basis.
    - Its control (unpatched stack, certificate rows only) reproduces 0.025678115830 exactly, so unpatched it is ≥ 0.0257.
    - It drops to **−0.00776** with all 7 entries, and to −0.00186 with the first entry alone.
  - **What this means:** the W7 lower certificate does not survive the patched stack, and W7's row pool no longer proves t* > 0.
    - It does **not** show t* ≤ 0, because rows are missing. A separation lowerR2 solve on the patched stack is needed.
    - The upper bound 0.041565 still holds, since kills can only lower t*.
- **29 apex-t kill lines (tkill format) [P]**, rings 7-12, D on kcc, dfast and dfast18.
  - Every 5-5-5-face row in the certificate has some apex letter killed. These rows carry 54.8 % of receiver mass.
  - 27 rows (48.1 % of receiver mass) have t ∈ {5,6} killed at every face.
  - Their LP effect could not be measured (see section 4).
- **42 more D windows ("cell kills") [P].** These kill fives among the private neighbours of a link 7 in the top rows. The current LP cannot use them until the receiver row gets a new key for those neighbours.
- **No C anywhere** (kcc -C, |X| ≤ 4, run on every window). **No D among the plain 2-ball windows** of the top 12 rows.

## 1. Decoding the certificate [M] (decode_B1.txt)
**Share of |w| by row type:** mrowL 31.9 %, senderR2 19.9 %, receiverR2 18.5 %, cons2 16.1 %, mrowR2 13.7 %.

**Sender contexts:**

| Word / context | Share of sender mass |
|---|---|
| 57777/00000 | 33.6 % |
| 55757/00000 | 20.7 % |
| 55767/00000\|0 | 14.8 % (the word as a whole: 16.7 %) |
| 55777/00000 | 14.4 % |
| 55667 (all contexts) | 5.0 % |

85.9 % of sender mass sits in contexts where every hat is small.

**Receiver motifs (d=7):**

| Motif | Rows | Share of receiver mass |
|---|---|---|
| 5-5-5 face | 67 | 54.8 % |
| mixed 5-6-7 | 84 | 19.0 % |
| 5-7 mesh | 4 | 17.2 % |
| lone 5 | 25 | 4.1 % |
| 55 pair | 10 | 2.9 % |
| relay (no 5) | 11 | 0.9 % |
| d = 8-10 (all) | — | 1.1 % |

**Top receiver rows:**

| # | Row | Share |
|---|---|---|
| 1 | 5757577/5577567 | 13.3 % |
| 2 | 6755566/7775768 | 12.9 % |
| 3 | 5556677/7576757 | 12.4 % |
| 4 | 5755755/7777757 | 11.7 % |
| 5 | 7767575/5665557 | 11.6 % |
| 6 | 7557755/7575757 | 4.4 % |
| 7 | 5557666/5776767 | 2.8 % |
| 8 | 7577575/7555775 | 2.6 % |

The top 5 hold 61.8 %; the top 12 hold 77.0 %.

**Coupling** (share of receiver mass in rows whose link holds a five with word X): 57777 79.7 %, 55757 44.6 %, 55767 35.9 %, 55777 33.3 %.

**Restricted LP over the certificate's rows** (rlp_summary.tsv, rlp_drop1_top30.txt):
- Removing the four heavy sender contexts, one at a time or all four together, leaves t at 0.0256781. **Kills aimed at sender contexts are useless.**
- Removing one receiver row at a time:
  - row #1 → −0.0559; row #4 → −0.0448; rows #3 and #5 → −0.0292 each;
  - row #6 → 0.0172; rows #7 and #8 → 0.020;
  - row #2 alone changes nothing (0.0256781);
  - every other row → 0.022-0.025.

## 2. Windows screened (kcc, then dfast and dfast18 on every D)
4,810 windows were run, plus 1,429 that explore had already judged (skipped).

| Family | Run (rings) | D | C |
|---|---|---|---|
| fam0: 2-ball windows of the top 12 rows | 778 (r9-14) + 1,429 judged N | 0 | 0 |
| fam2a: extra fives (private or ring-3), singles and pairs, top 5 rows | 255 (r8-12) | 65 | 0 |
| famT: apex t ∈ {5,6} at faces | 269 (r7-14) | 5 | 0 |
| famX: extensions of row #1 | 356 (r9-14) | 1 | 0 |
| famK: kill6, top 12 rows | 329 (r9-14) | 1 | 0 |
| famK2: kill6 for every link 6 of all 245 certificate rows (315 keys, 386 key/letter families) | 2,823: all families to ring 13; ring 14 only for the 11 heaviest keys | 6 | 0 |

- 24 of the 65 fam2a hits are apex-t windows; they are included in the 29 tkill lines.
- **Still open:** row #6 (7557755/7575757, 4.4 %), face 1, apex t = 6. No D up to ring 14 (145 windows).
- **Not run:** ring 14 for the remaining kill6 families (about 2,900 windows, roughly 4 hours of one core).
- The heavy keys 57667786, 56677687, 56777675 and 57775665 have no D up to ring 14.

## 3. The kill6 entries [P] (configs_D_kill6.txt has the kc lines and entries)
Key = U, then w(j-2, j-1, j+1, j+2), then s(j-2, j-1, j, j+1), then the killed letter of the private. '.' means any letter. Both orientations are set; only the U=7 table changes.

| # | U | w(j-2,j-1,j+1,j+2) | s(j-2,j-1,j,j+1) | Killed private | Ring |
|---|---|---|---|---|---|
| 1 | 7 | 556. | 576. | 6 | 12 |
| 2 | 7 | 655. | 676. | 5 | 12 |
| 3 | 7 | 655. | 676. | 6 | 13 |
| 4 | 7 | .556 | .576 | 6 | 12 (also 5576, subsumed) |
| 5 | 7 | 556. | 5765 | 6 | 13 (subsumed by #1) |
| 6 | 7 | 5656 | ..76 | 5 | 13 |

The table folds the 7 windows into 6 distinct entries; two of them are subsumed by others.

- **Patched table:** `kill6r/kill6r_U7.npy.gz`. It sets 222 new bits; U8 and U9 are copies of the k95f tables. `scripts/k6patch.py` rebuilds it from the result files.
- **Rows affected:** `k6_rows.txt` (22 rows, 34.3 %).

## 4. Apex t (tkill_B1.txt, configs_D_apex_t.txt, facekills.json)
**Smallest lines:**
- `* w@0=55 s@-1=65 kill=5` (r7)
- `* w@-1=555 s@-1=75 kill=5` (r8)
- `7 w@-1=5556 s@-1=757 kill=6` (r11)
- `7 w@-1=6556 s@-1=657 kill=6` (r11; this is D11)
- `7 w@-3=557555 s@-1=757 kill=6` (r12)

**LP effect [M]:**
- **Over the pool:**
  - fy2 with an empty table gives −0.00844, so the fy2 relaxation alone costs about 0.034.
  - With fy2 + tkill_B1 the LP sits at its floor, t = −0.100, with only 35 dual rows.
  - This number is uninformative: the pool has no rows that bound the cell columns the kills free up.
- **Over the certificate's rows:** fy2 empty −0.0141, tkill_B1 −0.213, oracle (t ≥ 7 everywhere) −0.243. So on these rows the B1 table gets most of the oracle's effect.
- Both cases need a separation solve to mean anything.

## 5. Cell kills [P] (configs_D_cells.tsv)
Non-apex windows, mostly fives among the private neighbours of a link 7:
- row #5 (7767575/5665557, 11.6 %): p52=5 (3 windows), p51=p52=5 (7), p32=p52=5 (5), and others;
- row #1: p11=p12=5 (10 windows), p51=5 (ring 13).

They need a new receiver key for the private neighbours of a link 7 before the LP can use them.

## Suggested next steps
1. Add kill6r_U7 to the stack and run lowerR2 with separation, warm-started from `results/pool_all_W7rows.txt.gz` plus `results/sol_b1k6rN.json.gz`. This settles whether the patched t* is still > 0.
2. Run ring 14 for the remaining kill6 families.
3. Run a separation solve for fy2 + tkill_B1.
4. Add an LP key for the private neighbours of a link 7.

## Files
- **Kill lists:** configs_D_kill6.txt, kill6_entries.txt, kill6r/, k6_rows.txt, tkill_B1.txt, configs_D_apex_t.txt, configs_D_cells.tsv, facekills.json
- **Decode and LP summaries:** decode_B1.txt, toprows.txt, rlp_summary.tsv, rlp_drop1_top30.txt, rlp_env.sh, rlp_flags_k6p.txt, rlp_flags_k6r.txt
- **windows/** (*.tsv.gz): every window list
- **results/:** res_*.tsv.gz (all verdicts), nosep_*.log.gz, cert_b1k6rN.json.gz, sol_b1k6rN.json.gz, pool_all_W7rows.txt.gz
- **scripts/:** the generators, the screeners, mapper, k6patch, rlp and rlpdiff

## Coordinator note (Opus, 5 Nov)
- The kill6 bits still need an independent rebuild: our table builder with the 7 configs added to the forbidden set, then Studio's builder.
- The 7 configs need Lean hD.
- Team A's flat 5/8 floor (lowerR2 VALID t ≥ 0): its rows have no degree-7 vertex, and only the U=7 table changed. So I infer
  that the patched stack still has t* ≥ 0; a re-run of that certificate on the patched tables would confirm it. The target is therefore t* = 0 exactly. That is enough for a proof, since every vertex ≤ 0 contradicts a total charge of 12.
