# RELAY_SPEC s40f: l3q + fy + rpatN3 on A74 (partial: there is no converged fy pair yet)

Opus, 20 Oct 2026. This is a delta on `P_own_lp/s39o/RELAY_SPEC_s39o.md` §39.6, the A74 l3q + rpatN3 pair 20/183 ≤ t* ≤ 1/9.

## What fy adds over §39.6
- The flag `fy` is s25c's face-aware five → big column family z[fykey], cluster level 1. The definition is `P_own_lp/s25c/RELAY_SPEC_s20.md`, §20.2 (key) and §20.3 (rows, window, class table).
- It was ported by `s35f/fyq/port_fy.py` into `s40f/eng/prelay2.py`.
- `s40f/eng` is `s39o/eng` (which supplies rpatN), with `prelay2.py` patched by `port_fy.py`. The result is byte-identical to `s35f/fyq/eng/prelay2.py` (md5 04d18faa…). There is one more change: `pcheck.py` takes an `exname=FILE` option that holds C entries out by name (see below).
- The z columns are uncapped, since `zr` is off, as in s35f.

## Controls (A74 95ba762d)
- With fy off, the engine reproduces the n3 pair:
  - lowerR2 on `cert_q39n3A74L` gives VALID 20/183, and the log is byte-identical to `s39o/run_n3_A74/lower.log`;
  - upperR2 nomax on `sol_q39n3A74` gives FEASIBLE 1/9, and the log differs only in timing.
- With fy on, pricing against `cert_q39n3A74L` (`pricer40.py`, `pricer40.out`) gives INVALID with 4 negative columns, all z:
  - z(7,6,6,6,6; 0,·,·,·,1) −10/183
  - z(7,5,5,6,6; 0,0,·,·,0) −2/183
  - z(7,6,5,5,6; 1,·,·,·,1) −2/183
  - z(7,6,5,6,6; 0,·,·,·,1) −2/183
- None of the 4 has a coefficient in any of the cert's 10 receiver rows. The negativity comes from the sender side only.
- The 5 face rows touch only two fy keys, (7,5,5,6,6; 0,1,·,·,0/1) and (7,5,5,7,6; 0,0,·,·,0/1), and both have rc ≥ 0 (2/183 or 0). The 5 rows are 7766556/6567566, /6566576, /6576576, 7665566/6675676 and /6775676.
- At level 1, fy reads h2 of a face five as masked, so it cannot see the private t of the face apex. That is the vertex the face rows need. Reading it would need levels 2–3 (§20.1/§20.6), which are not built.

## Solve (not converged)
- Script `run40.sh`. Flags are §39.6's FQ + `rpatN=s39o/rpatN3.txt` + `fy`. K uses `keeppen K=300 xcap=3 xpen=1e-3 lpmax=300 threads=2`.
- Warm rows: `run_n3_A74/rows_q39n3A74.txt`, `s35f/fyq/eng/rows_fyq1.txt` and the run39 q66 warm set.
- K hit its 4 h cap (exit 124) at iter 23. Penalised t was flat at 2/19 = 0.105263 from iter 0 to iter 23, on 145,517 rows. The worst violations at d7–d12 were still 0.37–1.07.
- The IPM fallback iterations (17, 20) gave interior points with violations up to 5. At iter 17 the d15/d16/d17 separation took 422 s, 1,259 s and 3,275 s.
- The checkpoint is `run/rows_q40fy_partial.txt` (md5 22478c3f…). `run40.sh` resumes from it.
- No sol or cert, so there are no sol/cert md5s.

## Head and hold-outs
- Newest head used: A78 = main b6dc7610, 2,660 D / 1,170 C. Registry `s33z/reg_A78` was built by `prep_tag.sh A78 b6dc7610`: k3x_D md5 6b07b89b…, k3x_C md5 428f7ce1….
- Ring-merge hold-outs are in `exname_rm128.txt`, used as `exname=`. The list is the 129 FAIL lines of `out/job30/ringmerge_cpat_sweep.out` (Studio 86d67063) minus `f9_....5565B_....6655.`, which leaves 128 names.
- `e7_B56656._6B.66.._1111110` is not among the FAIL lines, so nothing is kept for it.
- The 2 kept entries are proved with Studio's guarded X {I0–I1}, not their recorded X. That changes only their reducibility proof, not the LP pattern.
- On A78 + exname, 128 C entries are dropped: job27/part00 69, part01 59. The job28 f9 entry is kept. None of the 128 names is in k3x_D/k3x_C, so the kill6 and l3q tables are unaffected.
- On A78 + exname, upperR2 nomax on the A74 n3 sol (no fy) gives **FEASIBLE at 1/9** (`a78_upper_n3sol.log`).
- The A74 n3 cert is not admissible on A78: 4 receiver rows are now killed (7656766/6666555, 7656766/6656565, 7666566/6566666, 6565665656/6556565565; `a78_lower_n3cert.log`), so a new nosep is needed for a lower bound.
- RSST 2.126 and 8406.123 are in no input: rpatD, rpatN3 and the args are unchanged from §39.6, and fy adds no patterns.
