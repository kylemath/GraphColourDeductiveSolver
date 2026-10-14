"""Shared drawing helpers: game maps (~/4square layout cells) coloured by curvature, with distance shells."""
import json, os, collections, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
G4 = os.path.expanduser('~/4square/')
def _js(fn):
    s = open(G4 + fn).read(); return json.loads(s[s.index('{'):].rstrip().rstrip(';'))
LAYOUT = _js('layout.js'); GAME = _js('levels.js')['graphs']
KCOL = {1: '#e0533f', 0: '#ffffff', -1: '#9ecae1', -2: '#4a90c8', -3: '#1f5fa0', -4: '#0b3a6e'}
def kcol(k): return KCOL.get(max(-4, min(1, k)))
def load(key):
    m = json.load(open(G4 + 'maps/%s.json' % key)); L = LAYOUT[key]
    return m['rot'], L
def bfs(rot, h):
    n = len(rot); d = [-1] * n; d[h] = 0; q = collections.deque([h])
    while q:
        u = q.popleft()
        for w in rot[u]:
            if d[w] < 0: d[w] = d[u] + 1; q.append(w)
    return d
def label_point(L, v):
    if v not in L.get('border', []): return L['centre'][v]
    P = L['cells'][v]; best = None
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        on = (abs(a[0]) > .99 and abs(b[0]) > .99 and a[0] * b[0] > 0) or (abs(a[1]) > .99 and abs(b[1]) > .99 and a[1] * b[1] > 0)
        ln = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** .5
        if on and (best is None or ln > best[0]): best = (ln, ((a[0] + b[0]) / 2 * .93, (a[1] + b[1]) / 2 * .93))
    return best[1] if best else L['centre'][v]
def draw_map(ax, key, hole, title=None, fill=None, labels='curv', shells=True, alpha=1.0):
    rot, L = load(key); n = len(rot); deg = [len(r) for r in rot]; d = bfs(rot, hole)
    for v in range(n):
        fc = fill[v] if fill is not None else kcol(6 - deg[v])
        if v == hole: fc = '#222222'
        ax.add_patch(Polygon(L['cells'][v], closed=True, fc=fc, ec='#bbbbbb', lw=0.5, alpha=alpha))
    if shells:
        for s in L['sides']:
            u, v, p, q = s[0], s[1], s[2], s[3]
            if d[u] != d[v]:
                ax.plot([p[0], q[0]], [p[1], q[1]], color='#333333', lw=2.2, solid_capstyle='round', zorder=3)
    for v in range(n):
        x, y = label_point(L, v)
        if v == hole:
            ax.text(x, y, 'HOLE', ha='center', va='center', color='white', fontsize=7, fontweight='bold', zorder=5); continue
        k = 6 - deg[v]
        if labels == 'curv':
            if k != 0: ax.text(x, y + 0.03, '%+d' % k, ha='center', va='center', fontsize=8, fontweight='bold', color='#111', zorder=5)
            ax.text(x, y - 0.06, str(d[v]), ha='center', va='center', fontsize=6, color='#666', zorder=5)
        elif labels == 'deg':
            ax.text(x, y, str(deg[v]), ha='center', va='center', fontsize=8, color='#111', zorder=5)
    ax.set_xlim(-1.02, 1.02); ax.set_ylim(-1.02, 1.02); ax.set_aspect('equal'); ax.axis('off')
    if title: ax.set_title(title, fontsize=9, loc='left')
    return rot, L, d
def legend(fig, y=0.02, shells=True):
    from matplotlib.patches import Patch
    h = [Patch(fc=KCOL[1], ec='#999', label='+1: 5 neighbours (pentagon)'), Patch(fc=KCOL[0], ec='#999', label='0: 6 neighbours (flat)'),
         Patch(fc=KCOL[-1], ec='#999', label='-1: 7 neighbours'), Patch(fc=KCOL[-2], ec='#999', label='-2: 8'), Patch(fc=KCOL[-3], ec='#999', label='-3: 9'),
         Patch(fc='#222', label='the hole')] + ([plt.Line2D([], [], color='#333', lw=2.2, label='shell boundary (grey number = steps from hole)')] if shells else [])
    fig.legend(handles=h, loc='lower center', ncol=4, fontsize=8, frameon=False, bbox_to_anchor=(0.5, y))
