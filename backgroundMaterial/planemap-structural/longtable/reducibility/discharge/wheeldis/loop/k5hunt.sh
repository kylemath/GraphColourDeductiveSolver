#!/bin/bash
# EXPLORE round 4: randomised defect sampling with in-DFS receiver pruning (bin/defectr2), one centre per process,
# seeds 1.., wall cap.  usage: loop/k5hunt.sh CENTRE OUTDIR SECONDS [K=5] [NODECAP=300000] [TABLES]
cd "$(dirname $0)/.."; C=$1; O=$2; KK=${4:-5}; CAP=${5:-300000}; T=${6:-bin/defect_tables.txt}
end=$(( $(date +%s) + $3 )); s=1
while [ $(date +%s) -lt $end ]; do
  timeout $(( end - $(date +%s) + 1 )) nice -n 5 bin/defectr2 $T $C $KK 1 1000000 200 $((C*100000+s)) $CAP bin/rkeys7.txt >> $O/k${KK}r_c$C.txt 2>> $O/k${KK}r_c$C.err
  s=$((s+1))
done
echo "centre $C K $KK seeds $s leaves $(wc -l < $O/k${KK}r_c$C.txt)" >> $O/hunt.log
