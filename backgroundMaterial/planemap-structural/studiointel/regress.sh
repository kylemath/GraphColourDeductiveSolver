#!/bin/sh
# studiointel regression: producer vs published numbers (MathConjectureR sec.3) and vs the independent checker. Runs in seconds.
set -e
cd "$(dirname "$0")"; T=${TMPDIR:-/tmp}/studiointel-reg; mkdir -p $T
python3 - <<PY
import json, graphs
for n, f in (('ico', graphs.icosahedron()), ('A3', graphs.A_r(3)), ('A4', graphs.A_r(4)), ('A5', graphs.A_r(5))):
    json.dump({'faces': f}, open('$T/%s.json' % n, 'w'))
PY
exp() { python3 radius.py $1 0 | python3 -c "
import sys,json; r=json.loads(sys.stdin.read()); got=(r['n_states'],r['n_filled'],r['n_DL'],r['DL_radius_hist']); want=$2
assert got==want, (got,want); print('producer $1 ok', got)"; }
exp ico "(20,10,0,{})"
exp A:3 "(100,40,30,{'2':20,'3':10})"
exp A:4 "(520,200,80,{'2':80})"
exp A:5 "(2720,1040,530,{'2':530})"
for n in ico A3 A4 A5; do python3 check.py enum $T/$n.json 0; done
# certificate round trip: A_3 witness has r = 3 exactly: lb K=3 must pass, K=4 must fail
python3 radius.py A:3 0 | python3 -c "
import sys,json; r=json.loads(sys.stdin.read()); w=r['witness']; json.dump({str(u):c for u,c in zip(w['order'],w['state'])}, open('$T/A3_w.json','w'))"
python3 check.py lb $T/A3.json 0 $T/A3_w.json 3 | grep -q '^OK'
python3 check.py lb $T/A3.json 0 $T/A3_w.json 4 | grep -q '^FAIL'
echo "regression passed"
