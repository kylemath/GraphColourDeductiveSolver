# ST-108: W17 checker with HATBB keys (code_gk9), from in/HATBB_SPEC.md (a36ce8d2) only

No Opus / W6b code read. code_gk8, check8.sh, sep3r_gk8 unchanged (md5s equal ST-88's). Full diff: code_gk9.diff.

## Files changed (code_gk9 = cp -Rp code_gk8 + edits)
- hbfam.py (new): HAT(u->b)[ctx] parser (u, b nonempty subsets of {7,8,9}; 16 positions); receiver picture recv_pic (6-private pmask & ~extra6 at d <= 9, all at d >= 10; 7-private MASK/MASK8 & ~extra7 at d = 7, 8 when c, a <= 6); slot vectors per spec 3.1 / 3.2 (mirror by orientation o); OUT on SURE, IN on POSSIBLE; row = IN - OUT; edge_bound (per-edge separator bound); planted controls outposs / nomirror / inmirror.
- gkfam.py: load_keys(fn, skip_hat=True) skips HAT lines (without the flag a HAT line is still refused).
- st21_w17.py: HBKEYS from the GK file; receiver rows only (recv_spec, exact label, d = 7..26); HBREL[U][cell] table written to SEP_HB; hbrel_row in studio_val; DP d = 27..30 / Karp transitions add HBREL[U=9]; HBVEC / HBST hooks.
- hb_blocks.py (new): HBVEC (W6b vector comparison) and HBST (per-edge bound check, C++ 'e' vs Python rows d = 7..12, 18, 26, planted HATBB slots).
- gk_blocks.py: GKST_ONLY does not exit there when HAT keys are loaded (hb_blocks prints the verdict).
- sep3r_gk.cpp -> wd/bin/sep3r_gk9: SEP_HB loader; own HBREL recompute, refused if != Python's (exit 103); window term + HBREL at every link edge; anyStartR includes HB; leaf hbCorr = exact edge term - HBREL, exits 104 if an edge exceeds its bound; SEP_HBPLANT=inflip control.
- run17.sh, w17_upper.sh: defaults code_gk9 / sep3r_gk9; the stamp also covers hbfam.py and hb_blocks.py. New /tmp/swarm-W17/check9.sh = check8.sh pointing at code_gk9 / sep3r_gk9.

## Tail
I kept the tail rather than refusing it. HBREL[U][cell] is the max over (w_{i+2}, s_{i+1}) of the edge term, with every other position (privates included) read as the wildcard 31. A wildcard only adds possible IN matches and only removes sure OUT matches, so HBREL is >= the exact edge term for a receiver of any degree >= 9. The DP (d = 27..30) and Karp sum HBREL[U=9] over the transitions, so they bound the real HATBB row edge by edge. OUT at payer 9 stays in the bound. That is sound because a sure match with wildcards is a match in the real vertex (spec 4 allows dropping it but does not require that).

## Ambiguity
The lead's note says link-6 privates are the wildcard at d >= 9. The spec says the picture set at d <= 9 and all at d >= 10. The vectors decide between them: the spec reading gives 0 mismatches, the d >= 9 wildcard reading gives 5 (HB14, R9 rows; tests/t1_p6dmax8.log). code_gk9 uses the spec reading. Neither reading uses an apex mask.
