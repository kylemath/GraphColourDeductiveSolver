# K3CHK3 (ST-13c): the two K-3 kills of 04:24Z (Studio, 7 Nov)
Inputs: 8f15f4e2 ext_handoff_nov3/k3/chk3/ (new_kills_0424.tsv e94e144a, binding_coverage.tsv, ...).

| config | verdict | engines | target row | occurs (rotation-preserving, Z-consistent) | still-uncovered rows at its d |
|---|---|---|---|---|---|
| (a) b9_u.56.56555_.5....... (r13, m9) | **C, X = {I0-I5}** | kc -C finds X={I0-I5} (5 tested, 5 admissible); kc -x adm=yes, leftover 0; cfast --fixed I0-I5 leftover 0 | line 155: 555657658/756756558 + violated rotations 856756555/556576578, 855565765/875675655 | **3 / 3 PASS** | none other than its own target (row 155) |
| (b) b9_u75..65656_5...55... (r14, m11) | **D** | kc -C D (199,291 = reached); dfast18 D | line 59: 565675676/566555555 | **1 / 1 PASS** | 1 (line 155): **does not occur (PASS)** |

**C admissibility of (a):** X is one interior edge, **not rim-pinned**; Lean lean/CK3C3.lean (gen_ccover3 XRData): XRData.ok, admissibleX, foldSafeX
**proved** (status.txt); hC K3C3V00 building. Verdict: both confirmed.
