# keep95p131 rule provenance (Studio, 4 Nov)

## Derivation and identity check
- **Script:** out/job31/f2b_rulecheck.py, DERIVE mode. This is the derivation that produced rules_studio_keep95p131.json
  (f2439106).
- **Forbidden set:** the same keep95p131 forbidden set. Environment as keep95p131 (EXTRA_KC = nl51 + k3p_D + k3p_C_keep95p131,
  K3X = k3x_D_A100 + k3x_C_A100_keep95p131, RSSTC_KEEP = keep95p131_C.txt).
- **md5 before / after the change:** cd0cf180 (as committed) / 67e95b66. The diff is in rule_provenance.diff.
- **The change is opt-in logging only (env PROVENANCE).** job() also records every justifying configuration name for each
  requirement set. DERIVE then writes, for each rule, the union of the justifiers over all requirement sets and structures that
  produce that rule. Nothing that feeds the rules is changed.
- **The regenerated rules file is byte-identical:** rules_regen_prov.json has md5 f2439106a0bd83593d795ee46624d96d, which equals
  rules_studio_keep95p131.json (cmp: identical). Counts:

| d7_w6 | d8_w6 | d9_w6 | d7_w7 ±1 | d8_w7 ±1 | total |
|---|---|---|---|---|---|
| 2,455 | 1,756 | 481 | 1,444 each | 908 each | **9,396** |

## rule_provenance.tsv
One row per rule: group | rule [p, w_req, s_req] | side (0 for w6) | n_justifiers | configuration names.

**Summary** (rule_provenance_summary.txt):
- **Rules with 0 justifiers: 0.** Rules with exactly 1: **7,916**. Rules with 2 or more: 1,480.
- **Single-justifier rules by group:**

| d7_w6 | d8_w6 | d9_w6 | d7_w7 ±1 | d8_w7 ±1 |
|---|---|---|---|---|
| 2,057 | 1,400 | 357 | 1,260 each | 791 each |

- **Distinct justifying configurations: 3,636.** By source:

| kind | source | configurations |
|---|---|---|
| D | nl51 | 3,214 |
| D | RSST D2 | 107 |
| D | k3x | 106 |
| D | k3p | 2 |
| C | rsst118 | 118 |
| C | Lean531 | 56 + 10 RSST in CCover |
| C | k3x13 | 13 |
| C | core95 | 5 |
| C | **k3p C (q7-), not in any list** | **5** |

- **Single-justifier rules by the justifier's source:**

| source | rules |
|---|---|
| nl51 | 6,954 |
| rsst118 | 480 |
| Lean531 | 186 + 58 (RSST) |
| k3x D | 136 |
| q7- k3p C | 38 |
| k3x13 | 28 |
| k3p D | 18 |
| core95 | 10 |
| RSST D | 8 |

## FLAG: 5 non-Lean k3p C configurations leaked into the keep / keep95 / keep95p131 table forbidden sets
- **The entries:** tierA/k3p_C.cfast holds 6 C entries. One is q7u_.556676_.5...6._::::::5, one of the 13 k3x C. The other 5 are
  q7- entries:
  - q7-_....556_...756._::::::5_p3R1/s3=5
  - q7-_....556_...756._::::::5_s3#2=5
  - q7-_...5566_...56.._:::::5:5
  - q7-_....556_....567_5*::::::5
  - q7-_...5566_...567._:::::5:5
- **The cause:** Studio's keep filter matched header names with `[A-Za-z]\w*_\S+`, which does not match a name beginning `q7-_`. So
  these 5 blocks were kept, and k3p_C_keep*.cfast reported "kept 1 dropped 0".
- **The consequence:** the keep, keep95 and keep95p131 table forbidden sets each contain 5 C configurations that are in neither the
  Lean sets nor core95 / 131. Their stated counts include them, e.g. 12,273 for keep95p131.
  - **70 of the 9,396 derived rules are justified only by these 5:** 18 each in d7_w6, d8_w6 and d9_w6, and 4 per side in d7_w7 and
    d8_w7.
  - They may also contribute §14' kill cells and V7 / V8 mask kills. That has not been checked yet.
- **Effect on earlier conclusions:**
  - keepcover.md (keep infeasible) and the keep95 infeasibility both stand, because the leaked entries only made those keep sets
    stronger.
  - **keep95p131_upper.md (FEASIBLE at 0.041565) and Opus's re-solve may depend on these 5.** Two ways to close this:
    1. re-prove the 5 as C (two engines plus Lean, as CK108), which is cheap; or
    2. rebuild keep95p131 without them and re-run the upper.
