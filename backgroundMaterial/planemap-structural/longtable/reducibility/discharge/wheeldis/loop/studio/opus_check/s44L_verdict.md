# s44L (A78 fb6 nosep lower certs; RELAY_SPEC_s44 through 44.8 at 4045b217): Studio spec-only check

**Verdict.**
- **(1) Unrepaired cert.** Studio's engine reproduces Opus's 87 noise columns exactly: 45 g and 42 h, worst
  -5.62e-13, total -5.76e-12. It is INVALID as it stands, as Opus says.
- **Studio also finds 18 fb columns with rc < 0** (worst -2.4e-13, total -1.0e-12). These do NOT invalidate the cert,
  because 44.8 prices fb at its cap (3), and they stay within the noise level.
- **(2) Repaired cert: VALID in Studio's exact check.** It has 0 negative uncapped columns, and
  **D = 0.093306161279073** exactly (denominator 137 digits), within 1e-11 of the claimed 0.093306161279.
- **No kill line is met under the 44.8 rule (fb capped at 3).** If fb were treated as uncapped, both certs would fail on
  the fb columns, so the conclusion rests on the cap.

## Independence statement
I built this check from RELAY_SPEC_s44.md 44.1-44.5 (the fb build of s44/fb_keycheck.md) and the new 44.8 (4045b217),
on top of the s42a setup (RELAY_SPEC_s21 / s39o: l3q, rpatN3, kill tables, the 128 ring-merge entries held out).
44.8 changes no fb rule. It does add one data rule: a weight written as the string "p/q" is exact. I added that to
out/job31/st21_check.py (string weights are taken exactly, and float weights are rationalised as before). I also added
two opt-in options: WEXACT=1, which takes floats as exact binary values, and LOWER_TOL, which compares an exact D with a
decimal claim.

Opus files opened: RELAY_SPEC_s44.md (spec diff of 4045b217), run_A78/cert_q44fbA78L.json (03181fd2),
run_A78/cert_q44fbA78L_rep.json and run_A78/sol_q44fbA78.json, the last used only to load. I did not open prelay2.py,
port_repair.py, pcheck.py, eng/, cmd scripts, rows files or logs (lower.log, lower_rep.log); I saw their names via
git show --stat only. Team B material: none.

## Inputs
- **Certs:** cert_q44fbA78L.json md5 7bb0d135 (1,118 rows: 70 senderR2, 884 cons2, 100 mrowR2, 16 mrowL, 48 receiverR2);
  cert_q44fbA78L_rep.json md5 395bcb63 (the same 1,118 labels, exact "p/q" weights); sol_q44fbA78.json md5 775c91aa.
- **Registry and tables:** the same as s42a (s42a_verdict.md, 9bc9b2b2): A78 b6dc7610 with the 128 held out
  (argsA78_local_rpat_held128.txt), Studio's kill tables and l3q masks (= reg_A78), and rpatN3 at 2,287 patterns.
- **fb settings:** FB=1, FBDIR=6 (fb6 only: X = 6, U >= 7), FBCAP=3. The payer is -1 in u's receiverR2 row; the payee is
  +1 in the 6's cons2 row.

## (1) Unrepaired cert (weights rationalised per weight, limit_denominator 1e7; s44L/cert_q44fbA78L_studio.log)
- tco = 1.
- **Negative uncapped columns:** **87, of which 45 are g and 42 are h**; worst -5.62e-13, total -5.76e-12. This is the
  same count and split as Opus's 44.8. There is no negative y, r, M or lQ column. The verdict is INVALID, as Opus says.
- **fb columns with rc < 0: 18** (U X T- T+; rc):

  | key | rc | key | rc | key | rc |
  |---|---|---|---|---|---|
  | 96 5655 7550 | -2.4e-13 | 76 5555 9550 | -2.3e-13 | 96 5555 6770 | -1.8e-13 |
  | 96 5655 7570 | -6.7e-14 | 76 5655 9550 | -5.9e-14 | 76 5955 9550 | -5.1e-14 |
  | 96 5755 6570 | -3.8e-14 | 76 5575 5755 | -3.6e-14 | 96 5555 5755 | -2.5e-14 |
  | 96 5755 7550 | -2.3e-14 | 96 5755 9570 | -2.1e-14 | 76 5955 6570 | -1.6e-14 |
  | 96 5555 6750 | -1.5e-14 | 76 5755 6570 | -1.4e-14 | 96 5655 9550 | -1.1e-14 |
  | 76 5955 6550 | -7.9e-15 | 76 5955 7550 | -7.6e-15 | 96 5755 9550 | -2.4e-16 |

  - Under 44.8 these are priced at cap 3, which costs 3.1e-12: D = 0.093306161289246.
  - Without the fb charge, D would be 0.093306161292338, which is the LP t*.
  - Opus's "bound before the noise" is 0.093306161289. That equals Studio's D *with* the fb cap charge, so Opus's engine
    seems to see the same negative fb columns and price them at the cap. 44.8's "no fb column is negative" would then
    mean "none that the check counts as uncapped". **Opus should confirm this.**
- **Control, WEXACT=1** (floats taken as exact binary values; ..._wexact_studio.log): 141 negative uncapped columns
  (g 80, h 21, M 17, y 10, r 10, lQ 3), worst -1.9e-14, plus 27 fb columns at worst -6.4e-15; tco = 1 - 4.2e-14.
  This matches 44.8's remark that exact floats leave residuals of about 1e-14 spread over g, h, r, y and M.

## (2) Repaired cert (exact string weights; s44L/cert_q44fbA78L_rep_studio.log)
- All labels are admissible, signs are enforced, and every row is in canonical orientation. tco = 1.
- **Negative uncapped columns: 0.**
- **fb columns with rc < 0: 25**, worst -4.8e-13 (96 5555 7550), total -4.4e-12. They are priced at cap 3, which costs
  1.33e-11.
- **D = 0.093306161279073** (exact, denominator 137 digits, md5 of the fraction string ae628aba). That is within 1e-11
  of the claimed 0.093306161279. **VALID t >= D.**
- Without the fb charge, D would be 0.093306161292338 (= t*). The repair pins g and h but leaves fb to the cap, and fb
  goes from 18 to 25 negative columns, so about 1.3e-11 of the bound is lost to fb. Pinning fb as well would recover it.
  This is a remark only, not a failure.
- **The 0.0933 nosep lower bound is below the s42a upper bound of 0.109439356774, as 44.8 says.**
