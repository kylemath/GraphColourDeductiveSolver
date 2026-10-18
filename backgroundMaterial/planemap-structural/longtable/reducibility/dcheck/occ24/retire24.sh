#!/bin/zsh
# Retire old worker K (pid P, current key KEY) the moment KEY's result line appears, then start claim worker ID.
cd ${0:a:h}; K=$1; P=$2; KEY=$3; ID=$4
until grep -q "^$KEY " results24b_w$K.txt; do python3 -c 'import time; time.sleep(20)'; done
for c in $(pgrep -P $P); do pkill -P $c; kill $c; done; kill $P
echo "$(date -u '+%m-%d %H:%MZ') old worker $K retired after $KEY; claim worker $ID started" >> retire24.log
nohup ./run24claim.sh $ID > /dev/null 2>&1 &!
