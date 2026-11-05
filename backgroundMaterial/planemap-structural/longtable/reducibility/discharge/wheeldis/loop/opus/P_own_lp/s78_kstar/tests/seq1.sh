# s78 acceptance tests, sequential, 1 thread, nice 15 (upper78.sh).  usage: nohup bash seq1.sh [steps] > ../logs/seq1.out 2>&1 &
# steps (default all, in this order): st3 st1 plant nowin u1a u1b u2a u2b u5
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar
C=$N/cand; cd $N
STEPS=${1:-"st3 st1 plant nowin u1a u1b u2a u2b u5"}
for st in $STEPS; do
  echo "$(date -u +%H:%M:%SZ) seq1 step $st start"
  case $st in
    st3)   KS=1 bash upper78.sh t3_eval_ks0125 $C/in10_ks0125.json 1 f2bself=3000 ksforce seed=11 ;;          # test 3: exactness, K* firing
    st1)   KS=0 bash upper78.sh t1_eval_off_in09 $C/sol_q75B_in09_full.json 1 f2bself=3000 seed=1 ;;            # test 1: self-test with the family off
    plant) KS=1 bash upper78.sh t3_eval_ksplant $C/in10_ks0125.json 1 f2bself=1000 ksforce seed=11 ksplant ;;   # control: must FAIL
    nowin) KS=1 bash upper78.sh t3_eval_ksnowin $C/in10_ks0125.json 1 f2bself=500 ksforce seed=11 ksnowin ;;    # control: jsepf must refuse (exit 81)
    u1a)   KS=0 bash upper78.sh t1_off_in09 $C/sol_q75B_in09_full.json 1 ;;                                     # test 1: in09 (nc ref FEASIBLE 0.033528013422)
    u1b)   KS=0 bash upper78.sh t1_off_in10 $C/sol_q75B_in10_full.json 1 ;;                                     # test 1: in10 (clamp log FEASIBLE 0.033088194780)
    u2a)   KS=1 bash upper78.sh t2_zero_in09 $C/sol_q75B_in09_full.json 1 ;;                                    # test 2: family on, amount 0
    u2b)   KS=1 bash upper78.sh t2_zero_in10 $C/in10_ks0.json 1 ;;
    u5)    KEEPWK=1 KS=1 bash upper78.sh t5_plant_in09 $C/in09_ks_plant.json 1 vK=200 vfile=$N/logs/t5_violated.txt ;;   # test 5: planted K* overpayment
  esac
  echo "$(date -u +%H:%M:%SZ) seq1 step $st done: $(tail -1 $N/run.log | cut -c1-220)"
done
