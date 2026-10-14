"""Figure (c): what curvature is. Angle defect at a vertex; the same map as a triangulation (curvature at points)
and as the game's region / Gears map (curvature on faces: pentagons +, heptagons -)."""
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Wedge
from draw import *
KEY = 'six'; g = GAME[KEY]; rot, L = load(KEY); n = len(rot); deg = [len(r) for r in rot]; hole = g['hole']
fig = plt.figure(figsize=(14, 9.2))
# row 1: angle defect fans
for j, (k, title) in enumerate([(5, '5 triangles: a 60° gap;\nclose it -> a cone\ncurvature +60° = "+1"\n(a pentagon region)'),
                                 (6, '6 triangles: exactly 360°\nlies flat\ncurvature 0\n(a hexagon region)'),
                                 (7, '7 triangles: 60° too much\n-> buckles into a saddle\ncurvature -60° = "-1"\n(a heptagon region)')]):
    ax = fig.add_axes([0.02 + j * 0.135, 0.66, 0.12, 0.26]); ax.set_aspect('equal'); ax.axis('off')
    col = kcol(6 - k)
    for i in range(k):
        a0 = i * 60 + 90; a1 = a0 + 60
        if a1 > 450: a1 = 450
        pts = [(0, 0), (np.cos(np.radians(a0)), np.sin(np.radians(a0))), (np.cos(np.radians(a0 + 60)), np.sin(np.radians(a0 + 60)))]
        if i < 6: ax.add_patch(Polygon(pts, fc=col, ec='k', lw=1))
        else: ax.add_patch(Polygon([(0, 0), (1.15 * pts[1][0], 1.15 * pts[1][1]), (1.15 * pts[2][0], 1.15 * pts[2][1])], fc='none', ec='#c0392b', lw=1.5, hatch='///'))
    if k == 5:
        ax.add_patch(Wedge((0, 0), 0.6, 390, 450, fc='none', ec='k', ls='--')); ax.text(0.2, 0.75, 'gap', fontsize=8)
    if k == 7:
        ax.text(-0.15, 1.12, 'overlap', fontsize=8)
    ax.plot([0], [0], 'ko', ms=4); ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.35)
    ax.text(0, -1.3, title, fontsize=8, ha='center', va='top')
axt = fig.add_axes([0.42, 0.62, 0.56, 0.3]); axt.axis('off')
axt.text(0, 1, 'What "curvature" means here', fontsize=13, fontweight='bold', va='top')
axt.text(0, 0.82, (
    '- Glue equilateral triangles edge to edge. Around a point with 6 triangles the paper lies flat.\n'
    '  With 5 it must bend into a cone (like the tip of a football); with 7 it must buckle into a saddle.\n'
    '- The curvature at a point is the missing (or excess) angle: K = 60° x (6 - degree). It lives at points,\n'
    '  is a 2-D, intrinsic quantity (an ant on the surface can measure it), and needs no embedding in 3-D.\n'
    '- Gauss-Bonnet: on any closed sphere the curvature adds up to 720°, i.e. sum of (6 - degree) = 12.\n'
    '  So every map has "12 units" of net positive charge; degree-7+ vertices are negative charges.\n'
    '- In the game\'s region picture (right) a vertex is a region and its degree is the number of neighbours:\n'
    '  the curvature sits on the faces of the Gears/Tait map: pentagons +1, hexagons 0, heptagons -1, octagons -2.'),
    fontsize=9.5, va='top', family='DejaVu Sans')
# row 2 left: triangulation with curvature at points
ax = fig.add_axes([0.02, 0.03, 0.47, 0.56]); ax.set_aspect('equal'); ax.axis('off')
pos = np.array(g['pos'])
for u, v in g['edges']:
    ax.plot(*pos[[u, v]].T, color='#888', lw=0.8, zorder=1)
for v in range(n):
    k = 6 - deg[v]; c = '#222' if v == hole else kcol(k)
    ax.scatter(*pos[v], s=260, color=c, ec='k', zorder=3)
    ax.text(*pos[v], 'H' if v == hole else ('%+d' % k if k else '0'), ha='center', va='center', fontsize=7, color='white' if v == hole or k <= -2 else 'k', zorder=4)
ax.set_title('Triangulation view: regions are dots, neighbours are joined;\ncurvature (6 - degree) sits on the dots', fontsize=10, loc='left')
# row 2 right: region / Gears view
ax = fig.add_axes([0.51, 0.03, 0.47, 0.56])
draw_map(ax, KEY, hole, None, labels='deg', shells=False)
# junction dots: cell corners shared by 3 cells
from collections import Counter
cnt = Counter((round(p[0], 3), round(p[1], 3)) for c in L['cells'] for p in c)
J = np.array([p for p, c in cnt.items() if c >= 3]); ax.scatter(J[:, 0], J[:, 1], s=9, color='k', zorder=6)
ax.set_title('Region (Gears / Tait) view of the same map: every corner is a 3-way junction;\nthe number in a region = its sides; pentagons carry +1, heptagons -1, octagons -2', fontsize=10, loc='left')
legend(fig, y=0.0, shells=False)
fig.suptitle('Map "six" (order 28, a 66666 hole):  15 pentagons (+15), 1 heptagon (-1), 1 octagon (-2): total +12', fontsize=12, y=0.995)
fig.savefig('../figs/c_curvature_explained.png', dpi=140); fig.savefig('../figs/c_curvature_explained.svg')
print('ok')
