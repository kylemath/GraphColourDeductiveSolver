#!/usr/bin/env python3
"""Track S: every all-DL pi-cycle at the given holes (or all degree-5 holes of the given graphs), with the per-state word
kH kF13 kF12 (from chain counts: #P1-1, #P2-2, #P3-2; equal to Tait component counts on the sphere) and the flag
'Q-cycle' (P2 minimal at every state).  usage: ts_qcyc.py GRAPHFILE [name:hole ... | --all [stride off maxg]]"""
import sys, json
from ts_lib import load_graphs, HoleData


def cycles(hd):
    info = hd.info; on = set(); out = []
    for i in range(hd.S):
        if info[i]['kind'] != 'DL' or i in on: continue
        path = []; posd = {}; k = i
        while k is not None and info[k]['kind'] == 'DL' and k not in posd and k not in on:
            posd[k] = len(path); path.append(k); k = info[k]['pi']
        on.update(path)
        if k is not None and k in posd: out.append(path[posd[k]:])
    return out


def main():
    a = sys.argv
    if a[2] == '--all':
        s, off, mx = (int(a[3]), int(a[4]), int(a[5])) if len(a) > 3 else (1, 0, 10 ** 9)
        G = {}; specs = []
        for ln, l in enumerate(open(a[1])):
            if ln % s != off: continue
            p = l.split()
            if len(p) < 3: continue
            rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            G[p[0]] = rot; specs += [(p[0], h) for h in range(len(rot)) if len(rot[h]) == 5]
            if len(G) >= mx: break
    else:
        G = load_graphs(a[1], {q.rsplit(':', 1)[0] for q in a[2:]})
        specs = [(q.rsplit(':', 1)[0], int(q.rsplit(':', 1)[1])) for q in a[2:]]
    nh = 0
    for nm, h in specs:
        hd = HoleData(G[nm], h); nh += 1
        for c in cycles(hd):
            w = []
            for q in c:
                c6 = hd.info[q]['c6']; w.append('%d%d%d' % (c6[0] + c6[1] - 1, c6[2] + c6[3] - 2, c6[4] + c6[5] - 2))
            qc = all(x[1] == '1' for x in w)
            print(json.dumps(dict(g=nm, h=h, L=len(c), Q=qc, nQ=sum(x[1] == '1' for x in w),
                                  Nmin=min(hd.info[q]['N'] for q in c), word=' '.join(w))), flush=True)
    print(json.dumps(dict(holes=nh)), flush=True)


if __name__ == '__main__':
    main()
