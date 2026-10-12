#!/usr/bin/env python3
"""Track S: longest pi-runs of DL states with Q_t = F13 connected (P2 = (2,1)), versus R-runs (DL, N <= 9).
Also: are Q-cycles (pi-cycles with Q connected at all states) ever found?
usage: ts_qruns.py GRAPHFILE stride offset maxgraphs   (all degree-5 holes of each graph)
   or: ts_qruns.py GRAPHFILE name:hole ..."""
import sys, json
from ts_lib import load_graphs, HoleData


def longest(hd, pred):
    S = hd.S; ok = [pred(i) for i in range(S)]
    best = 0; cyc = 0
    pre = set()
    for i in range(S):
        p = hd.info[i].get('pi') if ok[i] else None
        if p is not None and ok[p]: pre.add(p)
    seen = set()
    for i in range(S):
        if not ok[i] or i in pre: continue
        L = 0; x = i
        while x is not None and ok[x] and x not in seen:
            seen.add(x); L += 1; x = hd.info[x].get('pi')
        best = max(best, L)
    for i in range(S):
        if ok[i] and i not in seen: cyc += 1
    return best, cyc


def main():
    a = sys.argv
    if len(a) > 2 and ':' in a[2]:
        G = load_graphs(a[1], {s.rsplit(':', 1)[0] for s in a[2:]}); specs = [(s.rsplit(':', 1)[0], int(s.rsplit(':', 1)[1])) for s in a[2:]]
    else:
        stride, off, mx = int(a[2]), int(a[3]), int(a[4]); G = {}; specs = []
        for ln, l in enumerate(open(a[1])):
            if ln % stride != off: continue
            p = l.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            G[p[0]] = rot
            specs += [(p[0], h) for h in range(len(rot)) if len(rot[h]) == 5]
            if len(G) >= mx: break
    hist = {}
    for nm, h in specs:
        hd = HoleData(G[nm], h)
        dl = lambda i: hd.info[i]['kind'] == 'DL'
        R = lambda i: dl(i) and hd.info[i]['N'] <= 9
        Q = lambda i: dl(i) and hd.info[i]['c6'][2] + hd.info[i]['c6'][3] == 3
        QQ = lambda i: Q(i) and hd.info[i]['c6'][4] + hd.info[i]['c6'][5] == 3
        r = dict(g=nm, h=h, R=longest(hd, R), Q=longest(hd, Q), QQ=longest(hd, QQ))
        print(json.dumps(r), flush=True)


if __name__ == '__main__':
    main()
