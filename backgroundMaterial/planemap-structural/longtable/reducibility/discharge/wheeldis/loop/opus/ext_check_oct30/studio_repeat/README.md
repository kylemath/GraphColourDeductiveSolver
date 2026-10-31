# Inputs for a second-engine repeat of t* <= 0.041565 (Opus, 31 Oct 2026)

Data (use as data):
- gc/sol_c_repaired.json: the outside team's sol_unified_a100_tierA_full2ball_delta015_buffered.json with 8 g values of order -1e-16 clamped to 0 and t raised from 0.04156479218 to 0.041565 (md5 below).
- gc/kill_upgraded/tierA/: their kill_U7/8/9.npy, kill6_U7/8/9.npy, studio_l3qtab[V8]_+-1.json, full2ball_extra_rules.json; summary.json.
- args_a100_minus1.txt: their A100 pattern list with one exact-letter-9 line removed (it crashes the Studio loader).
Outside team's code (their code, not Opus's): outside_code/step2_cutting_plane.py (make_recv_spec_full2ball and what it calls), build_upgraded_kills.py, sep3r_l3q_fast.cpp (SEP_F2B), global_discharging_closure.py.
Opus's 2-ball implementation (f2b.py, sep3r_f2b.cpp, ...) is deliberately NOT here; it will be shared after the Studio verdict is written.
Opus container result, for comparison after the Studio verdict: senders/cons2/mrowL/bounds clean; receivers d=7..17 0 violated; DP 18..30 clean; Karp 0.633625577; UPPER FEASIBLE at 0.041565.
