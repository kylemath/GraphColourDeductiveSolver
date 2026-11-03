# job R3A2 (c): can D11 / D12 enter Studio's receiver LP? Embed each into every receiver 2-ball frame (as f2b_rulecheck.py):
# d = 7, 8, 9 (and 10 for patterns), w0 = 5..8, every 5/non-5 structure Z. (i) receiver (w, s) pattern: an embedding into
# u + w + s only; (ii) private-letter kill (rules / 14'): an embedding using one of w0's privates. Degrees free 5..8 (u fixed).
import os, sys, itertools, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
G = {'__file__': os.path.join(HERE, 'loop', 'k42', 'grow.py'), '__name__': 'grow'}; exec(open(G['__file__']).read(), G)
Q = [G['kcline'](open(os.path.join(HERE, 'out', 'job_R3A2', f)).read().split('\n')[0], 'q') for f in ('d11.in', 'd12.in')]
def frame(d, w0, Z):
    G['D'] = d; G['LK'] = [w0] + [5 if (Z >> k) & 1 else 6 for k in range(1, d)]; G['SV'] = {}
    adj, name, faces = G['build2']({})
    pa = {x: {name[y] for y in adj[v] if y in name} for v, x in name.items()}
    pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
    return pa, pf
res = collections.Counter(); ex = {}
for d in (7, 8, 9, 10):
    for w0 in (5, 6, 7, 8):
        for Z in range(0, 1 << d, 2):
            pa, pf = frame(d, w0, Z)
            base = [('u',)] + [('w', k) for k in range(d)] + [('s', k) for k in range(d)]
            priv = sorted(x for x in pa if x[0] == 'p' and x[1] == 0)
            for mode, P in (('pattern', base), ('private', base + priv)):
                Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}
                fd = {('u',): d} if d <= 8 else {}
                for q in Q:
                    es = G['embeddings'](q, P, pa2, pf2, fd)
                    if mode == 'private': es = [e for e in es if any(v[0] == 'p' for _, v in e)]
                    if es: res[(q[0], mode, d)] += len(es); ex.setdefault((q[0], mode, d), (w0, Z, sorted(es)[0]))
        print('d=%d done' % d, flush=True)
for q in Q:
    for mode in ('pattern', 'private'):
        print(q[0], mode, {d: res[(q[0], mode, d)] for d in (7, 8, 9, 10)})
for k, v in ex.items(): print('example', k, v)
