#!/bin/zsh
cd "$(dirname $0)"
until [ -f out/census/DONE ]; do sleep 30; done
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do ./extra_worker.sh & done
wait
echo EXTRADONE > out/extra/DONE
