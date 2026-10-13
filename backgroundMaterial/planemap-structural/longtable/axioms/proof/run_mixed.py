import sys, json
from sat_t1v import Enc, run, to_line
n = int(sys.argv[1]); tl = float(sys.argv[2])
e = Enc(n, 10, 3); st, sols, info = run(e, tl, verbose=False)
print(json.dumps(dict(n=n, L=10, mode='mixed', status=st, **info)), flush=True)
for E, M, fv, inf in sols: print('SOL', to_line(e, E, fv), inf)
