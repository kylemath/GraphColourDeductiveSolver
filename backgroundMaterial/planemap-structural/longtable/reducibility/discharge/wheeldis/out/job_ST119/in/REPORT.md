# W6b round 12 (RSST-SUB2): substitutes for the full-world "none"-only leaves at d6/d7/d8

(Saved by the lead from W6b's hand-back, 10 Nov 2026 ~15:10Z. Full write-up in SUBSTITUTES2.md; MD5SUMS 9397b020, which does not cover this REPORT.md. [P], container engines.)

**Result.** Of the 143,961 full-world leaves (Studio RSST-1SHOT, K582) that only "none" configs kill, **143,535 now have a substitute. 426 are left.** They are all at d6 (needing 2.126) or d7 (needing 128.1324802).

**Method.** Each leaf is tested once. Its unread apexes and privates are 9+, which gives the fewest hosts, so a config found in the leaf is found in every state the leaf stands for. A model check on 3,000 random leaves matched the Studio's none sets.

| d | leaves | 7 Lean configs from the 2026 set | rest of the 2026 set (greedy 136) | windows (greedy 13) | left |
|---|---|---|---|---|---|
| 6 | 3,917 | 2,730 | 178 | 664 | 345 (2.126) |
| 7 | 84,292 | 25,273 | 58,680 | 258 | 81 (128.1324802) |
| 8 | 55,752 | 27,555 | 28,197 | 0 | 0 |

**Notes on the sources.**
- nl0004_r8 alone covers 47,694 leaves.
- The 136 other configs from the 2026 set would join the Lean D queue. They have not been D-rechecked this round.
- The windows include P20, three round-11 C windows, a new D window fw_980b7e87e4 (ring 13) and eight new C windows. All 67 new C windows pass valid_contract and admissibleX. P21 occurs in none of the leaves.

**What is left.**
- **d6, 345 leaves.** Links 565669, 565668, 565667 and 5659x9. Here the apexes next to the 2.126 occurrence are 9+, and every C window that was found needs a 6 there.
- **d7, 81 leaves.** Links 5657669, 5659669, 5658669 and 5658668, each with a 9+ vertex.
- **329 of the 426 are exhausted.** Every window inside the leaf's hosts up to ring 16 screened N under kc -C's |X| ≤ 4. So these need 2.126 or 128.1324802 themselves, which means ring-merge admissibility, or reasoning beyond the window.
- The other 97 leaves still have 352 unscreened windows (results/xf_batch.tsv).

**Not done:**
- the family-u u-centred patterns (the list was not on the mount);
- D rechecks of the 136;
- windows above ring 16, or with |X| > 4.
