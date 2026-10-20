# RELAY_SPEC_s39o — spec delta for [E2]: whole-window raw patterns (rpatN / rpatN2) and off-centre matching (offc)

Delta against the s33z stacked engine (RELAY_SPEC_s21/s22/s23 + PRIVCELL_SPEC; A67 registry `s33z/reg_A67`, `rpatD.txt`).
Full definitions are in `s39o/OFFC_SPEC.md`. That file's sections are cited here as §n.

## 39.1 Window model (unchanged, made explicit; §1)
A row is `d, w_0..w_{d-1}, s_0..s_{d-1}`, where `s_i` is the apex of `w_i w_{i+1}`. The known vertices are u, w, s. Exact means
u (degree d) or a letter 5..8, and 9 is never exact. Edges: `u w_i`, `w_i w_{i+1}`, `w_i s_i`, `w_{i+1} s_i`, and
`s_{i-1} s_i` iff `w_i = 5`. Faces: `u w_i w_{i+1}`, `w_i w_{i+1} s_i`, and `w_i s_{i-1} s_i` iff `w_i = 5`.

## 39.2 rpatN files (option `rpatN=FILE[,FILE]`; §3)
- Line format: `d LINK SWORD [# comment]`. Characters are 5–8 (that exact letter), `N` (LINK only, {6,7,8,9}) or `.`
  (free). A row is killed when some rotation or reflection of the pattern (the same 2d maps as `pcheck.instances`)
  has every slot letter in its set.
- Built by `s39o/rpatN_build.py KC OUT` from kc lines `NAME r m RINGNB INTNB`, where deg = |ring| + |interior|.
- For each configuration vertex c with degree d in 7..17, take every embedding with `c -> u` into the degree-d window.
  The embedding is injective, the images are exact with equal degree, it is induced, and the interior 3-cliques land on
  faces. Each embedding becomes one pattern: the image slots get their letters, and a non-image `w_i` between image
  `s_{i-1}, s_i` gets `5` (if the edge is in the configuration) or `N` (if not). Patterns are kept up to the
  dihedral maps.
- **rpatN** = `s39o/rpatN.txt`, md5 `c7e8bfa8b3430a546cf7bc2cd0239595`, 37 patterns.
  - Source: explore's `loop/k55/row55_hits_kc.txt` (57526d20), md5 `47afb28d71c487132281b3bd5b217b01`.
  - 35 configurations, each D on kc and on dfast (`loop/k53/N54_res.txt`, `N54_kcc.out`, `N54_df.out`; 35/35 checked).
- **rpatN2** = `s39o/rpatN2.txt`, md5 `b4ce13844f203a488e98abb936a54a43`, 2,059 patterns (d7 564, d8 762, d9 559, d10 166,
  d11 7, d12 1). It has 60 `N` conditions and contains every rpatN pattern.
  - Source: explore's `loop/k56/nl54d_confirmed_D_kc.txt` (branch `claude/project-thread-nh6pv2`, 2e2081df), md5
    `04403db1f5e7b0a774d5c57dd018f22e`.
  - 6,053 configurations, D on kc -C and on dfast, rings 6–14 plus 153 at ring 15.
  - Build time 26 s.
- Checks:
  - against explore's sites files: rpatN kills exactly the 27 of 45 A67 binders that have a u-embedding, and
    rpatN2 kills exactly the 5 of 13 rpatN binders that have one;
  - the per-configuration u-embedding counts equal explore's (`rpatN_check.log`, `rpatN2_check55.log`,
    `rpatN2_check56.log`);
  - one exhaustive separator pass takes 77 s with rpatN and 76 s with rpatN2.

- **rpatN3** = `s39o/rpatN3.txt`, md5 `e153fc4146e166b56f3bd64a75f38141`, 2,287 patterns (d7 621, d8 839, d9 631, d10 188,
  d11 7, d12 1). It contains every rpatN2 pattern.
  - Source: explore's whole 2026 set `loop/k51/nl51_kc.txt` (6368d2f5), md5 `b9bc6e8bd9b86cf3a95873c05d9e7c34`, 8,200 configurations,
    rings 6-18. All 8,200 are D on two engines (`loop/k53/nl54d_verdicts.txt`, 6368d2f5, md5 `952575cace5f1137365bfcff8e1fcd84`).
  - Count check: rpatN2's 6,053 + job54d (rings 16-18, 610/610 two-engine D) + job54e (ring 15, 1,535/1,535) from main da31feea
    = 8,198 names, all in nl51 with identical lines; nl51 adds nl1281_r15 and nl1282_r15. Both sources give the same 2,287
    patterns (`k57/rpatN3_union8198.txt`, same pattern set, differs only in its header).
  - Build time 48 s. One exhaustive separator pass (as for rpatN2): 81 s with rpatN3 against 85 s with rpatN2 in the same run.

## 39.3 offc (flag `offc`; §2, §4)
- Each registry entry (pat=, cpat=, nf, rpat, rpatN) gets a configuration K.
  - K = u + the exact singleton slots, with the induced window structure.
  - u is dropped iff `m = |exact|` and the ring size `Σdeg − E − 3n + 3` equals the recorded `r`.
  - The entry is skipped when an `s_{i-1}, s_i` pair has `w_i` unpinned, or when `(r, m)` is not reproduced.
  - RSST 2.126 and 8406.123 are excluded by name.
- Every embedding of K anywhere in the abstract degree-d window (d = 7..17; same conditions as 39.2, with the image of
  a K vertex being u only if its degree is d) becomes an extra pattern in `PATS[d]`. The DFS separator,
  `admissible()`, lowerR2, upperR2 and binderR2 therefore all treat it exhaustively, as before.
- A67: 15,990 configurations give 14,722 off-centre patterns.
- Controls:
  - (a) flag off reproduces q66: identical lower, upper and binder logs;
  - (b) the d12 row 555555555555/757575757575 is hit by f7..f11 `.....55_....575`, `f7_...5555_.......` and `nl0040_r8`;
  - (c) the networkx physical test has 0 mismatches over 955,500 (row, configuration) pairs, and its broken control has
    8 mismatches.

## 39.4 Results on A67 (l3q-only flag set FQ, warm; one engine)
| variant | keeppen t (upper) | lower (nosep cert) |
|---|---|---|
| reference q66 (none) | 0.128957775 | 55686/438047 = 0.127123 |
| (i) rpatN | 0.125955995 | 636/5071 = 0.125419 |
| (ii) offc | 0.128329786 | — |
| (iii) offc + rpatN | stopped unconverged (t flat 0.125896) | — |

## 39.5 Result on A74 (main 95ba762d, 2,645 D / 1,156 C): l3q + rpatN3 — the pair for Studio
- Flags (one engine, `s39o/eng/pcheck.py`): `xon apexcls filt16 killtab=reg_A74/f/kill/kill6 hat5 consall l3q
  l3qtab=reg_A74/tab_1.json,reg_A74/tab_-1.json lqcap=3 rpatN=s39o/rpatN3.txt` with `args=reg_A74/args_A74.txt rpat=rpatD.txt`,
  conservation basis `s21/cf/cons2basis_cls.json`. No offc and no stacked flags. Registry tables are `s33z/reg_A74`
  (`prep_tag.sh A74 95ba762d`; k3x_D md5 3c71d994…, k3x_C md5 14bbdeed…).
- keeppen K (warm from run_n's rows plus the partial A73 rows) converged at iter 34: t = 1/9, 132,551 rows.
- **UPPER-R2 FEASIBLE at t = 0.111111111111** (sol_q39n3A74.json, md5 2680fb64…).
- **LOWER-R2 VALID t ≥ 20/183 = 0.109289617** (nosep cert cert_q39n3A74L.json, 160 rows, md5 9ba47b69…).
- Binders (10 receiver rows, canonical keys in `run_n3_A74/binders_canon.txt`); 8 of the 10 are d7.
- RSST 2.126 and 8406.123 are not in any input: they are not in rpatD, the args registry or nl51_kc, and offc excludes them by name.

The stacked run (s33z F + rpatN3, `run39s.sh s3 A74`) is still running. See LOG.md.
