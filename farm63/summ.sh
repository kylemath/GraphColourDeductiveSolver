#!/bin/bash
# usage: summ.sh CHUNKNAME -> one line per window: name verdict (D / C X=.. / not) ; prints N done
d=/tmp/w/$1; echo "done $(ls $d/*.txt 2>/dev/null | wc -l)"
for f in $d/*.txt; do [ -f "$f" ] || continue; if grep -q 'D=true' $f; then echo "$(head -1 $f | cut -d' ' -f1-8) KILL_D"; elif grep -q 'C-REDUCIBLE' $f; then echo "$(grep -m1 'C-REDUCIBLE' $f | cut -c1-200) KILL_C"; fi; done
