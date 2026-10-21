# s54 scan.sh "tag pm" ... : nosep parametric LPs on the warm pool (lower bounds on the pool), sequential; no upper check
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s54
for tp in "$@"; do set -- $tp; NOUPPER=1 bash run1.sh $1 $2 nosep; done
