# s86 memory gate for one lowerR2: pause repladder + tightwatch, wait until no upperR2 runs and >= 5.5 GB is available,
# resume the (SIGSTOPped) watchL86p so it starts lowerR2 on the new phase-1 cert, then resume the others once that lowerR2 has a verdict.
# usage: bash memgate_lx.sh <watch pid> <lx log> <pids to pause...>
Z=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
W=$1; L=$2; shift 2; P="$*"
kill -STOP $P 2>/dev/null
echo "$(date -u +%H:%M:%SZ) [s86G] memgate: paused $P; waiting for upperR2 runs to end and 5.5 GB free before lowerR2 ($L)" >> $Z/run.log
while pgrep -f "pcheck.py upperR2" > /dev/null || [ $(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo) -lt 5500 ]; do sleep 30; done
kill -CONT $W
echo "$(date -u +%H:%M:%SZ) [s86G] memgate: resumed watch $W ($(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo) MB free)" >> $Z/run.log
until grep -q "LOWER-R2" $L 2>/dev/null || ! kill -0 $W 2>/dev/null; do sleep 60; done
sleep 30; kill -CONT $P 2>/dev/null
echo "$(date -u +%H:%M:%SZ) [s86G] memgate: lowerR2 done, resumed $P" >> $Z/run.log
