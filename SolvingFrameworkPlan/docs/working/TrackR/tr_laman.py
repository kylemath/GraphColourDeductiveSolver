#!/usr/bin/env python3
"""Track R, part 3: the Laman/Henneberg lead (TrackQ Lemma Q-L) along pi-orbits.
For every state t of (a) the law R-cycles of the data files and (b) maximal pi-runs inside R = {DL, N <= 9} of sphere
graphs (e = 0 automatically), compute on G - h:
  nA = |alpha_t|, nN = |N_t| (non-alpha vertices), eH = |E(G[N_t])|, r2 = generic 2D rigidity rank of H_t = G[N_t],
  red = eH - r2 (redundant edges), dof = 2 nN - 3 - r2 (internal degrees of freedom; 0 iff H_t rigid),
  |K_t| split (K_alpha, K_A), r2 of H_t cup H_{t+1} on N_t cup N_{t+1}, Henneberg balance 2(|K_a|-|K_A|) - (eH_{t+1}-eH_t).
usage: tr_laman.py cycles DATA.json ... | tr_laman.py sphere JSONL [maxgraphs] [minrun]"""
import sys, os, json, random
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'TrackQ'))
from tq_roles import roles
from tn_lib import Engine
from tn_forest import parse_dump

RNG = np.random.default_rng(7)


def rank2d(V, E):
    V = sorted(V)
    if len(V) < 2 or not E: return 0
    ix = {v: i for i, v in enumerate(V)}; best = 0
    for _ in range(2):
        P = RNG.standard_normal((len(V), 2))
        M = np.zeros((len(E), 2 * len(V)))
        for r, (a, b) in enumerate(E):
            d = P[ix[a]] - P[ix[b]]; M[r, 2 * ix[a]:2 * ix[a] + 2] = d; M[r, 2 * ix[b]:2 * ix[b] + 2] = -d
        best = max(best, np.linalg.matrix_rank(M, tol=1e-8))
    return int(best)


def state_rows(n, E, cols):
    rows = []; L = len(cols)
    for t, c in enumerate(cols):
        j, (a, m, A, B) = roles(c)
        Nset = {v for v in range(1, n) if c[v] != a}
        H = [e for e in E if e[0] in Nset and e[1] in Nset]
        r2 = rank2d(Nset, H)
        rows.append(dict(t=t, nA=n - 1 - len(Nset), nN=len(Nset), eH=len(H), r2=r2, red=len(H) - r2, dof=2 * len(Nset) - 3 - r2, N=None, roles=(a, m, A, B), Nset=Nset, H=H))
    return rows


def step_rows(n, E, cols, rows, cyclic):
    L = len(cols); out = []
    for t in range(L if cyclic else L - 1):
        c, c2 = cols[t], cols[(t + 1) % L]
        a, m, A, B = rows[t]['roles']; j2, (a2, m2, A2, B2) = roles(c2)
        mp = {a: a2, m: A2, B: m2, A: B2}
        K = {v for v in range(1, n) if mp[c[v]] != c2[v]}
        Ka = sum(1 for v in K if c[v] == a); KA = len(K) - Ka
        Nu = rows[t]['Nset'] | rows[(t + 1) % L]['Nset']
        Hu = sorted(set(rows[t]['H']) | set(rows[(t + 1) % L]['H']))
        Hi = sorted(set(rows[t]['H']) & set(rows[(t + 1) % L]['H']))
        out.append(dict(Ka=Ka, KA=KA, r2U=rank2d(Nu, Hu), nU=len(Nu), eU=len(Hu), r2I=rank2d(rows[t]['Nset'] & rows[(t + 1) % L]['Nset'], Hi), eI=len(Hi),
                        hb=2 * (Ka - KA) - (rows[(t + 1) % L]['eH'] - rows[t]['eH'])))
    return out


def show(name, e, Nprof, rows, steps):
    print('%s e=%s Nprof=%s' % (name, e, Nprof))
    print('   t N  |alpha| |N| eH 2|N|-3 r2 red dof |  Ka KA  hb  | r2(HtuHt+1) dofU red_U | r2(Ht^Ht+1) eI')
    for i, r in enumerate(rows):
        s = steps[i] if i < len(steps) else None
        tail = ('| %2d %2d %3d  | %3d %3d %3d | %3d %3d' % (s['Ka'], s['KA'], s['hb'], s['r2U'], 2 * s['nU'] - 3 - s['r2U'], s['eU'] - s['r2U'], s['r2I'], s['eI'])) if s else ''
        print('  %2d %s %5d %4d %3d %5d %4d %3d %3d %s' % (r['t'], Nprof[i], r['nA'], r['nN'], r['eH'], 2 * r['nN'] - 3, r['r2'], r['red'], r['dof'], tail))


def relabel(line, hole):
    p = line.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; n = len(rot)
    link = rot[hole]; order = [hole] + link + [v for v in range(n) if v != hole and v not in link]
    mp = {v: i for i, v in enumerate(order)}
    adj = [None] * n
    for v in range(n): adj[mp[v]] = [mp[w] for w in rot[v]]
    # rotate adj[0] to start at 1
    k = adj[0].index(1); adj[0] = adj[0][k:] + adj[0][:k]
    return '%s %d %s' % (p[0], n, ';'.join(','.join(map(str, a)) for a in adj)), n, adj


def runs_in_R(S):
    good = lambda x: x >= 0 and S[x]['kind'] == 1 and S[x]['N'] <= 9
    pred = {}
    for i in range(len(S)):
        if good(i) and good(S[i]['pi']): pred[S[i]['pi']] = i
    out = []
    for i in range(len(S)):
        if not good(i) or i in pred: continue
        path = [i]; x = S[i]['pi']
        while good(x) and x not in path: path.append(x); x = S[x]['pi']
        out.append(path)
    return out


def main():
    mode = sys.argv[1]
    if mode == 'cycles':
        for f in sys.argv[2:]:
            d = json.load(open(f)); n = d['n']; E = [tuple(e) for e in d['E'] if 0 not in e]
            rows = state_rows(n, E, d['cols']); steps = step_rows(n, E, d['cols'], rows, True)
            show(d['src'], len(E) - (3 * (n - 1) - 8), d['Nprof'], rows, steps)
    else:
        maxg = int(sys.argv[3]) if len(sys.argv) > 3 else 20; minrun = int(sys.argv[4]) if len(sys.argv) > 4 else 6
        recs = [json.loads(l) for l in open(sys.argv[2])]
        recs = [r for r in recs if r.get('where', {}).get('Rrun', 0) >= minrun]
        recs.sort(key=lambda r: -r['where']['Rrun'])
        ed = Engine(dump=True, maxstates=400000); seen = set(); done = 0
        for r in recs:
            line, n, adj = relabel(r['graph'], r['where']['hole'])
            if line.split()[2] in seen: continue
            seen.add(line.split()[2])
            js, tn, dump = ed.run(line)
            if dump is None: continue
            S = parse_dump(dump)
            E = sorted({tuple(sorted((u, v))) for u in range(1, n) for v in adj[u] if v != 0})
            for path in runs_in_R(S):
                if len(path) < minrun: continue
                cols = [[-1 if ch == '-' else int(ch) for ch in S[x]['col']] for x in path]
                rows = state_rows(n, E, cols); steps = step_rows(n, E, cols, rows, False)
                show('%s(h%d) run%d' % (r['graph'].split()[0], r['where']['hole'], len(path)), len(E) - (3 * (n - 1) - 8), ''.join(str(S[x]['N']) for x in path), rows, steps)
            done += 1
            if done >= maxg: break


if __name__ == '__main__':
    main()
