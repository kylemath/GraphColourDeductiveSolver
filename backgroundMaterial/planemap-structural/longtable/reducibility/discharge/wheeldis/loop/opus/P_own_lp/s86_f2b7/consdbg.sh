# s86 consdbg driver.  usage: CONSL="7,7,8,9,7,9;..." [ARGS=..] [KEYS=..] bash consdbg.sh <tag> <sol>
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
export STACK=${STACK:-s77} ARGS=${ARGS:-$N/args_A97_F_W13K3j.txt} KEYS=${KEYS:-$B/s85_edge56/keys/cg_keys_r13w16.txt}
export FAM=full KS=0; unset EGK; . $N/env86.sh; N=$N86
TAG=$1; SOL=$2; WK=$SD/wr86c_$TAG; mkdir -p $WK $N/logs; cd $E86
ROWDBG=$N/consdbg.py nice -n 12 python3 pcheck_dbg.py upperR2 $F $X nomax sol=$SOL $A threads=1 work=$WK gkeys=$KEYS gkwin gkleaf c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt f2bself=1 > $N/logs/consdbg_$TAG.log 2>&1
rm -rf $WK
