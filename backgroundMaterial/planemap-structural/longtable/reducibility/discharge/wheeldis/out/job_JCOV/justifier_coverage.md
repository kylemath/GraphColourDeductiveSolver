# JCOV (ST-5): Lean coverage of the keep95p131f justifiers (Studio, 7 Nov)

Input: keep95p131f/rule_provenance.tsv (45a4c6d1 rules; 3,631 distinct justifiers). Script loop/studio/opus_check/f2b041/keep95p131f/jcov.py; Lean index jcov_index.py
(every Conf literal and every hD/hC/run/dred/agreesRSST theorem in our .lean files, tracked and local). Identity = the justifier's own kc line, matched by
(r, m, ring lists, interior lists) to a Lean literal; RSST rsstNNN = DCheckData cfg_NNN (interior degrees checked) with an agreesRSST theorem on a D2 entry.

## Totals
| class | justifiers | of them cited by a 2b362955 rule | single-justifier rules resting on them |
|---|---|---|---|
| Lean | 647 | 576 | 1611 |
| engine-only | 2984 | 2279 | 6267 |
| none | 0 | 0 | 0 |

## By source (Lean / engine-only)
| source | Lean | engine-only |
|---|---|---|
| C Lean531 | 54 | 2 |
| C Lean531 (RSST) | 10 | 0 |
| C core95 | 5 | 0 |
| C k3x13 | 13 | 0 |
| C rsst118 | 118 | 0 |
| D RSST | 107 | 0 |
| D k3p | 0 | 2 |
| D k3x | 4 | 102 |
| D nl51 | 336 | 2878 |

**Single-justifier rules resting on a justifier with no Lean module: 6267** (of them, rules whose justifier is also cited by 2b362955: justifiers 2279).

## Findings
- **D nl51:** 336 of 3,214 have Lean hD (HDC502 HDCV, HD0 hd30, HDW13, OCC13 hd13, ...); 2,878 are engine-only. Evidence per name: explore round 54d (6368d2f5,
  loop/k53/nl54d_verdicts.txt; per-config kc / dfast lines in loop/k5x/*_kcc.out, *_df.out) and Studio job54d / job54e (8fd249f6, A_kcc.out kc -C -s 60 -t 600,
  A_df.out dfast18). Engine-column coverage among the engine-only nl51 (has kc line, has dfast line): {(True, True): 2878}.
- **D k3x:** 4 Lean, 102 engine-only (registry tierA/k3x_D_A100.out kc lines, D=true). **D k3p:** 2 engine-only (k3p_D.out, "two engines").
- **D RSST:** all 107 Lean (DCheck agreesRSST: rsst_r9_agree, rsst_r10_11_agree, rsst_r12*/r13* lists, on rsstContract = 0 entries).
- **C:** 200 of 202 Lean (Lean531 56 -> 54, RSST-named 10, CK108 18, rsst118 118). **The 2 exceptions are k63f entries** (f7_...5676_..56.5. and f7_..56766_...655.,
  listed in keep_lean_C.txt as k63f): out/lean_k63f/aa74d7ec/K63F.lean proves only XRData.ok, admissibleX and foldSafeX for the 111 k63 entries; no cReducible18 (hC)
  theorem for them is in our files. Their C verdicts are engine evidence (k3x_C_A100 cfast). One of them (f7_..56766_...655.) is cited by a 2b362955 rule.
- A literal counts as Lean-backed when the theorem exists in our files; HDC502's HDCV*.lean sources are local only (their logs and status.txt, exit 0 sorry 0, are on main).

Columns of justifier_coverage.tsv: name | kind | source | n_rules_citing | n_single_justifier_rules | cited_by_a_2b362955_rule | lean_module | engines | evidence | match_note.
