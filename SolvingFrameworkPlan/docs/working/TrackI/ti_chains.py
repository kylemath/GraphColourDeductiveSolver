#!/usr/bin/env python3
"""Track I: primal-only check of the chain-parity law (Track I Corollary 6), using only the TrackH vertex engine.

N(s) = total number of Kempe chains of s = sum over the six colour pairs of the number of components of the pair graph.
Law (sphere, conjectured in general, proved for rigid c and whenever K_{alpha A}(x_{j+2}) has no holes):
    for every DL state c:   N(pi(c)) - N(c)  ==  [pi(c) is DL]   (mod 2).
Rigid isolation is the special case N(c) = 8 (the minimum): N(pi c) = 8 would need [pi c DL] = 0.
Also tallies, per state kind of pi(c), the parity of N(pi c) - N(c).
usage: ti_chains.py GRAPHFILE STRIDE MAXGRAPHS [name-prefix]"""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackH'))
from th_engine import Hole

def nchains(H, col):
    tot = 0
    for p in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
        left = {v for v in H.V if col[v] in p}
        while left:
            s = next(iter(left)); left -= H.comp(col, s, p); tot += 1
    return tot

def main():
    gf, stride, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    filt = sys.argv[4] if len(sys.argv) > 4 else ''
    st = Counter(); k = 0
    for ln, l in enumerate(open(gf)):
        if ln % stride: continue
        p = l.split()
        if len(p) < 3 or not p[0].startswith(filt): continue
        rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        k += 1
        if k > maxg: break
        for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
            Hh = Hole(rot, h); S = len(Hh.states); info = [None] * S; Nc = [None] * S
            for i in range(S):
                r, col = Hh.analyse_state(i); info[i] = r; Nc[i] = nchains(Hh, col)
            for i in range(S):
                r = info[i]
                if r['kind'] != 'DL' or r['pi'] is None: continue
                t = r['pi']; kind = info[t]['kind']
                d = (Nc[t] - Nc[i]) % 2
                st[(kind, d)] += 1
                st['law_fail'] += d != (kind == 'DL')
                if Nc[i] == 8: st['rigid'] += 1; st['rigid_img_N8'] += Nc[t] == 8
    print(gf, filt, 'graphs', min(k, maxg), dict(sorted(st.items(), key=str)), flush=True)

if __name__ == '__main__':
    main()
