"""Independent check: each SOL line / window JSON graph is planar with the rotation at v (ax_lib.planar_rot,
5-wheel gadget + networkx), and its orbit data are re-derived by ax_lib.G5."""
import sys, json
sys.path.insert(0, '..')
from ax_lib import G5, parse_line, planar_rot
for path in sys.argv[1:]:
    for l in open(path):
        if l.startswith('SOL'):
            line = l.split(' ', 1)[1].split('{')[0]
            g = G5(*parse_line(line)); print(path, 'SOL planar_rot', planar_rot(g))
        elif l.startswith('{') and '"chords"' in l:
            d = json.loads(l); n = d['n']
            E = [(i, (i + 1) % n) for i in range(n)] + [tuple(c) for c in d['chords']]
            idx = {tuple(sorted(e)): i for i, e in enumerate(E)}
            fv = [idx[tuple(sorted(e))] for e in d['fv']]
            g = G5(n, E, fv); print(path, 'WIN planar_rot', planar_rot(g))
