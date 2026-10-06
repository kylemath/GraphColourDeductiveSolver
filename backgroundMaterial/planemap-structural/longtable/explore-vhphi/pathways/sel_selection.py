"""[exploratory] Long Table, 6 Oct 2026: selection-side kill tests for R* (see
SolvingFrameworkPlan/docs/working/creative-intel-2026-10-05/selection-sketches.md).

Modes (run from any cwd):
  census            selection statistics per graph (H / HP holes, holes with all link degrees <= 6,
                    min number of big neighbours); builds and checks the n-gonal stacks S(n,r).  < 1 s.
  certmin           per-graph min / max hole radius from Studio-intel certificate meta files.   < 1 s.
  stack N R         S(N,R): all degree-5 holes: max Kempe radius, number of Kempe classes,
                    number of targetless classes (a targetless class kills R* for the whole graph,
                    since all degree-5 vertices of S(N,R) are equivalent).                      Studio.
  rho GRAPH         same per-hole computation for a named graph (T4, A3, A4, A5, pentakis, sixring28).
  pair GRAPH [all]  two-hole statement J2 on 5-x-y-5 diamond pairs (u, v degree 5, non-adjacent,
                    two adjacent common neighbours): classes of T-{u,v}; does every class contain a
                    state with BOTH links <= 3 colours?  Also counts 'double-DL' classes (no state
                    with either link <= 3).  Default: one pair per graph; 'all' = every pair.  Studio.

State = canonical 4-colouring (first occurrence) of the graph minus the hole(s); moves = whole
two-colour component swaps (singletons allowed), as in pb_lib.  Stdlib only.
"""
import sys, os, json, glob, itertools
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *(['..'] * 5)))
sys.path.insert(0, HERE)
from pb_lib import T4F, from_faces, colourings, comps, swap, canon, key  # noqa: E402

sys.path.insert(0, os.path.join(ROOT, 'SolvingFrameworkPlan/docs/working/MathVacancyDRed'))
import graphs as MG  # noqa: E402  (Math's A(r), pentakis face lists)


def stack(n, r):
    """S(n,r): r stacked n-gonal antiprism rings capped by two poles of degree n (order n*r+2).
    S(5,r) = A_r; S(n,2) = belt G_n (holes (5,5,5,5,n), Theorem HP)."""
    N, S = 0, n * r + 1
    R = lambda i, t: 1 + n * (i - 1) + (t % n)
    F = []
    for t in range(n):
        F.append((N, R(1, t), R(1, t + 1)))
        F.append((S, R(r, t), R(r, t + 1)))
        for i in range(1, r):
            F.append((R(i, t), R(i, t + 1), R(i + 1, t)))
            F.append((R(i + 1, t), R(i + 1, t + 1), R(i, t + 1)))
    return F


def sixring28():
    txt = open(os.path.join(ROOT, 'docs/66666/build_data.py')).read()
    txt = txt.split('FACES_TXT = """')[1].split('"""')[0]
    return [tuple(map(int, f.split())) for f in txt.split(',')]


def named(name):
    if name == 'T4': return [tuple(f) for f in T4F]
    if name in ('A3', 'A4', 'A5'): return MG.A(int(name[1]))
    if name == 'pentakis': return MG.pentakis()
    if name == 'sixring28': return sixring28()
    if name.startswith('S'):  # S7_3 style
        n, r = name[1:].split('_'); return stack(int(n), int(r))
    raise SystemExit('unknown graph ' + name)


def check_tri(F):
    adj = from_faces(F)
    V = len(adj); E = sum(len(s) for s in adj.values()) // 2
    fs = {frozenset(f) for f in F}
    sep = [t for t in itertools.combinations(sorted(adj), 3)
           if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]] and frozenset(t) not in fs]
    return adj, (V - E + len(F) == 2), min(len(s) for s in adj.values()), len(sep)


def census_line(name, F):
    adj, euler, mind, nsep = check_tri(F)
    deg = {v: len(adj[v]) for v in adj}
    d5 = [v for v in adj if deg[v] == 5]
    nb5 = {v: sum(deg[w] == 5 for w in adj[v]) for v in d5}
    H = sum(nb5[v] == 5 for v in d5); HP = sum(nb5[v] == 4 for v in d5)
    light = sum(max(deg[w] for w in adj[v]) <= 6 for v in d5)
    minbig = min(5 - nb5[v] for v in d5)
    print(f"{name:14s} n={len(adj):2d} euler={euler} mindeg={mind} sep3={nsep} #deg5={len(d5):2d} "
          f"H={H} HP={HP} all-link<=6={light:2d} min#big-nbrs={minbig} "
          f"selection-covered-by-H/HP={'yes' if H + HP else 'NO'}")


def classes(adj, holes):
    """Kempe classes of adj minus holes. returns states(dict key->col), nbrs, comp id per key."""
    a2 = {u: {w for w in adj[u] if w not in holes[1:]} for u in adj if u not in holes[1:]}
    h = holes[0]
    st = {key(c): c for c in (canon(c) for c in colourings(a2, h))}
    nb = {}
    for k, c in st.items():
        nb[k] = list({key(canon(swap(c, x, y, K))) for x, y, K in comps(a2, c, h)})
    cid = {}
    for k in st:
        if k in cid: continue
        cid[k] = k; q = [k]
        while q:
            u = q.pop()
            for w in nb[u]:
                if w not in cid: cid[w] = k; q.append(w)
    return st, nb, cid


def hole_report(adj, h):
    st, nb, cid = classes(adj, [h])
    filled = lambda c: len({c[w] for w in adj[h]}) <= 3
    dist = {k: 0 for k, c in st.items() if filled(c)}
    dq = deque(dist)
    while dq:
        k = dq.popleft()
        for w in nb[k]:
            if w not in dist: dist[w] = dist[k] + 1; dq.append(w)
    cls = set(cid.values()); good = {cid[k] for k in dist}
    return len(st), len(cls), len(cls - good), (max(dist.values()) if dist else None)


def run_rho(name, F, only_one=False):
    adj = from_faces(F)
    holes = [v for v in sorted(adj) if len(adj[v]) == 5]
    if only_one: holes = holes[:1]
    for h in holes:
        ns, nc, tl, rho = hole_report(adj, h)
        link = sorted(len(adj[w]) for w in adj[h])
        print(f"{name} hole {h} link {link}: states {ns} classes {nc} TARGETLESS {tl} max-radius {rho}",
              flush=True)


def diamond_pairs(adj):
    d5 = [v for v in adj if len(adj[v]) == 5]
    out = []
    for u, v in itertools.combinations(sorted(d5), 2):
        if v in adj[u]: continue
        c = adj[u] & adj[v]
        if any(y in adj[x] for x, y in itertools.combinations(c, 2)): out.append((u, v))
    return out


def run_pair(name, F, allp=False):
    adj = from_faces(F)
    prs = diamond_pairs(adj)
    if not allp: prs = prs[:1]
    for u, v in prs:
        st, nb, cid = classes(adj, [u, v])
        fu = lambda c: len({c[w] for w in adj[u]}) <= 3
        fv = lambda c: len({c[w] for w in adj[v]}) <= 3
        cls = {}
        for k, c in st.items():
            f = cls.setdefault(cid[k], [0, 0, 0])
            a, b = fu(c), fv(c)
            f[0] |= a and b; f[1] |= a; f[2] |= b
        nfail = sum(1 for f in cls.values() if not f[0])
        ndd = sum(1 for f in cls.values() if not (f[1] or f[2]))
        print(f"{name} pair ({u},{v}) degs u-link {sorted(len(adj[w]) for w in adj[u])} "
              f"v-link {sorted(len(adj[w]) for w in adj[v])}: states {len(st)} classes {len(cls)} "
              f"J2-FAIL classes {nfail} double-DL classes {ndd}", flush=True)


def certmin():
    base = os.path.join(ROOT, 'backgroundMaterial/planemap-structural/studiointel')
    for m in sorted(glob.glob(base + '/run-[CD]-2026-10-06/cert/*.meta.json')):
        tag = os.path.basename(m).split('.')[0]
        rho = json.load(open(m))['rho']
        F = json.load(open(m.replace('.meta.', '.graph.')))['faces']
        adj = from_faces([tuple(f) for f in F])
        hp = sum(1 for v in adj if len(adj[v]) == 5 and sum(len(adj[w]) == 5 for w in adj[v]) >= 4)
        print(f"{tag} holes {len(rho)} min-rho {min(rho.values())} max-rho {max(rho.values())} H/HP-holes {hp}")


if __name__ == '__main__':
    a = sys.argv[1:] or ['census']
    if a[0] == 'census':
        for nm in ['T4', 'A3', 'A4', 'A5', 'pentakis', 'sixring28']:
            census_line(nm, named(nm))
        for n in (5, 6, 7, 8, 9, 12):
            for r in (2, 3, 4):
                census_line(f"S{n}_{r}", stack(n, r))
    elif a[0] == 'certmin':
        certmin()
    elif a[0] == 'stack':
        run_rho(f"S{a[1]}_{a[2]}", stack(int(a[1]), int(a[2])), only_one=('one' in a))
    elif a[0] == 'rho':
        run_rho(a[1], named(a[1]))
    elif a[0] == 'pair':
        run_pair(a[1], named(a[1]), allp=('all' in a))
