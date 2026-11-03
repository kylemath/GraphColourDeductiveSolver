# f2b041 job 3: per-rule soundness of the 5,954 full2ball rules (Studio, 3 Nov)

**Result: 5,954 / 5,954 PASS, 0 FAIL**, on the Tier A forbidden set (13,199 configurations). The w7 side→private mapping of
extract_full2ball_rules is confirmed, and both negative controls fail heavily.

## Method
The checker is out/job31/f2b_rulecheck.py, Studio's own code. It uses explore's grow.py `build2` frame and its induced `embeddings`,
the same machinery as out/job31/l3q_masks.py. No outside or Opus code is run.

**The forbidden set** is built exactly as for the Tier A tables (out/job31/f2bA):
- RSST D2/C2cons 582;
- k3x A100 D 3,096 and C 1,311 (c720336d);
- EXTRA_KC nl51_kc b9bc6e8b (8,200) and k3p D/C (10).

**What a rule claims.** Take a receiver row of degree d. At a spoke with w_i = w0 that satisfies w_req and s_req (offsets mod d),
the group's target private cannot have degree p. The target private is:
- **w0 = 6:** w0's one private;
- **w0 = 7, side +1 / −1:** w0's private adjacent to s_i / s_{i−1}. This is the l3q a2 of that side (l3q_masks.setup).

The claim holds because some forbidden configuration embeds into the 2-ball using the target private at degree p (reading A).

**The frame.** The 2-ball frame is u, w_0..w_{d−1}, s_0..s_{d−1} and w0's privates. On these vertices it depends on the letters only
through which w_k are 5, since w_k = 5 makes s_{k−1} and s_k adjacent.
- For each structure Z (each choice of which w_k are 5) and each (d, w0), all embeddings are enumerated once: 640 structures in all.
- u is fixed at degree d for d = 7, 8. At d = 9 it is excluded (the d ≥ 9 class). w0 is fixed at w0.
- Each embedding gives a requirement set. The check asserts that s_{k−1} and s_k are adjacent exactly when w_k = 5.

**When a rule PASSES.** Every structure consistent with the rule must contain a qualifying requirement set:
- **Consistent structures:** w_k = 5 iff allowed = {5}; w_k non-5 iff allowed ⊆ {6..9}; both otherwise, including unconstrained k.
- **Qualifying requirement set:** it uses the target at degree p, and every other vertex it uses is fixed by the rule (a w_k with
  allowed = {its degree}, or an s_k with s_req = its degree).
- In all, 29,312 (rule, structure) pairs were checked.

## Results (rulecheck_tierA.json / .log)
| group | target | rules | PASS | FAIL |
|---|---|---|---|---|
| d7_w6 | ('p',0,1) | 1,386 | 1,386 | 0 |
| d8_w6 | ('p',0,1) | 1,176 | 1,176 | 0 |
| d9_w6 | ('p',0,1) | 60 | 60 | 0 |
| d7_w7 +1 | ('p',0,2) | 938 | 938 | 0 |
| d7_w7 −1 | ('p',0,1) | 938 | 938 | 0 |
| d8_w7 +1 | ('p',0,2) | 728 | 728 | 0 |
| d8_w7 −1 | ('p',0,1) | 728 | 728 | 0 |

**Side→private mapping.** extract_full2ball_rules maps side −1 → ('p',0,1) and +1 → ('p',0,2). In Studio's frame, ('p',0,2) is the
private adjacent to s_0, which is the a2 of side +1 (l3q_masks: "sigma +1: a2 = ('p', 0, 2), a = ('s', 0)"), and ('p',0,1) is
adjacent to s_{d−1}. The mapping is therefore correct. The d = 7 rows then apply rules "1" to the side-+1 mask
MASK[(+1, c = w_{i+1}, a = s_i, …)], as make_recv_spec_full2ball does.

**Negative controls**, rerun from scratch:
| control | PASS | FAIL |
|---|---|---|
| CONTROL=swap (w7 rules checked against the other side's private) | 3,062 | 2,892 |
| CONTROL=pshift (killed letter p → p+1) | 118 | 5,836 |

Under swap, the w7 rules fail at 790 + 790 (d7) and 656 + 656 (d8). The rules that still pass are the side-symmetric ones; the w6
rules are unaffected. So the checker is sensitive both to which private is used and to which letter is killed.

**Completeness, the converse** (rules_studio_full.json, md5 4b8f6167; rules_cover.py, rules_cover_full.log):
- DERIVE builds Studio's own rule set from the same requirement sets:
  | d7_w6 | d8_w6 | d9_w6 | d7_w7 ±1 | d8_w7 ±1 |
  |---|---|---|---|---|
  | 2,477 | 1,778 | 493 | 1,473 each | 910 each |
- Studio's set does not apply the outside filter that drops rules lying inside the pmask / l3q window.
- On 20,862 arrangements (each outside rule instantiated 3 times, plus 3,000 random rows), 450,507 cells were compared. **No letter
  killed by the outside rules is missed by Studio's set.** Studio's set kills more in 89,130 cells.

## Dependence on non-Lean C entries (input to job 2)
Rechecked on the keep-only forbidden set (12,060: all D plus the 531 Lean-backed C), **312 of the 5,954 outside rules have no
justifying embedding**:
| group | rules without justification |
|---|---|
| d7_w6 | 40 |
| d8_w6 | 30 |
| d9_w6 | 0 |
| d7_w7 ±1 | 84 each |
| d8_w7 ±1 | 37 each |

These rules rest on C entries that are not Lean-backed (keep/rulecheck_keep.json). Job 2 therefore uses Studio's rules derived from
the keep set, keep/rules_studio_keep.json (fecebe35), not the outside file.
