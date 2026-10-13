#!/usr/bin/env python3
"""SCOPE-A5v (Long Table, 13 Oct 2026): A5v in primal language and its Tait cross-check.

Primal setting: graph G with hole h (degree 5, link x_0..x_4 = adj[h] in cyclic order); states = proper
4-colourings of G - h up to renaming (TrackH th_engine, read-only).  At a DL state c with frame j, roles
(alpha, mu, A, B) at x_j..x_{j+4}:
    K  = K_{alphaA}(x_{j+2})   (the component pi swaps; contains x_{j+3})
    K0 = K_{alphaA}(x_j)
    J  = K_{muB}(x_{j+1})      (the Lock-2 chain; contains x_{j+4} at a DL state)
    T  = { w != h : w adjacent to x_{j+2} and x_{j+3} }  (triangles across the link edge x_{j+2}x_{j+3},
         i.e. the primal picture of the far end of v's M-edge f_{j+2})
A5v-P (weak)   : every w in T gives two cross edges x_{j+2}w, x_{j+3}w in delta(K) and not in delta(K0)
                 [<=> not inA, whenever T is nonempty]
A5v-P (strong) : every w in T lies in J
A5v-P (switch) : pi switches the Tait colours of x_{j+2}w and x_{j+3}w (always true when K != K0)

Tait cross-check (only when G - h is a triangulated surface given by rotations): build the dual with
TrackT tt_lib.tait_dual, colour dual edges by c(u) xor c(w), M = colour alpha^A, and compute
  ax_lib's A5v (connected figure-eight case, independent engine), and the generalised location of the
  far end p of f_k in Q = E - M: 'X' (v-loop through f_{k+-1}), 'Y' (v-loop through f_{k+-2}), 'Z' (a cycle
  of Q not through v); plus switch(p) := (M_{t+1} edge at p == M_{t-1} edge at p), with M_{t-1} = colour
  alpha^B of c and M_{t+1} = colour alpha^mu of pi(c) (TrackS S1).
"""
import sys, os, json, gzip
from collections import Counter, defaultdict
W = os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working')
AX = os.path.expanduser('~/GraphColour/backgroundMaterial/planemap-structural/longtable/axioms')
sys.path.insert(0, W + '/TrackH'); sys.path.insert(0, W + '/TrackT'); sys.path.insert(0, AX)
import th_engine
import tt_lib
from ax_lib import G5 as AxG5, fig8_axioms

PAIRS = th_engine.PAIRS


def parse_graph_line(line):
    p = line.split()
    return p[0], [list(map(int, r.split(','))) for r in p[2].split(';')]


def nchains(H, col):
    n = 0
    for (p, q) in PAIRS:
        left = {v for v in H.V if col[v] in (p, q)}
        while left:
            s = next(iter(left)); left -= H.comp(col, s, (p, q)); n += 1
    return n


def ncomp_pair(H, col, p, q):
    n = 0; left = {v for v in H.V if col[v] in (p, q)}
    while left:
        s = next(iter(left)); left -= H.comp(col, s, (p, q)); n += 1
    return n


class TaitSide:
    """Tait dual of a triangulated surface (rotation system), hole h."""
    def __init__(self, rot, h):
        self.td = tt_lib.tait_dual(rot, h)
        td = self.td
        self.n = td.n; self.E = list(td.E); self.fv = list(td.fv)
        self.inc = [[] for _ in range(self.n)]
        for e, (a, b) in enumerate(self.E):
            self.inc[a].append(e); self.inc[b].append(e)
        self.ax = AxG5(self.n, self.E, self.fv)

    def other(self, e, x):
        a, b = self.E[e]; return b if a == x else a

    def colours(self, col):
        return [col[u] ^ col[w] for (u, w) in self.td.prim]

    def locate(self, colr, c2, k):
        """Q = edges with colour != c2.  Returns (pairing_ok, loc(p), qconn, loops)"""
        inQ = [c != c2 for c in colr]
        v = 0
        loops = {}
        seen = set()
        for s in range(5):
            f = self.fv[s]
            if not inQ[f] or f in seen: continue
            x = self.other(f, v); e = f; verts = []; seen.add(f)
            while x != v:
                verts.append(x)
                nxt = [g for g in self.inc[x] if inQ[g] and g != e]
                assert len(nxt) == 1, 'Q not 2-regular at a cubic vertex'
                e = nxt[0]; seen.add(e); x = self.other(e, x)
            t = self.fv.index(e)
            loops[frozenset({s, t})] = verts
        kX = frozenset({(k - 1) % 5, (k + 1) % 5}); kY = frozenset({(k + 2) % 5, (k - 2) % 5})
        if kX not in loops or kY not in loops:
            return False, None, None, loops
        p = self.other(self.fv[k], v)
        loc = 'X' if p in set(loops[kX]) else ('Y' if p in set(loops[kY]) else 'Z')
        nQv = 1 + len(loops[kX]) + len(loops[kY])
        qconn = (nQv == self.n)
        return True, loc, qconn, loops

    def pedges(self, p, colr, c):
        return [e for e in self.inc[p] if colr[e] == c]


def analyse_hole(rot, h, tait=False, which='dl', want_class=False, maxstates=400000):
    """which: 'dl' all DL states; 'cyc' only states on all-DL pi-cycles."""
    H = th_engine.Hole(rot, h)
    S = len(H.states)
    if S > maxstates: return None
    info = [None] * S
    for i in range(S):
        info[i] = H.analyse_state(i)[0]
    # all-DL cycles
    on = {}; cycs = []
    for i in range(S):
        if info[i]['kind'] != 'DL' or i in on: continue
        path = []; posd = {}; k = i
        while k is not None and info[k]['kind'] == 'DL' and k not in posd and k not in on:
            posd[k] = len(path); path.append(k); k = info[k]['pi']
        if k is not None and k in posd:
            c = path[posd[k]:]
            for t, s in enumerate(c): on[s] = (len(cycs), t)
            cycs.append(c)
    TS = TaitSide(rot, h) if tait else None
    recs = []
    targets = [i for i in range(S) if info[i]['kind'] == 'DL' and (which == 'dl' or i in on)]
    for i in targets:
        r = info[i]; col = H.col(i)
        j = r['j']; x = [H.X[(j + t) % 5] for t in range(5)]
        al, mu, A, B = r['roles']
        K = H.comp(col, x[2], (al, A)); K0 = H.comp(col, x[0], (al, A)); J = H.comp(col, x[1], (mu, B))
        T = [w for w in H.adj[x[2]] if w in set(H.adj[x[3]])]
        weak = all((w not in K) and (w not in K0) and (x[2] not in K0) and (x[3] not in K0) for w in T)
        strong = all(w in J for w in T)
        rec = dict(i=i, j=j, inA=r['inA'], L2=r['L2'], D1=r['D1'], D2=r['D2'], ntri=len(T),
                   weak=weak, strong=strong, wcols=sorted(col[w] == mu for w in T),
                   N=nchains(H, col), P2=(ncomp_pair(H, col, al, A), ncomp_pair(H, col, mu, B)),
                   cyc=on.get(i), pi=r['pi'], oA=r['oA'] % 2, oB=r['oB'] % 2, oM=r['oM'] % 2)
        if TS is not None:
            colr = TS.colours(col)
            c2 = al ^ A; c3 = al ^ B; c1 = al ^ mu
            k = (j + 2) % 5
            assert colr[TS.fv[k]] == c2
            ok, loc, qconn, loops = TS.locate(colr, c2, k)
            rec['t_pair'] = ok; rec['t_loc'] = loc; rec['t_qconn'] = qconn
            M = frozenset(e for e in range(len(colr)) if colr[e] == c2)
            d = TS.ax.dl(M)
            rec['ax_dlgood'] = d is not None
            if d is not None:
                rec['ax_A5v'] = fig8_axioms(TS.ax, M, d)['v_into_X']
            if r['pi'] is not None:
                p = TS.other(TS.fv[k], 0)
                colp = H.col(r['pi'])  # normalised colouring of pi(c): recompute roles there
                # M_{t+1} = colour-2 class of pi(c) in pi(c)'s own frame
                ri = info[r['pi']]
                if ri['kind'] in ('DL', 'S', 'N') and 'roles' in ri:
                    a2, m2, A2, B2 = ri['roles']
                    colr2 = TS.colours(colp)
                    mprev = TS.pedges(p, colr, c3)
                    mnext = TS.pedges(p, colr2, a2 ^ A2)
                    rec['t_switch'] = (mprev == mnext)
        recs.append(rec)
    out = dict(S=S, ndl=sum(1 for r in info if r['kind'] == 'DL'), cycles=[len(c) for c in cycs], recs=recs)
    if want_class and cycs:
        H.build()
        cls = {}
        for ci, c in enumerate(cycs):
            mem = H.class_members(c[0])
            cls[ci] = dict(size=len(mem), filled=sum(1 for m in mem if info[m]['kind'] == 'F'),
                           ondl=sum(1 for m in mem if m in on))
        out['classes'] = cls
    return out


def summarise(tag, res, law=True):
    C = Counter()
    for r in res['recs']:
        C['states'] += 1
        C['ntri=%d' % r['ntri']] += 1
        C['weak_ok' if r['weak'] else 'weak_FAIL'] += 1
        C['strong_ok' if r['strong'] else 'strong_FAIL'] += 1
        C['inA'] += r['inA']
        C['N>=10'] += r['N'] >= 10
        if 't_loc' in r:
            C['t_loc=%s' % r['t_loc']] += 1
            C['t_qconn'] += bool(r['t_qconn'])
            if 'ax_A5v' in r: C['ax_A5v_ok' if r['ax_A5v'] else 'ax_A5v_FAIL'] += 1
            if 't_switch' in r: C['t_switch_ok' if r['t_switch'] else 't_switch_FAIL'] += 1
            # consistency primal strong <-> tait X ; weak <-> not Y
            C['agree_strongX' if (r['strong'] == (r['t_loc'] == 'X')) else 'DISAGREE_strongX'] += 1
            C['agree_weakNotY' if (r['weak'] == (r['t_loc'] != 'Y')) else 'DISAGREE_weakNotY'] += 1
    return C


def cycle_law(res):
    """law violations along each cycle: N(pi c) - N(c) == 1 mod 2 (both DL)"""
    byi = {r['i']: r for r in res['recs']}
    v = 0; tot = 0
    for r in res['recs']:
        if r['cyc'] is None or r['pi'] is None or r['pi'] not in byi: continue
        tot += 1
        if (byi[r['pi']]['N'] - r['N']) % 2 != 1: v += 1
    return v, tot


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'one':
        path, name, h = sys.argv[2], sys.argv[3], int(sys.argv[4])
        tait = len(sys.argv) > 5 and sys.argv[5] == 'tait'
        for line in open(path):
            if line.split() and line.split()[0] == name:
                nm, rot = parse_graph_line(line)
                res = analyse_hole(rot, h, tait=tait, which='dl', want_class=True)
                print(nm, h, 'S', res['S'], 'DL', res['ndl'], 'cycles', res['cycles'], res.get('classes'))
                print(dict(summarise(nm, res)))
                print('law (viol/steps on cycles):', cycle_law(res))
                break


# ---------------------------------------------------------------------------------------------------
# Surface check over ALL DL-good perfect matchings of the Tait dual (not only integrable ones):
# is every A5v failure explained by (non-integrability) or (inA, i.e. a D2 failure)?
def tait_colouring_from_M(TS, M, d):
    k, L = d
    colr = [1] * len(TS.E)
    for e in M: colr[e] = 2
    for key, start in (('X', (k - 1) % 5), ('Y', (k - 2) % 5)):
        s0, s1, verts, edges = L[key]
        es = edges if s0 == start else edges[::-1]
        for t, e in enumerate(es): colr[e] = 1 if t % 2 == 0 else 3
    return colr


def integrate(TS, colr, rot, h, x0):
    """primal vertex colouring (Z_2^2 as 0..3) with c(x0)=0, or None if the Tait colouring does not integrate"""
    adj = defaultdict(list)
    for e, (u, w) in enumerate(TS.td.prim):
        adj[u].append((w, colr[e])); adj[w].append((u, colr[e]))
    c = {x0: 0}; st = [x0]
    while st:
        u = st.pop()
        for w, cc in adj[u]:
            if w not in c: c[w] = c[u] ^ cc; st.append(w)
            elif c[w] != c[u] ^ cc: return None
    return c


def surface_pm_check(rot, h, C):
    TS = TaitSide(rot, h)
    P = TS.ax.pms(limit=300000)
    X = rot[h]
    V = [v for v in range(len(rot)) if v != h]
    adjp = {v: [w for w in rot[v] if w != h] for v in V}
    def comp(col, s, pair):
        seen = {s}; st = [s]
        while st:
            u = st.pop()
            for w in adjp[u]:
                if w not in seen and col[w] in pair: seen.add(w); st.append(w)
        return seen
    for M in P:
        d = TS.ax.dl(M)
        if d is None: continue
        C['dlgood'] += 1
        a5 = fig8_axioms(TS.ax, M, d)['v_into_X']
        k = d[0]; j = (k - 2) % 5
        colr = tait_colouring_from_M(TS, M, d)
        x = [X[(j + t) % 5] for t in range(5)]
        c = integrate(TS, colr, rot, h, x[0])
        if c is None:
            C['nonint'] += 1; C['nonint_A5v_' + ('ok' if a5 else 'FAIL')] += 1; continue
        al, mu, A, B = c[x[0]], c[x[1]], c[x[3]], c[x[4]]
        assert c[x[2]] == al and len({al, mu, A, B}) == 4
        inA = x[0] in comp(c, x[2], (al, A)); L2 = x[4] in comp(c, x[1], (mu, B))
        L1 = x[3] in comp(c, x[1], (mu, A)); inB = x[0] in comp(c, x[2], (al, B))
        C['int'] += 1
        C['int_inA=%d_L2=%d_A5v=%s' % (inA, L2, 'ok' if a5 else 'FAIL')] += 1
        C['int_DL=%d' % (L1 and L2)] += 1


def iter_graph_file(path):
    for line in open(path):
        if not line.strip(): continue
        if line.lstrip().startswith('{'):
            d = json.loads(line); line = d['graph']
        if len(line.split()) < 3: continue
        yield parse_graph_line(line)


if __name__ == '__main__' and sys.argv[1] == 'surfpm':
    path, stride = sys.argv[2], int(sys.argv[3])
    C = Counter(); ng = 0
    for gi, (nm, rot) in enumerate(iter_graph_file(path)):
        if gi % stride: continue
        ng += 1
        for h in range(len(rot)):
            if len(rot[h]) != 5: continue
            C['holes'] += 1
            try:
                surface_pm_check(rot, h, C)
            except AssertionError as ex:
                C['skip_assert'] += 1
    print('surfpm', path.split('/')[-1], 'graphs', ng, dict(sorted(C.items())))

if __name__ == '__main__' and sys.argv[1] == 'batch':
    path, stride, tait, which = sys.argv[2], int(sys.argv[3]), sys.argv[4] == 'tait', sys.argv[5]
    holes = sys.argv[6] if len(sys.argv) > 6 else 'all'
    C = Counter(); LAW = [0, 0]; ng = 0
    for gi, (nm, rot) in enumerate(iter_graph_file(path)):
        if gi % stride: continue
        ng += 1
        hs = [0] if holes == 'h0' else [h for h in range(len(rot)) if len(rot[h]) == 5]
        for h in hs:
            try:
                res = analyse_hole(rot, h, tait=tait, which=which, maxstates=60000)
            except AssertionError:
                C['skip_assert'] += 1; continue
            if res is None: C['skip_big'] += 1; continue
            C['holes'] += 1; C['cycles'] += len(res['cycles'])
            C.update(summarise(nm, res))
            v, t = cycle_law(res); LAW[0] += v; LAW[1] += t
    print('batch', path.split('/')[-1], 'graphs', ng, 'law viol/steps', LAW, dict(sorted(C.items())))

if __name__ == '__main__' and sys.argv[1] == 'census33':
    gpath, hpath = sys.argv[2], sys.argv[3]
    G = {nm: rot for nm, rot in iter_graph_file(gpath)}
    C = Counter(); LAW = [0, 0]
    for nm, h, dlc, ndlc, w, S in json.load(open(hpath)):
        res = analyse_hole(G[nm], h, tait=True, which='dl', maxstates=10 ** 6)
        s = summarise(nm, res); C.update(s); C['holes'] += 1; C['cycles'] += len(res['cycles'])
        v, t = cycle_law(res); LAW[0] += v; LAW[1] += t
        cyc = [r for r in res['recs'] if r['cyc'] is not None]
        print(nm, h, w, 'S', res['S'], 'cycles', res['cycles'], 'cyc-states', len(cyc),
              'weak', sum(r['weak'] for r in cyc), 'strong', sum(r['strong'] for r in cyc),
              'tX', sum(r.get('t_loc') == 'X' for r in cyc), 'tZ', sum(r.get('t_loc') == 'Z' for r in cyc),
              'tY', sum(r.get('t_loc') == 'Y' for r in cyc), 'Nword', ''.join(str(min(r['N'], 9) if r['N'] < 10 else 'x') for r in sorted(cyc, key=lambda r: r['cyc'][1])), flush=True)
    print('census33 law viol/steps', LAW, dict(sorted(C.items())))


def local_surface_stats(rot, h):
    n = len(rot); adj = [set(r) for r in rot]
    E = {(min(u, w), max(u, w)) for u in range(n) for w in rot[u]}
    Eh = [e for e in E if h not in e]
    tri = defaultdict(int)
    for (u, w) in Eh:
        tri[(u, w)] = sum(1 for z in adj[u] & adj[w] if z != h)
    link = set(rot[h])
    bad_e = sum(1 for e in Eh if tri[e] != (1 if (e[0] in link and e[1] in link and
                                                  (rot[h].index(e[0]) - rot[h].index(e[1])) % 5 in (1, 4)) else 2))
    # vertex links: G[N(u)] is a single cycle?
    bad_v = 0
    for u in range(n):
        Nu = adj[u]
        sub = {z: (adj[z] & Nu) for z in Nu}
        if any(len(s) != 2 for s in sub.values()): bad_v += 1; continue
        # connected?
        s0 = next(iter(Nu)); seen = {s0}; st = [s0]
        while st:
            a = st.pop()
            for b in sub[a]:
                if b not in seen: seen.add(b); st.append(b)
        if len(seen) != len(Nu): bad_v += 1
    nT = sum(tri[e] for e in Eh) // 3
    return dict(n=n, m=len(E), excess=len(Eh) - (3 * n - 11), edges_not_2tri=bad_e, vertices_link_not_cycle=bad_v)


if __name__ == '__main__' and sys.argv[1] == 'general':
    path = sys.argv[2]; stride = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    which = sys.argv[4] if len(sys.argv) > 4 else 'cyc'
    TOT = Counter()
    for gi, (nm, rot) in enumerate(iter_graph_file(path)):
        if gi % stride: continue
        res = analyse_hole(rot, 0, tait=False, which=which, want_class=True, maxstates=200000)
        if res is None: print(nm, 'too big'); continue
        ls = local_surface_stats(rot, 0)
        cls = res.get('classes', {})
        frozen = [ci for ci, c in cls.items() if c['filled'] == 0]
        C = summarise(nm, res); v, t = cycle_law(res)
        filled_any = sum(1 for s in range(res['S']) if len(set(res['recs'][0:0] or [])) == 0) if False else None
        TOT.update(C); TOT['graphs'] += 1; TOT['frozen_classes'] += len(frozen); TOT['law_viol'] += v; TOT['law_steps'] += t
        Ns = Counter(r['N'] for r in res['recs']); P2s = Counter(r['P2'] for r in res['recs'])
        print(nm, 'S', res['S'], 'cycles', res['cycles'], 'classes', cls, 'frozen', len(frozen),
              '| A5vP weak', C['weak_ok'], '/', C['states'], 'strong', C['strong_ok'], 'inA', C['inA'],
              '| ntri', {k: v2 for k, v2 in C.items() if k.startswith('ntri')}, '| N', dict(Ns), 'P2', dict(P2s),
              '| law viol', v, '/', t, '| D1', sum(r['D1'] for r in res['recs']), 'D2', sum(r['D2'] for r in res['recs']),
              '| oddA,B,M', sum(r['oA'] for r in res['recs']), sum(r['oB'] for r in res['recs']), sum(r['oM'] for r in res['recs']),
              '|', ls, flush=True)
    print('TOTAL', dict(sorted(TOT.items())))


# Face-component lemma (any cellular embedding, integrable or not): let P2-face-components be the
# components of the primal (faces of the cubic embedding) under adjacency across colour-2 dual edges.
# Lemma: if comp(x_{j+2}) is neither comp(x_j) nor comp(x_{j+1}), then the far end of f_k is not on Y.
def face_lemma_check(rot, h, C):
    TS = TaitSide(rot, h)
    P = TS.ax.pms(limit=300000)
    X = rot[h]
    for M in P:
        d = TS.ax.dl(M)
        if d is None: continue
        C['dlgood'] += 1
        a5 = fig8_axioms(TS.ax, M, d)['v_into_X']
        k = d[0]; j = (k - 2) % 5
        x = [X[(j + t) % 5] for t in range(5)]
        par = {}
        def f(a):
            par.setdefault(a, a)
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        for e in M:
            u, w = TS.td.prim[e]; a, b = f(u), f(w)
            if a != b: par[a] = b
        c2 = f(x[2]); hyp = c2 not in (f(x[0]), f(x[1]))
        colr = tait_colouring_from_M(TS, M, d)
        cint = integrate(TS, colr, rot, h, x[0]); integ = cint is not None
        C['int' if integ else 'nonint'] += 1
        if integ:
            al, A = cint[x[0]], cint[x[3]]
            seen = {x[2]}; st = [x[2]]
            adjp = {}
            for (u, w) in TS.td.prim:
                adjp.setdefault(u, []).append(w); adjp.setdefault(w, []).append(u)
            while st:
                u = st.pop()
                for w in adjp[u]:
                    if w not in seen and cint[w] in (al, A): seen.add(w); st.append(w)
            inA = x[0] in seen
            C['int_inA=%d_A5v=%s' % (inA, 'ok' if a5 else 'FAIL')] += 1
        C['hyp=%d_A5v=%s' % (hyp, 'ok' if a5 else 'FAIL')] += 1
        if not a5:
            C['FAIL_c2=c0'] += f(x[2]) == f(x[0]); C['FAIL_c2=c1'] += f(x[2]) == f(x[1])


if __name__ == '__main__' and sys.argv[1] == 'facelemma':
    path, stride = sys.argv[2], int(sys.argv[3])
    C = Counter(); ng = 0
    for gi, (nm, rot) in enumerate(iter_graph_file(path)):
        if gi % stride: continue
        ng += 1
        for h in range(len(rot)):
            if len(rot[h]) != 5: continue
            C['holes'] += 1
            face_lemma_check(rot, h, C)
    print('facelemma', path.split('/')[-1], 'graphs', ng, dict(sorted(C.items())))
