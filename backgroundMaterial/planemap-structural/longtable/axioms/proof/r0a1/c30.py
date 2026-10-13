"""PM digraph D on the planar C30#0 graphs (TrackU seed_c30.txt) and on any graph line file.
usage: c30.py [file]"""
import sys, collections
from r0lib import G5, analyse
TU = '/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/TrackU/out/seed_c30.txt'

def from_line(line):
    t = list(map(int, line.split())); n, m = t[0], t[1]
    E = [(t[2 + 2 * i], t[3 + 2 * i]) for i in range(m)]
    fv = t[2 + 2 * m: 7 + 2 * m]
    a, b = E[fv[0]]; c, d = E[fv[1]]; v = a if a in (c, d) else b
    perm = {x: x for x in range(n)}; perm[v] = 0; perm[0] = v
    return G5(n, [(perm[a], perm[b]) for a, b in E], fv)

if __name__ == '__main__':
    for i, line in enumerate(open(sys.argv[1] if len(sys.argv) > 1 else TU)):
        if not line.strip(): continue
        g = from_line(line)
        A = analyse(g)
        print(f'line {i}: n={g.n} planar_rot={g.planar_rot()} #PM={len(A["P"])} #arcs={len(A["arcs"])} '
              f'#Ham arcs={len(A["ham"])} cyclic SCC sizes={sorted(len(c) for c in A["cyc"])} '
              f'Ham arcs inside an SCC={len(A["bad"])}')
        # where are the Ham arcs relative to the cyclic SCCs?
        cyc = set().union(*A['cyc']) if A['cyc'] else set()
        print('   Ham arcs with tail in a cyclic SCC:', sum(1 for i_, j in A['ham'] if i_ in cyc),
              ' head in a cyclic SCC:', sum(1 for i_, j in A['ham'] if j in cyc))
