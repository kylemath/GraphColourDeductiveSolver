# s78 acceptance tests for the generic EDGE keys (eng/edgekeys_r4.txt: A1 C1 E1), patched stack (s77), FAM=full, at the coordinator's
# best point s77 cand/sol_b77F_in02.json (nc FEASIBLE 0.029906108105).  1 thread, nice 15.  usage: nohup bash seqE.sh [steps] > ../logs/seqE.out 2>&1 &
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar; B=$(dirname $N)
C=$N/cand; IN02=$B/s77_k6patch/cand/sol_b77F_in02.json; EK=$N/eng/edgekeys_r4.txt; cd $N
STEPS=${1:-"e1off e2zero e3self e3plant e5"}
for st in $STEPS; do
  echo "$(date -u +%H:%M:%SZ) seqE step $st start"
  case $st in
    e1off)   STACK=s77 KS=0 bash upper78.sh e1_off_in02 $IN02 1 ;;                                                      # test 1: family off (new binary)
    e2zero)  STACK=s77 KS=1 EGK=$EK bash upper78.sh e2_zero_in02 $C/in02_eg0.json 1 ;;                                 # test 2: K* + EDGE on, amounts 0
    e3self)  STACK=s77 KS=1 EGK=$EK bash upper78.sh e3_eval_mix $C/in02_eg_mix.json 1 f2bself=3000 egforce seed=21 ;;   # test 3: exactness
    e3plant) STACK=s77 KS=1 EGK=$EK bash upper78.sh e3_eval_egplant $C/in02_eg_mix.json 1 f2bself=1000 egforce seed=21 egplant ;;   # control: must FAIL
    e5)      KEEPWK=1 STACK=s77 KS=1 EGK=$EK bash upper78.sh e5_plantA1_in02 $C/in02_eg_plantA1.json 1 vK=200 vfile=$N/logs/e5_violated.txt ;;   # test 5
  esac
  echo "$(date -u +%H:%M:%SZ) seqE step $st done: $(tail -1 $N/run.log | grep -o 'UPPER-R2.*' | cut -c1-120)"
done
