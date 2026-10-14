#!/bin/zsh
# Studio, 13 Oct 2026: build every RSST agreement file (exploratory). DCheckThms11 first, then the 16 ring 12-14
# files with 6 parallel lake processes (nice 10), ring 14 first.
cd "$(dirname $0)/.."
[[ -f studio-run/timings.txt ]] && grep -q "DCheckThms11 rc=0" studio-run/timings.txt || ./studio-run/one.sh DCheckThms11
grep -v ALLDONE studio-run/timings.txt > studio-run/t.tmp; mv studio-run/t.tmp studio-run/timings.txt
print -l DCheckR14{a..j} DCheckR13{a..d} DCheckR12{a,b} | xargs -P 6 -n 1 ./studio-run/one.sh
echo ALLDONE >> studio-run/timings.txt
