# s86: tighten every new FEASIBLE upper point of a GS run (repair-ladder NEW IN-POINT lines and watch86 in-point verdicts) on K3j, one at a time.
# usage: nohup bash tightwatch.sh k86GS3 > logs/tightwatch_k86GS3.out 2>&1 &
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; TAG=$1; cd $N
tail -n0 -F run.log | while read -r line; do
  sol=""
  case "$line" in
    *"[s86REP-$TAG] NEW IN-POINT "*) sol=$(echo "$line" | sed -n 's/.*NEW IN-POINT \(sol_[^ ]*\.json\).*/\1/p') ;;
    *"[s86U-sol_${TAG}_in"*"UPPER-R2: FEASIBLE"*) sol=$(echo "$line" | sed -n "s/.*\[s86U-\(sol_${TAG}_in[0-9]*\)\].*/\1.json/p") ;;
  esac
  [ -z "$sol" ] && continue
  for i in $(seq 1 30); do [ -s cand/$sol ] && break; sleep 5; done
  [ -s cand/$sol ] || { echo "$(date -u +%H:%M:%SZ) tightwatch: cand/$sol missing" ; continue; }
  until [ $(free -m | awk 'NR==2{print $7}') -ge 4000 ]; do sleep 20; done
  echo "$(date -u +%H:%M:%SZ) tightwatch: tightening $sol"
  bash $N/tighten.sh $N/cand/$sol 0.003
done
