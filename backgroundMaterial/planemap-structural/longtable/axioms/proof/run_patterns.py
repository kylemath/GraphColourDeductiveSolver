"""Closed 1212 orbits (L = 10, ham normal form) with a prescribed per-state A5v pattern.
By Lemma FE-parity (PROOF-ATTEMPT-1 sec. 2) b_t = b_{t+5} on every closed L = 10 orbit, so only 5-periodic
patterns can occur; up to the Phi-shift symmetry (t -> t+2, which acts transitively on Z/5) the mixed classes are
00001 00011 00101 00111 01011 01111 (1 = A5v, 0 = anti).  usage: run_patterns.py n tlimit [patterns...]"""
import sys, json
from sat_t1v import Enc, run, to_line
n, tl = int(sys.argv[1]), float(sys.argv[2])
pats = sys.argv[3:] or ['00001', '00011', '00101', '00111', '01011', '01111']
for p in pats:
    axv = [1 if p[t % 5] == '1' else 2 for t in range(10)]
    e = Enc(n, 10, axv)
    st, sols, info = run(e, tl, verbose=False)
    print(json.dumps(dict(n=n, L=10, pattern=p, status=st, **info)), flush=True)
    for E, M, fv, inf in sols: print('SOL', to_line(e, E, fv), inf, flush=True)
