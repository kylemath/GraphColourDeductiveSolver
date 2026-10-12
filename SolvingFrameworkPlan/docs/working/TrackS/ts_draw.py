#!/usr/bin/env python3
"""Track S: draw the longest R-run at a hole (Tutte embedding, link pentagon outside = h at infinity).
Per state: vertex roles (alpha black, mu red, A green, B blue), H (orange: dual of P1-crossing edges),
X (blue) and Y (magenta) = the two loops of Q_t = F13 (dual of P2-crossing edges).  Big ring = K_t (swap set).
usage: ts_draw.py GRAPHFILE name:hole out.png"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ts_lib import load_graphs, HoleData, Geo, runs, pair_components

ROLEC = {'a': 'black', 'm': 'red', 'A': 'green', 'B': 'blue'}


def tutte(rot, h):
    n = len(rot); X = list(rot[h]); P = {}
    for k, x in enumerate(X):
        ang = np.pi / 2 - 2 * np.pi * k / 5
        P[x] = (np.cos(ang), np.sin(ang))
    inner = [v for v in range(n) if v != h and v not in P]
    idx = {v: i for i, v in enumerate(inner)}
    A = np.zeros((len(inner), len(inner))); b = np.zeros((len(inner), 2))
    for v in inner:
        i = idx[v]; nb = rot[v]; A[i, i] = len(nb)
        for w in nb:
            if w in idx: A[i, idx[w]] -= 1
            else: b[i] += P[w]
    sol = np.linalg.solve(A, b)
    for v in inner: P[v] = tuple(sol[idx[v]])
    return P


def draw_state(ax, hd, geo, P, i, title):
    r = hd.info[i]; col = hd.col[i]; al, mu, A, B = r['roles']; x = r['x']
    role = {al: 'a', mu: 'm', A: 'A', B: 'B'}
    rot = hd.rot; h = hd.h
    KA = hd.Hh.comp(col, x[2], (al, A))
    # faces (triangles) not containing h: centroid
    cen = {}
    for f, tri in enumerate(geo.faces):
        if h in tri: continue
        cen[f] = tuple(np.mean([P[v] for v in tri], axis=0))
    for a in range(len(rot)):
        if a == h: continue
        for b in rot[a]:
            if b == h or b < a: continue
            ax.plot([P[a][0], P[b][0]], [P[a][1], P[b][1]], color='0.85', lw=0.5, zorder=1)
            ca, cb = role[col[a]], role[col[b]]
            s = {ca, cb}
            p1 = not (s <= {'a', 'm'} or s <= {'A', 'B'})       # crosses P1 -> H edge
            p2 = not (s <= {'a', 'A'} or s <= {'m', 'B'})       # crosses P2 -> F13 edge
            f1 = geo.dface[(a, b)]; f2 = geo.dface[(b, a)]
            pts = []
            for f in (f1, f2):
                if f in cen: pts.append(cen[f])
                else:
                    m = ((P[a][0] + P[b][0]) / 2 * 1.15, (P[a][1] + P[b][1]) / 2 * 1.15); pts.append(m)
            if p1:
                ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color='orange', lw=2.2, zorder=2)
            if p2:
                ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color='purple', lw=1.0, zorder=3, ls='--')
    for v in range(len(rot)):
        if v == h: continue
        ax.scatter([P[v][0]], [P[v][1]], s=28 if v not in KA else 70, c=ROLEC[role[col[v]]],
                   edgecolors='gold' if v in KA else 'none', linewidths=2, zorder=4)
    for k in range(5):
        ax.text(P[x[k]][0] * 1.12, P[x[k]][1] * 1.12, 'x%d' % k, fontsize=7, ha='center')
    ax.set_title(title, fontsize=8); ax.set_aspect('equal'); ax.axis('off')


def main():
    G = load_graphs(sys.argv[1]); nm, h = sys.argv[2].rsplit(':', 1); h = int(h)
    rot = G[nm]; hd = HoleData(rot, h); geo = Geo(rot, h); P = tutte(rot, h)
    rs = sorted(runs(hd), key=lambda z: -len(z[0]))
    run = rs[0][0]
    pre = [k for k in range(hd.S) if hd.info[k].get('pi') == run[0]]
    seq = run
    n = len(seq); cols = min(4, n); rows = (n + cols - 1) // cols
    fig, axs = plt.subplots(rows, cols, figsize=(4.2 * cols, 4.4 * rows))
    axs = np.array(axs).reshape(-1)
    for k, i in enumerate(seq):
        r = hd.info[i]
        draw_state(axs[k], hd, geo, P, i, 't=%d N=%d j=%d %s' % (k, r['N'], r['j'], 'rigid' if hd.rigid(i) else ('inshape' if hd.inshape(i) else '')))
    for k in range(n, len(axs)): axs[k].axis('off')
    plt.tight_layout(); plt.savefig(sys.argv[3], dpi=110)
    print('run length', n, [hd.info[i]['N'] for i in seq])


if __name__ == '__main__':
    main()
