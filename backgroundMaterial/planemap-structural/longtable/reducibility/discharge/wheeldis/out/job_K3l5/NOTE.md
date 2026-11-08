# K3l5 family (Studio, 8 Nov): args_A97F_W13K3l5_x_studio.txt = args_A97F_W13K3l_x_studio.txt (f90ed3dc) + pat=/tmp/swarm-W17/pat/K3/pat_K3l5_D.out + cpat=/tmp/swarm-W17/pat/K3/pat_K3l5_C.cfast
- pat_K3l5_C.cfast: K5H01 (f10_..5665665._...655...., X={I0-I3}) + K5b L1, L2, U1, U2 (X={I0-I1}); pat_K3l5_D.out: K5b L3 (f8_755..556_66...5..). Built by us from our kc lines
  (out/job_K5/chk/h01, out/job_K3CHK9/<tag>), format as pat_K3l_C.cfast; name, r, m, X and window identical to Opus's pat_K5h01_C.cfast f82166d5 / pat_K5b_C.cfast e8bf75d8 / pat_K5b_D.out 0348c777 (comments differ).
- W17 harness count (ST-48): D 18137, C 699, RPAT 158 = EXPECT_PAT 18137,699,158.
- 240-key GK (cg_keys_r13w16_16fik.txt 3d996dbb): W17 GK path has no 64-key / per-payer limit (sep3r_gk.cpp SEP_GK: nk <= 4096, vector<GKKey>; the 64 cap is only SEP_KS's table); no code change. Pair counts (raw masks) = Opus's list; 171-key file still gives the ST-31 counts.
