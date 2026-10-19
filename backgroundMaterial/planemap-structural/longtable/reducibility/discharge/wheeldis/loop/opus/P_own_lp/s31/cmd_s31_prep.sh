# s31 prep: Studio head 3cfd7f18 (2,397 D / 1,010 C, ring-merge 3 held). ex62 = ex60 + git archive 3cfd7f18 W/loop.
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
Q=$P/s31; cd $Q
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
EX=$S/ex62; TD=$Q/k3x_D_3cfd7f18.out; TC=$Q/k3x_C_3cfd7f18.cfast
date -u +%H:%M:%SZ > kill_start.txt
{ for U in 7 8 9; do echo "cd $Q/f && python3 s16_filter.py $EX $TD $TC kill/kill6_U$U.json wj=6 U=$U > kill/kill6_U$U.log 2>&1"; done
  echo "cd $Q && python3 dcount.py argsA62.txt $M > dcount.txt 2>&1"; } | xargs -P2 -I{} sh -c '{}'
(cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
md5sum f/kill/*.npy $P/s25/f/kill/*.npy > kill_md5.txt
date -u +%H:%M:%SZ > kill_end.txt
echo DONE > prep_done.txt
