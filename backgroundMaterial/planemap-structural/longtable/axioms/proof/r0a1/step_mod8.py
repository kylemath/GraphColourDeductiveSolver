"""Lemma E check: along every step (M_t, M_{t+1}) -> (M_{t+1}, M_{t+2}) of D in planar census graphs, the total
Tait sign S changes by 4 mod 8 (so closed walks have even length), and S = 4*deg_Fisk - 1.
usage: step_mod8.py n"""
import sys, json, collections
from r0lib import G5, analyse
from sigsum import ccw_rot, S
from fisk import embed, faces, degvec
n = int(sys.argv[1]); dS = collections.Counter(); fiskrel = collections.Counter(); hamD = collections.Counter()
for l in open(f'out/census_n{n}_p.jsonl'):
    r = json.loads(l); g = G5(r['n'], [tuple(e) for e in r['edges']], r['fv'])
    A = analyse(g); rot = ccw_rot(g); P = A['P']
    ccw = embed(g); F, cf = faces(g, ccw)
    Sv = {}
    for (i, j) in A['arcs']:
        Sv[(i, j)] = S(g, rot, P[i], P[j])
        d, link, ok = degvec(g, ccw, F, cf, P[i], P[j])
        fiskrel[(Sv[(i, j)] == 4 * d[0] - 1, d[0] == d[1] == d[2] == d[3] + 1)] += 1
        if (i, j) in A['ham']: hamD[d[0]] += 1
    for (i, j) in A['arcs']:
        for k in A['D'].successors(j):
            dS[(Sv[(j, k)] - Sv[(i, j)]) % 8] += 1
print(f'n={n}: (S_(t+1) - S_t) mod 8 over all steps: {dict(dS)};  (S == 4D-1, deg = (D,D,D,D-1)) over arcs: {dict(fiskrel)};  Fisk D at Ham arcs: {dict(sorted(hamD.items()))}')
