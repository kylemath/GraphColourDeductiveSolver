#!/usr/bin/env python3
"""Kempe's 1879 step at DL states, literal (simultaneous) vs sequential, per hole.
At a DL state (link alpha,mu,alpha,A,B at x_j..x_{j+4}) Kempe swaps K1 = K_{alpha B}(x_{j+2}) and K2 = K_{alpha A}(x_j)
at the same time. Literal success <=> the simultaneous swap is a proper colouring (then the link is filled).
Heawood trap <=> literal failure. We also record whether K1 and K2 share a vertex, and the sequential outcomes (tm_lib.kempe2).
usage: tm_kempe1879.py OUT.jsonl SRC (same --src syntax as tm_run, rot:/faces-json:/heawood:) [--names ...]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tm_lib import Hole, read_rot_lines, rot_from_faces
from collections import Counter
out, src = sys.argv[1], sys.argv[2]
names = set(sys.argv[sys.argv.index('--names') + 1].split(',')) if '--names' in sys.argv else None
kind, path = src.split(':', 1)
if kind == 'rot': graphs = read_rot_lines(path, names)
elif kind == 'faces-json': graphs = [(os.path.basename(p)[:-5], rot_from_faces((lambda d: d.get('faces_ccw') or d['faces'])(json.load(open(p))))) for p in path.split(',')]
elif kind == 'heawood': graphs = [('Heawood1890', json.load(open(path))['rotation'])]
fo = open(out, 'a')
for g, rot in graphs:
    for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
        H = Hole(rot, h); sp = H.sp; li = sp.linki; cyc = H.allDL_cycle_states(); H.classes_and_dist()
        c = Counter()
        for k in range(H.S):
            if H.filled[k] or H.phi[k] != 2: continue
            s = sp.states[k]; cm = sp.cmasks(s); col = [s[li[t]] for t in range(5)]; j = H.j[k]
            x = [li[(j + t) % 5] for t in range(5)]; al, mu, A, B = col[j], col[(j + 1) % 5], col[(j + 3) % 5], col[(j + 4) % 5]
            K1 = sp.flood(1 << x[2], cm[al] | cm[B]); K2 = sp.flood(1 << x[0], cm[al] | cm[A])
            d = list(s)
            for i in range(sp.N):
                if K1 >> i & 1: d[i] = B if s[i] == al else al
                if K2 >> i & 1 and not K1 >> i & 1: d[i] = A if s[i] == al else al
            proper = not (K1 & K2) and all(d[i] != d[w] for i in range(sp.N) for w in range(sp.N) if sp.nbm[i] >> w & 1)
            seq = [a for a, _, _ in H.kempe2[k]]
            tags = ['DL']
            if k in cyc: tags.append('CYC')
            for t in tags:
                c[t] += 1; c[t + '_lit_fail'] += not proper; c[t + '_share'] += bool(K1 & K2)
                c[t + '_seq_fail_both'] += not any(seq); c[t + '_seq_fail_one'] += (sum(seq) == 1)
                c[t + '_lit_fail_dF=%d' % H.dF[k]] += not proper
        fo.write(json.dumps(dict(graph=g, h=h, word=''.join(str(len(rot[v])) for v in rot[h]), **c)) + '\n'); fo.flush()
