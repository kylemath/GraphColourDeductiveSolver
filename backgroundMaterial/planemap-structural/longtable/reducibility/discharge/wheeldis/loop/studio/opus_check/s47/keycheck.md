# s47 (l3qV V = 8, RELAY_SPEC_s47.md at e1fadfcf, md5 84475374; on s45 0f510676): Studio build and key check

**Status: built. Every control reproduces the spec's §47.6 results, apart from report-count conventions (noted below).** No spec
ambiguity blocks a run.

## Independence statement
I built this from RELAY_SPEC_s47.md and RELAY_SPEC_s45.md alone, on top of my §21 / s39o / s44 checker. Opus files opened: those two
specs, plus data only:
- s47/tabV8_A78/tabV8_{1,-1}.json and s47/tabV8_A84/ (the diff only, after my own tables were built);
- the s42a A78 sol and cert;
- reg_A84 at 62bae93a.

I did not open s45/l3qtabV.py, port_l3qV.py, pricer45.py, s47/port_s47.py, eng/, jsep7.cpp, test_jsep7.py, cmd scripts or logs.
Team B material: none.

## Implementation
- **Tables:** out/job31/l3q_masks.py with L3QV=8 (§45.3: link length 8, payee centre degree exactly 8, w4 = the antipode; reading A, strict).
- **Checker:** out/job31/st21_check.py, flag L3Q8=1 with L3TAB8.
  - **Payer:** −lq[(8, c, a, a2)] at every d = 7 link 8, on both sides, when c, a ≤ 6.
  - **Payee:** +lQ[(8, c, a, m)] at every d = 8 link 7, on both sides, with m = T_8, indices mod 8.
  - **Qeff8, UB8:** as §47.3(i).
  - **Lower:** V = 8 mrowL labels accepted. lq is priced at lqcap. The s45.6 raw and bundle rc are reported.
  - **R8:** the V = 7 payer table is filled from 3-tuple keys only.
  - **§47.3(v):** a 4-tuple key with the family off, or malformed, is refused with the spec's message.
- **Separator:** bin/sep3r_l3q, opt-in SEP_L3Q8.
  - **d = 8:** the relaxed window term UB8(e, r) + UB8(b, q) at a link 7, and the exact Qeff8 payee terms at the leaf.
  - **d = 7:** the payer −q8 at a link 8, at the leaf only (R3).
  - Then the prune test (R4). Nothing changes without the flag.
- **Broken-build switches (controls only):** BROKEN8 = payersign (rows and separator mis-signed), apex (payee apex / o swapped),
  sep_payee0 / sep_payersign (separator only).

## Controls (logs in loop/studio/opus_check/s47/)
| control | Studio | spec §47.6 |
|---|---|---|
| V = 8 tables, A78 | 50 of 30 per side; forbidden set 4,412; equal to Opus's tabV8_A78 entry by entry (0 mismatches) | 50 of 30 per side; 4412; b0115b14 / 38c23474 |
| V = 8 tables, A84 | equal to Opus's tabV8_A84 entry by entry (0 mismatches) | b0115b14 / 38c23474 |
| (d') lowerR2 on cert_q42aA78L, l3qV = 7,8, full table | **VALID t ≥ −244/421**; negative lq (8,6,5,5) −24/421, (8,6,5,6) −24/421, (8,6,6,5) −48/421; no negative lQ; **bundle rc (8,6,6,5) −12/421** | VALID −244/421 = 44/421 − 3·(24+24+48)/421; bundle −12/421 |
| broken payer sign (lower) | caught: D = 44/421 ≠ −244/421; lq8 rc flip sign | — |
| broken apex (lower) | D unchanged (−244/421); lQ8 column set changes (4 → 3 keys). The lower check alone does not separate it; the separator test below does | — |
| separator self-test, random V = 8 q / Q (L8RAND) | leaf vs spec rows max 2.26e−10 (3,020 rows, all with l3q terms); relaxed vs spec on 3,620 arrangements: 0 below exact; d = 8 exhaustive: 5,000 rows re-checked exactly, 0 deviations | jsep7: 2,400 rows, 0 mismatches |
| broken separator (no exact V = 8 payee) | caught: d = 8 leaf differs from the spec row by 0.0866 | broken: 1,398 mismatches |
| (c) sol + 0.003, q(8,6,6,5) = 0.002, full table | senders 0, conservation 0, **d = 7: 0 violated**, d = 8: violated (40 oriented arrangements; load 2.113439, excess 0.001), d = 9..17 0, DP clean, Karp λ 0.573063 → INFEASIBLE | d = 7: 0, d = 8: 6 → INFEASIBLE |
| (c) brokensign (rows and separator) | **d = 7: 616 violated**, all on link 8665566 (rotations), excess 0.001 = 2·0.002 − 0.003; d = 8 as correct → INFEASIBLE | d = 7: 20 (report cap), all on 8665566, excess 0.001; d = 8: 6 |
| (c3) q(8,6,6,5) = 1, t + 0.02 | d = 8: ≥ 5,000 violated (cap); d = 7 0 | d = 8: 20 (cap) |

**Count conventions:** Studio counts every violating oriented arrangement up to the report cap of 5,000 (the d = 8 rows shown are
rotations of each other). Opus reports mode-0 rows with a report cap of 20. The binding row family, the link, the excess and every
verdict agree.
