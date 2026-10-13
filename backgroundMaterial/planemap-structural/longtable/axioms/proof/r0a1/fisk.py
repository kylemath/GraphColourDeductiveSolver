"""Coordinator lead (r0surfaces): Fisk degree of the face 4-colouring along R0 steps.
For an arc state (A, B) of D (A = M_t, B = M_{t+1}, R = rest), colour edges A -> 1, B -> 2, R -> 3 (Klein group
{0,1,2,3}, XOR) and lift to a face 4-colouring c of G (faces of G = vertices of T - x), normalised by
c(x_{k+1}) = 0 where x_i is the face in the corner (f_{i-1}, f_i) at v and k = k(A).  For a cubic w with faces
p, q, r in ccw order: missing colour m = p^q^r; sign eps = +1 iff (p, q, r) is positively oriented as a face of
the boundary of [0,1,2,3].  deg_m = sum of eps over w with m(w) = m (Fisk degree w.r.t. the triple {0,1,2,3}-m).
[hand] eps(w) = sigma(w) (Tait sign of (A, B, R)), so sum_m deg_m = S of Lemma K.
Prints deg vectors along the C30#0 cycle and along every maximal walk of the planar census at small n.
usage: fisk.py c30 | fisk.py n"""
import sys, json, collections
import networkx as nx
from r0lib import G5, analyse

POS = {frozenset({1, 2, 3}): (1, 2, 3), frozenset({0, 2, 3}): (0, 3, 2), frozenset({0, 1, 3}): (0, 1, 3), frozenset({0, 1, 2}): (0, 2, 1)}

def embed(g):
    gg = g.gadget(); ok, emb = nx.check_planarity(gg); assert ok
    base = g.n
    rim = [u - base for u in emb.neighbors_cw_order(base + 5)]
    i0 = rim.index(0); cwr = rim[i0:] + rim[:i0]
    flip = cwr[1] == 1                         # make f0..f4 ccw at v
    def eid(w, u):
        return g.fv[u - base] if u >= base else next(e for e in g.inc[w] if g.other(e, w) == u)
    ccw = {}
    for w in range(1, g.n):
        r = [eid(w, u) for u in emb.neighbors_cw_order(w)]
        ccw[w] = r if flip else r[::-1]
    ccw[0] = list(g.fv)                        # ccw at v by convention
    return ccw

def faces(g, ccw):
    """faces as lists of (vertex, incoming edge, outgoing edge) corners; face to the left of each dart"""
    pos = {w: {e: i for i, e in enumerate(ccw[w])} for w in ccw}
    seen = set(); F = []; corner_face = {}
    for e in range(g.m):
        for (a, b) in (g.E[e], g.E[e][::-1]):
            if (e, a) in seen: continue
            face = []; cur_e, cur_a = e, a
            while (cur_e, cur_a) not in seen:
                seen.add((cur_e, cur_a)); w = g.other(cur_e, cur_a)
                # next edge around w: clockwise from the incoming edge keeps the face on the left
                d = len(ccw[w]); nxt = ccw[w][(pos[w][cur_e] - 1) % d]
                face.append((w, cur_e, nxt)); corner_face[(w, cur_e, nxt)] = len(F)
                cur_e, cur_a = nxt, w
            F.append(face)
    return F, corner_face

def colouring(g, ccw, F, cf, A, B):
    col = [1 if A >> e & 1 else 2 if B >> e & 1 else 3 for e in range(g.m)]
    # dual adjacency: the face left of dart (e, a->b) and the face left of (e, b->a)
    left = {}
    for fi, face in enumerate(F):
        for (w, ein, eout) in face: left[(ein, w)] = fi    # dart ein arriving at w
    c = {0: 0}; st = [0]; ok = True
    adj = collections.defaultdict(list)
    for e, (a, b) in enumerate(g.E):
        f1, f2 = left[(e, b)], left[(e, a)]
        adj[f1].append((f2, col[e])); adj[f2].append((f1, col[e]))
    while st:
        f = st.pop()
        for f2, x in adj[f]:
            if f2 not in c: c[f2] = c[f] ^ x; st.append(f2)
            elif c[f2] != c[f] ^ x: ok = False
    return c, ok

def degvec(g, ccw, F, cf, A, B):
    c, ok = colouring(g, ccw, F, cf, A, B)
    k = g.k(A)
    # corner faces at v: corner (f_{i-1}, f_i) = the face containing the v-corner entered by f_{i-1}... find by search
    xs = {}
    for fi, face in enumerate(F):
        for (w, ein, eout) in face:
            if w == 0:
                i_in, i_out = g.fidx[ein], g.fidx[eout]
                xs[(i_in, i_out)] = fi
    # corner between consecutive v-edges: the pair (in, out) differs by one step
    x = {}
    for (a, b), fi in xs.items():
        lo = a if (b - a) % 5 == 1 else b
        x[(lo + 1) % 5] = fi                      # x_i between f_{i-1} and f_i
    shift = c[x[(k + 1) % 5]]
    cc = {f: v ^ shift for f, v in c.items()}
    deg = [0, 0, 0, 0]
    for w in range(1, g.n):
        fs = []
        for i in range(3):
            ein = ccw[w][i]; eout = ccw[w][(i - 1) % 3]
            fs.append(cc[cf[(w, ein, eout)]])
        p, q, r = fs[::-1] if False else fs
        m = p ^ q ^ r
        o = POS[frozenset({0, 1, 2, 3}) - {m}]
        # is (p, q, r) a cyclic rotation of o (or of its reverse)?
        rot = [o, o[1:] + o[:1], o[2:] + o[:2]]
        eps = 1 if (p, q, r) in [tuple(t) for t in rot] else -1
        deg[m] += eps
    link = [cc[x[i]] for i in range(5)]
    return tuple(deg), link, ok

if __name__ == '__main__':
    if sys.argv[1] == 'c30':
        from c30 import from_line, TU
        g = from_line(open(TU).readline()); A_ = analyse(g); ccw = embed(g); F, cf = faces(g, ccw)
        C = A_['cyc'][0]; D = A_['D'].subgraph(C); cyc = [min(C)]
        while True:
            nx_ = next(iter(D.successors(cyc[-1])))
            if nx_ == cyc[0]: break
            cyc.append(nx_)
        P = A_['P']; L = len(cyc)
        print('C30#0: #faces', len(F), 'Euler', g.n - g.m + len(F))
        for t in range(L):
            d, link, ok = degvec(g, ccw, F, cf, P[cyc[t]], P[cyc[(t + 1) % L]])
            print(f'  t={t:2d} k={A_["ks"][cyc[t]]} deg(m=0..3)={d} sum={sum(d)} link={link} lift={ok}')
    else:
        n = int(sys.argv[1]); cnt = collections.Counter(); steps = collections.Counter()
        for l in open(f'out/census_n{n}_p.jsonl'):
            r = json.loads(l); g = G5(r['n'], [tuple(e) for e in r['edges']], r['fv'])
            A_ = analyse(g); ccw = embed(g); F, cf = faces(g, ccw); P = A_['P']
            dv = {}
            for (i, j) in A_['arcs']:
                d, link, ok = degvec(g, ccw, F, cf, P[i], P[j]); assert ok
                dv[(i, j)] = d; cnt[(d, (i, j) in A_['ham'])] += 1
            for (i, j) in A_['arcs']:
                for j2 in A_['D'].successors(j):
                    d1, d2 = dv[(i, j)], dv[(j, j2)]
                    steps[(d1, d2)] += 1
        print(f'n={n}: deg vectors (deg_0..deg_3, Ham arc?) counts:')
        for k_, v in sorted(cnt.items(), key=lambda z: -z[1])[:25]: print('   ', k_, v)
        print('  step transitions (deg before -> after) counts:')
        for k_, v in sorted(steps.items(), key=lambda z: -z[1])[:25]: print('   ', k_, v)
