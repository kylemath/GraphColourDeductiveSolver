# s68_rrz: why rr (flag hatrr) and z (flag zh/zr) are OFF in keep95p131f / s60_f2b (read-only investigation, no solves)

## What they are (own columns, not published rules)
- rr = reverse hat, HAT(B->5): column rr[K]>=0 under the s15 hat key K, moves charge from the big hat b to the five v (distance 2).
  Coeff -1 in v's senderR2 row, -1 in b's receiverR2 load (= -r, so r free in sign). RELAY_SPEC.md 15r (l.1381-1440); prelay2.py HRR (l.331, 486-493, 551-558).
- z / zh: five -> big split (EDGE(5->B)), z[K] with K = five link from the big + hat classes (stage 13, FINDINGS.md l.360ff); zr = reverse (big -> five); both uncapped/capped via zcap. prelay2.py l.7-11, 331.
- Sign convention is the physical one checked by the orient test (v gets +rr; brokensign control flips b's row).

## Why off
- Not a soundness failure. Code and tests are in place: orient test 0 mismatches / 100k diamonds, brokenkey 15,898 and brokensign 100,000 mismatches (FINDINGS.md l.775); s33z regress.sh controls.
- History: rr (s23, NULL then, t*=16/101 unchanged, FINDINGS l.774-783) and zh/zr/hatrr/l6r were all ON in the s33z stack (cmd_s33.sh l.13; s39o/run39s.sh l.12; LOG.md l.614-622: sol_s33 t<=0.125836 vs l3q-only 0.128958, families each <=0.055).
- They dropped out at the l3q-only / l3q+rpatN3 line (s39o/run39.sh l.12 FQ has no zh zr hatrr), carried to s44..s54 and s60 (env60.sh FCOM l.9 = "xon apexcls filt16 hat5 consall l3q lqcap=3 l3qV=7,8").
- Reason is a claims decision (E2 two-engine policy): Studio confirms by spec-only reproduction, and only l3q (RSST rule 9 restatement) + rpatN3 have a Studio spec/verdict (LOG.md l.639-645 "l3q only (RSST rule 9 restatement; claim must name the source)", l.715-717; "one engine since" for stacked). zh/zr/rr have no Studio verdict, so the E2 bound is quoted without them (stacked bound is 1-engine).
- Also: fy replaced zh in s35f/s40f (prelay2 asserts fy excludes zh/zr, l.11); fy-only was worse than l3q (LOG l.654).
- W6 report (/mnt/project-files/swarm/round6/W6-rule-grammar/REPORT.md l.112-137): the top-priced rules are exactly the OFF families. rr keys price +0.98328 total, z keys +0.779; certificate VALID only certifies enabled families. Re-solve (rr_lp_test.py): rr on t=0.01041, z on 0.01887, both -0.0485 (impossible, so charge exported to unweighted bigs). Full separated re-solve on the 250k pool NOT completed (l.137). Next step recommended there: Opus engine with hatrr/zh/q7 + separation.
- Not found anywhere: a note that they were unsound. s60 REPORT.md (l.1-60) mentions neither.

## Sound?
- Believed sound as own columns: conservation by construction (single key computed at both ends), controls pass. Not independently confirmed (no Studio/Lean statement); not proven in Lean as far as the notes show.
- Caveat for f2b: f2bglue.py l.15 asserts exclude XO/FY/V6/W19/PCAM/ref/Q7, NOT hatrr/zh, so the flags are accepted, but the jsepf leaf correction and f2b masks were never exercised with rr/z columns (selftests s60 val/selftest_*.log run with FUP only). Note ZH variable also = 'zh' or FY in s60 prelay2 (l.7).

## What it would take
1. Add `hatrr` (and `zh zr zcap=3`) to FUP/FCOM, copy of env60.sh; xpen 1e-3 caps as in s33z (prelay2 l.967-969, 1356).
2. Controls: orientR2 plain/brokenkey/brokensign (s33z/regress.sh template); lowerR2 on old cert reproduces/ prices rr,z; selftest of jsepf vs python rows with f2b rules ON and rr/z nonzero (s60 selftest_on pattern, but with rr/z values) to prove masks+rr/z coexist.
3. Warm K from sol_q60A97 (rr/z = 0 is in class), keeppen, then nosep lowerR2, upperR2 exhaustive d=7..17, binders.
4. For an E2 claim: Studio spec-only reproduction of rr/z (RELAY_SPEC 15r / s22 / stage 13 text) and, for Lean-side use, nothing needed beyond the discharge rule statement; until then report as one-engine and label rr/z as own rules.
5. Expected value: small (s33z gain ~0.003 on A67); W6 sanity check says top-priced columns are these.
