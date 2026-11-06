# keep95p131f rule provenance (Studio, job PROV5F / claim ST-4, 6 Nov)

**Result:** all 9,326 rules of rules_studio_keep95p131f.json (45a4c6d1) have at least one witness configuration. The regenerated rules file is
**byte-identical** to 45a4c6d1. Every one of the 202 distinct C justifiers is in the keep95p131f keep set and Lean-backed. **0 rules depend only on
configurations outside the keep set or the Lean-backed lists.**

## Derivation and identity check
- **Script:** out/job31/f2b_rulecheck.py (md5 67e95b66, unchanged since 1dea8820/55cfd103), DERIVE mode with PROVENANCE. This is the derivation that produced 45a4c6d1.
- **Environment:** exactly the 55cfd103 rebuild, recovered from the run record: EXTRA_KC = tierA/nl51_kc.txt, tierA/k3p_D.out, keep95p131f/k3p_C_keep95p131f.cfast;
  K3X = tierA/k3x_D_A100.out, keep95p131f/k3x_C_A100_keep95p131f.cfast; RSSTC_KEEP = keep95p131f/keep95p131f_C.txt; NPROC = 5; the rule JSON argument is
  in/gc/kill_upgraded/tierA/full2ball_extra_rules.json. The forbidden set has 12,268 configurations. None of these inputs changed after 55cfd103 (git log and status are
  clean), and nothing that feeds the rules was modified. The command is in prov5f/cmd.txt and the log in prov5f/rule_provenance_run.log.
- **The regenerated rules are byte-identical:** prov5f/rules_regen_prov.json has md5 45a4c6d1275f4bb2adb9826e4d8c953c, and cmp against rules_studio_keep95p131f.json is identical.
  CONTROL is PASS 5,954, FAIL 0.
- **Provenance:** prov5f/rule_provenance.tsv is byte-identical (cmp) to keep95p131f/rule_provenance.tsv, which was written by the 55cfd103 rebuild. The
  published copy is therefore unchanged. Its format is the same as before: group | rule [p, w_req, s_req] | side (0 for w6) | n_justifiers | configuration names.

## Counts per group
| group | side | rules | 0 justifiers | exactly 1 | 2 or more |
|---|---|---|---|---|---|
| d7_w6 | 0 | 2,437 | 0 | 2,047 | 390 |
| d8_w6 | 0 | 1,738 | 0 | 1,390 | 348 |
| d9_w6 | 0 | 463 | 0 | 347 | 116 |
| d7_w7 | 1 | 1,440 | 0 | 1,258 | 182 |
| d7_w7 | -1 | 1,440 | 0 | 1,258 | 182 |
| d8_w7 | 1 | 904 | 0 | 789 | 115 |
| d8_w7 | -1 | 904 | 0 | 789 | 115 |
| **total** | | **9,326** | **0** | **7,878** | **1,448** |

**Rules with 0 justifiers: none.**

## Single-justifier rules, by source of the justifier
| group | side | C Lean531 | C Lean531 (RSST) | C core95 | C k3x13 | C rsst118 | D RSST | D k3p | D k3x | D nl51 |
|---|---|---|---|---|---|---|---|---|---|---|
| d7_w6 | 0 | 44 | 22 | 0 | 8 | 88 | 4 | 6 | 28 | 1847 |
| d8_w6 | 0 | 34 | 10 | 0 | 10 | 62 | 0 | 6 | 92 | 1176 |
| d9_w6 | 0 | 32 | 10 | 0 | 0 | 46 | 0 | 6 | 10 | 243 |
| d7_w7 | 1 | 31 | 8 | 5 | 5 | 87 | 2 | 0 | 0 | 1120 |
| d7_w7 | -1 | 31 | 8 | 5 | 5 | 87 | 2 | 0 | 0 | 1120 |
| d8_w7 | 1 | 7 | 0 | 0 | 0 | 55 | 0 | 0 | 3 | 724 |
| d8_w7 | -1 | 7 | 0 | 0 | 0 | 55 | 0 | 0 | 3 | 724 |
| **total** | | **186** | **58** | **10** | **28** | **480** | **8** | **18** | **136** | **6954** |

## Distinct justifying configurations: 3,631, by source
| source | count | in keep95p131f keep set | Lean-backed C list |
|---|---|---|---|
| C Lean531 | 56 | yes | keep_lean_C (531) |
| C Lean531 (RSST) | 10 | yes | keep_lean_C (531), RSST names |
| C core95 | 5 | yes | ck108 (CK108) |
| C k3x13 | 13 | yes | ck108 (CK108) |
| C rsst118 | 118 | yes | rsst118 (CR118) |
| D RSST | 107 | yes | – (D) |
| D k3p | 2 | yes | – (D) |
| D k3x | 106 | yes | – (D) |
| D nl51 | 3,214 | yes | – (D) |

- **C justifiers: 202**, all in keep95p131f_C.txt and all Lean-backed: 56 in Lean531, 10 RSST-named in Lean531, 18 in CK108 (core95 5 + k3x13 13), and 118 in rsst118.
  Unclassified: 0. The 5 q7- k3p C flagged last time are gone; the filter fix removed them, and no rule cites them.
- **D justifiers: 3,429** (nl51 3,214, RSST 107, k3x 106, k3p 2). All are in the forbidden D set of the keep95p131f keep (keep = all D + Lean C). Lean hD coverage for D
  justifiers was not part of this check.

## Rules whose only justifiers are outside the keep set or the Lean-backed lists
**None: 0 rules.** No justifier is outside the keep set, and no C justifier is outside the Lean-backed lists.

Full lists: prov5f/distinct_justifiers_by_source.json, prov5f/perGroupSrc.json (justifier occurrences per group and source), and rule_provenance_summary.txt.

**Independence:** this is our own DERIVE code only (f2b_rulecheck.py). I read neither Opus's REVIEW.md nor any Opus engine code.
