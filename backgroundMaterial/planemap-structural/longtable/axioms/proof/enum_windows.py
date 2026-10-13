"""Enumerate ALL open 1212 windows (ham normal form, M_0 u M_1 Hamiltonian) at given n, W, axiom pattern.
Blocking on (chord set, v-labels).  Output: one JSON line per window: chords, labels, matchings.
usage: enum_windows.py n W axv [maxsol] [tlimit]"""
import sys, json, time
from sat_t1v import Enc
from pysat.solvers import Cadical153

n, W = int(sys.argv[1]), int(sys.argv[2])
axv = [int(c) for c in sys.argv[3]] if len(sys.argv[3]) > 1 else int(sys.argv[3])
maxsol = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 6
tl = float(sys.argv[5]) if len(sys.argv) > 5 else 550
enc = Enc(n, W, axv, word='1212', eager=1, closed=False)
s = Cadical153(bootstrap_with=enc.cl)
t0 = time.time(); nsol = 0; status = 'DONE'
while True:
    if time.time() - t0 > tl: status = 'TIMEOUT'; break
    if not s.solve(): break
    E, M, fv = enc.decode(s.get_model())
    cuts, info = enc.check(E, M, fv)
    if cuts:
        for c in cuts: s.add_clause(c)
        continue
    ch = [enc.edges[e] for e in E if enc.X[e] is not None]
    print(json.dumps(dict(n=n, W=W, chords=ch, fv=[enc.edges[e] for e in fv],
                          M=[sorted(enc.edges[e] for e in M[t]) for t in range(W)], word=info['word'])), flush=True)
    nsol += 1
    blk = [-enc.X[e] for e in E if enc.X[e] is not None]
    blk += [-enc.lab[sv][fv[sv]] for sv in (1, 3, 4)]
    s.add_clause(blk)
    if nsol >= maxsol: status = 'CAP'; break
print(json.dumps(dict(n=n, W=W, axv=sys.argv[3], nsol=nsol, status=status, sec=round(time.time() - t0, 1))), file=sys.stderr)
