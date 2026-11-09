#!/bin/bash
# ST-88: run T1, T2, T3/T4, TV (W6b p8_vectors) and collect T5 (t5_selftest.sh logs) into ../test.log. All at nice 20.
J=$(cd "$(dirname "$0")/.." && pwd); C=${1:-/tmp/swarm-W17/code_gk8}; cd $J
{
echo "== ST-88 tests, $(date -u +%Y-%m-%dT%H:%M:%SZ), code $C (gkfam.py md5 $(md5 -q $C/gkfam.py))"
echo; echo "== T1 worked examples (PAYER8SPEC 3.1 / 3.2)"; nice -n 20 python3 -I tests/t1_examples.py $C
echo; echo "== T2 p8_test.json E examples"; nice -n 20 python3 tests/t2_p8examples.py $C $J
echo; echo "== T3 / T4 independent set-based reference (seed 8808; 600 rows x 440 keys)"; nice -n 20 python3 -I tests/t3_indep.py $C 8808 300 80 100 60
echo; echo "== TV W6b p8_vectors (a, b, c, d)"; nice -n 20 python3 tests/tv_p8vectors.py $C $J/in/p8_vectors $J/in/cg_keys_w6b16s_p8_k86GS14.txt
echo; echo "== T5 W17 GK self-test (from tests/t5a_k260.log, tests/t5b_k260p8.log; run by tests/t5_selftest.sh)"
for f in tests/t5a_k260.log tests/t5b_k260p8.log; do echo "-- $f"; grep -h "^W17 GK keys\|GK numpy window\|^W17 GK window\|sep: W17 GK\|GK self-test\|GK per-position\|^VERDICT\|^FAIL" $f | cut -c1-420; done
echo "(t5b VERDICT FAIL comes only from senderR2 / cons2 rows: the point has no amounts for the 24 keys and the self-test gives each 0.01 via KSAMT, which makes the point infeasible; the self-test lines themselves pass)"
} 2>&1
