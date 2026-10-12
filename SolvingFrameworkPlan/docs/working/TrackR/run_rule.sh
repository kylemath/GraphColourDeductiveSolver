#!/bin/sh
# per-cycle local-rule tests: state-specific part-trajectory prices (partT r=1,2) and tag-equivariant prices (part r=2,5)
cd "$(dirname "$0")"
for f in data/*_data.json; do b=$(basename $f _data.json); for spec in "1 partT" "2 partT" "5 part" "2 part"; do set -- $spec; echo "$1 $2 $f out/rule_${b}_r$1_$2"; done; done | \
 xargs -P 4 -L 1 sh -c 'nice -n 10 ../TrackQ/.venv/bin/python tr_rule.py $0 $1 $2 --out $3.json > $3.log 2>&1'
