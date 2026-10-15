#!/bin/zsh
cd ${0:a:h}
for p in part00 part01; do nice -n 10 ../../studio15/cfast $p --search --limit 1 > $p.cfast 2>&1 & done
wait; echo DONE > a.DONE
