# fb (RELAY_SPEC s44, def18bc8 / aaf71a79): Studio build and key check

Built from RELAY_SPEC_s44.md 44.1-44.5 alone (no Opus code: port_fb.py, pricer44.py, phys44.py, sepfb44chk.py, eng/ not
opened; file names seen via git ls-tree only). fb is Studio's own implementation; nothing about it is near Team B material.

## Implementation
- out/job31/st21_check.py, flag FB=1 (FBDIR = 6 / 7 / 67, FBCAP optional): key sigma = (U, X, min(T+, T-), max(T+, T-)),
  face side (c, b, e) = (5, 5, 5); payer -1 in u's receiverR2 at w_j >= 6 with T+ = (w_{j+1}, s_j, w_{j+2}, e+),
  T- = (w_{j-1}, s_{j-1}, w_{j-2}, e-); fb7 payee +1 in X's receiverR2 at L_k >= 7 with T+ = (L_{k+1}, L_{k+2}, t_k, ..);
  fb6 payee +1 in cons2 (L, s) at L_k >= 7; cons2 checked over all 1,424 x 5^6 exact apex words when FB; lower: an fb
  column with rc < 0 invalidates the cert unless FBCAP (then priced at the cap).
- bin/sep3r_l3q, opt-in SEP_FB6: exact window term (payer at c >= 6, payee at c >= 7 when U >= 7) over the 9-slot window
  (a, b, c, e, f, p, q, r, s) as in 44.3, with the relaxed max over the unread (a, f, p, s) in the search bound and the
  exact term swapped in at the leaf (as SEP_RTAB / SEP_L3Q); the d >= 18 DP / Karp tail adds the relaxed term at U = 9.

## Key check against 44.7 (data)
Pricing of every fb column on cert_q39n3A74L with Studio's own row coefficients (s44/fbprice_{6,7,67}.log):
- **fbdir=6: the same 8 negative columns as 44.7, every rc equal:** (7,6,5655,7670) -18/183 [= -6/61]; (7,6,5755,6670)
  -10/183; (7,6,5755,7670) -10/183; (7,6,5755,6770) -1/183; (9,6,5655,7550) -8/183; (8,6,5655,7550) -4/183;
  (9,6,5655,9550) -2/183; (7,6,5555,9670) -2/183.
- **fbdir=7: no negative column** (VALID 20/183), as 44.7. **fbdir=67 = fbdir=6**, as 44.7.
- 0 mismatches.

## Self-test (s44/fb_selftest.log)
22,300 random fb values on every possible key: sep3r_l3q's exact leaf (with SEP_FB6) matches the spec rows on the 2,000
heaviest d = 7 rows (1,916 with l3q terms) to 4.9e-10 and at d = 8 to 2.9e-10 (the run was cut by a session teardown before
the relaxed-vs-exact stage; that stage runs again in the first real fb check).

## Spec reading notes
- e in T is 0 (masked) unless the side's first entry c is 5; a face side needs (c, b, e) = (5, 5, 5), so e = 5 there.
- U in the key is min(deg u, 9) at the payer and the payee reads it as L_k (a letter), the same value.
