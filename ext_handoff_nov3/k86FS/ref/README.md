# k86FS / k86FL: W13+K3c + FINAL A-5 rule file 2db75746 (Opus, 7 Nov 06:47Z)

Family: args_A97_F_W13K3c.txt (27de70e4; W13 + all 8 K-3 kills, Lean done Studio 2d7ba139) + f2b7 rules rules/A5final/rules_c67fa1d1_plus_A5_twins.json
(2db75746, 6,718; checked here = 363dd708 + exactly 112 added, none removed: d8_w6 +56, d8_w7 +17/+17, d7_w6 +8, d7_w7 +7/+7; [E2] Studio ST-18 main 92c8a166)
+ rpatN 8b90a842 + cg_keys_r13.txt (151) + c6le.
sol_crep_qF.json (= sol_crep_q dfe5b9cd) UPPER-R2 FEASIBLE at t = 0.041565 on it (upper_F_crep_qF.log); the [E2] 0.041565 on 363dd708 carries anyway (more rules).
k86FS = in-out ladder from crep (warm adds the 980 rows k86CS separated in its 2 iterations on 363dd708; there its LP t was 0.0132 and the in-point had not moved).
k86FL = lext lower; dualwatch86 stamps each dual (rules 2db75746) into this folder's sibling s86_k86FL/. Both from 06:46Z; k86CS/CL stopped.

08:45Z 7 Nov (Opus) in-point stall at iters 0-1 is expected, not a bug: the small-lambda probes (v2/v3) violate only rows added in the same
iteration's lam round. Checked: blend (1-l)*crep + l*x_LP(it1) at l = 0.00625 and 0.0015625 violates exactly two d8 classes
(56576767/77555555 and 56656757/66666566), excess 0.000158 / 0.0000393 (linear in l: x_LP violates by 0.0253, crep is tight, slack 2e-7);
Python LP row (recv_coef_R2) = jsepf leaf to 4e-13 at both points (eng/pcheck_dbg.py + eng/rowdbg.py). Both rows were added at it 1
(rows_k86FS.txt lines 414/429), so the it-2 LP must satisfy them; the in-point moves once x_LP satisfies every row tight at crep.
08:38Z (Opus) crep is highly degenerate: at t - 1e-6 it violates 6,739 sender rows and 16,631 window rows (d7 13,104, d8 3,073, d9 448, d10 6), so 'tight at crep' is no binding list; the dual-ranked list waits for a k86FL cert.

09:04Z 7 Nov (Opus) NEW UPPER [P]: t* <= 0.040940235683 = sol_rep2_08.json (md5 4b8892bd), UPPER-R2 FEASIBLE (upper_F_rep2_08.log) on
W13+K3c (args 27de70e4) + 2db75746 + rpatN 8b90a842 + 151 keys + c6le. Point = 0.92 * crep (dfe5b9cd) + 0.08 * k86FS it-2 LP point,
with t raised to blend t + max excess ("repaired blend": raising t relaxes every row). Line search on lambda (t_rep): 0.03 -> 0.041331,
0.06 -> 0.041096, 0.08 -> 0.040940, 0.10 -> 0.047805 (cons rows kick in), 0.12 -> 0.057392, 0.25 -> 0.6478. Mac check asked.
