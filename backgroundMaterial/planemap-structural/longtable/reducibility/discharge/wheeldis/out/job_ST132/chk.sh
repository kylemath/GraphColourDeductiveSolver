#!/bin/bash
# ST-132 K3CHK of W6b's 15 rotsub configs: D = kc -t 600 -C + dfast18; C = kc -t 600 -C -x X + cfast --fixed X
cd "$(dirname "$0")/../.." || exit 1
J=out/job_ST132
while IFS= read -r L; do
  n=${L%% *}; d=$J/chk/$n; mkdir -p $d; echo "$L" > $d/cfg.in
  v=$(awk -F'\t' -v n="$n" '$1==n{print $5"\t"$7}' $J/in/used15_res.tsv); V=${v%%	*}; X=${v#*	}
  if [ "$V" = C ]; then
    echo "$n {$X}" > $d/cfg.x
    nice -n 10 loop/kc/kc -t 600 -C -x $d/cfg.x $d/cfg.in > $d/kc.out 2>&1
    nice -n 10 ../studio15/cfast $d/cfg.in --fixed "$X" > $d/cfast.out 2>&1
    a=$(grep -c 'adm=yes leftover 0' $d/kc.out); b=$(grep -c 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' $d/cfast.out)
    [ "$a" -ge 1 ] && [ "$b" -ge 1 ] && r=PASS || r=FAIL
  else
    nice -n 10 loop/kc/kc -t 600 -C $d/cfg.in > $d/kc.out 2>&1
    nice -n 10 out/job52/dfast18 $d/cfg.in > $d/df18.out 2>&1
    a=$(grep -c 'D=true' $d/kc.out); b=$(grep -c 'D=true' $d/df18.out)
    [ "$a" -ge 1 ] && [ "$b" -ge 1 ] && r=PASS || r=FAIL
  fi
  printf '%s\t%s\t%s\tkc=%s\teng2=%s\t%s\n' "$n" "$V" "$X" "$a" "$b" "$r" >> $J/verdicts.tsv
done < $J/in/rotsub15_kc.txt
echo DONE >> $J/verdicts.tsv
