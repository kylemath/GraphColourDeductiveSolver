#!/usr/bin/env python3
"""Track R: sigma-type check from data files: at every N = 9 state list the link-free parts (pair name, size);
sigma-type <=> the only link-free part is an alpha-mu part.  usage: tr_ztag.py DATA.json ..."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tr_lag import load
from tr_show import rolename
for f in sys.argv[1:]:
    D = load(f); out = []
    for t, c in enumerate(D['cols']):
        if D['Nprof'][t] != '9': continue
        z = [rolename(c, p, q) + str(len(P)) for (tt, p, q, P) in D['parts'] if tt == t and not (P & {1, 2, 3, 4, 5})]
        out.append('/'.join(z) or '-')
    tag = 'NON-sigma (Z in AB somewhere)' if any(x.startswith('AB') for x in out) else 'sigma-type (no AB link-free part; - = Z is a single vertex)'
    print(D['src'], D['Nprof'], 'Z by in-shape state:', ' '.join(out), ' ', tag)
