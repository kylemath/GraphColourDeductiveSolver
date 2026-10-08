#!/usr/bin/env python3
"""Track H: validate the chord model of th_chord.py against the vertex engine.
For every chord-model instance with N <= NMAX that the model classifies as DL: build the plane near-cubic graph
(rotation system), trace its faces, form the primal near-triangulation T - h (vertices = faces; h added inside the
face of v), recover the vertex 4-colouring from the Tait colouring (Z2^2 integration), and compare with th_engine:
DL, rigid (component counts (1,1,2,1,2,1)), and DL / rigid of pi(c).  Instances whose primal has a multi-edge are
reported separately (th_engine needs a simple graph).
usage: th_chordcheck.py NMAX"""
import sys
from collections import Counter
import th_chord as C
from th_engine import Hole
from th_rigidscan_lib import counts

TAIT = {1: (0, 1), 2: (1, 0), 3: (1, 1)}   # alpha=00, mu=01, A=10, B=11: 1 = a+m, 2 = a+A, 3 = a+B

def instance_graph(N, mi, mo):
    """returns darts: list of (x, y, colour, id) with rotation lists of dart ids at each vertex (ccw)."""
    E = []  # edges: (x, y, colour)
    def add(x, y, c): E.append((x, y, c)); return len(E) - 1
    eH = {}
    eH[0] = add(0, 1, 2)                     # e2
    for i in range(1, N): eH[i] = add(i, i + 1, 3 if i % 2 == 1 else 2)
    eH[N] = add(N, 0, 3)                     # e4
    chord_in = {}; chord_out = {}; vlab = {'e2': eH[0], 'e4': eH[N]}
    for side, M in (('in', mi), ('out', mo)):
        for a, b in M:
            if isinstance(a, str): a, b = b, a
            if isinstance(b, str):
                k = add(a, 0, 1); vlab[b] = k
            else:
                k = add(a, b, 1); (chord_in if side == 'in' else chord_out)[b] = k
            (chord_in if side == 'in' else chord_out)[a] = k
    rot = {}
    for i in range(1, N + 1):
        nxt, prv = eH[i], eH[i - 1]
        if i in chord_in: rot[i] = [nxt, chord_in[i], prv]
        else: rot[i] = [nxt, prv, chord_out[i]]
    rot[0] = [vlab['e0'], vlab['e1'], vlab['e2'], vlab['e3'], vlab['e4']]
    return E, rot, vlab

def faces(E, rot):
    # dart = (edge id, from vertex); next dart in face: at head w, take the edge after e in rot[w] clockwise...
    def other(k, x):
        a, b, _ = E[k]; return b if a == x else a
    seen = set(); F = []
    for k in range(len(E)):
        for x in (E[k][0], E[k][1]):
            if (k, x) in seen: continue
            face = []; d = (k, x)
            while d not in seen:
                seen.add(d); face.append(d)
                kk, xx = d; w = other(kk, xx)
                if E[kk][0] == E[kk][1]: raise ValueError('loop')
                r = rot[w]; pos = [t for t, e in enumerate(r) if e == kk]
                # for a double edge between xx and w, pick the occurrence matching this dart: ambiguous only with loops
                p = pos[0] if len(pos) == 1 else pos[0]
                nk = r[(p - 1) % len(r)]       # clockwise successor at w -> faces on the left
                d = (nk, w)
            F.append(face)
    return F

def main():
    nmax = int(sys.argv[1]); st = Counter(); bad = []
    for N in range(3, nmax + 1, 2):
        U = list(range(1, N + 1))
        for mask in range(1 << N):
            I = [u for u in U if mask >> (u - 1) & 1]; O = [u for u in U if not mask >> (u - 1) & 1]
            if (len(I) + 1) % 2 or len(O) % 2: continue
            for mi in C.ncm(I + ['e3']):
                for mo in C.ncm(O + ['e0', 'e1']):
                    if any(isinstance(a, str) and isinstance(b, str) for a, b in mi + mo): continue
                    Em = [(0, 1, 2, 'e2')] + [(i, i + 1, 3 if i % 2 else 2, None) for i in range(1, N)] + [(N, 0, 3, 'e4')]
                    for a, b in mi + mo:
                        if isinstance(a, str): a, b = b, a
                        Em.append((a, 0, 1, b) if isinstance(b, str) else (a, b, 1, None))
                    res = C.analyse(N, Em)
                    if res is None or not res[0]: continue
                    dl, rigid, img = res
                    E, rot, vlab = instance_graph(N, mi, mo)
                    try:
                        F = faces(E, rot)
                    except ValueError:
                        st['loop'] += 1; continue
                    # Euler check: V - E + F = 2
                    if (N + 1) - len(E) + len(F) != 2: st['euler_fail'] += 1; continue
                    # primal: face index per dart
                    fid = {}
                    for t, f in enumerate(F):
                        for d in f: fid[d] = t
                    adj = {t: [] for t in range(len(F))}; multi = False
                    for k, (a, b, c) in enumerate(E):
                        f1, f2 = fid[(k, a)], fid[(k, b)]
                        if f2 in adj[f1]: multi = True
                        adj[f1].append(f2); adj[f2].append(f1)
                    # colour faces by Z2^2 integration
                    colr = {0: (0, 0)}; stack = [0]; ok = True
                    while stack:
                        f = stack.pop()
                        for k, (a, b, c) in enumerate(E):
                            for (x, y) in ((a, b), (b, a)):
                                if fid[(k, x)] == f:
                                    g = fid[(k, y)]; t = TAIT[c]; cg = (colr[f][0] ^ t[0], colr[f][1] ^ t[1])
                                    if g in colr:
                                        if colr[g] != cg: ok = False
                                    else: colr[g] = cg; stack.append(g)
                    if not ok: st['colour_inconsistent'] += 1; continue
                    if multi: st['multi'] += 1; continue
                    # primal T: add h adjacent to the faces around v in rotation order; link x_t sits between e_{t-1}, e_t
                    nF = len(F); h = nF
                    link = []
                    for t in range(5):
                        ea, eb = vlab['e%d' % ((t - 1) % 5)], vlab['e%d' % t]
                        fa = {fid[(ea, E[ea][0])], fid[(ea, E[ea][1])]}; fb = {fid[(eb, E[eb][0])], fid[(eb, E[eb][1])]}
                        link.append((fa & fb).pop())
                    rotT = [sorted(set(adj[t])) for t in range(nF)] + [link]
                    for x in link: rotT[x] = rotT[x] + [h]
                    H = Hole(rotT, h)
                    cmap = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}
                    colv = {t: cmap[colr[t]] for t in range(nF)}
                    i = H.idx[H.norm(colv)]
                    r, colx = H.analyse_state(i)
                    edl = r['kind'] == 'DL'; erig = edl and counts(H, colx, r['roles']) == [1, 1, 2, 1, 2, 1]
                    st['checked'] += 1
                    if edl != dl or (dl and erig != rigid): st['MISMATCH_state'] += 1; bad.append((N, mi, mo)); continue
                    if dl and r['pi'] is not None:
                        r2, col2 = H.analyse_state(r['pi'])
                        e2dl = r2['kind'] == 'DL'; e2rig = e2dl and counts(H, col2, r2['roles']) == [1, 1, 2, 1, 2, 1]
                        if rigid:
                            st['rigid_checked'] += 1
                            if e2dl != img[1] or (e2rig != (img[0] and img[1])): st['MISMATCH_image'] += 1; bad.append((N, mi, mo))
    print(dict(st), bad[:3])

if __name__ == '__main__':
    main()
