# RSST-SUB2: substitutes for the full-world d6/d7/d8 states that only "none" configs kill

W6b, 10 Nov 2026, [P].

- **Input:** Studio RSST1SHOT `results/NEEDS_NONE.tsv.gz`, source = fullworld. These are 143,961 DFS leaves: d6 3,917, d7 84,292, d8 55,752.
- **Engines:**
  - my fp2 window and matcher (round10, 0c4804e2);
  - W13's mscreen, running kcc_o3 and dfast18/cfast from /tmp/swarm-W13/bin;
  - round9's vc_check `check()`, used unchanged, for valid_contract and Lean admissibleX.
- **Limits:** 1 cpuslot slot (tag W6b-RSSTSUB2).

## Leaf-level reasoning (why one test per leaf is enough)

A leaf fixes its read letters; its unread apexes and privates are 9+.

- The leaf's hosts are u (letter d), plus every w, s or private whose letter is 5..8.
- A configuration found among those hosts is also among the hosts of every state the leaf stands for. Changing an unread or dominated 9+ letter to 5..8 only adds a host, and fp2's containment is monotone in the hosts.
- So each leaf is tested once, and no filling is enumerated.
- **Model check:** 3,000 random leaves. 3,000/3,000 contain no proved RSST configuration, and the none configurations they contain equal the Studio's none set.

## Result

| d | leaves | L7 (2026 configs already in Lean) | N51 (rest of the 2026 set) | windows (already-proved E2 / round-11 C / new D / new C) | left |
|---|---|---|---|---|---|
| 6 | 3,917 | 2,730 | 178 | 0 / 56 / 0 / 608 | **345** (2.126) |
| 7 | 84,292 | 25,273 | 58,680 | 46 (P20) / 23 / 35 / 154 | **81** (128.1324802) |
| 8 | 55,752 | 27,555 | 28,197 | 0 | **0** |

- **(i) Family u-kills: not tested.** K3gB5u (ea00eec1) and pat_K5u_C.cfast (d0cdf5c1) were not found by name in W12, W13 or W17, in loop/, /tmp or /home/user within the 10 minutes. I could not ask (no messages in my rules).
  - K3gB5n's lists are in W12-studio-K/from_opus/fam_args, but they are not the requested family.
  - **Caution for when the list arrives:** slot-set patterns (B = {7,8,9}) are not monotone in the hosts. A pattern is sound at leaf level only if it has '.' at every position where the leaf has 9+.
- **(ii) L7:** 55,558 leaves. All 7 configurations are used.
  - Greedy order: nl0004_r8 47,694; nl0078_r11 3,241; nl0008_r9 2,317; nl0050_r10 1,700; nl2837_r11 577; nl0018_r11 24; nl0067_r10 5.
- **(ii) N51:** 87,055 of the remaining 88,403 leaves. Greedy cover: 136 configurations. The first 34 reach 90%, and 36 picks add ≤ 10 leaves each.
  - Largest: nl0289_r11 8,212; nl1755_r13 6,612; nl3352_r13 5,528; nl3174_r13 4,904; nl0278_r11 4,674; nl1816_r12 3,881; nl0077_r11 3,573; nl0857_r13 3,559.
  - The full list is results/fw_greedy.tsv.
  - Not re-checked D in this round. Round 11 re-checked 39 of the 2026 set D on both engines; the coordinator states all 8,200 are D on two engines.
- **(iii) Windows** for the 1,348 leaves left after nl51. 922 are covered, by a greedy of 13 windows (results/cf_given_greedy.tsv), all screened on two engines (kc -C, then dfast18 or cfast --fixed):
  - fw_13f30da28e: C, ring 10, 387 leaves (d6)
  - fw_f7c75a21e2: C, ring 13, 144 (d7, 126.3686402)
  - fw_d80034e607: C, ring 10, 132 (d6)
  - fw_59905b5526: C, ring 12, 55 (d6)
  - **fix_63c8a193fe = P20: C, ring 14, 46 (d7, 128.1324802)**
  - fix_b80e8a0990 (round 11): C, ring 11, 46 (d6)
  - **fw_980b7e87e4: D, ring 13, 35 (d7, 126.687602; dfast18 D)**
  - fw_e4befbe5e1: C, ring 11, 24 (d6)
  - sub_b376bcffea (round 11): C, ring 14, 23 (d7, 128.1324802)
  - fw_f3d4a8ea73: C, ring 12, 10 (d6)
  - fix_50f4aa3e7d (round 11): C, ring 11, 10 (d6)
  - fw_ed8b171a03: C, ring 14, 6 (d7, 128.1324802)
  - fw_5ce6c53845: C, ring 16, 4 (d7, 128.1324802)
  - **Contract check:** all 67 new C windows from this round's screens pass valid_contract and lean_admissibleX (results/vc_fw_windows.tsv), as the round-11 windows did. So they use our admissibleX C path, not the valid_contract port.
  - P21 (fix_404d45e819) occurs in none of the 1,348 leaves left after nl51.

## Per sole killer: which source covers its leaves

From results/fw_final_by_sole.tsv. Each leaf counts once, under its cheapest source: L7, then N51, then E2 window, then round-11 window, then new D, then new C.

- **All sole killers are fully covered except 2.126 at d6 and 128.1324802 at d7.**
- **d8 (23 sole killers):**
  - covered by L7 alone: 126.442802;
  - L7 + N51: 2.126 and 126.1306802;
  - N51 only: the other 20.
- **d7 (26 sole killers):**
  - all by N51, except as listed;
  - 126.1306802 and 126.442802 mostly by L7, and 2.126 at d7 127/142 by L7;
  - 126.3686402: 20 N51 + 144 by window fw_f7c75a21e2 (C);
  - 126.687602: 35/35 by window fw_980b7e87e4 (D).

| sole killer | sole leaves | L7 | N51 | windows | left |
|---|---|---|---|---|---|
| d6 2.126 | 3,917 | 2,730 | 178 | 664 | **345** |
| d7 128.1324802 | 4,368 | 0 | 4,208 | 79 | **81** |

**What is left: 426 leaves.**

- **d6 2.126, 345 leaves.**
  - Links: 565669 (78), 565668 (60), 565667 (21), and 9 each for 565959, 565969, 565979, 565989 and 565999.
  - Typically the apexes s0 and s1 next to the 2.126 occurrence are unread, so 9+. The C windows here all need s0 = 6 or s1 = 6.
- **d7 128.1324802, 81 leaves.**
  - Links: 5657669 (46), 5659669 (16), 5658669 (13) and 5658668 (6). Each has a 9+ link vertex.
- **Exhaustion status** (results/xf_leaves.tsv):
  - 329 of the 426 (2.126: 289; 128.1324802: 40) are **exhausted**: every window inside the leaf's hosts, at ring ≤ 16, was screened N.
  - So no D or C substitute exists inside the 2-ball window for them. That holds within kc -C's |X| ≤ 4 search.
  - These leaves need 2.126 or 128.1324802 itself, or a model larger than the 2-ball.
  - The other 97 (2.126: 56; 128.1324802: 41) still have 352 unscreened windows (results/xf_batch.tsv).

## Greedy minimal set by source

- **L7:** all 7.
- **N51:** 136 configurations (fw_greedy.tsv), which would join the Lean D queue.
- **Windows:** 13. Of these, 1 is the already-proved P20 and 3 are round-11 C windows. The rest are new: 1 D and 8 C.
- **Left:** 426 leaves for 2.126 and 128.1324802, of which 329 are exhausted.

## Method / files

- `code/fwsub.py`: leaf reading, model check, L7, N51 and the greedy.
- `code/fwwin.py`: windows by the round-11 method; cover check of given windows; window greedy (E2 first, then D).
- `code/fwexh.py`: all windows per leaf, and exhaustion status.
- `code/fwhosts.py`: hosts and windows per leaf.
- `code/vc_fw.py`: contract check.
- `code/fwfinal.py`: source assignment.
- `code/run_ms.sh`: mscreen with a stop time.
- `results/`:
  - fw_leaves.tsv.gz: every leaf with its source and pick;
  - fw_final_leaves.tsv.gz, fw_final_by_sole.tsv: per-leaf and per-sole-killer tables;
  - fw_greedy.tsv, fw_by_noneconfig.tsv, fwsub.log;
  - s4..s7.tsv (+ .log): mscreen results;
  - batches and supports: w4, c1, c128, g2126, g128, x1, the *_rr files;
  - cf_*: final window cover, greedy and still-uncovered leaves;
  - xf_*: exhaustion;
  - vc_fw_windows.tsv; c2_still_hosts.tsv.

## Verified / not verified

- **Verified:**
  - the leaf model (3,000/3,000);
  - the coverage of every leaf by L7, N51 or windows;
  - window verdicts on two engines;
  - the contract checks;
  - exhaustion of 329 leaves within ring ≤ 16 and |X| ≤ 4.
- **Not verified or not done:**
  - the family u-kills (list not found);
  - D re-checks of the 136 N51 picks in this round;
  - the 352 unscreened windows of the 97 open leaves;
  - windows at ring > 16;
  - kc -C with |X| > 4.
