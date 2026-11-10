# s86 (9 Nov 19:58Z): ST-89 point sol_k86MK1_in08__K3l5j_k260 (f3ca0aa8, 0.015523694 [E2] on K3l5j + 260) is not named sol_rep*, so
# macinject86p8 skips it: check it here on GS15's family + keys (K3gB5m + 329, eng_p8) and inject it as GS15's in-point if FEASIBLE.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; b=sol_k86MK1_in08__K3l5j_k260; tg=MI_k86MK1_in08_k86GS15
E86OVR=$N/eng_p8 STACK=s77 ARGS=$N/args_A97_F_W13K3gB5m.txt KEYS=$N/p1r/cg_keys_r13w16_16fikpqrs.txt bash $N/U86.sh $tg $N/cand/$b.json 2 c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt > /dev/null 2>&1
if grep "\[s86U-$tg\] STACK" $N/run.log | tail -1 | grep -q "UPPER-R2: FEASIBLE"; then
  if pgrep -f "tag=k86GS15 " > /dev/null; then cp $N/cand/$b.json $N/eng_p8/inject_k86GS15.json.tmp && mv $N/eng_p8/inject_k86GS15.json.tmp $N/eng_p8/inject_k86GS15.json; fi
  echo "$(date -u +%H:%M:%SZ) [s86MI-k86GS15] $b (0.015523694) FEASIBLE on K3gB5m + 329 keys -> inject_k86GS15.json" >> $N/run.log
else echo "$(date -u +%H:%M:%SZ) [s86MI-k86GS15] $b NOT feasible on K3gB5m + 329 keys; not injected" >> $N/run.log; fi
