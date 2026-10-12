#!/bin/sh
# leave-one-lineage-out test of a shared anchored rule (r=2, partA) on the sigma-type 10-cycles
cd "$(dirname "$0")"
PY="nice -n 10 ../TrackQ/.venv/bin/python"
T="data/n1_7121_17_230_K_L_L_data.json@0 data/n1_7121_138_352_data.json@0 data/n1_7511_15_3104_data.json@4 data/n1_7511_15_2656_data.json@4 data/n1_7121_119_1473_data.json@2 data2/n1_7121_127_2225_data.json@8"
$PY tr_rule.py 2 partA $T --out out/rule_train6_r2.json | grep -E "RESULT|EXACT"
$PY tr_apply.py out/rule_train6_r2.json $(cat data2/sigma_list.txt) | cut -c1-90
for X in 7121_17 7121_138 7511_15 7121_119 7121_127; do
  TT=$(for f in $T; do echo $f; done | grep -v "n1_${X}_" | tr '\n' ' ')
  echo "== leave out $X"
  $PY tr_rule.py 2 partA $TT --out out/rule_lolo_$X.json | grep RESULT | cut -c1-80
  $PY tr_apply.py out/rule_lolo_$X.json $(tr ' ' '\n' < data2/sigma_list.txt | grep "n1_${X}_") | cut -c1-90
done
