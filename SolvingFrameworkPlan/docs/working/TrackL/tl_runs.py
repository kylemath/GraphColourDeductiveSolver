#!/usr/bin/env python3
"""Track L [data]: per-state quantities along maximal pi-runs inside R = {DL, N <= 9} at sphere holes.

For each listed hole, every maximal pi-run inside R of length >= MINLEN is printed with, per state:
  N, extra role (9-states), l1/l2 = lengths of the Lock1 (muA, x1->x3) / Lock2 (muB, x1->x4) paths,
  |K| = |K_aA(x2)| (pi's swap set), |Kt| = |K_aB(x0)| (pi^-1's swap set), |L| = |K_am(x2)|, |LAB| = |K_AB(x3)|,
  |Z| (9-states), and the run's ends (state kind / N of the pi-preimage and pi-image).
usage: tl_runs.py GRAPHFILE NOTABLE.jsonl MINLEN [prefix]"""
import sys, json
from collections import deque
from tl_lib import HoleData, read_graphs, RIGID

ROLE = ['am', 'AB', 'aA', 'mB', 'aB', 'mA']


def dist(hd, col, s, t, pair):
    prev = {s: None}; dq = deque([s])
    while dq:
        u = dq.popleft()
        if u == t: break
        for w in hd.Hh.adj[u]:
            if w not in prev and col[w] in pair: prev[w] = u; dq.append(w)
    if t not in prev: return -1
    k = 0; x = t
    while prev[x] is not None: x = prev[x]; k += 1
    return k


def quantities(hd, i):
    r = hd.info[i]; col = hd.col[i]; x = r['x']; al, mu, A, B = r['roles']; Hh = hd.Hh
    q = dict(N=r['N'])
    q['l1'] = dist(hd, col, x[1], x[3], (mu, A)); q['l2'] = dist(hd, col, x[1], x[4], (mu, B))
    q['K'] = len(Hh.comp(col, x[2], (al, A))); q['Kt'] = len(Hh.comp(col, x[0], (al, B)))
    L = Hh.comp(col, x[2], (al, mu)); q['L'] = len(L); LAB = Hh.comp(col, x[3], (A, B)); q['LAB'] = len(LAB)
    z = {al: 0, mu: 1, A: 2, B: 3}; CYC = {(1, 2, 3), (2, 3, 1), (3, 1, 2)}; cw = 0; nf = 0
    for u, ru in enumerate(hd.rot):
        if u == hd.h: continue
        for t in range(len(ru)):
            a, b = ru[t], ru[(t + 1) % len(ru)]
            if hd.h in (a, b) or u > a or u > b: continue
            nf += 1
            if (z[col[u]] ^ z[col[a]], z[col[a]] ^ z[col[b]], z[col[b]] ^ z[col[u]]) in CYC: cw += 1
    q['cw'] = cw
    q['a'] = sum(1 for v in Hh.V if col[v] == al)
    q['sizes'] = '%d/%d/%d/%d' % tuple(sum(1 for v in Hh.V if col[v] == cc) for cc in (al, mu, A, B))
    if r['N'] == 9:
        ex = hd.extra(i); q['ex'] = ROLE[ex[0]] if len(ex) == 1 else '?'
        if ex == [0]:
            q['Z'] = len([v for v in Hh.V if col[v] in (al, mu)]) - len(L)
        elif ex == [1]:
            q['Z'] = len([v for v in Hh.V if col[v] in (A, B)]) - len(LAB)
    return q


def lab(hd, i):
    if i is None: return 'undef'
    r = hd.info[i]
    if r['kind'] != 'DL': return r['kind']
    return 'DL%d' % r['N']


def main():
    gf, notable, minlen = sys.argv[1], sys.argv[2], int(sys.argv[3])
    pref = sys.argv[4] if len(sys.argv) > 4 else ''
    want = {}
    for l in open(notable):
        d = json.loads(l)
        if d['Rrun'] >= minlen and d['name'].startswith(pref): want.setdefault(d['name'], []).append(d['hole'])
    for name, rot in read_graphs(gf):
        if name not in want: continue
        for h in want[name]:
            hd = HoleData(rot, h)
            inR = lambda i: i is not None and hd.info[i]['kind'] == 'DL' and hd.info[i]['N'] <= 9
            pre = {}
            for i in range(hd.S):
                if hd.info[i]['kind'] == 'DL' and hd.info[i]['pi'] is not None: pre[hd.info[i]['pi']] = i
            for i in range(hd.S):
                if not inR(i) or inR(pre.get(i)): continue
                run = [i]; y = hd.info[i]['pi']
                while inR(y) and y != i: run.append(y); y = hd.info[y]['pi']
                if len(run) < minlen: continue
                print('%s h%d run %d  [%s] ... [%s]' % (name, h, len(run), lab(hd, pre.get(i)), lab(hd, y)))
                for s in run:
                    q = quantities(hd, s)
                    print('    ', ' '.join('%s=%s' % (k, q[k]) for k in ('N', 'ex', 'sizes', 'cw', 'l1', 'l2', 'K', 'Kt', 'L', 'LAB', 'Z') if k in q))
                sys.stdout.flush()


if __name__ == '__main__':
    main()
