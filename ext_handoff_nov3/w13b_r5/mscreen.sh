#!/bin/bash
# W13b round-5 Mac screener, bash fallback for mscreen.py (use only if python3 is missing). Same pipeline, same 12-column
# W13 res output; no per-call timeout (macOS has no `timeout` by default). bash 3.2 compatible.
# usage:  KC=/path/kc DF18=/path/dfast18 CF=/path/cfast [DF=/path/dfast] bash mscreen.sh BATCH.tsv OUT.tsv
B=$1; OUT=$2; TMP=$OUT.one; KC=${KC:-kc}; DF18=${DF18:-dfast18}; CF=${CF:-cfast}; DF=${DF:-}
touch "$OUT"; TAB=$(printf '\t'); n=0
echo "todo $(wc -l < "$B" | tr -d ' ') (before resume skip) batch $(basename "$B")"
while IFS="$TAB" read -r code ring m n5 fam name kl; do
  [ -z "$code" ] && continue
  if grep -q "^$code$TAB" "$OUT"; then continue; fi
  printf '%s\n' "$kl" > "$TMP"; t0=$(date +%s)
  o=$("$KC" -C "$TMP" </dev/null 2>/dev/null)
  lo=$(printf '%s\n' "$o" | sed -n 's/.*leftover \([0-9][0-9]*\).*/\1/p' | head -1)
  X=$(printf '%s\n' "$o" | sed -n 's/[^{]*X={\([^}]*\)}.*/\1/p' | head -1)
  rr=$(printf '%s\n' "$o" | sed -n 's/.*classes=\([0-9][0-9]*\) ext=[0-9][0-9]* reached=\([0-9][0-9]*\).*/\2\/\1/p' | head -1)
  conf=""
  if printf '%s' "$o" | grep -q 'D=true'; then
    v=D; a=na
    if [ -n "$DF" ]; then if [ "$ring" -le 16 ]; then a=$("$DF" "$TMP" </dev/null | grep -q 'D=true' && echo D || echo noD); else a=skip; fi; fi
    b=$("$DF18" "$TMP" </dev/null | grep -q 'D=true' && echo D || echo noD); conf="dfast:$a dfast18:$b"
  elif printf '%s' "$o" | grep -q 'C-REDUCIBLE'; then
    v=C; c2=$("$CF" "$TMP" --fixed "$X" </dev/null | grep -q 'C-REDUCIBLE' && echo C-REDUCIBLE || echo noC); conf="cfast:$c2"
  elif [ -z "$o" ]; then v=ERROR
  else v=N; fi
  n=$((n+1)); dt=$(( $(date +%s) - t0 ))
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$code" "$ring" "$m" "$name" "$v" "$lo" "$X" "$rr" "$dt" "$fam" "$conf" "$kl" >> "$OUT"
  [ "$v" != N ] && echo "HIT $v $ring $name $fam $X $conf"
done < "$B"
echo "COMPLETE $n"
