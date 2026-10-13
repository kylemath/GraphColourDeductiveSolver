"""Total Tait sign S(M,M') = sum over cubic w of sigma(w), sigma = +1 iff (M, M', R) is ccw at w (planar
embedding from the gadget, oriented so that f0..f4 is ccw at v), for every arc of D.  Prints the
distribution of S for Ham arcs / other arcs, and per step along the C30#0 orbit.  usage: sigsum.py n | c30"""
import sys, json, collections
import networkx as nx
from r0lib import G5, analyse

def ccw_rot(g):
    gg = g.gadget(); ok, emb = nx.check_planarity(gg); assert ok
    base = g.n
    rim = [u - base for u in emb.neighbors_cw_order(base + 5)]
    # make f0..f4 ccw at v: cw rim order must be decreasing
    i0 = rim.index(0); cw = rim[i0:] + rim[:i0]
    flip = cw[1] == 1    # cw order 0,1,2.. means f increases clockwise -> mirror
    def edge_to(w, u):
        return g.fv[u - base] if u >= base else next(e for e in g.inc[w] if g.other(e, w) == u)
    rot = {}
    for w in range(1, g.n):
        r = [edge_to(w, u) for u in emb.neighbors_cw_order(w)]   # cw
        rot[w] = r if flip else r[::-1]                              # -> ccw (after mirror if needed)
    return rot

def S(g, rot, M, Mp):
    tot = 0
    for w in range(1, g.n):
        a = next(e for e in g.inc[w] if M >> e & 1); b = next(e for e in g.inc[w] if Mp >> e & 1)
        r = rot[w]; tot += 1 if (r.index(b) - r.index(a)) % 3 == 1 else -1
    return tot

if __name__ == '__main__':
    if sys.argv[1] == 'c30':
        from c30 import from_line, TU
        for line in open(TU):
            if not line.strip(): continue
            g = from_line(line); A = analyse(g); rot = ccw_rot(g)
            C = A['cyc'][0]; D = A['D'].subgraph(C); cyc = [min(C)]
            while True:
                nx_ = next(iter(D.successors(cyc[-1])))
                if nx_ == cyc[0]: break
                cyc.append(nx_)
            print('C30#0 per-step S:', [S(g, rot, A['P'][cyc[t]], A['P'][cyc[(t + 1) % len(cyc)]]) for t in range(len(cyc))])
        sys.exit()
    n = int(sys.argv[1]); hh = collections.Counter(); ho = collections.Counter()
    for l in open(f'out/census_n{n}_p.jsonl'):
        r = json.loads(l); g = G5(r['n'], [tuple(e) for e in r['edges']], r['fv'])
        A = analyse(g); rot = ccw_rot(g)
        for (i, j) in A['arcs']:
            s = S(g, rot, A['P'][i], A['P'][j])
            (hh if (i, j) in A['ham'] else ho)[s] += 1
    print(f'n={n}: S on Ham arcs', dict(sorted(hh.items())), '| S on other arcs', dict(sorted(ho.items())))
