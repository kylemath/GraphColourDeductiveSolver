# s86 offc2 builder.  usage: [ARGS=..] bash offc2.sh <tag> [extra opts, e.g. offctest=CERT]   -> offc/offc_<tag>.txt, logs/offc2_<tag>.log
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
export STACK=${STACK:-s77} ARGS=${ARGS:-$N/args_A97_F_W13K3g.txt} KEYS=${KEYS:-$B/s85_edge56/keys/cg_keys_r13w16.txt}
export FAM=full KS=0; unset EGK; . $N/env86.sh; N=$N86
TAG=$1; shift; WK=$SD/wr86o_$TAG; mkdir -p $WK $N/logs $N/offc; cd $E86
ROWDBG=$N/offc2.py nice -n 10 python3 pcheck_dbg.py upperR2 $F $X $A threads=1 work=$WK gkeys=$KEYS gkwin gkleaf c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt offcout=$N/offc/offc_$TAG.txt "$@" > $N/logs/offc2_$TAG.log 2>&1
rm -rf $WK
