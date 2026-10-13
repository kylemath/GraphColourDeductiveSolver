"""Open-window experiment (Long Table run 2): W consecutive states M_0..M_{W-1}, M_0 u M_1 Hamiltonian
(the 'ham' labelling), each M_t DL-good, M_{t+1} the successor, A5v (axv=1) / none (0) / anti (2) at
every state, no closure.  word: None (no condition) or '1212' (alternation imposed on t=1..W-1).
Usage: sat_window.py n W axv word(none|1212) [tlimit]"""
import sys, json
from sat_t1v import Enc, run, to_line

n, W = int(sys.argv[1]), int(sys.argv[2])
axv = [int(c) for c in sys.argv[3]] if len(sys.argv[3]) > 1 else int(sys.argv[3])  # e.g. 12 = A5v at t=0, anti at t=1
word = None if sys.argv[4] == 'none' else sys.argv[4]
tl = float(sys.argv[5]) if len(sys.argv) > 5 else 300
enc = Enc(n, W, axv, word=word, eager=1, closed=False)
st, sols, stats = run(enc, tl, verbose=False)
print(json.dumps(dict(n=n, W=W, axv=axv, word=word, status=st, **stats)), flush=True)
for E, M, fv, info in sols:
    print('SOL', to_line(enc, E, fv), info)

# per-state loop sizes |X_t|, |Y_t| (cubic vertices on each loop) and word letters
if sols and '--dump' in sys.argv:
    from ax_lib import G5, parse_line
    E, M, fv, info = sols[0]
    g = G5(*parse_line(to_line(enc, E, fv)))
    idx = {e: i for i, e in enumerate(E)}
    rows = []
    for t in range(W):
        Mt = frozenset(idx[e] for e in M[t])
        k, d = g.dl(Mt)
        rows.append((t, k, len(d['X'][2]), len(d['Y'][2]), info['word'][t]))
    print('STATES (t,k,|X|,|Y|,w)', rows)
