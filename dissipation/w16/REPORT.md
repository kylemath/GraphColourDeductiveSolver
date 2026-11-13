# W16 zero-Euler: final report (5 Nov 2026, about 20:05Z)

Saved by the thread lead from W16's hand-back, because the harness refused the worker's own write. Everything else is in this folder: certs/, data/, code/, logs/ and FALSIFICATION.md. Cert md5: x567SO_base e2040ec0, x567SO_rrz 64c6d3bd, x567SO_all 774e1603, x567SO_allK 752accf0.

Labels:
- **[M]**: HiGHS float.
- **[P]**: exact result, one engine.
- **[E2]**: two engines agree. One is the Opus pcheck `lowerR2` (A97 stack, FLAGS line, families on). The other is W16's exact Fraction algebra on the Studio-side rows (st21_w10 row functions, keep95p131f stack).
- **[E3]**: st21_w10 `LOWER` also returns VALID.

## 1. Answer

**No family that exists can reach t = 0. The reason lies entirely in the 5/6/7 world.**

What the world contains:
- Every admissible degree-7 receiver whose link and second ring use only the letters 5, 6 and 7: 110,087 rows on the Studio-full stack.
- Every sender whose word is in {5,6,7}: 2,020 rows.
- Every cons2 row of a {5,6,7} 6-word that is not R6: 1,984 rows.
- The mrow closure.

These rows are a subset of the full LP. So each value below is a lower bound on t* for that family, and no rule at degree 8 or more can lower it.

| family | 5/6/7 world bound | label | certificate (certs/) |
|---|---|---|---|
| base | **t ≥ 7/247 = 0.028340** | [E3] | x567SO_base_cert.json (21 rows) |
| + rr z zr (ZCAP 3) | **t ≥ 1/37 = 0.027027** | [E3] | x567SO_rrz_cert.json (22 rows) |
| + full q7 (Q7 Q7M Q7CAP 3; 999 q keys occur) | **t ≥ 9088476198451/1257073899483180 = 0.0072298663** | [E2] (st21 has no mrowQ) | x567SO_all_cert.json (710 rows) |
| + K* = EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B] | **t ≥ 267615649991/42380779135951 = 0.0063146** | [P], W16's builder only; no engine had K* when this ran | x567SO_allK_cert.json (693 rows) |

**The bounds hold on both stacks.** Every receiver in these certificates is admissible on Studio-full (A111 C included) and on Opus A97. During row generation W16 checked 7,600–8,500 active receivers per run with the Opus `admissible()`, and it rejected none. So the bounds hold on any stack whose kills are no more than Studio-full and Opus A97 combined. (Lead's note: not yet checked against the B1 patched298 kill6 bits or the route-F patterns; Opus asked to replay.)

**Opus results:**
- The q7 certificate passes as given: `LOWER-R2: VALID t >= 9088476198451/1257073899483180`, with no repair needed.
- The base and rrz certificates pass Opus `lowerR2` and st21 `LOWER` (VALID 7/247 and VALID 1/37).

**Comparison with known values:**
- rrz 1/37 = 0.0270 sits below Team C's rr+z+zr in-points on A97: 0.0320 (in13) and 0.0316 (in14).
- base 7/247 = 0.0283 sits below b77's A97 base bound of 667/19840 = 0.0336.
- So the 5/6/7 world alone gives about 84–85% of both.

**The small certificates name the rows.**
- rrz (1/37):
  - 8 senders (55757, 55767, 55777, 57777 in various hats)
  - cons2 5766 67
  - mrowR2 / mrowL rows
  - 6 receivers: 5556667/7576677, 5556677/7576757, 5557557/5777777, 5757577/5577567, 5757677/5556657, 5757677/5577657
- base (7/247): the same core receivers, plus 5575577/5775757, 5575757/7775577 and 5757577/7577755.

**Killing link classes does not restore 0 [M]:**
- Dropping all receivers of any one of the 12 heaviest link classes leaves t > 0. The values run from 0.00397 (dropping 5556677) to 0.00702.
- Dropping 5556677 (Team C's E), 5757677 (G) and 5556676 together, then re-running full row generation over the world, still gives **t = 0.000213659539**.
- The q7 certificate spreads 150 receivers over more than 60 link classes.

**Other worlds:** the pure 5/7 world reaches 0 with q7, and the 5/8 floor reaches exactly 0. So this obstruction needs the 6s.

## 2. Falsification (FALSIFICATION.md)

**No explicit small torus triangulation was found with all rows admissible and no payee kill [M].** The search was not exhaustive:
- About 150 anneal runs: tori with n = 9..30, over 12 degree sets (5/7, 5/8, 5/9, 5/6/7, 5/6/8, 5/7/8, 5..9, and others).
- 1,675 six-sea defect clusters, with at most 4 flips each.
- Every vertex was checked with Studio `admissible()` and with the k6, l3q V7/V8 and f2b payee-kill masks.

What blocked them:
- Near-misses always failed at a big vertex: PAT, RBIG, or k6/l3q payee kills.
- The 6-sea clusters failed on R6 (566666), R6 fans and RBIG.
- One n = 12 5/6/8 torus passed the 2-ball tests but was killed by k6.

A torus with all rows admissible can only certify t ≥ 0, through uniform weights. So the positive obstruction is a fractional world pattern: the families cannot tell its rows apart.

The pre-registered kill criterion ("every pattern is feasible at 0") is **not met**.

Validation gate passed: the 5/8 floor certificate gives st21 `LOWER` VALID t ≥ 0 with families on [E2].

## 3. Pure 5/7 world

W6 already covered this case, and W16's numbers agree.

| stack (receivers) | base | rrz | all | allK |
|---|---|---|---|---|
| Studio-full (363) | 0 | 0 | 0 | 0 |
| Common stack, Studio minus A111 C ∩ Opus (369) | 8/273 [E2] | 18/1813 [E2] | 0 | 0 |

- The 6 extra common-stack rows are link 5757577 with second ring 7557{555,557,575,577,757,777}.
- Studio kills them only through the A111 C patterns f7_..57575_...55.. and f7_.575757_..55..., which are not in Lean.

Rows that every t = 0 solution must hold at exactly 0 [M]:
- **all families:** 3 rows, R7 5575577/5775777, R7 5757777/5555755 and S 55777 H11011. This is exactly W6's certificate.
- **base:** 38 rows, in data/imp57SO_base.json. They include Team C's D (5557557/5777777), A (5575577/5775757) and C (5575757/7775577).

## 4. Team C cross-check (targets_v2; data/xcheck_teamC_v2.txt)

Strongest targets: rows that are both in the 5/6/7 world and carry weight in the certificates.

| Team C row | share of the q7 certificate | also in |
|---|---|---|
| r4b 5556677/7576757 | 8.7% (heaviest receiver) | base, rrz |
| r7 5757677/5556657 | 5.0% | base, rrz |
| r5 5557557/5777777 | 4.4% | base, rrz |
| r3b 5757577/5577567 | 3.0% | base, rrz |
| r1 5575577/5775757 | 2.6% | base |
| r6d 5556667/7576777 | 1.9% | |
| r6b 5556667/7576677 | not in q7 | base, rrz |
| r2 5575757/7775577 | not in q7 | base |

Rows outside this obstruction:
- r3 7577575/7555755 and r3c 7577575/7565755: Studio kills them (r3 via A111).
- r6: has an 8.
- r10 and r10b: have a 9.

So killing B (r3) does not touch the 5/6/7 obstruction.

## 5. What would change the plan

1. **A new family must first bring the 5/6/7 world to 0.** This is a necessary test and it is cheap: about 10 minutes with `rowgen.py` on data/world_567_7_std.pkl, plus a family hook in `w16lib.coef_of`, which is how K* was added. rr z zr, full q7 and K* all fail it; K* only lowers 0.00723 to 0.00631. W6 and W12 should screen candidate keys here.
2. **Killing the named rows is not a realistic way to reach 0.** The q7 certificate is broad, and dropping three whole link classes still leaves t > 0. A new family needs keys that tell apart the 5/6/7 second rings around a 7, where the 6s enter through cons2.
3. **Not done:** the 5/6/8 and 5/7/8 worlds. Their degree-8 receivers need roughly an hour of enumeration each.

## Files (/mnt/project-files/swarm/round6/W16-zero-euler/)

- **certs/**
  - x567SO_{base,rrz,all,allK}_cert.json with summaries: exact string weights in pcheck format, with the Opus 5-tuple q7sig.
  - c57O_{base,rrz}, c57noA111_{base,all}: pure 5/7 certificates.
- **data/**
  - world_567_7_std.pkl: 114,091 labels. Load it only with `python3 -I`.
  - drop567_all.json, xcheck_teamC_v2.txt, imp57SO_{base,all}.json, world57*_lp.json, six_rows.txt.
  - world57_SO.pkl and world57_noA111_opus.pkl.
- **code/**
  - world.py: builds the worlds.
  - rowgen.py: row generation; OPUSF=1 adds the lazy Opus admissibility check, DROPLINK drops link classes.
  - exact_dual.py: exact vertex dual by sparse Fraction elimination.
  - cert.py, opus_lower.py, opus_ns.py, st21_lower.py, drop_links.py, implicit.py, xcheck2.py.
  - w16lib.py (includes K*), explore.py, clusters.py, torus.py, load21.py.
- **logs/**: the key runs, including olowx567SO_{all,rrz,base}.log and st21_x567SO_{rrz,base}.log.
