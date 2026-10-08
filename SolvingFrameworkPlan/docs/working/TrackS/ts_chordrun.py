#!/usr/bin/env python3
"""Track S: R-runs in the exhaustive planar chord model (TrackH model, generator TrackI ti_lib.chord_instances).
Every rigid DL instance (a planar cubic multigraph G with one degree-5 vertex v and a Tait colouring with H, F12, F13
connected) is iterated under pi at the Tait level:  switch 1<->3 on X (F13-trail through e1, e3), rename colours
(1',2',3') = (3,1,2) and v-labels e'_t = e_{t+3}.  We record the length of the forward run inside R = {DL, N <= 9}
(N = 5 + k(H) + k(F12) + k(F13), sphere) and detect closed orbits.
usage: ts_chordrun.py NMAX"""
import sys, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackI'))
from ti_lib import chord_instances, analyse, Tait, DL12, DL13

RN = {3: 1, 1: 2, 2: 3}


def state_info(E):
    T = Tait(E)
    M = {c: {k for k, e in enumerate(E) if e[2] == c} for c in (1, 2, 3)}
    H = M[2] | M[3]; F12 = M[1] | M[2]; F13 = M[1] | M[3]
    vcol = [E[T.lab['e%d' % t]][2] for t in range(5)]
    if vcol != [1, 1, 2, 1, 3]: return None
    if T.pairing(F12) != DL12 or T.pairing(F13) != DL13: return dict(DL=False)
    return dict(DL=True, N=5 + T.ncomp(H) + T.ncomp(F12) + T.ncomp(F13), T=T, F13=F13)


def pi(E, info):
    T = info['T']; X, _ = T.trail(info['F13'], T.lab['e1']); X = set(X)
    out = []
    for k, (a, b, c, l) in enumerate(E):
        if k in X: c = {1: 3, 3: 1}[c]
        c = RN[c]
        if l: l = 'e%d' % ((int(l[1]) + 2) % 5)
        out.append((a, b, c, l))
    return out


def main():
    for N in range(3, int(sys.argv[1]) + 1, 2):
        st = Counter(); hist = Counter()
        for E, meta in chord_instances(N):
            r = analyse(E)
            if r is None or not r['rigid']: continue
            st['rigid'] += 1
            key0 = tuple(E); cur = E; L = 0; closed = False; seen = {key0}
            while True:
                inf = state_info(cur)
                if inf is None or not inf['DL'] or inf['N'] > 9: break
                L += 1
                nxt = pi(cur, inf)
                if tuple(nxt) in seen:
                    closed = True; break
                seen.add(tuple(nxt)); cur = nxt
                if L > 200: break
            hist[L] += 1; st['closed'] += closed
        print('N', N, dict(st), 'forward R-run length histogram', sorted(hist.items()), flush=True)


if __name__ == '__main__':
    main()
