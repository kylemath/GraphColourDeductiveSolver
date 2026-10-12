#!/usr/bin/env python3
"""Track L [data]: sector of the extra chain Z at in-shape states.  The lock paths P1 (x1->x3 in muA) and P2 (x1->x4 in
muB) plus h cut the sphere; Z (minus path vertices) is located by which of x0, x2 its component of
T - (P1 u P2 u {h}) reaches ('S0' / 'S2' / 'S34' = neither / 'mixed').  Along runs, prints the sector sequence.
usage: tl_sector.py GRAPHFILE NOTABLE.jsonl MINLEN [prefix]"""
import sys, json
from collections import Counter, deque
from tl_lib import HoleData, read_graphs


def path(hd, col, s, t, pair):
    prev = {s: None}; dq = deque([s])
    while dq:
        u = dq.popleft()
        for w in hd.Hh.adj[u]:
            if w not in prev and col[w] in pair: prev[w] = u; dq.append(w)
    P = [t]
    while prev[P[-1]] is not None: P.append(prev[P[-1]])
    return P


def sector(hd, i):
    r = hd.info[i]; col = hd.col[i]; al, mu, A, B = r['roles']; x = r['x']; Hh = hd.Hh
    P = set(path(hd, col, x[1], x[3], (mu, A))) | set(path(hd, col, x[1], x[4], (mu, B)))
    L = Hh.comp(col, x[2], (al, mu))
    Z = [v for v in Hh.V if col[v] in (al, mu) and v not in L]
    blocked = P | {hd.h}
    secs = set(); onpath = 0
    for z in Z:
        if z in P: onpath += 1; continue
        seen = {z}; st = [z]; hit = set()
        while st:
            u = st.pop()
            if u == x[0]: hit.add('S0')
            if u == x[2]: hit.add('S2')
            for w in hd.rot[u]:
                if w not in seen and w not in blocked: seen.add(w); st.append(w)
        secs.add('/'.join(sorted(hit)) if hit else 'S34')
    return ('|'.join(sorted(secs)) or 'none') + ('+p%d' % onpath if onpath else '')


def main():
    gf, notable, minlen = sys.argv[1], sys.argv[2], int(sys.argv[3])
    pref = sys.argv[4] if len(sys.argv) > 4 else ''
    want = {}
    for l in open(notable):
        d = json.loads(l)
        if d['Rrun'] >= minlen and d['name'].startswith(pref): want.setdefault(d['name'], []).append(d['hole'])
    T = Counter(); TS = Counter()
    for name, rot in read_graphs(gf):
        if name not in want: continue
        for h in want[name]:
            hd = HoleData(rot, h)
            inR = lambda i: i is not None and hd.info[i]['kind'] == 'DL' and hd.info[i]['N'] <= 9
            pre = {hd.info[i]['pi']: i for i in range(hd.S) if hd.info[i]['kind'] == 'DL' and hd.info[i]['pi'] is not None}
            for i in range(hd.S):
                if not inR(i) or inR(pre.get(i)): continue
                run = [i]; y = hd.info[i]['pi']
                while inR(y) and y != i: run.append(y); y = hd.info[y]['pi']
                if len(run) < minlen: continue
                seq = [sector(hd, s) for s in run if hd.inshape(s)]
                for s in seq: TS[s] += 1
                T[' '.join(seq)] += 1
    for k, v in sorted(TS.items(), key=lambda t: -t[1]): print('sector', k, v)
    for k, v in sorted(T.items(), key=lambda t: -t[1])[:30]: print('seq', k, v)


if __name__ == '__main__':
    main()
