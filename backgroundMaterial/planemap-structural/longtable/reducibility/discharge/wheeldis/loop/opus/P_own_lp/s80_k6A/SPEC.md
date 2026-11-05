# s80 Team E: routes A' and L' in the LP stack (spec)

All values below are [P] (our engine) unless marked [M].

## 1. Where kill6 and l3q masks enter a receiver row now

Receiver row (d, w, s): centre u of degree d, link w_0..w_{d-1}, apex s_i between w_i and w_{i+1}. Python row = `recv_coef_R2` (prelay2.py), wrapped by f2bglue.py.

- **6 spoke j (M term).** sig = sig2_of(U, w_{j+1}, s_j, s_{j-1}, w_{j-1}, w_{j+2}, w_{j-2}) with U = min(d, 9). The private mask is am = amask(U, w_{j-2}, w_{j-1}, w_{j+1}, w_{j+2}, s_{j-2}, s_{j-1}, s_j, s_{j+1}). It is KT[U] (kill6 table) applied to that 8-slot window. The row gets +1 on column ('M', sig + (am,)). That column's value is MV2 = max of h over sig2_keys.
- **7 spoke j, side sg (l3q).** Here c = w_{j+sg}. The apex is a = s_j for sg = +1 and s_{j-1} for sg = -1, and o is the other apex. The side counts only when c <= 6 and a <= 6. The l3q table gives m = L3T[(sg, c, w_{j+2sg}, w_{j+3sg}, w_{j+4sg}, a, o)]: the a2 letters still possible. The payee column is ('lQ', (c, a, m)), valued Qeff(c, a, m) = max(LQQ(c, a, m), max over a2 in m of lq(c, a, a2)). At d = 8 the V=8 table is used and the key is ('lQ', (8, c, a, m)).
- **q7m (FAM=full).** The payer column ('Q', q7sig(..., m_+, m_-)) uses the same two side masks.
- **Studio f2b rules (f2b.py, group dD_w6 / dD_w7[sg]).** A rule is (p, w_req, s_req), with offsets mod d from spoke i. It fires iff w_{i+o} is in the allowed set for every w requirement and s_{i+o} = v for every s requirement. A firing rule clears bit p in a mask:
  - for w6, in am, so the column becomes ('M', sig + (am & ~ex,));
  - for w7[sg], in that side's m, so the lQ column and the q7m payer key both change.

  Python applies this in f2bglue.py: overrides of recv_coef_R2 (w6 and q7m), l3q_terms (d = 7) and l3q_terms_payeeV (d = 8).

## 2. What an A' / L' entry is, and what it does to a row

B3 entry (configs_D_kill6wide.txt = A', configs_D_l3qrow.txt = L'): a two-engine D window whose PRIVCELL q-name pins:
- some link slots and apex slots;
- one exact parent link vertex w_j;
- one private of w_j at letter p.

The windows are:
- **A'**: parent 6. The window reads slots outside the 8-slot kill6 window, so KT cannot hold it.
- **L'**: parent 7, and the private is that side's l3q a2. L1 next to s_{j-1} gives sg = -1, L2 next to s_j gives sg = +1. The window reads slots outside the l3q key.

**Implementation: each entry is an extra f2b rule, in exactly Studio's format.** scripts/mkrules.py builds the rule from the q-name:
- every constrained slot except the parent becomes a requirement at its offset from j;
- p and sg come from the single constrained private;
- both orientations are emitted (mirror: w offset o -> -o, s offset o -> -o-1, sg -> -sg);
- a centred name (`u`) acts only at d = its D;
- a centre-free name (`b10_-...`) is placed at every d' in 7..9 where PRIVCELL places it.

Row change, for a row and spoke where the rule fires:
- **A'**: ('M', sig + (am & ~ex0,)) -> ('M', sig + (am & ~ex0 & ~bit_p,)). Here ex0 is what the other rules already remove.
- **L'**: ('lQ', (c, a, m')) -> ('lQ', (c, a, m' & ~bit_p)), where m' = m & ~ex0 for that side. With q7m, the payer key Q(q7sig(.., m_+, m_-)) moves to the new masks too.

There is no change when bit p is already off: KT/L3T may not allow it, or another rule may already remove it. No new LP column is needed, because all keys are existing (sig, mask) / (c, a, mask) families.

**Soundness of each rule.** mkrules.py checks every rule independently of B3's naming code. It covers every structural variant of the matched 2-ball: each free link slot is 5, 6 or 7; each multi-letter slot takes each of its letters. For each variant:
- grow.py build2 builds the 2-ball;
- the entry's kc configuration must embed, with exact degrees, induced, and interior triangles onto faces;
- the embedding must cover the pinned vertices, with the killed private in the image.

Result: 98 / 98 placements verified (logs/mkrules.log). The q-names also match B3's route text. Negative controls (logs/mkrules_negctl.log) all fail as they should:

| Control | Failed |
|---|---|
| Letter changed | 98/98 |
| One w requirement dropped | 356/356 |
| One s requirement dropped | 298/298 |
| Side flipped | 40/40 |

Rule files are rules/rules_Ap.json (58), rules_Lp.json (40) and rules_ApLp.json (98). Against Studio's keep95p131f set, 22 of the 98 are already present, so 76 are new: d7_w6 34, d8_w6 6, d9_w6 6, d7_w7_1 15, d7_w7_-1 15.

Not covered: d >= 10. The f2b plumbing stops at d = 9 for w6 and d = 8 for w7, so B3's four d = 10 windows on 6656665665/6555655655 act only through their d = 7..9 placements. B3 lists that row as zero-dual. The Lean side needs the same hD lemma per window as for any f2b rule.

## 3. Separator (jsepf) stays an exact upper bound

The extra rules are appended to the f2b group lists (f2b.py `load(..., extra=)`). Python and jsepf therefore read the same rule set:
- f2b_write packs the rules into jsepf's per-d bucket file (keyed by s_{-1}, s_0; w and s requirements as 5-bit masks per offset over the whole link);
- the leaf correction (f2bExtra) is evaluated on the full row.

The DFS window bounds do not use the rules. A leaf can rise above its rule-free value only through a positive mask correction. The prune slack covers that: SLACK = d*dV + 2d*dQ + d*dT, where dV, dQ and dT are the largest increases of V6M, QMT and QTM over *all* (mask, submask) pairs. That covers one w6, two l3q sides and one q7m per spoke. The slack depends only on the value tables, not on which rules exist, so adding rules keeps every pruned subtree pruned soundly. A' / L' are therefore exact in the separator, not only conservative.

## 4. Interface

- Engine $N/eng = byte copy of s77_k6patch/eng plus two changed files: f2b.py (extra rule files, XRULES / XSTATS) and f2bglue.py (option, log line, self-tests). jsepf and other binaries are unchanged.
- Option `f2bx=FILE[,FILE..]` (requires f2b=). It is set by env80.sh when F2BX is set. A rule already in the base set is counted and skipped.
- Without f2bx, the engine builds exactly the original rule lists, so it reproduces eng_orig. See test (a) in run.log.
- Self-test: `upperR2 ... f2bx=.. f2bself=0 f2bxself=N [f2bxtries= f2bxkeep= f2bxsub= f2bxsl= f2bxtight=]`. It has parts (b), (c1), (c2) and (t); see the comment block in f2bglue.py.

## 5. Effect on our stack (measured at sol_b77F_in02, route-F args, FAM=full)

Coefficients are [P]. Values are [M] at fixed in02 weights.

- **Feasibility.** upperR2 with f2bx=rules_ApLp.json is FEASIBLE at t = 0.029906108105, Karp 0.546518400. These are the same numbers as without the extra rules.
- **Which rules change rows.** B3 measured its gains against KT / L3T only, not against Studio's f2b rules. On our stack most new rules are already implied:
  - 8 of the 76 new rules changed a sampled matched row: 2 A' and 6 L'.
  - The other 68 changed none. That is up to 1,500 tries per rule and 40 kept admissible matched rows each, so it is sampling, not proof of redundancy.
- **Near-tight rows (slack <= 1e-3).** 2 of the 634 d=7 rows change, each with a load drop of 0.3326. 0 of the 172 d=8 rows and 0 of the 56 d=9 rows change.
- **B3 target rows (1,054).** 24 change:
  - 21 are A' changes from M mask 30 -> 28, with no value change at in02.
  - 5577577/6675576 is tight and drops 1.029906 -> 0.697261, via B3's b7_u55775.._66.55.._p215 / p325 on both 7-sides.
  - 5766767/5656665 and 7676675/6665655 drop 0.0700.
