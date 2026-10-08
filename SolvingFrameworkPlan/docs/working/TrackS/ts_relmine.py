#!/usr/bin/env python3
"""Track S experiment 3: mine universal set relations (subset / disjoint) between the named chain vertex sets of the
three states of a Phi-step u (rigid) -> c = pi(u) (in-shape) -> u2 = pi(c) (rigid), and of the next Phi-step.
Named sets at a DL state (roles in its own frame, x_k = x_{j+k}):
  am, AB (P1; at in-shape am = link am chain, Z = link-free am chain), K = K_aA(x2), K0 = K_aA(x0), mB (P2),
  J0 = K_aB(x0), J2 = K_aB(x2), mA (P3);  colour classes a, m, A, B.
Relations that hold at every instance on the sphere are candidate planar lemmas; we then test them off the sphere.
usage: ts_relmine.py OUTJSON GRAPHFILE name:hole ...  | GRAPHFILE --stride s off maxg"""
import sys, json, itertools
from ts_lib import load_graphs, HoleData, phi_steps, pair_components


def named(hd, i):
    r = hd.info[i]; col = hd.col[i]; al, mu, A, B = r['roles']; x = r['x']
    out = {}
    for nm, pr in (('am', (al, mu)), ('AB', (A, B)), ('aA', (al, A)), ('mB', (mu, B)), ('aB', (al, B)), ('mA', (mu, A))):
        cs = pair_components(hd, col, pr)
        if nm == 'am':
            for K in cs:
                if x[0] in K: out['am'] = frozenset(K)
                else: out['Z'] = frozenset(K) if 'Z' not in out else out['Z'] | frozenset(K)
        elif nm == 'aA':
            for K in cs:
                if x[2] in K: out['K'] = frozenset(K)
                elif x[0] in K: out['K0'] = frozenset(K)
        elif nm == 'aB':
            for K in cs:
                if x[0] in K: out['J0'] = frozenset(K)
                elif x[2] in K: out['J2'] = frozenset(K)
        else:
            out[nm] = frozenset(set().union(*cs))
    for nm, cc in (('a', al), ('m', mu), ('A', A), ('B', B)):
        out[nm] = frozenset(v for v in hd.Hh.V if col[v] == cc)
    return out


def main():
    outp = sys.argv[1]; a = sys.argv[2:]
    if len(a) > 1 and a[1] == '--stride':
        s, off, mx = int(a[2]), int(a[3]), int(a[4]); G = {}; specs = []
        for ln, l in enumerate(open(a[0])):
            if ln % s != off: continue
            p = l.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            G[p[0]] = rot; specs += [(p[0], h) for h in range(len(rot)) if len(rot[h]) == 5]
            if len(G) >= mx: break
    else:
        G = load_graphs(a[0], {q.rsplit(':', 1)[0] for q in a[1:]})
        specs = [(q.rsplit(':', 1)[0], int(q.rsplit(':', 1)[1])) for q in a[1:]]
    holds = None; count = 0; nontriv = None
    for nm, h in specs:
        hd = HoleData(G[nm], h)
        for (u, c, u2) in phi_steps(hd):
            if not hd.inshape(c): continue
            S = {}
            for tag, i in (('u', u), ('c', c), ('w', u2)):
                for k, v in named(hd, i).items(): S[tag + '.' + k] = v
            rel = set(); nonempty = set()
            keys = sorted(S)
            for p, q in itertools.permutations(keys, 2):
                if p.split('.')[0] == q.split('.')[0] and p < q: pass
                A, B = S[p], S[q]
                if A and A <= B: rel.add(('sub', p, q))
                if p < q and not (A & B): rel.add(('dis', p, q))
            count += 1
            holds = rel if holds is None else holds & rel
    res = sorted(holds) if holds else []
    # drop relations inside one state (definitional) for the summary
    cross = [r for r in res if r[1].split('.')[0] != r[2].split('.')[0]]
    json.dump(dict(instances=count, cross=cross, all=res), open(outp, 'w'), indent=0)
    print('instances', count, 'universal cross-state relations', len(cross))
    for r in cross: print(' ', r)


if __name__ == '__main__':
    main()
