# eng_p8 validation chain (9 Nov): each step through T86.sh (one check at a time, memcg gate). Results in logs/t86_p8*.log and run.log.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
export E86OVR=$N/eng_p8 STACK=s77 ARGS=$N/args_A97_F_W13K3gB5l.txt
KEYS=$N/p8test/keys_p8test.txt T86CMD=p8reftest bash $N/T86.sh p8ref - 1 $XF N=1500
KEYS=$N/p8test/keys_p8test.txt T86CMD=gkwintest bash $N/T86.sh p8win - 1 $XF N=1500
KEYS=$N/p8test/keys_305p8.txt bash $N/T86.sh p8self $N/p8test/sol_GS14in01_p8amt.json 2 $XF f2bself=400
KEYS=$N/p8test/keys_305p8.txt bash $N/T86.sh p8selfCTL $N/p8test/sol_GS14in01_p8amt.json 2 $XF f2bself=400 gkoplant
echo "$(date -u +%H:%M:%SZ) [s86P8] eng_p8 test chain done" >> $N/run.log
